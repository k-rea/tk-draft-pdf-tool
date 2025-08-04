from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm
from pypdf import PdfReader
import io

pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
PAGE_BOTTOM = 10 * mm
PAGE_PREFIX = "  "


def create_page_number_pdf(num_pages: int, page_sizes: list[tuple[float, float]]) -> PdfReader:
    bs = io.BytesIO()
    c = canvas.Canvas(bs)
    c.setFont("HeiseiMin-W3", 10)
    for i in range(num_pages):
        size = page_sizes[i]
        c.setPageSize(size)
        c.drawCentredString(size[0] / 2.0, PAGE_BOTTOM, PAGE_PREFIX + str(i + 1))
        c.showPage()
    c.save()
    bs.seek(0)
    return PdfReader(bs)
