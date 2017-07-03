from tank_library import*
from cocos.actions import Driver
class driverBySecondUser(Driver):
    def step(self, dt):
        TankMechanics.set_nickname('Боб')
        if TankMechanics.get_y() >= 300:
            TankMechanics.move_tank_body('w', 0)
            TankMechanics.fire()
        elif TankMechanics.get_y() <= 100:
            TankMechanics.move_tank_body('w', 0)
        #tank_mechanics.rotate_gun(20, 'left')
        #print('2', self)