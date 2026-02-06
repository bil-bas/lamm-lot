from io import BytesIO
import os
from zipfile import ZipFile

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image, CoreImage
from kivy.properties import ListProperty, DictProperty, StringProperty

from .sticker_generator import StickerGenerator
from .utils import print_to_screen


class StickerScreen(Screen):
    selected = ListProperty()
    site = DictProperty()
    sticker_type = StringProperty()

    def on_pre_enter(self, *args) -> None:
        if self.sticker_type == "small":
            size = StickerGenerator.SIZE_SMALL
        elif self.sticker_type == "large":
            size = StickerGenerator.SIZE_LARGE
        else:
            raise ValueError(f"Bad sticker type {self.sticker_type}")

        for item in self.selected:
            generator = StickerGenerator(item=item, site=self.site)
            self._add_sticker(generator, size)

    def on_leave(self, *args):
        self.ids["stickers"].clear_widgets()

        return super().on_leave(*args)

    def _add_sticker(self, generator: StickerGenerator, size: list[int, int]) -> None:
        data = generator.generate(size)

        tex = CoreImage(BytesIO(data.read()), ext="png")
        image = Image()
        image.texture = tex.texture
        image.size_hint = None, None
        image.size = print_to_screen(size[0]), print_to_screen(size[1])

        self.ids["stickers"].add_widget(image)

    def save_images(self):
        stickers = self.ids["stickers"].children

        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if len(stickers) == 1:
           stickers[0].texture.save(os.path.join(folder, f"{self.selected[0]["sku"]}.png"),
                                   flipped=False)
        else:
            with ZipFile("stickers.zip", "w") as zip_file:
                for sticker, item in zip(stickers, self.selected):
                    data = BytesIO()
                    sticker.texture.save(data, flipped=False, fmt="png")
                    zip_file.writestr(f"{item["sku"]}.png", data.getvalue())
