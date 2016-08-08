
#include <stdio.h>
#include <wiringPiI2C.h>

//int id = 0x40 ;
unsigned char TCN_ADRESS_W=0x77;
unsigned char TCN_ADRESS_R=0x40;
unsigned char TCN_TEMP=0x00;
unsigned char temp1,temp2;
int fd,e;

void read_temperature(void)
{

if((fd=wiringPiI2CSetup(TCN_TEMP))<0)
printf("Error opening i2c channel\n\r");

if((e= wiringPiI2CWrite(fd,TCN_ADRESS_W))<0)
printf("Error writing to slave\n\r");

if((temp1= wiringPiI2CReadReg8 (e,TCN_ADRESS_R))<0)
printf("Error writing to slave\n\r");

temp2= wiringPiI2CReadReg8 (e,TCN_ADRESS_R);
printf("Temperature =%d",temp1);
printf("Temperature =%d",temp2);
}