from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from barcode import Code128
from barcode.writer import ImageWriter

from .utils import mm_to_print_px, DPI_PRINT_QUALITY


class StickerGenerator:
    SIZE_SMALL = [40, 30]
    SIZE_MEDIUM = [50, 40]
    SIZE_LARGE = [80, 50]
    
    TEXT_COLOR = 0, 0, 0
    MARGIN = mm_to_print_px(2)

    def __init__(self, item: dict, site: dict):
        self._item = item
        self._site = site

    def generate(self, size: list[int, int]) -> BytesIO:
        assert size in (self.SIZE_SMALL, self.SIZE_MEDIUM, self.SIZE_LARGE), size

        size_px = mm_to_print_px(size[0]), mm_to_print_px(size[1])
        image = Image.new(mode="RGB", size=size_px, color=(255, 255, 255))

        self._draw_picture(image)
        self._draw_text(image)
        self._draw_barcode(image)

        data = BytesIO()
        image.save(data, format="png", dpi=(DPI_PRINT_QUALITY, DPI_PRINT_QUALITY))
        data.seek(0)

        return data

    def _draw_picture(self, image: Image, greyscale: bool = True) -> None:
        try:
            picture = Image.open(self._item["image"])
        except (PermissionError, KeyError):
            return

        size = image.height - mm_to_print_px(16)
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

