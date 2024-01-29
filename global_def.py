import os
import sys
import socket
import fcntl
import struct

VERSION = '20240129_01'


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


root_dir = os.path.dirname(sys.modules['__main__'].__file__)
try:
    if get_ip_address('ppp0'):
        SWU_INSTALL_FOLDER = '/home/eduarts/ota_data_v1.0.0'
    else:
        SWU_INSTALL_FOLDER = '/home/{}/test_ota_data_v1.0.0'.format(os.getlogin())
except Exception as e:
    SWU_INSTALL_FOLDER = '/home/{}/test_ota_data_v1.0.0'.format(os.getlogin())

SOURCE_CODE_FOLDER_PREFIX = "EDB"
COMPANY_NAME = "Eudarts"

#INSTALL_FOLDER_NAME = "ota_data_v1.0.0"
#INSTALL_FOLDER_URI = "/home/" + os.getlogin() + "/" + INSTALL_FOLDER_NAME
#INSTALL_FOLDER_URI_BAK = root_dir


'''
Definitions of json

'''
