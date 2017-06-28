from pyglet.gl import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *

class MainMenu(Menu):
    def __init__( self ):
        super( MainMenu, self ).__init__()

        item1 = ImageMenuItem('res/menu_start.jpg', self.on_play)
        item2 = MenuItem('Авторы', self.on_authors)
        item3 = MenuItem('Выход', self.on_quit )

        self.create_menu( [item1,item2,item3] )


    def on_quit( self ):
        pyglet.app.exit()

    def on_authors(self):
        director.run(Scene(Authors()))

    def on_play(self):
        # Здесь будет переход к игровой сцене
        print('image item callback')

class Authors(Menu):
    def __init__(self):
        super( Authors, self).__init__()

        auth_1 = MenuItem(' Константин Чимпоеш ', self.on_callback)
        auth_2 = MenuItem(' Доктор Артём', self.on_callback)
        auth_3 = MenuItem(' Спасенов Иван', self.on_callback())

        back_item = ImageMenuItem('res/back.png', self.on_back)
        self.create_menu([auth_1, auth_2, auth_3, back_item])

    def on_callback(self):
        print('item callback')

    def on_back(self):
        pyglet.app.exit()
        director.run(Scene(MainMenu()))


def main():

    director.init()
    director.run( Scene( MainMenu() ) )

if __name__ == '__main__':
    main()