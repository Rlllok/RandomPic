from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty

from kivy.lang.builder import Builder

import buttons


Builder.load_string(
    """
#: import StartButton buttons.StartButton
#: import SettingsButton buttons.SettingsButton
#: import RoundedLineButton buttons.RoundedLineButton
#: import TimeButton buttons.TimeButton
#: import TimeInput buttons.TimeInput
#:import utils kivy.utils

<MenuScreen>:
    Image:
        source: 'data/icons/background1.png'
        keep_ratio: False
        allow_stretch: True

<MenuLayout>:
    time_input: time_input
    start_button: start_button
    settings_button: settings_button

    BoxLayout:
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        size_hint: (0.7, 0.7)
        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#060d15')
                a: 0.8
            Rectangle:
                pos: self.pos
                size: self.size
    BoxLayout:
        pos_hint: {'center_x':0.5, 'center_y':0.6}
        size_hint: (0.4, 0.1)
        spacing: 10
        padding: 10
        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#0B1624')
                a: 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
        TimeButton:
            text: '30'
            group: 'time'
        TimeButton:
            text: '60'
            group: 'time'
        TimeButton:
            text: '120'
            group: 'time'
        TimeButton:
            text: '300'
            group: 'time'
        TimeButton:
            text: '600'
            group: 'time'
        TimeInput:
            id: time_input
            text: '0'
            group: 'time'
        

    BoxLayout:
        orientation: 'horizontal'
        pos_hint: {'center_x':0.5, 'center_y':0.4}
        size_hint: (0.5, 0.1)
        spacing: 10 
            
        StartButton:
            id: start_button
            size_hint: (0.9, 1)
        FolderButton:
            id: settings_button
            size_hint: (0.1, 1)
    Label:
        text: root.number_of_imgs
                    """
)


class MenuLayout(FloatLayout):

    time_input = ObjectProperty(None)
    start_button = ObjectProperty(None)
    settings_button = ObjectProperty(None)
    number_of_imgs = StringProperty()

    def __init__(self, **kwargs):
        super(MenuLayout, self).__init__(**kwargs)

        self.start_button.bind(on_press=self.start_session)
        app = App.get_running_app()
        self.number_of_imgs = str(app.get_number_of_imgs())
        # self.settings_button.bind(on_press=self.go_to_settings)

    def start_session(self, button):
        app = App.get_running_app()
        
        if len(app.get_paths().keys()) == 0: # if paths is empty
            print('Empty paths')
            return
        else:
            if app.get_images().size == 0: # if images is empty
                print('Empty images')
                return

        if app.begin_time == 0:
            print("Choose time")
            return
        app.manager.transition.direction = "left"
        app.manager.current = "session"

    def go_to_settings(self, button):
        app = App.get_running_app()
        app.manager.transition.direction = "left"
        app.manager.current = "settings"

    def update(self):
        app = App.get_running_app()
        self.number_of_imgs = app.get_number_of_imgs()

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.add_widget(MenuLayout())
