from tank_library import*
import math
from cocos.actions import Driver
class driverByFirstUser(Driver):
    def step(self, dt):
        driverByFirstUser.strategy2()

    def strategy1(self = 0):
        tank_mechanics.set_nickname('Анастасия')
        if (tank_mechanics.get_boolean_recharging() == False):
            tank_mechanics.stop_moving(0.3)
            tank_mechanics.rotate_gun(15, 'right', 1)
        else:
            tank_mechanics.move_tank_body('w', 70, -60)
        tank_mechanics.fire()

    def strategy2(self=0):
        tank_mechanics.set_nickname('Екатерина')
        if tank_mechanics.get_y() >= tank_mechanics.right_up_end_of_map:
            tank_mechanics.move_tank_body('w', -80)
        elif tank_mechanics.get_y() <= tank_mechanics.left_down_end_of_map:
            tank_mechanics.move_tank_body('w', 80)
        if tank_mechanics.get_speed() == 0:
            tank_mechanics.move_tank_body('w', 80)
        angle = math.degrees(math.atan((tank_mechanics.get_enemy_y() - tank_mechanics.get_y())/
                          (tank_mechanics.get_enemy_x() - tank_mechanics.get_x())))
        driverByFirstUser.determine_angle(angle)
        tank_mechanics.fire()

    def determine_angle(angle):
        if ((tank_mechanics.get_enemy_x() - tank_mechanics.get_x() > 0) and
            (tank_mechanics.get_enemy_y() - tank_mechanics.get_y() > 0)):
            tank_mechanics.make_gun_angle(90 - angle)
        elif ((tank_mechanics.get_enemy_x() - tank_mechanics.get_x() < 0) and
                (tank_mechanics.get_enemy_y() - tank_mechanics.get_y() > 0)):
            tank_mechanics.make_gun_angle( - angle - 90)
        elif ((tank_mechanics.get_enemy_x() - tank_mechanics.get_x() < 0) and
                  (tank_mechanics.get_enemy_y() - tank_mechanics.get_y() < 0)):
            tank_mechanics.make_gun_angle(- angle + 270)
        elif ((tank_mechanics.get_enemy_x() - tank_mechanics.get_x() > 0) and
                  (tank_mechanics.get_enemy_y() - tank_mechanics.get_y() < 0)):
            tank_mechanics.make_gun_angle(-angle + 90)
        elif  ((tank_mechanics.get_enemy_x() - tank_mechanics.get_x() == 0) and
                  (tank_mechanics.get_enemy_y() - tank_mechanics.get_y() < 0)):
            tank_mechanics.make_gun_angle(180)
        elif  ((tank_mechanics.get_enemy_x() - tank_mechanics.get_x() == 0) and
                  (tank_mechanics.get_enemy_y() - tank_mechanics.get_y() > 0)):
            tank_mechanics.make_gun_angle(0)
        elif  ((tank_mechanics.get_enemy_x() - tank_mechanics.get_x() > 0) and
                  (tank_mechanics.get_enemy_y() - tank_mechanics.get_y() == 0)):
            tank_mechanics.make_gun_angle(0)
