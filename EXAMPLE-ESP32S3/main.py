
import time
import machine

import sys

from CanvasPainter import CanvasPainter
from ST7735 import ST7735

from machine import Pin, SPI

machine.freq(240000000)
print("CPU FREQUENCY",machine.freq())

led = machine.Pin(2, machine.Pin.OUT)


spi = SPI(1, baudrate=33000000, polarity=0, phase=0, sck=Pin(17), mosi=Pin(18), miso=Pin(0))
tft = ST7735(spi,4,5,6)
data = CanvasPainter(window=tft)

start_time = time.ticks_ms()
data.setColor(0,255,0,CanvasPainter.COLOR_FILL)
data.setWindow(0,128,0,160,False)
data.flush()
end_time = time.ticks_ms()
print("1sT TIME mS", (end_time-start_time) )

start_time = time.ticks_ms()
data.setThikness(1)
data.setColor(126,126,0,CanvasPainter.COLOR_FILL)
data.setColor(0,0,255)
data.drawRectangle(5,5,100,30,True)
end_time = time.ticks_ms()
print("2nD TIME mS", (end_time-start_time) )

start_time = time.ticks_ms()
data.setThikness(3)
data.setColor(255,0,0)
data.drawLineH(5,5,50)
end_time = time.ticks_ms()
print("3tH TIME mS", (end_time-start_time) )

start_time = time.ticks_ms()
data.loadFont('font16bits-20X5.bmp')
data.setColor(0,255,0,CanvasPainter.COLOR_FILL)
data.setColor(0,0,255)
data.setWindow(0,128,10,21,False)
data.printChars(5,1,'Hello World!')
data.flush()
print("4tH TIME mS", (end_time-start_time) )

start_time = time.ticks_ms()
data.setColor(255,0,0,CanvasPainter.COLOR_FILL)
data.setWindow(30,72,30,72,False)
data.setColor(255,255,255,CanvasPainter.COLOR_TRANSPARENCY)
data.loadImage(2,2,'picture16bits.bmp')
data.flush()
end_time = time.ticks_ms()
print("5tH TIME mS", (end_time-start_time) )


xHline = 5
xInc = 5

rCircle = 5
rInc = 5

fSize = 8
fInc = 1

angleStart = 5
angleEnd = 10
angleInc = 5

while True:

    led.value(1)

    if xHline > 78: xInc *= -1
    if xHline < 5: xInc *= -1
    start_time = time.ticks_ms()
    data.setColor(0,255,0,CanvasPainter.COLOR_FILL)
    data.setWindow(0,128,0,10,False)
    data.setThikness(3)
    data.setColor(255,0,0)
    data.drawLineH(xHline,3,50)
    data.flush()
    xHline += xInc
    end_time = time.ticks_ms()
    print("HLine mS", (end_time-start_time) )


    if angleEnd > 360:
        angleEnd = 360
        angleStart += 5

    if angleStart >= angleEnd:
        angleStart = 5
        angleEnd = 10

    if rCircle > 25: rInc *= -1
    if rCircle < 5: rInc *= -1
    if rCircle < 1: rCircle = 1
    start_time = time.ticks_ms()
    data.setColor(0,255,0,CanvasPainter.COLOR_FILL)
    data.setWindow(34,94,90,150,False)
    data.setThikness(1)
    data.setColor(0,0,255)
    data.setColor(255,0,0,CanvasPainter.COLOR_FILL)
    data.drawCircle(30,30,rCircle,False,angleStart,angleEnd)
    data.flush()
    rCircle += rInc
    angleEnd += angleInc
    end_time = time.ticks_ms()
    print("CIRCLE mS", (end_time-start_time) )



    if fSize < 8: fInc *= -1
    if fSize > 16: fInc *= -1
    start_time = time.ticks_ms()
    data.setColor(0,255,0,CanvasPainter.COLOR_FILL)
    data.setColor(255,0,0)
    data.setWindow(72,128,30,70,False)
    data.printChars(20,20,'Oi',fSize)
    data.flush()
    fSize += fInc
    end_time = time.ticks_ms()
    print("CHAR mS", (end_time-start_time) )

    led.value(0)