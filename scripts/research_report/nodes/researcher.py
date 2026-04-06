"""Web Researcher node — gathers information via Tavily search.

Teaches: tool-based web search, state accumulation via reducers.

Uses the Tavily client directly (rather than ToolNode) so the search logic is
transparent.  The teaching notebook shows the ToolNode alternative.
"""

import os

from tavily import TavilyClient

from scripts.research_report.models import ResearchState, SearchResult

# Limit queries per section to stay within free-tier rate limits
MAX_QUERIES_PER_SECTION = 2
MAX_RESULTS_PER_QUERY = 3


def web_researcher(state: ResearchState) -> dict:
    """Search the web for each section's queries and accumulate results."""
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    plan = state["research_plan"]
    new_results: list[SearchResult] = []

    for section in plan.sections:
        for query in section.search_queries[:MAX_QUERIES_PER_SECTION]:
            try:
                response = client.search(
                    query=query,
                    max_results=MAX_RESULTS_PER_QUERY,
                    search_depth="basic",
                )
                for result in response.get("results", []):
                    new_results.append(
                        SearchResult(
                            query=query,
                            url=result.get("url", ""),
                            title=result.get("title", ""),
                            content=result.get("content", ""),
                            section=section.title,
                        )
                    )
            except Exception as e:
                print(f"  ⚠ Search failed for '{query}': {e}")

    print(f"  ✓ Gathered {len(new_results)} search results")
    return {
        "search_results": new_results,
        "status": "researched",
    }
