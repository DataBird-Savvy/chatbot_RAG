
from langgraph.graph import StateGraph, END
from agentapp.processing.graph_nodes import research_node, summarize_node, critic_node, writer_node
from agentapp.core.state import ResearchState
from agentapp.exception import MultiAgentException
from agentapp.logger import logging

def build_langgraph():
    logging.info("Orchestrator: Initializing LangGraph construction...")

    try:
        sg = StateGraph(state_schema=ResearchState)
        logging.info("Orchestrator: Created StateGraph with schema.")

        # Adding nodes
        sg.add_node("research", research_node)
        logging.info("Orchestrator: Added 'research' node.")
        
        sg.add_node("summarize", summarize_node)
        logging.info("Orchestrator: Added 'summarize' node.")
        
        sg.add_node("critic", critic_node)
        logging.info("Orchestrator: Added 'critic' node.")
        
        sg.add_node("writer", writer_node)
        logging.info("Orchestrator: Added 'writer' node.")

        # Define flow
        sg.set_entry_point("research")
        logging.info("Orchestrator: Set entry point to 'research'.")

        sg.add_edge("research", "summarize")
        sg.add_edge("summarize", "critic")
        sg.add_edge("critic", "writer")
        logging.info("Orchestrator: Defined node transitions.")

        sg.set_finish_point("writer")
        logging.info("Orchestrator: Set finish point to 'writer'.")

        compiled_graph = sg.compile()
        logging.info("Orchestrator: LangGraph compiled successfully.")
        return compiled_graph

    except Exception as e:
        logging.error(f"Orchestrator: Failed to build LangGraph: {e}")
        raise MultiAgentException(f"LangGraph construction error: {e}")
