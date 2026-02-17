# core/feedback.py
import time
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

class FeedbackSystem:
    def __init__(self):
        self.GREEN_PIN = 17   
        self.RED_PIN = 27     
        self.YELLOW_PIN = 22  
        self.BUZZER_PIN = 4   
        self.SERVO_PIN = 18   
        
        self.servo = None
        
        if GPIO_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            GPIO.setup(self.GREEN_PIN, GPIO.OUT)
            GPIO.setup(self.RED_PIN, GPIO.OUT)
            GPIO.setup(self.YELLOW_PIN, GPIO.OUT)
            GPIO.setup(self.BUZZER_PIN, GPIO.OUT)
            
            GPIO.setup(self.SERVO_PIN, GPIO.OUT)
            self.servo = GPIO.PWM(self.SERVO_PIN, 50) 
            self.servo.start(0)
            
            self.reset_leds()
            self.lock_door() 

    def reset_leds(self):
        if GPIO_AVAILABLE:
            GPIO.output(self.GREEN_PIN, 0)
            GPIO.output(self.RED_PIN, 0)
            GPIO.output(self.YELLOW_PIN, 0)
            GPIO.output(self.BUZZER_PIN, 0)

    def set_servo_angle(self, angle):
        if not GPIO_AVAILABLE: return
        try:
            duty = 2.5 + (angle / 18)
            GPIO.output(self.SERVO_PIN, True)
            self.servo.ChangeDutyCycle(duty)
            time.sleep(0.5)
            GPIO.output(self.SERVO_PIN, False)
            self.servo.ChangeDutyCycle(0)
        except: pass

    # 🔥 REVERSED LOGIC HERE (INVERSED)
    def lock_door(self):
        self.set_servo_angle(0)   # Changed from 70 to 0

    def unlock_door(self):
        self.set_servo_angle(70)  # Changed from 0 to 70

    def access_granted(self):
        if GPIO_AVAILABLE:
            GPIO.output(self.GREEN_PIN, 1)
            GPIO.output(self.YELLOW_PIN, 0)
            self.unlock_door()
            time.sleep(5) 
            self.lock_door()
            GPIO.output(self.GREEN_PIN, 0)

    def access_denied(self):
        if GPIO_AVAILABLE:
            GPIO.output(self.YELLOW_PIN, 0)
            for _ in range(3):
                GPIO.output(self.RED_PIN, 1)
                GPIO.output(self.BUZZER_PIN, 1)
                time.sleep(0.1)
                GPIO.output(self.RED_PIN, 0)
                GPIO.output(self.BUZZER_PIN, 0)
                time.sleep(0.1)

    def processing(self):
        if GPIO_AVAILABLE:
            GPIO.output(self.YELLOW_PIN, 1)

    def stop_processing(self):
        if GPIO_AVAILABLE:
            GPIO.output(self.YELLOW_PIN, 0)
            
    def cleanup(self):
        if GPIO_AVAILABLE:
            try:
                if self.servo: 
                    self.servo.stop()
                    self.servo = None
                GPIO.cleanup()
            except: pass