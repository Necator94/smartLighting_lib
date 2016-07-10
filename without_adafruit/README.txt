SmartLighting project
---------------------
Autor: Ivan Matveev
E-mail: ivan.matveev@student.emw.hs-anhalt.de
---------------------
Library for PIR sensor using. Performed without external GPIO handling libraries.

Directory contains consumer.py and sensorsLib.py files. 
consumer.py - example of library using
sensorsLib.py - the library

This implementation of library returns time samples via calling method in case of movement detection via PIR sensor.

Avaliable methods:

get_queue() - non-blocking method. Checking cycle is started via method calling (GPIO initialization included). Returns time sample in case of movement. 

stop() - stop checking cycle. Interaction with sensor is stopped.

setTime() - Provides sleep time functionality. Allows to define iteration pause in main checking cycle (0.1 second by default). 




