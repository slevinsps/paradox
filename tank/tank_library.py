class TankMechanics(object):
    """Библиотека для управления танком"""

    '''Крайние значения карты'''
    left_down_end_of_map = 50
    right_up_end_of_map = 1200

    '''Начальные координаты тела первого танка'''
    tank1_body_position_x_start = 250
    tank1_body_position_y_start = 150

    '''Начальные координаты тела второго танка'''
    tank2_body_position_x_start = 400
    tank2_body_position_y_start = 300

    '''Стрельба'''
    @staticmethod
    def fire():
        pass

    '''Автонаведение'''
    @staticmethod
    def pointing():
        pass

    '''Инвертирование направления движения'''
    @staticmethod
    def invert_moving():
        pass

    '''Инвертирование угла поворота корпуса'''
    @staticmethod
    def invert_body_rotating():
        pass

    '''Инвертирование угла поворота пушка'''
    @staticmethod
    def invert_gun_rotating():
        pass

    '''Возвращает True, если последний выпущенный снаряд попал в цель. В противном случае вернет False'''
    @staticmethod
    def get_boolean_hit_the_tank():
        pass

    '''Возвращает True, если танк ещё перезаряжается или False, если танк еще не перезарядился'''
    @staticmethod
    def get_boolean_recharging():
        pass

    '''Возвращает True или False в зависимости, есть ли на вашем танке фокус или нет'''
    @staticmethod
    def get_boolean_focus_on():
        pass

    '''Поворачивает пушку'''
    '''angle - угол поворота(в градусах), строго больше нуля'''
    '''side - выбор направления вращения. rigtht - по часовой, left - против часовой'''
    '''continued. 0 - повторить действие 1 раз. 1 - постоянное повторение'''
    @staticmethod
    def rotate_gun(angle=1, side='right', continued=0):
        pass

    '''Сделать угол поворота пушки равным определенному углк'''
    @staticmethod
    def make_gun_angle(angle=1):
        pass

    '''Дать имя танку'''
    @staticmethod
    def set_nickname(nickname='Tank'):
        pass

    '''Движение танка'''
    '''key - направление движения.w - движение вперёд,s - движение назад'''
    '''speed - скорость движения'''
    '''rotation - угол кривизны движения'''
    @staticmethod
    def move_tank_body(key='', speed=0, rotation=0):
        pass

    '''Останавливает движение'''
    '''t - время стоянки(в секундах)'''
    @staticmethod
    def stop_moving(t=0):
        pass

    '''Возвращает координату X положения центра собственного танка'''
    @staticmethod
    def get_x():
        pass

    '''Возвращает координату Y положения центра собственного танка'''
    @staticmethod
    def get_y():
        pass

    '''Возвращает угол поворота корпуса'''
    @staticmethod
    def get_body_angle():
        pass

    '''Возвращает угол поворота пушки'''
    @staticmethod
    def get_gun_angle():
        pass

    '''Возвращает здоровье танка'''
    @staticmethod
    def get_health():
        pass

    '''Возвращает скорость танка'''
    @staticmethod
    def get_speed():
        pass

    '''Возвращает координату X положения центра вражеского танка'''
    @staticmethod
    def get_enemy_x():
        pass

    '''Возвращает координату Y положения центра вражеского танка'''
    @staticmethod
    def get_enemy_y():
        pass

    '''Возвращает время последнего выстрела противника'''
    @staticmethod
    def get_last_enemy_shot_time():
        pass



