from tank_library import*
from cocos.actions import Driver
class driverByFirstUser(Driver):
    def step(self, dt):
        tank_mechanics.move_tank_body('w', 70, -60, 1)
        tank_mechanics.rotate_gun(90,'right',1)