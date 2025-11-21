import re
import argparse
from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except Exception:
    PYPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except Exception:
    PDFPLUMBER_AVAILABLE = False

DEFAULT_DEMO_PDF = "data/data.pdf"
DEFAULT_OUTPUT = "outputs/full_text.txt"


def extract_with_pypdf(pdf_path: str) -> str:
    if not PYPDF_AVAILABLE:
        raise RuntimeError("pypdf is not installed")
    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        pages.append(text)
    return "\n\n".join(pages)


def extract_with_pdfplumber(pdf_path: str) -> str:
    if not PDFPLUMBER_AVAILABLE:
        raise RuntimeError("pdfplumber is not installed")
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            try:
                txt = page.extract_text() or ""
            except Exception:
                txt = ""
            texts.append(txt)
    return "\n\n".join(texts)


def clean_extracted_text(raw: str) -> str:
    if not raw:
        return ""
    raw = re.sub(r"(?<=\w)-\n(?=\w)", "", raw)
    raw = re.sub(r"\n(?=[a-z0-9(])", " ", raw)
    raw = re.sub(r"\n+\s*(?=(?:\d{1,3}\.|Section|SECTION|CHAPTER)\s)", "\n\n", raw)
    raw = re.sub(r"\n+\s*(?=[A-Z][A-Z\s]{3,})", "\n\n", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    raw = re.sub(r"[ \t]{2,}", " ", raw)
    raw = "\n".join(line.rstrip() for line in raw.splitlines())
    return raw.strip() + "\n"


def extract_text(pdf_path: str, prefer: str = "auto") -> str:
    pdf_path = str(pdf_path)
    text = ""
    methods_tried = []
    if prefer == "pypdf":
        text = extract_with_pypdf(pdf_path)
        methods_tried.append("pypdf")
    elif prefer == "pdfplumber":
        text = extract_with_pdfplumber(pdf_path)
        methods_tried.append("pdfplumber")
    else:
        if PYPDF_AVAILABLE:
            try:
                text = extract_with_pypdf(pdf_path)
                methods_tried.append("pypdf")
            except Exception:
                text = ""
        if not text and PDFPLUMBER_AVAILABLE:
            try:
                text = extract_with_pdfplumber(pdf_path)
                methods_tried.append("pdfplumber")
            except Exception:
                text = ""
    if not text:
        raise RuntimeError(f"Failed to extract text. Methods tried: {methods_tried}")
    return clean_extracted_text(text)


def write_output(text: str, out_path: str):
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"Saved cleaned text ({len(text)} chars) to: {out.resolve()}")


def main(pdf: Optional[str], out: Optional[str], prefer: str):
    pdf_path = pdf or DEFAULT_DEMO_PDF
    out_path = out or DEFAULT_OUTPUT
    print(f"Using PDF: {pdf_path}")
    print(f"Output file: {out_path}")
    text = extract_text(pdf_path, prefer=prefer)
    write_output(text, out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=str)
    parser.add_argument("--out", type=str)
    parser.add_argument("--prefer", type=str, choices=["auto", "pypdf", "pdfplumber"], default="auto")
    args = parser.parse_args()
    main(args.pdf, args.out, args.prefer)
