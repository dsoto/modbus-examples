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
    address = 227      # this is the location for the wheel diameter
    num_registers = 1  # number of 16-bit readings to make
    device_ID = 0x01   # identifier for the ASI controller to distinguish from other devices
    values = [568]     # values should be passed in as a list

    # query the ASI controller for a register value
    reading = client.read_holding_registers(address, num_registers, unit=0x01).registers[0]

    # write to the console
    print(reading)

    # write values to the controller
    # NOTE: these values will not persist in flash
    client.write_registers(address, values, unit=device_ID);

    # delay for one second
    time.sleep(1.0)


#                            byte    1    2   3    4   5   6   7   8    9   10   11
# DEBUG:pymodbus.transaction:SEND: 0x1 0x10 0x0 0xe3 0x0 0x1 0x2 0x2 0x38 0xb0 0xb1
# byte 1      - device ID
# byte 2      - write multiple registers command
# byte 3, 4   - address to begin writes 0xe3 = 15*16 + 3 = 227
# byte 5      - blank byte
# byte 6      - number of registers to write
# byte 7      - number of bytes in payload
# byte 8, 9   - data values 0x238 = 2*256 + 3*16 + 8 = 568
# byte 10, 11 - CRC checksum

#                            byte    1    2   3    4   5   6    7    8
# DEBUG:pymodbus.transaction:RECV: 0x1 0x10 0x0 0xe3 0x0 0x1 0xf0 0x3f
# byte 1       - device ID
# byte 2       - write multiple registers command
# byte 3, 4    - address of write
# byte 5       - blank byte
# byte 6       - registers written
# byte 7, 8    - CRC checksum
