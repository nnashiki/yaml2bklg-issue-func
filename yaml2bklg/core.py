import dataclasses


@dataclasses.dataclass
class BacklogIssueAddReq:
    projectId: int
    summary: str
    description: str
    issueTypeId: int
    priorityId: int = 3

