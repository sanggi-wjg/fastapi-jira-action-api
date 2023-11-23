import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jira.exceptions import JIRAError

from app.api import home, jira
from app.core.exceptions import (
    BadRequest,
    validation_error_handler,
    bad_request_handler,
    Forbidden,
    forbidden_handler,
    jira_error_handler,
)
from app.core.setting import get_cached_settings

settings = get_cached_settings()


def create_app():
    a = FastAPI(
        title=settings.title,
        description=settings.description,
        debug=settings.debug,
    )

    # API Router
    a.include_router(home.router)
    a.include_router(jira.router)

    # Exception Handler
    a.add_exception_handler(BadRequest, bad_request_handler)
    a.add_exception_handler(Forbidden, forbidden_handler)
    a.add_exception_handler(JIRAError, jira_error_handler)
    a.add_exception_handler(RequestValidationError, validation_error_handler)

    return a


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        workers=settings.workers,
        use_colors=settings.use_colors,
    )
