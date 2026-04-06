"""Research Planner node — the first node in the graph.

Teaches: structured output with Pydantic + `with_structured_output()`.
"""

from scripts.research_report.config import get_llm
from scripts.research_report.models import ResearchPlan, ResearchState

PLANNER_SYSTEM_PROMPT = """\
You are a senior research analyst who creates detailed research plans.

Given a topic, produce a structured research plan with:
1. A professional, descriptive report title
2. A prompt describing what the executive summary should address
3. 4-6 well-scoped sections, each with 2-3 targeted search queries
4. 2-4 suggested chart/visualization types that would enhance the report
5. Up to 5 real, publicly accessible URLs worth screenshotting (documentation pages,
   dashboards, comparison sites, etc.)

Make the sections flow logically — start broad (overview/context), go deep
(analysis/comparison), and end with implications/outlook.
"""


def research_planner(state: ResearchState) -> dict:
    """Use the LLM to create a structured research plan from the topic."""
    llm = get_llm().with_structured_output(ResearchPlan, method="function_calling")

    plan = llm.invoke([
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
        {"role": "user", "content": f"Create a research plan for: {state['topic']}"},
    ])

    return {
        "research_plan": plan,
        "status": "planned",
        "iteration_count": 0,
    }
