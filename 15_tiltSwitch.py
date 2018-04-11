#!/usr/bin/env python
#red lead to 3.3v
#black lead to GND
#yellow lead to GPIO 17
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import socket
import time


SERVERIP = '10.0.0.43'
TiltPin = 17
LedPin  = 12
Led_status = 1


def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(TiltPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(LedPin, GPIO.LOW) # Set LedPin high(+3.3V) to off led

def swLed(ev=None):
    n = 0
    global Led_status
    global LCD
    lcd = LCD.Adafruit_CharLCDPlate()
    Led_status = not Led_status
    GPIO.output(LedPin, Led_status)  # switch led status(on-->off; off-->on)
    print "LED: off" if Led_status else "LED: on"
    if Led_status == 1:
        lcd.message("LED off")
    else:
        lcd.message("LED: on")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVERIP, 8881))
    print "%d : Connected to server" % n,
    data = "'Matts tilt switch','n', 'Tilt Detected'"
    sock.sendall(data)
    print " Sent:", data
    sock.close( )
    n += 1
    time.sleep(30)

def loop():
    GPIO.add_event_detect(TiltPin, GPIO.FALLING, callback=swLed, bouncetime=100) # wait for falling
    while True:
        pass   # Don't do anything

def destroy():
    GPIO.output(LedPin, GPIO.LOW)     # led off
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()