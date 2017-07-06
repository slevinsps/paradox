from menu import MainMenu, Authors, BackgroundLayer
from main import FinalMenu
from cocos.scene import *
from cocos.layer import *


def run_main():
    menu_scene = Scene()
    menu_scene.add(BackgroundLayer())
    menu_scene.add(MultiplexLayer(MainMenu(), Authors()))
    director.run(menu_scene)

if __name__ == '__main__':
    run_main()

