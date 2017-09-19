import socket
import time
import select
from utils import calc

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
	time.sleep(300)
	# s_open = '010f00100004010fbf51'
	# s_close = '010f001000040100ff55'

	# s_open = '0101001300138c02'
	
	s_close = '010600000001480a'
	s_open = '01060000000949cc'

	bytearray_open = bytearray.fromhex(s_open)
	bytearray_close = bytearray.fromhex(s_close)

	hexstr_open = str(bytearray_open)
	hexstr_close = str(bytearray_close)

	print(hexstr_open)
	print(hexstr_close)
	inp = 'input'

	rs485_socket.sendall(hexstr_open)
	ready = select.select([rs485_socket], [], [], timeout_in_seconds)

	if ready[0]:
		print('have open data!')
		data = rs485_socket.recv(1024)
		ret_str = str(data)
		print(ret_str)


	time.sleep(300)

	rs485_socket.sendall(hexstr_close)
	ready1 = select.select([rs485_socket], [], [], timeout_in_seconds)

	if ready1[0]:
		data1 = rs485_socket.recv(1024)

		print('have close data!')


		ret_str = str(data1)
		print(ret_str)

	# if inp == "q":
	#     obj.sendall(bytes(inp,encoding="utf-8"))
	#     # break
	# else:
	#     obj.sendall(hexstr_open)
	#     ret_bytes = obj.recv(1024)
	#     ret_str = str(ret_bytes)
	#     print(ret_str)
	#     time.sleep(5)
    
	#     obj.sendall(hexstr_close)
	#     ret_bytes = obj.recv(1024)
	#     ret_str = str(ret_bytes)
	#     print(ret_str)
