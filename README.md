# Legal Lens Agent

**Project:** Legal Lens Agent  
**Purpose:** Extract, summarise and evaluate legislative documents (PDF → text → structured sections → rule checks).

---

## Table of Contents

1. [Project Layout](#1--project-layout)
2. [Requirements & Installation](#2--requirements--installation)
3. [Environment Variables](#3--environment-variables-env)
4. [Step-by-Step Run Instructions](#4--step-by-step-run-instructions)
5. [What Each Script Does](#5--what-each-script-does)
6. [Expected Outputs](#6--expected-outputs)
7. [Troubleshooting & Tips](#7--troubleshooting--tips)
8. [Next Steps & Optional Enhancements](#8--next-steps--optional-enhancements)

---

## 1 — Project Layout

```
legal-lens-agent/
├─ src/
│  ├─ extract_text.py       # Task 1: PDF -> cleaned text
│  ├─ summarise.py          # Task 2: cleaned text -> 7-bullet summary
│  ├─ extract_sections.py   # Task 3: cleaned text -> sections.json
│  └─ rule_checker.py       # Task 4: sections.json -> rules_output.json
├─ outputs/
│  ├─ full_text.txt
│  ├─ summary.txt
│  ├─ sections.json
│  └─ rules_output.json
├─ requirements.txt
└─ README.md
```

---

## 2 — Requirements & Installation

### Create and Activate Virtual Environment

**Linux / macOS**

```bash
python -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### Install Python Packages

```bash
pip install -r requirements.txt
```

### `requirements.txt` Contents

```
pypdf>=3.10.0
pdfplumber>=0.9.0
python-dotenv>=1.0.0
requests>=2.28.0
```

---

## 3 — Environment Variables (`.env`)

Create a `.env` file in the repo root with the following content:

```env
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

**Optional** (if using OpenAI for summarization):

```env
OPENAI_API_KEY=your_openai_api_key_here
```
---

## 4 — Step-by-Step Run Instructions

Run each task in order. Inputs and outputs are consistent across steps.

### 1) Extract Text from PDF (Task 1)

Default demo PDF is used if you don't pass `--pdf`. Replace path with your PDF if needed.

```bash
python src/extract_text.py
```

If you omit `--pdf`, it uses the built-in demo path.  
**Output:** `outputs/full_text.txt`

### 2) Generate 7-Bullet Summary (Task 2)

Uses Perplexity `sonar` by default. Ensure `PERPLEXITY_API_KEY` is set.

```bash
python src/summarise.py
```

**Output:** `outputs/summary.txt`

### 3) Extract Structured Sections (Task 3)

```bash
python src/extract_sections.py
```

**Output:** `outputs/sections.json`

### 4) Run Rule Checks (Task 4)

```bash
python src/rule_checker.py
```

**Output:** `outputs/rules_output.json`

---

## 5 — What Each Script Does

### `src/extract_text.py`
Reads a PDF, extracts text (pypdf or pdfplumber), cleans line-breaks/hyphenation/headings, and writes `outputs/full_text.txt`.

### `src/summarise.py`
Reads `outputs/full_text.txt`, calls Perplexity `sonar` to produce a 7-bullet summary, and writes `outputs/summary.txt`. Truncates very large documents to avoid token limits.

### `src/extract_sections.py`
Reads `outputs/full_text.txt`, prompts Perplexity `sonar` to extract seven fields into strict JSON with `text` + `evidence` keys for each field. Writes `outputs/sections.json`.

### `src/rule_checker.py`
Reads `outputs/sections.json` and `outputs/full_text.txt`. Runs six rule checks using section text, evidence, or keyword fallbacks. Writes `outputs/rules_output.json`.

---

## 6 — Expected Outputs

### Output Files

- **`outputs/full_text.txt`** — Cleaned, readable plain text of the PDF
- **`outputs/summary.txt`** — 7 bullet point summary (plain text)
- **`outputs/sections.json`** — JSON object with keys:
  - `definitions`
  - `obligations`
  - `responsibilities`
  - `eligibility`
  - `payments`
  - `penalties`
  - `record_keeping`
  
  Each key maps to `{"text": "...", "evidence": "..."}`

- **`outputs/rules_output.json`** — Array of 6 objects:

```json
[
  {
    "rule": "Act must define key terms",
    "status": "pass",
    "evidence": "...",
    "confidence": 92
  }
]
```

---

## 7 — Troubleshooting & Tips

### Common Issues

#### Missing `PERPLEXITY_API_KEY`
Script raises `RuntimeError`. Add the key to `.env`.

#### 400 Bad Request from Perplexity
Model name or payload is incorrect. This project uses model name `"sonar"`. If your account allows other model names, you may change `model` in the payload.

#### Large Documents Truncated
Summariser and extractor implement a safe character cap. For full coverage, implement chunking by splitting the text by headings and calling the model per chunk, then merge results.

#### PDF Extraction Yields Garbled Text
Try `--prefer pdfplumber` or `--prefer pypdf` depending on your PDF:

```bash
python src/extract_text.py --pdf path/to/doc.pdf --prefer pdfplumber
```

### Debugging Tips

- Inspect `outputs/full_text.txt` if sections extraction looks wrong
- If `sections.json` evidence keys are empty, re-run `src/extract_sections.py` and check printed raw response (scripts print raw Perplexity errors)
- If `rules_output.json` returns unexpected fails, open `outputs/sections.json` to confirm presence of `text` or `evidence`

---

## 8 — Next Steps & Optional Enhancements

- **Add chunking:** Split `full_text.txt` at headings and call models per chunk (recommended for very long Acts)
- **Switch summariser to OpenAI:** For higher quality summarisation, replace `summarise.py` call to use `openai` (requires `OPENAI_API_KEY`)
- **Add unit tests:** Create `tests/test_rule_checker.py` to assert expected pass/fail on sample `sections.json`
- **Create `pipeline.py`:** Convenience script to run all steps in order (`python pipeline.py`). Keep the modular scripts for submission
- **Create a short demo video:** 2-minute recording showing the pipeline (run commands + outputs open in editor)

---

## Assignment Reference

The assignment brief is located at:

```
/data/data.pdf
```
