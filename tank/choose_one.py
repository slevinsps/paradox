from pyglet.gl import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
import cocos.actions as ac
import sys, os
import shutil
from cocos.sprite import Sprite
import main
from cocos.text import Label
from cocos.scenes.transitions import FadeTRTransition
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QApplication)

first_file_is_right = 0
second_file_is_right = 0

text1 = 'Ничего не загружено'
text2 = 'Ничего не загружено'


class ChooseOneLayer(Layer):
    def __init__(self, picture):
        super(ChooseOneLayer, self).__init__()
        global text1, text2, first_file_is_right, second_file_is_right
        try:
            self.img = pyglet.resource.image(picture)
        except AttributeError:
            print(AttributeError)

        frame1_image = Sprite("res/frame_black.png")
        frame1_image.position = (180, 300)
        self.add(frame1_image)

        frame2_image = Sprite("res/frame_white.png")
        frame2_image.position = (620, 300)
        self.add(frame2_image)

        if os.path.isfile('files/blue_bot.py') and text1 == 'Ничего не загружено':
            first_file_is_right = 1
            text1 = 'Загружен файл с прошлой игры'
        if os.path.isfile('files/red_bot.py') and text2 == 'Ничего не загружено':
            second_file_is_right = 1
            text2 = 'Загружен файл с прошлой игры'

        if first_file_is_right == 0:
            label1 = Label(text1, color=(255, 0, 0, 255))
        elif first_file_is_right == 1:
            label1 = Label(text1, color=(255, 255, 255, 255))

        if second_file_is_right == 0:
            label2 = Label(text2, color=(255, 0, 0, 255))
        elif second_file_is_right == 1:
            label2 = Label(text2, color=(255, 255, 255, 255))

        label1.position = (40, 460)
        label2.position = (480, 460)

        self.add(label1)
        self.add(label2)

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
        self.font_title['font_size'] = 50
        self.font_title['bold'] = True

        self.item1 = ImageMenuItem('res/download_white.png', self.on_image_callback_red)
        self.item2 = ImageMenuItem('res/download_black.png', self.on_image_callback_blue)

        self.item1.do(ac.ScaleBy(10))
        self.item2.do(ac.ScaleBy(10))

        self.font_item['font_name'] = 'Oswald'
        self.font_item['font_size'] = 20
        self.font_item_selected['font_size'] = 20
        self.font_item_selected['color'] = (255, 255, 255, 1000)

        self.create_menu([self.item1, self.item2], ac.ScaleTo(10.0, duration=0.1), ac.ScaleTo(8, duration=0.1),
                         layout_strategy=fixedPositionMenuLayout([(180, 300), (620, 300),
                                                                  (450, 260), (750, 360)]))

    @staticmethod
    def on_image_callback_red():
        global first_file_is_right, second_file_is_right, text1
        try:
            OpenFile(1)
            first_file_is_right = 1
        except FileNotFoundError:
            first_file_is_right = 0
            text1 = 'Файла не существует'
        except PermissionError:
            first_file_is_right = 0
            text1 = 'Нет доступа к файлу'
        except RuntimeError:
            first_file_is_right = 0
            text1 = 'Превышено время ожидания'
        finally:
            ChooseOneMenu.update_screen(first_file_is_right, second_file_is_right)

    @staticmethod
    def on_image_callback_blue():
        global first_file_is_right, second_file_is_right, text2
        try:
            OpenFile(2)
            second_file_is_right = 1
        except FileNotFoundError:
            second_file_is_right = 0
            text2 = 'Файла не существует'
        except PermissionError:
            second_file_is_right = 0
            text2 = 'Нет доступа к файлу'
        except RuntimeError:
            second_file_is_right = 0
            text2 = 'Превышено время ожидания'
        finally:
            ChooseOneMenu.update_screen(first_file_is_right, second_file_is_right)

    @staticmethod
    def update_screen(first, second):
        if first == 1 and second == 1:
            ChooseOneMenu.redraw('res/back_ground_red_blue.png')
        elif first == 0 and second == 0:
            ChooseOneMenu.redraw('res/back_ground.png')
        elif first == 1 and second == 0:
            ChooseOneMenu.redraw('res/back_ground_red.png')
        elif first == 0 and second == 1:
            ChooseOneMenu.redraw('res/back_ground_blue.png')

    @staticmethod
    def redraw(picture):

        global chooseOneLayer

        layer.remove(chooseOneLayer)
        layer.remove(startGameMenu)
        layer.remove(chooseOneMenu)

        chooseOneLayer = ChooseOneLayer(picture)

        layer.add(chooseOneLayer)
        layer.add(startGameMenu)
        layer.add(chooseOneMenu)


class StartGameMenu(Menu):
    def __init__(self):
        super(StartGameMenu, self).__init__()

        item1 = MenuItem('Старт', self.on_start)
        item2 = MenuItem('Выход', self.on_quit)

        self.font_item['font_name'] = 'Oswald'
        self.font_item['font_size'] = 25

        self.create_menu([item1, item2],
                         layout_strategy=fixedPositionMenuLayout([(400, 120), (400, 70), (500, 100), (500, 50)]))

    @staticmethod
    def on_start():
        global text1, text2
        if os.path.isfile('files/blue_bot.py'):
            if os.path.isfile('files/red_bot.py'):
                main.ConnectionClass.connect_to_tank1(0)
                main.ConnectionClass.connect_to_tank2(0)
                main.ConnectionClass.connect_both_tanks()
                director.replace(FadeTRTransition(main.scene))
            else:
                text1 = 'Ошибка при считывании файла. Загрузите файл еще раз.'
        else:
            text2 = 'Ошибка при считывании файла. Загрузите файл еще раз.'

    @staticmethod
    def on_quit():
        sys.exit(0)


def copy_file(name_of_file, number):
    if number == 1:
        shutil.copy(name_of_file, 'files/blue_bot.py')
    else:
        shutil.copy(name_of_file, 'files/red_bot.py')


class OpenFile(QMainWindow):
    def __init__(self, number):
        super().__init__()

        file = QFileDialog.getOpenFileName(self, caption='Загрузка бота', filter='Py (*.py*)',
                                           initialFilter='Exes (*.exe*.dll)')
        file_name = file[0]

        if number == 1:
            global text1
            text1 = 'Загружен ' + file[0]
        else:
            global text2
            text2 = 'Загружен ' + file[0]

        copy_file(file_name, number)

layer = Scene()

chooseOneLayer = ChooseOneLayer('res/back_ground.png')
startGameMenu = StartGameMenu()
chooseOneMenu = ChooseOneMenu()

layer.add(chooseOneLayer)
layer.add(startGameMenu)
layer.add(chooseOneMenu)

ChooseOneMenu.update_screen(first_file_is_right, second_file_is_right)

app = QApplication(sys.argv)
# sys.exit(0)
