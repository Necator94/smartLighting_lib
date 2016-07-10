import time
import threading
import Queue
import logging

class sensors(threading.Thread):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.queue = Queue.Queue()
        self.gpio_read = 49                         # GPIO recieves current detector status 0 - motion detected, 1 - no motion
        self.gpio_source = 115                      # GPIO sets source voltage for futher recieving by gpio_read 
        self.stopsign = None
        self.tm = 0.1                               # Default iteration pause in main checking cycle
        threading.Thread.__init__(self)

    def run(self):
        self.logger.info('Checking cycle start')
        try:                                        # Clean previous state of GPIOs
            self.__gpio_unexport(self.gpio_read)    
            self.__gpio_unexport(self.gpio_source)
        except: self.logger.warning('GPIO %s and %s need to be exported' % (self.gpio_read, self.gpio_source))
        
        try:                                        # Export of GPIOs (make GPIOs ready to further configuration)
            self.__gpio_export(self.gpio_read)
            self.__gpio_export(self.gpio_source)
        except: self.logger.error('Error during GPIO %s and %s export' % (self.gpio_read, self.gpio_source))
        
        self.__gpio_set_high(self.gpio_source)

        while True:                                 # Main Checking cycle
            if self.stopsign == 'stopScanning':     # Break checking cycle in case of using "stop" method
                    self.logger.warning('Checking cycle stoped')
                    break          
            if int(self.__gpio_read(self.gpio_read)) == 0: self.queue.put(time.time()) # Put time sample in queue in case of movement
            time.sleep(self.tm)                     # Iteration pause to avoid redundancy
   
    def __gpio_export(self, gpio_n):                # Method to export GPIO 
        ex_fd = open('/sys/class/gpio/export', 'w')
        ex_fd.write(str(gpio_n))
        ex_fd.close()
        self.logger.info('GPIO %s exported' % (gpio_n))

    def __gpio_unexport(self, gpio_n):              # Method to unexport GPIO 
        unex_fd = open('/sys/class/gpio/unexport', 'w')
        unex_fd.write(str(gpio_n))
        unex_fd.close()
        self.logger.info('GPIO %s unexported' % (gpio_n))          

    def __gpio_set_high(self, gpio_n):              # Method to set high level of GPIO
        set_fd = open('/sys/class/gpio/gpio%s%s' % (gpio_n, '/direction'), 'w')
        set_fd.write('out')
        set_fd.close()
        set_fd = open('/sys/class/gpio/gpio%s%s' % (gpio_n, '/value'), 'w')
        set_fd.write("1")
        set_fd.close()
        self.logger.info('High level of GPIO %s have set' % (gpio_n))

    def __gpio_read(self,gpio_n):                    # Method to read current state of GPIO
        checkValue = open('/sys/class/gpio/gpio%s%s' % (gpio_n, '/value'), 'r')
        return checkValue.read()
 
    def get_queue(self): return self.queue.get()    # Returns a queue object

    def stop(self):                                 # Method to stop checking cycle
        self.stopsign = 'stopScanning'
        self.__gpio_unexport(self.gpio_read)
        self.__gpio_unexport(self.gpio_source)

    def setTime(self, tm=0.1):                      # Method to set iteration pause (0.1 second by default)
        self.tm = tm
        self.logger.info('Current iteration pause is %s seconds' % (self.tm))