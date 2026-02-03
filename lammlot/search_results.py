from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView, RecycleViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class SearchResults(RecycleView):
    pass


class SearchResult(RecycleViewBehavior, BoxLayout):
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    title_ = StringProperty()
    description_ = StringProperty()
    loan_fee_ = StringProperty()
    image_ = StringProperty()

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True

        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(touch)

    def apply_selection(self, results, index: int, is_selected: bool = True):
        self.selected = is_selected
        print("SELECTED" if is_selected else "DESELECTED")
