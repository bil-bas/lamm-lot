MM_TO_PX = 3.7792 * (300/72)



def mm_to_px(value: float) -> int:
    return int(round(value * MM_TO_PX))