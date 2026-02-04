from PIL import Image, ImageDraw, ImageFont
from math import floor
from io import BytesIO

from barcode import Code128
from barcode.writer import ImageWriter

class StickerGenerator:
    MM_TO_PX = 3.7792 * (300/72)
    LARGE = (floor(80 * MM_TO_PX), floor(50 * MM_TO_PX))

    def __init__(self, item: dict, site: dict):
        self._item = item
        self._site = site

    def generate(self) -> BytesIO:
        image = Image.new(mode="RGB", size=self.LARGE, color=(255, 255, 255))
        black = (0, 0, 0)
        font_title = ImageFont.truetype(f"arial.ttf", size=70)
        font_subtitle = ImageFont.truetype(f"arial.ttf", size=50)

        draw = ImageDraw.Draw(image)
        draw.text((20, image.height - 70 - 50 - 16), self._site["name"], black, font_title)
        draw.text((20, image.height - 50 - 16), "Part of ldlot.org.uk", black, font_subtitle)

        barcode = self._create_barcode(self._item["sku"])
        barcode = barcode.transpose(Image.ROTATE_90)
        image.paste(barcode, (image.width - barcode.width, (image.height - barcode.height) // 2))

        data = BytesIO()
        image.save(data, format="png", dpi=(300, 300))
        data.seek(0)

        return data

    def _create_barcode(self, sku: str) -> Image:
        data = BytesIO()
        Code128(sku, writer=ImageWriter()).write(data)
        image = Image.open(data)

        return image

