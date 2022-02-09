import RPi.GPIO as GPIO
from gpiozero import LED
import time

class SoundSensor:
    """
    Class to deal with sound sensor lol
    Requires a 5V.
    Pin number is from D0 (direct output).
    """
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN)
    
    def detected(self):
        """
        Returns True if a sound has been detected by the sensor,
        False otherwise.
        """
        return GPIO.input(SOUND_SENSOR_PIN) == GPIO.HIGH
    
    

LED_PIN = 21
SOUND_SENSOR_PIN = 20

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def cleanup():
    GPIO.cleanup()

if __name__ == '__main__':
    
    setup()
    led = LED(LED_PIN)
    GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN)
    print('starting')
    led.on()
    time.sleep(2)
    led.off()
    print('now')
    try: 
        while True:
            
            if GPIO.input(SOUND_SENSOR_PIN) == GPIO.HIGH:
                print('SOUND DETECTED')
                led.on()
                time.sleep(.3)
            else:
                led.off()
        
    except KeyboardInterrupt:
        print('exiting program')
        cleanup()
        

    
    
