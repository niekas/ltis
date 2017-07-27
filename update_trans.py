import configparser
import os


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
                    f.write('%s=\n' % key)

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
                        f.write('%s=\n' % (os.path.join(category_dir, img)))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    languages = config['DEFAULT']['languages'].split(',')
    update_translations(languages=languages)
