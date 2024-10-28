from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import logging
import struct
def signed_to32bitFloat(result):
    register1 = result[0]  # Higher 16 bits
    register2 = result[1]   # Lower 16 bits

# Convert to hexadecimal
    hex_value = (register1 << 16) | register2

# Convert to bytes (big-endian)
    byte_value = hex_value.to_bytes(4, byteorder='big')

# Convert bytes to float
    float_value = struct.unpack('>f', byte_value)[0]

    print(f"Float value: {float_value}")
    return float_value

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x01

def run_sync_client():
    client = ModbusClient(method='rtu', port='COM7', timeout=1, baudrate=9600, parity='E', stopbits=1, bytesize=8)
    if client.connect():
        try:
            request = client.read_holding_registers(address=3027, count=2, unit=UNIT)
            if not request.isError():
                result = request.registers
                log.info(f"Registers: {result}")
                
                # Create a BinaryPayloadDecoder with the correct endianness
                #decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Little, wordorder=Endian.Big)
                float_value = signed_to32bitFloat(result)
                
                log.info(f"Decoded 32-bit float: {float_value}")
            else:
                log.error(f"Modbus request error: {request}")
        except Exception as e:
            log.error(f"Exception occurred: {e}")
        finally:
            client.close()
    else:
        log.error("Failed to connect to Modbus client.")

if __name__ == "__main__":

    run_sync_client()
