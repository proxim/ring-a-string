import RPi.GPIO as GPIO
import time

class DCMotor:
    """
    Class to control DC motor via L298n motor controller.
    """

    def __init__(self, pin_one, pin_two,
                 pwm_pin, freq=50, name='DC Motor',
                 time_dist_const=1):
        """ init method
        (1) pin_one, type=int,  GPIO pin connected to IN1 or IN3
        (2) Pin two type=int, GPIO pin connected to IN2 or IN4
        (3) pwm_pin type=int, GPIO pin connected to EnA or ENB
        (4) freq in Hz default 50
        (5) name, type=string, name attribute
        """
        self.name = name
        self.pin_one = pin_one
        self.pin_two = pin_two
        self.pwm_pin = pwm_pin
        self.freq = freq
        self.time_dist_const = time_dist_const

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin_one, GPIO.OUT)
        GPIO.setup(self.pin_two, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)

        self.my_pwm = GPIO.PWM(self.pwm_pin, self.freq)
        self.last_pwm = 0
        self.my_pwm.start(self.last_pwm)


    def forward(self, duty_cycle=50):
        """ Move motor forwards passed duty cycle for speed control """
        GPIO.output(self.pin_one, True)
        GPIO.output(self.pin_two, False)
        if duty_cycle != self.last_pwm:
            self.my_pwm.ChangeDutyCycle(duty_cycle)
            self.last_pwm = duty_cycle

    def backward(self, duty_cycle=50):
        """ Move motor backwards passed duty cycle for speed control"""
        GPIO.output(self.pin_one, False)
        GPIO.output(self.pin_two, True)
        if duty_cycle != self.last_pwm:
            self.my_pwm.ChangeDutyCycle(duty_cycle)
            self.last_pwm = duty_cycle

    def stop(self, duty_cycle=0):
        """ Stop motor"""
        GPIO.output(self.pin_one, False)
        GPIO.output(self.pin_two, False)
        if duty_cycle != self.last_pwm:
            self.my_pwm.ChangeDutyCycle(duty_cycle)
            self.last_pwm = duty_cycle

    def brake(self, duty_cycle=100):
        """ brake motor"""
        GPIO.output(self.pin_one, True)
        GPIO.output(self.pin_two, True)
        if duty_cycle != self.last_pwm:
            self.my_pwm.ChangeDutyCycle(duty_cycle)
            self.last_pwm = duty_cycle

    def cleanup(self, clean_up=False):
        """ cleanup all GPIO connections used in event of error by lib user"""
        GPIO.output(self.pin_one, False)
        GPIO.output(self.pin_two, False)
        self.my_pwm.ChangeDutyCycle(0)
        if clean_up:
            GPIO.cleanup()
    
    def move(self, distance):
        self.forward(self.freq)
        time.sleep(distance * self.time_dist_const)
        self.stop()
        
    def move_back(self, distance):
        self.backward(self.freq)
        time.sleep(distance * self.time_dist_const)
        self.stop()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def cleanup():
    GPIO.cleanup()

def test_motors(*motors):
    print('Testing motors.')
    
    for i in range(2):
        for motor in motors:
            print('forward')
            motor.move(2)
        
        for motor in motors:
            print('backward')
            motor.move_back(2)
        
        for motor in motors:
            motor.stop()
        print('testing done')
        
if __name__ == '__main__':
    setup()
    # motor controller 1 pins
    PWM1 = 14
    LN1 = 15
    LN2 = 18
    
    setup()
    
    # set up motor
    motor = DCMotor(LN1, LN2, PWM1)

    
    test_motors(motor)

    cleanup()
    
    
    
    
    
    
    