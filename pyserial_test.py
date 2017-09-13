import socket
import time

obj = socket.socket()

obj.connect(("192.168.0.7", 26))

# ret_bytes = obj.recv(1024)
# ret_str = str(ret_bytes,encoding="utf-8")
# print(ret_str)

while True:
	time.sleep(10)
	s_open = '010f00100004010fbf51'
	s_close = '010f001000040100ff55'

	bytearray_open = bytearray.fromhex(s_open)
	bytearray_close = bytearray.fromhex(s_close)

	hexstr_open = str(bytearray_open)
	hexstr_close = str(bytearray_close)

	print(hexstr_open)
	print(hexstr_close)
	inp = 'input'

	if inp == "q":
	    obj.sendall(bytes(inp,encoding="utf-8"))
	    # break
	else:
	    obj.sendall(hexstr_open)
	    ret_bytes = obj.recv(1024)
	    ret_str = str(ret_bytes)
	    print(ret_str)
	    time.sleep(10)

	    obj.sendall(hexstr_close)
	    ret_bytes = obj.recv(1024)
	    ret_str = str(ret_bytes)
	    print(ret_str)
