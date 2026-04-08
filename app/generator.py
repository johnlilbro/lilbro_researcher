import os
from pathlib import Path
from textwrap import shorten

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
SYSTEM_PROMPT = (
    "You are a research copilot that transforms markdown summaries into useful business and research artifacts. "
    "Be concrete, structured, and insightful. Avoid generic filler."
)


def summarize_excerpt(content: str, width: int = 1200) -> str:
    return shorten(" ".join(content.split()), width=width, placeholder="...")


def generate_startup_thesis_template(filename: str, content: str) -> str:
    excerpt = summarize_excerpt(content)
    return f"""# Startup Thesis\n\nSource: {filename}\n\n## Thesis\nBuild a venture-backed product around the core insight in this document. The opportunity is to convert dense research into a usable product wedge with clear operator value.\n\n## Problem\nTeams have interesting research and strategy insights, but they often lack a fast way to turn those insights into product theses, MVPs, and investor-friendly narratives.\n\n## Opportunity\nUse the ideas from this document to identify a product surface, target user, workflow wedge, and decision advantage.\n\n## Likely wedge\n- Start with one painful workflow\n- Make the output inspectable and operator-friendly\n- Use structured generation, not black-box magic\n\n## Why now\n- Better language models\n- Faster prototyping stacks\n- Rising demand for tools that turn strategy into execution\n\n## Source excerpt\n{excerpt}\n"""


def generate_research_agenda_template(filename: str, content: str) -> str:
    excerpt = summarize_excerpt(content)
    return f"""# Research Agenda\n\nSource: {filename}\n\n## Goal\nTurn the source document into a concrete research plan.\n\n## Key questions\n1. Which claims in the document are most testable?\n2. Which assumptions need stronger evidence?\n3. What adjacent literature should be reviewed next?\n4. What prototype or experiment would best validate the core idea?\n\n## Workstreams\n- Literature review expansion\n- Competitive analysis\n- Technical feasibility analysis\n- Prototype design\n- Evaluation methodology\n\n## Deliverables\n- cited bibliography\n- concept map\n- prototype brief\n- risk register\n- experiment plan\n\n## Source excerpt\n{excerpt}\n"""


def generate_deck_outline_template(filename: str, content: str) -> str:
    excerpt = summarize_excerpt(content)
    return f"""# PowerPoint-Style Deck Outline\n\nSource: {filename}\n\n1. Title / framing\n2. The problem\n3. Why this matters now\n4. Core insight from the summary\n5. Product / research direction\n6. Architecture or system model\n7. Market / user impact\n8. Risks and constraints\n9. Pilot / prototype plan\n10. Closing takeaway\n\n## Speaker note seed\n{excerpt}\n"""


def generate_pitch_decks_template(filename: str, content: str) -> str:
    excerpt = summarize_excerpt(content, width=800)
    sections = []
    for i in range(1, 6):
        sections.append(
            f"## Pitch Idea {i}\n"
            f"- Title: Candidate venture concept {i}\n"
            f"- Problem: Important workflow or market pain surfaced by the source\n"
            f"- Solution: Productized system derived from the summary\n"
            f"- Why now: AI, automation, and market timing make this newly possible\n"
            f"- Wedge: Start narrow, prove value, then expand\n"
            f"- Risk: Model quality, trust, integration complexity, or distribution\n"
        )
    joined = "\n".join(sections)
    return f"""# 5 Best Pitch Deck Ideas\n\nSource: {filename}\n\n{joined}\n## Source excerpt\n{excerpt}\n"""


def template_generate(kind: str, filename: str, content: str) -> str:
    handlers = {
        "startup-thesis": generate_startup_thesis_template,
        "research-agenda": generate_research_agenda_template,
        "deck-outline": generate_deck_outline_template,
        "pitch-decks": generate_pitch_decks_template,
    }
    if kind not in handlers:
        raise ValueError(f"Unknown generation kind: {kind}")
    return handlers[kind](filename, content)


def prompt_for_kind(kind: str, filename: str, content: str) -> str:
    prompts = {
        "startup-thesis": "Create a strong startup thesis from this source document. Include problem, customer, product wedge, why now, moat, risks, and an MVP suggestion.",
        "research-agenda": "Create a concrete research agenda from this source document. Include key questions, workstreams, deliverables, experiment ideas, and next-step recommendations.",
        "deck-outline": "Create a PowerPoint-style deck outline from this source document. Make it specific and presentation-ready, with slide titles and bullet points.",
        "pitch-decks": "Generate the 5 best pitch deck ideas from this source document. For each, include title, problem, solution, target user, why now, wedge, moat, and risks.",
    }
    if kind not in prompts:
        raise ValueError(f"Unknown generation kind: {kind}")

    return (
        f"Source file: {filename}\n\n"
        f"Task: {prompts[kind]}\n\n"
        "Source markdown:\n\n"
        f"{content}"
    )


def llm_generate(kind: str, filename: str, content: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        raise RuntimeError("LLM generation unavailable")

    client = OpenAI(api_key=api_key)
    prompt = prompt_for_kind(kind, filename, content)
    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text.strip()


def generate(kind: str, filename: str, content: str) -> tuple[str, str]:
    try:
        output = llm_generate(kind, filename, content)
        return output, f"model-backed ({MODEL_NAME})"
    except Exception:
        output = template_generate(kind, filename, content)
        return output, "template-fallback"
