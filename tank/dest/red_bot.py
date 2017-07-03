import math
import time
from tank_library import*
from cocos.actions import Driver

class driverByFirstUser(Driver):
    def step(self, dt):
        #print(time.clock(),dt)
        driverByFirstUser.strategy2()

    def strategy1(self = 0):
        TankMechanics.set_nickname('Анастасия')
        if (TankMechanics.get_boolean_recharging() == False):
            TankMechanics.stop_moving(0.3)
            TankMechanics.rotate_gun(15, 'right', 1)
        else:
            TankMechanics.move_tank_body('w', 70, -60)
            TankMechanics.fire()

    def move_tank_body(key='', speed=0, rotation=0):
        pass

    def rotate_gun(angle=1, side='right', continued=0):
        pass

    @staticmethod
    def strategy3(s):
        s.move_tank_body('w', 80)
        s.rotate_gun(1, 'right')

    @staticmethod
    def strategy2(seeel):
        #seeel.set_nickname('Екатерина')
        if seeel.get_y() >= 50:
            seeel.move_tank_body('w', -80)
        elif seeel.get_y() <= 1200:
            seeel.move_tank_body('w', 80)
        if seeel.get_speed() == 0:
            seeel.move_tank_body('w', 80)
        angle = math.degrees(math.atan((seeel.get_enemy_y() - seeel.get_y())/
                          (seeel.get_enemy_x() - seeel.get_x())))
        #print(TankMechanics.pointing())
        driverByFirstUser.determine_angle(angle)
        seeel.fire()

    @staticmethod
    def determine_angle(angle):
        if ((TankMechanics.get_enemy_x() - TankMechanics.get_x() > 0) and
            (TankMechanics.get_enemy_y() - TankMechanics.get_y() > 0)):
            TankMechanics.make_gun_angle(90 - angle)
        elif ((TankMechanics.get_enemy_x() - TankMechanics.get_x() < 0) and
                (TankMechanics.get_enemy_y() - TankMechanics.get_y() > 0)):
            TankMechanics.make_gun_angle( - angle - 90)
        elif ((TankMechanics.get_enemy_x() - TankMechanics.get_x() < 0) and
                  (TankMechanics.get_enemy_y() - TankMechanics.get_y() < 0)):
            TankMechanics.make_gun_angle(- angle + 270)
        elif ((TankMechanics.get_enemy_x() - TankMechanics.get_x() > 0) and
                  (TankMechanics.get_enemy_y() - TankMechanics.get_y() < 0)):
            TankMechanics.make_gun_angle(-angle + 90)
        elif  ((TankMechanics.get_enemy_x() - TankMechanics.get_x() == 0) and
                  (TankMechanics.get_enemy_y() - TankMechanics.get_y() < 0)):
            TankMechanics.make_gun_angle(180)
        elif  ((TankMechanics.get_enemy_x() - TankMechanics.get_x() == 0) and
                  (TankMechanics.get_enemy_y() - TankMechanics.get_y() > 0)):
            TankMechanics.make_gun_angle(0)
        elif  ((TankMechanics.get_enemy_x() - TankMechanics.get_x() > 0) and
                  (TankMechanics.get_enemy_y() - TankMechanics.get_y() == 0)):
            TankMechanics.make_gun_angle(0)
