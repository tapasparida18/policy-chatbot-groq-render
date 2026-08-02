import re
 
 
def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()
 
 
def detect_section_title(text):
    """
    Simple section detector.
    It picks the beginning of the chunk as section title.
    Later this can be improved with heading detection.
    """
 
    cleaned = clean_text(text)
 
    if not cleaned:
        return "General Policy Section"
 
    words = cleaned.split()
 
    title_words = words[:8]
 
    title = " ".join(title_words)
 
    if len(title) > 80:
        title = title[:80]
 
    return title if title else "General Policy Section"
 
 
def create_chunks(
    pages,
    chunk_size=500,
    overlap=100
):
    chunks = []
 
    chunk_id = 0
 
    for page in pages:
 
        page_number = page["page"]
 
        text = clean_text(page["text"])
 
        if not text:
            continue
 
        start = 0
        text = text.replace(
            "Corporate Employee Policy Manual - India Template",
            ""
        )
 
        text = text.replace(
            "Confidential - HR controlled document",
            ""
        )
 
        text = text.replace(
            "Template for company customization. Verify with current law and company HR before use.",
            ""
        )
        
        while start < len(text):
 
            end = start + chunk_size
 
            chunk_text = text[start:end].strip()
 
            if len(chunk_text) >= 80:
 
                section_title = detect_section_title(chunk_text)
 
                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "page": page_number,
                        "section_title": section_title,
                        "text": chunk_text
                    }
                )
 
                chunk_id += 1
 
            start += chunk_size - overlap
 
    return chunks