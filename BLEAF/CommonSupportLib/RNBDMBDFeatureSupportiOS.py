import os
import sys
import serial
import serial.tools.list_ports
import time
import json
import pytest
import threading

from ..CommonSupportLib.StationData import stationData
from ..MCP2200.MCP2200 import Mcp2200
from . import android_locators as locators
from .BLEUARTFeatureSupportiOS import BLEUARTFeatureSupportiOS
from .AppScanAndConnect import ScanningandConnection
from . import ios_locators as ioslocators
from ..StationConfig import conf_file

sd = stationData()
com_port = conf_file.com_port
baud_rate = conf_file.baud_rate
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


class RNBDFeatureSupportiOS:
    def __init__(self, driver=sd.mobile_driver):
        self.thread = ""
        if not driver:
            sd = stationData()
            self.driver = sd.mobile_driver
            print("Driver-##############################################", self.driver)
        else:
            self.driver = driver
            print("Driver-##############################################", self.driver)
        self.bleuartfeatureiOS = BLEUARTFeatureSupportiOS()
        self.scanandconnect = ScanningandConnection()

    def testcase(self):
        self.testcasename = None

    def ComportSet(self, com_port, baud_rate):
        Com = str(com_port).upper()
        if not self.ComportCheck(Com):
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

    def rnbd_comport_set(self, comport, baudrates):
        Com = str(comport).upper()
        if not self.rnbd_comportcheck(Com):
            sys.exit()
        try:
            serial_port = serial.Serial(comport, baudrates, parity=serial.PARITY_NONE, timeout=0.10, xonxoff=1,
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

    def rnbd_comportcheck(self, comport):
        Com = str(comport).upper()
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

    def read_serial_port_data(self, ser, input_data):
        reading = ''
        print("read_serial_port")
        timeout = time.time() + 1.0
        while ser.inWaiting() or time.time() - timeout < 0.0:
            if ser.inWaiting() > 0:
                reading = ser.readline(ser.inWaiting()).decode()
                timeout = time.time() + 1.0
                print(reading)
        return reading

    def send_data_uart_ios(self, input_data):
        status = False
        TX_string = "[TX] - " + input_data
        result_status, pass_status = self.driver.find_element('XPATH', ioslocators.raw_data_log_message)
        assert result_status, "Failed to find the raw data log message"
        pass_status_get_text = self.driver.get_text(pass_status)
        if (TX_string in pass_status_get_text):
            print("TX input is matching. Data sent correctly")
            status = True
        else:
            status = False
            print("TX input is not matching. Data mismatch")
        return status

    def write_serial_port(self, ser, input_data):
        print("write_serial_port")
        input_data = bytes(input_data, encoding='utf-8')
        print(input_data)
        ser.write(input_data)

    def init_com_port(self, baud_rate):
        global serialPort
        print("Initialize com port")
        if not self.bleuartfeatureiOS.IniMCP2200(com_port, baud_rate):
            sys.exit()
        time.sleep(5)

    def rnbd_send_raw_data_uart_mode_app_to_dut_ios(self):
        input_data = "ABCDEFGHIJKLMNOPQ!@#$%^&*()\n"
        time.sleep(2)
        status, raw_text_field = self.driver.find_element('XPATH', ioslocators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        assert status, "Failed to find the raw data text field to input"
        serialPort = self.ComportSet(com_port, baud_rate)
        self.driver.send_keys(raw_text_field, input_data)
        read_data = self.read_serial_port_data(serialPort, input_data)
        print(read_data)
        time.sleep(5)
        status = self.send_data_uart_ios(input_data)
        assert status, "Test Fails as the comparison is not successful"
        if read_data in input_data:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        serialPort.close()
        return status

    def rnbd_send_raw_data_uart_mode_dut_to_app_ios(self):
        input_data = "ABCDEFGHIJKLMNOPQ!@#$%^&*()\n"
        time.sleep(2)
        serialPort = self.ComportSet(com_port, baud_rate)
        print("Checking for input string", input_data)
        self.write_serial_port(serialPort, input_data)
        time.sleep(5)
        result_status, pass_status = self.driver.find_element('XPATH', ioslocators.raw_data_log_message)
        assert result_status, "Failed to find the raw data log message"
        pass_status_get_text = self.driver.get_text(pass_status)
        if input_data in pass_status_get_text:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        serialPort.close()
        return status

    def rnbd_send_raw_data_uart_mode_app_to_dut_stress_test_ios(self, input_data):
        time.sleep(2)
        status, raw_text_field = self.driver.find_element('XPATH', ioslocators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        assert status, "Failed to find the raw data text field to input"
        serialPort = self.ComportSet(com_port, baud_rate)
        self.driver.send_keys(raw_text_field, input_data)
        read_data = self.read_serial_port_data(serialPort, input_data)
        print(read_data)
        time.sleep(5)
        status = self.send_data_uart_ios(input_data)
        assert status, "Test Fails as the comparison is not successful"
        if read_data in input_data:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        serialPort.close()
        return status

    def rnbd_send_raw_data_uart_mode_dut_to_app_stress_test_ios(self, input_data):
        serialPort = self.ComportSet(com_port, baud_rate)
        print("Checking for input string", input_data)
        self.write_serial_port(serialPort, input_data)
        time.sleep(5)
        result_status, pass_status = self.driver.find_element('XPATH', ioslocators.raw_data_log_message)
        assert result_status, "Failed to find the raw data log message"
        pass_status_get_text = self.driver.get_text(pass_status)
        time.sleep(5)
        status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.raw_clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        time.sleep(5)
        if input_data in pass_status_get_text:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        serialPort.close()
        return status

    def rnbd_uart_mode_data_transfer_ios(self, baudrates):
        print("Start the Data transfer from the DUT side <PC Tool>")
        status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.raw_clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        serialPort = self.rnbd_comport_set(com_port, baudrates)
        self.rnbd_TxEntry(serialPort, text_file)
        time.sleep(35)
        serialPort.close()

    def rnbd_app_uart_mode_data_transfer_ios(self, baudrates):
        serialPort = self.rnbd_comport_set(com_port, baudrates)
        print("Start the Data transfer from the App side")
        status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.raw_clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        self.thread = self.rnbd_RxEntry(serialPort)
        self.bleuartfeatureiOS.ios_data_transfer_START()
        time.sleep(55)
        self.rnbd_CloseSerialPort(serialPort)

    def rnbd_TxEntry(self, serialPort, textFile):
        print("TxEntry, file = " + textFile)
        textStr = self.bleuartfeatureiOS.LoadFile(textFile)
        print("send 500k")
        txSendData = textStr
        TxEnd = False
        BlockSize = int(block_size)
        info = [txSendData, TxEnd, BlockSize]
        while not TxEnd:
            TxEnd = self.bleuartfeatureiOS.RawDataTxSend(serialPort, info)
        else:
            print("End sending Tx data")

    def rnbd_RxEntry(self, Ser):
        print("New RxEntry")
        t = threading.Thread(target=self.rnbd_read_serial_port, args=(Ser,))
        t.start()
        return t

    def rnbd_CloseSerialPort(self, serialPort):
        print("CloseSerialPort")
        global flagReadSerialData
        #flagReadSerialData = False
        serialPort.close()

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
                    # print("500ms")
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
                text_file = open(os.getcwd() + '\\TextFiles\\' + '/Raw_data.txt', "w")
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

    def verify_rnbd_mode_uart_birectional_data_transfer_ios(self, baudrates):
        t3 = []
        serialPort = self.ComportSet(com_port, baudrates)
        time.sleep(5)
        status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        print("Start the Data transfer from the App side & DUT side <PC Tool> simultaneously")
        t0 = threading.Thread(target=self.rnbd_read_serial_port, args=(serialPort,))
        t0.start()
        t1 = threading.Thread(target=self.bleuartfeatureiOS.ios_data_transfer_START, args=())
        t2 = threading.Thread(target=self.rnbd_TxEntry, args=(serialPort, text_file,))
        t3.append(t1)
        t3.append(t2)
        # t1.start()
        # t2.start()
        for eachThread in t3:
            eachThread.start()
            eachThread.join()
        t0.join()
        time.sleep(50)
        self.rnbd_CloseSerialPort(serialPort)
        time.sleep(5)
        return receive_serial_str

    def rnbd_uart_mode_results_TX_display_ios(self):
        time.sleep(5)
        status, result_str = self.rnbd_uart_mode_results_TX_ios(receive_serial_str)
        return status, result_str

    def rnbd_uart_mode_results_TX_ios(self, msg):
        status = False
        message = ''
        result_str = "File transfer is complete."
        downlink_text = "Downlink: 500004 bytes"
        status, uart_TX_throughput_result = self.driver.find_element('XPATH', ioslocators.throughput_result_tx)
        assert status, "Failed to find element for UART TX throughput result"
        throughput_result_field = self.driver.get_text(uart_TX_throughput_result)
        throughput_value_TX = throughput_result_field.strip("Downlink:")
        status1, logmessage = self.driver.find_element('XPATH', ioslocators.logmessage)
        assert status1, "Failed to find log message"
        log_text = self.driver.get_text(logmessage)
        transmission_time_tx = ''
        if "Transmission elapsed time" in log_text:
            for line in log_text.split("\n"):
                if "Transmission elapsed time" in line:
                    transmission_time_tx = line.split("Transmission elapsed time = ")[1]
                    break
        else:
            print("Transmission time is not present in the log")
        fail_result = "UART Mode - Downlink test results (Mobile App to DUT):\nTest Failed with following data:\nTx Size, Time and Throughput: {time},{throughput}\n\n".format(
            time=transmission_time_tx, throughput=throughput_value_TX)
        if (result_str in log_text) and (downlink_text in log_text) and (msg == "Compare PASS"):
            message = "UART Mode - Downlink test results (Mobile App to DUT):\nTest Passed with following data:\nTx Size, Time and Throughput: {time},{throughput}\n\n".format(
                time=transmission_time_tx, throughput=throughput_value_TX)
            print(message)
            status = True
        else:
            print("Comparison Failed from the DUT side or matching string not found")
            message = fail_result
            print(message)
            status = False
        return status, message