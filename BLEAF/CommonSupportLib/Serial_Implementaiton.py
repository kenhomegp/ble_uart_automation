import sys

from ..BaseWrappers.SerialDriver import SerialAccess
import serial
import serial.tools.list_ports
import re

class SerialSuppport:
    def __init__(self):
        '''
        Initialise serial port

        print('Connect to DUT Serial')

        self.dut_serial = SerialAccess(com_port, baud_rate)

    def open_serial_com_port(self):
        self.dut_serial.open_port()
        
    def close_serial_com_port(self):
        self.dut_serial.cleanup_for_exit()
        return True

    def verify_dut_started(self, profile):
        
        
        :param profile:
        :return:
        
        exp_profile_resp = "MEDC {} Profile".format(profile)
        resp = self.dut_serial.wait_for_resp(exp_resp="Reset complete", timeout_s=10)
        assert "TIMEOUT" not in resp, "MEDC DUT Not reset successfully. Response: {}".format(resp)
        assert exp_profile_resp in resp, "MEDC DUT Profile not correct. Expected: " \
                                         "{}, Actual: {}".format(exp_profile_resp, resp)
    '''

    def ComportSet(self, com_port, baud_rate):
        global serial_port
        Com = str(com_port).upper()
        if not self.ComportCheck(Com):
            print("sys exit")
            sys.exit()
        else:
            try:
                serial_port = serial.Serial(com_port, baud_rate, parity=serial.PARITY_NONE, timeout=0.10, xonxoff=1,
                                            rtscts=1)

                if not serial_port.isOpen():
                    print("Comport connect fail, please check the port status")
                    sys.exit()
                else:
                    print("Comport is connected")
                return serial_port
            except(OSError, serial.SerialException):
                print("Open comport fail, please checked {0} has release or not".format(Com))
                sys.exit()

    def ComportCheck(self, com_port):
        Com = str(com_port).upper()
        comlist = serial.tools.list_ports.comports()
        ComportList = []
        for list_ in comlist:
            str(list_)
            ComportList.append(list_[0])

        if Com not in ComportList:
            print("Comport not found, please check the setting file")
            return False
        else:
            return True
        