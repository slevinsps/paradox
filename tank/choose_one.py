from pyglet.gl import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
import cocos.actions as Acrions

#director.init(width=800, height=600, autoscale=False, resizable=True)

class ChooseOneLayer(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(ChooseOneLayer, self).__init__(115, 207, 57, 1000)


class ChooseOneMenu(Menu):

    def __init__(self):
        super(ChooseOneMenu, self).__init__("Загрузка ботов")

        self.font_title['font_name'] = 'Oswald'
        self.font_title['font_size'] = 50
        self.font_title['bold'] = True

        item1 = ImageMenuItem('res/red_button.png', self.on_image_callback)
        item2 = ImageMenuItem('res/blue_button.png', self.on_image_callback)
        item3 = MenuItem('Главное меню', self.on_main)
        #item4 = MenuItem('Выход', self.on_exit)

        self.font_item['font_name'] = 'Oswald'
        self.font_item['font_size'] = 25

        self.create_menu([item1, item2, item3], Acrions.ScaleTo(0.8, duration=0.25),
                         Acrions.ScaleTo(0.7, duration=0.25),
                         layout_strategy=fixedPositionMenuLayout([(150, 400), (650, 400), (400, 200),
                                                                  (250, 360), (750, 360), (130, 180)]))

    def on_image_callback(self):
        print('image')

    def on_main(self):
        from starter import main
        main()

    #def on_exit(self):
    #    pyglet.app.exit()

#def download_file():


layer  = Scene()
back_layer = ChooseOneLayer()
back_layer.opacity = 40
layer.add(back_layer)
layer.add(ChooseOneMenu())
