from smbus import SMBus
import time
eeprom = 0x50
bus = SMBus(2)

#sys, dia, bpm
def getBPData():
    bus.write_byte(eeprom, 0x60)
    if (bus.read_byte(eeprom) < 1):
       print("No data")
       exit(1)

    bus.write_byte(eeprom, 0xAC)
    bloodPressureData = [bus.read_byte(eeprom) + 25, bus.read_byte(eeprom), bus.read_byte(eeprom)]
    print(bloodPressureData)
    time.sleep(0.1)
    bus.write_i2c_block_data(eeprom, 0x68, [0xFF, 0xFF])
    time.sleep(0.1)
    bus.write_i2c_block_data(eeprom, 0x60, [0x00, 0x80])
    time.sleep(0.1)
    bus.write_i2c_block_data(eeprom, 0x64, [0x00, 0x80])
    return bloodPressureData
