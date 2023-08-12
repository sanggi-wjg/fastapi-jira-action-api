import logging
import re
from datetime import datetime
from enum import Enum
from typing import Union

from jira import JIRA, Issue
from jira.resources import Version

from app.core.exception import BadRequest
from app.core.utils import parse_next_version_name, get_current_date_text
from app.model.jira import JiraAuth

logger = logging.getLogger(__file__)


class FieldType(Enum):
    PRIORITY = "PRIORITY"
    CUSTOM_FIELD = "CUSTOM_FIELD"
    CUSTOM_STRING_FIELD = "CUSTOM_STRING_FIELD"


class Field:
    field_type: FieldType
    name: str

    def get_value(self, fields: Issue._IssueFields) -> str:
        raise NotImplementedError


class PriorityField(Field):
    field_type = FieldType.PRIORITY
    name = "priority"

    def get_value(self, fields: Issue._IssueFields) -> str:
        priority = getattr(fields, self.name)
        return priority.name


class CustomField(Field):
    field_type = FieldType.CUSTOM_FIELD

    def get_value(self, fields: Issue._IssueFields) -> str:
        pass


class CustomStringField(Field):
    field_type = FieldType.CUSTOM_STRING_FIELD

    def __init__(self, name: str):
        self.name = name

    def get_value(self, fields: Issue._IssueFields) -> str:
        return getattr(fields, self.name)


class JiraClient:

    def __init__(self, auth: JiraAuth):
        self.jira = JIRA(
            server=auth.jira_url,
            basic_auth=(auth.jira_username, auth.jira_token)
        )
        self.jira_project = auth.jira_project

    @classmethod
    def get_available_fields(cls) -> dict:
        return {
            "priority": PriorityField(),
            "target-start": CustomStringField("customfield_10022"),
            "target-end": CustomStringField("customfield_10023"),
        }

    def _get_available_field_klass(self, field_name) -> Field:
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
        return field_klass.get_value(issue.fields)

    def get_versions(self) -> [Version]:
        """

        :return:
        :rtype:
        """
        return self.jira.project_versions(self.jira_project)

    def generate_next_version_name(self, version_name_prefix: str) -> Union[str | None]:
        """

        :param version_name_prefix:
        :type version_name_prefix:
        :return:
        :rtype:
        """
        versions = self.get_versions()
        matched_version_names = sorted([
            version.name for version in versions
            if version.name.startswith(version_name_prefix)
        ])
        if len(matched_version_names) == 0:
            return None
        return parse_next_version_name(version_name_prefix, matched_version_names[-1])

    def create_version(self, version_name_prefix: str, version_name: str) -> bool:
        """

        :param version_name_prefix:
        :type version_name_prefix:
        :param version_name:
        :type version_name:
        :return:
        :rtype:
        """
        next_version_name = self.generate_next_version_name(version_name_prefix)
        self.jira.create_version(
            name=next_version_name if next_version_name else version_name,
            project=self.jira_project,
            description="Created by Jira Action",
            startDate=get_current_date_text()
        )
        return True

    def release_version(self, version_name: str) -> bool:
        """

        :param version_name:
        :type version_name:
        :return:
        :rtype:
        """
        version: Version = self.jira.get_project_version_by_name(version_name)
        version.update(released=True, releaseDate=get_current_date_text())
        return True
