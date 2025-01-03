
import machine
import time
from FrameBuffer import *
from ST7735 import * 

from machine import Pin

machine.freq(240000000)
print("CPU FREQUENCY",machine.freq())

led = machine.Pin(2, machine.Pin.OUT)


spi = SPI(1, baudrate=33000000, polarity=0, phase=0, sck=Pin(17), mosi=Pin(18), miso=Pin(0))
tft = ST7735(spi,4,5,6)
data = FrameBuffer(128,160,window=tft)



start_time = time.ticks_ms()
data.setColor(0,255,0,True)
data.setWindow(0,128,0,160,False)
data.flush()
end_time = time.ticks_ms()
print("1sT TIME mS", (end_time-start_time) )


start_time = time.ticks_ms()
#data.setColor(0,255,0,True)
#data.setWindow(0,128,0,50)
data.setThikness(1)
data.setColor(126,126,0,True)
data.setColor(0,0,255)
data.drawRectangle(5,5,100,30,True)
#data.flush()
end_time = time.ticks_ms()
print("2nD TIME mS", (end_time-start_time) )

start_time = time.ticks_ms()
#data.setColor(0,255,0,True)
#data.setWindow(0,128,100,160)
data.setThikness(3)
data.setColor(255,0,0)
data.drawLineH(5,5,50)
#data.flush()
end_time = time.ticks_ms()
print("3tH TIME mS", (end_time-start_time) )

start_time = time.ticks_ms()
data.loadFont('font16bits-20X5.bmp')
data.setColor(0,255,0,True)
data.setColor(0,0,255)
data.setWindow(0,128,20,30,False)
data.printChars(5,1,'Hello World!')
data.flush()
print("4tH TIME mS", (end_time-start_time) )

start_time = time.ticks_ms()
data.setColor(255,255,255,True)
data.setWindow(0,128,30,70,False)
data.loadImage(0,0,'dog.bmp')
data.flush()
end_time = time.ticks_ms()
print("5tH TIME mS", (end_time-start_time) )

xHline = 4
xInc = 4

rCircle = 4
rInc = 4


while True:

    led.value(1)

    if xHline > 78: xInc *= -1
    if xHline < 4: xInc *= -1
    start_time = time.ticks_ms()
    data.setColor(0,255,0,True)
    data.setWindow(0,128,5,11,False)
    data.setThikness(3)
    data.setColor(255,0,0)
    data.drawLineH(xHline,3,50)
    data.flush()
    xHline += xInc
    end_time = time.ticks_ms()
    print("HLine mS", (end_time-start_time) )


    if rCircle > 25: rInc *= -1
    if rCircle < 4: rInc *= -1
    if rCircle == 0: rCircle = 1
    start_time = time.ticks_ms()
    data.setColor(0,255,0,True)
    data.setWindow(0,128,80,160,False)
    data.setThikness(0)
    data.setColor(0,255,255)
    data.drawCircle(64,40,rCircle)
    data.flush()
    rCircle += rInc
    end_time = time.ticks_ms()
    print("CIRCLE mS", (end_time-start_time) )

    led.value(0)