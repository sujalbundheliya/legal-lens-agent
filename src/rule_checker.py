import json
from pathlib import Path
from typing import Dict, Any, List

SECTIONS_FILE = Path("outputs/sections.json")
FULL_TEXT_FILE = Path("outputs/full_text.txt")


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def safe_get_text(obj: Dict[str, Any], key: str) -> str:
    field = obj.get(key, {})
    if isinstance(field, dict):
        return (field.get("text") or "").strip()
    return ""


def safe_get_evidence(obj: Dict[str, Any], key: str) -> str:
    field = obj.get(key, {})
    if isinstance(field, dict):
        return (field.get("evidence") or "").strip()
    return ""


def compute_confidence(text: str, evidence: str) -> int:
    if not text:
        return 0
    base = 50
    length_bonus = min(25, int(len(text) / 250 * 25))
    evidence_bonus = 25 if evidence else 0
    return min(100, base + length_bonus + evidence_bonus)


def keyword_scan(full_text: str, keywords: List[str]) -> List[str]:
    if not full_text:
        return []
    ft = full_text.lower()
    return [k for k in keywords if k in ft]


def evaluate_rules(sections: Dict[str, Any], full_text: str) -> List[Dict[str, Any]]:
    RULES = [
        ("Act must define key terms", "definitions"),
        ("Act must specify eligibility criteria", "eligibility"),
        ("Act must specify responsibilities of the administering authority", "responsibilities"),
        ("Act must include enforcement or penalties", "penalties"),
        ("Act must include payment calculation or entitlement structure", "payments"),
        ("Act must include record-keeping or reporting requirements", "record_keeping"),
    ]

    PENALTIES_KW = ["penalt", "offenc", "fine", "sanction", "enforce", "liable", "prosecut", "criminal"]
    RECORD_KW = ["record", "report", "information requirement", "assessment", "retain", "evidence"]
    GENERIC_KW = ["oblig", "respons", "eligib", "payment", "entit", "award", "uprat", "increase"]

    results = []

    for rule_text, key in RULES:
        text = safe_get_text(sections, key)
        evidence = safe_get_evidence(sections, key)

        passed_text = bool(text)
        passed_evidence = bool(evidence)

        if key == "penalties":
            hits = keyword_scan(full_text, PENALTIES_KW)
        elif key == "record_keeping":
            hits = keyword_scan(full_text, RECORD_KW)
        else:
            hits = keyword_scan(full_text, GENERIC_KW)

        passed_kw = len(hits) > 0

        if passed_text:
            status = "pass"
            confidence = compute_confidence(text, evidence)
            ev = evidence or text[:300]
        elif passed_evidence:
            status = "pass"
            confidence = 60
            ev = evidence
        elif passed_kw:
            status = "pass"
            confidence = 55 + min(20, 5 * len(hits))
            ev = ", ".join(hits)
        else:
            status = "fail"
            confidence = 95 if key == "penalties" else 10
            ev = ""

        results.append({
            "rule": rule_text,
            "status": status,
            "evidence": ev,
            "confidence": confidence
        })

    return results


def save_results(results: List[Dict[str, Any]], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Saved: {path.resolve()}")


def main():
    sections = load_json(SECTIONS_FILE)
    full_text = load_text(FULL_TEXT_FILE)
    results = evaluate_rules(sections, full_text)
    save_results(results, Path("outputs/rules_output.json"))

    print("\nSummary:")
    for r in results:
        ev = (r['evidence'][:120] + "...") if r['evidence'] and len(r['evidence']) > 120 else r['evidence']
        print(f"- {r['rule']}: {r['status']} ({r['confidence']}%) — {ev}")


if __name__ == "__main__":
    main()
