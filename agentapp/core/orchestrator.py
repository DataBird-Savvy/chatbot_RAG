# agentapp/processing/langgraph_builder.py

from langgraph.graph import StateGraph, END
from agentapp.processing.graph_nodes import GraphPipeline
from agentapp.core.state import ResearchState
from agentapp.exception import MultiAgentException
from agentapp.logger import logging


class LangGraphBuilder:
    def __init__(self):
        self.pipeline = GraphPipeline()

    def build(self):
        logging.info("Orchestrator: Initializing LangGraph construction...")

        try:
            sg = StateGraph(state_schema=ResearchState)
            logging.info("Orchestrator: Created StateGraph with schema.")

            # Add class methods as nodes
            sg.add_node("research", self.pipeline.research_node)
            sg.add_node("summarize", self.pipeline.summarize_node)
            sg.add_node("critic", self.pipeline.critic_node)
            sg.add_node("writer", self.pipeline.writer_node)
            logging.info("Orchestrator: Added all pipeline nodes.")

            # Define flow
            sg.set_entry_point("research")
            sg.add_edge("research", "summarize")
            sg.add_edge("summarize", "critic")
            sg.add_edge("critic", "writer")
            sg.set_finish_point("writer")
            logging.info("Orchestrator: Defined graph edges and finish point.")

            compiled_graph = sg.compile()
            logging.info("Orchestrator: LangGraph compiled successfully.")
            return compiled_graph

        except Exception as e:
            logging.error(f"Orchestrator: Failed to build LangGraph: {e}")
            raise MultiAgentException(f"LangGraph construction error: {e}")
