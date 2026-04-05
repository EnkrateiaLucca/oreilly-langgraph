[Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/oss/python)Python
Search...
⌘K
OSS (v1-alpha)
LangChain and LangGraph
  * [Overview](https://docs.langchain.com/oss/python/langgraph/overview)


##### Get started
  * [Install](https://docs.langchain.com/oss/python/langgraph/install)
  * [Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
  * [Local server](https://docs.langchain.com/oss/python/langgraph/local-server)
  * [Workflows + agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)


##### Capabilities
  * [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
  * [Durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)
  * [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)
  * [Human-in-the-loop](https://docs.langchain.com/oss/python/langgraph/add-human-in-the-loop)
  * [Time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel)
  * [Add and manage memory](https://docs.langchain.com/oss/python/langgraph/add-memory)
  * [Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)


##### Production
  * [Application structure](https://docs.langchain.com/oss/python/langgraph/application-structure)
  * [(Coming Soon) Studio](https://docs.langchain.com/oss/python/langgraph/studio)
  * [Test](https://docs.langchain.com/oss/python/langgraph/test)
  * [(Coming Soon) Deploy](https://docs.langchain.com/oss/python/langgraph/deploy)
  * [UI](https://docs.langchain.com/oss/python/langgraph/ui)
  * [Observability](https://docs.langchain.com/oss/python/langgraph/observability)


##### LangGraph APIs
  * [Graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api)
  * [Functional API](https://docs.langchain.com/oss/python/langgraph/use-functional-api)
  * [Runtime](https://docs.langchain.com/oss/python/langgraph/pregel)


[Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/oss/python)
Python
Search...
⌘K
  * [](https://github.com/langchain-ai)
  * [Forum](https://forum.langchain.com/)
  * [Forum](https://forum.langchain.com/)


Search...
Navigation
Overview
[LangChain](https://docs.langchain.com/oss/python/langchain/overview)[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)[Integrations](https://docs.langchain.com/oss/python/integrations/providers)[Learn](https://docs.langchain.com/oss/python/learn)[Reference](https://docs.langchain.com/oss/python/versioning)[Contributing](https://docs.langchain.com/oss/python/contributing)
[LangChain](https://docs.langchain.com/oss/python/langchain/overview)[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)[Integrations](https://docs.langchain.com/oss/python/integrations/providers)[Learn](https://docs.langchain.com/oss/python/learn)[Reference](https://docs.langchain.com/oss/python/versioning)[Contributing](https://docs.langchain.com/oss/python/contributing)
* [](https://github.com/langchain-ai)
* [Forum](https://forum.langchain.com/)
On this page
  * [ Install](https://docs.langchain.com/oss/python/langgraph/overview#install)
  * [Core benefits](https://docs.langchain.com/oss/python/langgraph/overview#core-benefits)
  * [LangGraph ecosystem](https://docs.langchain.com/oss/python/langgraph/overview#langgraph-ecosystem)
  * [Acknowledgements](https://docs.langchain.com/oss/python/langgraph/overview#acknowledgements)


# Overview
Copy page
Copy page
**Alpha Notice:** These docs cover the **v1-alpha** release. Content is incomplete and subject to change.For the latest stable version, see the current [LangGraph Python](https://langchain-ai.github.io/langgraph/) or [LangGraph JavaScript](https://langchain-ai.github.io/langgraphjs/) docs.
Trusted by companies shaping the future of agents - including Klarna, Replit, Elastic, and more - LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents. LangGraph is very low-level, and focused entirely on agent **orchestration**. Before using LangGraph, it is recommended you familiarize yourself with some of the components used to build agents, starting with [models](https://docs.langchain.com/oss/python/langchain/models) and [tools](https://docs.langchain.com/oss/python/langchain/tools). We will commonly use [LangChain](https://docs.langchain.com/oss/python/langchain/overview) components throughout the documentation, but you don’t need to use LangChain to use LangGraph. If you are just getting started with agents, or want a higher level abstraction, it is recommended that you use LangChain’s [agents](https://docs.langchain.com/oss/python/langchain/agents). LangGraph is focused on the underlying capabilties important for agent orchestration: durable execution, streaming, human-in-the-loop, etc. We expose two different APIs for consuming these capabilities: a Graph API and a functional API. We largely use the Graph API throughout the documentation, but feel free to use the functional API if you’d prefer.
## 
[​](https://docs.langchain.com/oss/python/langgraph/overview#install)
pip
uv
Copy
```
pip install --pre -U langgraph

```

Then, create a simple hello world example:
Copy
```
from langgraph.graph import StateGraph, MessagesState, START, END
def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}
graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()
graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})

```

## 
[​](https://docs.langchain.com/oss/python/langgraph/overview#core-benefits)
Core benefits
LangGraph provides low-level supporting infrastructure for _any_ long-running, stateful workflow or agent. LangGraph does not abstract prompts or architecture, and provides the following central benefits:
  * [Durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution): Build agents that persist through failures and can run for extended periods, resuming from where they left off.
  * [Human-in-the-loop](https://docs.langchain.com/oss/python/langgraph/add-human-in-the-loop): Incorporate human oversight by inspecting and modifying agent state at any point.
  * [Comprehensive memory](https://docs.langchain.com/oss/python/memory): Create stateful agents with both short-term working memory for ongoing reasoning and long-term memory across sessions.
  * [Debugging with LangSmith](https://docs.langchain.com/langsmith/home): Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.
  * [Production-ready deployment](https://docs.langchain.com/langgraph-platform/deployment-options): Deploy sophisticated agent systems confidently with scalable infrastructure designed to handle the unique challenges of stateful, long-running workflows.


## 
[​](https://docs.langchain.com/oss/python/langgraph/overview#langgraph-ecosystem)
LangGraph ecosystem
While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents. To improve your LLM application development, pair LangGraph with:
  * [LangSmith](http://www.langchain.com/langsmith) — Helpful for agent evals and observability. Debug poor-performing LLM app runs, evaluate agent trajectories, gain visibility in production, and improve performance over time.
  * [LangGraph Platform](https://docs.langchain.com/langgraph-platform) — Deploy and scale agents effortlessly with a purpose-built deployment platform for long running, stateful workflows. Discover, reuse, configure, and share agents across teams — and iterate quickly with visual prototyping in [LangGraph Studio](https://docs.langchain.com/langgraph-platform/langgraph-studio).
  * [LangChain](https://docs.langchain.com/oss/python/langchain/overview) - Provides integrations and composable components to streamline LLM application development. Contains agent abstractions built on top of LangGraph.


## 
[​](https://docs.langchain.com/oss/python/langgraph/overview#acknowledgements)
Acknowledgements
LangGraph is inspired by [Pregel](https://research.google/pubs/pub37252/) and [Apache Beam](https://beam.apache.org/). The public interface draws inspiration from [NetworkX](https://networkx.org/documentation/latest/). LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.
Was this page helpful?
YesNo
[Install](https://docs.langchain.com/oss/python/langgraph/install)
Assistant
Responses are generated using AI and may contain mistakes.
[Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/oss/python)
[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)
Resources
[Changelog](https://changelog.langchain.com/)[LangChain Academy](https://academy.langchain.com/)[Trust Center](https://trust.langchain.com/)
Company
[About](https://langchain.com/about)[Careers](https://langchain.com/careers)[Blog](https://blog.langchain.com/)
[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)
[Powered by Mintlify](https://mintlify.com/preview-request?utm_campaign=poweredBy&utm_medium=referral&utm_source=langchain-5e9cc07a)
