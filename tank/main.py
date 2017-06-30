# Imports as usual
from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.layer import ScrollingManager, ScrollableLayer
from cocos.director import director
from cocos.scene import Scene
import math
import time
import cocos.actions as Acrions
from cocos.text import Label
from cocos.actions import Driver
from cocos.actions import*
from pyglet.window import key
from cocos.director import director
from cocos.actions import  Rotate, MoveBy, ScaleBy, Flip, Waves3D,RotateTo
import FirstTankClass
import SecondTankClass

director.init(width=800, height=600, autoscale=False, resizable=True)

keyboard = key.KeyStateHandler()

scroller = ScrollingManager()

# Координаты тела первого танка
tank1_body_position_x = 200
tank1_body_position_y = 100
tank1_body_rotation = 0

# Координаты тела второго танка
tank2_body_position_x = 500
tank2_body_position_y = 300
tank2_body_rotation = 0

# Координаты танков в начале раунда
tank1_start_x = 200
tank1_start_y = 100
tank2_start_x = 300
tank2_start_y = 300

# Максимальные углы поворота корпуса и орудия
TANK_MAX_ANGLE_OF_BODY_ROTATION = 30
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

# Урон от столкновения со стенами
WALL_DAMAGE = 5

# Действующая скорость первого танка и второга танков
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

#перемнные для времени
time_point1 = 0
time_point2 = 0
time1 = 0
time2 = 0

#Прекращение вращения
stop_tank1_gun_side_angle = 0
stop_tank2_gun_side_angle = 0

bool1 = 1
bool2 = 1
bool_end = 1
bool_border1 = 1
bool_border2 = 1

# Уникальные коды move_tank_body
move_tank_body_1_code = ''
move_tank_body_2_code = ''

# Уникальные коды rotate_gun
rotate_gun_1_code = ''
rotate_gun_2_code = ''



class tankFocusDriver(Driver):

    def tankFocusDriver_settings(self,
                                number_of_tank):
        self.number_of_tank = number_of_tank

    def step(self, dt):
        super(tankFocusDriver, self).step(dt)
        if self.number_of_tank == 1:
            global tank1_body_position_x, tank1_body_position_y
            self.target.x = tank1_body_position_x
            self.target.y = tank1_body_position_y
        else:
            global tank2_body_position_x, tank2_body_position_y
            self.target.x = tank2_body_position_x
            self.target.y = tank2_body_position_y
        scroller.set_focus(self.target.x, self.target.y)






# Управление надписями
class textDriver(Driver):

    # Настройка класса(выбор к какому танку подключается драйвер)
    def textDriver_settings(self,
                            number_of_tank,
                            dx,
                            dy):
        self.number_of_tank = number_of_tank
        self.dx = dx
        self.dy = dy

    def step(self, dt):
        super(textDriver, self).step(dt)

        if self.number_of_tank == 1:
            global tank1_body_position_x, tank1_body_position_y
            self.target.x = tank1_body_position_x + self.dx
            self.target.y = tank1_body_position_y + self.dy
        else:
            global tank2_body_position_x, tank2_body_position_y
            self.target.x = tank2_body_position_x + self.dx
            self.target.y = tank2_body_position_y + self.dy

# Управление дулом пушки первого тела
class tankGunDriver(Driver):

    # Настройка класса(выбор к какому танку подключается драйвер)
    def tankGunDriver_settings(self,
                                tank_body_position_x,
                                tank_body_position_y,
                                tank_gun_rotation,
                                user_tank_gun_angle,
                                user_tank_gun_side_angle,
                                stop_tank_gun_side_angle,
                                number_of_tank):
        self.tank_body_position_x = tank_body_position_x
        self.tank_body_position_y = tank_body_position_y
        self.tank_gun_rotation = tank_gun_rotation
        self.user_tank_gun_angle = user_tank_gun_angle
        self.user_tank_gun_side_angle = user_tank_gun_side_angle
        self.stop_tank_gun_side_angle = stop_tank_gun_side_angle
        self.number_of_tank = number_of_tank

    def step(self, dt):
        global TANK_MAX_ANGLE_OF_GUN_ROTATION

        super(tankGunDriver, self).step(dt)

        #self.target.rotation += (keyboard[key._1] - keyboard[key._2]) * TANK_MAX_ANGLE_OF_GUN_ROTATION * dt
        if self.stop_tank_gun_side_angle != 50:
            if self.user_tank_gun_angle < TANK_MAX_ANGLE_OF_GUN_ROTATION:
                if self.user_tank_gun_side_angle == "right":
                    self.target.rotation += self.user_tank_gun_angle/50
                else:
                    self.target.rotation -= self.user_tank_gun_angle/50
                self.stop_tank_gun_side_angle += 1
            else:
                if self.user_tank_gun_side_angle == "right":
                    self.target.rotation += TANK_MAX_ANGLE_OF_GUN_ROTATION/50
                    self.user_tank_gun_angle -= TANK_MAX_ANGLE_OF_GUN_ROTATION/50
                elif self.user_tank_gun_side_angle == "left":
                    self.target.rotation -= TANK_MAX_ANGLE_OF_GUN_ROTATION/50
                    self.user_tank_gun_angle -= TANK_MAX_ANGLE_OF_GUN_ROTATION/50

        if (self.number_of_tank == 1):
            global tank1_body_position_x, tank1_body_position_y
            self.target.x = tank1_body_position_x
            self.target.y = tank1_body_position_y
        else:
            global tank2_body_position_x, tank2_body_position_y
            self.target.x = tank2_body_position_x
            self.target.y = tank2_body_position_y

        #Обновление глобальных переменных
        if self.number_of_tank == 1:
            global tank1_gun_rotation
            tank1_gun_rotation = self.target.rotation
        else:
            global tank2_gun_rotation
            tank2_gun_rotation = self.target.rotation

#Управление ракетами первого телами
class tankBulletDriver(Driver):

    # Настройка класса(выбор к какому танку подключается драйвер)
    def tankBulletDriver_settings(self,
                                    bool,
                                    tank_damage,
                                    tank_gun_rotation,
                                    number_of_tank):
        self.bool = bool
        self.tank_damage = tank_damage
        self.tank_gun_rotation = tank_gun_rotation
        self.number_of_tank = number_of_tank

    #Управление полётом ракеты первого тела
    def step(self, dt):
        global tank1_health, tank1_body_position_x, tank1_body_position_y
        global tank2_health, tank2_body_position_x, tank2_body_position_y

        super(tankBulletDriver, self).step(dt)

        if self.number_of_tank == 1:

            self.tank_health = tank2_health

            self.tank_body_position_x = tank2_body_position_x
            self.tank_body_position_y = tank2_body_position_y
        else:

            self.tank_health = tank1_health

            self.tank_body_position_x = tank1_body_position_x
            self.tank_body_position_y = tank1_body_position_y

        self.target.rotation = self.tank_gun_rotation
        self.target.speed = BULLET_MAX_SPEED
        self.determine_hit()

    #Определение попадания ракеты в танк
    def determine_hit(self):
        global bool_end, tank1_health, tank2_health

        if self.bool and bool_end:
            if math.sqrt(abs(self.tank_body_position_x - self.target.x) ** 2 + abs(
                            self.tank_body_position_y - self.target.y) ** 2) <= 20:

                if self.number_of_tank == 1:
                    global tank2_health, bool1
                    tank2_health -= self.tank_damage
                    self.tank_health = tank2_health
                    tank2_gun_layer.text_health.element.text = str(tank2_health)
                    tank2_body_layer.tank_body_image.do(
                        RotateTo(-15, 0.2) + RotateTo(+15, 0.2) + RotateTo(-15, 0.2) + RotateTo(+15, 0.2))
                    bool1 = 0
                else:
                    global tank1_health, bool2
                    self.tank_health = tank1_health
                    tank1_health -= self.tank_damage
                    tank1_gun_layer.text_health.element.text = str(tank1_health)
                    tank1_body_layer.tank_body_image.do(
                        RotateTo(-15, 0.2) + RotateTo(+15, 0.2) + RotateTo(-15, 0.2) + RotateTo(+15, 0.2))
                    bool2 = 0
                self.bool = 0
            if self.tank_health == 0:
                    if self.number_of_tank == 1 and tank1_health == 0:
                        tank1_body_layer.stop()
                        tank1_body_layer.tank_body_image.stop()
                        tank1_body_layer.tank_body_image.do(
                            ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))
                        tank1_body_layer.tank_body_image.do(Acrions.FadeOut(1))
                        tank1_gun_layer.tank_gun_image.do(Acrions.FadeOut(1))
                        tank1_gun_layer.text_recharge.do(Acrions.FadeOut(1))
                        tank1_gun_layer.text_health.do(Acrions.FadeOut(1))
                    elif self.number_of_tank == 2 and tank2_health == 0:
                        tank2_body_layer.stop()
                        tank2_body_layer.tank_body_image.stop()
                        tank2_body_layer.tank_body_image.do(
                            ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))
                        tank2_body_layer.tank_body_image.do(Acrions.FadeOut(1))
                        tank2_gun_layer.tank_gun_image.do(Acrions.FadeOut(1))
                        tank2_gun_layer.text_recharge.do(Acrions.FadeOut(1))
                        tank2_gun_layer.text_health.do(Acrions.FadeOut(1))
                    bool_end = 0

# Управление телом первого танка
class tankBodyDriver (Driver):

    # Настройка класса(выбор к какому танку подключается драйвер)
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
        global tank1_body_position_x, tank1_body_position_y, tank1_body_rotation, tank1_speed, tank1_health, bool_border1
        global tank2_body_position_x, tank2_body_position_y, tank2_body_rotation, tank2_speed, tank2_health, bool_border2

        super(tankBodyDriver, self).step(dt)

        self.change_angle(dt)
        self.change_speed()


        #self.determine_hit()
        if (self.number_of_tank == 1):

            tank1_body_position_x = self.target.x
            tank1_body_position_y = self.target.y
            tank1_body_rotation = self.target.rotation
            tank1_speed = self.target.speed

            if tank1_health <= 0 and bool_border1:
                tank1_body_layer.tank_body_image.do(
                    ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))
                tank1_body_layer.tank_body_image.do(Acrions.FadeOut(1))
                tank1_gun_layer.tank_gun_image.do(Acrions.FadeOut(1))
                tank1_gun_layer.text_health.do(Acrions.FadeOut(1))
                tank1_gun_layer.text_recharge.do(Acrions.FadeOut(1))
                bool_border1 = 0
            if bool_border1:
                self.target.x = self.manage_side(1, tank1_gun_layer,
                                                 tank1_body_layer, self.target.x <= 50, 53,self.target.x)
                self.target.x = self.manage_side(1, tank1_gun_layer,
                                                 tank1_body_layer, self.target.x >= 1229, 1226, self.target.x)
                self.target.y = self.manage_side(1, tank1_gun_layer,
                                                 tank1_body_layer, self.target.y <= 50, 53, self.target.y)
                self.target.y = self.manage_side(1, tank1_gun_layer,
                                                 tank1_body_layer, self.target.y >= 1229, 1226, self.target.y)


        elif (self.number_of_tank == 2):

            tank2_body_position_x = self.target.x
            tank2_body_position_y = self.target.y
            tank2_body_rotation = self.target.rotation
            tank2_speed = self.target.speed

            if tank2_health <= 0 and bool_border2:
                tank2_body_layer.tank_body_image.do(
                    ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))
                tank2_body_layer.tank_body_image.do(Acrions.FadeOut(1))
                tank2_gun_layer.tank_gun_image.do(Acrions.FadeOut(1))
                tank2_gun_layer.text_health.do(Acrions.FadeOut(1))
                tank2_gun_layer.text_recharge.do(Acrions.FadeOut(1))
                bool_border2 = 0
            if bool_border2:
                self.target.x = self.manage_side(2, tank2_gun_layer,
                                                 tank2_body_layer, self.target.x <= 50, 53, self.target.x)
                self.target.x = self.manage_side(2, tank2_gun_layer,
                                                 tank2_body_layer, self.target.x >= 1229, 1226, self.target.x)
                self.target.y = self.manage_side(2, tank2_gun_layer,
                                                 tank2_body_layer, self.target.y <= 50, 53, self.target.y)
                self.target.y = self.manage_side(2, tank2_gun_layer,
                                                 tank2_body_layer, self.target.y >= 1229, 1226, self.target.y)




######################################

    #def determine_hit(self):
    #    global bool_end, tank1_health, tank2_health, time1,time2
    #    global tank1_body_position_x, tank1_body_position_y
    #    global tank2_body_position_x, tank2_body_position_y
    #    if math.sqrt(abs(tank1_body_position_x - tank2_body_position_x) ** 2 + abs(
    #                    tank1_body_position_y - tank2_body_position_y) ** 2) <= 36:
    #        if time2 == time1 == 0:
    #            time2 = time.clock()
    #            time1 = time.clock()
#
    #        if time2 - time1 > 1:
    #            self.push_bullet()
    #        else:
    #            time2 = time.clock()
#
    #        self.target.speed = 0
    #        tank2_health -= WALL_DAMAGE
    #        tank2_gun_layer.text_health.element.text = str(tank1_health)
    #        tank1_health -= WALL_DAMAGE
    #        tank1_gun_layer.text_health.element.text = str(tank1_health)
    #        tank1_body_layer.tank_body_image.do(
    #            RotateTo(-15, 0.2) + RotateTo(+15, 0.2) + RotateTo(-15, 0.2) + RotateTo(+15, 0.2))
    #        tank2_body_layer.tank_body_image.do(
    #            RotateTo(-15, 0.2) + RotateTo(+15, 0.2) + RotateTo(-15, 0.2) + RotateTo(+15, 0.2))
    # ###############################

    def manage_side(self, number_of_tank, tank_gun_layer, tank_body_layer, bool, true, false):
        coordinate = false
        if bool:
            coordinate = true
            self.target.speed = 0
            if number_of_tank == 1:
                global tank1_health
                tank1_health -= WALL_DAMAGE
                tank_gun_layer.text_health.element.text = str(tank1_health)
            else:
                global tank2_health
                tank2_health -= WALL_DAMAGE
                tank_gun_layer.text_health.element.text = str(tank2_health)
            tank_body_layer.tank_body_image.do(
                RotateBy(-10, 0.2) + RotateBy(+10, 0.2) + RotateBy(-10, 0.2) + RotateBy(+10, 0.2))
        return coordinate

    # Поворот танка
    def change_angle(self, dt):
        global TANK_MAX_ANGLE_OF_BODY_ROTATION

        if self.user_tank_body_rotation == 0:
            self.target.rotation += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * TANK_MAX_ANGLE_OF_BODY_ROTATION * dt
        else:
            if self.user_tank_body_rotation < TANK_MAX_ANGLE_OF_BODY_ROTATION:
                self.target.rotation += self.user_tank_body_rotation / 10
            else:
                self.target.rotation += TANK_MAX_ANGLE_OF_BODY_ROTATION / 10

    # Скорость танка
    def change_speed(self):
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

        if keyboard[key.ENTER]:
            self.target.speed = 0

class tankGunAndBulletLayer(ScrollableLayer):
    is_event_handler = True
    tank_gun_image = Sprite("res/tank_pushka.png")

    def __init__(self, x, y, health, enemy_health, text_color, number_of_tank, bool):
        super(tankGunAndBulletLayer, self).__init__()

        self.tank_gun_image = Sprite("res/tank_pushka.png")
        self.position_x = x
        self.position_y = y
        self.health = health
        self.enemy_health = enemy_health
        self.number_of_tank = number_of_tank
        self.bool = bool

        self.j = 0

        self.text_recharge = Label("Перезарядка",
                          font_name = "Helvetica",
                          font_size = 10,
                          x = 50,
                          y = 0,
                          color = text_color)

        self.text_health = Label(str(self.health),
                           font_name = "BOLD",
                           font_size = 15,
                           x = 0,
                           y = 60,
                           color = text_color)

        self.text_recharge.do(Acrions.FadeOut(0))

        driver_health = textDriver()
        driver_recharge = textDriver()

        if number_of_tank == 1:
            global tank1_body_position_x, tank1_body_position_y
            driver_health.textDriver_settings(1,
                                              0,
                                              0)
            driver_recharge.textDriver_settings(1,
                                              0,
                                              100)
        else:
            global tank2_body_position_x, tank2_body_position_y
            driver_health.textDriver_settings(2,
                                              0,
                                              0)
            driver_recharge.textDriver_settings(2,
                                                0,
                                                100)

        self.text_health.do(driver_health)
        self.text_recharge.do(driver_recharge)

        self.bullet_array = [Sprite("res/bullet.png"), Sprite("res/bullet.png"), Sprite("res/bullet.png")];

        for i in range(len(self.bullet_array)):
            self.bullet_array[i].position = x, y
            self.bullet_array[i].do(Acrions.FadeOut(0))
            self.add(self.bullet_array[i])

        self.tank_gun_image.x = x
        self.tank_gun_image.y = y

        self.add(self.tank_gun_image)
        self.add(self.text_recharge)
        self.add(self.text_health)

    # Управление перезарядкой
    def shoot_bullet(self):
        if self.number_of_tank == 1:
            global time_point1
            time_point3 = time.clock()
            if time_point1 == 0:
                time_point1 = time.clock()
                self.push_bullet()
            else:
                if time_point3 - time_point1 > 1:
                    self.push_bullet()
                    time_point1 = time.clock()
        else:
            global time_point2
            time_point3 = time.clock()
            if time_point2 == 0:
                time_point2 = time.clock()
                self.push_bullet()
            else:
                if time_point3 - time_point2 > 1:
                    self.push_bullet()
                    time_point2 = time.clock()


    # Нажатие на клавишу
    def on_key_press(self, key, modifiers):
        global tank1_body_position_x, tank1_body_position_y
        if key == 32:
            self.shoot_bullet()

        if key == 49:
            tankFocusDriver1 = tankFocusDriver()
            tankFocusDriver1.tankFocusDriver_settings(1)
            tank2_body_layer.focus_frame.stop()
            tank2_body_layer.focus_frame.do(Acrions.FadeOut(0))
            tank1_body_layer.focus_frame.do(Acrions.FadeIn(0))
            tank1_body_layer.focus_frame.do(tankFocusDriver1)


        if key == 50:
            tankFocusDriver2 = tankFocusDriver()
            tankFocusDriver2.tankFocusDriver_settings(2)
            tank1_body_layer.focus_frame.stop()
            tank1_body_layer.focus_frame.do(Acrions.FadeOut(0))
            tank2_body_layer.focus_frame.do(Acrions.FadeIn(0))
            tank2_body_layer.focus_frame.do(tankFocusDriver2)

    # Полёт ракеты
    def push_bullet(self):

        if self.j>=len(self.bullet_array):
            while self.j > 0:
                self.j -= 1
                self.bullet_array[self.j].stop()
                self.bullet_array[self.j].do(Acrions.FadeOut(0))

        if self.j < len(self.bullet_array):
            self.bullet_array[self.j].x = self.position_x
            self.bullet_array[self.j].y = self.position_y

            self.bullet_array[self.j].do(Acrions.FadeOut(1.5))

            self.tank_damage = 0

            if self.number_of_tank == 1:
                global tank1_gun_rotation, bool1, TANK1_DAMAGE, tank1_body_position_x, tank1_body_position_y
                bool1 = 1
                self.bullet_array[self.j].rotation = tank1_gun_rotation
                self.bullet_array[self.j].x = tank1_body_position_x
                self.bullet_array[self.j].y = tank1_body_position_y
                self.tank_damage = TANK1_DAMAGE
            else:
                global tank2_gun_rotation, bool2, TANK2_DAMAGE,  tank2_body_position_x, tank2_body_position_y
                bool2 = 1
                self.bullet_array[self.j].rotation = tank2_gun_rotation
                self.bullet_array[self.j].x = tank2_body_position_x
                self.bullet_array[self.j].y = tank2_body_position_y
                self.tank_damage = TANK2_DAMAGE

            bullet_driver = tankBulletDriver()

            bullet_driver.tankBulletDriver_settings(self.bool,
                                                    self.tank_damage,
                                                    self.bullet_array[self.j].rotation,
                                                    self.number_of_tank)

            self.bullet_array[self.j].do(bullet_driver)

            self.text_recharge.do(Acrions.FadeIn(0.4))
            self.text_recharge.do(Acrions.FadeOut(1.2))

            self.j += 1

# Отрисовка танка
class TankBodyLayer(ScrollableLayer):

    tank_body_image = Sprite("res/bullet.png")
    camera_image = Sprite("res/camera.png")
    focus_frame = Sprite("res/focus_frame.png")

    def __init__(self, picture, pos, max_speed, min_speed):

        super(TankBodyLayer, self).__init__()

        self.tank_body_image = Sprite(picture)
        self.focus_frame = Sprite("res/focus_frame.png")
        self.tank_body_image.position = pos
        self.focus_frame.position = pos

        self.tank_body_image.max_forward_speed = max_speed
        self.tank_body_image.max_reverse_speed = min_speed

        self.add(self.tank_body_image)
        self.add(self.focus_frame)
        self.focus_frame.do(Acrions.FadeOut(0))
        self.camera_image = Sprite("res/camera.png")
        self.add(self.camera_image)


#Заполнение функций из библиотеки
class tank_library_initialize():

    def get_x(number_of_tank = 1):
        if number_of_tank == 1:
            global tank1_body_position_x
            return tank1_body_position_x
        else:
            global tank2_body_position_x
            return tank2_body_position_x

    def get_y(number_of_tank=1):
        if number_of_tank == 1:
            global tank1_body_position_y
            return tank1_body_position_y
        else:
            global tank2_body_position_y
            return tank2_body_position_y

    #key1 - направление движения. Может принимать значения w(ехать вперёд),s(ехать назад)
    #speed - скорость движения
    #rotation - угол кривизны движения
    def move_tank_body(key = "w", speed = 0, rotation = 0, number_of_tank = 1):

        global move_tank_body_1_code, move_tank_body_2_code

        code = key + str(speed) + str(rotation)

        if number_of_tank == 1 and move_tank_body_1_code != code:
            tank1_body_layer.tank_body_image.stop()

            move_tank_body_1_code = code
            body_driver = tankBodyDriver()

            global TANK1_MAX_FORWARD_SPEED
            global TANK1_MAX_REVERSE_SPEED
            global tank1_body_position_x
            global tank1_body_position_y
            global tank1_body_rotation

            body_driver.tankBodyDriver_setting(
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

            tank1_body_layer.tank_body_image.do(body_driver)
            gun_driver = tankGunDriver()
            gun_driver.tankGunDriver_settings(tank1_body_position_x,
                                              tank1_body_position_y,
                                              tank1_gun_rotation,
                                              0,
                                              'r',
                                              0,
                                              1)
            tank1_gun_layer.tank_gun_image.do(gun_driver)
        elif number_of_tank == 2 and move_tank_body_2_code != code:

            tank2_body_layer.tank_body_image.stop()
            move_tank_body_2_code = code
            body_driver = tankBodyDriver()

            global TANK2_MAX_FORWARD_SPEED
            global TANK2_MAX_REVERSE_SPEED
            global tank2_body_position_x
            global tank2_body_position_y
            global tank2_body_rotation

            body_driver.tankBodyDriver_setting(
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

            tank2_body_layer.tank_body_image.do(body_driver)

            gun_driver = tankGunDriver()
            gun_driver.tankGunDriver_settings(tank1_body_position_x,
                                              tank1_body_position_y,
                                              tank1_gun_rotation,
                                              0,
                                              'r',
                                              0,
                                              2)
            tank2_gun_layer.tank_gun_image.do(gun_driver)

    #side - направление движения. Может принимать значения right(по часовой стрелке), left(против часовой стрелки)
    #angle - угол, на который повернется танк
    def rotate_gun(angle = 1, side = 'right', number_of_tank = 1):
        assert (angle > 0)

        global rotate_gun_1_code, rotate_gun_2_code

        code = str(angle) + side

        if number_of_tank == 1 and rotate_gun_1_code != code:
            global stop_tank1_gun_side_angle

            global tank1_body_position_x
            global tank1_body_position_y
            global tank1_gun_rotation

            rotate_gun_1_code = code

            tank1_gun_layer.tank_gun_image.stop()
            gun_driver = tankGunDriver()

            stop_tank1_gun_side_angle = 0

            gun_driver.tankGunDriver_settings(tank1_body_position_x,
                                                tank1_body_position_y,
                                                tank1_gun_rotation,
                                                angle,
                                                side,
                                                stop_tank1_gun_side_angle,
                                                1)

            tank1_gun_layer.tank_gun_image.do(gun_driver)
        elif number_of_tank == 2 and rotate_gun_2_code != code:
            global stop_tank2_gun_side_angle

            global tank2_body_position_x
            global tank2_body_position_y
            global tank2_gun_rotation

            rotate_gun_2_code = code

            tank2_gun_layer.tank_gun_image.stop()
            gun_driver = tankGunDriver()

            stop_tank2_gun_side_angle = 0

            gun_driver.tankGunDriver_settings(tank2_body_position_x,
                                              tank2_body_position_y,
                                              tank2_gun_rotation,
                                              angle,
                                              side,
                                              stop_tank2_gun_side_angle,
                                              2)
            tank2_gun_layer.tank_gun_image.do(gun_driver)

#class driverByFirstUser(Driver):
#    def step(self, dt):
#        if(tank1_body_position_y <= tank1_start_y+100):
#            tank_library_initialize.move_tank_body('w', 70, 0, 1)
#        if(tank1_body_position_y >= 300):
#            tank_library_initialize.move_tank_body('w', -70, 0, 1)
#            tank_library_initialize.rotate_gun(115, 'right', 1)
#
#class driverBySecondUser(Driver):
#    def step(self, dt):
#        tank_library_initialize.move_tank_body('w', 20, 30, 2
#        tank_library_initialize.rotate_gun(15, 'right', 2)


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
                                        tank1_health,
                                        tank2_health,
                                        (255, 0, 0, 255),
                                        1,
                                        bool1)
#Создание класса пушки второго танка
tank2_gun_layer = tankGunAndBulletLayer(tank2_body_position_x,
                                        tank2_body_position_y,
                                        tank2_health,
                                        tank1_health,
                                        (0, 0, 255, 255),
                                        2,
                                        bool2)

#Обнолвение библиотечных функций
FirstTankClass.tank_mechanics.move_tank_body = tank_library_initialize.move_tank_body
FirstTankClass.tank_mechanics.rotate_gun = tank_library_initialize.rotate_gun
FirstTankClass.tank_mechanics.get_x = tank_library_initialize.get_x
FirstTankClass.tank_mechanics.get_y = tank_library_initialize.get_y

#Подключение драйверов разработчиков
tank1_body_layer.do(FirstTankClass.driverByFirstUser())
tank2_body_layer.do(SecondTankClass.driverBySecondUser())

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

#director.run(scene)
