from enum import Enum

from pydantic import BaseModel, Field


class JiraAuthDto(BaseModel):
    jira_url: str = Field(title="Jira URL", examples=["https://dev.atlassian.net/"], max_length=100)
    jira_project: str = Field(title="Jira Project", examples=["TJP"], max_length=3)
    jira_username: str = Field(title="Jira Username", examples=["user@dev.com"], max_length=100)
    jira_token: str = Field(title="Jira Token", examples=["secret_api_token"])


class CreateIssueCommentRequestDto(BaseModel):
    comment: str = Field(title="코멘트", examples=["Updated by Jira Action"])


class VersionSearchDto(BaseModel):
    is_released: bool = Field(title="버전 릴리즈 여부", examples=[False], default=False)
    is_archived: bool = Field(title="버전 아카이브 여부", examples=[False], default=False)
    version_name: str = Field(title="버전명 (contain)", examples=["BE-MALL-"], default="")


class CreateVersionTypeEnum(Enum):
    major = "major"
    minor = "minor"
    patch = "patch"


class CreateVersionReqeustDto(BaseModel):
    version_type: CreateVersionTypeEnum = Field(title="버전 생성 유형")
    version_name_prefix: str = Field(title="버전 접두사", examples=["BE-ADMIN-TEST"])
    version_name: str | None = Field(
        title="버전명 (이걸로 생성하고 싶을 때)",
        description="버전 접두사와 일치하는게 없을 경우 사용 됩니다.",
        examples=["BE-ADMIN-TEST-4.0.x"],
        default=None,
    )


class UpdateVersionReqeustDto(BaseModel):
    version_name: str = Field(title="버전명", examples=["BE-ADMIN-TEST-4.0.x"])
