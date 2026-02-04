from PIL import Image, ImageDraw, ImageFont
from math import floor
from io import BytesIO

from barcode import Code128
from barcode.writer import ImageWriter

from .utils import mm_to_px


class StickerGenerator:
    SMALL_SIZE = mm_to_px(50), mm_to_px(30)
    LARGE_SIZE = mm_to_px(80), mm_to_px(50)
    SHEET_SIZE = mm_to_px(75), mm_to_px(42)
    TEXT_COLOR = 0, 0, 0
    MARGIN = mm_to_px(2)

    def __init__(self, item: dict, site: dict):
        self._item = item
        self._site = site

    def generate(self, size: tuple[int, int] = LARGE_SIZE) -> BytesIO:
        image = Image.new(mode="RGB", size=size, color=(255, 255, 255))

        self._draw_picture(image)
        self._draw_text(image)
        self._draw_barcode(image)

        data = BytesIO()
        image.save(data, format="png", dpi=(300, 300))
        data.seek(0)

        return data

    def _draw_picture(self, image: Image) -> None:
        picture = Image.open(self._item["image_"])
        size = image.height - mm_to_px(12)
        picture = picture.resize((size, size), resample=Image.Resampling.LANCZOS)
        image.paste(picture, (self.MARGIN, self.MARGIN,
                              self.MARGIN + picture.width, self.MARGIN + picture.height))

    def _draw_text(self, image: Image) -> None:
        font_title = ImageFont.truetype(f"arial.ttf", size=70)
        font_subtitle = ImageFont.truetype(f"arial.ttf", size=50)

        draw = ImageDraw.Draw(image)
        draw.text((self.MARGIN, image.height - 70 - 50 - self.MARGIN),
                   self._site["name"], self.TEXT_COLOR, font_title)
        draw.text((self.MARGIN, image.height - 50 - self.MARGIN),
                  "Part of BayShare - bayshare.org.uk", self.TEXT_COLOR, font_subtitle)

    def _draw_barcode(self, image: Image) -> None:
        barcode = self._create_barcode(self._item["sku"])
        barcode = barcode.transpose(Image.ROTATE_90)
        image.paste(barcode, (image.width - barcode.width, (image.height - barcode.height) // 2))

    def _create_barcode(self, sku: str) -> Image:
        data = BytesIO()
        Code128(sku, writer=ImageWriter()).write(data)
        image = Image.open(data)

        return image

