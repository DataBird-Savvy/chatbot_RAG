# agentapp/core/state.py

from typing import TypedDict, List, Optional

class ResearchState(TypedDict):
    query: str
    documents: Optional[List[dict]]
    summaries: Optional[List[str]]
    vetted: Optional[List[dict]]
    report: Optional[str]
