from io import BytesIO
from pathlib import Path

from sanitize_filename.sanitize_filename import sanitize
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image, CoreImage
from kivy.factory import Factory
from kivy.properties import ListProperty, DictProperty

from .sticker_generator import StickerGenerator
from .utils import mm_to_screen_px


class StickerScreen(Screen):
    selected = ListProperty()
    site = DictProperty()
    sticker_size = ListProperty()

    def on_pre_enter(self, *args) -> None:
        for item in self.selected:
            generator = StickerGenerator(item=item, site=self.site)
            self._add_sticker(generator)

    def on_leave(self, *args):
        self.ids["stickers"].clear_widgets()

        return super().on_leave(*args)

    def _add_sticker(self, generator: StickerGenerator) -> None:
        data = generator.generate(self.sticker_size)

        tex = CoreImage(BytesIO(data.read()), ext="png")
        image = Image()
        image.texture = tex.texture
        image.size_hint = None, None
        image.size = mm_to_screen_px(self.sticker_size[0]), mm_to_screen_px(self.sticker_size[1])

        self.ids["stickers"].add_widget(image)

    def save_images(self):
        stickers = self.ids["stickers"].children

        # TODO: Show a folder save dialog, rather than using project folder.
        folder = Path(__file__).absolute().parent.parent / "output" / f"{self.sticker_size[0]}x{self.sticker_size[1]}mm"
        folder.mkdir(parents=True, exist_ok=True)
        
        for sticker, item in zip(stickers, self.selected):
            filename = sanitize(f"{item["sku"]}-{item["name"]["en"][:40]}.png")
            sticker.texture.save(str(folder / filename), flipped=False)

        self.manager.current = "search"

        popup = Factory.SavedDialog()
        popup.num_saved = len(self.selected)
        popup.open()
            