import os
import re
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
DEFAULT_OUTPUT = "outputs/sections.json"
MAX_DOC_CHARS = 160000


def read_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input text not found: {p.resolve()}")
    return p.read_text(encoding="utf-8")


def build_prompt(doc_text: str) -> str:
    return f"""
Extract the following 7 fields and return strict JSON only:

- definitions
- obligations
- responsibilities
- eligibility
- payments
- penalties
- record_keeping

Format:
{{
  "definitions": {{"text": "...", "evidence": "..."}},
  "obligations": {{"text": "...", "evidence": "..."}},
  "responsibilities": {{"text": "...", "evidence": "..."}},
  "eligibility": {{"text": "...", "evidence": "..."}},
  "payments": {{"text": "...", "evidence": "..."}},
  "penalties": {{"text": "...", "evidence": "..."}},
  "record_keeping": {{"text": "...", "evidence": "..."}}
}}

Rules:
- Use only information from the document.
- If a field is missing, return empty text and evidence.
- No external knowledge.
- Return only JSON.

Document:
{doc_text}
"""


def call_perplexity(prompt: str, retries: int = 2, timeout: int = 30) -> dict:
    if not PERPLEXITY_API_KEY:
        raise RuntimeError("PERPLEXITY_API_KEY not set")

    payload = {"model": "sonar", "messages": [{"role": "user", "content": prompt}]}

    for attempt in range(1, retries + 1):
        r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        time.sleep(1.5 * attempt)

    r.raise_for_status()


def parse_model_json(raw_resp: dict) -> dict:
    try:
        content = raw_resp["choices"][0]["message"]["content"]
    except:
        content = json.dumps(raw_resp)

    try:
        return json.loads(content)
    except:
        m = re.search(r"(\{[\s\S]*\})", content)
        if not m:
            raise ValueError("Invalid JSON output")
        return json.loads(m.group(1))


def normalize_fields(extracted: dict) -> dict:
    fields = [
        "definitions", "obligations", "responsibilities",
        "eligibility", "payments", "penalties", "record_keeping"
    ]
    result = {}

    for f in fields:
        obj = extracted.get(f, {}) or {}
        text_val = obj.get("text", "")
        evidence_val = obj.get("evidence", "")

        if isinstance(text_val, list):
            text_val = " ".join(str(x).strip() for x in text_val)
        if isinstance(evidence_val, list):
            evidence_val = " ".join(str(x).strip() for x in evidence_val)

        result[f] = {
            "text": text_val.strip(),
            "evidence": evidence_val.strip()
        }
    return result


def extract_sections(text: str) -> dict:
    truncated = False
    if len(text) > MAX_DOC_CHARS:
        text = text[:MAX_DOC_CHARS] + "\n\n[TRUNCATED]\n\n"
        truncated = True

    prompt = build_prompt(text)
    raw = call_perplexity(prompt)
    extracted = parse_model_json(raw)
    normalized = normalize_fields(extracted)

    if truncated:
        for k in normalized:
            if not normalized[k]["evidence"]:
                normalized[k]["evidence"] = "[document truncated]"

    return normalized


def save_output(data: dict, path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved: {p.resolve()}")


def main(input_path=DEFAULT_INPUT, output_path=DEFAULT_OUTPUT):
    text = read_text(input_path)
    sections = extract_sections(text)
    save_output(sections, output_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_path", default=DEFAULT_INPUT)
    parser.add_argument("--out", dest="output_path", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    main(args.input_path, args.output_path)
