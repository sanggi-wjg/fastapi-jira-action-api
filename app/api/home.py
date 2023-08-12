from fastapi import APIRouter
from starlette import status
from starlette.responses import PlainTextResponse

from app.core.utils import get_logger

router = APIRouter(tags=["Home"])
log = get_logger()


@router.get("/ping", status_code=status.HTTP_200_OK, summary="Ping Pong", response_class=PlainTextResponse)
async def ping():
    log.debug("pong")
    return PlainTextResponse(status_code=status.HTTP_200_OK, content="pong")
