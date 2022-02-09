import RPi.GPIO as GPIO
import time
from motor_control import DCMotor
from sound_sensor import SoundSensor
from play_sound import play_mp3
from gpiozero import LED

# motor controller pins
PWM1 = 14
LN1 = 15
LN2 = 18
# sound sensor pin
SOUND_PIN = 20 
# LED pin
LED_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def ms_now():
    """
    Returns the current time in miliseconds.
    """
    return round(time.time() * 1000)

class KnockCounter:
    """
    Class to handle knocks.
    """
    def __init__(self, correct_knock_pattern):
        self.knock_count = 1
        self.max_knock_interval = 2000 # 2 seconds
        self.knock_timing_tolerance = 300
        self.avg_timing_tolerance = 200
        self.correct_pattern = correct_knock_pattern
        self.reset_knock_pattern()
        self.last_knock_time = ms_now()
        
        
    def reset_knock_pattern(self):
        self.knock_pattern = [0] * len(self.correct_pattern)
        
    def pattern_not_full(self):
        return self.knock_count < len(self.knock_pattern) + 1
        
    def knock_within_interval(self, time):
        return time - self.last_knock_time < self.max_knock_interval
    
    def update_knock_pattern(self):
        knock_interval = ms_now() - self.last_knock_time
        self.knock_pattern[self.knock_count-1] = knock_interval
        self.knock_count += 1
        self.last_knock_time = ms_now()
        print(f'Knock interval: {knock_interval}')
                
    def normalize_knock_pattern(self):
        longest = max(self.knock_pattern)
        shortest = min(self.knock_pattern)
        scale = 100
        normalized_pattern = filter(
            lambda k: scale * (k - shortest) / (longest - shortest),
            self.knock_pattern
        )
        return normalized_pattern
    
    def is_correct_pattern(self):
        # Test 1: must be correct number of knocks
        if 0 in self.knock_pattern:
            return False
        patterns = zip(self.knock_pattern, self.correct_pattern)
        
        # Test 2: must be within tolerance
        total_error = 0
        for actual, correct in patterns:
            timing_error = abs(actual - correct)
            total_error += timing_error
            if abs(actual - correct) > self.knock_timing_tolerance:
                return False
        
        # Test 3: must be somewhat accurate throughout
        if total_error / len(self.correct_pattern) > self.avg_timing_tolerance:
            return False
        
        return True
    
def open_close_door(motor, timeout=5):
    handle_distance = 2
    print('Opening door...')
    motor.move(handle_distance)
    print('Door open.')
    time.sleep(timeout)
    print('Closing door...')
    motor.move_back(handle_distance)
    print('Door closed.')

def flash_led(led, times=4):
    for _ in range(times):
        led.on()
        time.sleep(.3)
        led.off()
        time.sleep(.3)
        
def handle_door_handle():
    motor = DCMotor(LN1, LN2, PWM1)
    sensor = SoundSensor(SOUND_PIN)
    led = LED(LED_PIN)
    
    CORRECT_KNOCK_PATTERN = [1000, 300]
    
    while True:
        
        if not sensor.detected():
            continue
        
        knc = KnockCounter(CORRECT_KNOCK_PATTERN)
        now = ms_now()
        print(f'SENSOR INIT DETECTED at {now}\n')
        
        if knc.pattern_not_full() and knc.knock_within_interval(now):
            print('LISTENING FOR NEXT KNOCKS')
            
        while knc.pattern_not_full() and knc.knock_within_interval(now):
            now = ms_now()
            if sensor.detected() and now - knc.last_knock_time > 120:
                print('SENSOR DETECTED\nUPDATING PATTERN\n')
                knc.update_knock_pattern()
                print(f'KNOCK PATTERN: {knc.knock_pattern}')
                
        print(f'PATTERN NOT FULL: {knc.pattern_not_full()}')
        print(f'KNOCK W/N INTERVAL: {knc.knock_within_interval(now)}')
        
        if knc.is_correct_pattern():
            print('CORRECT PATTERN\n')
            play_mp3('nice.mp3')
            open_close_door(motor)
        else:
            print('INCORRECT PATTERN\n')
            play_mp3('you_stoopid.mp3')
            flash_led(led)


if __name__ == '__main__':
    print('Listening for knocks...')
    try:
        handle_door_handle()
    except KeyboardInterrupt:
        print('Exiting!')
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        
