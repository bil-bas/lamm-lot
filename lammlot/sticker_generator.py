from PIL import Image, ImageDraw, ImageFont
from math import floor
from io import BytesIO

from barcode import Code128
from barcode.writer import ImageWriter

from .utils import mm_to_px


class StickerGenerator:
    SIZE_SMALL = mm_to_px(50), mm_to_px(30)
    SIZE_LARGE = mm_to_px(80), mm_to_px(50)
    SIZE_SHEET = mm_to_px(75), mm_to_px(42)
    TEXT_COLOR = 0, 0, 0
    MARGIN = mm_to_px(2)

    def __init__(self, item: dict, site: dict):
        self._item = item
        self._site = site

    def generate(self, size: tuple[int, int]) -> BytesIO:
        image = Image.new(mode="RGB", size=size, color=(255, 255, 255))

        self._draw_picture(image)
        self._draw_text(image)
        self._draw_barcode(image)

        data = BytesIO()
        image.save(data, format="png", dpi=(300, 300))
        data.seek(0)

        return data

    def _draw_picture(self, image: Image, greyscale: bool = True) -> None:
        picture = Image.open(self._item["image_"])
        size = image.height - mm_to_px(16)
        picture = picture.resize((size, size), resample=Image.Resampling.LANCZOS)

        if greyscale:
            picture = picture.convert("L")

        top_margin = (image.height - picture.height) // 2
        image.paste(picture, (self.MARGIN, top_margin,
                              self.MARGIN + picture.width, top_margin + picture.height))

    def _draw_text(self, image: Image) -> None:
        font_size_large = image.height / 16
        font_size_small = image.height / 18

        font_title = ImageFont.truetype(f"arial.ttf", size=font_size_large)
        font_subtitle = ImageFont.truetype(f"arial.ttf", size=font_size_small)

        draw = ImageDraw.Draw(image)

        # Top Text
        draw.text((self.MARGIN, self.MARGIN),
                   self._item["name"]["en"], self.TEXT_COLOR, font_title)

        # Bottom text
        draw.text((self.MARGIN, image.height - font_size_large - font_size_small - self.MARGIN),
                   self._site["name"], self.TEXT_COLOR, font_title)
        draw.text((self.MARGIN, image.height - font_size_small - self.MARGIN),
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

