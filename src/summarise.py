import os
import time
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
API_URL = "https://api.perplexity.ai/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
}

DEFAULT_INPUT = "outputs/full_text.txt"
DEFAULT_OUTPUT = "outputs/summary.txt"
MAX_DOC_CHARS = 160000


def read_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input text not found: {p.resolve()}")
    return p.read_text(encoding="utf-8")


def summarise_text(text: str, retries: int = 2, timeout: int = 30) -> str:
    if not PERPLEXITY_API_KEY:
        raise RuntimeError("PERPLEXITY_API_KEY not set")

    doc_text = text
    truncated = False
    if len(doc_text) > MAX_DOC_CHARS:
        doc_text = doc_text[:MAX_DOC_CHARS] + "\n\n[TRUNCATED]\n\n"
        truncated = True

    prompt = f"""
Summarize the Act into exactly 7 bullet points covering:
- Purpose
- Key definitions
- Eligibility
- Obligations
- Payments / entitlements
- Enforcement
- Record-keeping

Rules:
- Use only the document text.
- No external knowledge.
- If a topic is missing, write 'Not present in document.'
Return as 7 plain-text bullets.

Document:
{doc_text}
"""

    payload = {"model": "sonar", "messages": [{"role": "user", "content": prompt}]}

    for attempt in range(1, retries + 1):
        r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            try:
                summary = data["choices"][0]["message"]["content"].strip()
            except Exception:
                summary = json.dumps(data)
            if truncated:
                summary = "(document truncated)\n\n" + summary
            return summary
        time.sleep(1.5 * attempt)

    r.raise_for_status()


def save(text: str, path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print(f"Saved: {p.resolve()}")


def main(input_path=DEFAULT_INPUT, output_path=DEFAULT_OUTPUT):
    text = read_text(input_path)
    summary = summarise_text(text)
    save(summary, output_path)


if __name__ == "__main__":
    main()
