import time
import math
import grove_i2c_adc
import Adafruit_BBIO.GPIO as GPIO

adc = grove_i2c_adc.I2cAdc()

def read_temperature(model = 'v1.2'):
    "Read temperature values in Celsius from Grove Temperature Sensor"
    # each of the sensor revisions use different thermistors, each with their own B value constant
    if model == 'v1.2':
        bValue = 3975  # sensor v1.2 uses thermistor ??? (assuming NCP18WF104F03RC until SeeedStudio clarifies)
    elif model == 'v1.1':
        bValue = 4250  # sensor v1.1 uses thermistor NCP18WF104F03RC
    elif model == 'v1.0':
        bValue = 3975  # sensor v1.0 uses thermistor TTC3A103*39H
    elif model == 'hts':   
        bValue = 3975  # High Temperature Sensor uses thermistor TTC3A103*39H
        
    total_value = 0
    for index in range(20):
        sensor_value = adc.read_adc()
        total_value += sensor_value
        time.sleep(0.05)
    average_value = float(total_value / 20)

    #print "average_value", average_value
    print "model", model
    
    # Transform the ADC data into the data of Arduino platform.
    sensor_value_tmp = (float)(average_value / 4095 * 2.95 * 2 / 3.3 * 1023)
    print "sensor_value_tmp", sensor_value_tmp
    resistance = (float)(1023 - sensor_value_tmp) * 10000 / sensor_value_tmp
    temperature = round((float)(1 / (math.log(resistance / 10000) / bValue + 1 / 298.15) - 273.15), 2)
    return temperature

# Hardware: Grove - I2C ADC, Grove - Temperature Sensor
# Connect the Grove - I2C ADC to I2C Grove port of Beaglebone Green, and then connect the Grove - Temperature Sensor to Grove - I2C ADC.
if __name__ == '__main__':

    while True:
        try:
            # Read temperature values in Celsius from Grove Temperature Sensor
            temperature = read_temperature('v1.2')
            
            print "temperature = ", temperature
    
            GPIO.setup("USR0", GPIO.OUT) 
            GPIO.setup("USR1", GPIO.OUT)
            GPIO.setup("USR2", GPIO.OUT)
            GPIO.setup("USR3", GPIO.OUT) 
   
            GPIO.output("USR0", GPIO.LOW)
            GPIO.output("USR1", GPIO.LOW)
            GPIO.output("USR2", GPIO.LOW)
            GPIO.output("USR3", GPIO.LOW)
                
            if temperature >= 28:
                GPIO.output("USR3", GPIO.HIGH)
                GPIO.output("USR2", GPIO.HIGH)
                GPIO.output("USR1", GPIO.HIGH)
                GPIO.output("USR0", GPIO.HIGH)
            elif temperature >= 26:
                GPIO.output("USR3", GPIO.LOW)                
                GPIO.output("USR2", GPIO.HIGH)
                GPIO.output("USR1", GPIO.HIGH)
                GPIO.output("USR0", GPIO.HIGH)                
            elif temperature >= 24:
                GPIO.output("USR3", GPIO.LOW)                
                GPIO.output("USR2", GPIO.LOW)
                GPIO.output("USR1", GPIO.HIGH)
                GPIO.output("USR0", GPIO.HIGH)               
            elif temperature >= 22:
                GPIO.output("USR3", GPIO.LOW)                
                GPIO.output("USR2", GPIO.LOW)
                GPIO.output("USR1", GPIO.LOW)
                GPIO.output("USR0", GPIO.HIGH)                

        except IOError:
            print "Error"