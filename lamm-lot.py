from kivy.app import App
from kivy.uix.widget import Widget


class LAMMLoTWindow(Widget):
    pass


class LAMMLoTApp(App):
    def build(self):
        return LAMMLoTWindow()
  

if __name__ == "__main__":
   LAMMLoTApp.run()
