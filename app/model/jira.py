from pydantic import BaseModel, Field


class CreateIssueCommentRequest(BaseModel):
    comment: str = Field(title="코멘트", examples=["Updated by Jira Action"])


class JiraAuth(BaseModel):
    jira_url: str = Field(title="Jira URL", examples=["https://dev.atlassian.net/"], max_length=100)
    jira_project: str = Field(title="Jira Project", examples=["TJP"], max_length=3)
    jira_username: str = Field(title="Jira Username", examples=["user@dev.com"], max_length=100)
    jira_token: str = Field(title="Jira Token", examples=["secret_api_token"])


class CreateVersionReqeust(BaseModel):
    version_name_prefix: str = Field(title="버전 접두사", examples=["BE-ADMIN-TEST"])
    version_name: str = Field(title="버전명", description="버전 접두사와 일치하는게 없을 경우 사용 됩니다.", examples=["BE-ADMIN-TEST-4.0.x"])


class UpdateVersionReqeust(BaseModel):
    version_name: str = Field(title="버전명", examples=["BE-ADMIN-TEST-4.0.x"])
