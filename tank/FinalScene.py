from cocos.layer import *
from cocos.menu import *
from cocos.scene import *
from cocos.text import Label
import cocos.actions as Acrions
from cocos.scenes.transitions import FadeTRTransition


class FinalScene(ColorLayer):
    is_event_handler = True

    def __init__(self, winner):
        super(FinalScene, self).__init__(115, 207, 57, 1000)

        text1 = Label("Конец игры", font_name='Oswald', font_size = 25)
        text2 = Label("Выиграл " + winner + " танк", font_name = 'Oswald', font_size = 25)
        text1.position = director._window_virtual_width / 2 - 90, director._window_virtual_height / 2 + 30
        text2.position = director._window_virtual_width / 2 - 180, director._window_virtual_height / 2 - 20

        self.add(text1)
        self.add(text2)


class FinalMenu(Menu):
    def __init__(self):
        super(FinalMenu, self).__init__()

        self.menu_valign = BOTTOM

        main_menu = MenuItem('Главное меню', self.on_menu)
        Quit = MenuItem('Выход', self.on_qiut)

        self.font_item['font_name'] = 'Oswald'
        self.font_item['font_size'] = 25

        self.create_menu([main_menu, Quit], Acrions.ScaleTo(0.8, duration=0.25),
                         Acrions.ScaleTo(0.7, duration=0.25),
                         layout_strategy=fixedPositionMenuLayout([(400, 200), (400, 150), (130, 180), (130, 150)]))

    def on_menu(self):
        from starter import main
        main()


    def on_qiut(self):
        pyglet.app.exit()

