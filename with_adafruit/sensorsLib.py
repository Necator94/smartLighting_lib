import time
import threading
import Queue
import Adafruit_BBIO.GPIO as GPIO
import logging

class sensors(threading.Thread):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.queue = Queue.Queue()
        self.gpio_read = 'P9_23'                    # GPIO recieves current detector status 0 - motion detected, 1 - no motion
        self.gpio_source = 'P9_27'                  # GPIO sets source voltage for futher recieving by gpio_read
        self.stopsign = None
        self.tm = 0.1                               # Default iteration pause in main checking cycle
        threading.Thread.__init__(self)

    # checking cycle
    def run(self):
        self.logger.info('Checking cycle start')
        GPIO.setup(self.gpio_read, GPIO.IN)         # Prepare corresponding GPIO for further usage with neccecary paramenters
        GPIO.setup(self.gpio_source, GPIO.OUT)      # Prepare corresponding GPIO for further usage with neccecary paramenters
        GPIO.output(self.gpio_source, GPIO.HIGH)    

        while True:                                 # Main Checking cycle
            if self.stopsign == 'stopScanning':     # Break checking cycle in case of using "stop" method
                    self.logger.warning('Checking cycle stoped')
                    break          
            if GPIO.input(self.gpio_read) == 0: self.queue.put(time.time()) # Put time sample in queue in case of movement
            time.sleep(self.tm)                     # Iteration pause to avoid redundancy
 
    def get_queue(self): return self.queue.get()    # Returns a queue object

    def stop(self):                                 # Method to stop checking cycle
        self.stopsign = 'stopScanning'
        GPIO.cleanup()

    def setTime(self, tm=0.1):                      # Method to set iteration pause (0.1 second by default)
        self.tm = tm         
        self.logger.info('Current iteration pause is %s seconds' % (self.tm))
