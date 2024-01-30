# pdf_generation.py
from fpdf import FPDF

def generate_pdf(text_chunks):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    for chunk in text_chunks:
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, chunk)

    pdf_output_path = "output_notes.pdf"
    pdf.output(pdf_output_path)
    return pdf_output_path
