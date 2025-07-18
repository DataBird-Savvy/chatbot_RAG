# graph_nodes.py

from agentapp.agents.research import ResearchAgent
from agentapp.agents.summarize import SummarizationAgent
from agentapp.agents.critic import CriticAgent
from agentapp.agents.writer import WriterAgent
from agentapp.core.state import ResearchState

def research_node(state: ResearchState) -> ResearchState:
    agent = ResearchAgent()
    papers = agent.fetch_documents(state["query"])
    state["documents"] = papers
    return state

def summarize_node(state: ResearchState) -> ResearchState:
    agent = SummarizationAgent()
    summaries = []
    for doc in state["documents"]:
        summaries.append(agent.summarize_document(doc["content"]))
    state["summaries"] = summaries
    return state

def critic_node(state: ResearchState) -> ResearchState:
    agent = CriticAgent()
    vetted = []
    for summary in state["summaries"]:
        vetted.append(agent.evaluate_summary(summary))
    state["vetted"] = vetted
    return state

def writer_node(state: ResearchState) -> ResearchState:
    agent = WriterAgent()
    state["report"] = agent.compile_report(state["vetted"])
    return state
