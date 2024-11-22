from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ObjectProperty)
import myconfig
import json
import TabsWidget

class MyApp(App):
    def build(self):
        tabsWidget=TabsWidget.TabsWidget()
        tabsWidget.load_default_tabs()
        return tabsWidget
