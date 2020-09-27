from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton, ToggleButtonBehavior
from kivy.uix.button import ButtonBehavior
from kivy.uix.textinput import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.effectwidget import EffectWidget
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.graphics import Canvas, Color, RoundedRectangle
from kivy.properties import ListProperty


Builder.load_string(
    """
#: import ew kivy.uix.effectwidget
#:import utils kivy.utils

<MyButton>:
    background_color: (0,0,0,0)
    background_normal: ''
    back_color: (1,0,1,1)
    border_radius: [18]
    canvas.before:
        Color:
            rgba: self.back_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: self.border_radius
            
<RoundedLineButton>:
    background_color: (0,0,0,0)
    background_normal: ''
    border_radius: 18
    color: self.back_color
    bold: True
    canvas.before:
        Color:
            rgba: self.back_color
        Line:
            rounded_rectangle: (self.pos[0], self.pos[1], self.size[0], self.size[1], self.border_radius)
            width: 1.2

<TimeButton>:
    background_color: (0,0,0,0)
    background_normal: ''
    border_radius: 18
    color: self.back_color
    bold: True
    group: 'time'
    canvas.before:
        Color:
            rgba: self.back_color
        Line:
            rounded_rectangle: (self.pos[0], self.pos[1], self.size[0], self.size[1], self.border_radius)
            width: 1.2

<TimeInput>:
    background_color: (0,0,0,0)
    background_normal: ''
    border_radius: 18
    color: self.back_color
    bold: True
    halign: 'center'
    padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
    group: 'time'
    canvas.before:
        Color:
            rgba: self.back_color
        Line:
            rounded_rectangle: (self.pos[0], self.pos[1], self.size[0], self.size[1], self.border_radius)
            width: 1.2
"""
)


class RoundedLineButton(Button):
    def __init__(self, **kwargs):
        super(RoundedLineButton, self).__init__(**kwargs)
        self.back_color = (0.159, 0.319, 0.52, 0.7)

    def color_down(self):
        self.back_color = (1, 0, 0, 1)

    def color_up(self):
        self.back_color = (0.157, 0.455, 0.753, 1.0)


class CancelButton(RoundedLineButton):
    def __init__(self, **kwargs):
        super(CancelButton, self).__init__(**kwargs)
        self.text = "Cancel"


class TimeButton(ToggleButton):

    back_color = ListProperty([])

    def __init__(self, **kwargs):
        super(TimeButton, self).__init__(**kwargs)
        self.back_color = (0.159, 0.319, 0.52, 0.7)
        self.bind(state=self.change_state)

    def change_state(self, button, value):
        if self.state == "down":
            self.back_color = (0.319, 0.52, 0.159, 0.8)
            app = App.get_running_app()
            app.begin_time = int(self.text)
        else:
            self.back_color = (0.159, 0.319, 0.52, 0.7)


class TimeInput(TextInput, ToggleButtonBehavior):
    back_color = ListProperty([])

    def __init__(self, **kwargs):
        super(TimeInput, self).__init__(**kwargs)
        self.multiline = False
        self.input_filter = "int"
        self.back_color = (0.159, 0.319, 0.52, 0.7)
        self.bind(state=self.change_state)
        self.bind(focus=self.on_foc)
        self.bind(text=self.on_t)

    def on_t(self, instance, value):
        app = App.get_running_app()
        if self.text is not "":
            app.begin_time = int(self.text)

    def change_state(self, button, value):
        if self.state == "down":
            self.back_color = (0.319, 0.52, 0.159, 0.8)
            self.focus = True
        else:
            self.back_color = (0.159, 0.319, 0.52, 0.7)
            self.focus = False

    def on_foc(self, insd, value):
        if value:
            self._release_group(self)
            self.state = "down"
        else:
            pass

    def release_group(self):
        widgets = self.get_widgets(self.group)

        if widgets is None:
            return
        for widget in widgets:
            if widget is self:
                continue
            widget.state = "normal"


class IconButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(IconButton, self).__init__(**kwargs)


class NextButton(IconButton):
    
    def __init__(self, **kwargs):
        super(NextButton, self).__init__(**kwargs)
        self.source = 'data/icons/next.png'

class PreviousButton(IconButton):
    
    def __init__(self, **kwargs):
        super(PreviousButton, self).__init__(**kwargs)
        self.source = 'data/icons/previous.png'

class StopButton(IconButton):
    
    def __init__(self, **kwargs):
        super(StopButton, self).__init__(**kwargs)
        self.source = 'data/icons/stop.png'


class StartButton(RoundedLineButton):
    def __init__(self, **kwargs):
        super(StartButton, self).__init__(**kwargs)
        self.text = "Start"


class PauseButton(ToggleButtonBehavior, Image):

    def __init__(self, do_pause=None, do_unpause=None, **kwargs):
        super(PauseButton, self).__init__(**kwargs)
        self.source = 'data/icons/pause.png'
        self.do_pause = do_pause
        self.do_unpause = do_unpause
        self.bind(state=self.change_state)

    def bind_pause(self, func):
        self.do_pause = func

    def bind_unpause(self, func): 
        self.do_unpause = func    

    def change_state(self, button, value):
        if self.state == "down":
            self.source = 'data/icons/play.png'
            if self.do_pause:
                self.do_pause()
        else:
            self.source = 'data/icons/pause.png'
            if self.do_unpause:
                self.do_unpause()


class SettingsButton(RoundedLineButton):
    def __init__(self, **kwargs):
        super(SettingsButton, self).__init__(**kwargs)
        self.on_press = self.callback
        self.text = 'Settings'

    def callback(self):
        app = App.get_running_app()
        app.manager.transition.direction = "left"
        app.manager.current = "settings"


class BackButton(RoundedLineButton):
    def __init__(self, **kwargs):
        super(BackButton, self).__init__(**kwargs)
        self.text = "Back"
        self.on_press = self.callback

    def callback(self):
        app = App.get_running_app()
        app.manager.transition.direction = "right"
        app.manager.current = app.manager.previous()


class FolderButton(RoundedLineButton):
    def __init__(self, **kwargs):
        super(FolderButton, self).__init__(**kwargs)
        self.text = 'Folder'
        self.on_press = self.callback

    def callback(self):
        app = App.get_running_app()
        app.manager.transition.direction = 'left'
        app.manager.current = 'folder_setting'

class AddFolderButton(RoundedLineButton):
    def __initi(self, **kwargs):
        super(AddFolderButton, self).__init__(**kwargs)
        self.text = 'Add'
        self.on_press = self.callback

    def callback(self):
        app = App.get_running_app()
        app.manager.current = 'folder_chooser'

class RemoveButton(RoundedLineButton):
    def __init__(self, **kwargs):
        super(RemoveButton, self).__init__(**kwargs)
        self.back_color = (0.65098039, 0.16862745, 0.23921569, 1)