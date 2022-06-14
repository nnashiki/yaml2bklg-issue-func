import dataclasses


@dataclasses.dataclass
class BacklogIssueAddReq:
    projectId: int
    summary: str
    description: str
    issueTypeId: int
    priorityId: int = 3
    parentIssueId: int = None


def add_issues(parent_req: BacklogIssueAddReq, child_issues_req: list[BacklogIssueAddReq]):
    pass
