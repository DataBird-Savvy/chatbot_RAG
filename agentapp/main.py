# main.py

from agentapp.core.orchestrator import build_langgraph
from agentapp.logger import logging
from agentapp.exception import MultiAgentException

def main():
    logging.info("Main: Starting LangGraph orchestration...")

    try:
        graph = build_langgraph()
        logging.info("Main: LangGraph built successfully.")

        initial_state = {"query": "AI in healthcare"}
        logging.info(f"Main: Initial state: {initial_state}")

        final_state = graph.invoke(initial_state)
        logging.info("Main: LangGraph execution completed.")

        print("\n=== FINAL REPORT ===\n")
        print(final_state["report"])

    except MultiAgentException as cbe:
        logging.error(f"Main: MultiAgentException occurred: {cbe}")
    except Exception as e:
        logging.exception(f"Main: Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
