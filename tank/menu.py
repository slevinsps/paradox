from pyglet.gl import *
from cocos.menu import *
import shutil
import os
import threading
import time
from cocos.actions import*
from cocos.layer import *
from cocos.sprite import Sprite
import cocos.actions as ac
from cocos.scenes.transitions import FadeTRTransition
from choose_one import layer as choose_layer

disconnect = 0

class BackgroundLayer(Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('res/back_ground.png')

        self.red_image = Sprite("res/back_red.png")
        self.red_image.position = (400, 300)
        self.add(self.red_image)

        self.blue_image = Sprite("res/back_blue.png")
        self.blue_image.position = (400, 300)
        self.add(self.blue_image)

        self.red_image.do(FadeOut(0))
        self.blue_image.do(FadeOut(0))

        t = threading.Thread(target=self.play_animation)
        t.start()

    def play_animation(self):
        while True:
            self.red_image.do(FadeOut(2))
            self.blue_image.do(FadeIn(2))
            time.sleep(4)
            self.blue_image.do(FadeOut(2))
            self.red_image.do(FadeIn(2))
            time.sleep(4)


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
        item3 = MenuItem('Авторы', self.on_authors)
        item4 = MenuItem('Выход', self.on_quit)

        self.font_item['font_name'] = 'Times New Roman'
        self.sprite = Sprite('res/back.png')
        self.sprite.position = 0, 0

        self.create_menu([item1, item3, item4], ac.ScaleTo(1.25, duration=0.25), ac.ScaleTo(1.0, duration=0.25))
    @staticmethod
    def on_quit():
        global disconnect
        disconnect = 1
        pyglet.app.exit()

    def on_authors(self):
        self.parent.switch_to(1)

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
        super(Authors, self).__init__("Paradox")

        self.font_title['font_name'] = 'Oswald'
        self.font_title['font_size'] = 50
        self.font_title['bold'] = True

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