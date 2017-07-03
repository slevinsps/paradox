from cocos.layer import *
from cocos.menu import *
from cocos.scene import *
from pyglet.gl import *
from cocos.text import Label
import cocos.actions as Acrions
import sys

class FinalBack(Layer):
    def __init__(self):
        super(FinalBack, self).__init__()
        self.img = pyglet.resource.image('res/background.png')

    def draw(self):
        glColor4ub(255, 255, 255, 255)
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()


class FinalScene(Layer):
    is_event_handler = True

    def __init__(self, winner):
        super(FinalScene, self).__init__()

        text1 = Label("Конец игры", font_name='Oswald', font_size = 25)
        text2 = Label(winner, font_name='Oswald', font_size=25)



        text1.position = director._window_virtual_width / 2 - 90, director._window_virtual_height / 2 + 30
        text2.position = director._window_virtual_width / 2 - 180, director._window_virtual_height / 2 - 20

        self.add(text1)
        self.add(text2)


class FinalMenu(Menu):
    def __init__(self):
        super(FinalMenu, self).__init__()

        self.menu_valign = BOTTOM

        quit_now = MenuItem('Выход', self.on_quit)

        self.font_item['font_name'] = 'Oswald'
        self.font_item['font_size'] = 25

        self.create_menu([quit_now], Acrions.ScaleTo(0.8, duration=0.25),
                         Acrions.ScaleTo(0.7, duration=0.25),
                         layout_strategy=fixedPositionMenuLayout([(400, 150), (130, 150)]))

    @staticmethod
    def on_quit():
        sys.exit()

