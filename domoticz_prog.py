import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import domoticz_lib as D

a = D.Domoticz("192.168.1.62", 8080);

GPIO.setmode(GPIO.BCM)

DHT_PIN = 14

LED_RED, LED_GREEN, LED_BLUE = 17, 27, 22

GPIO.setup(LED_RED, GPIO.OUT, initial=GPIO.LOW)
#led_red = GPIO.PWM(LED_RED, 0.5)
#led_red.start(100)

while True:
    time.sleep(1)
    GPIO.output(LED_RED, GPIO.LOW)
    time.sleep(1)
    GPIO.output(LED_RED, GPIO.HIGH)
    
    """humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")
    """


GPIO.cleanup();
