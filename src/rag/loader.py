from pathlib import Path
from pypdf import PdfReader
import docx


def load_text_from_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf(file_path)
    if suffix == ".docx":
        return load_docx(file_path)
    if suffix == ".txt":
        return path.read_text(encoding="utf-8")

    raise ValueError("Unsupported file type. Please use PDF, DOCX, or TXT.")


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text_parts = []

    for page in reader.pages:
        try:
            page_text = page.extract_text()
        except Exception:
            page_text = None
        if page_text:
            text_parts.append(page_text)

    return "\n".join(text_parts)


def load_docx(file_path: str) -> str:
    document = docx.Document(file_path)
    return "\n".join(
        para.text for para in document.paragraphs if para.text.strip()
    )