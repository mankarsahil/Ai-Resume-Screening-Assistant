"""Utilities for extracting plain text from resume files."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import pdfplumber
from docx import Document


def _as_binary_stream(file_path_or_bytes: Any):
    if isinstance(file_path_or_bytes, (bytes, bytearray)):
        return BytesIO(file_path_or_bytes)
    if hasattr(file_path_or_bytes, "read"):
        return file_path_or_bytes
    return file_path_or_bytes


def extract_text_from_pdf(file_path_or_bytes):
    source = _as_binary_stream(file_path_or_bytes)
    extracted_pages = []

    with pdfplumber.open(source) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            extracted_pages.append(page_text)

    return "\n".join(extracted_pages).strip()


def extract_text_from_docx(file_path_or_bytes):
    source = _as_binary_stream(file_path_or_bytes)
    document = Document(source)
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()


def extract_text(file_path_or_bytes, filename):
    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path_or_bytes)
    elif extension == ".docx":
        return extract_text_from_docx(file_path_or_bytes)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX.")