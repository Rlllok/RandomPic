from kivy.uix.label import Label
from kivy.clock import Clock 
  

class Timer(Label):
      
    def __init__(self, func=None, **kwargs): 
        super(Timer, self).__init__(**kwargs)
        self.begin_time = 0
        self.time = 0
        self.text = str(self.time)
        self.to_do_func = func
        # self.start()

    def dicrement_time(self, interval):
        self.time -= 1
        if self.to_do_func:
            if self.time == 0:
                self.to_do_func()
        self.text = str(self.time)
  
    def start(self, begin_time):
        self.begin_time = begin_time
        self.reset()
        Clock.unschedule(self.dicrement_time)
        Clock.schedule_interval(self.dicrement_time, 1)
  
    def stop(self): 
        Clock.unschedule(self.dicrement_time)

    def unpause(self):
        Clock.schedule_interval(self.dicrement_time, 1)

    def reset(self):
        self.time = self.begin_time
        self.text = str(self.time)

    def set_function(self, func):
        self.to_do_func = func

