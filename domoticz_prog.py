import time
import RPi.GPIO as GPIO
import domoticz_lib as D
import Adafruit_DHT


GPIO.setmode(GPIO.BCM)

dom = D.Domoticz("domoticz", 8080)
dom.startDHT(Adafruit_DHT.DHT22, 14)


LED_RED, LED_GREEN, LED_BLUE = 17, 27, 22

GPIO.setup(LED_RED, GPIO.OUT, initial=GPIO.LOW)
#led_red = GPIO.PWM(LED_RED, 0.5)
#led_red.start(100)

while True:
    time.sleep(1)
    GPIO.output(LED_RED, GPIO.LOW)
    time.sleep(1)
    GPIO.output(LED_RED, GPIO.HIGH)
    
GPIO.cleanup();
