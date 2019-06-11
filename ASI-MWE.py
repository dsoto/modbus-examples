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
    # response = client.read_holding_registers(address, num_registers, unit=0x01)

    # pull the data from the "deferred response handle"
    # the reading is a 16-bit integer but we divide and get a floating point number
    # reading = response.registers[0] / scale

    reading = client.read_holding_registers(address, num_registers, unit=0x01).registers[0]

    # write to the console
    print(reading/scale)

    # delay for one second
    time.sleep(1.0)


