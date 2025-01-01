#driver for Sainsmart 1.8" ST7735 display ST7735
#Translated by Guy Carver from the ST7735 sample code.
#Modirfied for micropython-esp32 by boochow 

import machine
from machine import SPI, Pin
import time

#ST7735Rotations and ST7735RGB are bits to set
# on MADCTL to control display rotation/color layout
#Looking at display with pins on top.
#00 = upper left printing right
#10 = does nothing (MADCTL_ML)
#20 = upper left printing down (backwards) (Vertical flip)
#40 = upper right printing left (backwards) (X Flip)
#80 = lower left printing right (backwards) (Y Flip)
#04 = (MADCTL_MH)

#60 = 90 right rotation
#C0 = 180 right rotation
#A0 = 270 right rotation
ST7735Rotations = [0x00, 0x60, 0xC0, 0xA0]
ST7735BGR = 0x08 #When set color is bgr else rgb.
ST7735RGB = 0x00

ScreenSize = (128, 160)


class ST7735(object) :
    """Sainsmart TFT 7735 display driver."""

    NOP = 0x0
    SWRESET = 0x01
    RDDID = 0x04
    RDDST = 0x09

    SLPIN  = 0x10
    SLPOUT  = 0x11
    PTLON  = 0x12
    NORON  = 0x13

    INVOFF = 0x20
    INVON = 0x21
    DISPOFF = 0x28
    DISPON = 0x29
    CASET = 0x2A
    RASET = 0x2B
    RAMWR = 0x2C
    RAMRD = 0x2E

    VSCRDEF = 0x33
    VSCSAD = 0x37

    COLMOD = 0x3A
    MADCTL = 0x36

    FRMCTR1 = 0xB1
    FRMCTR2 = 0xB2
    FRMCTR3 = 0xB3
    INVCTR = 0xB4
    DISSET5 = 0xB6

    PWCTR1 = 0xC0
    PWCTR2 = 0xC1
    PWCTR3 = 0xC2
    PWCTR4 = 0xC3
    PWCTR5 = 0xC4
    VMCTR1 = 0xC5

    RDID1 = 0xDA
    RDID2 = 0xDB
    RDID3 = 0xDC
    RDID4 = 0xDD

    PWCTR6 = 0xFC

    GMCTRP1 = 0xE0
    GMCTRN1 = 0xE17

    BLACK = 0

    def __init__( self, spi, aDC, aReset, aCS) :
        """aLoc SPI pin location is either 1 for 'X' or 2 for 'Y'.
            aDC is the DC pin and aReset is the reset pin."""
        self._size = ScreenSize
        self._offset = bytearray([0,0])
        self.rotate = 0                    #Vertical with top toward pins.
        self._rgb = True                   #color order of rgb.
        self.tfa = 0                       #top fixed area
        self.bfa = 0                       #bottom fixed area
        self.dc  = machine.Pin(aDC, machine.Pin.OUT, machine.Pin.PULL_DOWN)
        self.reset = machine.Pin(aReset, machine.Pin.OUT, machine.Pin.PULL_DOWN)
        self.cs = machine.Pin(aCS, machine.Pin.OUT, machine.Pin.PULL_DOWN)
        self.cs(1)
        self.spi = spi
        self.colorData = bytearray(2)
        self.windowLocData = bytearray(4)

        #FOR WINDOW
        self._bits = 0
        self._bytes = 0

        self._buffer = None
        self._windowBuffer = None

        self._columns = 0
        self._rows = 0

        self._windowColumnStart = 0
        self._windowColumnEnd = 0
        self._windowRowStart = 0
        self._windowRowEnd = 0
        self._windowColumns = 0
        self._windowRows = 0

        self._init()
        self._setMADCTL()

    def _init(self) :
        '''Initialize a red tab version.'''
        self._reset()

        self._writecommand(ST7735.SWRESET)              #Software reset.
        time.sleep_us(150)
        self._writecommand(ST7735.SLPOUT)               #out of sleep mode.
        time.sleep_us(500)

        data3 = bytearray([0x01, 0x2C, 0x2D])       #fastest refresh, 6 lines front, 3 lines back.
        self._writecommand(ST7735.FRMCTR1)              #Frame rate control.
        self._writedata(data3)

        self._writecommand(ST7735.FRMCTR2)              #Frame rate control.
        self._writedata(data3)

        data6 = bytearray([0x01, 0x2c, 0x2d, 0x01, 0x2c, 0x2d])
        self._writecommand(ST7735.FRMCTR3)              #Frame rate control.
        self._writedata(data6)
        time.sleep_us(10)

        data1 = bytearray(1)
        self._writecommand(ST7735.INVCTR)               #Display inversion control
        data1[0] = 0x07                             #Line inversion.
        self._writedata(data1)

        self._writecommand(ST7735.PWCTR1)               #Power control
        data3[0] = 0xA2
        data3[1] = 0x02
        data3[2] = 0x84
        self._writedata(data3)

        self._writecommand(ST7735.PWCTR2)               #Power control
        data1[0] = 0xC5   #VGH = 14.7V, VGL = -7.35V
        self._writedata(data1)

        data2 = bytearray(2)
        self._writecommand(ST7735.PWCTR3)               #Power control
        data2[0] = 0x0A   #Opamp current small
        data2[1] = 0x00   #Boost frequency
        self._writedata(data2)

        self._writecommand(ST7735.PWCTR4)               #Power control
        data2[0] = 0x8A   #Opamp current small
        data2[1] = 0x2A   #Boost frequency
        self._writedata(data2)

        self._writecommand(ST7735.PWCTR5)               #Power control
        data2[0] = 0x8A   #Opamp current small
        data2[1] = 0xEE   #Boost frequency
        self._writedata(data2)

        self._writecommand(ST7735.VMCTR1)               #Power control
        data1[0] = 0x0E
        self._writedata(data1)

        self._writecommand(ST7735.INVOFF)

        self._writecommand(ST7735.MADCTL)               #Power control
        data1[0] = 0xC8
        self._writedata(data1)

        self._writecommand(ST7735.COLMOD)               #Collor Mode
        # 3 = 12bit, 5 = 16bit, 6 = 18bit
        data1[0] = 0x05
        self._writedata(data1)

        self._writecommand(ST7735.CASET)                #Column address set.
        self.windowLocData[0] = 0x00
        self.windowLocData[1] = 0x00
        self.windowLocData[2] = 0x00
        self.windowLocData[3] = self._size[0] - 1
        self._writedata(self.windowLocData)

        self._writecommand(ST7735.RASET)                #Row address set.
        self.windowLocData[3] = self._size[1] - 1
        self._writedata(self.windowLocData)

        dataGMCTRP = bytearray([0x0f, 0x1a, 0x0f, 0x18, 0x2f, 0x28, 0x20, 0x22, 0x1f,
                            0x1b, 0x23, 0x37, 0x00, 0x07, 0x02, 0x10])
        self._writecommand(ST7735.GMCTRP1)
        self._writedata(dataGMCTRP)

        dataGMCTRN = bytearray([0x0f, 0x1b, 0x0f, 0x17, 0x33, 0x2c, 0x29, 0x2e, 0x30,
                            0x30, 0x39, 0x3f, 0x00, 0x07, 0x03, 0x10])
        self._writecommand(ST7735.GMCTRN1)
        self._writedata(dataGMCTRN)
        time.sleep_us(10)

        self._writecommand(ST7735.DISPON)
        time.sleep_us(100)

        self._writecommand(ST7735.NORON)                #Normal display on.
        time.sleep_us(10)

        self.cs(1)

    def on( self, aTF = True ) :
        '''Turn display on or off.'''
        self._writecommand(ST7735.DISPON if aTF else ST7735.DISPOFF)

    #   @micropython.native
    def _setwindowloc( self, aPos0, aPos1 ) :
        '''Set a rectangular area for drawing a color to.'''
        self._writecommand(ST7735.CASET)            #Column address set.
        self.windowLocData[0] = self._offset[0]
        self.windowLocData[1] = self._offset[0] + int(aPos0[0])
        self.windowLocData[2] = self._offset[0]
        self.windowLocData[3] = self._offset[0] + int(aPos1[0])
        self._writedata(self.windowLocData)

        self._writecommand(ST7735.RASET)            #Row address set.
        self.windowLocData[0] = self._offset[1]
        self.windowLocData[1] = self._offset[1] + int(aPos0[1])
        self.windowLocData[2] = self._offset[1]
        self.windowLocData[3] = self._offset[1] + int(aPos1[1])
        self._writedata(self.windowLocData)

        self._writecommand(ST7735.RAMWR)            #Write to RAM.

    #@micropython.native
    def _writecommand( self, aCommand ) :
        '''Write given command to the device.'''
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([aCommand]))
        self.cs(1)

    #@micropython.native
    def _writedata( self, aData ) :
        '''Write given data to the device.  This may be
            either a single int or a bytearray of values.'''
        self.dc(1)
        self.cs(0)
        self.spi.write(aData)
        self.cs(1)

    #@micropython.native
    def _setMADCTL( self ) :
        '''Set screen rotation and RGB/BGR format.'''
        self._writecommand(ST7735.MADCTL)
        rgb = ST7735RGB if self._rgb else ST7735BGR
        self._writedata(bytearray([ST7735Rotations[self.rotate] | rgb]))

    #@micropython.native
    def _reset( self ) :
        '''Reset the device.'''
        self.dc(0)
        self.reset(1)
        time.sleep_us(500)
        self.reset(0)
        time.sleep_us(500)
        self.reset(1)
        time.sleep_us(500)

    def setWindow(self,columnStart,columnEnd,rowStart,rowEnd,copy=True):
        
        if columnStart < 0: columnStart *= -1
        if rowStart < 0: rowStart *= -1
    
        if columnStart > columnEnd:
            tmp = columnEnd
            columnEnd = columnStart
            columnStart = tmp
        
        if rowStart > rowEnd:
            tmp = rowEnd
            rowEnd = rowStart
            rowStart = tmp

        if columnEnd > self._columns: columnEnd = self._columns
        if rowEnd > self._rows: rowEnd = self._rows

        self._windowColumnStart = columnStart
        self._windowColumnEnd = columnEnd
        self._windowRowStart = rowStart
        self._windowRowEnd = rowEnd
        self._windowColumns = self._windowColumnEnd - self._windowColumnStart
        self._windowRows = self._windowRowEnd - self._windowRowStart
        self._windowColumnSize = self._bytes
        self._windowRowSize = self._windowColumns * self._bytes

        self._windowBuffer = bytearray(self._windowColumns*self._windowRows*self._bytes)
        
        self._setwindowloc([self._windowColumnStart,self._windowRowStart],[self._windowColumnEnd,self._windowRowEnd])

    def flush(self):
        self._writedata(self._windowBuffer)



