/*
	Author: Jure Bartol
	Date: 07.05.2016

-> Rpi2_ads1256
	-> C
		-> RPi_AD.h
		-> RPi_AD.c
		-> exampleMain.c
		-> makefile.make
		-> src
			-> enum.c
			-> enum.h
			-> spi.c
			-> spi.h
			-> ads1256.c
			-> ads1256.h
*/

#ifndef ADS1256_H_INCLUDED
#define ADS1256_H_INCLUDED

#include <stdio.h>

/*	*******************************
	** PART 1 - serial interface **
	*******************************
	Functions:
		- CS_1()
		- CS_0()
		- RST_1()
		- RST_0()
		- DRDY_LOW()
		- delayus()
		- send8bit()
		- recieve8bit()
		- waitDRDY()
		- initializeSPI()
		- endSPI()
*/

void    delayus(uint64_t microseconds);
void    send8bit(uint8_t data);
uint8_t recieve8bit(void);
void    waitDRDY(void);
uint8_t initializeSPI();
void    endSPI();


/*	*****************************
	** PART 2 - ads1256 driver **
	*****************************
	Functions:
		- readByteFromReg()
		- writeByteToReg()
		- writeCMD()
		- readChipID()
		- setSEChannel()
		- setDIFFChannel()
		- setPGA()
		- setDataRate()
		- readData()
		- getValSEChannel()
		- getValDIFFChannel()
		- scanSEChannels()
		- scanDIFFChannels()
		- scanSEChannelsContinuous()
		- scanDIFFChannelsContinuous()
*/

uint8_t readByteFromReg(uint8_t registerID);
void    writeByteToReg(uint8_t registerID, uint8_t value);
uint8_t writeCMD(uint8_t command);
uint8_t setBuffer(bool val);
uint8_t readChipID(void);
void    setSEChannel(uint8_t channel);
void    setDIFFChannel(uint8_t positiveCh, uint8_t negativeCh);
void    setPGA(uint8_t pga);
void    setDataRate(uint8_t drate);
int32_t readData(void);
int32_t getValSEChannel(uint8_t channel);
int32_t getValDIFFChannel(uint8_t positiveCh, uint8_t negativeCh);
void    scanSEChannels(uint8_t channels[], uint8_t numOfChannels, uint32_t *values);
void    scanDIFFChannels(uint8_t positiveChs[], uint8_t negativeChs[], uint8_t numOfChannels, uint32_t *values);
void    scanSEChannelContinuous(uint8_t channel, uint32_t numOfMeasure, uint32_t *values);
void    scanDIFFChannelContinuous(uint8_t positiveCh, uint8_t negativeCh, uint32_t numOfMeasure, uint32_t *values);


/*	********************************************
	** PART 3 - "high-level" data acquisition **
	********************************************
	Functions:
		- writeToFile()
		- getValsMultiChSE()
		- getValsMultiChDIFF()
		- getValsSingleChSE()
		- getValsSingleChDIFF()

*/

void writeValsToFile(FILE *file, uint32_t *values[], uint8_t numOfValues, uint8_t numOfChannels, char *pathWithFileName[]);
void getValsMultiChSE(uint32_t numOfMeasure, uint32_t *values[], uint8_t *channels[], uint8_t numOfChannels, bool flushToFile, char *path[]);
void getValsSingleChSE(uint32_t numOfMeasure, uint32_t *values[], uint8_t channel, bool flushToFile, char *path[]);
void getValsSingleChDIFF(uint32_t numOfMeasure, uint32_t **values, uint8_t posCh, uint8_t negCh, uint8_t numOfChannels, bool flushToFile);


#endif



