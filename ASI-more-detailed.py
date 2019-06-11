import pymodbus.client.sync      # Python Modbus library
import logging
import time

# configure logging
# this allows you to see the bytes being sent and received
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# connect to serial and start modbus using the RTU protocol
port = '/dev/tty.usbserial-AM00G7KX'
client = pymodbus.client.sync.ModbusSerialClient(method='rtu',
                                                 port=port,
                                                 timeout=2,
                                                 baudrate=115200)
client.connect()

# read battery voltage and loop
while 1:
    address = 265      # this is the location for the battery voltage data
    scale = 32.0       # this is the number the data must be divided by to get the voltage
    num_registers = 1  # number of 16-bit readings to make
    device_ID = 0x01   # identifier for the ASI controller to distinguish from other devices

    # query the device
    response = client.read_holding_registers(address, num_registers, unit=0x01)
    print("Here is the response object type", type(response))
    print("Here is the response registers type (list)", type(response.registers))
    print("Here is that list", response.registers)
    print("The data register values are of type:", type(response.registers[0]))

    # get the data and divide by the scaling factor
    reading = response.registers[0] / scale

    # the reading is a 16-bit integer but we divide and get a floating point number
    print("Now that you have divided, you have a float", type(reading))

    # write to the console
    print(reading)

    # remove this to get continuous readings
    break

    # delay for one second
    time.sleep(1.0)



# Here is the request from the console log
# DEBUG:pymodbus.transaction:SEND: 0x1 0x3 0x1 0x9 0x0 0x1 0x55 0xf4
# The first byte is the device_ID, 0x1
# The second byte is the command type, 0x3 for reading registers
# Bytes 3 and 4 are the address 1*256 + 9 = 265
# Bytes 5 and 6 are the number of registers to read
# Bytes 7 and 8 are the CRC checksum to ensure data integrity

# Here is the response from the console log
# DEBUG:pymodbus.transaction:RECV: 0x1 0x3 0x2 0x7 0x1c 0xbb 0xbd
# The first byte is the device_ID, 0x1
# The second byte is the command type, 0x3 for reading registers
# Byte 3 is the length of the payload in bytes (2 for a 16-bit int)
# Bytes 4 and 5 are the data 0x71c = 7*256 + 1*16 + 12 = 1820 (divided by 32 is about 57V)
# Bytes 6 and 7 are the CRC checksum to ensure data integrity
