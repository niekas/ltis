#! /usr/bin/env python3
import argparse
import configparser
import random
import os

# import pygame           # Initial position of window
import kivy

from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.carousel import Carousel
from collections import OrderedDict


## Debuging
Config.set('graphics', 'width',  960)
Config.set('graphics', 'height', 480)


def load_word_translations(img_dir='img/words', translations_dir='translations', languages=[]):
    translated_word_categories = OrderedDict()
    for lang in languages:
        # Load category names
        category_titles = {}
        with open(os.path.join(translations_dir, 'categories-%s.tr' % lang)) as f:
            for line in f:
                category_key, category_title = line.split(':')
                category_titles[category_key] = category_title.strip()

        # Load word translations
        word_translations = {}
        with open(os.path.join(translations_dir, 'words-%s.tr' % lang)) as f:
            for line in f:
                word_key, word_translation = line.split(':')
                word_translations[word_key] = word_translation.strip()

        # Load translated words for each category
        categories = OrderedDict()
        for category in sorted(os.listdir(img_dir)):
            words = []
            categories[category] = {'title': category_titles[category], 'words': words}
            for img in os.listdir(os.path.join(img_dir, category)):
                img_path = os.path.join(img_dir, category, img)
                word_translation = word_translations.get(img_path)
                if word_translation:
                    words.append((img_path, word_translation))

        # Todo: Sort OrderedDict by category['title'] in unicode
        # categories = OrderedDict(sorted(categories.items(), key=lambda x: x[1]['title']))

        translated_word_categories[lang] = categories
    return translated_word_categories


class Pannel(Carousel):
    def __init__(self, **kwargs):
        super(Pannel, self).__init__(**kwargs)

        with self.canvas.before:  # White background
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size_hint=(1, 1), size=[2000,2000], pos=self.pos)

        # config = configparser.ConfigParser()
        # config.read('settings.cfg')
        # languages = config['DEFAULT']['languages'].split(',')
        languages = ['lt', 'en']
        translated_word_categories = load_word_translations(languages=languages)

        # main_language = config['DEFAULT']['main_language']
        main_language = 'lt'

        for key, category in translated_word_categories[main_language].items():
            for img_source, word in category['words']:
                word = '\n'.join(word.split())
                box = BoxLayout(orientation='horizontal', padding=20, pos=self.pos, size=self.size)
                img = Image(source=img_source, size_hint=(0.4, 1))
                img.allow_stretch = True
                img.size = [img.size[0] * 10, img.size[1]*10]
                label = Label(text=word, size_hint=(0.6, 1), font_size=134., color=[0,0,0,1], halign='center', valign='middle')
                box.add_widget(img)
                box.add_widget(label)
                self.add_widget(box)

        self.index = random.randint(0, len(self.slides))


class PannelApp(App):
    def on_pause(self):
        # Here you can save data if needed
        return False

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass

    def build(self):
        self.title = ''
        app = Pannel(direction='right', min_move=0.05, loop=True)
        app.opacity = 1.
        return app


if __name__ == '__main__':
    PannelApp().run()
