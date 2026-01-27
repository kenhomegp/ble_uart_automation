import os
import ctypes
import platform

class Mcp2200:
    def __init__(self, PID=0x00da):
        self.vid = 0x04d8
        #self.pid = 0x00df
        #self.pid = 0x00da
        self.pid = int(PID, 16)

        self.checkOS = platform.system()

        if self.checkOS == "Windows":
            dir_path = os.path.dirname(os.path.realpath(__file__))
            print('Load MCP2200.dll. dir_path = {}'.format(dir_path))

            #self.dll = ctypes.WinDLL(os.getcwd() + '\\BLEAF\\MCP2200\\MCP2200.dll')
            self.dll = ctypes.WinDLL(dir_path + '\\MCP2200.dll')
            self.dll.InitMCP2200.argtype = [ctypes.c_uint,ctypes.c_uint]
            self.dll.InitMCP2200(self.vid, self.pid)

    def IsConnected(self):
        if self.checkOS == "Windows":
            self.dll.IsConnected.restype = ctypes.c_bool
            return self.dll.IsConnected()

    def ConfigureMCP2200(self, IOmap, BaudRate, RxLedMode, TxLedMode,
                         Flow=False, Uload=False, SSPND=False, Invert=False):

        self.dll.ConfigureMCP2200.argtype = [ctypes.c_ubyte,ctypes.c_ulong,ctypes.c_uint,ctypes.c_int,
                                             ctypes.c_bool,ctypes.c_bool,ctypes.c_bool,ctypes.c_bool]
        self.dll.ConfigureMCP2200.restype = ctypes.c_bool
        return self.dll.ConfigureMCP2200(IOmap,BaudRate,RxLedMode,TxLedMode,Flow,Uload,SSPND,Invert)

    def ConfigureIO(self, IOmap):
        '''
        :param IOmap:
            IOMap - a byte which represents a bitmap of the GPIO configuration
            a bit set to '1' will be a digital input
            a bit set to '0' will be a digital output
            MSB - - - - - - LSB
            GP7 GP6 GP5 GP4 GP3 GP2 GP1 GP0
        :return: True
        '''
        self.dll.ConfigureIO.argtype = ctypes.c_ubyte
        self.dll.ConfigureIO.restype = ctypes.c_bool
        return self.dll.ConfigureIO(IOmap)

    def SetPin(self, Pin):
        self.dll.SetPin.argtype = ctypes.c_int
        self.dll.SetPin.restype = ctypes.c_bool
        return self.dll.SetPin(Pin)

    def ClearPin(self,Pin):
        self.dll.ClearPin.argtype = ctypes.c_int
        self.dll.ClearPin.restype = ctypes.c_bool
        return self.dll.ClearPin(Pin)

    def ReadPinValue(self,Pin):
        self.dll.ReadPinValue.argtype = ctypes.c_int
        self.dll.ReadPinValue.restype = ctypes.c_int
        return self.dll.ReadPinValue(Pin)

    def Release(self):
        del self.dll
