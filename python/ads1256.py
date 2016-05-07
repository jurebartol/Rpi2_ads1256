"""
	Author: Jure Bartol
	Date:   16/04/2016

	TO-DO:
	- (optional)live plotting
	- acquisition.py: 
		- use pickle instead of write
		- ConfigureFile() -> convert every value to volt
		-(DONE) write time to file too
	- ads1256.py:
		- Add comments + organize
	- gui
"""

from _bcm2835 import *

AD30000SPS = 0
AD15000SPS = 1
AD7500SPS = 2
AD3750SPS = 3
AD2000SPS = 4
AD1000SPS = 5
AD500SPS = 6
AD100SPS = 7
AD60SPS = 8
AD50SPS = 9
AD30SPS = 10
AD25SPS = 11
AD15SPS = 12
AD10SPS = 13
AD5SPS = 14
AD2d5SPS = 15
DRATE_MAX = 16

GAIN_1 = 0 
GAIN_2 = 1
GAIN_4 = 2
GAIN_6 = 3
GAIN_16 = 4
GAIN_32 = 5
GAIN_64 = 6

#/*Register address, followed by reset the default values */
REG_STATUS = 0	 #// x1H
REG_MUX    = 1  #// 01H
REG_ADCON  = 2  #// 20H
REG_DRATE  = 3  #// F0H
REG_IO     = 4  #// E0H
REG_OFC0   = 5  #// xxH
REG_OFC1   = 6  #// xxH
REG_OFC2   = 7  #// xxH
REG_FSC0   = 8  #// xxH
REG_FSC1   = 9  #// xxH
REG_FSC2   = 10 #// xxH

CMD_WAKEUP  = 0x00	#// Completes SYNC and Exits Standby Mode 0000  0000 (00h)
CMD_RDATA   = 0x01 #// Read Data 0000  0001 (01h)
CMD_RDATAC  = 0x03 #// Read Data Continuously 0000   0011 (03h)
CMD_SDATAC  = 0x0F #// Stop Read Data Continuously 0000   1111 (0Fh)
CMD_RREG    = 0x10 #// Read from REG rrr 0001 rrrr (1xh)
CMD_WREG    = 0x50 #// Write to REG rrr 0101 rrrr (5xh)
CMD_SELFCAL = 0xF0 #// Offset and Gain Self-Calibration 1111    0000 (F0h)
CMD_SELFOCAL= 0xF1 #// Offset Self-Calibration 1111    0001 (F1h)
CMD_SELFGCAL= 0xF2 #// Gain Self-Calibration 1111    0010 (F2h)
CMD_SYSOCAL = 0xF3 #// System Offset Calibration 1111   0011 (F3h)
CMD_SYSGCAL = 0xF4 #// System Gain Calibration 1111    0100 (F4h)
CMD_SYNC    = 0xFC #// Synchronize the A/D Conversion 1111   1100 (FCh)
CMD_STANDBY = 0xFD #// Begin Standby Mode 1111   1101 (FDh)
CMD_RESET   = 0xFE #// Reset to Power-Up Values 1111   1110 (FEh)

DRDY  = RPI_GPIO_P1_11 # = 17 P0
RST   = RPI_GPIO_P1_12 #  = 18 P1
SPICS = RPI_GPIO_P1_15 #= 22 P3

def CS_1():
	return bcm2835_gpio_write(SPICS, HIGH)
def CS_0():
	return bcm2835_gpio_write(SPICS, LOW)

def SetChannel(ch):
	if ch > 7:
		return
	WriteReg(REG_MUX, (ch << 4) | (1 << 3))
	
def WriteReg(RegID, RegValue):
	CS_0()
	Send8Bit(CMD_WREG | RegID)
	Send8Bit(0x00)
	Send8Bit(RegValue)
	CS_1()
	
def Send8Bit(data):
	bsp_delayUS(2)
	bcm2835_spi_transfer(data)
	
def bsp_delayUS(micros):
	bcm2835_delayMicroseconds(micros)
	
def ReadData():
	CS_0()
	Send8Bit(CMD_RDATA)	
	buf1 = Recieve8Bit()
	buf2 = Recieve8Bit()
	buf3 = Recieve8Bit()
	read = buf1 << 16 & 0x00FF0000
	read |= buf2 << 8
	read |= buf3
	CS_1()
	return read

def Recieve8Bit():
	return bcm2835_spi_transfer(0xff)

def delayDATA():
	bsp_delayUS(10)
	
def CfgADC(gain, data_rate):
	s_tabDataRate = (0xF0, 0xE0, 0xD0, 0xC0, 0xB0, 0xA1, 0x92, 0x82, 0x72, 0x63, 
	0x53, 0x43, 0x33, 0x20, 0x13, 0x03)
	buf1 = ((0 << 3) | (1 << 2) | (0 << 1))
	buf2 = 0x08
	buf3 = ((0 << 5) | (0 << 3) | (gain << 0))
	buf4 = s_tabDataRate[data_rate]
	CS_0()
	Send8Bit(CMD_WREG | 0)
	Send8Bit(0x03)
	Send8Bit(buf1)
	Send8Bit(buf2)
	Send8Bit(buf3)
	Send8Bit(buf4)
	CS_1()
	bsp_delayUS(50)
	
def ADInitialize():
	bcm2835_init()
	bcm2835_spi_begin()
	bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_LSBFIRST)
	bcm2835_spi_setDataMode(BCM2835_SPI_MODE1)
	bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_32)
	bcm2835_gpio_fsel(SPICS, BCM2835_GPIO_FSEL_OUTP)
	bcm2835_gpio_write(SPICS, HIGH)
	bcm2835_gpio_fsel(DRDY, BCM2835_GPIO_FSEL_INPT)
	bcm2835_gpio_set_pud(DRDY, BCM2835_GPIO_PUD_UP)
	CfgADC(GAIN_1, AD30000SPS)
	
def ADEnd():
	bcm2835_spi_end()
	bcm2835_close()	
