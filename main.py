#---------------------------------------------------
# main.py 
# "Esero Kit Superblack: Measuring light reflections surfaces"
# written in MICROPYTHON (not circuitpython !)
# LED: RGB 3528 DFR0239
# Light sensor: VEML7700 ADA4162
# OLED: 0.96" I2C
#---------------------------------------------------


#---------------------------------------------------
# Libraries
#---------------------------------------------------
import time
from machine import Pin, I2C
from machine import PWM

# OLED
import ssd1306
import framebuf # some oled functions

# Light sensor
import veml7700
#---------------------------------------------------


#---------------------------------------------------
# GPIO, peripherals
#---------------------------------------------------

# VEML7700
i2c_VEML = I2C(1, scl=Pin(3), sda=Pin(2), freq=10000) # define ports
# create I2C object + initialization parameters
veml = veml7700.VEML7700(address=0x10, i2c=i2c_VEML, it=200, gain=1/8) 

# OLED Screen
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# RGB LED 
LED_R = PWM( Pin(6) )
LED_G = PWM( Pin(4) )
LED_B = PWM( Pin(5) )
LED_R.freq(5000)
LED_G.freq(5000)
LED_B.freq(5000)
#---------------------------------------------------


#---------------------------------------------------
# Functions
#---------------------------------------------------

# RGB LED:
# 0..10; 0:Off, 10:Max
def Set_Led(R,G,B):
    factor=const(6553) # round(65535/10); NO FLOATS here
    maxValue=const(10) # Max Input Value

    LED_R.duty_u16(factor*(maxValue-R) +1)
    LED_G.duty_u16(factor*(maxValue-G) +1)
    LED_B.duty_u16(factor*(maxValue-B) +1)

# OLED 
def ClearDisplay():
    display.fill_rect(0, 0, 128, 64, 0)
    display.show()
    
    
#---------------------------------------------------
#---------------------------------------------------
# START main:
#---------------------------------------------------
#---------------------------------------------------
display.rotate(False)

#---------------------------------------------------
# LOGO
#---------------------------------------------------
#Background ON; Active Pixels OFF
display.invert(1) 

# ESERO logo
with open('ESERO_logo.pbm', 'rb') as img1:
    img1.readline() 
    img1.readline() 
    img1.readline() 
    data = bytearray(img1.read())
fbuf = framebuf.FrameBuffer(data, 100, 33, framebuf.MONO_HLSB)
display.blit(fbuf, 0, 0, 0)

# LIST logo
with open('LIST_logo.pbm', 'rb') as img2:
    img2.readline() 
    img2.readline() 
    img2.readline() 
    data = bytearray(img2.read())
fbuf = framebuf.FrameBuffer(data, 50, 20, framebuf.MONO_HLSB)
display.blit(fbuf, 70, 40, 0)

display.show()

time.sleep(5)

ClearDisplay()

#Background OFF; Active Pixels ON
display.invert(0) 


# Const Text for main loop
display.text('Values in [lx]: ', 10, 30, 1)
display.show()
 
#------------------------------------------------
# MAIN LOOP
# only result is being newly displayed on screen. 
# clear screen: old value
# read+ display values
#------------------------------------------------
Set_Led(10,0,0)
while True:
    display.fill_rect(10, 40, 80, 10, 0)
    display.show()
    #time.sleep(0.1)
    
    display.text( str(veml.read_lux()), 10, 40, 1)
    display.show()
    
    lux_val = veml.read_lux()
    print(lux_val)
    time.sleep(0.5)

#------------------------------------------------   