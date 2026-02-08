DPI_PRINT_QUALITY = 300
DPI_DEFAULT_QUALITY = 72
DPI_DEFAULT_TO_DMM = 3.7792


def mm_to_screen_px(value: float) -> int:
    return int(round(value * 4))


def mm_to_print_px(value: float):
    return int(round(value * (DPI_PRINT_QUALITY / DPI_DEFAULT_QUALITY) *
                     DPI_DEFAULT_TO_DMM))
