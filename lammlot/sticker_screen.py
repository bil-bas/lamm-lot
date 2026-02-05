from io import BytesIO

from kivy.uix.layout import Layout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image, CoreImage
from kivy.properties import ListProperty, DictProperty, StringProperty

from .sticker_generator import StickerGenerator
from .utils import print_to_screen


class StickerScreen(Screen):
    selected = ListProperty()
    site = DictProperty()
    sticker_type = StringProperty()

    def on_enter(self, **kwargs) -> None:
        stickers: Layout = self.ids["stickers"]

        stickers.clear_widgets()

        for item in self.selected:
            generator = StickerGenerator(item=item, site=self.site)

            if self.sticker_type == "small":
                size = StickerGenerator.SIZE_SMALL
            else:
                size = StickerGenerator.SIZE_LARGE

            self._add_sticker(stickers, generator, size)

    def _add_sticker(self, stickers: Layout, generator: StickerGenerator, size: list[int, int]) -> None:
        data = generator.generate(size)

        tex = CoreImage(BytesIO(data.read()), ext="png")
        image = Image()
        image.texture = tex.texture
        image.size_hint = None, None
        image.size = print_to_screen(size[0]) * 2, print_to_screen(size[1]) * 2

        stickers.add_widget(image)

