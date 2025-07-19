#  Conversational AI & Multi-Agent Knowledge Research Assistant

A dual-system project built with **FastAPI**, **LangGraph**, and **UltraSafe LLM APIs**, demonstrating RAG-based chat and multi-agent orchestration for advanced document reasoning.

---

##  Overview

| Component                          | Description                                                                                        |
| ---------------------------------- | -------------------------------------------------------------------------------------------------- |
|  **Chatbot (Test A)**            | FastAPI-based chat app with JWT login, ChromaDB vector retrieval, UltraSafe embedding & LLM.       |
|  **Multi-Agent System (Test B)** | LangGraph-coordinated research agents for summarizing, critiquing, and reporting academic content. |

---

##  Features at a Glance

###  **Test A – RAG ChatApp**

* Secure login, session-based chat history
* UltraSafe embedding + ChromaDB for vector retrieval
* Context-aware LLM answers (`usf1-mini`)
* Fully structured logs & unit-tested endpoints
  🡉 **[See ChatApp README](chatapp/README.md)**

### **Test B – Research Agent System**

* Research → Summarize → Critique → Synthesize (LangGraph flow)
* Uses UltraSafe APIs for embeddings, rerank, summarize, and critique
* Each agent logs outputs and errors clearly
  🡉 **[See Agent README](agentapp/README.md)**

---

