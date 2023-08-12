import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse, PlainTextResponse

from app.core.auth import api_key_header
from app.core.jira_client import JiraClient
from app.model.jira import JiraAuth, CreateIssueCommentRequest, CreateVersionReqeust, UpdateVersionReqeust

router = APIRouter(tags=["Jira"])
logger = logging.getLogger(__file__)


@router.post(
    "/jira/issues/{issue_id}/comments",
    status_code=status.HTTP_201_CREATED,
    summary="지라 이슈 코멘트 생성",
    response_class=PlainTextResponse
)
async def create_jira_issue_comment(
        token: Annotated[str, Depends(api_key_header)],
        issue_id: str,
        issue_comment_request: CreateIssueCommentRequest,
        jira_auth: JiraAuth
):
    JiraClient(jira_auth).add_comment(issue_id, issue_comment_request.comment)
    return PlainTextResponse(
        status_code=status.HTTP_201_CREATED,
        content="Success"
    )


@router.get(
    "/jira/issues/{issue_id}/fields",
    status_code=status.HTTP_200_OK,
    summary="지라 이슈 필드 네임 리스트"
)
async def get_jira_available_issue_fields(
        token: Annotated[str, Depends(api_key_header)]
):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder([
            k for k, v in JiraClient.get_available_fields().items()
        ])
    )


@router.get(
    "/jira/issues/{issue_id}/fields/{field_name}",
    status_code=status.HTTP_200_OK,
    summary="지라 이슈 필드 값 가져오기",
    response_class=PlainTextResponse,
)
async def get_jira_issue_field_value_by_name(
        token: Annotated[str, Depends(api_key_header)],
        issue_id: str,
        field_name: str,
        jira_auth: JiraAuth
):
    value = JiraClient(jira_auth).get_field_value_by_name(issue_id, field_name)
    return PlainTextResponse(
        status_code=status.HTTP_200_OK,
        content=value
    )


@router.get(
    "/jira/versions/",
    status_code=status.HTTP_200_OK,
    summary="지라 버전들 가져오기",
)
async def get_jira_versions(
        token: Annotated[str, Depends(api_key_header)],
        version_request: CreateVersionReqeust,
        jira_auth: JiraAuth
):
    versions = JiraClient(jira_auth).get_versions()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder([
            version.name for version in versions
        ])
    )


@router.post(
    "/jira/versions/",
    status_code=status.HTTP_201_CREATED,
    summary="지라 버전 생성",
    response_class=PlainTextResponse,
)
async def create_jira_version(
        token: Annotated[str, Depends(api_key_header)],
        version_request: CreateVersionReqeust,
        jira_auth: JiraAuth
):
    JiraClient(jira_auth).create_version(version_request.version_name_prefix, version_request.version_name)
    return PlainTextResponse(
        status_code=status.HTTP_201_CREATED,
        content="Success"
    )


@router.put(
    "/jira/versions/release",
    status_code=status.HTTP_200_OK,
    summary="지라 버전 릴리즈",
    response_class=PlainTextResponse,
)
async def release_jira_version(
        token: Annotated[str, Depends(api_key_header)],
        version_request: UpdateVersionReqeust,
        jira_auth: JiraAuth
):
    JiraClient(jira_auth).release_version(version_request.version_name)
    return PlainTextResponse(
        status_code=status.HTTP_200_OK,
        content="Success"
    )
