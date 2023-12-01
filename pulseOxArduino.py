#!/usr/bin/env python3
import serial

if __name__ == '__main__':
    # First arg: serial device name/port ['COM3', '/dev/ttyUSB0']
    # Second arg: data rate, can reduce it to 96000 or something if we don't need to poll a lot
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.reset_input_buffer()

    count = 0
    while count < 2:  # Two serial messages are sent at the start (start confirm & config confirm)
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)

    count = 0
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            case = count % 4

            if case == 0:
                heartrate = line
            elif case == 1:
                confidence = line
            elif case == 2:
                oxygen = line
            elif case == 3:
                extStatus = line
                print(heartrate)
                print(confidence)
                print(oxygen)
                print(extStatus)
            else:
                print("This shouldn't be possible...")
            count += 1
