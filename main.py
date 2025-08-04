from pdf_tool.processor import process_all_pdfs
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="PDF加工ツール")
    parser.add_argument("--watermark", action="store_true", help="透かしを追加")
    parser.add_argument("--pagenumber", action="store_true", help="ページ番号を追加")
    parser.add_argument("--password", action="store_true", help="パスワードを追加")
    parser.add_argument("--all", action="store_true", help="すべての機能を実行")
    parser.add_argument("--prefix", type=str, default="", help="ページ番号のプレフィックス")
    parser.add_argument("--suffix", type=str, default="(draft)", help="ページ番号のサフィックス")

    args = parser.parse_args()

    options = {
        "watermark": args.watermark or args.all,
        "pagenumber": args.pagenumber or args.all,
        "password": args.password or args.all,
    }

    cur_dir = os.getcwd()
    process_all_pdfs(
        input_dir=os.path.join(cur_dir, "pdf"),
        output_dir=os.path.join(cur_dir, "output"),
        sign_path=os.path.join(cur_dir, "mark", "sign.pdf"),
        draft_path=os.path.join(cur_dir, "mark", "draft.pdf"),
        prefix=args.prefix,
        suffix=args.suffix,
        **options
    )

if __name__ == "__main__":
    main()
