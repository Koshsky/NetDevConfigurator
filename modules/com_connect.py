import serial
import time

with serial.Serial('/dev/ttyUSB0', 115200, timeout=2) as ser:
    time.sleep(1)
    login = "mvsadmin\n"
    password = "MVS_admin\n"
    
    ser.write(login.encode())
    ser.write(password.encode())
    ser.write("set cli pagination off\n".encode())

    ser.write("show run\n".encode())
    ser.write("exit\n".encode())

    for line in ser.readlines():
        print(line.decode('utf-8'), end='')