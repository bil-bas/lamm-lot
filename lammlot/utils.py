PRINT_QUALITY = 300 / 72

MM_TO_PX = 3.7792 * PRINT_QUALITY


def mm_to_px(value: float) -> int:
    return int(round(value * MM_TO_PX))

def px_to_mm(value: int) -> float:
    return value // MM_TO_PX

def print_to_screen(value: int) -> int:
    return value / PRINT_QUALITY
