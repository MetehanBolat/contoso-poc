#!/usr/bin/env python3
"""Docs-vs-code drift checker.

Feeds the management summary and the Terraform code to an LLM (via OpenRouter)
and asks it to list every claim in the docs that the code contradicts, plus
compliance gaps relevant to a regulated bank.

Usage:
    export OPENROUTER_API_KEY=sk-or-...
    python ai/drift_check.py > drift-report.md

Model is configurable via DRIFT_MODEL (any slug from openrouter.ai/models).
"""

import os
import pathlib
import sys

from openai import OpenAI

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_FILE = REPO_ROOT / "docs" / "architecture-summary.md"
IAC_DIR = REPO_ROOT / "iac"

MODEL = os.environ.get("DRIFT_MODEL", "anthropic/claude-sonnet-4.5")

PROMPT_TEMPLATE = """\
You are reviewing a consulting deliverable for Contoso, a regulated EU business
migrating to Azure. Below is the management summary that was delivered to the
client, followed by the Terraform code that actually deploys the environment.

Produce a markdown report with two sections:

## Docs vs code
List every claim in the document that the code contradicts. For each finding:
quote the claim, name the Terraform file/resource that contradicts it, and say
what the code actually does. If a claim matches the code, do not mention it.
If nothing contradicts, say so.

## Compliance gaps
Flag anything in the code that is a problem for a regulated bank: publicly
accessible databases, disabled TLS, log retention below 12 months, missing
diagnostic settings, secrets handling issues. Name the file and setting for
each finding.

Be concrete and brief. No preamble, no closing summary, no emojis, no em-dash.

<document>
{docs}
</document>

<terraform>
{terraform}
</terraform>
"""


def gather_terraform() -> str:
    files = sorted(list(IAC_DIR.rglob("*.tf")) + list(IAC_DIR.rglob("*.tfvars")))
    return "\n\n".join(
        f"# {path.relative_to(REPO_ROOT)}\n{path.read_text()}" for path in files
    )


def main() -> int:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("error: OPENROUTER_API_KEY is not set", file=sys.stderr)
        return 1
    if not DOCS_FILE.exists():
        print(f"error: {DOCS_FILE} not found", file=sys.stderr)
        return 1

    prompt = PROMPT_TEMPLATE.format(docs=DOCS_FILE.read_text(), terraform=gather_terraform())

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=128000,
        messages=[{"role": "user", "content": prompt}],
    )

    print(f"# AI drift check (`{MODEL}`)\n")
    print(response.choices[0].message.content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
