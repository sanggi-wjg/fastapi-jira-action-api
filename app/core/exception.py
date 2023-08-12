import logging

from jira.exceptions import JIRAError
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__file__)


class BadRequest(Exception):
    pass


class Forbidden(Exception):
    pass


async def bad_request_handler(request: Request, e: BadRequest):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": status.HTTP_400_BAD_REQUEST,
            "detail": f"Bad request, {e}"
        }
    )


async def forbidden_handler(request: Request, e: Forbidden):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "code": status.HTTP_403_FORBIDDEN,
            "detail": "Not authenticated"
        }
    )


async def jira_error_handler(request: Request, e: JIRAError):
    logger.error(f"[JIRA_ERROR] {request.url}\n {e.url}\n {e.text}\n {e.headers}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": status.HTTP_400_BAD_REQUEST,
            "detail": "Not authenticated"
        }
    )


async def validation_error_handler(request: Request, e: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": status.HTTP_400_BAD_REQUEST,
            "detail": f"{e.errors()}"
        }
    )
