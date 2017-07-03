from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.layer import ScrollingManager, ScrollableLayer
from cocos.scene import Scene
import math
import time
import random
import pyglet
from cocos import draw
from ctypes import *
from tank_library import*
from cocos.text import Label
from cocos.actions import*
from pyglet.window import key
from cocos.director import director
from cocos.scenes.transitions import FadeTRTransition
from cocos.actions import Rotate, ScaleBy, RotateTo
import FirstTankClass  # Класс управления первого пользователя
import SecondTankClass  # Класс управления второго пользователя
import inspect  # Стек функций, нужен, чтобы определить, какая функция какую функцию вызывает
from FinalScene import FinalScene, FinalMenu, FinalBack

director.init(width=800, height=600, autoscale=False, resizable=False)

keyboard = key.KeyStateHandler()

scroller = ScrollingManager()

# Координаты тела первого танка
tank1_body_position_x = 250
tank1_body_position_y = 150
tank1_body_rotation = 0

# Координаты тела второго танка
tank2_body_position_x = 400
tank2_body_position_y = 300
tank2_body_rotation = 0

# Максимальные углы поворота корпуса и орудия
TANK_MAX_ANGLE_OF_BODY_ROTATION = 30
TANK_MAX_ANGLE_OF_GUN_ROTATION = 155

# Угол поворота башни первого и второго танков
tank1_gun_rotation = 0
tank2_gun_rotation = 0

# Здороваье и урон первого танка
tank1_health = 100
TANK1_DAMAGE = 10

# Здороваье и урон второго танка
tank2_health = 100
TANK2_DAMAGE = 10

# Урон от столкновения со стенами
WALL_DAMAGE = 1

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
BULLET_MAX_SPEED = 700

# Прекращение вращения
stop_tank1_gun_side_angle = 0
stop_tank2_gun_side_angle = 0

# Попал ли танк
is_hitted1 = 0
is_hitted2 = 0

# Происходит ли перезарядка
is_recharging1 = 0
is_recharging2 = 0

bool_end = 1
bool_border1 = 1
bool_border2 = 1

# Перечисленные ниже коды нужны для оптимизации работы
# Уникальные коды move_tank_body
move_tank_body_1_code = ''
move_tank_body_2_code = ''

# Уникальные коды rotate_gun
rotate_gun_1_code = ''
rotate_gun_2_code = ''

# Уникальные коды set_nickname
set_nickname_1_code = ''
set_nickname_2_code = ''

# Размеры танка в пикселях
TANK_WIDTH = 36
TANK_HEIGHT = 39

# Размер анимации загрузки
RELOAD_IMAGE_SIZE = 20

# Выбор танка
key_choose = 0

# Танк, на который ставится фокус
focus_on = 1

# Время остановки
stop_time1 = 0
stop_time2 = 0

# Промежуток между перезапуском прицеливания
make_gun_angle_time1 = 0
make_gun_angle_time2 = 0

# Инвертировать движение танка
invert_moving1 = 1
invert_moving2 = 1

# Инвертировать поворот корпуса
invert_body_rotate1 = 1
invert_body_rotate2 = 1

# Инвертировать поворот башни
invert_gun_rotate1 = 1
invert_gun_rotate2 = 1

# Время последнего выстрела танка
last_tank1_shot_time = 0
last_tank2_shot_time = 0

time1 = 0
time2 = 0
timer = 60

# Все объекты графического интерфейса, привязанные к танкам, цепляем за класс отрисовки пушки!
# В драйвере stripDriver закрепляем их координаты


# Управление счётчиком
class TimerDriver(Driver):

    def step(self, dt):
        super(TimerDriver, self).step(dt)

        global time1, time2, timer, tank1_health, tank2_health
        if time2 == time1 == 0:
            time2 = time.clock()
            time1 = time.clock()

        if time2 - time1 >= 1:
            timer -= 1
            if timer < 10:
                if timer_label.element.color == (255, 0, 0, 180):
                    timer_label.element.color = (255, 255, 255, 180)
                else:
                    timer_label.element.color = (255, 0, 0, 180)
                l = '0' + str(timer)
            else:
                l = str(timer)

            timer_label.element.text = l
            if timer == 0:

                tank2_body_layer.tank_body_image.do(
                        ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))
                tank2_body_layer.tank_body_image.do(FadeOut(1))
                tank2_gun_layer.tank_gun_image.do(FadeOut(1))

                tank1_body_layer.tank_body_image.do(
                        ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))
                tank1_body_layer.tank_body_image.do(FadeOut(1))
                tank1_gun_layer.tank_gun_image.do(FadeOut(1))

                final_scene = Scene()
                final_scene.add(FinalScene('красный'))
                final_scene.add(FinalMenu())
                timer_label.stop()
                director.run(FadeTRTransition(final_scene, duration=2))

            time2 = time1 = 0

        else:
            time2 = time.clock()


# Управление полоской здоровья
class StripDriver(Driver):

    # Настройка класса(выбор к какому танку подключается драйвер)
    def strip_driver_settings(self, number_of_tank):
        self.number_of_tank = number_of_tank

    def step(self, dt):
        super(StripDriver, self).step(dt)
        global TANK_WIDTH, TANK_HEIGHT, RELOAD_IMAGE_SIZE, tank1_health, tank2_health

        if self.number_of_tank == 1 and tank1_health >= 0:
            global tank1_body_position_x, tank1_body_position_y, health_strip1
            tank1_gun_layer.remove(health_strip1)
            health_strip1 = StripCanvas(tank1_body_position_x,
                                        tank1_body_position_y,
                                        (255, 0, 0, 255),
                                        (122, 0, 0, 122),
                                        tank1_health)
            tank1_gun_layer.add(health_strip1)

        elif self.number_of_tank == 2 and tank2_health >= 0:
            global tank2_body_position_x, tank2_body_position_y, health_strip2
            tank2_gun_layer.remove(health_strip2)
            health_strip2 = StripCanvas(tank2_body_position_x,
                                        tank2_body_position_y,
                                        (0, 0, 255, 255),
                                        (0, 0, 122, 122),
                                        tank2_health)
            tank2_gun_layer.add(health_strip2)


# Управление дулом пушки
class TankGunDriver(Driver):
    # Настройка класса(выбор к какому танку подключается драйвер)
    def tank_gun_driver_settings(
            self,
            tank_body_position_x=0,
            tank_body_position_y=0,
            tank_gun_rotation=0,
            user_tank_gun_angle=0,
            user_tank_gun_side_angle='r',
            stop_tank_gun_side_angle=0,
            number_of_tank=1
    ):
        self.tank_body_position_x = tank_body_position_x
        self.tank_body_position_y = tank_body_position_y
        self.tank_gun_rotation = tank_gun_rotation
        self.user_tank_gun_angle = user_tank_gun_angle
        self.user_tank_gun_side_angle = user_tank_gun_side_angle
        self.stop_tank_gun_side_angle = stop_tank_gun_side_angle
        self.number_of_tank = number_of_tank

    def step(self, dt):
        global TANK_MAX_ANGLE_OF_GUN_ROTATION, tank1_body_position_x

        super(TankGunDriver, self).step(dt)

        if self.number_of_tank == 1:
            global invert_gun_rotate1
            self.change_angle_gun(self, dt, invert_gun_rotate1)
        else:
            global invert_gun_rotate2
            self.change_angle_gun(self, dt, invert_gun_rotate2)

        # Обновление глобальных переменных
        if self.number_of_tank == 1:
            global tank1_gun_rotation, last_tank1_shot_time, is_recharging1
            tank1_gun_rotation = self.target.rotation
            if (time.clock() - last_tank1_shot_time > 1) and (is_recharging1 != 0):
                is_recharging1 = 0
        else:
            global tank2_gun_rotation, last_tank2_shot_time, is_recharging2
            tank2_gun_rotation = self.target.rotation
            if (time.clock() - last_tank2_shot_time > 1) and (is_recharging2 != 0):
                is_recharging2 = 0

    @staticmethod
    def change_angle_gun(self, dt, invert_gun_rotate):
        if key_choose == self.number_of_tank:
            self.target.rotation += (keyboard[101] - keyboard[113]) * TANK_MAX_ANGLE_OF_GUN_ROTATION * dt
        if self.stop_tank_gun_side_angle != 50:
            if self.user_tank_gun_angle < TANK_MAX_ANGLE_OF_GUN_ROTATION:
                if self.user_tank_gun_side_angle == "right":
                    self.target.rotation += self.user_tank_gun_angle / 50 * invert_gun_rotate
                else:
                    self.target.rotation -= self.user_tank_gun_angle / 50 * invert_gun_rotate
                self.stop_tank_gun_side_angle += 1
            else:
                if self.user_tank_gun_side_angle == "right":
                    self.target.rotation += TANK_MAX_ANGLE_OF_GUN_ROTATION / 50 * invert_gun_rotate
                    self.user_tank_gun_angle -= TANK_MAX_ANGLE_OF_GUN_ROTATION / 50
                else:
                    self.target.rotation -= TANK_MAX_ANGLE_OF_GUN_ROTATION / 50 * invert_gun_rotate
                    self.user_tank_gun_angle -= TANK_MAX_ANGLE_OF_GUN_ROTATION / 50


# Управление ракетами
class TankBulletDriver(Driver):

    # Настройка класса(выбор к какому танку подключается драйвер)
    def tank_bullet_driver_settings(self,
                                    tank_damage,
                                    tank_gun_rotation,
                                    number_of_tank):
        self.tank_damage = tank_damage
        self.tank_gun_rotation = tank_gun_rotation
        self.number_of_tank = number_of_tank

    # Управление полётом ракеты первого тела
    def step(self, dt):

        super(TankBulletDriver, self).step(dt)

        if self.number_of_tank == 1:
            global tank2_health, tank2_body_position_x, tank2_body_position_y

            self.tank_health = tank2_health
            self.tank_body_position_x = tank2_body_position_x
            self.tank_body_position_y = tank2_body_position_y
        else:
            global tank1_health, tank1_body_position_x, tank1_body_position_y

            self.tank_health = tank1_health

            self.tank_body_position_x = tank1_body_position_x
            self.tank_body_position_y = tank1_body_position_y

        self.target.rotation = self.tank_gun_rotation
        self.target.speed = BULLET_MAX_SPEED
        self.determine_hit(self)

    #Определение попадания ракеты в танк
    @staticmethod
    def determine_hit(self):
        global bool_end

        if bool_end:
            global tank2_body_position_x, tank2_body_position_y
            if self.number_of_tank == 1:
                global tank2_health, is_hitted1, TANK1_DAMAGE, bool_border2

                if math.sqrt(abs(tank2_body_position_x - self.target.x) ** 2 + abs(
                                tank2_body_position_y - self.target.y) ** 2) <= 25:
                    is_hitted1 = True
                    tank2_health -= TANK1_DAMAGE
                    tank2_body_layer.tank_body_image.do(
                            RotateTo(-15, 0.2) + RotateTo(+15, 0.2) + RotateTo(-15, 0.2) + RotateTo(+15, 0.2))

                if tank2_health <= 0:
                    tank2_body_layer.tank_body_image.do(
                        ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))

                    TankLibraryInitialize.die(2)
            elif self.number_of_tank == 2:
                global tank1_body_position_x, tank1_body_position_y
                global tank1_health, is_hitted2, TANK2_DAMAGE, bool_border1
                if math.sqrt(abs(tank1_body_position_x - self.target.x) ** 2 + abs(
                                tank1_body_position_y - self.target.y) ** 2) <= 25:
                        is_hitted2 = True
                        tank1_health -= TANK1_DAMAGE
                        tank1_body_layer.tank_body_image.do(
                            RotateTo(-15, 0.2) + RotateTo(+15, 0.2) + RotateTo(-15, 0.2) + RotateTo(+15, 0.2))

                if tank1_health <= 0:
                    TankLibraryInitialize.die(1)


# Управление телом
class TankBodyDriver (Driver):
    # Настройка класса(выбор к какому танку подключается драйвер)
    def tank_body_driver_setting(
            self,
            number_of_tank=1,
            tank_body_x=0,
            tank_body_y=0,
            tank_body_rotation=0,
            that_key='',
            tank_speed=0,
            max_speed=0,
            min_speed=0,
            user_body_rotation=0):
        self.number_of_tank = number_of_tank
        self.tank_body_position_x = tank_body_x
        self.tank_body_position_y = tank_body_y
        self.tank_body_rotation = tank_body_rotation
        self.key_clicked = that_key
        self.tank_speed = tank_speed
        self.user_tank_body_rotation = user_body_rotation
        self.max_speed = max_speed
        self.min_speed = min_speed

    def step(self, dt):
        global tank1_body_position_x, tank1_body_position_y, tank1_body_rotation, tank1_speed, tank1_health
        global tank2_body_position_x, tank2_body_position_y, tank2_body_rotation, tank2_speed, tank2_health
        global focus_on, bool_border1, bool_border2

        super(TankBodyDriver, self).step(dt)

        # Обновление фокуса
        if (focus_on == self.number_of_tank):
            scroller.set_focus(self.target.x, self.target.y)

        # Изменение скорости и угла поворота
        if self.number_of_tank == 1:
            global invert_moving1, invert_body_rotate1

            self.change_angle(dt, self.number_of_tank, invert_body_rotate1)
            self.change_speed(self.number_of_tank, invert_moving1)

            # Если танк погиб от удара об стенку
            if tank1_health <= 0 and bool_border1:
                TankLibraryInitialize.die(self.number_of_tank)

            # Если танк врезался в стенку
            if bool_border1:
                self.target.x = self.manage_side(self.number_of_tank, self.target.x <= 50, 51, self.target.x)
                self.target.x = self.manage_side(self.number_of_tank, self.target.x >= 1229, 1228, self.target.x)
                self.target.y = self.manage_side(self.number_of_tank, self.target.y <= 50, 51, self.target.y)
                self.target.y = self.manage_side(self.number_of_tank, self.target.y >= 1229, 1228, self.target.y)

            # Прикрепляем все танковые объекты к танку
            tank1_body_position_x = self.target.x
            tank1_body_position_y = self.target.y

            tank1_gun_layer.tank_gun_image.x = self.target.x
            tank1_gun_layer.tank_gun_image.y = self.target.y

            tank1_gun_layer.tank_gun_image_copy.x = self.target.x
            tank1_gun_layer.tank_gun_image_copy.y = self.target.y

            tank1_body_layer.focus_frame.x = self.target.x
            tank1_body_layer.focus_frame.y = self.target.y

            health_strip1.x = self.target.x
            health_strip1.y = self.target.y

            tank1_gun_layer.whoom_control_image.x = self.target.x - TANK_WIDTH - RELOAD_IMAGE_SIZE
            tank1_gun_layer.whoom_control_image.y = self.target.y + TANK_WIDTH

            tank1_gun_layer.reload_image.x = self.target.x + TANK_WIDTH + RELOAD_IMAGE_SIZE
            tank1_gun_layer.reload_image.y = self.target.y + TANK_HEIGHT

            nickname1_label.x = self.target.x - TANK_WIDTH
            nickname1_label.y = self.target.y + TANK_HEIGHT + RELOAD_IMAGE_SIZE

            tank1_body_rotation = self.target.rotation
            tank1_speed = self.target.speed

        else:
            global invert_moving2, invert_body_rotate2

            self.change_angle(dt, self.number_of_tank, invert_body_rotate2)
            self.change_speed(self.number_of_tank, invert_moving2)

            # Если танк погиб от удара об стенку
            if tank2_health <= 0 and bool_border2:
                TankLibraryInitialize.die(self.number_of_tank)

            # Если танк врезался в стенку
            if bool_border2:
                self.target.x = self.manage_side(self.number_of_tank, self.target.x <= 50, 51, self.target.x)
                self.target.x = self.manage_side(self.number_of_tank, self.target.x >= 1229, 1228, self.target.x)
                self.target.y = self.manage_side(self.number_of_tank, self.target.y <= 50, 51, self.target.y)
                self.target.y = self.manage_side(self.number_of_tank, self.target.y >= 1229, 1228, self.target.y)

            # Прикрепляем все танковые объекты к танку
            tank2_body_position_x = self.target.x
            tank2_body_position_y = self.target.y

            tank2_gun_layer.tank_gun_image.x = self.target.x
            tank2_gun_layer.tank_gun_image.y = self.target.y

            tank2_gun_layer.tank_gun_image_copy.x = self.target.x
            tank2_gun_layer.tank_gun_image_copy.y = self.target.y

            tank2_body_layer.focus_frame.x = self.target.x
            tank2_body_layer.focus_frame.y = self.target.y

            health_strip2.x = self.target.x
            health_strip2.y = self.target.y

            tank2_gun_layer.whoom_control_image.x = self.target.x - TANK_WIDTH - RELOAD_IMAGE_SIZE
            tank2_gun_layer.whoom_control_image.y = self.target.y + TANK_WIDTH

            tank2_gun_layer.reload_image.x = self.target.x + TANK_WIDTH + RELOAD_IMAGE_SIZE
            tank2_gun_layer.reload_image.y = self.target.y + TANK_HEIGHT

            nickname2_label.x = self.target.x - TANK_WIDTH
            nickname2_label.y = self.target.y + TANK_HEIGHT + RELOAD_IMAGE_SIZE

            tank2_body_rotation = self.target.rotation
            tank2_speed = self.target.speed

        self.determine_tanks_hit(self.number_of_tank)

    # Столкновение танков друг с другом
    def determine_tanks_hit(self, number_of_tank):
        global tank1_health, tank2_health
        global tank1_body_position_x, tank1_body_position_y
        global tank2_body_position_x, tank2_body_position_y
        if math.sqrt(abs(tank1_body_position_x - tank2_body_position_x) ** 2 + abs(
                        tank1_body_position_y - tank2_body_position_y) ** 2) <= TANK_WIDTH:

            teleport_image.do(FadeIn(0) + FadeOut(1))
            if number_of_tank == 1:
                tank1_body_layer.tank_body_image.do(
                    RotateBy(-360, 0.3) + RotateBy(-20, 0.2) + RotateBy(+20, 0.2) + RotateBy(
                        -20, 0.2) + RotateBy(20, 0.2))

                self.target.x = random.randint(60, 1200)
                self.target.y = random.randint(60, 1200)

            if number_of_tank == 2:
                tank2_body_layer.tank_body_image.do(
                    RotateBy(-360, 0.3) + RotateBy(-20, 0.2) + RotateBy(+20, 0.2) + RotateBy(
                        -20, 0.2) + RotateBy(20, 0.2))

                self.target.x = random.randint(60, 1200)
                self.target.y = random.randint(60, 1200)

            tank2_health -= WALL_DAMAGE * 5
            tank1_health -= WALL_DAMAGE * 5

    # Столкновение с границами
    @staticmethod
    def manage_side(number_of_tank, boolean, true, false):
        coordinate = false
        if boolean:
            coordinate = true
            if number_of_tank == 1:
                global tank1_health
                tank1_health -= WALL_DAMAGE
                tank1_body_layer.tank_body_image.do(
                    RotateBy(-10, 0.2) + RotateBy(+10, 0.2) + RotateBy(-10, 0.2) + RotateBy(+10, 0.2))
            else:
                global tank2_health
                tank2_health -= WALL_DAMAGE
                tank2_body_layer.tank_body_image.do(
                    RotateBy(-10, 0.2) + RotateBy(+10, 0.2) + RotateBy(-10, 0.2) + RotateBy(+10, 0.2))
        return coordinate

    # Поворот танка
    def change_angle(self, dt, number_of_tank, invert_body_rotate):
        global TANK_MAX_ANGLE_OF_BODY_ROTATION

        if key_choose == number_of_tank:
            self.target.rotation += (keyboard[100] - keyboard[97]) * TANK_MAX_ANGLE_OF_BODY_ROTATION * dt
        else:
            if self.user_tank_body_rotation < TANK_MAX_ANGLE_OF_BODY_ROTATION:
                self.target.rotation += self.user_tank_body_rotation * dt * invert_body_rotate
            else:
                self.target.rotation += TANK_MAX_ANGLE_OF_BODY_ROTATION * dt * invert_body_rotate

    # Скорость танка
    def change_speed(self, number_of_tank, invert_moving):
        if key_choose == number_of_tank:
            self.target.acceleration = (keyboard[119] - keyboard[115]) * 100
        else:
            first_boolean = (self.key_clicked == 'w')
            second_boolean = (self.key_clicked == 's')
            if self.tank_speed >= self.max_speed:
                self.target.speed = (first_boolean - second_boolean) * self.max_speed * invert_moving
            elif self.tank_speed <= self.min_speed:
                self.target.speed = (first_boolean - second_boolean) * self.min_speed * invert_moving
            else:
                self.target.speed = (first_boolean - second_boolean) * self.tank_speed * invert_moving

        if keyboard[key.ENTER]:
            self.target.speed = 0


# Отрисовка пуль и пушки
class TankGunAndBulletLayer(ScrollableLayer):

    reload_image = Sprite("res/reload.png")  # Картинка перезарядки
    whoom_control_image = Sprite("res/robot.png")  # Картинка управления
    tank_gun_image = Sprite("res/tank_pushka.png")  # Картинка пушки
    tank_gun_image_copy = Sprite("res/tank_pushka.png")  # Картинка, к которой крепится полоска здоровья
    bullet_array = [Sprite("res/bullet.png"), Sprite("res/bullet.png"), Sprite("res/bullet.png")]  # Массив пуль
    explosion_image = Sprite(pyglet.image.load_animation("res/explosion.gif"))  # Анимация взрыва

    def __init__(self):
        super(TankGunAndBulletLayer, self).__init__()

        # ОБЯЗАТЕЛЬНО ДУБЛИРОВАТЬ СПРАЙТЫ, ИНАЧЕ ДВА ОБЪЕКТЫ ПРЕВРАТЯТСЯ В ОДИН
        self.tank_gun_image = Sprite("res/tank_pushka.png")
        self.whoom_control_image = Sprite("res/robot.png")
        self.tank_gun_image_copy = Sprite("res/tank_pushka.png")
        self.reload_image = Sprite("res/reload.png")
        self.explosion_image = Sprite(pyglet.image.load_animation("res/explosion.gif"))

        self.j = 0

        self.whoom_control_image.do(ScaleBy(0.8, 0))
        self.reload_image.do(FadeOut(0))
        self.tank_gun_image_copy.do(FadeOut(0))
        self.explosion_image.do(FadeOut(0))

        self.bullet_array = [Sprite("res/bullet.png"), Sprite("res/bullet.png"), Sprite("res/bullet.png")]

        for i in range(len(self.bullet_array)):
            self.bullet_array[i].do(FadeOut(0))
            self.add(self.bullet_array[i])

        self.add(self.whoom_control_image)
        self.add(self.tank_gun_image)
        self.add(self.tank_gun_image_copy)
        self.add(self.reload_image)
        self.add(self.explosion_image)

    # Управление перезарядкой
    @staticmethod
    def shoot_bullet(j,
                     bullet_array,
                     number_of_tank,
                     position_x,
                     position_y):
        if number_of_tank == 1:
            global last_tank1_shot_time, tank1_body_position_x, tank1_body_position_y, is_hitted1, is_recharging1
            if last_tank1_shot_time == 0:
                last_tank1_shot_time = time.clock()
                TankGunAndBulletLayer.reload_animation_launch(tank1_gun_layer)
                is_hitted1 = False
                j = TankGunAndBulletLayer.push_bullet(
                    j,
                    bullet_array,
                    number_of_tank,
                    position_x,
                    position_y)
            else:
                if time.clock() - last_tank1_shot_time > 1:
                    TankGunAndBulletLayer.reload_animation_launch(tank1_gun_layer)
                    is_hitted1 = False
                    j = TankGunAndBulletLayer.push_bullet(
                        j,
                        bullet_array,
                        number_of_tank,
                        position_x,
                        position_y)
                    last_tank1_shot_time = time.clock()
                    is_recharging1 = 0
                else:
                    is_recharging1 += 0.5
        else:
            global last_tank2_shot_time, tank2_body_position_x, tank2_body_position_y, is_hitted2, is_recharging2
            if last_tank2_shot_time == 0:
                last_tank2_shot_time = time.clock()
                TankGunAndBulletLayer.reload_animation_launch(tank2_gun_layer)
                is_hitted2 = False
                j = TankGunAndBulletLayer.push_bullet(
                    j,
                    bullet_array,
                    number_of_tank,
                    position_x,
                    position_y)
            else:
                if time.clock() - last_tank2_shot_time > 1:
                    TankGunAndBulletLayer.reload_animation_launch(tank2_gun_layer)
                    is_hitted2 = False
                    j = TankGunAndBulletLayer.push_bullet(
                        j,
                        bullet_array,
                        number_of_tank,
                        position_x,
                        position_y)
                    last_tank2_shot_time = time.clock()
                    is_recharging2 = 0
                else:
                    is_recharging2 += 0.5
        return j

    # Запуск анимации перезагрузки
    @staticmethod
    def reload_animation_launch(tank_gun_layer):
        tank_gun_layer.reload_image.do(FadeIn(0))
        tank_gun_layer.reload_image.do(Rotate(360, 1))
        tank_gun_layer.reload_image.do(FadeOut(1))

    # Полёт ракеты
    @staticmethod
    def push_bullet(j,
                    bullet_array,
                    number_of_tank,
                    position_x,
                    position_y):

        if j >= len(bullet_array):
            while j > 0:
                j -= 1
                bullet_array[j].stop()

        if j < len(bullet_array):
            bullet_array[j].x = position_x
            bullet_array[j].y = position_y

            if number_of_tank == 1:
                global tank1_gun_rotation, TANK1_DAMAGE, tank1_body_position_x, tank1_body_position_y, is_recharging1
                bullet_array[j].rotation = tank1_gun_rotation
                bullet_array[j].x = tank1_body_position_x
                bullet_array[j].y = tank1_body_position_y
                tank_damage = TANK1_DAMAGE
            else:
                global tank2_gun_rotation, TANK2_DAMAGE,  tank2_body_position_x, tank2_body_position_y, is_recharging2
                bullet_array[j].rotation = tank2_gun_rotation
                bullet_array[j].x = tank2_body_position_x
                bullet_array[j].y = tank2_body_position_y
                tank_damage = TANK2_DAMAGE

            bullet_driver = TankBulletDriver()

            bullet_driver.tank_bullet_driver_settings(
                tank_damage,
                bullet_array[j].rotation,
                number_of_tank)
            if number_of_tank == 1:
                tank1_gun_layer.bullet_array[j].stop()
                tank1_gun_layer.bullet_array[j].do(FadeOut(1.5))
                tank1_gun_layer.bullet_array[j].do(bullet_driver)
            else:
                tank2_gun_layer.bullet_array[j].stop()
                tank2_gun_layer.bullet_array[j].do(FadeOut(1.5))
                tank2_gun_layer.bullet_array[j].do(bullet_driver)

            j += 1
        return j


# Слушатель событий клавиатуры
class KeyListener(ScrollableLayer):
    is_event_handler = True

    # Нажатие на клавишу
    @staticmethod
    def on_key_press(key_click, modifiers):
        global tank1_body_position_x, tank1_body_position_y, key_choose, focus_on

        # Клавиша пробел
        if key_click == 32 :
            if key_choose == 1:
                tank1_gun_layer.j = tank1_gun_layer.shoot_bullet(
                    tank1_gun_layer.j,
                    tank1_gun_layer.bullet_array,
                    key_choose,
                    tank1_body_position_x,
                    tank1_body_position_y)
            elif key_choose == 2:
                tank2_gun_layer.j = tank2_gun_layer.shoot_bullet(
                    tank2_gun_layer.j,
                    tank2_gun_layer.bullet_array,
                    key_choose,
                    tank2_body_position_x,
                    tank2_body_position_y)
        # Клавиша 'Z'
        if key_click == 122 and key_choose != 1:
            global move_tank_body_1_code, rotate_gun_1_code

            move_tank_body_1_code = ''
            rotate_gun_1_code = ''
            key_choose = 1
            focus_on = 1

            TankLibraryInitialize.stop_all()
            TankLibraryInitialize.connect1()
            TankLibraryInitialize.connect2(1)

            KeyListener.delete_and_load_image("res/man.png", "res/robot.png")

            tank2_body_layer.focus_frame.do(FadeOut(0))
            tank1_body_layer.focus_frame.do(FadeIn(0))

        # Клавиша 'X'
        if key_click == 120 and key_choose != 2:
            global move_tank_body_2_code, rotate_gun_2_code

            move_tank_body_2_code = ''
            rotate_gun_2_code = ''
            key_choose = 2
            focus_on = 2

            KeyListener.delete_and_load_image("res/robot.png", "res/man.png")

            TankLibraryInitialize.stop_all()
            TankLibraryInitialize.connect2()
            TankLibraryInitialize.connect1(1)

            tank1_body_layer.focus_frame.do(FadeOut(0))
            tank2_body_layer.focus_frame.do(FadeIn(0))

        # Клавиша 'C'
        if key_click == 99 and key_choose != 0:
            move_tank_body_1_code = ''
            rotate_gun_1_code = ''
            move_tank_body_2_code = ''
            rotate_gun_2_code = ''

            key_choose = 0
            TankLibraryInitialize.connect1(1)
            TankLibraryInitialize.connect2(1)

            KeyListener.delete_and_load_image("res/robot.png", "res/robot.png")

        # Клавиша '1'
        elif key_click == 49:
            focus_on = 1
            tank2_body_layer.focus_frame.do(FadeOut(0))
            tank1_body_layer.focus_frame.do(FadeIn(0))

        # Клавиша '2'(два)
        elif key_click == 50:
            focus_on = 2
            tank1_body_layer.focus_frame.do(FadeOut(0))
            tank2_body_layer.focus_frame.do(FadeIn(0))

    @staticmethod
    def delete_and_load_image(picture1, picture2):
        tank1_gun_layer.remove(tank1_gun_layer.whoom_control_image)
        tank2_gun_layer.remove(tank2_gun_layer.whoom_control_image)

        tank1_gun_layer.whoom_control_image = Sprite(picture1)
        tank2_gun_layer.whoom_control_image = Sprite(picture2)

        tank1_gun_layer.add(tank1_gun_layer.whoom_control_image)
        tank2_gun_layer.add(tank2_gun_layer.whoom_control_image)


# Отрисовка танка
class TankBodyLayer(ScrollableLayer):

    tank_body_image = Sprite("res/bullet.png")
    focus_frame = Sprite("res/focus_frame.png")

    def __init__(self, picture, pos, max_speed, min_speed):

        super(TankBodyLayer, self).__init__()

        self.tank_body_image = Sprite(picture)
        self.focus_frame = Sprite("res/focus_frame.png")
        self.tank_body_image.position = pos
        self.focus_frame.position = pos

        self.tank_body_image.max_forward_speed = max_speed
        self.tank_body_image.max_reverse_speed = min_speed

        self.focus_frame.do(FadeOut(0))

        self.add(self.focus_frame)
        self.add(self.tank_body_image)


# Рисование полоски
class StripCanvas(draw.Canvas):
    def __init__(self, x, y, main_color, color, health):
        super(StripCanvas, self).__init__()
        self.x = x
        self.y = y
        self.health = health
        self.main_color = main_color
        self.color = color
        self.render()

    def render(self):
        line_width = 10
        self.set_stroke_width(line_width)

        self.set_join(draw.ROUND_JOIN)

        self.full_life()
        self.real_life()

    def full_life(self):
        global TANK_HEIGHT, TANK_WIDTH
        self.set_color(self.color)
        self.move_to((-TANK_WIDTH*3/4, TANK_HEIGHT))
        self.line_to((-TANK_WIDTH*3/4 + 100 / 2, TANK_HEIGHT))

    def real_life(self):
        global TANK_HEIGHT, TANK_WIDTH
        self.set_color(self.main_color)
        self.move_to((-TANK_WIDTH*3/4, TANK_HEIGHT))
        self.line_to((-TANK_WIDTH*3/4 + self.health / 2, TANK_HEIGHT))


# Заполнение функций из библиотеки
class TankLibraryInitialize(TankMechanics):

    @staticmethod
    def fire():
        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            global tank1_gun_layer, tank1_body_position_x, tank1_body_position_y
            tank1_gun_layer.j = tank1_gun_layer.shoot_bullet(
                tank1_gun_layer.j,
                tank1_gun_layer.bullet_array,
                number_of_tank,
                tank1_body_position_x,
                tank1_body_position_y)
        else:
            global tank2_gun_layer, tank2_body_position_x, tank2_body_position_y
            tank2_gun_layer.j = tank2_gun_layer.shoot_bullet(
                tank2_gun_layer.j,
                tank2_gun_layer.bullet_array,
                number_of_tank,
                tank2_body_position_x,
                tank2_body_position_y)

    @staticmethod
    def get_boolean_hit_the_tank():
        global is_hitted1, is_hitted2

        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            return is_hitted1
        else:
            return is_hitted2

    @staticmethod
    def get_boolean_recharging():
        global is_recharging1, is_recharging2

        number_of_tank = TankLibraryInitialize.determine_the_number()
        if number_of_tank == 1:
            if is_recharging1 > 0:
                return True
            else:
                return False
        else:
            if is_recharging2 > 0:
                return True
            else:
                return False

    @staticmethod
    def stop_moving(t=0):
        global stop_time1, stop_time2

        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            TankLibraryInitialize.stop_moving1()
            stop_time1 = time.clock() + t
        else:
            TankLibraryInitialize.stop_moving2()
            stop_time2 = time.clock() + t

    @staticmethod
    def stop_moving1():
        TankLibraryInitialize.move_tank_body()

    @staticmethod
    def stop_moving2():
        TankLibraryInitialize.move_tank_body()

    @staticmethod
    def get_boolean_focus_on(self=0):
        global focus_on

        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == focus_on:
            return True
        else:
            return False

    @staticmethod
    def invert_moving(self=0):
        global invert_moving1, invert_moving2

        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            invert_moving1 *= -1
        else:
            invert_moving2 *= -1

    @staticmethod
    def invert_body_rotating(self=0):
        global invert_body_rotate1, invert_body_rotate2

        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            invert_body_rotate1 *= -1
        else:
            invert_body_rotate2 *= -1

    @staticmethod
    def invert_gun_rotating(self=0):
        global invert_gun_rotate1, invert_gun_rotate2

        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            invert_gun_rotate1 *= -1
        else:
            invert_gun_rotate2 *= -1

    @staticmethod
    def set_nickname(nickname='Tank'):
        global set_nickname_1_code, set_nickname_2_code

        number_of_tank = TankLibraryInitialize.determine_the_number()

        if (number_of_tank == 1) and (set_nickname_1_code != nickname):
            global nickname1_label

            set_nickname_1_code = nickname

            tank1_gun_layer.remove(nickname1_label)
            nickname1_label = Label(nickname,
                                    font_name="BOLD",
                                    font_size=15,
                                    color=(255, 0, 0, 180))
            tank1_gun_layer.add(nickname1_label)
        elif (number_of_tank == 2) and (set_nickname_2_code != nickname):
            global nickname2_label

            set_nickname_2_code = nickname

            tank2_gun_layer.remove(nickname2_label)
            nickname2_label = Label(nickname,
                                    font_name="BOLD",
                                    font_size=15,
                                    color=(0, 0, 255, 180))
            tank2_gun_layer.add(nickname2_label)

    @staticmethod
    def get_body_angle(self=0):
        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            global tank1_body_rotation
            return tank1_body_rotation
        else:
            global tank2_body_rotation
            return tank2_body_rotation

    @staticmethod
    def get_gun_angle(self=0):
        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            global tank1_gun_rotation
            return tank1_gun_rotation
        else:
            global tank2_gun_rotation
            return tank2_gun_rotation

    @staticmethod
    def get_health(self=0):
        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            global tank1_health
            return tank1_health
        else:
            global tank2_health
            return tank2_health

    @staticmethod
    def get_speed(self=0):
        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            global tank1_speed
            return tank1_speed
        else:
            global tank2_speed
            return tank2_speed

    @staticmethod
    def get_enemy_x(self=0):
        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            global tank2_body_position_x
            return tank2_body_position_x
        else:
            global tank1_body_position_x
            return tank1_body_position_x

    @staticmethod
    def get_enemy_y(self=0):
        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            global tank2_body_position_y
            return tank2_body_position_y
        else:
            global tank1_body_position_y
            return tank1_body_position_y

    @staticmethod
    def get_last_enemy_shot_time(self=0):
        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            global last_tank2_shot_time
            return last_tank2_shot_time
        else:
            global last_tank1_shot_time
            return last_tank1_shot_time

    @staticmethod
    def get_x(self=0):

        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            global tank1_body_position_x
            return tank1_body_position_x
        else:
            global tank2_body_position_x
            return tank2_body_position_x

    @staticmethod
    def get_y(self=0):

        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            global tank1_body_position_y
            return tank1_body_position_y
        else:
            global tank2_body_position_y
            return tank2_body_position_y

    @staticmethod
    def pointing():
        global tank1_body_position_x, tank1_body_position_y
        global tank2_body_position_x, tank2_body_position_y
        adder = CDLL('./make_angle.dll')

        number_of_tank = TankLibraryInitialize.determine_the_number()

        if number_of_tank == 1:
            x1 = c_float(tank1_body_position_x)
            x2 = c_float(tank2_body_position_x)
            y1 = c_float(tank1_body_position_y)
            y2 = c_float(tank2_body_position_y)
        else:
            x2 = c_float(tank1_body_position_x)
            x1 = c_float(tank2_body_position_x)
            y2 = c_float(tank1_body_position_y)
            y1 = c_float(tank2_body_position_y)

        make_angle = adder.make_angle
        make_angle.restype = c_float
        return make_angle(x1, y1, x2, y2)

    @staticmethod
    def move_tank_body(that_key='w', speed=0, rotation=0):
        global move_tank_body_1_code, move_tank_body_2_code, stop_time1, stop_time2

        number_of_tank = TankLibraryInitialize.determine_the_number()

        (frame, filename, line_number, function_name, lines, index) = \
            inspect.getouterframes(inspect.currentframe())[2]

        code = that_key + str(speed) + str(rotation) + function_name

        if (number_of_tank == 1) and (move_tank_body_1_code != code) and (time.clock() > stop_time1):

            tank1_body_layer.tank_body_image.stop()
            move_tank_body_1_code = code
            body_driver = TankBodyDriver()

            global TANK1_MAX_FORWARD_SPEED
            global TANK1_MAX_REVERSE_SPEED
            global tank1_body_position_x
            global tank1_body_position_y
            global tank1_body_rotation

            body_driver.tank_body_driver_setting(
                number_of_tank,
                tank1_body_position_x,
                tank1_body_position_y,
                tank1_body_rotation,
                that_key,
                speed,
                TANK1_MAX_FORWARD_SPEED,
                TANK1_MAX_REVERSE_SPEED,
                rotation
            )

            tank1_body_layer.tank_body_image.do(body_driver)

            gun_driver = TankGunDriver()
            gun_driver.tank_gun_driver_settings(
                tank1_body_position_x,
                tank1_body_position_y,
                tank1_gun_rotation,
                0,
                'r',
                0,
                1)
            tank1_gun_layer.tank_gun_image.do(gun_driver)
        elif (number_of_tank == 2) and (move_tank_body_2_code != code) and (time.clock() > stop_time2):

            tank2_body_layer.tank_body_image.stop()
            move_tank_body_2_code = code
            body_driver = TankBodyDriver()

            global TANK2_MAX_FORWARD_SPEED
            global TANK2_MAX_REVERSE_SPEED
            global tank2_body_position_x
            global tank2_body_position_y
            global tank2_body_rotation

            body_driver.tank_body_driver_setting(
                number_of_tank,
                tank2_body_position_x,
                tank2_body_position_y,
                tank2_body_rotation,
                that_key,
                speed,
                TANK2_MAX_FORWARD_SPEED,
                TANK2_MAX_REVERSE_SPEED,
                rotation
            )

            tank2_body_layer.tank_body_image.do(body_driver)

            gun_driver = TankGunDriver()
            gun_driver.tank_gun_driver_settings(
                tank1_body_position_x,
                tank1_body_position_y,
                tank1_gun_rotation,
                0,
                'r',
                0,
                2)
            tank2_gun_layer.tank_gun_image.do(gun_driver)

    @staticmethod
    def make_gun_angle(angle=1):
        global TANK_MAX_ANGLE_OF_GUN_ROTATION, make_gun_angle_time1, make_gun_angle_time2

        if time.clock() > make_gun_angle_time1:
            make_gun_angle_time1 = time.clock() + 0.1

            number_of_tank = TankLibraryInitialize.determine_the_number()

            # side = 'right'
            # if angle < 0:
            #    angle *= -1
            #    side = 'left'
#
            if number_of_tank == 1:
                tank1_gun_layer.tank_gun_image.rotation = angle
#
                # print(angle,tank1_gun_layer.tank_gun_image.rotation)
#
            #    if tank1_gun_rotation != angle:
            #        if angle < TANK_MAX_ANGLE_OF_GUN_ROTATION:
            #            tank_library_initialize.rotate_gun1(angle, side, 1)
            #        else:
            #            tank_library_initialize.rotate_gun1(TANK_MAX_ANGLE_OF_GUN_ROTATION, side, 1)
            else:
                tank2_gun_layer.tank_gun_image.rotation = angle
            #    if tank2_gun_rotation != angle:
            #        if angle < TANK_MAX_ANGLE_OF_GUN_ROTATION:
            #            tank_library_initialize.rotate_gun2(angle, side, 1)
            #        else:
            #            tank_library_initialize.rotate_gun2(TANK_MAX_ANGLE_OF_GUN_ROTATION, side, 1)

    @staticmethod
    def rotate_gun1(angle=1, side='right', continued=0):
        TankLibraryInitialize.rotate_gun(angle, side, continued)

    @staticmethod
    def rotate_gun2(angle=1, side='right', continued=0):
        TankLibraryInitialize.rotate_gun(angle, side, continued)

    @staticmethod
    def rotate_gun(angle=1, side='right', continued=0):
        assert (angle > 0)

        # print('sooo',angle, side)

        global rotate_gun_1_code, rotate_gun_2_code

        number_of_tank = TankLibraryInitialize.determine_the_number()

        (frame, filename, line_number, function_name, lines, index) = \
            inspect.getouterframes(inspect.currentframe())[2]

        code = str(angle) + side + function_name

        if (number_of_tank) == 1 and ((rotate_gun_1_code != code) or (continued == 1)):
            global stop_tank1_gun_side_angle

            global tank1_body_position_x
            global tank1_body_position_y
            global tank1_gun_rotation

            rotate_gun_1_code = code

            tank1_gun_layer.tank_gun_image.stop()
            gun_driver = TankGunDriver()

            stop_tank1_gun_side_angle = 0

            gun_driver.tank_gun_driver_settings(tank1_body_position_x,
                                                tank1_body_position_y,
                                                tank1_gun_rotation,
                                                angle,
                                                side,
                                                stop_tank1_gun_side_angle,
                                                1)

            tank1_gun_layer.tank_gun_image.do(gun_driver)
        elif (number_of_tank == 2) and ((rotate_gun_2_code != code) or (continued == 1)):
            global stop_tank2_gun_side_angle

            global tank2_body_position_x
            global tank2_body_position_y
            global tank2_gun_rotation

            rotate_gun_2_code = code

            tank2_gun_layer.tank_gun_image.stop()
            gun_driver = TankGunDriver()

            stop_tank2_gun_side_angle = 0

            gun_driver.tank_gun_driver_settings(
                tank2_body_position_x,
                tank2_body_position_y,
                tank2_gun_rotation,
                angle,
                side,
                stop_tank2_gun_side_angle,
                2)
            tank2_gun_layer.tank_gun_image.do(gun_driver)

    @staticmethod
    def determine_the_number():
        (frame, filename, line_number, function_name, lines, index) = \
            inspect.getouterframes(inspect.currentframe())[2]

        number_of_tank = 0
        if 'FirstTankClass' in filename:
            number_of_tank = 1
        elif 'SecondTankClass' in filename:
            number_of_tank = 2
        elif 'main':
            if '1' in function_name:
                number_of_tank = 1
            elif '2' in function_name:
                number_of_tank = 2
        return number_of_tank

    @staticmethod
    def stop_all(real_all=0):
        tank1_body_layer.stop()
        tank2_body_layer.stop()

        # tank_body_layer.tank_body_image.stop() не отключать, он регулируется в move_tank_body

        tank1_gun_layer.stop()
        tank2_gun_layer.stop()
        tank1_gun_layer.tank_gun_image.stop()
        tank2_gun_layer.tank_gun_image.stop()
        tank1_gun_layer.tank_gun_image_copy.stop()
        tank2_gun_layer.tank_gun_image_copy.stop()

        if real_all == 1:
            tank1_body_layer.stop()
            tank2_body_layer.stop()

    @staticmethod
    def connect1(connect_user=0):
        if connect_user == 0:
            TankLibraryInitialize.move_tank_body()
            TankLibraryInitialize.rotate_gun()
        else:
            tank1_body_layer.do(FirstTankClass.driverByFirstUser())

        strip_health1_driver = StripDriver()
        strip_health1_driver.strip_driver_settings(1)
        tank1_gun_layer.tank_gun_image_copy.do(strip_health1_driver)

    @staticmethod
    def connect2(connect_user=0):
        if connect_user == 0:
            TankLibraryInitialize.move_tank_body()
            TankLibraryInitialize.rotate_gun()
        else:
            tank2_body_layer.do(SecondTankClass.driverBySecondUser())

        strip_health2_driver = StripDriver()
        strip_health2_driver.strip_driver_settings(2)
        tank2_gun_layer.tank_gun_image_copy.do(strip_health2_driver)

    @staticmethod
    def die(number_of_tank):
        global bool_end
        bool_end = 0

        if number_of_tank == 1:
            global bool_border1

            tank1_body_layer.tank_body_image.do(
                ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))

            # Исчезновение погибшего танка
            tank1_body_layer.tank_body_image.do(FadeOut(1))
            tank1_gun_layer.tank_gun_image.do(FadeOut(1))
            nickname1_label.do(FadeOut(1))
            health_strip1.do(FadeOut(1))

            name = 'танк названием "' + nickname2_label.element.text + '"'
            bool_border1 = 0
        else:
            global bool_border2

            tank2_body_layer.tank_body_image.do(
                ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2) + ScaleBy(1.5, 0.2) + ScaleBy(2 / 3, 0.2))

            # Исчезновение погибшего танка
            tank2_body_layer.tank_body_image.do(FadeOut(1))
            tank2_gun_layer.tank_gun_image.do(FadeOut(1))
            nickname2_label.do(FadeOut(1))
            health_strip2.do(FadeOut(1))

            name = 'танк названием "' + nickname1_label.element.text + '"'
            bool_border2 = 0

        # Запуск финальной сцены
        final_scene = Scene()
        final_scene.add(FinalScene(name))
        final_scene.add(FinalBack())
        final_scene.add(FinalMenu())
        director.replace(FadeTRTransition(final_scene, duration=2))

# Создание класса корпуса первого танка
tank1_body_layer = TankBodyLayer(
    "res/tank_telo.png",
    (tank1_body_position_x, tank1_body_position_y),
    TANK1_MAX_FORWARD_SPEED,
    TANK1_MAX_REVERSE_SPEED)

# Создание класса корпуса второго танка
tank2_body_layer = TankBodyLayer(
    "res/tank_telo2.png",
    (tank2_body_position_x, tank2_body_position_y),
    TANK2_MAX_FORWARD_SPEED,
    TANK2_MAX_REVERSE_SPEED)

# Создание классов пушек
tank1_gun_layer = TankGunAndBulletLayer()
tank2_gun_layer = TankGunAndBulletLayer()

# Установка названия первого танка
nickname1_label = Label("Tank1",
                        font_name="BOLD",
                        font_size=15,
                        color=(255, 0, 0, 180))
tank1_gun_layer.add(nickname1_label)

# Установка названия второго танка
nickname2_label = Label("Tank2",
                        font_name="BOLD",
                        font_size=15,
                        color=(0, 0, 255, 180))
tank2_gun_layer.add(nickname2_label)

# Полоска жизней первого танка и её настройка
health_strip1 = StripCanvas(
    0,
    0,
    (0, 0, 255, 255),
    (0, 0, 122, 122),
    tank1_health)
tank1_gun_layer.add(health_strip1)

# Полоска жизней второго танка и её настройка
health_strip2 = StripCanvas(
    0,
    0,
    (0, 0, 255, 255),
    (0, 0, 122, 122),
    tank2_health)
tank2_gun_layer.add(health_strip2)

# Обновление библиотечных функций
TankMechanics.move_tank_body = TankLibraryInitialize.move_tank_body
TankMechanics.rotate_gun = TankLibraryInitialize.rotate_gun
TankMechanics.get_x = TankLibraryInitialize.get_x
TankMechanics.get_y = TankLibraryInitialize.get_y
TankMechanics.get_gun_angle = TankLibraryInitialize.get_gun_angle
TankMechanics.get_body_angle = TankLibraryInitialize.get_body_angle
TankMechanics.set_nickname = TankLibraryInitialize.set_nickname
TankMechanics.fire = TankLibraryInitialize.fire
TankMechanics.get_boolean_hit_the_tank = TankLibraryInitialize.get_boolean_hit_the_tank
TankMechanics.get_boolean_recharging = TankLibraryInitialize.get_boolean_recharging
TankMechanics.get_boolean_focus_on = TankLibraryInitialize.get_boolean_focus_on
TankMechanics.stop_moving = TankLibraryInitialize.stop_moving
TankMechanics.invert_moving = TankLibraryInitialize.invert_moving
TankMechanics.invert_body_rotating = TankLibraryInitialize.invert_body_rotating
TankMechanics.invert_gun_rotating = TankLibraryInitialize.invert_gun_rotating
TankMechanics.get_health = TankLibraryInitialize.get_health
TankMechanics.get_speed = TankLibraryInitialize.get_speed
TankMechanics.get_enemy_x = TankLibraryInitialize.get_enemy_x
TankMechanics.get_enemy_y = TankLibraryInitialize.get_enemy_y
TankMechanics.get_last_enemy_shot_time = TankLibraryInitialize.get_last_enemy_shot_time
TankMechanics.make_gun_angle = TankLibraryInitialize.make_gun_angle
TankMechanics.pointing = TankLibraryInitialize.pointing

# Подключение драйверов разработчиков
TankLibraryInitialize.connect1(1)
TankLibraryInitialize.connect2(1)

# Настройка карты
map_layer = load("res/road.tmx")["map0"]
scroller.add(map_layer)

keyListener = KeyListener()

# Покдючаем танки
scroller.add(tank1_body_layer)
scroller.add(tank2_body_layer)
scroller.add(tank1_gun_layer)
scroller.add(tank2_gun_layer)
scroller.add(keyListener)

scene = Scene(scroller)

director.set_show_FPS = True
director.show_FPS = True

# Счётчик времени
timer_label = Label(
    "60",
    font_name="BOLD",
    font_size=25,
    position=(375, 540),
    color=(255, 255, 255, 180))
timer_label.do(TimerDriver())
timer_frame = Sprite("res/timer_frame.png")
timer_frame.position = (394, 553)

teleport_image = Sprite("res/teleport.png")
teleport_image.position = (400, 300)
teleport_image.do(FadeOut(0))

scene.add(teleport_image)
scene.add(timer_frame)
scene.add(timer_label)

director.window.push_handlers(keyboard)

#director.run(scene)
