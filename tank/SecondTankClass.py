from tank_library import*
from cocos.actions import Driver
class driverBySecondUser(Driver):
    def step(self, dt):
        if tank_mechanics.get_y(2) >= 300:
            tank_mechanics.move_tank_body('w', -40, 10, 2)
        elif tank_mechanics.get_y(2) <= 100:
            tank_mechanics.move_tank_body('w', 40, 0, 2)
        tank_mechanics.rotate_gun(20, 'left', 2)
