import fitz
 
def extract_text_from_pdf(file_path):
 
    pdf = fitz.open(file_path)
 
    pages = []
 
    for page_num in range(len(pdf)):
 
        page = pdf.load_page(page_num)
 
        text = page.get_text()
 
        pages.append({
            "page": page_num + 1,
            "text": text
        })
 
    pdf.close()
 
    return pages