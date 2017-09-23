from utils import str2hexstr
import socket
import time
import select

def rs485_socket_send(hexstr):
    """
    send data use Eth2RS485 by socket
    """
    timeout_in_seconds = 5

    rs485_socket = socket.socket()
    rs485_socket.connect(("192.168.0.7", 26))
    rs485_socket.setblocking(0)

    rs485_socket.sendall(hexstr)
    ready = select.select([rs485_socket], [], [], timeout_in_seconds)

    if ready[0]:
        print('have received data!')
        data = rs485_socket.recv(1024)
        ret_str = str(data)
        print('received ret_str:', ret_str)
        
    rs485_socket.close()


if __name__ == '__main__':
	power_1_close = '010500100000CC0F'
	power_1_open = '01050010FF008DFF'

	power_2_close = '020500100000CC3C'
	power_2_open = '02050010FF008DCC'


	power_1_close_hex = str2hexstr(power_1_close)
	power_1_open_hex = str2hexstr(power_1_open)
	power_2_close_hex = str2hexstr(power_2_close)
	power_2_open_hex = str2hexstr(power_2_open)


	rs485_socket_send(power_1_close_hex)
	rs485_socket_send(power_2_close_hex)

