from __future__ import annotations
from typing import Any, Optional


class ApiError(Exception):

    """Server returned a non-2xx response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        url: str | None = None,
        payload: Any | None = None,
    ) -> None:

        super().__init__(message)
        self.status_code = status_code
        self.url = url
        self.payload = payload

    def __str__(self) -> str:  # pragma: no cover

        base = super().__str__()
        parts = []
        if self.status_code is not None:
            parts.append(f"status={self.status_code}")
        if self.url:
            parts.append(f"url={self.url}")
        if parts:
            base = f"{base} ({', '.join(parts)})"
        return base


class NetworkError(Exception):

    """Networking, DNS, connection, or timeout issues."""


class SerializationError(Exception):

    """Invalid or unexpected response format (e.g., non-JSON)."""
