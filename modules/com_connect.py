import serial

ser = serial.Serial('COM1', 115200)

with open("input.txt", "r") as file:
    for line in file:
        command = line.strip().encode()
        ser.write(command)

response = ser.read(10)
print(response)

ser.close()