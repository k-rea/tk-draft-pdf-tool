def get_page_size(page) -> tuple[float, float]:
    box = page.mediabox
    return float(box.right), float(box.top)
