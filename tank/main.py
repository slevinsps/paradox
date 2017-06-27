# Imports as usual
from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.layer import ScrollingManager, ScrollableLayer
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer
import math
import time
import cocos.actions as Acrions
from cocos.text import Label
from cocos.actions import Driver
from pyglet.window import key
from pyglet.window import mouse

director.init(width=800, height=600, autoscale=False, resizable=True)

keyboard = key.KeyStateHandler()
m = key.KeyStateHandler

scroller = ScrollingManager()

# Координаты тела первого танка
tank1_body_position_x = 0
tank1_body_position_y = 0
tank1_body_rotation = 0

# Координаты пушки первого танка
tank1_gun__rotation = 0

# Здороваье и урон первого танка
tank1_health = 10
tank1_damage = 3

#перемнная для времени
time_point1 = 0

# Управление надписью 'перезарядка'
class TextDriver1(Driver):
    def step(self, dt):
        global tank1_body_position_x
        global tank1_body_position_y
        global tank1_gun_rotation

        super(TextDriver1, self).step(dt)

        self.target.x = tank1_body_position_x
        self.target.y = tank1_body_position_y

# Управление дулом пушки первого тела
class tankGunDriver1 (Driver):
    def step(self, dt):
        global tank1_body_position_x
        global tank1_body_position_y
        global tank1_gun_rotation
        global tank1_body_rotation

        super(tankGunDriver1, self).step(dt)
        self.target.rotation += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 60 * dt
        tank1_gun_rotation = self.target.rotation

        self.target.x = tank1_body_position_x
        self.target.y = tank1_body_position_y

# Управление полётом ракеты первого тела
class tankBulletDriver1 (Driver):
    def step(self, dt):
        global tank1_body_position_x
        global tank1_body_position_y

        super(tankBulletDriver1, self).step(dt)
        self.target.speed = 500

# Управление телом первого танка
class tankBodyDriver1 (Driver):
    def step(self, dt):
        global tank1_body_position_x
        global tank1_body_position_y
        global tank1_body_rotation

        self.target.rotation += (keyboard[key.D] - keyboard[key.A]) * 30 * dt
        self.target.acceleration = (keyboard[key.W] - keyboard[key.S]) * 350

        if keyboard[key.ENTER]:
            self.target.speed = 0

        super(tankBodyDriver1, self).step(dt)

        tank1_body_position_x = self.target.x
        tank1_body_position_y = self.target.y

        tank1_body_rotation = self.target.rotation

        scroller.set_focus(self.target.x, self.target.y)


class MouseInput(ScrollableLayer):
    is_event_handler = True
    def __init__(self):
        super(MouseInput, self).__init__()

        self.position_x = 0
        self.position_y = 0
        self.j = 0

        self.sprite_array = [Sprite("res/bullet.png"), Sprite("res/bullet.png"), Sprite("res/bullet.png")];
        for i in range(len(self.sprite_array)):
            self.sprite_array[i].position = 200, 100
            self.sprite_array[i].do(Acrions.FadeOut(0))
            self.add(self.sprite_array[i])

        self.text = Label("Перезарядка",
                          font_name = "Helvetica",
                          font_size = 10,
                          x = 100,
                          y = 0)

        self.text.do(Acrions.FadeOut(0))

        self.sprite = Sprite("res/tank_pushka.png")

        self.text.do(TextDriver1())

        self.sprite.position = 200, 100

        self.add(self.sprite)
        self.add(self.text)
        self.sprite.do(tankGunDriver1())

    def on_key_press(self, key, modifiers):
        if key == 32:
            global tank1_body_position_x
            global tank1_body_position_y
            global tank1_body_rotation
            global tank1_gun_rotation
            global time_point1

            time_point2 = time.clock()

            if time_point1==0:
                time_point1 = time.clock()
                self.push_bullet()
            else:
                if time_point2 - time_point1 > 1:
                    self.push_bullet()
                    time_point1 = time.clock()

    def push_bullet(self):
        global tank1_body_position_x
        global tank1_body_position_y

        if self.j>=len(self.sprite_array):
            while self.j > 0:
                self.j -= 1
                self.sprite_array[self.j].stop()
                self.sprite_array[self.j].do(Acrions.FadeOut(0))
                #self.sprite_array[self.j].do(Acrions.MoveTo((tank1_body_position_x, tank1_body_position_y), 0.1))

        if self.j < len(self.sprite_array):

            self.sprite_array[self.j].x = tank1_body_position_x
            self.sprite_array[self.j].y = tank1_body_position_y

            self.sprite_array[self.j].do(Acrions.FadeOut(1.5))
            self.sprite_array[self.j].rotation = tank1_gun_rotation
            self.sprite_array[self.j].do(tankBulletDriver1())

            self.text.do(Acrions.FadeIn(0.4))
            self.text.do(Acrions.FadeOut(1.2))

            self.j += 1

# Отрисовка первого танка
class TankBodyLayer1(ScrollableLayer):
    def __init__(self, picture, pos):
        super(TankBodyLayer1, self).__init__()

        self.sprite = Sprite(picture)

        self.sprite.position = pos

        self.sprite.max_forward_speed = 200
        self.sprite.max_reverse_speed = -100

        self.add(self.sprite)
    def go(self):
        self.sprite.do(tankBodyDriver1())


tank1 = TankBodyLayer1("res/tank_telo.png",(200,100))
tank1.go()
tank2 = TankBodyLayer1("res/tank_telo2.png",(300,300))

tank_body_layer1 = tank1
tank_body_layer2 = tank2

MouseInput_layer = MouseInput()

map_layer = load("res/road.tmx")["map0"]

scroller.add(map_layer)
scroller.add(tank_body_layer1)
scroller.add(tank_body_layer2)
scroller.add(MouseInput_layer)

scene = Scene(scroller)

director.window.push_handlers(keyboard)

director.run(scene)