import os
import sys
import pytest
import time
from ..MCP2200.MCP2200 import Mcp2200
from .StationData import stationData

sd = stationData()

# Button control and LED Control
BTN_CTRL_PIN = 0x04
LED_IND_PIN_G = 0x03
LED_IND_PIN_R = 0x05
baudrate = '921600'

class IOControlLEDStatus:
    def __init__(self):
        self.driver = sd.mobile_driver

    def InitMCP2200(self, baudrate, mcu):
        if not mcu.IsConnected():
            print("The MCP2200 is disconnected")
            return False

        #                            I/O,Baudrate,RxLED,TxLED,Flow Control,ULOAD,SSPND
        #  if not mcu.ConfigureMCP2200((0xFF, baudrate_, 0, 0, flowctrl, False, False)):
        if not mcu.ConfigureMCP2200(0xFF, baudrate, 0, 0, Flow=True, Uload=False, SSPND=False, Invert=False):
            print("Configure MCP2200 failed")
            return False

        # set gp4 as output
        if not mcu.ConfigureIO(0xEF):
            print("Configure GPIO failed")
            return False
        else:
            print("Configure MCP2200 successfully")
        return True

    def ChecKLEDStatus(self, mcu):
        #mcu = Mcp2200()
        if not self.InitMCP2200(baudrate, mcu):
            sys.exit()
        rStatus = ''
        gStatus = ''
        count = 3
        while count > 0:
            gStatus += str(mcu.ReadPinValue(LED_IND_PIN_G))
            rStatus += str(mcu.ReadPinValue(LED_IND_PIN_R))
            count -= 1
            time.sleep(0.25)

        if gStatus == '101' or gStatus == '010':
            print("In advertising mode")
        elif gStatus == '111':
            print("In connected mode (a)")
        elif rStatus == '101' or rStatus == '010':
            print("In scan mode")
        elif rStatus == '111':
            print("In connected mode (s)")
        else:
            print("In unknown status: {0}".format(gStatus))

    def IOCtrl(self, mcu, io_pin, press_t):
        #mcu = Mcp2200()
        if not self.InitMCP2200(baudrate, mcu):
            sys.exit()
        if not mcu.ClearPin(io_pin) or mcu.ReadPinValue(io_pin) != 0:
            print("In Loop 1")
            print("Set GPIO {0} failed".format(io_pin))
            return False
        time.sleep(press_t)
        if not mcu.SetPin(io_pin) or mcu.ReadPinValue(io_pin) != 1:
            print("In Loop 2")
            print("Set GPIO {0} failed".format(io_pin))
            return False

    def Zephyr_InitMCP2200(self, baudrate, mcu):
        if not mcu.IsConnected():
            print("The MCP2200 is disconnected")
            return False

        #                            I/O,Baudrate,RxLED,TxLED,Flow Control,ULOAD,SSPND
        #  if not mcu.ConfigureMCP2200((0xFF, baudrate_, 0, 0, flowctrl, False, False)):
        if not mcu.ConfigureMCP2200(0xFF, baudrate, 0, 0, Flow=False, Uload=False, SSPND=False, Invert=False):
            print("Configure MCP2200 failed")
            return False

        status = self.Zephyr_IO_Initial(mcu)
        if status:
            print("Configure MCP2200 successfully")
            return True
        else:
            return False

    def Zephyr_IO_Initial(self, mcu):
        print('Zephyr_IO_Initial.')
        # set gp2,gp4 as output
        if not mcu.ConfigureIO(0xEB):
            print("Configure GPIO failed")
            return False
        else:
            print("Configure Zephyr_IO successfully")
            return True

    def Zephyr_IOCtrl(self, mcu, io_pin, press_t):
        #mcu = Mcp2200()
        #if not self.Zephyr_InitMCP2200('115200', mcu):
        #    sys.exit()
        if not mcu.ClearPin(io_pin) or mcu.ReadPinValue(io_pin) != 0:
            print("In Loop 1")
            print("Set GPIO {0} failed".format(io_pin))
            return False
        time.sleep(press_t)
        if not mcu.SetPin(io_pin) or mcu.ReadPinValue(io_pin) != 1:
            print("In Loop 2")
            print("Set GPIO {0} failed".format(io_pin))
            return False