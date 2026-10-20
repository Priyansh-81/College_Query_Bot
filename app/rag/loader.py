from pathlib import Path
import pymupdf

def load_pdf(file_path:str|Path)->str:
    path=Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"File is not a PDF: {file_path}, It should be a PDF file with .pdf ext")

    extracted_pages=[]
    with pymupdf.open(path) as doc:
        for page in doc:
            page_text=page.get_text().strip()
            if page_text:
                extracted_pages.append(page_text)

    return "\n\n".join(extracted_pages)

    