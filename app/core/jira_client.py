from typing import Union

from jira import JIRA, Issue
from jira.resources import Version

from app.core.exceptions import BadRequest
from app.core.model.jira_fields import PriorityField, CustomStringField, JiraField
from app.core.utils import parse_next_version_name, get_current_date_text, get_logger
from app.model.jira import JiraAuthDto, CreateVersionTypeEnum

log = get_logger()


class JiraClient:
    def __init__(self, auth: JiraAuthDto):
        self.jira_url = auth.jira_url
        self.jira_username = auth.jira_username
        self.jira_token = auth.jira_token
        self.jira_project = auth.jira_project
        self.jira = self.get_jira_client()

    def get_jira_client(self):
        return JIRA(server=self.jira_url, basic_auth=(self.jira_username, self.jira_token))

    @classmethod
    def get_available_fields(cls) -> dict:
        return {
            "priority": PriorityField(),
            "target-start": CustomStringField("customfield_10022"),
            "target-end": CustomStringField("customfield_10023"),
        }

    def _get_available_field_klass(self, field_name) -> JiraField:
        field_klass = self.get_available_fields().get(field_name)
        if field_klass is None:
            raise BadRequest(f"field klass is not exist, {field_name}")
        return field_klass

    def find_issue(self, issue_id: str) -> Issue:
        """

        :param issue_id:
        :type issue_id:
        :return:
        :rtype:
        """
        try:
            return self.jira.issue(issue_id)
        except ValueError:
            raise BadRequest(f"can not find issue:{issue_id}")

    def add_comment(self, issue_id: str, comment: str) -> bool:
        """

        :param issue_id:
        :type issue_id:
        :param comment:
        :type comment:
        :return:
        :rtype:
        """
        issue = self.find_issue(issue_id)
        self.jira.add_comment(issue, comment)
        return True

    def get_field_value_by_name(self, issue_id: str, field_name: str) -> str:
        """

        :param issue_id:
        :type issue_id:
        :param field_name:
        :type field_name:
        :return:
        :rtype:
        """
        issue = self.find_issue(issue_id)
        field_klass = self._get_available_field_klass(field_name)
        value = field_klass.get_value(issue.fields)
        log.debug(f"{issue_id}, {field_name}, {value}")
        return value

    def get_versions(self) -> [Version]:
        """

        :return:
        :rtype:
        """
        return self.jira.project_versions(self.jira_project)

    def is_exists_version_by_name(self, version_name: str) -> bool:
        """

        :param version_name:
        :type version_name:
        :return:
        :rtype:
        """
        return self.jira.get_project_version_by_name(version_name) is not None

    def generate_next_version_name(
        self, version_type: CreateVersionTypeEnum, version_name_prefix: str
    ) -> Union[str | None]:
        """

        :param version_type:
        :type version_type:
        :param version_name_prefix:
        :type version_name_prefix:
        :return:
        :rtype:
        """
        versions = self.get_versions()
        matched_version_names = sorted(
            [
                (version.name, version.releaseDate)
                for version in versions
                if version.released and version.name.startswith(version_name_prefix)
            ],
            key=lambda x: x[1],
        )
        if len(matched_version_names) == 0:
            return None

        next_version_name = parse_next_version_name(version_type, version_name_prefix, matched_version_names[-1][0])
        log.debug(f"generate_next_version_name, {next_version_name}")
        return next_version_name

    def create_version(
        self,
        version_type: CreateVersionTypeEnum,
        version_name_prefix: str,
        version_name: str,
    ) -> bool:
        """

        :param version_type:
        :type version_type:
        :param version_name_prefix:
        :type version_name_prefix:
        :param version_name:
        :type version_name:
        :return:
        :rtype:
        """
        next_version_name = self.generate_next_version_name(version_type, version_name_prefix)
        next_version_name = next_version_name if next_version_name else version_name
        if self.is_exists_version_by_name(next_version_name):
            log.warn(f"{next_version_name} is exits")
            return False

        self.jira.create_version(
            name=next_version_name,
            project=self.jira_project,
            description="Created by Jira Action",
            startDate=get_current_date_text(),
        )
        log.info(f"{next_version_name} is created")
        return True

    def release_version(self, version_name: str) -> bool:
        """

        :param version_name:
        :type version_name:
        :return:
        :rtype:
        """
        version = self.jira.get_project_version_by_name(version_name)
        if version is None:
            log.warn(f"{version_name} is not exists")
            raise BadRequest(f"version is not exists, {version_name}")

        version.update(released=True, releaseDate=get_current_date_text())
        log.info(f"{version_name} is released")
        return True
