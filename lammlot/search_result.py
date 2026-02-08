from kivy.properties import (BooleanProperty, StringProperty, NumericProperty,
                             ObjectProperty)
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    pass


class SearchResults(RecycleView):
    pass


class SearchResult(RecycleDataViewBehavior, BoxLayout):
    index = NumericProperty()
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    title = StringProperty()
    description = StringProperty()
    loan_fee = StringProperty()
    image = StringProperty()
    screen = ObjectProperty()

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''

        if super().on_touch_down(touch):
            return True

        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

        self.screen.update_selected()
