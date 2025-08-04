import argparse
import os
import io
import glob
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm

# ページ番号の位置やフォント
PAGE_BOTTOM = 10 * mm
PAGE_PREFIX = "  "
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))


def get_page_size(page):
    mediabox = page.mediabox
    return float(mediabox.right), float(mediabox.top)


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


def process_pdf(
    input_path: str,
    output_dir: str,
    do_watermark: bool,
    do_pagenumber: bool,
    do_password: bool,
    sign_pdf: PdfReader,
    draft_pdf: PdfReader,
):
    filename = os.path.basename(input_path)
    reader = PdfReader(input_path)
    writer = PdfWriter()

    pages = []
    page_sizes = []
    for i, page in enumerate(reader.pages):
        if do_watermark:
            watermark_page = sign_pdf.pages[0] if i == 0 else draft_pdf.pages[0]
            page.merge_page(watermark_page)

        pages.append(page)
        page_sizes.append(get_page_size(page))

    if do_pagenumber:
        page_num_reader = create_page_number_pdf(len(pages) - 2, page_sizes[2:])
        for i, page in enumerate(pages):
            if i >= 2:
                page.merge_page(page_num_reader.pages[i - 2])
            writer.add_page(page)
    else:
        for page in pages:
            writer.add_page(page)

    if do_password:
        writer.encrypt(user_password="", owner_password="tanikan")

    writer.page_layout = "/SinglePage"

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"processed_{filename}")
    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✅ 出力完了: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="PDF加工ツール")
    parser.add_argument("--watermark", action="store_true", help="透かしを追加")
    parser.add_argument("--pagenumber", action="store_true", help="ページ番号を追加")
    parser.add_argument("--password", action="store_true", help="パスワードを追加")
    parser.add_argument("--all", action="store_true", help="すべての機能を実行")
    args = parser.parse_args()

    do_watermark = args.watermark or args.all
    do_pagenumber = args.pagenumber or args.all
    do_password = args.password or args.all

    cur_dir = os.getcwd()
    input_dir = os.path.join(cur_dir, "pdf")
    output_dir = os.path.join(cur_dir, "output")
    sign_path = os.path.join(cur_dir, "mark", "sign.pdf")
    draft_path = os.path.join(cur_dir, "mark", "draft.pdf")

    if not os.path.exists(sign_path) or not os.path.exists(draft_path):
        print("❌ mark/sign.pdf または mark/draft.pdf が見つかりません")
        return

    sign_pdf = PdfReader(sign_path)
    draft_pdf = PdfReader(draft_path)

    input_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    if not input_files:
        print("⚠️ pdf/ フォルダに処理対象のPDFがありません")
        return

    for path in input_files:
        process_pdf(path, output_dir, do_watermark, do_pagenumber, do_password, sign_pdf, draft_pdf)

    print("\n🎉 すべての処理が完了しました。")


if __name__ == "__main__":
    main()

