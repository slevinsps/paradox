from tank_library import*
from cocos.actions import Driver
class driverBySecondUser(Driver):
    def step(self, dt):
        self.strategy1()

    def move_tank_body(key='', speed=0, rotation=0):
        pass

    def rotate_gun(angle=1, side='right', continued=0):
        pass

    def strategy3(self):
        self.move_tank_body('w', 80)
        self.rotate_gun(1, 'right')

    def strategy1(self=0):
        TankMechanics.set_nickname('Боб')
        if TankMechanics.get_y() >= 300:
            TankMechanics.move_tank_body('w', -40)
            TankMechanics.fire()
        elif TankMechanics.get_y() <= 100:
            TankMechanics.move_tank_body('w', 40)
            # tank_mechanics.rotate_gun(20, 'left')
            # print('2', self)
