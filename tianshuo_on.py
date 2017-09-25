
from utils import calc, str2hexstr, calc_modus_hex_str_to_send
import time
from rs485_socket import rs485_socket_send
#
#
off_1_output_hex = calc_modus_hex_str_to_send(1, 6, 0, 0, 0, 1)
# print('close_1_output_hex', off_1_output_hex)
# print('--------str2hexstr----------')
# str2hexstr('010600000001480a')
#
#rs485_socket_send(off_1_output_hex)
#
#
#
off_2_output_hex = calc_modus_hex_str_to_send(2, 6, 0, 0, 0, 1)
print('close_2_output_hex', off_2_output_hex)
#
#rs485_socket_send(off_2_output_hex)


on_1_output_hex = calc_modus_hex_str_to_send(1, 6, 0, 0, 0, 9)
print('open_1_output_hex', on_1_output_hex)

rs485_socket_send(on_1_output_hex)



on_2_output_hex = calc_modus_hex_str_to_send(2, 6, 0, 0, 0, 9)
print('open_2_output_hex', on_2_output_hex)

rs485_socket_send(on_2_output_hex)
