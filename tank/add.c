#include <stdio.h>
#include <math.h>

float get_angle(float, float,float, float);
//float get_angle(int, int,int, int);

float get_angle(float enemy_y, float y,float enemy_x, float x){
	float angle = atan((enemy_y - y)/(enemy_x - x));
    if ((enemy_x - x > 0) && (enemy_y - y > 0))
            angle = 90 - angle;
    if ((enemy_x - x < 0) && (enemy_y - y > 0))
            angle = -angle - 90;
    if ((enemy_x - x < 0) && (enemy_y - y < 0))
            angle = - angle + 270;
    if ((enemy_x - x > 0) && (enemy_y - y < 0))
            angle = -angle + 90;
    if ((enemy_x - x == 0) && (enemy_y - y < 0))
            angle = 180;
    if ((enemy_x - x == 0) && (enemy_y - y > 0))
            angle = 0;
    if ((enemy_x - x > 0) && (enemy_y - y == 0))
            angle = 0;
	printf("%f",angle);
    return angle;
}
//float get_angle(int enemy_y, int y,int enemy_x, int x){
//	float angle = atan((enemy_y - y)/(enemy_x - x))*180/3.16;
//    if ((enemy_x - x > 0) || (enemy_y - y > 0))
//            angle = 90 - angle;
//    if ((enemy_x - x < 0) || (enemy_y - y > 0))
//            angle = -angle - 90;
//    if ((enemy_x - x < 0) || (enemy_y - y < 0))
//            angle = - angle + 270;
//    if ((enemy_x - x > 0) || (enemy_y - y < 0))
//            angle = -angle + 90;
//    if ((enemy_x - x == 0) || (enemy_y - y < 0))
//            angle = 180;
//    if ((enemy_x - x == 0) || (enemy_y - y > 0))
//            angle = 0;
//    if ((enemy_x - x > 0) || (enemy_y - y == 0))
//            angle = 0;
//    return angle;
//}