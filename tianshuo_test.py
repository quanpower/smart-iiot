import socket
import time
import select
from utils import calc, str2hexstr

timeout_in_seconds = 5

rs485_socket = socket.socket()
rs485_socket.connect(("192.168.0.7", 26))
rs485_socket.setblocking(0)

address = chr(0x01)
function_code = chr(0x01)
start_at_reg = chr(0x00) + chr(0x13)
num_of_reg = chr(0x00) + chr(0x13)

read_device = address + function_code + start_at_reg + num_of_reg
print(type(read_device))
print(read_device)
crc = calc(read_device)
crc_hi = crc/256
crc_lo = crc & 0xFF
print "meter add: " + str(ord(address))
print "crc_lo: " + str(hex(crc_lo))
print "crc_hi: " + str(hex(crc_hi))


read_switch_str = '010600000001'


bytearray_switch = bytearray.fromhex(read_switch_str)
hexstr_switch = str(bytearray_switch)

print(hex(calc(hexstr_switch)))


while True:
	time.sleep(10)
	# s_open = '010f00100004010fbf51'
	# s_close = '010f001000040100ff55'

	# s_open = '0101001300138c02'
	
	power_1_close = '010500100000CC0F'
	power_1_open = '01050010FF008DFF'

	power_2_close = '020500100000CC3C'
	power_2_open = '02050010FF008DCC'

	power_1_close_hex = str2hexstr(power_1_close)
	power_1_open_hex = str2hexstr(power_1_open)

	power_2_close_hex = str2hexstr(power_2_close)
	power_2_open_hex = str2hexstr(power_2_open)

	inp = 'input'

	rs485_socket.sendall(power_1_close_hex)
	ready = select.select([rs485_socket], [], [], timeout_in_seconds)

	if ready[0]:
		print('have open data!')
		data = rs485_socket.recv(1024)
		ret_str = str(data)
		print(ret_str)


	time.sleep(10)

	# rs485_socket.sendall(power_1_open_hex)
	# ready1 = select.select([rs485_socket], [], [], timeout_in_seconds)

	# if ready1[0]:
	# 	data1 = rs485_socket.recv(1024)

	# 	print('have close data!')


	# 	ret_str = str(data1)
	# 	print(ret_str)


	rs485_socket.sendall(power_2_close_hex)
	ready = select.select([rs485_socket], [], [], timeout_in_seconds)

	if ready[0]:
		print('have open data!')
		data = rs485_socket.recv(1024)
		ret_str = str(data)
		print(ret_str)


	time.sleep(10)

	# rs485_socket.sendall(power_2_open_hex)
	# ready1 = select.select([rs485_socket], [], [], timeout_in_seconds)

	# if ready1[0]:
	# 	data1 = rs485_socket.recv(1024)

	# 	print('have close data!')


	# 	ret_str = str(data1)
	# 	print(ret_str)




