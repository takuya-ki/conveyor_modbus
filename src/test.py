from pymodbus.client.sync import ModbusSerialClient as ModbusClient

#---------- open connection ----------#
client = ModbusClient(method = "rtu", port="COM5",stopbits = 1, bytesize = 8, parity = 'E', baudrate= 115200, timeout= 1)
client.connect()

#---------- read data ----------#
# address   : register number
# count     : number of registers to be read 
# unit      : unit number of slave device
result= client.read_holding_registers(address=100, count=1, unit= 1)

print(result.registers)

#---------- close connection ----------#
client.close()
