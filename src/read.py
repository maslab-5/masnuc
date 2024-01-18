import serial

# python3 -m serial.tools.list_ports
# sudo chmod 666 /dev/ttyACM0

ser = serial.Serial(port='/dev/...',baudrate=9600)

while True:
    value = ser.readline()
    valueInString = str(value,'UTF-8')
    print(valueInString)
