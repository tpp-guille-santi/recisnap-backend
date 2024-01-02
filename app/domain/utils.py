def get_total_pages(count: int, page_size: int) -> int:
    return -(-count // page_size)


def get_next_page(page: int, total_pages: int) -> int | None:
    return page + 1 if page + 1 < total_pages else None
