from __future__ import annotations

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.event import EventDispatcher
from kivy.properties import (
  ObjectProperty,
  ListProperty,
  StringProperty,
  BooleanProperty,
  ColorProperty
  )

from kivyutils import load_kv_for

import importlib as _importlib

import typing

import functools

#The keys for the translated text used in tab name display
tabmodule_IDs=["Campaign","NPC","fight","notepad","music","spells","equipment"]

#The names of the folders fo the modules in ./tabmodules
def to_tabmodule_names(tabmodule_IDs):
  return map(lambda id: id.lower(),tabmodule_IDs)

load_kv_for(__file__)

from dataclasses import (dataclass,field)
import weakref
import abc
  
class _TabMenuBarButton(Button):
  def __init__(self,tabmodule_ID:str,**kwargs):
    self.tabmodule_ID=tabmodule_ID
    #Super after assignment,
    #because otherwise the button tries to get text translation for an empty id
    super().__init__(**kwargs)
  tabmodule_ID:str = StringProperty()
  is_selected:bool = BooleanProperty(False)
  background_selected = ColorProperty((0.0, 0.0, 1.0, 1.0))
  background_default = ColorProperty((0.0, 1.0, 0.0, 1.0))

@dataclass
class Tab:
  """A class that represents a single tab"""
  tabmodule_ID:str
  tabmodule_Widget:Widget
  _assigned_Button = typing.cast(_TabMenuBarButton,None)


class TabsWidget(BoxLayout,Widget):
  """Displays a menu for switching tabs,
     as well as the content of the selected one,
     content is represented by a `Widget`"""
  #Going through a fake cast, because
  #ListProperty doesn't have typing information, for some reason
  tabs = typing.cast(list[Tab],ListProperty())
  _tabs_by_IDs:dict[str,Tab]

  @staticmethod
  def on_tabs(inst:TabsWidget,tabs:list[Tab]):
    menu_bar:Widget=inst.ids.tabs_menu_bar
    menu_bar.clear_widgets()
    inst._tabs_by_IDs.clear()
    if len(inst.tabs) < 0:
      return
    for tab in tabs:
      btn = _TabMenuBarButton(tab.tabmodule_ID)
      btn.on_press = functools.partial(inst.on_tabmenubarbutton_press,btn)
      menu_bar.add_widget(btn)
      tab._assigned_Button = weakref.proxy(btn)
      inst._tabs_by_IDs[tab.tabmodule_ID]=tab
    if inst.selected_tab is None:
      inst.selected_tab=inst.tabs[0]
    
  def on_tabmenubarbutton_press(self,btn):
    #select tab.
    self.selected_tab = self._tabs_by_IDs[btn.tabmodule_ID]


  selected_tab = ObjectProperty(None)
  selected_tab_previous:Tab|None = None

  @staticmethod
  def on_selected_tab(inst:TabsWidget,tab:Tab):
    #SwitchButtonColors
    if inst.selected_tab_previous is not None:
      inst.selected_tab_previous._assigned_Button.is_selected=False
    tab._assigned_Button.is_selected=True
    #ContentAreaSwitch
    content_area:Widget=inst.ids.content_area
    content_area.clear_widgets()
    content_area.add_widget(tab.tabmodule_Widget)
    #end
    inst.selected_tab_previous=tab

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._tabs_by_IDs={}

  def load_default_tabs(self):
    self.tabs=load_tabmodules(tabmodule_IDs)



def load_tabmodules(tabmodule_IDs=tabmodule_IDs):
  tabmodule_names = to_tabmodule_names(tabmodule_IDs)
  tabs:list[Tab] = []
  for [tabmodule_ID,tabmodule_name] in zip(tabmodule_IDs,tabmodule_names):
    tabmodule=_importlib.import_module("tabmodules."+tabmodule_name, package=None)
    #instantiate the exported class
    tab_Widget:Widget=tabmodule.tabmodule_tab_export()
    tabs.append(Tab(tabmodule_ID,tab_Widget))
  return tabs