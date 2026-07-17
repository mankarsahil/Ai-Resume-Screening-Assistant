"""Utilities for extracting plain text from resume files."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import pdfplumber
from docx import Document


def _as_binary_stream(file_path_or_bytes: Any):
    """Return a file-like object for bytes input so the extractors can read it."""

    if isinstance(file_path_or_bytes, (bytes, bytearray)):
        return BytesIO(file_path_or_bytes)
    if hasattr(file_path_or_bytes, "read"):
        return file_path_or_bytes
    return file_path_or_bytes


def extract_text_from_pdf(file_path_or_bytes):
    """Extract all text from a PDF because resume PDFs are usually scanned page by page."""

    source = _as_binary_stream(file_path_or_bytes)
    extracted_pages = []

    with pdfplumber.open(source) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            extracted_pages.append(page_text)

    return "\n".join(extracted_pages).strip()


def extract_text_from_docx(file_path_or_bytes):
    """Extract all paragraph text from a DOCX because resumes are often structured as paragraphs."""

    source = _as_binary_stream(file_path_or_bytes)
    document = Document(source)
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs).strip()


def extract_text(file_path_or_bytes, filename):
    """Route a resume file to the correct extractor so the API can treat PDF and DOCX the same way."""

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path_or_bytes)
    if extension == ".docx":
        return extract_text_from_docx(file_path_or_bytes)

    raise ValueError("Unsupported file type. Please upload a PDF or DOCX.")
