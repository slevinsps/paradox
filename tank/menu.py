from pyglet.gl import *
from cocos.menu import *
import shutil
import os
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import Sprite
import cocos.actions as ac
from cocos.scenes.transitions import FadeTRTransition
from main import scene as new_game
from choose_one import layer as choose_layer


class BackgroundLayer(Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('res/background.png')

    def draw(self):
        glColor4ub(255, 255, 255, 255)
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()


class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Меню')

        self.font_title['font_name'] = 'Oswald'
        self.font_title['font_size'] = 35
        self.font_title['bold'] = True

        item1 = MenuItem('Начать игру', self.on_play)
        item2 = MenuItem('Инструкция', self.on_instructions)
        item3 = MenuItem('Авторы', self.on_authors)
        item4 = MenuItem('Выход', self.on_quit)

        self.font_item['font_name'] = 'Times New Roman'
        self.sprite = Sprite('res/back.jpg')
        self.sprite.position = 0, 0

        self.create_menu([item1, item2, item3, item4], ac.ScaleTo(1.25, duration=0.25), ac.ScaleTo(1.0, duration=0.25))
    @staticmethod
    def on_quit():
        pyglet.app.exit()

    def on_authors(self):
        self.parent.switch_to(1)

    @staticmethod
    def on_play():
        director.replace(FadeTRTransition(new_game, duration=2))

    def on_instructions(self):
        pass

    def on_play(self):
        try:
            shutil.rmtree('dest')
        except FileNotFoundError:
            pass
        try:
            os.mkdir('dest')
        except OSError:
            pass
        director.replace(FadeTRTransition(choose_layer, duration=2))


class Authors(Menu):
    def __init__(self):
        super(Authors, self).__init__()

        auth_1 = MenuItem(' Константин Чимпоеш ', self.on_callback)
        auth_2 = MenuItem(' Доктор Артём', self.on_callback)
        auth_3 = MenuItem(' Спасенов Иван', self.on_callback)
        auth_4 = MenuItem(' Васильев Никита', self.on_callback)

        back_item = ImageMenuItem('res/back.png', self.on_back)
        self.create_menu([auth_1, auth_2, auth_3, auth_4, back_item], ac.ScaleTo(1.25, duration=0.25),
                         ac.ScaleTo(1.0, duration=0.25))

    def on_callback(self):
        pass

    def on_back(self):
        self.parent.switch_to(0)
