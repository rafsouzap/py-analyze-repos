from dataclasses import dataclass, field
from typing import List

@dataclass
class Stats:
    additions: int
    deletions: int
    total: int

@dataclass
class Commit:
    id: str
    title: str
    stats: Stats

@dataclass
class MergeRequest:
    id: int
    project_id: int
    title: str
    state: str
    merge_commit_sha: str
    reference: str
    created_at: str
    merged_at: str
    prepared_at: str
    commit: Commit

@dataclass
class User:
    user_id: int
    user_name: str
    merge_request: List[MergeRequest] = field(default_factory=list)