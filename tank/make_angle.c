#include <stdio.h>
#include <math.h>

float get_angle(int, int, int, int);

float get_angle(int x1, int y1, int x2, int y2){
    int angle = 360 / M_PI * (atan((y2 - y1) / (x2 - x1)));
    return angle;
}