from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ObjectProperty)
import config
import json

data = ""
with open('./code/localization.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


class MyGrid(BoxLayout):
    redBtn = ObjectProperty(None)
    lastRedBtn = None
    translation = data[config.language]

    def on_redBtn(self, i, btn):
        btn.background_color = (0.0, 0.0, 1.0, 1.0)
        if self.lastRedBtn is not None:
            self.lastRedBtn.background_color = (0.0, 1.0, 0.0, 1.0)
        self.lastRedBtn = btn

    def campaign(self, text, btn):
        self.ids.label1.text = text
        self.redBtn = btn


class MyApp(App):
    def build(self):
        return MyGrid()
