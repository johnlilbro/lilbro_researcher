from pathlib import Path
from datetime import datetime, timezone

TOPIC = "dynamic UI generation in e-commerce"

PROMPT_TEMPLATE = f"""Research topic: {TOPIC}

Tasks:
1. Gather recent papers and blog posts from roughly the last year.
2. Prioritize sources that discuss adaptive UI, personalized storefronts, generative UI, and AI-assisted merchandising.
3. Summarize the key idea, why it matters, and practical implications for e-commerce product teams.
4. Save the summary to summaries/summary_<timestamp>.md
"""


def main():
    out = Path("research/agent_prompt.txt")
    out.write_text(PROMPT_TEMPLATE)
    print(f"Wrote {out}")
    print("This script is a lightweight placeholder for a future autonomous research workflow.")


if __name__ == "__main__":
    main()
