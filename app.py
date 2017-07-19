#! /usr/bin/env python3
import ctypes
import copy
import sys
if sys.platform.startswith('linux'):
    x11 = ctypes.cdll.LoadLibrary('libX11.so')
    x11.XInitThreads()  # Initialise multithreaded program
import gi
import json
import numpy as np
import os
import pyautogui as pa  # Mouse and keyboard event simulator
import pygame           # Initial position of window
import pyscreeze as ps  # Screen analysis
import threading
import time
import random
gi.require_version('Gtk', '3.0')
# from PIL import Image
from collections import OrderedDict
from datetime import datetime
from datetime import datetime, timedelta
from functools import partial
from gi.repository import GLib, Gtk
from math import floor
from random import randint, gauss

from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Rectangle

from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.uix.carousel import Carousel

size = [960, 540]

# from kivy.core.window import Window
# Window.clearcolor = (1, 1, 1, 1)

profiles = {}
active_profile = 0


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        # self._stopper = threading.Event()

    # def stop(self):
    #     self._stopper.set()
    #
    # def stopped(self):
    #     return self._stopper.isSet()
    #
    # def run(self):
    #     self._target(profile=None,
    #                  *self._args, **self._kwargs)
    #     # self._target(self, *self._args, **self._kwargs)

def run_as_thread(instance=None, method=None, cls='action', *args, **kwargs):
    t = StoppableThread(target=method, args=args)
    t.daemon = True
    t.start()

## Challange1: text scales to fit label space without wrapping text
# class BlockLabel(Label):
#     scale_factor = .9
#     factor = dimension = None
#
#     def on_texture_size(self, *args):
#         if not self.factor:
#             self.factor = [self.font_size / self.texture_size[0], self.font_size / self.texture_size[1]]
#         if not self.dimension:
#             self.dimension = 1 if self.texture_size[0] * self.size[1] < self.texture_size[1] * self.size[0] else 0
#         self.font_size = self.size[self.dimension] * self.scale_factor * self.factor[self.dimension]
#
#     def on_texture_size(self, *args):
#         try:
#             if not self.factor:
#                 self.factor = [self.font_size / self.texture_size[0], self.font_size / self.texture_size[1]]
#
#             self.font_size0 = self.size[0] * self.scale_factor * self.factor[0]
#             self.font_size1 = self.size[1] * self.scale_factor * self.factor[1]
#
#             if self.font_size0 < self.font_size1:
#                 self.font_size = self.font_size0
#             else:
#                 self.font_size = self.font_size1
#         except ZeroDivisionError:
#             pass

pages = [('cat.png', 'katinas'), ('car.png', 'mašina'), ('plain.png', 'lėktuvas')]


# class Pannel(FloatLayout):
class Pannel(Carousel):
    def __init__(self, **kwargs):
        super(Pannel, self).__init__(**kwargs)

        global size
        self.size = size

        with self.canvas.before:
            Color(1, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        for source, text in pages:
            box = BoxLayout(orientation='horizontal', padding=20, pos=self.pos, size=self.size)
            img = Image(source=source, size_hint=(0.3, 1))

            label = Label(text=text, size_hint=(0.7, 1), font_size=self.size[0]/7., color=[0,0,0,1], halign='center', valign='middle')
            # label.bind(size=self.update_text_size)

            box.add_widget(img)
            box.add_widget(label)

            self.add_widget(box)


## Challange3: make it work on Android device.

    # def swap_image(self, instance, *args, **kwargs):
    #     # Start animation of cashed button: wait some time idle (0.6 sec), opacity 1
    #     # During same time fade away original button
    #     # Make cashed button original, prepare next cashed button with new image and text
    #     # Image and text database stored in file
    #
    #     animation = Animation(pos=(-200, 0), duration=1.5)
    #     animation &= Animation(opacity=0, duration=0.3)
    #
    #     # animation = Animation(opacity=0, duration=0.3)
    #     #
    #     # animation += Animation(pos=(20, 10), t='out_bounce')
    #     # animation = Animation(size=(50, 50))
    #     # animation += Animation(size=(10, 5))
    #     # animation = Animation(pos=(10, 10), t='out_bounce')
    #     # animation &= Animation(size=(50, 50))
    #     # animation += Animation(size=(10, 5))
    #
    #     # apply the animation on the button, passed in the "instance" argument
    #     # Notice that default 'click' animation (changing the button
    #     # color while the mouse is down) is unchanged.
    #     animation.start(instance)
    #
    #     # time.sleep(0.6)
    #     #
    #     # self.img.source='cat.png'
    #     # self.lb.text='labas'
    #     # animation = Animation(opacity=1, duration=0.3)
    #     # animation.start(instance)
    #
    # def update_pos(self, instance, value):
    #     self.bl.pos = value

    # def update_text_size(self, instance, value):
    #     self.lb.font_size = value[0]/5

    # def update_size(self, instance, value):
    #     # print(self.bl.size, value, instance)
    #     self.bl.size = value


    # def build(self):
    #     # create a button, and  attach animate() method as a on_press handler
    #     button = Button(size_hint=(None, None), text='plop',
    #                     on_press=self.animate)
    #     return button
    #
    #     print('Swapping image')
    #     pass


class PannelApp(App):
    def build(self):
        self.title = ''
        app = Pannel(direction='right', loop=True)
        app.opacity = 1.
        return app

def exit_pannel(*args):
    loop.quit()
    App.get_running_app().stop()

# Image of any dimensions displayed correctly
#


if __name__ == '__main__':
    # Set place where window will appear
    os.environ['SDL_VIDEO_WINDOW_POS'] = "650,500"
    pygame.init()

    # Set window size
    Config.set('graphics', 'width',  size[0])
    Config.set('graphics', 'height', size[1])
    # Turn off orange dot on left click
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

    # Run hotkey bindings
    PannelApp().run()
