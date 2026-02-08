from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from barcode import Code128
from barcode.writer import ImageWriter
import qrcode

from .utils import mm_to_print_px, DPI_PRINT_QUALITY
from .config import get_config


class StickerGenerator:  
    TEXT_COLOR = 0, 0, 0
    MARGIN = mm_to_print_px(2)

    def __init__(self, item: dict, site: dict):
        self._item = item
        self._site = site

    def generate(self, size: list[int, int]) -> BytesIO:
        size_px = mm_to_print_px(size[0]), mm_to_print_px(size[1])
        image = Image.new(mode="RGB", size=size_px, color=(255, 255, 255))

        self._draw_barcode(image)
        self._draw_picture(image)
        self._draw_text(image)
        self._draw_qr_code(image)

        data = BytesIO()
        image.save(data, format="png", dpi=(DPI_PRINT_QUALITY, DPI_PRINT_QUALITY))
        data.seek(0)

        return data

    def _draw_qr_code(self, image: Image) -> None:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_M,
                           box_size=image.height / 60, border=0)
        qr.add_data(self._item["url"])
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        top_margin = (image.height - qr_image.size[1]) // 2
        image.paste(qr_image,
                    (self.MARGIN, top_margin, self.MARGIN + qr_image.size[0], top_margin + qr_image.size[1]))

    def _draw_picture(self, image: Image, greyscale: bool = True) -> None:
        try:
            picture = Image.open(self._item["image"])
        except (PermissionError, KeyError):
            return

        size = image.height // 3
        picture = picture.resize((size, size), resample=Image.Resampling.LANCZOS)

        if greyscale:
            picture = picture.convert("L")

        left_margin = image.width  // 2
        top_margin = (image.height - picture.height) // 2
        
        image.paste(picture, (left_margin, top_margin,
                              left_margin + picture.width, top_margin + picture.height))

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
        if get_config().stickers.show_site:
            draw.text((self.MARGIN, image.height - font_size_large - font_size_small - self.MARGIN),
                    self._site["name"], self.TEXT_COLOR, font_title)
    
        draw.text((self.MARGIN, image.height - font_size_small - self.MARGIN),
                  get_config().stickers.organization, self.TEXT_COLOR, font_subtitle)

    def _draw_barcode(self, image: Image) -> None:
        barcode = self._create_barcode(self._item["sku"])
        barcode = barcode.transpose(Image.ROTATE_90)
        image.paste(barcode, (image.width - barcode.width, (image.height - barcode.height) // 2))

    def _create_barcode(self, sku: str) -> Image:
        data = BytesIO()
        Code128(sku, writer=ImageWriter()).write(data)
        image = Image.open(data)

        return image

