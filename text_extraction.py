from typing import BinaryIO


def extract_text(resume_file: BinaryIO, filename: str) -> str:
    if not filename:
        raise ValueError("Please upload a resume file.")

    file_extension = filename.lower().split(".")[-1]
    if file_extension not in {"txt", "md", "pdf", "docx"}:
        raise ValueError("Unsupported file type. Please upload a .txt, .md, .pdf, or .docx file.")

    if hasattr(resume_file, "read"):
        content = resume_file.read()
    else:
        content = b""

    if file_extension in {"txt", "md"}:
        return content.decode("utf-8", errors="ignore")

    if file_extension == "pdf":
        return "PDF text extraction is not implemented in this demo backend."

    if file_extension == "docx":
        return "DOCX text extraction is not implemented in this demo backend."

    return ""
