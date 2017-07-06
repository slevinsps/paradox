
def strategy1(self):
    self.set_nickname('Анастасия')
    if (self.get_boolean_recharging() == False):
        self.stop_moving(0.3)
        self.rotate_gun(15, 'right', 1)
    else:
        self.move_tank_body('w', 70, -60)
        self.fire()


def strategy3(self):
    self.move_tank_body('w', 80)
    self.rotate_gun(1, 'right')

#name = 'Анастасия' 1.0

#name = 'Екатерина' 2.0

name = 'Елизавета' #3.0
#model = 'light' #3.0

def strategy(functions):
    #print(functions.get_x(), functions.get_y())

    if functions.get_y() <= 100:
        if functions.get_x() > 200 and functions.get_x() < 800 :
            functions.move_tank_body('w', 80)
        elif functions.get_x() < 100:
            functions.move_tank_body('w', 50, 20)
        elif functions.get_x() > 900:
            functions.move_tank_body('w', 50, -20)
    elif functions.get_y() >= 1000:
        if functions.get_x() > 200:
            functions.move_tank_body('s', 80)
        elif functions.get_x() < 100:
            functions.move_tank_body('s', 50, -20)
        elif functions.get_x() > 900:
            functions.move_tank_body('s', 50, 20)

    if functions.get_speed() == 0:
        functions.move_tank_body('w', 80, 80)
    functions.make_gun_angle(functions.determine_angle())
    functions.fire()