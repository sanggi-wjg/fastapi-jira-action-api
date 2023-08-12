import logging
import re
from datetime import datetime
from functools import lru_cache
from typing import Union

from app.core.setting import get_cached_settings


def parse_next_version_name(prefix: str, latest_version_name: str) -> Union[str | None]:
    """

    :param prefix:
    :type prefix:
    :param latest_version_name:
    :type latest_version_name:
    :return:
    :rtype:
    """
    match = re.search(r'(\d+\.\d+\.\d+)$', latest_version_name)
    if match:
        current_version = match.group(1)
        major, minor, patch = map(int, current_version.split('.'))
        next_version = f"{major}.{minor}.{patch + 1}"
        return f"{prefix}-{next_version}"
    else:
        return None


def get_current_date_text() -> str:
    return datetime.now().strftime("%Y-%m-%d")


@lru_cache
def get_logger():
    settings = get_cached_settings()

    formatter = logging.Formatter("[%(levelname)s]\t %(asctime)s\t %(pathname)s:%(lineno)d\t\t %(message)s", datefmt="%Y-%m-%d %I:%M:%S")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger("jira-action")
    logger.setLevel(logging.DEBUG if settings.debug else logging.WARN)
    logger.addHandler(stream_handler)
    return logger
