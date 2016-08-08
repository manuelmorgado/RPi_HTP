#include <stdio.h>
#include <wiringPiI2C.h>

int fd ;
int main (void)
{

fd = wiringPiI2CSetup(0x00);
printf( "hola","%d \n",fd);

wiringPiI2CReadReg8(fd, 0x22) ;
wiringPiI2CReadReg8(fd, 0x40) ;
float e = wiringPiI2CReadReg8(fd, 0x40) ;
printf( "%d \n",fd,e);

}
