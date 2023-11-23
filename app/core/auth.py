from typing import Optional

from fastapi.security import APIKeyHeader
from starlette.requests import Request

from app.core.exceptions import Forbidden
from app.core.setting import get_cached_settings


class CustomAPIKeyHeader(APIKeyHeader):
    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)
        if not api_key or api_key != get_cached_settings().api_key:
            raise Forbidden()
        return api_key


api_key_header = CustomAPIKeyHeader(name="x-api-key")
