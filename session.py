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


Builder.load_string(
    """
#: import StartButton buttons.StartButton
#: import NextButton buttons.NextButton
#: import PreviousButton buttons.PreviousButton
#: import StopButton buttons.StopButton
#: import PauseButton buttons.PauseButton
#: import Timer timer.Timer
<SessionLayout>:
    timer: timer
    picture: picture
    next_button: next_button
    previous_button: previous_button
    stop_button: stop_button
    pause_button: pause_button

    Picture:
        id: picture
        nocache: True

    Timer:
        id: timer
        pos_hint: {"top": 1, "right": 1}
        size_hint: (0.1, 0.1)

    BoxLayout:
        pos_hint: {'center_x':0.5, 'bottom': 1}
        size_hint: (0.4, 0.07)
        spacing: 10
        padding: 10

        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#000000')
                a: 0.6
            RoundedRectangle:
                pos: self.pos
                size: self.size
            
        PreviousButton:
            id: previous_button

        PauseButton:
            id: pause_button

        StopButton:
            id: stop_button

        NextButton:
            id: next_button

                    """
)


class Picture(AsyncImage):
    def __init__(self, **kwargs):
        super(Picture, self).__init__(**kwargs)

    def selected(self, filename):
        if filename:
            self.source = filename
            self.reload()
        else:
            self.source = "test.jpg"


class SessionLayout(FloatLayout):

    timer = ObjectProperty(None)
    picture = ObjectProperty(None)
    next_button = ObjectProperty(None)
    previous_button = ObjectProperty(None)
    stop_button = ObjectProperty(None)
    pause_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SessionLayout, self).__init__(**kwargs)
        app = App.get_running_app()
        self.images = []
        self.timer.set_function(self.next_picture)
        self.next_button.bind(on_press=self.next_picture)
        self.previous_button.bind(on_press=self.previous_picture)
        self.stop_button.bind(on_press=self.stop)
        self.pause_button.bind_pause(self.pause)
        self.pause_button.bind_unpause(self.unpause)

    def start(self, time):
        app = App.get_running_app()
        self.images = vector.Vector(app.get_images())
        self.images.shuffle()
        self.picture.selected(self.images.current())
        self.timer.start(time)

    def end(self):
        self.timer.stop()
        self.timer.reset()

    def pause(self, button=None):
        self.timer.stop()

    def unpause(self, button=None):
        self.timer.unpause()

    def next_picture(self, instance=None):
        next_image = self.images.next()
        if next_image:
            self.picture.selected(next_image)
            self.timer.reset()

    def previous_picture(self, button):
        previous_image = self.images.previous()
        if previous_image:
            self.picture.selected(previous_image)
            self.timer.reset()

    def stop(self, button):
        app = App.get_running_app()
        app.manager.transition.direction = "right"
        app.manager.current = "main"


class SessionScreen(Screen):
    def __init__(self, **kwargs):
        super(SessionScreen, self).__init__(**kwargs)
        self.session_layout = SessionLayout()
        self.add_widget(self.session_layout)

    def on_transition_state(self, instance, value):
        if value == "in":
            app = App.get_running_app()
            self.session_layout.start(app.begin_time)
        else:
            self.session_layout.end()
