from __future__ import annotations
import logging
from typing import Iterable
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_LOG = logging.getLogger(__name__)

# Sensitive headers that will be redacted in logs
_SENSITIVE = {"AppApiToken", "Cookie", "Authorization"}


def _redact_headers(headers: dict[str, str] | None) -> dict[str, str] | None:
    if not headers:
        return headers
    redacted: dict[str, str] = {}
    for k, v in headers.items():
        redacted[k] = "<redacted>" if k in _SENSITIVE and v else v
    return redacted


def build_session(*, retries: int = 3, backoff_factor: float = 0.5,
                  status_forcelist: Iterable[int] = (429, 500, 502, 503, 504)) -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=retries,
        connect=retries,
        read=retries,
        backoff_factor=backoff_factor,
        status_forcelist=tuple(status_forcelist),
        allowed_methods={"GET", "POST", "PUT", "PATCH", "DELETE"},
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def log_request(method: str, url: str, *, headers: dict[str, str] | None, params, json):
    if _LOG.isEnabledFor(logging.DEBUG):
        _LOG.debug("→ %s %s headers=%s params=%s json=%s",
                   method, url, _redact_headers(headers), params, json)


def log_response(resp: requests.Response):
    if _LOG.isEnabledFor(logging.DEBUG):
        try:
            body = resp.json()
        except Exception:
            body = resp.text[:500]
        _LOG.debug("← %s %s %s", resp.status_code, resp.url, body)
