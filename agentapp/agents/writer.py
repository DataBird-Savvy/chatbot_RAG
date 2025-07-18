# agentapp/agents/writer.py

from agentapp.logger import logging
from agentapp.exception import MultiAgentException


class WriterAgent:
    def __init__(self):
        logging.info("WriterAgent initialized.")

    def compile_report(self, vetted_summaries: list[dict]) -> str:
        logging.info("WriterAgent: Compiling final report from vetted summaries.")

        try:
            logging.info(f"WriterAgent: Received {len(vetted_summaries)} summaries to vet.")

            high_quality = [item["summary"] for item in vetted_summaries if item["label"] == "High"]
            medium_quality = [item["summary"] for item in vetted_summaries if item["label"] == "Medium"]

            logging.info(f"WriterAgent: {len(high_quality)} high-quality summaries selected.")
            logging.info(f"WriterAgent: {len(medium_quality)} medium-quality summaries selected.")

            report_sections = []

            if high_quality:
                report_sections.append("## High-Quality Insights:\n" + "\n".join(high_quality))
            if medium_quality:
                report_sections.append("## Additional Insights:\n" + "\n".join(medium_quality))

            if not report_sections:
                logging.warning("WriterAgent: No high or medium quality summaries found.")
                report_sections.append("No relevant insights found.")
            else:
                logging.info("WriterAgent: Report sections successfully compiled.")

            return "\n\n".join(report_sections)

        except Exception as e:
            logging.error(f"WriterAgent: Failed to compile report: {e}")
            raise MultiAgentException(f"WriterAgent failed to compile report: {e}")
