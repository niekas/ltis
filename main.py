#! /usr/bin/env python3
import argparse
import configparser
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
# Config.set('graphics', 'width',  960)
Config.set('graphics', 'width',  1080)
Config.set('graphics', 'height', 480)

# po failo updatas: jeigu failas nerastas, tada eilutė užkomentuojama.
# Jeigu rastas failas, kuris dar nebuvo užregistruotas, tada ji pridedamas su
# tuščia simbolių eilute:
# 'animals/dog.png' ''    <-- įrašas
# % 'animals/cat.png' 'katė'
# 'mammals/cat.png' ''
# Jeigu dingo vertimų įrašas, bet atsirado įrašas kitoje kategorijoje su tokiu
# pačiu failo vardu, tada perkelti vertimus iš dingusių įrašų.
# Jeigu žodis turi tuščia eilutę, jis nerodomas naudotojui.
#
# words-lt.po
# words-en.po
# categories-lt.po
# 'animals' 'gyvūnai'
# categories-en.po
# 'animals' 'Animals'


# Categorijos:  # Galima draginti kategorija i virsu, taip pakeliant jos prioriteta
#  v gyvūnai
#  v maistas
#
# Kalbos:       # Todo: kas geriau vieną kalbą ar kelias kalbas iš karto rodyti?
#  v lietuvių
#    anglų
#
# Sound:  on/off

## Kategorijos is pradziu surikiuojamas pagal abecele, o jeigu naudotojas nustato kita prioriteta, tada perrikiuojama pagal prioritetus
# translated_categorised_words_with_images =
# {'en': {'animals': {'title': 'animals', 'words': [('img/words/animals/cat.png', 'cat'), ('img/words/animals/dog.png', 'dog'), ],
#  'lt': OrderedDict({'animals': {'title': 'gyvūnai', 'words': [('img/words/animals/cat.png', 'katė), ('img/words/animals/dog.png', 'šuo'), ],
#          'food': {'name': 'maistas'

# Dumpu kol kas nereikia

# {'animals': {
#   'en': {'animals',
#   'lt': 'gyvūnai',
#   'words-lt'
# }}



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
                words.append((img_path, word_translations[img_path]))

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


        config = configparser.ConfigParser()
        config.read('settings.cfg')
        languages = config['DEFAULT']['languages'].split(',')
        translated_word_categories = load_word_translations(languages=languages)

        main_language = config['DEFAULT']['main_language']

        for key, category in translated_word_categories[main_language].items():
            for img_source, word in category['words']:
                word = '\n'.join(word.split())
                box = BoxLayout(orientation='horizontal', padding=20, pos=self.pos, size=self.size)
                img = Image(source=img_source, size_hint=(0.4, 1))
                label = Label(text=word, size_hint=(0.6, 1), font_size=150., color=[0,0,0,1], halign='center', valign='middle')
                box.add_widget(img)
                box.add_widget(label)
                self.add_widget(box)


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
