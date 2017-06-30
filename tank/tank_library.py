from abc import ABCMeta, abstractmethod, abstractproperty


class tank_mechanics(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def rotate_gun(angle=1, side='right', number_of_tank=1):
        pass

    @abstractmethod
    def set_nickname(nickname = 'Tank', number_of_tank=1):
        pass

    @abstractmethod
    def move_tank_body(key="w", speed=0, rotation=0, number_of_tank=1):
        pass

    @abstractmethod
    def get_x(number_of_tank=1):
        pass

    @abstractmethod
    def get_y(number_of_tank=1):
        pass


