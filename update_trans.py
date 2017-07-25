import configparser
import os


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

## User settings:
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

# {'animals': {
#   'en': {'animals',
#   'lt': 'gyvūnai',
#   'words-lt'
# }}



def update_translations(img_dir='img/words', translation_dir='translations', languages=[]):
    category_keys = os.listdir(img_dir)
    for lang in languages:
        filename = os.path.join('translations', 'categories-%s.tr' % lang)
        if os.path.exists(filename):
            print('exists %s' % filename)
            pass
        else:
            print('Generating %s' % filename)
            with open(filename, 'w') as f:
                for key in category_keys:
                    f.write('%s: \n' % key)

        filename = os.path.join('translations', 'words-%s.tr' % lang)
        if os.path.exists(filename):
            print('exists %s' % filename)
            pass
        else:
            print('Generating %s' % filename)
            with open(filename, 'w') as f:
                for category in category_keys:
                    category_dir = os.path.join(img_dir, category)
                    for img in os.listdir(category_dir):
                        f.write('%s: \n' % (os.path.join(category_dir, img)))



if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    languages = config['DEFAULT']['languages'].split(',')
    update_translations(languages=languages)
