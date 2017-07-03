from menu import MainMenu, Authors,BackgroundLayer
from FinalScene import FinalMenu
from pyglet.gl import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import Sprite
import cocos.actions as ac
from cocos.scenes.transitions import FadeTRTransition

def main():
    menu_scene = Scene()
    back_layer = BackgroundLayer()
    menu_scene.add(back_layer)
    menu_scene.add(MultiplexLayer(MainMenu(), Authors()))
    director.run( menu_scene )

if __name__ == '__main__':
    main()

