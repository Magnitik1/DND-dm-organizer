from kivy.uix.widget import Widget
from kivyutils import load_kv_for

load_kv_for(__file__)

#exported to the tab loader, and instantiated only when accessed
class Example_Tab(Widget):
  pass

#used by the tab module importer
#must be a parameterless widget class
tabmodule_tab_export=Example_Tab