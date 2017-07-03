from tank_library import*
from cocos.actions import Driver
class driverByFirstUser(Driver):
    def step(self, dt):
        tank_mechanics.set_nickname('Анастасия', 1)
        tank_mechanics.move_tank_body('', 70, 0, 1)
        tank_mechanics.rotate_gun(90,'right',1)