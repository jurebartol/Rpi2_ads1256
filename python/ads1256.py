"""
	Author: Jure Bartol
	Date:   16/04/2016
"""

from _bcm2835 import *

AD30000SPS = 0xF0
AD15000SPS = 0xF0
AD7500SPS  = 0xD0
AD3750SPS  = 0xC0
AD2000SPS  = 0xB0
AD1000SPS  = 0xA1
AD500SPS   = 0x92
AD100SPS   = 0x82
AD60SPS    = 0x72
AD50SPS    = 0x63
AD30SPS    = 0x53
AD25SPS    = 0x43
AD15SPS    = 0x33
AD10SPS    = 0x20
AD5SPS     = 0x13
AD2d5SPS   = 0x03

GAIN_1 = 0 
GAIN_2 = 1
GAIN_4 = 2
GAIN_6 = 3
GAIN_16 = 4
GAIN_32 = 5
GAIN_64 = 6

REG_STATUS = 0
REG_MUX    = 1
REG_ADCON  = 2
REG_DRATE  = 3
REG_IO     = 4
REG_OFC0   = 5
REG_OFC1   = 6
REG_OFC2   = 7
REG_FSC0   = 8
REG_FSC1   = 9
REG_FSC2   = 10

CMD_WAKEUP  = 0x00
CMD_RDATA   = 0x01
CMD_RDATAC  = 0x03
CMD_SDATAC  = 0x0F
CMD_RREG    = 0x10
CMD_WREG    = 0x50
CMD_SELFCAL = 0xF0
CMD_SELFOCAL= 0xF1
CMD_SELFGCAL= 0xF2
CMD_SYSOCAL = 0xF3
CMD_SYSGCAL = 0xF4
CMD_SYNC    = 0xFC
CMD_STANDBY = 0xFD
CMD_RESET   = 0xFE

DRDY  = RPI_GPIO_P1_11
RST   = RPI_GPIO_P1_12
SPICS = RPI_GPIO_P1_15

def CS_1():
	bcm2835_gpio_write(SPICS, HIGH)
def CS_0():
	bcm2835_gpio_write(SPICS, LOW)

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
	buf1 = ((0 << 3) | (1 << 2) | (0 << 1))
	buf2 = 0x08
	buf3 = ((0 << 5) | (0 << 3) | (gain << 0))
	buf4 = data_rate
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
	bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_256)
	bcm2835_gpio_fsel(SPICS, BCM2835_GPIO_FSEL_OUTP)
	bcm2835_gpio_write(SPICS, HIGH)
	bcm2835_gpio_fsel(DRDY, BCM2835_GPIO_FSEL_INPT)
	bcm2835_gpio_set_pud(DRDY, BCM2835_GPIO_PUD_UP)
	CfgADC(GAIN_1, AD30000SPS)
	
def ADEnd():
	bcm2835_spi_end()
	bcm2835_close()	
