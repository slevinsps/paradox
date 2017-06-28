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
from cocos.director import director
from cocos.actions import  Rotate, MoveBy, ScaleBy, Flip, Waves3D,RotateTo,RotateBy
from cocos.sprite import Sprite
director.init(width=800, height=600, autoscale=False, resizable=True)

keyboard = key.KeyStateHandler()
m = key.KeyStateHandler

scroller = ScrollingManager()

# Координаты тела первого танка
tank1_body_position_x = 0
tank1_body_position_y = 0
tank1_body_rotation = 0

# Координаты тела второго танка
tank2_body_position_x = 300
tank2_body_position_y = 300
tank2_body_rotation = 0

# Координаты пушки первого танка
tank1_gun__rotation = 0

# Здороваье и урон первого танка
tank1_health = 100
tank1_damage = 3

# Здороваье и урон второго танка
tank2_health = 100
tank2_damage = 3

#перемнная для времени
time_point1 = 0

bool = 1
bool2 = 1
bool_border = 1
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
    global tank2_body_position_x
    global tank2_body_position_y


    def step(self, dt):
        global tank2_health
        global bool
        global bool2
        super(tankBulletDriver1, self).step(dt)
        self.target.speed = 500

        if bool and bool2:
            if math.sqrt(abs(tank2_body_position_x - self.target.x) ** 2 + abs(
            tank2_body_position_y - self.target.y) ** 2) <= 20:
                tank2_health -= 20
                pushka2.text1.element.text = str(tank2_health)
                tank2.sprite.do(RotateBy(-15, 0.2)+RotateBy(+15, 0.2)+RotateBy(-15, 0.2)+RotateBy(+15, 0.2))
                bool = 0
            if tank2_health == 0:
                tank2.sprite.do(ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2)+ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))
                tank2.sprite.do(Acrions.FadeOut(1))
                pushka2.sprite.do(Acrions.FadeOut(1))
                bool2 = 0


# Управление телом первого танка
class tankBodyDriver1 (Driver):
    def step(self, dt):
        global tank1_body_position_x
        global tank1_body_position_y
        global tank1_body_rotation
        global tank1_health
        global bool_border

        if tank1_health == 0 and bool_border:
            tank1.sprite.do(ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))
            tank1.sprite.do(Acrions.FadeOut(1))
            pushka1.sprite.do(Acrions.FadeOut(1))
            pushka1.text1.do(Acrions.FadeOut(1))
            pushka1.text.do(Acrions.FadeOut(0))
            bool_border = 0
        if bool_border:
           if self.target.x <= 50:
               self.target.x = 51
               self.target.speed = 0
               tank1_health -= 5
               pushka1.text1.element.text = str(tank1_health)
               tank1.sprite.do(RotateBy(-10, 0.2) + RotateBy(+10, 0.2) + RotateBy(-10, 0.2) + RotateBy(+10, 0.2))
           if self.target.x >= 1229:
               self.target.x = 1228
               self.target.speed = 0
               tank1_health -= 5
               pushka1.text1.element.text = str(tank1_health)
               tank1.sprite.do(RotateBy(-10, 0.2) + RotateBy(+10, 0.2) + RotateBy(-10, 0.2) + RotateBy(+10, 0.2))
           if self.target.y <= 50:
               self.target.y = 51
               self.target.speed = 0
               tank1_health -= 5
               pushka1.text1.element.text = str(tank1_health)
               tank1.sprite.do(RotateBy(-10, 0.2) + RotateBy(+10, 0.2) + RotateBy(-10, 0.2) + RotateBy(+10, 0.2))
           if self.target.y >= 1229:
               self.target.y = 1228
               self.target.speed = 0
               tank1_health -= 5
               pushka1.text1.element.text = str(tank1_health)
               tank1.sprite.do(RotateBy(-10, 0.2) + RotateBy(+10, 0.2) + RotateBy(-10, 0.2) + RotateBy(+10, 0.2))



        self.target.rotation += (keyboard[key.D] - keyboard[key.A]) * 30 * dt
        self.target.acceleration = (keyboard[key.W] - keyboard[key.S]) * 350



        if keyboard[key.ENTER]:
            self.target.speed = 0

        super(tankBodyDriver1, self).step(dt)

        tank1_body_position_x = self.target.x
        tank1_body_position_y = self.target.y

        tank1_body_rotation = self.target.rotation

        scroller.set_focus(self.target.x, self.target.y)


class tankBulletLayer(ScrollableLayer):
    is_event_handler = True
    def __init__(self,pos,health):
        super(tankBulletLayer, self).__init__()

        self.position_x = 0
        self.position_y = 0
        self.j = 0
        self.health = health

        self.text = Label("Перезарядка",
                          font_name = "Helvetica",
                          font_size = 10,
                          x = 50,
                          y = 0)

        self.text1 = Label(str(self.health),
                          font_name = "Helvetica",
                          font_size = 15,
                          x = 0,
                          y = 60)


        self.sprite_array = [Sprite("res/bullet.png"), Sprite("res/bullet.png"), Sprite("res/bullet.png")];
        for i in range(len(self.sprite_array)):
            self.sprite_array[i].position = pos
            self.sprite_array[i].do(Acrions.FadeOut(0))
            self.add(self.sprite_array[i])


        self.text.do(Acrions.FadeOut(0))

        self.sprite = Sprite("res/tank_pushka.png")

        self.sprite.position = pos

        self.add(self.sprite)
        self.add(self.text1)
        self.add(self.text)

        self.text.do(TextDriver1())
    def go(self):
        self.text.do(TextDriver1())
        self.text1.do(TextDriver1())
        self.sprite.do(tankGunDriver1())

    def on_key_press(self, key, modifiers):
        if key == 32:
            global tank1_body_position_x
            global tank1_body_position_y
            global tank1_body_rotation
            global tank1_gun_rotation
            global time_point1
            time_point2 = time.clock()
            if time_point1 == 0:
                time_point1 = time.clock()
                self.push_bullet()
            else:
                if time_point2 - time_point1 > 1:
                    self.push_bullet()
                    time_point1 = time.clock()
    def push_bullet(self):
        global tank1_body_position_x
        global tank1_body_position_y
        global bool

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
            bool = 1
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
tank2 = TankBodyLayer1("res/tank_telo3.png",(300,300))


pushka1 = tankBulletLayer((200, 100),100)
pushka1.go()
pushka2 = tankBulletLayer((tank2_body_position_x, tank2_body_position_y),100)





tank_body_layer1 = tank1
tank_body_layer2 = tank2

tankBulletLayer_layer1 = pushka1
tankBulletLayer_layer2 = pushka2
map_layer = load("res/road.tmx")["map0"]

scroller.add(map_layer)
scroller.add(tank_body_layer1)
scroller.add(tank_body_layer2)
scroller.add(tankBulletLayer_layer1)
scroller.add(tankBulletLayer_layer2)

scene = Scene(scroller)

director.window.push_handlers(keyboard)

director.run(scene)