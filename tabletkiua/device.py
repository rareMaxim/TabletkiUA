from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
import uuid


DEFAULT_UA = (
    "Dalvik/2.1.0 (Linux; U; Android 16; Pixel 8 Pro Build/BP41.250822.010)"
)


@dataclass(slots=True)
class DeviceProfile:

    """Encapsulates device/user identity headers required by the API."""

    adid: str
    device_id: str
    user_id: str
    user_agent: str = DEFAULT_UA
    device_os: str = "android"
    device_os_version: str = "36"
    app_version: str = "4.1.674"
    lang: str = "uk"
    is_new_user: bool = True
    location_header: str = ""

    @classmethod
    def generate(
        cls,
        *,
        user_agent: str = DEFAULT_UA,
        device_os: str = "android",
        device_os_version: str = "36",
        app_version: str = "4.1.674",
        lang: str = "uk",
        is_new_user: bool = True,
        location_header: str = "",
        adid: Optional[str] = None,
        device_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> "DeviceProfile":

        return cls(
            adid=adid or str(uuid.uuid4()),
            device_id=device_id or str(uuid.uuid4()),
            user_id=user_id or str(uuid.uuid4()),
            user_agent=user_agent,
            device_os=device_os,
            device_os_version=device_os_version,
            app_version=app_version,
            lang=lang,
            is_new_user=is_new_user,
            location_header=location_header,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeviceProfile":
        return cls(**data)

    def headers(self, app_api_token: str) -> Dict[str, str]:
        """Base headers used by all requests."""
        return {
            "adid": self.adid,
            "AppApiToken": app_api_token,
            "appVersion": self.app_version,
            "deviceID": self.device_id,
            "deviceOS": self.device_os,
            "deviceOSversion": self.device_os_version,
            "isNewUser": "1" if self.is_new_user else "0",
            "Lang": self.lang,
            # `Location` must NOT be sent if empty (caller decides)
            # We'll inject it in client only when non-empty.
            "User-Agent": self.user_agent,
            "UserID": self.user_id,
            # requests handles compression automatically; including it is harmless
            "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json",
        }
