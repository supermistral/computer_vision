import RPi.GPIO as gpio

class Motors():
    def __init__(self):
        gpio.setmode(gpio.BCM)
        self.motors = [26, 19, 13, 6]
        gpio.setup(self.motors[0], gpio.OUT)
        gpio.setup(self.motors[1], gpio.OUT)
        gpio.setup(self.motors[2], gpio.OUT)
        gpio.setup(self.motors[3], gpio.OUT)
    
    def forward(self):
        gpio.output(self.motors[0], gpio.LOW)
        gpio.output(self.motors[1], gpio.HIGH)
        gpio.output(self.motors[2], gpio.LOW)
        gpio.output(self.motors[3], gpio.HIGH)
        
    def back(self):
        gpio.output(self.motors[0], gpio.HIGH)
        gpio.output(self.motors[1], gpio.HIGH)
        gpio.output(self.motors[2], gpio.HIGH)
        gpio.output(self.motors[3], gpio.HIGH)
        
    def left(self):
        gpio.output(self.motors[3], gpio.LOW)
        gpio.output(self.motors[1], gpio.HIGH)
        
    def right(self):
        gpio.output(self.motors[1], gpio.LOW)
        gpio.output(self.motors[3], gpio.HIGH)
        
    def stop(self):
        gpio.output(self.motors[1], gpio.LOW)
        gpio.output(self.motors[3], gpio.LOW)
