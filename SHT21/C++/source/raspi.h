#ifndef RASPI_H
#define RASPI_H

//=== Includes =====================================================================================	

#include "std_c.h"

//=== Global function prototypes ===================================================================

int GetRaspberryHwRevision(void);
void DelayMs(uint32 ms);
void DelayUs(uint32 us);

#endif
