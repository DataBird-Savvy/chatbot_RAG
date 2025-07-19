from agentapp.core.orchestrator import LangGraphBuilder
from agentapp.logger import logging
from agentapp.exception import MultiAgentException


class LangGraphRunner:
    def __init__(self):
        self.builder = LangGraphBuilder()

    def run(self, query: str):
        logging.info("LangGraphRunner: Starting orchestration...")

        try:
            # Build the graph
            graph = self.builder.build()
            logging.info("LangGraphRunner: Graph built successfully.")

            # Define initial state
            initial_state = {"query": query}
            logging.info(f"LangGraphRunner: Initial state: {initial_state}")

            # Invoke the graph
            final_state = graph.invoke(initial_state)
            logging.info("LangGraphRunner: Execution completed.")

            # Display result
            print("\n=== FINAL REPORT ===\n")
            print(final_state["report"])

        except MultiAgentException as mae:
            logging.error(f"LangGraphRunner: MultiAgentException occurred: {mae}")
        except Exception as e:
            logging.exception(f"LangGraphRunner: Unexpected error occurred: {e}")


if __name__ == "__main__":
    runner = LangGraphRunner()
    runner.run("AI in healthcare")
