# O'Reilly Live Training — Getting Started with LangGraph

Build stateful, multi-step AI agents using [LangGraph](https://docs.langchain.com/oss/python/langgraph/).

## Setup

**Conda** (recommended)

```bash
conda create -n oreilly-langgraph python=3.11
conda activate oreilly-langgraph
pip install -r requirements/requirements.txt
```

**Pip**

```bash
python -m venv oreilly-langgraph
source oreilly-langgraph/bin/activate   # macOS/Linux
# .\oreilly-langgraph\Scripts\activate  # Windows
pip install -r requirements/requirements.txt
```

### Environment Variables

Copy `.env.example` to `.env` and add your API keys:

```
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

### Jupyter Kernel

```bash
pip install jupyter
python -m ipykernel install --user --name=oreilly-langgraph
```

## Notebooks

| # | Notebook | Topics |
|---|----------|--------|
| 1 | [LangGraph Fundamentals](notebooks/1.0-langgraph-fundamentals.ipynb) | States, nodes, edges, conditional routing, messages & reducers, LLM patterns (chaining, parallel, routing), tool integration |
| 2 | [ReAct Agent with Memory](notebooks/2.0-react-agent-with-memory.ipynb) | Web search agent, ToolNode, tools_condition, MemorySaver, thread-based persistence |
| 3 | [RAG Agent](notebooks/3.0-rag-agent.ipynb) | Document retrieval, Chroma vectorstore, question routing, document grading, web search fallback, local model option (gemma4) |

## Guides

- [LangGraph Studio Setup](notebooks/5.0-langgraph-studio-guide.md) — Visual debugging with LangGraph Studio

## Project Structure

```
├── notebooks/
│   ├── 1.0-langgraph-fundamentals.ipynb
│   ├── 2.0-react-agent-with-memory.ipynb
│   ├── 3.0-rag-agent.ipynb
│   ├── 5.0-langgraph-studio-guide.md
│   ├── assets-resources/          # Images and reference docs
│   ├── extra-notebooks/           # Supplementary notebooks and demos
│   └── langgraph-studio/          # Example project for Studio
├── scripts/                       # Standalone Python scripts
├── presentation/                  # Slide deck
└── requirements/                  # Dependencies
```

## Extra Materials

- `notebooks/extra-notebooks/` — Additional notebooks including advanced RAG with hallucination grading, agents from scratch, live demo examples
- `scripts/` — Standalone Python scripts (agentic RAG, YouTube workflow, bulk task agent)
- `notebooks/assets-resources/` — Architecture diagrams and reference documents
