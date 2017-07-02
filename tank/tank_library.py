from abc import ABCMeta, abstractmethod, abstractproperty


class tank_mechanics(object):
    __metaclass__ = ABCMeta

    left_down_end_of_map = 50
    right_up_end_of_map = 1200

    '''Начальные координаты тела первого танка'''
    tank1_body_position_x_start = 250
    tank1_body_position_y_start = 150

    '''Начальные координаты тела второго танка'''
    tank2_body_position_x_start = 400
    tank2_body_position_y_start = 300

    '''Стрельба'''
    @abstractmethod
    def fire(self = 0):
        pass

    '''Инвертирование направления движения'''
    @abstractmethod
    def invert_moving(self = 0):
        pass

    '''Инвертирование угла поворота корпуса'''
    @abstractmethod
    def invert_body_rotating(self = 0):
        pass

    '''Инвертирование угла поворота пушка'''
    @abstractmethod
    def invert_gun_rotating(self = 0):
        pass

    '''Возвращает True, если последний выпущенный снаряд попал в цель. В противном случае вернет False'''
    @abstractmethod
    def get_boolean_hit_the_tank(self = 0):
        pass

    '''Возвращает True, если танк ещё перезаряжается или False, если танк еще не перезарядился'''
    @abstractmethod
    def get_boolean_recharging(self = 0):
        pass

    '''Возвращает True или False в зависимости, есть ли на вашем танке фокус или нет'''
    @abstractmethod
    def get_boolean_focus_on(self = 0):
        pass

    '''Поворачивает пушку'''
    '''angle - угол поворота(в градусах), строго больше нуля'''
    '''side - выбор направления вращения. rigtht - по часовой, left - против часовой'''
    '''continued. 0 - повторить действие 1 раз. 1 - постоянное повторение'''
    @abstractmethod
    def rotate_gun(angle = 1, side = 'right', continued = 0):
        pass

    '''Сделать угол поворота пушки равным определенному углк'''
    @abstractmethod
    def make_gun_angle(angle = 1):
        pass

    '''Дать имя танку'''
    @abstractmethod
    def set_nickname(nickname = 'Tank'):
        pass

    '''Движение танка'''
    '''key - направление движения.w - движение вперёд,s - движение назад'''
    '''speed - скорость движения'''
    '''rotation - угол кривизны движения'''
    @abstractmethod
    def move_tank_body(key = '', speed = 0, rotation = 0):
        pass

    '''Останавливает движение'''
    '''t - время стоянки(в секундах)'''
    @abstractmethod
    def stop_moving(t = 0):
        pass

    '''Возвращает координату X положения центра собственного танка'''
    @abstractmethod
    def get_x(self = 0):
        pass

    '''Возвращает координату Y положения центра собственного танка'''
    @abstractmethod
    def get_y(self = 0):
        pass

    '''Возвращает угол поворота корпуса'''
    @abstractmethod
    def get_body_angle(self = 0):
        pass

    '''Возвращает угол поворота пушки'''
    @abstractmethod
    def get_gun_angle(self = 0):
        pass

    '''Возвращает здоровье танка'''
    @abstractmethod
    def get_health(self = 0):
        pass

    '''Возвращает скорость танка'''
    @abstractmethod
    def get_speed(self = 0):
        pass

    '''Возвращает координату X положения центра вражеского танка'''
    @abstractmethod
    def get_enemy_x(self = 0):
        pass

    '''Возвращает координату Y положения центра вражеского танка'''
    @abstractmethod
    def get_enemy_y(self = 0):
        pass

    '''Возвращает время последнего выстрела противника'''
    @abstractmethod
    def get_last_enemy_shot_time(self = 0):
        pass



