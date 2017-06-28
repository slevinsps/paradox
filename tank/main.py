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
from cocos.actions import*
from pyglet.window import key
from pyglet.window import mouse
from cocos.director import director
from cocos.actions import  Rotate, MoveBy, ScaleBy, Flip, Waves3D,RotateTo

director.init(width=800, height=600, autoscale=False, resizable=True)

keyboard = key.KeyStateHandler()
m = key.KeyStateHandler

scroller = ScrollingManager()

# Координаты тела первого танка
tank1_body_position_x = 200
tank1_body_position_y = 100
tank1_body_rotation = 0

# Координаты тела второго танка
tank2_body_position_x = 300
tank2_body_position_y = 300
tank2_body_rotation = 0

# Координаты танков в начале раунда
tank1_start_x = 200
tank1_start_y = 100
tank2_start_x = 300
tank2_start_y = 300

# Максимальные углы поворота корпуса и орудия
TANK_MAX_ANGLE_OF_BODY_ROTATION = 5
TANK_MAX_ANGLE_OF_GUN_ROTATION = 55

# Угол поворота башни первого и второго танков
tank1_gun_rotation = 0
tank2_gun_rotation = 0

# Здороваье и урон первого танка
tank1_health = 100
TANK1_DAMAGE = 20

# Здороваье и урон второго танка
tank2_health = 100
TANK2_DAMAGE = 20

#действующая скорость первого танка и второга танков
tank1_speed = 0
tank2_speed = 0

# Максимальная и минимальаня скорости движения первого танка
TANK1_MAX_FORWARD_SPEED = 200
TANK1_MAX_REVERSE_SPEED = -100

# Максимальная и минимальаня скорости движения второго танка
TANK2_MAX_FORWARD_SPEED = 200
TANK2_MAX_REVERSE_SPEED = -100

# Максимальная скорость движения ракеты
BULLET_MAX_SPEED = 500

#перемнная для времени
time_point1 = 0

#Угол, на который повернется пушка. Задаётся пользователем
user_tank1_gun_angle = 0

#Выбор направления поворота
user_tank1_gun_side_angle = 'right'

#Прекращение вращения
stop_tank1_gun_side_angle = 0

#Что это?
bool = 1
bool2 = 1

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
        global user_tank1_gun_angle
        global user_tank1_gun_side_angle
        global TANK_MAX_ANGLE_OF_GUN_ROTATION
        global stop_tank1_gun_side_angle

        super(tankGunDriver1, self).step(dt)

        if user_tank1_gun_angle == 0:
            self.target.rotation += (keyboard[key._1] - keyboard[key._2]) * TANK_MAX_ANGLE_OF_GUN_ROTATION * dt
        elif stop_tank1_gun_side_angle != 100:
            if user_tank1_gun_angle < TANK_MAX_ANGLE_OF_GUN_ROTATION:
                if user_tank1_gun_side_angle == "right":
                    self.target.rotation += user_tank1_gun_angle/100
                else:
                    self.target.rotation -= user_tank1_gun_angle/100
                stop_tank1_gun_side_angle += 1
            else:
                if user_tank1_gun_side_angle == "right":
                    self.target.rotation += TANK_MAX_ANGLE_OF_GUN_ROTATION/100
                    user_tank1_gun_angle -= TANK_MAX_ANGLE_OF_GUN_ROTATION/100
                elif user_tank1_gun_side_angle == "left":
                    self.target.rotation -= TANK_MAX_ANGLE_OF_GUN_ROTATION/100
                    user_tank1_gun_angle -= TANK_MAX_ANGLE_OF_GUN_ROTATION/100

        self.target.x = tank1_body_position_x
        self.target.y = tank1_body_position_y

        #Обновление глобальных переменных
        tank1_gun_rotation = self.target.rotation

#Управление ракетами первого телами
class tankBulletDriver1 (Driver):
    global tank2_health
    global TANK2_DAMAGE
    global bool
    global bool2
    global tank1_body_position_x
    global tank1_body_position_y

    #Управление полётом ракеты первого тела
    def step(self, dt):
        super(tankBulletDriver1, self).step(dt)
        self.target.speed = BULLET_MAX_SPEED
        self.determine_hit(self)

    #Определение попадания ракеты в танк
    def determine_hit(self):
        if self.bool and self.bool2:
            if math.sqrt(abs(tank2_body_position_x - self.target.x) ** 2 + abs(
                            tank2_body_position_y - self.target.y) ** 2) <= 20:
                self.tank2_health -= self.TANK2_DAMAGE
                tank2_gun_layer.text1.element.text = str(self.tank2_health)
                # tank2.sprite.do(ScaleBy(1.5, 0.2)+ScaleBy(2/3, 0.2))
                tank2_body_layer.sprite.do(RotateTo(-15, 0.2) + RotateTo(+15, 0.2) + RotateTo(-15, 0.2) + RotateTo(+15, 0.2))
                self.bool = 0
            if self.tank2_health == 0:
                tank2_body_layer.sprite.do(ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))
                tank2_body_layer.sprite.do(Acrions.FadeOut(1))
                tank2_gun_layer.sprite.do(Acrions.FadeOut(1))
                self.bool2 = 0

# Управление телом первого танка
class tankBodyDriver (Driver):
    tank_body_position_x = 0
    tank_body_position_y = 0
    tank_body_rotation = 0
    key_clicked = ''
    tank_speed = 0
    user_tank_body_rotation = 0
    number_of_tank = 1
    max_speed = 0
    min_speed = 0

    def tankBodyDriver_setting(self,
                               number_of_tank = 0,
                               tank_body_x = 0,
                               tank_body_y = 0,
                               tank_body_rotation = 0,
                               key = '',
                               tank_speed = 0,
                               max_speed = 0,
                               min_speed = 0,
                               user_body_rotation = 0):
        self.number_of_tank = number_of_tank
        self.tank_body_position_x = tank_body_x
        self.tank_body_position_y = tank_body_y
        self.tank_body_rotation = tank_body_rotation
        self.key_clicked = key
        self.tank_speed = tank_speed
        self.user_tank_body_rotation = user_body_rotation
        self.max_speed = max_speed
        self.min_speed = min_speed

    def step(self, dt):
        global TANK_MAX_ANGLE_OF_BODY_ROTATION

        if self.user_tank_body_rotation == 0:
            self.target.rotation += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * TANK_MAX_ANGLE_OF_BODY_ROTATION * dt
        else:
            if self.user_tank_body_rotation < TANK_MAX_ANGLE_OF_BODY_ROTATION:
                self.target.rotation += self.user_tank_body_rotation/100
            else:
                self.target.rotation += TANK_MAX_ANGLE_OF_BODY_ROTATION/100


        if self.key_clicked == '':
            self.target.acceleration = (keyboard[key.UP] - keyboard[key.DOWN]) * 350
        else:
            first_boolean = (self.key_clicked == 'w')
            second_boolean = (self.key_clicked == 's')
            if self.tank_speed >= self.max_speed:
                self.target.speed = (first_boolean - second_boolean) * self.max_speed
            elif self.tank_speed <= self.min_speed:
                self.target.speed = (first_boolean - second_boolean) * self.min_speed
            else:
                self.target.speed = (first_boolean - second_boolean) * self.tank_speed

        if keyboard[key.SPACE]:
            self.target.speed = 0

        super(tankBodyDriver, self).step(dt)

        if (self.number_of_tank == 1):
            global tank1_body_position_x, tank1_body_position_y, tank1_body_rotation, tank1_speed

            tank1_body_position_x = self.target.x
            tank1_body_position_y = self.target.y
            tank1_body_rotation = self.target.rotation
            tank1_speed = self.target.speed
        elif (self.number_of_tank == 2):
            global tank2_body_position_x, tank2_body_position_y, tank2_body_rotation, tank2_speed

            tank2_body_position_x = self.target.x
            tank2_body_position_y = self.target.y
            tank2_body_rotation = self.target.rotation
            tank2_speed = self.target.speed

        #print(self.target.speed)
        #print(self.target.acceleration)

        scroller.set_focus(self.target.x, self.target.y)


class tankGunAndBulletLayer(ScrollableLayer):
    is_event_handler = True
    sprite = Sprite("res/tank_pushka.png")

    def __init__(self, x, y, health):
        super(tankGunAndBulletLayer, self).__init__()

        self.position_x = x
        self.position_y = y
        self.health = health

        self.j = 0

        self.sprite_array = [Sprite("res/bullet.png"), Sprite("res/bullet.png"), Sprite("res/bullet.png")];
        for i in range(len(self.sprite_array)):
            self.sprite_array[i].position = x, y
            self.sprite_array[i].do(Acrions.FadeOut(0))
            self.add(self.sprite_array[i])

        self.text = Label("Перезарядка",
                          font_name = "Helvetica",
                          font_size = 10,
                          x = 100,
                          y = 0)

        self.text.do(Acrions.FadeOut(0))

        self.text.do(TextDriver1())

        self.sprite.x = x
        self.sprite.y = y

        self.add(self.sprite)
        self.add(self.text)
        #self.sprite.do(tankGunDriver1())

    def update_gun(self, mouse_x_pos, mouse_y_pos):

        if (self.sprite.y < self.position_y):
            self.sprite.rotation = math.degrees(
                math.atan((self.sprite.x - self.position_x)/(self.sprite.y - self.position_y)))
        elif (self.sprite.y > self.position_y):
            self.sprite.rotation = math.degrees(
                math.atan((self.sprite.x - self.position_x) / (self.sprite.y - self.position_y)))+180

        global tank_rotation
        tank_rotation = self.sprite.rotation

    def on_mouse_motion(self, x, y, dx, dy):
        #self.update_gun(x, y)
        self.position_x, self.position_y = director.get_virtual_coordinates(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
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

        self.position_x, self.position_y = director.get_virtual_coordinates(x, y)

    def push_bullet(self):
        global tank1_body_position_x
        global tank1_body_position_y

        if self.j>=len(self.sprite_array):
            while self.j > 0:
                self.j -= 1
                self.sprite_array[self.j].stop()
                self.sprite_array[self.j].do(Acrions.FadeOut(0))
                #self.sprite_array[self.j].do(Acrions.MoveTo((tank1_body_position_x, tank1_body_position_y), 0.1))
                self.sprite_array[self.j].position = tank1_body_position_x, tank1_body_position_y

        if self.j < len(self.sprite_array):

            self.sprite_array[self.j].x = tank1_body_position_x
            self.sprite_array[self.j].y = tank1_body_position_y

            self.sprite_array[self.j].do(Acrions.FadeOut(1.5))
            self.sprite_array[self.j].rotation = tank1_gun_rotation
            self.sprite_array[self.j].do(tankBulletDriver1())

            self.text.do(Acrions.FadeIn(0.4))
            self.text.do(Acrions.FadeOut(1.2))

            self.j += 1

# Отрисовка танка
class TankBodyLayer(ScrollableLayer):

    #sprite = Sprite
    Picture = ''
    sprite = Sprite("res/bullet.png")

    def __init__(self, picture, pos, max_speed, min_speed):

        super(TankBodyLayer, self).__init__()

        self.sprite = Sprite(picture)
        self.sprite.position = pos

        self.sprite.max_forward_speed = max_speed
        self.sprite.max_reverse_speed = min_speed

        self.add(self.sprite)

#key1 - направление движения. Может принимать значения w(ехать вперёд),s(ехать назад)
#speed - скорость движения
#rotation - угол кривизны движения
def move_tank_body(key = "w", speed = 0, rotation = 0, number_of_tank = 1):

    copy_driver = tankBodyDriver()

    if number_of_tank == 1:
        global TANK1_MAX_FORWARD_SPEED
        global TANK1_MAX_REVERSE_SPEED
        global tank1_body_position_x
        global tank1_body_position_y
        global tank1_body_rotation

        copy_driver.tankBodyDriver_setting(
            number_of_tank,
            tank1_body_position_x,
            tank1_body_position_y,
            tank1_body_rotation,
            key,
            speed,
            TANK1_MAX_FORWARD_SPEED,
            TANK1_MAX_REVERSE_SPEED,
            rotation
        )
        tank1_body_layer.sprite.do(copy_driver)
    else:
        global TANK2_MAX_FORWARD_SPEED
        global TANK2_MAX_REVERSE_SPEED
        global tank2_body_position_x
        global tank2_body_position_y
        global tank2_body_rotation

        copy_driver.tankBodyDriver_setting(
            number_of_tank,
            tank2_body_position_x,
            tank2_body_position_y,
            tank2_body_rotation,
            key,
            speed,
            TANK2_MAX_FORWARD_SPEED,
            TANK2_MAX_REVERSE_SPEED,
            rotation
        )
        tank2_body_layer.sprite.do(copy_driver)

#side - направление движения. Может принимать значения right(по часовой стрелке), left(против часовой стрелки)
#angle - угол, на который повернется танк
def rotate_gun(angle = 1, side = 'right'):
    assert (angle > 0)

    global stop_tank1_gun_side_angle

    tankGunAndBulletLayer.sprite.stop()
    stop_tank1_gun_side_angle = 0

    global user_tank1_gun_angle
    global user_tank1_gun_side_angle

    user_tank1_gun_angle = angle
    user_tank1_gun_side_angle = side

    tankGunAndBulletLayer.sprite.do(tankGunDriver1())

class driverByFirstUser(Driver):
    def step(self, dt):
        if(tank1_body_position_y <= tank1_start_y):
            move_tank_body('w', 70, 0, 1)
        elif(tank1_body_position_y >= 300):
            move_tank_body('w', -150, 0, 1)
        #rotate_gun(115, 'right')

class driverBySecondUser(Driver):
    def step(self, dt):
        if (tank2_body_position_y <= tank2_start_y):
            move_tank_body('w', 70, 0, 2)
        elif (tank2_body_position_y >= 300):
            move_tank_body('w', -150, 0, 2)
        #rotate_gun(720, 'left')


#Создание класса корпуса первого танка
tank1_body_layer = TankBodyLayer("res/tank_telo.png",
                       (tank1_body_position_x, tank1_body_position_y),
                       TANK1_MAX_FORWARD_SPEED,
                       TANK1_MAX_REVERSE_SPEED)

#Создание класса корпуса второго танка
tank2_body_layer = TankBodyLayer("res/tank_telo2.png",
                      (tank2_body_position_x, tank2_body_position_y),
                       TANK2_MAX_FORWARD_SPEED,
                       TANK2_MAX_REVERSE_SPEED)

#Создание класса пушки первого танка
tank1_gun_layer = tankGunAndBulletLayer(tank1_body_position_x,
                                tank1_body_position_y,
                                tank2_health)

#Создание класса пушки второго танка
tank2_gun_layer = tankGunAndBulletLayer(tank2_body_position_x,
                                tank2_body_position_y,
                                tank1_health)

#Подключение драйверов разработчиков
tank1_body_layer.sprite.do(driverByFirstUser())
tank2_body_layer.sprite.do(driverBySecondUser())

#Настройка карты
map_layer = load("res/road.tmx")["map0"]
scroller.add(map_layer)

#Покдючаем танки
scroller.add(tank1_body_layer)
scroller.add(tank2_body_layer)
scroller.add(tank1_gun_layer)
scroller.add(tank2_gun_layer)

scene = Scene(scroller)

director.window.push_handlers(keyboard)

director.run(scene)