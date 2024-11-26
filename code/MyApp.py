from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ObjectProperty)
import myconfig
import json
import TabsWidget
from kivy.core.window import Window

class MyApp(App):
    def build(self):
        Window.size = (1050, 700)
        tabsWidget=TabsWidget.TabsWidget()
        tabsWidget.load_default_tabs()
        return tabsWidget
