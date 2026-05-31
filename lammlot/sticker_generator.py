from PIL import Image as PILImage, ImageDraw, ImageFont
from PIL.Image import Image

from io import BytesIO

from barcode import Code128
from barcode.writer import ImageWriter
import qrcode

from .utils import mm_to_print_px, DPI_PRINT_QUALITY
from .config import get_config


class StickerGenerator:
    TEXT_COLOR = 0, 0, 0
    PAPER_COLOR = 255, 255, 255
    MARGIN = mm_to_print_px(2)
    PHOTO_SCALE = 5

    def __init__(self, item: dict, site: dict, curved_surface: bool):
        self._item = item
        self._site = site
        self._curved_surface = curved_surface

    def generate(self, size: list[int]) -> BytesIO:
        size_px = mm_to_print_px(size[0]), mm_to_print_px(size[1])
        image: Image = PILImage.new(mode="RGB", size=size_px,
                                    color=self.PAPER_COLOR)

        self._draw_barcode(image)
        if image.height / image.width <= 5/8:
            self._draw_logo(image)
        self._draw_text(image)
        self._draw_qr_code(image)

        data = BytesIO()
        image.save(data, format="png", dpi=(DPI_PRINT_QUALITY,
                                            DPI_PRINT_QUALITY))
        data.seek(0)

        return data

    def _draw_qr_code(self, image: Image) -> None:
        box_size = image.height / (100 if self._curved_surface else 50)

        qr = qrcode.QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_M,
                           box_size=box_size, border=0)
        qr.add_data(self._item["url"])
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color=self.TEXT_COLOR,
                                 back_color=self.PAPER_COLOR).get_image()

        top_margin = (image.height - qr_image.size[1]) // 2
        image.paste(qr_image,
                    (self.MARGIN,
                     top_margin,
                     self.MARGIN + qr_image.size[0],
                     top_margin + qr_image.size[1]))

    def _draw_logo(self, image: Image) -> None:
        picture = PILImage.open("images/bayshare_logo.png")

        display_size = image.height // 2
        picture = picture.resize((display_size, display_size))

        left_margin = int(image.width * 0.4)
        top_margin = (image.height - picture.height) // 2

        image.paste(picture,
                    (left_margin, top_margin,
                     left_margin + picture.width, top_margin + picture.height))

    def _draw_picture(self, image: Image, greyscale: bool = True) -> None:
        try:
            picture = PILImage.open(self._item["image"])
        except (PermissionError, KeyError):
            return

        display_size = image.height // 2

        if greyscale:
            # Greyscale and then dither.
            picture = picture.convert("L")
            size = display_size // self.PHOTO_SCALE
            picture = picture.resize((size, size),
                                     resample=PILImage.Resampling.LANCZOS)
            picture = picture.convert("1")

        display_size = image.height // 2
        picture = picture.resize((display_size, display_size))

        left_margin = int(image.width * 0.4)
        top_margin = (image.height - picture.height) // 2

        image.paste(picture,
                    (left_margin, top_margin,
                     left_margin + picture.width, top_margin + picture.height))

    def _draw_text(self, image: Image) -> None:
        font_size_title = image.width / 20
        font_size_regular = image.width / 20
        font_size_small = image.width / 25

        font_title = ImageFont.truetype("arial.ttf", size=font_size_title)
        font_regular = ImageFont.truetype("arial.ttf", size=font_size_regular)
        font_small = ImageFont.truetype("arial.ttf", size=font_size_small)

        draw = ImageDraw.Draw(image)

        # Top Text
        draw.text((self.MARGIN, self.MARGIN),
                  self._item["name"]["en"], self.TEXT_COLOR, font_title)

        # Bottom text
        y = image.height - font_size_regular - font_size_small - self.MARGIN
        name_and_code = f"{self._site["name"]} - {self._site["postCode"]}"
        draw.text((self.MARGIN, y),
                  name_and_code, self.TEXT_COLOR, font_regular)

        draw.text((self.MARGIN, image.height - font_size_small - self.MARGIN),
                  get_config().stickers.organization,
                  self.TEXT_COLOR,
                  font_small)

    def _draw_barcode(self, image: Image) -> None:
        barcode: Image = self._create_barcode(self._item["sku"])
        barcode: Image = barcode.transpose(PILImage.Transpose.ROTATE_90)
        aspect_ratio = barcode.width / barcode.height

        barcode = barcode.resize((round(image.height * aspect_ratio),
                                  image.height),
                                 resample=PILImage.Resampling.LANCZOS)

        image.paste(barcode,
                    (image.width - barcode.width, 0))

    def _create_barcode(self, sku: str) -> Image:
        data = BytesIO()
        Code128(sku, writer=ImageWriter()).write(data)
        image = PILImage.open(data)

        return image
