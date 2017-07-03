import math
from tank_library import*
from cocos.actions import Driver

class driverByFirstUser(Driver):
    def step(self, dt):
        driverByFirstUser.strategy2()

    def strategy1(self = 0):
        TankMechanics.set_nickname('Анастасия')
        if (TankMechanics.get_boolean_recharging() == False):
            TankMechanics.stop_moving(0.3)
            TankMechanics.rotate_gun(15, 'right', 1)
        else:
            TankMechanics.move_tank_body('w', 70, -60)
            TankMechanics.fire()

    def strategy2(self=0):
        TankMechanics.set_nickname('Екатерина')
        if TankMechanics.get_y() >= TankMechanics.right_up_end_of_map:
            TankMechanics.move_tank_body('w', -80)
        elif TankMechanics.get_y() <= TankMechanics.left_down_end_of_map:
            TankMechanics.move_tank_body('w', 80)
        if TankMechanics.get_speed() == 0:
            TankMechanics.move_tank_body('w', 80)
        angle = math.degrees(math.atan((TankMechanics.get_enemy_y() - TankMechanics.get_y())/
                          (TankMechanics.get_enemy_x() - TankMechanics.get_x())))
        #print(TankMechanics.pointing())
        driverByFirstUser.determine_angle(angle)
        TankMechanics.fire()

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
