"""Report Writer node — writes polished report sections, then self-reviews quality.

Teaches: quality self-review loops, multi-destination conditional routing.

Two-phase node:
  1. Write each section using relevant search results + analysis
  2. Self-review using structured output → QualityReview drives routing
"""

from scripts.research_report.config import get_llm
from scripts.research_report.models import QualityReview, ResearchState

WRITER_SYSTEM_PROMPT = """\
You are a professional report writer producing publication-quality research reports.

Write the requested section using the provided research material. Requirements:
- Clear, authoritative prose suitable for a professional audience
- Cite specific data points and sources where available
- Use markdown formatting (headers, bold, bullet points) for readability
- Each section should be 200-400 words
- Reference charts or data that will appear in the report when relevant
"""

REVIEWER_SYSTEM_PROMPT = """\
You are a quality reviewer for research reports. Assess whether the report is
complete and ready for publication.

Consider:
- Are all sections substantive (not thin or vague)?
- Is there enough quantitative data and evidence?
- Are there obvious gaps in coverage?

Route to:
- "compiler" if the report is ready for final assembly
- "web_researcher" if specific sections need more source material
- "data_analyst" if more quantitative analysis or charts are needed

Be pragmatic — the report doesn't need to be perfect, just thorough and professional.
"""


def report_writer(state: ResearchState) -> dict:
    """Write report sections from research, then self-review quality."""
    llm = get_llm(temperature=0.3)  # slight creativity for writing
    plan = state["research_plan"]
    analysis = state.get("analysis")

    # Build context from search results grouped by section
    results_by_section: dict[str, list[str]] = {}
    for r in state["search_results"]:
        results_by_section.setdefault(r.section, []).append(
            f"**{r.title}** ({r.url})\n{r.content}"
        )

    analysis_context = ""
    if analysis:
        findings = "\n".join(f"- {f}" for f in analysis.key_findings)
        analysis_context = f"\n\nKey findings from data analysis:\n{findings}"

    # --- Phase 1: Write each section ---
    sections: dict[str, str] = {}

    # Executive summary
    exec_prompt = (
        f"Write an executive summary for a report titled '{plan.title}'.\n"
        f"Focus on: {plan.executive_summary_prompt}\n"
        f"{analysis_context}"
    )
    exec_response = llm.invoke([
        {"role": "system", "content": WRITER_SYSTEM_PROMPT},
        {"role": "user", "content": exec_prompt},
    ])
    sections["Executive Summary"] = exec_response.content

    # Content sections
    for section in plan.sections:
        source_material = "\n---\n".join(
            results_by_section.get(section.title, ["No search results available."])
        )
        section_prompt = (
            f"Write the section '{section.title}' for the report '{plan.title}'.\n"
            f"Section goal: {section.description}\n\n"
            f"Source material:\n{source_material}\n"
            f"{analysis_context}"
        )
        response = llm.invoke([
            {"role": "system", "content": WRITER_SYSTEM_PROMPT},
            {"role": "user", "content": section_prompt},
        ])
        sections[section.title] = response.content
        print(f"  ✓ Wrote section: {section.title}")

    # --- Phase 2: Self-review quality ---
    review_llm = get_llm().with_structured_output(QualityReview, method="function_calling")

    sections_preview = "\n\n".join(
        f"### {title}\n{content[:300]}..." for title, content in sections.items()
    )
    review = review_llm.invoke([
        {"role": "system", "content": REVIEWER_SYSTEM_PROMPT},
        {"role": "user", "content": (
            f"Review this report draft:\n\n"
            f"**Title**: {plan.title}\n"
            f"**Sections written**: {list(sections.keys())}\n"
            f"**Charts available**: {len(state.get('charts', []))}\n"
            f"**Screenshots available**: {len(state.get('screenshots', []))}\n\n"
            f"Section previews:\n{sections_preview}"
        )},
    ])

    print(f"  ✓ Quality review: complete={review.is_complete}, route={review.route_to}")

    return {
        "report_sections": sections,
        "status": review.route_to,
        "iteration_count": state["iteration_count"] + 1,
    }
