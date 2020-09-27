from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.image import Image, AsyncImage
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from functools import partial

import vector
import timer
import random
import buttons


Builder.load_string(
    """
#: import StartButton buttons.StartButton
#: import SettingsButton buttons.SettingsButton
#: import RoundedLineButton buttons.RoundedLineButton
#: import BackButton buttons.BackButton
#: import FolderButton buttons.FolderButton
#:import utils kivy.utils

<SettingsScreen>:
    Image:
        source: 'data/icons/background1.png'
        keep_ratio: False
        allow_stretch: True

<SettingsLayout>:
    BackButton:
        pos_hint: {"top": 1}
        size_hint: (0.05, 0.05)
    
    FolderButton:
        pos_hint: {"botton": 1}
        size_hint: (0.05, 0.05)

                    """
)


class SettingsLayout(FloatLayout):

    time_input = ObjectProperty(None)
    start_button = ObjectProperty(None)
    settings_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SettingsLayout, self).__init__(**kwargs)



class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.add_widget(SettingsLayout())