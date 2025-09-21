from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import requests

from .device import DeviceProfile
from .exceptions import ApiError, NetworkError, SerializationError
from .models import Location, SearchHintsResponse, ProductCard
from ._http import build_session, log_request, log_response

_LOG = logging.getLogger(__name__)


@dataclass(slots=True)
class ClientConfig:
    base_url: str = "https://app.tabletki.ua/api/app/v1"
    # seconds; can be (connect, read)
    timeout: float | tuple[float, float] = 15.0
    retries: int = 3
    backoff_factor: float = 0.5
    status_forcelist: tuple[int, ...] = (429, 500, 502, 503, 504)


class TabletkiUA:
    """Typed, robust client for app.tabletki.ua API.

    Usage::

        from tabletkiua import TabletkiUA, DeviceProfile

        client = TabletkiUA(
            app_api_token="YOUR_TOKEN",
            identity=DeviceProfile.generate(lang="uk"),
        )
        with client:
            loc = client.location_by_ip()
            res = client.search_hints_v2("4820142437368")
            card = client.product_card(name="...", goods_int_code=1025098)
    """

    def __init__(
        self,
        app_api_token: str,
        *,
        identity: Optional[DeviceProfile] = None,
        config: Optional[ClientConfig] = None,
        session: Optional[requests.Session] = None,
        cookies: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
    ) -> None:
        self._app_api_token = app_api_token
        self.identity = identity or DeviceProfile.generate()
        self.config = config or ClientConfig()

        self.session = session or build_session(
            retries=self.config.retries,
            backoff_factor=self.config.backoff_factor,
            status_forcelist=self.config.status_forcelist,
        )
        if proxies:
            self.session.proxies.update(proxies)
        if cookies:
            self.session.cookies.update(cookies)

        # Normalize timeout
        self._timeout = self.config.timeout

    # ---- Context manager ----
    def __enter__(self) -> "TabletkiUA":  # pragma: no cover
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # pragma: no cover
        self.close()

    def close(self) -> None:
        try:
            self.session.close()
        except Exception:
            pass

    # ---- Internal request helper ----
    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        base_headers = self.identity.headers(self._app_api_token)

        # Only attach Location if non-empty and not overridden
        if self.identity.location_header and (not headers or "Location" not in headers):
            base_headers["Location"] = self.identity.location_header

        if headers:
            base_headers.update(headers)

        # Logging (with redaction)
        log_request(method, url, headers=base_headers,
                    params=params, json=json)

        try:
            resp = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json,
                headers=base_headers,
                timeout=self._timeout,
                verify=True,
            )
        except requests.RequestException as e:  # networking/timeouts
            raise NetworkError(str(e)) from e

        log_response(resp)

        # Raise for non-2xx with detail
        if not (200 <= resp.status_code < 300):
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text[:500]
            raise ApiError(
                f"HTTP {resp.status_code}",
                status_code=resp.status_code,
                url=resp.url,
                payload=detail,
            )

        # Expect JSON body
        try:
            return resp.json()
        except ValueError as e:
            # Non-JSON or invalid JSON
            raise SerializationError(f"Invalid JSON from {resp.url}") from e

    # ---- Public API methods ----

    def location_by_ip(self, *, store: bool = True) -> Location:
        """GET /Locations/locationByIp — determine location by caller IP.

        If ``store=True`` (default), saves ``identity.location_header = loc.id``.
        """
        data = self._request("GET", "Locations/locationByIp")
        loc = Location.from_dict(data)
        if store:
            self.identity.location_header = loc.id
        return loc

    def search_hints_v2(
        self,
        term: str,
        *,
        transliterate: int | bool = 0,
        type: str = "DEFAULT",
        location: Optional[str] = None,
    ) -> SearchHintsResponse:
        """POST /Search/searchHintsV2.

        If ``location`` provided, it's sent as the ``Location`` header.
        Otherwise, header is omitted if no saved location.
        """
        payload = {
            "term": term,
            "transliterate": 1 if str(transliterate) in {"1", "True", "true"} else 0,
            "type": type,
        }
        extra_headers = {"Location": location} if location else None
        data = self._request("POST", "Search/searchHintsV2",
                             json=payload, headers=extra_headers)
        return SearchHintsResponse.from_dict(data)

    def product_card(
        self,
        *,
        name: str,
        goods_int_code: str | int,
        with_content_plus: bool = True,
    ) -> ProductCard:
        """GET /ProductCard/card?name=...&id=...&withContentPlus=true"""
        params = {
            "name": name,
            "id": str(goods_int_code),
            "withContentPlus": "true" if with_content_plus else "false",
        }
        data = self._request("GET", "ProductCard/card", params=params)
        return ProductCard.from_dict(data)
