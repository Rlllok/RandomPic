from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import Screen, ScreenManager

from functools import partial

import buttons


Builder.load_string('''
#: import Popup kivy.uix.popup
#: import BackButton buttons.BackButton
#: import RemoveButton buttons.RemoveButton

<RecycleViewRow>:
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgb: utils.get_color_from_hex('#0B1624')
            a: 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
    Label:
        size_hint: (0.8, 1)
        text: root.path
    Label:
        size_hint: (0.1, 1)
        text: root.number_of_img
    RemoveButton:
        size_hint: (0.1, 1)
        text: 'Remove'
        on_press: root.parent.parent.delete_data(root.path)

<MainScreen>:
    viewclass: 'RecycleViewRow'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<FolderSettingScreen>:
    Image:
        source: 'data/icons/background1.png'
        keep_ratio: False
        allow_stretch: True

<FolderChooserScreen>:
    Image:
        source: 'data/icons/background1.png'
        keep_ratio: False
        allow_stretch: True
                    ''')


class RecycleViewRow(BoxLayout):
    path = StringProperty()
    number_of_img = StringProperty()

    def __init__(self, **kwargs):
        super(RecycleViewRow, self).__init__(**kwargs)


class MainScreen(RecycleView): 

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.refresh()

    def refresh(self):
        app = App.get_running_app()
        self.data = [{'path': path, 'number_of_img': str(app.paths.get(path))} for path in app.paths]
        self.refresh_from_data()

    def delete_data(self, path):
        app = App.get_running_app()
        app.delete_path(path)


class FolderChooser(FileChooserIconView):

    def __init__(self, **kwargs):
        super(FolderChooser, self).__init__(**kwargs)
        # self.on_selection = self.select_folder
        self.dirselect = True


class FolderChooserScreen(Screen):

    folder_chooser = None

    def __init__(self, **kwargs):
        super(FolderChooserScreen, self).__init__(**kwargs)
        layout = BoxLayout()
        layout.orientation = 'vertical'
        self.folder_chooser = FolderChooser()
        self.folder_chooser.size_hint = (1, 0.8)
        layout.add_widget(self.folder_chooser)
        add_button = Button(text='Add')
        add_button.size_hint = (1, 0.1)
        add_button.background_normal = ''
        add_button.background_color = (0.159, 0.319, 0.52, 0.7)
        add_button.bind(on_press=self.add_path)
        layout.add_widget(add_button)
        back_button = Button()
        back_button.size_hint = (1, 0.1)
        back_button.text = 'Back'
        back_button.background_normal = ''
        back_button.background_color = (0.159, 0.319, 0.52, 0.7)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def add_path(self, button):
        app = App.get_running_app()
        path = self.folder_chooser.selection[0]
        app.add_path(path)
        self.go_back(None)

    def go_back(self, button):
        app = App.get_running_app()
        app.manager.transition.direction = 'right'
        app.manager.current = app.manager.previous()


class FolderSettingLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(FolderSettingLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.folder_list = MainScreen()
        self.folder_list.size_hint = (1, 0.8)
        self.add_widget(self.folder_list)
        add_button = Button()
        add_button.text = 'Add Folder'
        add_button.background_normal = ''
        add_button.bind(on_press=self.add_folder)
        add_button.size_hint = (1, 0.1)
        add_button.background_color = (0.159, 0.319, 0.52, 0.7)
        self.add_widget(add_button)
        back_button = Button(text='Back')
        back_button.size_hint = (1, 0.1)
        back_button.background_normal = ''
        back_button.bind(on_press=self.go_back)
        back_button.background_color = (0.159, 0.319, 0.52, 0.7)
        self.add_widget(back_button)

    def refresh_folder_list(self):
        self.folder_list.refresh()

    def add_folder(self, button):
        app = App.get_running_app()
        app.manager.transition.direction = 'left'
        app.manager.current = 'folder_chooser'

    def go_back(self, button):
        app = App.get_running_app()
        app.manager.transition.direction = 'right'
        app.manager.current = app.manager.previous()


class FolderSettingScreen(Screen):

    def __init__(self, **kwargs):
        super(FolderSettingScreen, self).__init__(**kwargs)
        self.folder_setting_layout = FolderSettingLayout()

        self.add_widget(self.folder_setting_layout)

    def refresh_path_list(self):
        self.folder_setting_layout.refresh_folder_list()


        
        
