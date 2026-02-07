from io import BytesIO

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image, CoreImage

from .sticker_generator import StickerGenerator


class SheetScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # TODO: generate PDFs
