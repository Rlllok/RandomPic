from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup

Builder.load_string('''
<RecycleViewRow>:
    orientation: 'horizontal'
    Label:
        text: root.text
    Button:
        text: 'Show'
        on_press: app.root.message_box(root.text)

<MainScreen>:
    viewclass: 'RecycleViewRow'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'                    
                    ''')   


class RecycleViewRow(BoxLayout):
    text = StringProperty()


class FolderListRecycle(RecycleView):    
    def __init__(self, **kwargs):
        super(FolderListRecycle, self).__init__(**kwargs)
        self.data = [{'text': "Button " + str(x), 'id': str(x)} for x in range(3)]