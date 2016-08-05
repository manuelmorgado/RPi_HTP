// Blink test for Raspberry Pi B, using the port 15(wiringPi) or GPIO14 in the board.
// Connect to the General Purpose I/O (port IO14) the correct resistors and then one LED
// and finally to the GND. (C++ version)
// Date: 28/07/2016

//Importing libraries.
#include <stdio.h>
#include <wiringPi.h>
 
int main (void)
{
  printf ("Raspberry Pi blink test.\n") ;
 
  if (wiringPiSetup () == -1)
    return 1 ;
 
  pinMode (15, OUTPUT) ;            // AKA: BCM_GPIO pin 14 in the RPi board (15 for Raspberry).
 
  for (;;)
  {
    digitalWrite (15, 1) ;          // Turning in the LED.
    delay (500) ;                   // Waiting 500 mS.
    digitalWrite (15, 0) ;          // Turning off the LED.
    delay (500) ;
  }
  return 0 ;
}