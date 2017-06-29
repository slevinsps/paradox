from tank_library import*
from cocos.actions import Driver
class driverBySecondUser(Driver):
    def step(self, dt):
        tank_mechanics.move_tank_body('w', 20, 20, 2)
        tank_mechanics.rotate_gun(20, 'left', 2)