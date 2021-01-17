from pymodbus.client.sync import ModbusSerialClient

client = ModbusSerialClient(port='/dev/ttyUSB0')
response = client.read_holding_registers(0x00,4,unit=1)
print(response)
client.close()
