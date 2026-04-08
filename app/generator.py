from pathlib import Path
from textwrap import shorten


def summarize_excerpt(content: str, width: int = 1200) -> str:
    return shorten(" ".join(content.split()), width=width, placeholder="...")


def generate_startup_thesis(filename: str, content: str) -> str:
    excerpt = summarize_excerpt(content)
    return f"""# Startup Thesis\n\nSource: {filename}\n\n## Thesis\nBuild a venture-backed product around the core insight in this document. The opportunity is to convert dense research into a usable product wedge with clear operator value.\n\n## Problem\nTeams have interesting research and strategy insights, but they often lack a fast way to turn those insights into product theses, MVPs, and investor-friendly narratives.\n\n## Opportunity\nUse the ideas from this document to identify a product surface, target user, workflow wedge, and decision advantage.\n\n## Likely wedge\n- Start with one painful workflow\n- Make the output inspectable and operator-friendly\n- Use structured generation, not black-box magic\n\n## Why now\n- Better language models\n- Faster prototyping stacks\n- Rising demand for tools that turn strategy into execution\n\n## Source excerpt\n{excerpt}\n"""


def generate_research_agenda(filename: str, content: str) -> str:
    excerpt = summarize_excerpt(content)
    return f"""# Research Agenda\n\nSource: {filename}\n\n## Goal\nTurn the source document into a concrete research plan.\n\n## Key questions\n1. Which claims in the document are most testable?\n2. Which assumptions need stronger evidence?\n3. What adjacent literature should be reviewed next?\n4. What prototype or experiment would best validate the core idea?\n\n## Workstreams\n- Literature review expansion\n- Competitive analysis\n- Technical feasibility analysis\n- Prototype design\n- Evaluation methodology\n\n## Deliverables\n- cited bibliography\n- concept map\n- prototype brief\n- risk register\n- experiment plan\n\n## Source excerpt\n{excerpt}\n"""


def generate_deck_outline(filename: str, content: str) -> str:
    excerpt = summarize_excerpt(content)
    return f"""# PowerPoint-Style Deck Outline\n\nSource: {filename}\n\n1. Title / framing\n2. The problem\n3. Why this matters now\n4. Core insight from the summary\n5. Product / research direction\n6. Architecture or system model\n7. Market / user impact\n8. Risks and constraints\n9. Pilot / prototype plan\n10. Closing takeaway\n\n## Speaker note seed\n{excerpt}\n"""


def generate_pitch_decks(filename: str, content: str) -> str:
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


def generate(kind: str, filename: str, content: str) -> str:
    handlers = {
        "startup-thesis": generate_startup_thesis,
        "research-agenda": generate_research_agenda,
        "deck-outline": generate_deck_outline,
        "pitch-decks": generate_pitch_decks,
    }
    if kind not in handlers:
        raise ValueError(f"Unknown generation kind: {kind}")
    return handlers[kind](filename, content)
