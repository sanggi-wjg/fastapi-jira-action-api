from enum import Enum

from jira import Issue


class JiraFieldType(Enum):
    PRIORITY = "PRIORITY"
    CUSTOM_FIELD = "CUSTOM_FIELD"
    CUSTOM_STRING_FIELD = "CUSTOM_STRING_FIELD"


class JiraField:
    field_type: JiraFieldType
    name: str

    def get_value(self, fields: Issue._IssueFields) -> str:
        raise NotImplementedError


class PriorityField(JiraField):
    field_type = JiraFieldType.PRIORITY
    name = "priority"

    def get_value(self, fields: Issue._IssueFields) -> str:
        priority = getattr(fields, self.name)
        return priority.name


class CustomField(JiraField):
    field_type = JiraFieldType.CUSTOM_FIELD

    def get_value(self, fields: Issue._IssueFields) -> str:
        pass


class CustomStringField(JiraField):
    field_type = JiraFieldType.CUSTOM_STRING_FIELD

    def __init__(self, name: str):
        self.name = name

    def get_value(self, fields: Issue._IssueFields) -> str:
        return getattr(fields, self.name)
