import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse, PlainTextResponse

from app.core.auth import api_key_header
from app.core.jira_sdk.jira_client import JiraClient
from app.api.model.jira import (
    CreateIssueCommentRequestDto,
    JiraAuthDto,
    CreateVersionReqeustDto,
    UpdateVersionReqeustDto,
    VersionSearchDto,
)

router = APIRouter(tags=["Jira"])
logger = logging.getLogger(__file__)


@router.post(
    "/jira/issues/{issue_id}/comments",
    status_code=status.HTTP_201_CREATED,
    summary="지라 이슈 댓글 생성",
    response_class=PlainTextResponse,
)
async def create_jira_issue_comment(
    token: Annotated[str, Depends(api_key_header)],
    jira_auth: JiraAuthDto,
    issue_id: str,
    create_issue_comment_request: CreateIssueCommentRequestDto,
):
    JiraClient(jira_auth).add_comment(issue_id, create_issue_comment_request.comment)
    return PlainTextResponse(status_code=status.HTTP_201_CREATED, content="Success")


@router.post(
    "/jira/issues/{issue_id}/fields/list",
    status_code=status.HTTP_200_OK,
    summary="지라 이슈 필드 네임 리스트 조회",
)
async def get_jira_available_issue_fields(token: Annotated[str, Depends(api_key_header)]):
    fields = [k for k, v in JiraClient.get_available_fields().items()]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(fields),
    )


@router.post(
    "/jira/issues/{issue_id}/fields/{field_name}/one",
    status_code=status.HTTP_200_OK,
    summary="지라 이슈 필드 값 조회",
    response_class=PlainTextResponse,
)
async def get_jira_issue_field_value_by_name(
    token: Annotated[str, Depends(api_key_header)],
    jira_auth: JiraAuthDto,
    issue_id: str,
    field_name: str,
):
    value = JiraClient(jira_auth).get_field_value_by_name(issue_id, field_name)
    return PlainTextResponse(status_code=status.HTTP_200_OK, content=value)


@router.post(
    "/jira/versions/list",
    status_code=status.HTTP_200_OK,
    summary="지라 릴리즈 버전들 가져오기",
)
async def get_jira_versions(
    token: Annotated[str, Depends(api_key_header)],
    jira_auth: JiraAuthDto,
    version_search_dto: VersionSearchDto,
):
    versions = JiraClient(jira_auth).get_versions(version_search_dto)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder([version.name for version in versions]),
    )


@router.post(
    "/jira/versions/",
    status_code=status.HTTP_201_CREATED,
    summary="지라 릴리즈 버전 생성",
    response_class=PlainTextResponse,
)
async def create_jira_version(
    token: Annotated[str, Depends(api_key_header)],
    jira_auth: JiraAuthDto,
    create_version_request: CreateVersionReqeustDto,
):
    JiraClient(jira_auth).create_version(
        create_version_request.version_type,
        create_version_request.version_name_prefix,
        create_version_request.version_name,
    )
    return PlainTextResponse(status_code=status.HTTP_201_CREATED, content="Success")


@router.put(
    "/jira/versions/release",
    status_code=status.HTTP_200_OK,
    summary="지라 릴리즈 버전 릴리즈 상태로 변경",
    response_class=PlainTextResponse,
)
async def release_jira_version(
    token: Annotated[str, Depends(api_key_header)],
    jira_auth: JiraAuthDto,
    update_version_request: UpdateVersionReqeustDto,
):
    JiraClient(jira_auth).release_version(update_version_request.version_name)
    return PlainTextResponse(status_code=status.HTTP_200_OK, content="Success")
