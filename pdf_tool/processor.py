from .utils import get_page_size
from .page_number import create_page_number_pdf
from pypdf import PdfReader, PdfWriter
import os


def process_pdf(input_path, output_dir, do_watermark, do_pagenumber, do_password, sign_pdf, draft_pdf, prefix, suffix):
    filename = os.path.basename(input_path)
    reader = PdfReader(input_path)
    writer = PdfWriter()

    pages = []
    page_sizes = []
    for i, page in enumerate(reader.pages):
        if do_watermark:
            watermark = sign_pdf.pages[0] if i == 0 else draft_pdf.pages[0]
            page.merge_page(watermark)

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

    # PDFタイトルを設定
    writer.add_metadata({
        "/Title": f"{prefix}{filename}{suffix}"
    })

    os.makedirs(output_dir, exist_ok=True)
    name, ext = os.path.splitext(filename)
    new_filename = f"{prefix}{name}{suffix}{ext}"
    output_path = os.path.join(output_dir, new_filename)
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"✅ 出力完了: {filename}")


def process_all_pdfs(input_dir, output_dir, sign_path, draft_path, watermark, pagenumber, password, prefix, suffix):
    if not os.path.exists(sign_path) or not os.path.exists(draft_path):
        print("❌ sign.pdf または draft.pdf が見つかりません")
        return

    sign_pdf = PdfReader(sign_path)
    draft_pdf = PdfReader(draft_path)

    pdfs = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
    if not pdfs:
        print("⚠️ 入力PDFが見つかりません")
        return

    for pdf in pdfs:
        process_pdf(
            input_path=os.path.join(input_dir, pdf),
            output_dir=output_dir,
            do_watermark=watermark,
            do_pagenumber=pagenumber,
            do_password=password,
            sign_pdf=sign_pdf,
            draft_pdf=draft_pdf,
            prefix=prefix,
            suffix=suffix
        )

    print("\n🎉 すべての処理が完了しました。")
