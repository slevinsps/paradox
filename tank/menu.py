from pyglet.gl import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import Sprite
import cocos.actions as ac
from cocos.scenes.transitions import FadeTRTransition
from main import scene as new_game
from choose_one import layer


class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Меню')

        self.font_title['font_name'] = 'Oswald'
        self.font_title['font_size'] = 50
        self.font_title['bold'] = True

        item1 = ImageMenuItem('res/menu_start.png', self.on_play)
        item2 = MenuItem('Авторы', self.on_authors)
        item3 = MenuItem('Выход', self.on_quit)

        self.font_item['font_name'] = 'Times New Roman'
        self.sprite = Sprite('res/back.jpg')
        self.sprite.position = 0, 0

        self.create_menu([item1, item2, item3], ac.ScaleTo(1.25, duration=0.25), ac.ScaleTo(1.0, duration=0.25))

    def on_quit(self):
        pyglet.app.exit()

    def on_authors(self):
        self.parent.switch_to(1)

    def on_play(self):
        #new_game.add(layer)
        director.run(FadeTRTransition(new_game, duration=2))
        print('on_play')


class Authors(Menu):
    def __init__(self):
        super(Authors, self).__init__()

        auth_1 = MenuItem(' Константин Чимпоеш ', self.on_callback)
        auth_2 = MenuItem(' Доктор Артём', self.on_callback)
        auth_3 = MenuItem(' Спасенов Иван', self.on_callback())
        auth_4 = MenuItem(' Васильев Никита', self.on_callback())

        back_item = ImageMenuItem('res/back.png', self.on_back)
        self.create_menu([auth_1, auth_2, auth_3, auth_4, back_item], ac.ScaleTo(1.25, duration=0.25),
                         ac.ScaleTo(1.0, duration=0.25))

    def on_callback(self):
        print('item callback')

    def on_back(self):
        self.parent.switch_to(0)
