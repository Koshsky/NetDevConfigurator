import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port="/dev/ttyUSB1",
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS,
)

ser.open()

print('Enter your commands below.\r\nInsert "exit" to leave the application.')

while 1:
    req = input(">> ")
    if req == "exit":
        ser.close()
        exit()
    else:
        ser.write(input + "\r\n")
        out = ""
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)
        if out != "":
            print(">>" + out)
