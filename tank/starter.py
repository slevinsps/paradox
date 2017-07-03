from menu import MainMenu, Authors, BackgroundLayer
from FinalScene import FinalMenu
from cocos.scene import *
from cocos.layer import *


def main():
    menu_scene = Scene()

    menu_scene.add(BackgroundLayer())
    menu_scene.add(MultiplexLayer(MainMenu(), Authors(), FinalMenu()))
    director.run(menu_scene)

if __name__ == '__main__':
    main()

