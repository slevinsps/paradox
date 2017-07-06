def strategy3(self):
    self.move_tank_body('w', 80)
    self.rotate_gun(1, 'right')

name = 'Боб'
#model = 'heavy' #3.0

def strategy(self):
    smart_angle = 0
    if self.get_distance_between_tanks() < 300:
        self.stop_moving(0.2)
    elif self.get_enemy_y() > self.get_y():
        self.move_tank_body('w',80)
        smart_angle = self.get_distance_between_tanks()/100
    else:
        self.move_tank_body('s', 80)
        smart_angle = - self.get_distance_between_tanks() / 100
    self.make_gun_angle(self.determine_angle() + smart_angle)
    self.fire()