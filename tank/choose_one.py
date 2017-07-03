from pyglet.gl import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
import cocos.actions as ac
import sys, os
import shutil
from cocos.scenes.transitions import FadeTRTransition
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QApplication)


class ChooseOneLayer(Layer):
    def __init__(self):
        super(ChooseOneLayer, self).__init__()
        self.img = pyglet.resource.image('res/background.png')

    def draw( self ):
        glColor4ub(255, 255, 255, 255)
        glPushMatrix()
        self.transform()
        self.img.blit(0,0)
        glPopMatrix()


class ChooseOneMenu(Menu):

    def __init__(self):
        super(ChooseOneMenu, self).__init__("Загрузка ботов")

        self.font_title['font_name'] = 'Oswald'
        self.font_title['font_size'] = 15
        self.font_title['bold'] = True

        item1 = MenuItem('Красный бот', self.on_image_callback_red)
        item2 = MenuItem('Синий бот', self.on_image_callback_blue)

        self.font_item['font_name'] = 'Oswald'
        self.font_item['font_size'] = 20
        self.font_item_selected['font_size'] = 20
        self.font_item_selected['color'] = (255, 255, 255, 1000)

        self.create_menu([item1, item2], ac.ScaleTo(1.0, duration=0.25), ac.ScaleTo(0.8, duration=0.25),
                         layout_strategy=fixedPositionMenuLayout([(150, 400), (650, 400),
                                                                  (450, 260), (750, 360)]))

    def on_image_callback_red(self):
        print('image')
        try:
            open('dest/red_bot.py')


        except FileNotFoundError:
            pass
        except PermissionError:
            pass
        except RuntimeError:
            pass

        print('red_choose')


    def on_image_callback_blue(self):
        print('image2')
        try:
            open('dest/blue_bot.py')

        except FileNotFoundError:
            pass
        except PermissionError:
            pass
        except RuntimeError:
            pass

        print('blue_choose')


class Start_game_menu(Menu):
    def __init__(self):
        super(Start_game_menu, self).__init__()

        item1 = MenuItem('Старт', self.on_start)
        item2 = MenuItem('Выход', self.on_quit)

        self.font_item['font_name'] = 'Oswald'
        self.font_item['font_size'] = 25

        self.create_menu([item1, item2],
                         layout_strategy=fixedPositionMenuLayout([(400, 120), (400, 70), (500, 100), (500, 50)]))

    def on_start(self):
        if os.path.isfile('dest/blue_bot.py'):
            if os.path.isfile('dest/red_bot.py'):
                from main import scene
                director.replace(FadeTRTransition(scene))
                print('start')
            else:
                print('Noo')
        else:
            print('Noo')

    def on_quit(self):
        sys.exit()


class OpenFile(QMainWindow):
    def __init__(self, name):
        super().__init__()

        file = QFileDialog.getOpenFileName(self, caption='Загрузка бота', filter='Py (*.py*.dll)',
                                           initialFilter='Exes (*.exe*.dll)')
        fileName = file[0]
        shutil.copy(fileName, name)

def open(name):
    print('open')
    OpenFile(name)
    director.run(layer)

layer = Scene()
layer.add(ChooseOneLayer())
layer.add(Start_game_menu())
layer.add(ChooseOneMenu())

app = QApplication(sys.argv)

