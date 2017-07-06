def strategy3(self):
    self.move_tank_body('w', 80)
    self.rotate_gun(1, 'right')

name = 'Боб'
model = 'heavy'


def strategy(self):
    smart_angle = 0
    if self.get_x() > self.RIGHT_END_OF_MAP - 10 or self.get_x() < self.LEFT_DOWN_END_OF_MAP + 10 or (
                self.get_y() < self.LEFT_DOWN_END_OF_MAP + 10 or self.get_y() > self.UP_END_OF_MAP - 10 ):
        self.invert_moving()
    if self.get_distance_between_tanks() < 300:
        self.stop_moving(0.2)
    if self.get_enemy_y() > self.get_y() and self.get_enemy_x() > self.get_x():
        if self.get_body_angle() != 90:
            self.move_tank_body('w',80,90)
        else:
            self.move_tank_body('s', 30)
        smart_angle = self.get_distance_between_tanks()/100
    elif self.get_enemy_y() > self.get_y() and self.get_enemy_x() < self.get_x():
        if self.get_body_angle() != -90 :
            self.move_tank_body('s',80,-90)
        else:
            self.move_tank_body('w', 30)
        smart_angle = - self.get_distance_between_tanks() / 100
    elif self.get_enemy_y() < self.get_y() and self.get_enemy_x() < self.get_x():
            self.move_tank_body('w',200,-90)
    elif self.get_enemy_y() < self.get_y() and self.get_enemy_x() > self.get_x():
            self.move_tank_body('w',200, 90)
    self.make_gun_angle(self.determine_angle() + smart_angle)
    self.fire()