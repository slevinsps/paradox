from tank_library import*
from cocos.actions import Driver
class driverBySecondUser(Driver):
    def step(self, dt):
        tank_mechanics.set_nickname('Боб')
        if tank_mechanics.get_y() >= 300:
            tank_mechanics.move_tank_body('w', -40)
            tank_mechanics.fire()
        elif tank_mechanics.get_y() <= 100:
            tank_mechanics.move_tank_body('w', 40)
        #tank_mechanics.rotate_gun(20, 'left')
        #print('2', self)