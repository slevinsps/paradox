import pytest
import main
from math import*
import os
import pyglet
import time


def test_manage_side1():
    tank_body = main.TankBodyDriver()
    res = tank_body.manage_side(1, 1, 1, 0)
    assert(1 == res)

def test_manage_side2():
    tank_body = main.TankBodyDriver()
    res = tank_body.manage_side(0, 0, 1, 0)
    assert(0 == res)

def test_get_boolean_hit_the_tank_1():
    main.is_hitted1 = 1
    get = main.TankLibraryInitialize.get_boolean_hit_the_tank()
    assert(get == 1)

def test_get_boolean_hit_the_tank_2():
    main.is_hitted2 = 2
    get = main.TankLibraryInitialize.get_boolean_hit_the_tank()
    assert(get == 2)

def test_get_boolean_recharging_0_1():
    main.is_recharging1 = 2
    get = main.TankLibraryInitialize.get_boolean_recharging()
    assert(get == True)

def test_get_boolean_recharging_1_1():
    main.is_recharging1 = 0
    get = main.TankLibraryInitialize.get_boolean_recharging()
    assert(get == False)

def test_get_boolean_recharging_0_2():
    main.is_recharging2 = 2
    get = main.TankLibraryInitialize.get_boolean_recharging()
    assert(get == True)

def test_get_boolean_recharging_2_2():
    main.is_recharging2 = 0
    get = main.TankLibraryInitialize.get_boolean_recharging()
    assert(get == False)

def test_stop_moving_1():
    main.TankLibraryInitialize.stop_moving(5)
    get = main.stop_time1
    t = time.clock() + 5
    assert (abs(get - t) < 1e-4)

def test_stop_moving_2():
    main.TankLibraryInitialize.stop_moving(0)
    get = main.stop_time2
    t = time.clock()
    assert (abs(get - t) < 1e-4)

def test_get_boolean_focus_on1():
    main.focus_on = 1
    get = main.TankLibraryInitialize.get_boolean_focus_on()
    assert ( get == True)

def test_get_boolean_focus_on2():
    main.focus_on = 1
    get = main.TankLibraryInitialize.get_boolean_focus_on()
    assert ( get == False)
    
def test_invert_moving1():
    main.invert_moving1 = 1
    main.TankLibraryInitialize.invert_moving()
    get = main.invert_moving1
    assert(get == -1)

def test_invert_moving2():
    main.invert_moving2 = -1
    main.TankLibraryInitialize.invert_moving()
    get = main.invert_moving2
    assert(get == 1)

def test_invert_body_rotating1():
    main.invert_body_rotate1 = 1
    main.TankLibraryInitialize.invert_body_rotating()
    get = main.invert_body_rotate1
    assert(get == -1)

def test_invert_body_rotating2():
    main.invert_body_rotate2 = -1
    main.TankLibraryInitialize.invert_body_rotating()
    get = main.invert_body_rotate2
    assert(get == 1)
    
def test_invert_gun_rotating1():
    main.invert_gun_rotate1 = 1
    main.TankLibraryInitialize.invert_gun_rotating()
    get = main.invert_gun_rotate1
    assert(get == -1)

def test_invert_gun_rotating2():
    main.invert_gun_rotate2 = -1
    main.TankLibraryInitialize.invert_gun_rotating()
    get = main.invert_gun_rotate2
    assert(get == 1)
    
def test_get_body_angle1():
    main.tank1_body_rotation = 1
    get = main.TankLibraryInitialize.get_body_angle()
    assert(get == 1)

def test_get_body_angle2():
    main.tank2_body_rotation = 1
    get = main.TankLibraryInitialize.get_body_angle()
    assert(get == 1)

def test_get_gun_angle1():
    main.tank1_gun_rotation = 1
    get = main.TankLibraryInitialize.get_gun_angle()
    assert(get == 1)

def test_get_gun_angle2():
    main.tank2_gun_rotation = 1
    get = main.TankLibraryInitialize.get_body_angle()
    assert(get == 1)
    

def test_get_health1():
    main.tank1_health = 1
    get = main.TankLibraryInitialize.get_health()
    assert(get == 1)

def test_get_health2():
    main.tank2_health = 1
    get = main.TankLibraryInitialize.get_health()
    assert(get == 1)    


def test_get_speed1():
    main.tank1_speed = 1
    get = main.TankLibraryInitialize.get_speed()
    assert(get == 1)

def test_get_speed2():
    main.tank2_speed = 1
    get = main.TankLibraryInitialize.get_speed()
    assert(get == 1)
    

def test_enemy_x1():
    main.tank2_body_position_x = 1
    get = main.TankLibraryInitialize.get_enemy_x()
    assert(get == 1)

def test_enemy_x2():
    main.tank1_body_position_x = 1
    get = main.TankLibraryInitialize.get_enemy_x()
    assert(get == 1)

def test_enemy_y1():
    main.tank2_body_position_y = 1
    get = main.TankLibraryInitialize.get_enemy_y()
    assert(get == 1)

def test_enemy_y2():
    main.tank1_body_position_y = 1
    get = main.TankLibraryInitialize.get_enemy_y()
    assert(get == 1)
  
def test_get_distance_between_tanks():
    main.tank1_body_position_x = 100
    main.tank1_body_position_y = 100
    main.tank2_body_position_x = 200
    main.tank2_body_position_y = 200

    test_dist = sqrt(20000)

    get_distance = main.TankLibraryInitialize.get_distance_between_tanks()

    assert(abs(get_distance - test_dist) < 1e-6)

def test_get_x_1():
    main.tank1_body_position_x = 1
    get = main.TankLibraryInitialize.get_x()
    
    assert (get == 1)

def test_get_x_2():
    main.tank2_body_position_x = 1
    get = main.TankLibraryInitialize.get_x()
    
    assert (get == 1)

def test_get_y_1():
    main.tank1_body_position_y = 1
    get = main.TankLibraryInitialize.get_y()
    
    assert (get == 1)

def test_get_y_2():
    main.tank2_body_position_y = 1
    get = main.TankLibraryInitialize.get_y()

    assert (get == 1)

def test_get_last_enemy_shot_time1():
    main.last_tank2_shot_time = 2
    get = main.TankLibraryInitialize.get_last_enemy_shot_time()

    assert(get == 2)

def test_get_last_enemy_shot_time2():
    main.last_tank1_shot_time = 2
    get = main.TankLibraryInitialize.get_last_enemy_shot_time()

    assert(get == 2)    

def test_move_tank_body_1():
    main.stop_time1 = 0
    main.stop_time2 = 0

    main.move_tank_body_1_code = 'qwe'

    main.TankLibraryInitialize.move_tank_body('w', 0,0)

    assert ( main.move_tank_body_1_code == 'w00pytest_pyfunc_call')

def test_move_tank_body_2():
    main.stop_time1 = 0
    main.stop_time2 = 0

    main.move_tank_body_2_code = 'qwe'

    main.TankLibraryInitialize.move_tank_body('w', 0,0)

    assert ( main.move_tank_body_2_code == 'w00pytest_pyfunc_call')
    
def test_determine_angle_1():
    main.tank1_body_position_x = 30
    main.tank1_body_position_y = 30
    main.tank2_body_position_x = 60
    main.tank2_body_position_y = 60

    
    angle = main.TankLibraryInitialize.determine_angle()
    curr_angle = 45
    assert(abs(angle - curr_angle) < 1e-6)


def test_determine_angle_2():
    main.tank1_body_position_x = 30
    main.tank1_body_position_y = 30
    main.tank2_body_position_x = 60
    main.tank2_body_position_y = 60

    
    angle = main.TankLibraryInitialize.determine_angle()
    curr_angle = -135
    assert(abs(angle - curr_angle) < 1e-6)

def test_help_to_determinate_angle1():
    angle = main.TankLibraryInitialize.help_to_determine_angle(30, 30, 60, 60)
    curr_angle = 45
    assert (abs(angle - curr_angle) < 1e-6)

def test_help_to_determinate_angle2():
    angle = main.TankLibraryInitialize.help_to_determine_angle(60, 30, 30, 60)
    curr_angle = -45
    assert (abs(angle - curr_angle) < 1e-6)

def test_help_to_determinate_angle3():
    angle = main.TankLibraryInitialize.help_to_determine_angle(60, 30, 30, 60)
    curr_angle = -45
    assert (abs(angle - curr_angle) < 1e-6)

def test_help_to_determinate_angle4():
    angle = main.TankLibraryInitialize.help_to_determine_angle(30, 60, 60, 30)
    curr_angle = 135
    assert (abs(angle - curr_angle) < 1e-6)

def test_help_to_determinate_angle5():
    angle = main.TankLibraryInitialize.help_to_determine_angle(30, 60, 30, 30)
    curr_angle = 180
    assert (abs(angle - curr_angle) < 1e-6)

def test_help_to_determinate_angle6():
    angle = main.TankLibraryInitialize.help_to_determine_angle(30, 30, 60, 30)
    curr_angle = 90
    assert (abs(angle - curr_angle) < 1e-6)

def test_help_to_determinate_angle7():
    angle = main.TankLibraryInitialize.help_to_determine_angle(30, 30, 30, 60)
    curr_angle = 0
    assert (abs(angle - curr_angle) < 1e-6)

def test_help_to_determinate_angle8():
    angle = main.TankLibraryInitialize.help_to_determine_angle(60, 30, 30, 30)
    curr_angle = -90
    assert (abs(angle - curr_angle) < 1e-6)

def test_rotate_gun_1():
    main.rotate_gun_1_code = 'qwe'

    main.TankLibraryInitialize.rotate_gun(40, 'left',0)

    assert ( main.rotate_gun_1_code == '40leftpytest_pyfunc_call')

def test_rotate_gun_2():
    main.rotate_gun_2_code = 'qwe'

    main.TankLibraryInitialize.rotate_gun(40, 'left',0)

    assert ( main.rotate_gun_2_code == '40leftpytest_pyfunc_call')

def test_determine_the_number1():
    def FirstTankClass():
        return main.TankLibraryInitialize.determine_the_number()

    get = FirstTankClass()
    assert (get == 1)

def test_determine_the_number2():
    def SecondTankClass():
        return main.TankLibraryInitialize.determine_the_number()

    get = SecondTankClass()
    assert (get == 2)

    
