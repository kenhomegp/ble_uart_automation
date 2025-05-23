import os
import sys
import time
import json
import pytest
import threading
import serial

from ..CommonSupportLib.StationData import stationData
from ..MCP2200.MCP2200 import Mcp2200
from . import android_locators as locators
from .BLEUARTFeatureSupport import BLEUARTFeatureSupport
from .AppScanAndConnect import ScanningandConnection
from ..StationConfig import conf_file
from ..CommonSupportLib.Serial_Implementaiton import SerialSuppport
sd = stationData()

comport = conf_file.com_port
block_size = '4096'
global com
global baudrates
read_value = ''
q_receiveData = []
text_file = '500k'
text_file1 = '100k'
BTN_CTRL_PIN = 0x07
MCU = Mcp2200()
DUT_FLOW = False

didReceiveTextFile = False
flagReadSerialData = True
OverNightCounter = 0
receive_serial_str = ""
TestCaseRunning = ""

global serialPort
global maincommand


@pytest.fixture(scope="class", autouse=True)
def define_class_attributes(request, default_class_fixture):
    print("this is local specific class fixture")
    DUT_VID_PID_HEX = int("00DF", 16)
    request.cls.IniMCP2200 = Mcp2200(DUT_VID_PID_HEX)


    def class_finalizer():
        print("Local Class finalizer")
    request.addfinalizer(class_finalizer)


class RNBDFeatureSupport:
    def __init__(self, driver=sd.mobile_driver):
        self.thread = ""
        if not driver:
            sd = stationData()
            self.driver = sd.mobile_driver
            print("Driver-##############################################", self.driver)
        else:
            self.driver = driver
            print("Driver-##############################################", self.driver)
        self.bleuartfeature = BLEUARTFeatureSupport()
        self.scanandconnect = ScanningandConnection()
        self.serialdriver = SerialSuppport()

    def testcase(self):
        self.testcasename = None

    # def rnbd_comportcheck(self, comport):
        # Com = str(comport).upper()
        # comlist = serial.tools.list_ports.comports()
        # ComportList = []
        # for list_ in comlist:
            # str(list_)
            # ComportList.append(list_[0])

        # if Com not in ComportList:
            # print("Comport not found, please check the setting file")
            # return False
        # else:
            # return True

    # def rnbd_ComportSet(self, comport, baudrates):
        # Com = str(comport).upper()
        # if not self.rnbd_comportcheck(Com):
            # sys.exit()
        # try:
            # serial_port = serial.Serial(comport, baudrates, parity=serial.PARITY_NONE, timeout=0.10, xonxoff=1,
                                        # rtscts=1)
            # if not serial_port.isOpen():
                # print("Comport connect fail, please check the port status")
                # sys.exit()
            # else:
                # print("Comport is connected")
                # return serial_port
        # except(OSError, serial.SerialException):
            # print("Open comport fail, please checked {0} has release or not".format(Com))
            # sys.exit()

    def Send_Receive_Msg(self, comport, sendmsg, recmsg, timeout=1):
        result = ""
        timecnt = 0
        global com
        global baudrates

        if self.testcasename == "RNBD_Baudrate_115200_to_921600":
            baudrates = '115200'
        elif self.testcasename == "RNBD_Baudrate_921600":
            baudrates = '921600'
        elif self.testcasename == "RNBD_Baudrate_921600_to_115200_CHANGE":
            baudrates = '921600'
        elif self.testcasename == "RNBD_Baudrate_115200":
            baudrates = '115200'
        elif self.testcasename == "RNBD_Baudrate_115200_to_2400":
            baudrates = '115200'
        elif self.testcasename == "RNBD_Baudate_2400" or self.testcasename == "RNBD_Baudrate_2400_to_115200":
            baudrates = '2400'
        elif self.testcasename == "RNBD_MTP_Command_Test":
            baudrates = '115200'
        elif self.testcasename == "RNBD_115200_SET":
            baudrates = '115200'
        elif self.testcasename == "RNBD_Baudrate_115200_to_921600_SET":
            baudrates = '115200'
        elif self.testcasename == "RNBD_Conn_Interval_Param_Set1" or self.testcasename == "RNBD_Sleepmode_Enable_Test" or \
                self.testcasename == "RNBD_Sleepmode_Disable_Test" or self.testcasename == "RNBD_115200_Sleep_Mode":
            baudrates = '115200'
        elif self.testcasename == "RNBD_Sleepmode_Enable_command":
            baudrates = '115200'

        try:
            if self.serialdriver.ComportCheck(comport) == False:
                print('Com Port Connect fail , Please Check the Port status')
                return False

            com = self.serialdriver.ComportSet(comport, baudrates)
            if com.isOpen() == False:
                print('Com Port Connect fail , Please Check the Port status')
                time.sleep(1)
                return False
            else:
                while timecnt < timeout:
                    msg = sendmsg
                    com.write(msg)
                    time.sleep(3)
                    print('send command: ' + str(msg))
                    retrycnt = 0
                    while True:
                        count = com.inWaiting()
                        if count > 0:
                            data = com.read(count)
                            print("Actually receive:", data)
                            print("Need receive:", recmsg)
                            if data.find(recmsg) < 0:
                                print("result: Fail")
                                result = False
                            else:
                                print("result: Pass")
                                result = True
                            break
                        else:
                            retrycnt = retrycnt + 1
                            time.sleep(1)
                            if retrycnt > 3:
                                print("Fail to receive data")
                                result = False
                                break

                    if result == True:
                        break
                    else:
                        timecnt = timecnt + 1
                if com != None:
                    com.close()
                return result
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            if com != None:
                com.close()

    def Read_json_file(self, command_set):
        ret_str = ""
        step_result = []
        step_descript = []
        json_file = os.getcwd() + "\Tests\RNBD45x_JSON_File\RNBD45x_vs_Phone_Command_Set.json"
        with open(json_file) as f:
            testSet = json.load(f)
        f.close()
        self.testcasename = command_set
        print(command_set)
        testSet = testSet[command_set]
        for tc in testSet:
            for key, value in dict.items(tc):
                print("=========================================")
                print(str(dict.items(tc)))
                param_list = value.split("/")
                print(param_list)
                if len(param_list) == 2:
                    name = param_list[0]
                    time.sleep(int(param_list[1]))
                    print(name + ":" + str(param_list[1]) + "(seconds)")

                elif len(param_list) == 3:
                    name = param_list[0]
                    sendmsg = str(param_list[1]).encode()
                    needreceivemsg = str(param_list[2]).encode()

                    retcode = self.Send_Receive_Msg(comport, sendmsg, needreceivemsg)
                    print("retcode: " + str(retcode))

                elif len(param_list) == 4:
                    name = param_list[0]
                    sendmsg = str(param_list[1]).encode()
                    needreceivemsg = str(param_list[2]).encode()
                    timeout = int(param_list[3])
                    print(timeout)

                    retcode = self.Send_Receive_Msg(comport, sendmsg, needreceivemsg, timeout)
                    step_result.append(retcode)
                    print("retcode ", retcode)
                    if retcode == True:
                        step_descript.append(str(dict.items(tc)) + ": Pass \n")
                    else:
                        step_descript.append(str(dict.items(tc)) + ": Fail \n")

                elif len(param_list) == 5:
                    name = param_list[0]
                    sendmsg = str(param_list[1]).encode()
                    needreceivemsg = str(param_list[2]).encode()
                    timeout = int(param_list[3])
                    testlinkid = param_list[4]

                    retcode = self.Send_Receive_Msg(comport, sendmsg, needreceivemsg, timeout)
                    print("retcode: " + str(retcode))

        return step_result, step_descript

    def init_com_port(self, baud_rate):
        global serialPort
        print("Initialize com port")
        if not self.bleuartfeature.IniMCP2200(comport, baud_rate):
            sys.exit()
        time.sleep(5)

    def Parsingphyupdatestring(self, connection_log):
        count = 0
        global maincommand
        mystr = connection_log
        emptystr = []
        mainstr = ""
        print(emptystr)
        emptystr = mystr.split("%%")
        for eachele in emptystr:
            if "PHY_UPDATED" in eachele:
                status = True
                count += 1
                mainstr = eachele
                break
        maincommand = mainstr.replace("PHY_UPDATED", "MTP")
        print(maincommand)
        maincommand = maincommand[0:11]
        return (maincommand)

    def verify_rnbd_mode_uart_birectional_data_transfer(self, baudrates):
        t3 = []
        serialPort = self.serialdriver.ComportSet(comport, baudrates)
        time.sleep(5)
        status_clear, clear_text = self.driver.find_element('XPATH', locators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        print("Start the Data transfer from the App side & DUT side <PC Tool> simultaneously")
        t0 = threading.Thread(target=self.rnbd_read_serial_port, args=(serialPort,))
        t0.start()
        t1 = threading.Thread(target=self.bleuartfeature.data_transfer_START_mobile_app, args=())
        t2 = threading.Thread(target=self.bleuartfeature.TxEntry, args=(serialPort, text_file,))
        t3.append(t1)
        t3.append(t2)
        # t1.start()
        # t2.start()
        for eachThread in t3:
            eachThread.start()
            eachThread.join()
        t0.join()
        time.sleep(100)
        self.rnbd_CloseSerialPort(serialPort)
        time.sleep(5)
        return receive_serial_str

    def verify_rnbd_mode_uart_birectional_data_transfer_100k(self, baudrates):
        t3 = []
        serialPort = self.serialdriver.ComportSet(comport, baudrates)
        time.sleep(5)
        status_clear, clear_text = self.driver.find_element('XPATH', locators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        print("Start the Data transfer from the App side & DUT side <PC Tool> simultaneously")
        t0 = threading.Thread(target=self.rnbd_read_serial_port, args=(serialPort, q_receiveData,))
        t0.start()
        t1 = threading.Thread(target=self.bleuartfeature.data_transfer_START_mobile_app, args=())
        t2 = threading.Thread(target=self.bleuartfeature.TxEntry_100, args=(serialPort, text_file1,))
        t3.append(t1)
        t3.append(t2)
        # t1.start()
        # t2.start()
        for eachThread in t3:
            eachThread.start()
            eachThread.join()
        t0.join()
        time.sleep(75)
        self.rnbd_CloseSerialPort(serialPort)
        time.sleep(5)
        return receive_serial_str

    def rnbd_RxEntry(self, Ser):
        print("New RxEntry")
        #t = threading.Thread(target=self.rnbd_read_serial_port, args=(Ser, q_receiveData,))
        t = threading.Thread(target=self.rnbd_read_serial_port, args=(Ser,))
        t.start()
        return t

    #def rnbd_read_serial_port(self, ser, dat):
    def rnbd_read_serial_port(self, ser):
        global didReceiveTextFile
        global flagReadSerialData
        global receive_serial_str
        global TestCaseRunning

        emptyCount = 0
        time1 = 0.0
        time2 = 0.0
        #flagReadSerialData = True
        dat = []

        print("read_serial_port")
        while flagReadSerialData:
            while ser.in_waiting:
                num = ser.in_waiting
                reading = ser.read(num)

                if len(dat) == 0:
                    time1 = round(time.time() * 1000)

                dat.append(reading)

                if len(dat) != 0 and num != 0:
                    emptyCount = 1

            if len(dat) != 0 and emptyCount >= 1:
                time2 = round(time.time() * 1000)
                if (time2 - time1) > 500:
                    time1 = time2
                    emptyCount += 1

            if len(dat) != 0 and emptyCount > 5:
                emptyCount = 0
                uartData = bytearray()
                for dd in dat:
                    uartData += bytearray(dd)
                rxData = bytes(uartData)

                print("Data transmission timeout.")
                str1 = rxData.decode()
                size = str1[-7:-2]  # Get last data
                print(size)
                if size == "41667":
                    name = "500k.txt"
                elif size == "16667":
                    name = "200k.txt"
                elif size == "08334":
                    name = "100k.txt"

                file = open(os.getcwd() + '\\TextFiles\\' + name, 'rb')
                comp = file.read()
                file.close()
                text_file = open(os.getcwd() + '\\TextFiles\\'+'/Raw_data.txt', "w")
                text_file.write(str1)
                file.close()
                str2 = comp.decode()
                if str1 == str2:
                    print("Compare PASS")
                    receive_serial_str = "Compare PASS"
                    didReceiveTextFile = True
                else:
                    print("Compare FAIL")
                    receive_serial_str = "Compare FAIL"
                    didReceiveTextFile = False
                break

    def rnbd_CloseSerialPort(self, serialPort):
        print("CloseSerialPort")
        global flagReadSerialData
        #flagReadSerialData = False
        # self.thread.do_run = False
        # self.thread.join()
        serialPort.close()

    def rnbd_uart_mode_data_transfer(self, baudrates):
        print("Start the Data transfer from the DUT side <PC Tool>")
        status_clear, clear_text = self.driver.find_element('XPATH', locators.clear_text)
        time.sleep(3)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        serialPort = self.serialdriver.ComportSet(comport, baudrates)
        self.rnbd_TxEntry(serialPort, text_file)
        time.sleep(25)
        serialPort.close()

    def rnbd_app_uart_mode_data_transfer(self, baudrates):
        serialPort = self.serialdriver.ComportSet(comport, baudrates)
        print("Start the Data transfer from the App side")
        status_clear, clear_text = self.driver.find_element('XPATH', locators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        self.thread = self.rnbd_RxEntry(serialPort)
        self.bleuartfeature.data_transfer_START()
        time.sleep(75)
        self.rnbd_CloseSerialPort(serialPort)

    def rnbd_TxEntry(self, serialPort, textFile):
        print("TxEntry, file = " + textFile)
        textStr = self.bleuartfeature.LoadFile(textFile)
        print("send 500k")
        txSendData = textStr
        TxEnd = False
        BlockSize = int(block_size)
        info = [txSendData, TxEnd, BlockSize]
        while not TxEnd:
            TxEnd = self.bleuartfeature.RawDataTxSend(serialPort, info)
        else:
            print("End sending Tx data")

    def rnbd_uart_mode_results_TX(self, msg):
        status = False
        message = ''
        print(msg)
        result_str = "File Transfer is complete! 500k.txt\nBytes transferred = 500004"
        status, uart_TX_throughput_result = self.driver.find_element('XPATH', locators.uart_TX_throughput_result)
        assert status, "Failed to find element for UART TX throughput result"
        throughput_value_TX = self.driver.get_text(uart_TX_throughput_result)
        status1, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status1, "Failed to find the UART mode log message screen"
        log_text = self.driver.get_text(logmessage)
        fail_result = "UART Mode - Downlink test results (Mobile App to DUT):\nTest Failed with following data:\nTx Size, Time and Throughput: {}\n\n".format(
            throughput_value_TX)
        if (result_str in log_text) and (msg == "Compare PASS"):
            message = "UART Mode - Downlink test results (Mobile App to DUT):\nTest Passed with following data:\nTx Size, Time and Throughput: {}\n\n".format(
                throughput_value_TX)
            print(message)
            status = True
        else:
            print("Comparison Failed from the DUT side or matching string not found")
            message = fail_result
            print(message)
            status = False
        return status, message

    def rnbd_uart_mode_results_TX_display(self):
        time.sleep(5)
        status, result_str = self.rnbd_uart_mode_results_TX(receive_serial_str)
        return status, result_str

    def IOCtrl_Pull_Low(self, mcu, io_pin, press_t):
        if not mcu.ClearPin(io_pin) or mcu.ReadPinValue(io_pin) != 0:
            time.sleep(press_t)
            print("Set GPIO {0} failed".format(io_pin))
            return False
        else:
            time.sleep(press_t)
            print("Set GPIO {0} pass".format(io_pin))
            return True

    def IOCtrl_Pull_High(self, mcu, io_pin, press_t):
        if not mcu.SetPin(io_pin) or mcu.ReadPinValue(io_pin) != 1:
            time.sleep(press_t)
            print("Set GPIO {0} failed".format(io_pin))
            return False
        else:
            time.sleep(press_t)
            print("Set GPIO {0} pass".format(io_pin))
            return True

    def WakeupFromSleep(self, baudrates=115200):
        if not self.IniMCP2200(baudrates, MCU):
            print('w Configure DUT1 failed')
            return False
        else:
            self.IOCtrl_Pull_Low(MCU, BTN_CTRL_PIN, 0.2)
            print("[Wake up From Sleep][MCP2200]Press PB4 button")
            return True

    def SleepFromWakeup(self):
        self.IOCtrl_Pull_High(MCU, BTN_CTRL_PIN, 0.2)
        print("[Sleep From Wakeup][MCP2200]Press PB4 button")
        return True

    def IniMCP2200(self, baudrates, mcu):
        if not mcu.IsConnected():
            print('w The MCP2200 is disconnected')
            return False
        #                            I/O,Baudrate,RxLED,TxLED,Flow Control,ULOAD,SSPND
        #  if not mcu.ConfigureMCP2200((0xFF, baudrate_, 0, 0, flowctrl, False, False)):
        if not mcu.ConfigureMCP2200(0x7F, baudrates, 0, 0, Flow=True, Uload=False, SSPND=False, Invert=False):
            print('e Configure MCP2200 failed')
            return False
        # set gp7 as output
        if not mcu.ConfigureIO(0x7F):
            print('e Configure GPIO failed')
            return False
        else:
            print('i Configure MCP2200 successfully')
            return True

    def search_for_dut(self, dut_friendly_name):
        self.scanandconnect.click_start_scan()
        time.sleep(15)
        self.scanandconnect.click_cancel_button()
        status = self.driver.find_element('XPATH', locators.text_view_place_holder.format(
            dut_friendly_name))
        assert status, "Failed to find text view matching DUT name:{}".format(dut_friendly_name)
        return status

    def connect_ble_uart_dut(self, dut_friendly_name):
        status, dut_to_select = self.driver.find_element('XPATH', locators.text_view_place_holder.format(
            dut_friendly_name))
        assert status, "Failed to find text view matching DUT name:{}".format(dut_friendly_name)
        status = self.driver.click_element(dut_to_select)
        assert status, "Failed to click DUT name to pair"
