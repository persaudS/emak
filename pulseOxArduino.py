#!/usr/bin/env python3
import serial


def read_pulseOx():
    # First arg: serial device name/port ['COM3', '/dev/ttyUSB0']
    # Second arg: data rate, can reduce it to 96000 or something if we don't need to poll a lot
    ser = serial.Serial('COM3', 115200, timeout=1)
    ser.reset_input_buffer()

    count = 0
    while count < 2:  # Two serial messages are sent at the start (start confirm & config confirm)
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            count += 1

    count = 0
    successes = 0
    heartrates = []
    oxygenlevels = []
    while successes < 10:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            case = count % 4

            if case == 0:
                heartrate = int(line)
            elif case == 1:
                confidence = int(line)
            elif case == 2:
                oxygen = int(line)
            elif case == 3:
                extStatus = int(line)
                print("HR: ", heartrate)
                print("Conf: ", confidence)
                print("O2: ", oxygen)
                print("Status: ", extStatus)
                print("Successes: ", successes)
                if confidence >= 95 and oxygen > 0 and extStatus == 0:
                    heartrates.append(heartrate)
                    oxygenlevels.append(oxygen)
                    successes += 1
            else:
                print("This shouldn't be possible...")
            count += 1
    avgHR = sum(heartrates) / 10.0
    avgO2 = sum(oxygenlevels) / 10.0
    return avgHR, avgO2


if __name__ == '__main__':
    read_pulseOx()
