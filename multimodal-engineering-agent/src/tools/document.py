from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def extract_text(file_path: str, max_chars: int = 3000) -> Dict[str, Any]:
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ImportError("pypdf is required for PDF parsing. Install it with: pip install pypdf") from exc

        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        text = "\n".join(pages)
        return {
            "file_name": path.name,
            "num_pages": len(reader.pages),
            "text_preview": text[:max_chars],
            "num_chars": len(text),
        }

    if ext in {".txt", ".md"}:
        text = path.read_text(encoding="utf-8", errors="ignore")
        return {
            "file_name": path.name,
            "num_pages": None,
            "text_preview": text[:max_chars],
            "num_chars": len(text),
        }

    raise ValueError(f"Unsupported document type: {ext}")


def run_document_tool(file_path: str, task_type: str) -> Dict[str, Any]:
    return extract_text(file_path)
