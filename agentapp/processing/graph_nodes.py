# graph_nodes.py

from agentapp.agents.research import ResearchAgent
from agentapp.agents.summarize import SummarizationAgent
from agentapp.agents.critic import CriticAgent
from agentapp.agents.writer import WriterAgent
from agentapp.core.state import ResearchState

class GraphPipeline:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.summarization_agent = SummarizationAgent()
        self.critic_agent = CriticAgent()
        self.writer_agent = WriterAgent()

    def research_node(self, state: ResearchState) -> ResearchState:
        papers = self.research_agent.fetch_documents(state["query"])
        state["documents"] = papers
        return state

    def summarize_node(self, state: ResearchState) -> ResearchState:
        summaries = [self.summarization_agent.summarize_document(doc["content"])
                     for doc in state["documents"]]
        state["summaries"] = summaries
        return state

    def critic_node(self, state: ResearchState) -> ResearchState:
        vetted = [self.critic_agent.evaluate_summary(summary)
                  for summary in state["summaries"]]
        state["vetted"] = vetted
        return state

    def writer_node(self, state: ResearchState) -> ResearchState:
        state["report"] = self.writer_agent.compile_report(state["vetted"])
        return state
