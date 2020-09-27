from kivy import Config

Config.set("graphics", "width", "1200")
Config.set("graphics", "height", "800")
Config.set("graphics", "minimum_width", "800")
Config.set("graphics", "minimum_height", "600")
Config.set("graphics", "multisamples", "4")

import kivy

# kivy.require('1.0.6')
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.clock import Clock

from functools import partial

from pathlib import Path

import numpy as np

import os
import random
import glob
import csv
import chooser
import timer
import buttons
import menu
import session
import settings


class SettingsButton(Button):
    def __init__(self, **kwargs):
        super(SettingsButton, self).__init__(**kwargs)
        self.on_press = self.callback

    def callback(self):
        app = App.get_running_app()
        app.manager.transition.direction = "left"
        app.manager.current = "settings"


class WindowsManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowsManager, self).__init__(**kwargs)

    def go_to_settings(self):
        self.current = "settings"


class RandomPicApp(App):

    main_layout = FloatLayout()
    manager = WindowsManager(transition=NoTransition())

    begin_time = 0

    def build(self):
        self.paths, self.images = self.load_data()
        self.images_count = 0

        self.folder_setting_screen = chooser.FolderSettingScreen(name="folder_setting")

        Window.bind(on_request_close=self.on_request_close)
        self.manager.add_widget(menu.MenuScreen(name="main"))
        # self.manager.add_widget(settings.SettingsScreen(name="settings"))
        self.manager.add_widget(self.folder_setting_screen)
        self.manager.add_widget(chooser.FolderChooserScreen(name="folder_chooser"))
        self.manager.add_widget(session.SessionScreen(name="session"))
        self.main_layout.add_widget(self.manager)
        return self.main_layout

    def on_request_close(self, *args):
        self.textpopup(title="Exit", text="Are you sure?")
        return True
    
    def textpopup(self, title="", text=""):
        box = BoxLayout(orientation="vertical")
        box.add_widget(Label(text=text))
        mybutton = Button(text="OK", size_hint=(1, 0.25))
        box.add_widget(mybutton)
        popup = Popup(title=title, content=box, size_hint=(None, None), size=(600, 300))
        mybutton.bind(on_release=self.app_exit)
        popup.open()

    def get_paths(self):
        return self.paths

    def get_images(self):
        return self.images

    def add_path(self, path):
        if path not in self.paths:
            self.paths[path] = 0 # 
            self.save_paths_csv()
            self.reload_data()
            self.folder_setting_screen.refresh_path_list()
            # self.reload_images()

    def delete_path(self, path):
        if path in self.paths:
            self.paths.pop(path, None)
            self.folder_setting_screen.refresh_path_list()
            self.save_paths_csv()
            self.reload_data()

    def find_images(self, dir_name):
        images = []

        # for ext in ['**/*.png', '**/*.jpg']:
        for img in glob.glob(os.path.join(dir_name, "**/*.jpg"), recursive=True):
            images.append(img)
        return np.array(images)

    def load_images(self):
        images = []
        for path in self.paths:
            images.extend(self.find_images(path))

        return np.array(images)

    def reload_data(self):
        self.paths, self.images = self.load_data()

    def save_paths_csv(self):
        with open(Path("data/paths.csv"), mode="w") as paths_file:
            paths_writer = csv.writer(
                paths_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            for path in self.paths.keys():
                paths_writer.writerow([path])

    def load_data(self):
        paths = dict()
        images = list()
        with open(Path('data/paths.csv'), mode='r') as paths_file:
            paths_reader = csv.reader(paths_file)
            for row in paths_reader:
                if row:
                    path = row[0]
                    images_in_path = self.find_images(path)
                    paths[path] = len(images_in_path)
                    images.extend(images_in_path)

        return paths, np.array(images)

    def get_number_of_imgs(self):
        print(len(self.images))
        return len(self.images)

    def app_exit(self, button):
        # self.save_paths_csv()
        self.stop()


if __name__ == "__main__":
    app = RandomPicApp()
    app.run()
