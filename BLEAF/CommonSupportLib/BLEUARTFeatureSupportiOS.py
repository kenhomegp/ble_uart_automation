import os
import sys
import threading
import time

import pytest
import serial
import serial.tools.list_ports
from appium.webdriver.common.appiumby import AppiumBy

from ..MCP2200.MCP2200 import Mcp2200
from . import android_locators as locators
from . import ios_locators as ioslocators
from .StationData import stationData

# Text for result strings for each mode
checksum_comparepass_text = "[TX] - Compare checksum : PASS"
loopback_comparepass_text = "Compare data: PASS"
fixed_pattern_comparepass_text = "[Fixed data pattern] - Compare data: PASS"
uart_comparepass_text = "UART UpLink: PASS"

text_500K = "500004"
text_100k = "100008"
text_fixed_pattern = "512000"
text_UART = "Uplink: 500004 bytes"

# Move to config file
#com_port = 'COM62'
com_port = '/dev/tty.usbmodem00098255751'
baud_rate = '921600'
block_size = '4096'
#text_file = '500k'
text_file = '1k'
text_file1 = '100k'
q_receiveData = []
serialPort = ""
result_string = ""

didReceiveTextFile = False
flagReadSerialData = True
OverNightCounter = 0
receive_serial_str = ""
TestCaseRunning = ""
sd = stationData()
result_str = ""

dut_friendly_name = "BLE_UART_0BC6"


class BLEUARTFeatureSupportiOS:
    def __init__(self, driver=sd.mobile_driver):
        self.thread = ""
        if not driver:
            sd = stationData()
            self.driver = sd.mobile_driver
            print("Driver-##############################################", self.driver)
        else:
            self.driver = driver
            print("Driver-##############################################", self.driver)

    def IniMCP2200(self, com_port, baud_rate):
        mcu = Mcp2200()
        if not mcu.IsConnected():
            print("The MCP2200 is disconnected")
            return False
        else:
            print("MCP2200 is connected")

        # I/O,Baudrate,RxLED,TxLED,Flow Control,ULOAD,SSPND
        if not mcu.ConfigureMCP2200(0xFF, baud_rate, 0, 0, Flow=True, Uload=False, SSPND=False, Invert=False):
            print("Configure MCP2200 failed")
            return False
        else:
            print("Configure MCP2200 successfully")
        return True

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

    def ComportSet(self, com_port, baud_rate):
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
            print("Open comport fail, please checked {0} has release or not".format(com_port))
            sys.exit()

        '''
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
        '''

    def initialize_com_port(self):
        global serialPort
        print ("Initialize com port")
        if not self.IniMCP2200(com_port, baud_rate):
            sys.exit()
        time.sleep(5)

    def read_serial_port_data(self, ser, input_data):
        reading =''
        print("read_serial_port")
        timeout = time.time() + 1.0
        while ser.inWaiting() or time.time() - timeout < 0.0:
            if ser.inWaiting() > 0:
                reading = ser.readline(ser.inWaiting()).decode()
                timeout = time.time() + 1.0
                print(reading)
        return reading

    def write_serial_port(self, ser, input_data):
        print("write_serial_port")
        input_data = bytes(input_data, encoding='utf-8')
        print(input_data)
        ser.write(input_data)

    def LoadFile(self, text_file):
        loadstr = ''
        #file = open(os.getcwd() + '\\TextFiles\\' + text_file + '.txt', 'rb')
        file = open(os.getcwd() + '/BLEAF/TextFiles/' + text_file + '.txt', 'rb')
        for line in file:
            loadstr += line.decode("utf-8")
        file.close()
        return loadstr

    def AddHciUartACLId(self, buf):
        # data = bytes(('02' + buf), encoding='utf-8')
        data = bytes(buf, encoding='utf-8')
        return data

    def RawDataTxSend(self, serialPort, info_, ):
        data_ = info_[0]
        blocksize = info_[2]
        i = 0
        tmp = ''
        while i < len(data_) and i < blocksize:
            tmp += data_[i]
            i += 1

        if i == len(data_):
            info_[1] = True
        else:
            info_[0] = data_[i:]
            info_[1] = False

        data = self.AddHciUartACLId(tmp)

        serialPort.write(data)
        # message('i <-- ' + tmp)
        return info_[1]

    def convert_lf_to_crlf(input_filepath, output_filepath):
        """
        Reads a file with LF line endings and writes it to a new file
        with CRLF line endings.

        Args:
            input_filepath (str): The path to the input file.
            output_filepath (str): The path to the output file.
        """
        try:
            with open(input_filepath, 'r', newline='') as infile:
                content = infile.read()

            # Replace all existing line endings with CRLF
            # First, normalize to LF, then replace LF with CRLF
            normalized_content = content.replace('\r\n', '\n').replace('\n', '\r\n')

            with open(output_filepath, 'w', newline='') as outfile:
                outfile.write(normalized_content)

            print(f"Successfully converted '{input_filepath}' to CRLF format in '{output_filepath}'")

        except FileNotFoundError:
            print(f"Error: File not found at '{input_filepath}'")
        except Exception as e:
            print(f"An error occurred: {e}")

    def ConvertTextFile(self):
        input_file = os.getcwd() + '/BLEAF/TextFiles/1k.txt'
        output_file = os.getcwd() + '/BLEAF/TextFiles/mac_1k.txt'
        self.convert_lf_to_crlf(input_file, output_file)
        print("ConvertTextFile.1k.txt")

    def TxEntry(self, serialPort, textFile):
        print("TxEntry, file = " + textFile)
        #self.ConvertTextFile()
        textStr = self.LoadFile(textFile)
        txSendData = textStr
        TxEnd = False
        BlockSize = int(block_size)
        info = [txSendData, TxEnd, BlockSize]
        print("Data len = {}".format(len(txSendData)))
        while not TxEnd:
            TxEnd = self.RawDataTxSend(serialPort, info)
        else:
            print("End sending Tx data")

    def TxEntry_100(self, serialPort, textFile1):
        print("TxEntry, file = " + textFile1)
        textStr = self.LoadFile(textFile1)
        txSendData = textStr
        TxEnd = False
        BlockSize = int(block_size)
        info = [txSendData, TxEnd, BlockSize]
        while not TxEnd:
            TxEnd = self.RawDataTxSend(serialPort, info)
        else:
            print("End sending Tx data")

    def read_serial_port(self, ser, dat):
        global didReceiveTextFile
        global flagReadSerialData
        global receive_serial_str
        global TestCaseRunning

        emptyCount = 0
        time1 = 0.0
        time2 = 0.0

        print("read_serial_port")
        time.sleep(10)
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

                print("Compared file = {}".format(name))
                #file = open(os.getcwd() + '\\TextFiles\\' + name, 'rb')
                file = open(os.getcwd() + '/BLEAF/TextFiles/' + name, 'rb')
                comp = file.read()
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

    def RxEntry(self, Ser):
        print("New RxEntry")
        t = threading.Thread(target=self.read_serial_port, args=(Ser, q_receiveData,))
        t.start()
        return t

    def CloseSerialPort(self, serialPort):
        print("CloseSerialPort")
        global flagReadSerialData
        flagReadSerialData = False
        serialPort.close()

    def close_mbd_app(self):
        self.driver.close_app(sd.config.ios_mbda_app_package)

    def verify_mode_checksum_ios(self):
        self.click_settings_icon_ios()
        time.sleep(5)
        self.change_mode_ios()
        time.sleep(5)
        print("Select checksum mode in settings")
        self.checksum_mode_ios()
        time.sleep(5)
        print("Select 500K file")
        self.ios_set_500K()
        time.sleep(5)

    def click_settings_icon_ios(self):
        status, start_scan_button = self.driver.find_element('XPATH', ioslocators.mbd_settings_icon)
        assert status, "Settings icon not found"
        status = self.driver.click_element(start_scan_button)
        assert status, "Failed to click on Settings icon"

    def change_mode_ios(self):
        status, change_mode_button = self.driver.find_element('XPATH', ioslocators.change_mode_icon)
        assert status, "Change mode icon not found"
        status = self.driver.click_element(change_mode_button)
        assert status, "Failed to click on change mode icon"

    def checksum_mode_ios(self):
        status, checksum_mode_button = self.driver.find_element('XPATH', ioslocators.demo_mode_checksum)
        assert status, "Checksum mode icon not found"
        status = self.driver.click_element(checksum_mode_button)
        assert status, "Failed to click on checksum mode icon"
        time.sleep(5)

    def loopback_mode_ios(self):
        status, loopback_mode_button = self.driver.find_element('XPATH', ioslocators.demo_mode_loopback)
        assert status, "Loopback mode icon not found"
        status = self.driver.click_element(loopback_mode_button)
        assert status, "Failed to click on loopback mode icon"
        time.sleep(5)

    def fixed_pattern_mode_ios(self):
        status, fixed_pattern_mode_button = self.driver.find_element('XPATH', ioslocators.demo_mode_fixed_pattern)
        assert status, "Fixed pattern mode icon not found"
        status = self.driver.click_element(fixed_pattern_mode_button)
        assert status, "Failed to click on fixed pattern mode icon"
        time.sleep(5)

    def uart_mode_ios(self):
        status, uart_mode_button = self.driver.find_element('XPATH', ioslocators.demo_mode_uart)
        assert status, "UART mode icon not found"
        status = self.driver.click_element(uart_mode_button)
        assert status, "Failed to click on UART mode icon"
        time.sleep(5)

    def ios_set_500K(self):
        status1, select_file = self.driver.find_element('XPATH', ioslocators.select_file)
        assert status1, "File selection icon not found"
        status1 = self.driver.click_element(select_file)
        assert status1, "Failed to click file select icon"
        time.sleep(5)
        status2, click_on_500K = self.driver.find_element('XPATH', ioslocators.select_500K_file)
        assert status2, "500K file not found"
        status2 = self.driver.click_element(click_on_500K)
        assert status2, "Failed to set 500K file"

    def switch_to_trcbp_ios(self):
        print("Switch to TRCBP profile")
        status, change_to_trcbp = self.driver.find_element('XPATH', ioslocators.TRCBP_icon)
        assert status, "TRCBP icon not found"
        status = self.driver.click_element(change_to_trcbp)
        assert status, "Failed to click on TRCBP icon"

    def save_settings_ios(self):
        status, save_settings = self.driver.find_element('XPATH', ioslocators.Done_icon)
        assert status, "Done icon not found"
        status = self.driver.click_element(save_settings)
        assert status, "Failed to click on Done icon"

    def clear_text_ios(self):
        status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"

    def confirm_checksum_mode_trcbp_ios(self):
        status = False
        checksum_comparepass_text_trcbp = "checksum ,Profile : TRCBP, Text file : 500k.txt"
        status, confirm_checksum_500K = self.driver.find_element('XPATH', ioslocators.confirm_modes)
        ble_data_value = self.driver.get_text(confirm_checksum_500K)
        if ble_data_value == checksum_comparepass_text_trcbp:
            print("Checksum mode, TRCBP and 500K is set accordingly")
        return status

    def confirm_checksum_mode_ios(self):
        status = False
        checksum_comparepass_text_trp = "checksum ,Profile : TRP, Text file : 500k.txt"
        status, confirm_checksum_500K = self.driver.find_element('XPATH', ioslocators.confirm_modes)
        ble_data_value = self.driver.get_text(confirm_checksum_500K)
        if status:
            if ble_data_value == checksum_comparepass_text_trp:
                print("Checksum mode, TRP, 500K is set accordingly")
                status = True
        return status

    def checksum_mode_data_transfer_ios(self):
        print("Start the Data transfer")
        self.ios_data_transfer_START()
        time.sleep(15)

    def loopback_mode_data_transfer_ios(self):
        print("Start the Data transfer")
        self.ios_data_transfer_START()
        #time.sleep(15)

    def ios_data_transfer_START(self):
        status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        time.sleep(1)
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        time.sleep(1)
        status, transfer_data = self.driver.find_element('XPATH', ioslocators.start_data_transfer)
        assert status, "START icon not found"
        status = self.driver.click_element(transfer_data)
        assert status, "Failed to transfer Data"
        #time.sleep(10)

    def checksum_mode_results_ios(self):
        result_status = False
        status, checksum_throughput_value = self.driver.find_element('XPATH', ioslocators.throughput_result_tx)
        assert status, "Failed to find locator for checksum throughput result"
        throughput_result_field = self.driver.get_text(checksum_throughput_value)
        throughput_value = throughput_result_field.strip("Downlink:")
        status1, logmessage = self.driver.find_element('XPATH', ioslocators.logmessage)
        assert status1, "Failed to find log message"
        log_text = self.driver.get_text(logmessage)
        transmission_time_tx = ''
        if "Transmission elapsed time" in log_text :
            for line in log_text.split("\n"):
                if "Transmission elapsed time" in line:
                    transmission_time_tx= line.split("Transmission elapsed time = ")[1]
                    break
        else :
            print("Transmission time is not present in the log")
        result_str = "Test Failed with following data:\nTx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_tx, throughput=throughput_value)
        if (text_500K in log_text) and (checksum_comparepass_text in log_text):  # To do Byte transfer and compare data size
            print("Checking if the transmitted file size matches 500004")
            result_str = "Checksum Mode Test results:\n Test Passed with following data:\nTx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_tx, throughput=throughput_value)
            result_status = True
            print(result_str)
        else:
            result_status = False
            print(result_str)
        return result_status, result_str

    def confirm_loopback_mode_trcbp_ios(self):
        status = False
        loopback_comparepass_text_trcbp = "loopback ,Profile : TRCBP, Text file : 500k.txt"
        status, confirm_loopback_500K_trcbp = self.driver.find_element('XPATH', ioslocators.confirm_modes)
        ble_data_value = self.driver.get_text(confirm_loopback_500K_trcbp)
        if ble_data_value == loopback_comparepass_text_trcbp:
            print("Loopback mode, TRCBP and 500K is set accordingly")
        return status

    def confirm_loopback_mode_ios(self):
        status = False
        loopback_comparepass_text_trp = "loopback ,Profile : TRP, Text file : 500k.txt"
        #status, confirm_loopback_500K = self.driver.find_element('XPATH', ioslocators.confirm_modes)
        status, confirm_loopback_500K = self.driver.find_element('XPATH', "//XCUIElementTypeStaticText[@label = \"Loopback,Profile : TRP, Text file: 500k.txt\"]")

        '''
        ble_data_value = self.driver.get_text(confirm_loopback_500K)
        if ble_data_value == loopback_comparepass_text_trp:
            print("Loopback mode, TRP and 500K is set accordingly")
        '''
        return status

    '''
    def loopback_mode_results_TX_ios(self):
        result_status = False
        status, loopback_throughput_value_TX = self.driver.find_element('XPATH', ioslocators.throughput_result_tx)
        assert status, "Failed to find locator for loopback throughput result"
        throughput_result_field = self.driver.get_text(loopback_throughput_value_TX)
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
        result_str_TX = "Test Failed with following data:\nTx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_tx, throughput=throughput_value_TX)
        if ((text_500K in log_text) and (loopback_comparepass_text in log_text)):
            result_str_TX = "Loopback Mode Test Results(TX):\nTest Passed with following data:\nTx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_tx, throughput=throughput_value_TX)
            result_status = True
            print(result_str_TX)
        else:
            result_status = False
            print(result_str_TX)
        return result_status, result_str_TX

    def loopback_mode_results_RX_ios(self):
        result_status = False
        status, loopback_throughput_value_RX = self.driver.find_element('XPATH', ioslocators.throughput_result_rx)
        assert status, "Failed to find locator for loopback throughput result"
        throughput_result_field = self.driver.get_text(loopback_throughput_value_RX)
        throughput_value_RX = throughput_result_field.strip("Uplink:")
        status1, logmessage = self.driver.find_element('XPATH', ioslocators.logmessage)
        assert status1, "Failed to find log message"
        log_text = self.driver.get_text(logmessage)
        transmission_time_rx = ''
        if "Transmission elapsed time" in log_text:
            for line in log_text.split("\n"):
                if "Transmission elapsed time" in line:
                    transmission_time_rx = line.split("Transmission elapsed time = ")[1]
                    break
        else:
            print("Transmission time is not present in the log")
        result_str_RX = "Test Failed with following data:\nRx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_rx, throughput=throughput_value_RX)
        if ((text_500K in log_text) and (loopback_comparepass_text in log_text)):
            print("Checking if the Received file size matches 500004")
            result_str_RX = "Loopback Mode Test Results(RX):\nTest Passed with following data:\nRx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_rx, throughput=throughput_value_RX)
            result_status = True
            print(result_str_RX)
        else:
            result_status = False
            print(result_str_RX)
        return result_status, result_str_RX
    '''
    def loopback_mode_results_TX_ios(self):
        result_status = False
        status, loopback_throughput_value_TX = self.driver.find_element('XPATH', ioslocators.throughput_result_tx)
        assert status, "Failed to find locator for loopback throughput result"
        throughput_result_field = self.driver.get_text(loopback_throughput_value_TX)
        throughput_value_TX = throughput_result_field.strip("Downlink:")
        status1, logmessage = self.driver.find_element('XPATH', ioslocators.logmessage)
        assert status1, "Failed to find log message"
        log_text = self.driver.get_text(logmessage)
        transmission_time_tx = ''
        #if "Transmission elapsed time" in log_text:
        if "Downlink transmission time" in log_text:
            for line in log_text.split("\n"):
                #if "Transmission elapsed time" in line:
                if "Downlink transmission time" in line:
                    #transmission_time_tx = line.split("Transmission elapsed time = ")[1]
                    transmission_time_tx = line.split("Downlink transmission time = ")[1]
                    break
        else:
            print("Transmission time is not present in the log")
        result_str_TX = "Test Failed with following data:\nTx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_tx, throughput=throughput_value_TX)
        #if ((text_500K in log_text) and (loopback_comparepass_text in log_text)):
        if (("Downlink: 500004 bytes" in log_text) and ("Compare data: PASS" in log_text)):
            result_str_TX = "Loopback Mode Test Results(TX):\nTest Passed with following data:\nTx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_tx, throughput=throughput_value_TX)
            result_status = True
            print(result_str_TX)
        else:
            result_status = False
            print(result_str_TX)
        return result_status, result_str_TX

    def loopback_mode_results_RX_ios(self):
        result_status = False
        status, loopback_throughput_value_RX = self.driver.find_element('XPATH', ioslocators.throughput_result_rx)
        assert status, "Failed to find locator for loopback throughput result"
        throughput_result_field = self.driver.get_text(loopback_throughput_value_RX)
        throughput_value_RX = throughput_result_field.strip("Uplink:")
        status1, logmessage = self.driver.find_element('XPATH', ioslocators.logmessage)
        assert status1, "Failed to find log message"
        log_text = self.driver.get_text(logmessage)
        transmission_time_rx = ''
        #if "Transmission elapsed time" in log_text:
        if "Uplink transmission time" in log_text:
            for line in log_text.split("\n"):
                #if "Transmission elapsed time" in line:
                if "Uplink transmission time" in line:
                    #transmission_time_rx = line.split("Transmission elapsed time = ")[1]
                    transmission_time_rx = line.split("Uplink transmission time = ")[1]
                    break
        else:
            print("Transmission time is not present in the log")
        result_str_RX = "Test Failed with following data:\nRx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_rx, throughput=throughput_value_RX)
        #if ((text_500K in log_text) and (loopback_comparepass_text in log_text)):
        if (("Uplink: 500004 bytes" in log_text) and ("Compare data: PASS" in log_text)):
            print("Checking if the Received file size matches 500004")
            result_str_RX = "Loopback Mode Test Results(RX):\nTest Passed with following data:\nRx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_rx, throughput=throughput_value_RX)
            result_status = True
            print(result_str_RX)
        else:
            result_status = False
            print(result_str_RX)
        return result_status, result_str_RX

    def verify_mode_loopback_ios(self):
        self.click_settings_icon_ios()
        #time.sleep(1)
        self.change_mode_ios()
        #time.sleep(5)
        print("Select loopback mode in settings")
        self.loopback_mode_ios()
        #time.sleep(5)
        print("Select 500K file")
        self.ios_set_500K()
        #time.sleep(5)
        print("Skip the timeout value")
        #self.set_receive_timeout_ios()

    def confirm_fixed_pattern_mode_ios(self):
        status = False
        fixed_pattern_comparepass_text_trp = "Fixed pattern,Profile : TRP, Text file : 500k.txt"
        status, confirm_fixed_pattern = self.driver.find_element('XPATH', ioslocators.confirm_modes)
        ble_data_value = self.driver.get_text(confirm_fixed_pattern)
        if ble_data_value == fixed_pattern_comparepass_text_trp:
            print("Fixed pattern mode, TRP and 500K is set accordingly")
        return status

    def confirm_fixed_pattern_mode_trcbp_ios(self):
        status = False
        fixed_pattern_comparepass_text_trcbp = "Fixed pattern,Profile : TRCBP, Text file : 500k.txt"
        status, confirm_fixed_pattern_500K_trcbp = self.driver.find_element('XPATH', ioslocators.confirm_modes)
        ble_data_value = self.driver.get_text(confirm_fixed_pattern_500K_trcbp)
        if ble_data_value == fixed_pattern_comparepass_text_trcbp:
            print("Fixed pattern mode, TRCBP and 500K is set accordingly")
        return status

    def confirm_uart_mode_ios(self):
        status = False
        uart_comparepass_text_trp = "UART ,Profile : TRP, Text file : 500k.txt"
        status, confirm_uart_500k = self.driver.find_element('XPATH', ioslocators.confirm_modes)
        ble_data_value = self.driver.get_text(confirm_uart_500k)
        if ble_data_value == uart_comparepass_text_trp:
            print("UART mode, TRP is set accordingly")
        return status

    def confirm_uart_mode_trcbp_ios(self):
        status = False
        uart_comparepass_text_trcbp = "UART ,Profile : TRCBP, Text file : 500k.txt"
        status, confirm_uart_500k_trcbp = self.driver.find_element('XPATH', ioslocators.confirm_modes)
        ble_data_value = self.driver.get_text(confirm_uart_500k_trcbp)
        if ble_data_value == uart_comparepass_text_trcbp:
            print("UART mode, TRCBP, 500K is set accordingly")
        return status

    def fixed_pattern_mode_data_transfer_ios(self):
        print("Start the Data transfer")
        self.ios_data_transfer_START()
        time.sleep(10)

    def fixed_pattern_mode_results_RX_ios(self):
        result_status = False
        status, fixed_pattern_RX_throughput_result = self.driver.find_element('XPATH', ioslocators.throughput_result_rx)
        assert status, "Failed to find the fixed pattern locator"
        throughput_result_field = self.driver.get_text(fixed_pattern_RX_throughput_result)
        throughput_value_RX = throughput_result_field.strip("Uplink:")
        status1, logmessage = self.driver.find_element('XPATH', ioslocators.logmessage)
        assert status1, "Failed to find log message"
        log_text = self.driver.get_text(logmessage)
        transmission_time_rx = ''
        if "Transmission elapsed time" in log_text:
            for line in log_text.split("\n"):
                if "Transmission elapsed time" in line:
                    transmission_time_rx = line.split("Transmission elapsed time = ")[1]
                    break
        else:
            print("Transmission time is not present in the log")
        fail_result = "Test Failed with following data:\nRx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_rx, throughput=throughput_value_RX)
        if (text_fixed_pattern in log_text) and (fixed_pattern_comparepass_text in log_text):
            print("Checking if the Received file size matches 512000")
            print("In the loop")
            result_status = True
            result_str = "Fixed Pattern Mode Test Results: \nTest Passed with following data:\nRx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_rx, throughput=throughput_value_RX)
            print(result_str)
        else:
            result_status = False
            result_str = fail_result
            print(result_str)
        return result_status, result_str

    def verify_mode_fixed_pattern_ios(self):
        self.click_settings_icon_ios()
        time.sleep(5)
        self.change_mode_ios()
        time.sleep(5)
        print("Select Fixed pattern mode in settings")
        self.fixed_pattern_mode_ios()
        time.sleep(5)
        print("Select 500K file")
        self.ios_set_500K()
        time.sleep(5)

    def verify_mode_uart_ios(self):
        self.click_settings_icon_ios()
        time.sleep(2)
        print("Select UART mode")
        self.change_mode_ios()
        time.sleep(2)
        self.uart_mode_ios()
        time.sleep(2)
        print("Select 500K file")
        self.ios_set_500K()
        time.sleep(2)
        self.set_receive_timeout_ios()
        time.sleep(2)

    def uart_mode_data_transfer_from_ios_app(self):
        serialPort = self.ComportSet(com_port, baud_rate)
        print("Start the Data transfer from the App side")
        status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        self.thread = self.RxEntry(serialPort)
        self.ios_data_transfer_START()
        time.sleep(120)
        self.CloseSerialPort(serialPort)

    def uart_mode_results_TX_display_ios(self):
        time.sleep(5)
        status, result_str = self.uart_mode_results_TX_ios(receive_serial_str)
        print(receive_serial_str)
        return status, result_str

    def uart_mode_results_TX_ios(self, msg):
        status = False
        message = ''
        result_str = "File transfer is complete!, Total Bytes transfer = 500004"
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
        fail_result = "UART Mode - Downlink test results (Mobile App to DUT):\nTest Failed with following data:\nTx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_tx, throughput=throughput_value_TX)
        if (result_str in log_text) and (msg == "Compare PASS"):
            message = "UART Mode - Downlink test results (Mobile App to DUT):\nTest Passed with following data:\nTx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_tx, throughput=throughput_value_TX)
            print(message)
            status = True
        else:
            print("Comparison Failed from the DUT side or matching string not found")
            message = fail_result
            print(message)
            status = False
        return status, message

    def uart_mode_results_RX_ios(self):
        status = False
        result_str = ""
        status, uart_RX_throughput_result = self.driver.find_element('XPATH', ioslocators.throughput_result_rx)
        assert status, "Failed to find the locator for UART RX throughput result"
        throughput_result_field = self.driver.get_text(uart_RX_throughput_result)
        throughput_value_RX = throughput_result_field.strip("Uplink:")
        status1, logmessage = self.driver.find_element('XPATH', ioslocators.logmessage)
        assert status1, "Failed to find log message"
        log_text = self.driver.get_text(logmessage)
        transmission_time_rx = ''
        if "Transmission elapsed time" in log_text:
            for line in log_text.split("\n"):
                if "Transmission elapsed time" in line:
                    transmission_time_rx = line.split("Transmission elapsed time = ")[1]
        else:
            print("Transmission time is not present in the log")
        fail_result = "UART Mode - Uplink Test Results\nTest Failed with following data:\nRx Size, Time and Throughput: {time},{throughput}\n\n".format(time=transmission_time_rx, throughput=throughput_value_RX)
        if (uart_comparepass_text in log_text) and (text_UART in log_text):
            result_str = "UART Mode - Uplink Test Results (DUT to Mobile App):\nTest Passed with following data:\nRx Size, Time and Throughput: {time},{throughput}\n\n".format(time=transmission_time_rx, throughput=throughput_value_RX)
            print(result_str)
            status = True
        else:
            status = False
            result_str = fail_result
            print(result_str)
        return status, result_str

    def dut_uart_mode_data_transfer_ios(self):
        print("Start the Data transfer from the DUT side <PC Tool>")
        serialPort = self.ComportSet(com_port, baud_rate)
        self.TxEntry(serialPort, text_file)
        time.sleep(25)
        serialPort.close()

    def verify_mode_uart_birectional_data_transfer_ios(self):
        t3 = []
        serialPort = self.ComportSet(com_port, baud_rate)
        time.sleep(5)
        #status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.clear_text)
        #assert status_clear, "Failed to find the clear icon"
        #status_clear = self.driver.click_element(clear_text)
        #assert status_clear, "Failed to click on clear icon"
        print("Start the Data transfer from the App side & DUT side <PC Tool> simultaneously")
        #t0 = threading.Thread(target=self.read_serial_port, args=(serialPort, q_receiveData,))
        #t0.start()
        #t1 = threading.Thread(target=self.ios_data_transfer_START, args=())
        t2 = threading.Thread(target=self.TxEntry, args=(serialPort, text_file,))
        #t3.append(t1)
        t3.append(t2)
        for eachThread in t3:
            eachThread.start()
            eachThread.join()
        #t0.join()
        print("Sleep 75 ")
        time.sleep(75)
        self.CloseSerialPort(serialPort)
        time.sleep(5)
        return receive_serial_str

    def data_transfer_START_mobile_app_ios(self):
        status, transfer_data = self.driver.find_element('XPATH', ioslocators.start_data_transfer)
        assert status, "START icon not found"
        status = self.driver.click_element(transfer_data)
        assert status, "Failed to transfer Data"

    def enable_write_with_response_ios(self):
        print("Enable write with response")
        status1, enable = self.driver.find_element('XPATH', ioslocators.write_with_response_icon)
        assert status1, "Write with response icon not found"
        status1 = self.driver.click_element(enable)
        assert status1, "Failed to enable Write with response"

    def start_stop_data_transfer_ios(self):
        print("Start the Data transfer")
        status, transfer_data = self.driver.find_element('XPATH', ioslocators.start_data_transfer)
        assert status, "START icon not found"
        status = self.driver.click_element(transfer_data)
        assert status, "Failed to transfer Data"
        # time.sleep(1)
        print("Stop the Data transfer")
        status, stop_transfer = self.driver.find_element('XPATH', ioslocators.stop_data_transfer)
        assert status, "STOP icon not found"
        status = self.driver.click_element(stop_transfer)
        assert status, "Failed to Stop Data Transfer"
        time.sleep(5)

    def stop_data_transfer_results_ios(self):
        status = True
        result_str = "File transfer is complete!, Total Bytes transfer = 500004"
        status, logmessage = self.driver.find_element('XPATH', ioslocators.logmessage)
        assert status, "Failed to find the UART mode log message screen"
        log_text = self.driver.get_text(logmessage)
        fail_result = "File Transfer is complete! 500k.txt"
        if result_str not in log_text:
            result_str = "Data transmission stopped. Zero bytes transferred."
            print("The data transfer has stopped accordingly")
            return status, result_str
        else:
            status = False
        return status, fail_result

    def verify_mode_100K_uart_ios(self):
        self.click_settings_icon_ios()
        time.sleep(5)
        print("Select UART mode")
        self.change_mode_ios()
        time.sleep(5)
        self.uart_mode_ios()
        time.sleep(5)
        print("Select 100K file")
        self.ios_set_100K()
        time.sleep(5)

    def ios_set_100K(self):
        status1, select_file = self.driver.find_element('XPATH', ioslocators.select_file)
        assert status1, "File selection icon not found"
        status1 = self.driver.click_element(select_file)
        assert status1, "Failed to click file select icon"
        time.sleep(5)
        status2, click_on_100K = self.driver.find_element('XPATH', ioslocators.select_100K_file)
        assert status2, "100K file not found"
        status2 = self.driver.click_element(click_on_100K)
        assert status2, "Failed to set 100K file"

    def ios_confirm_uart_mode_100k_trcbp(self):
        status = False
        status, confirm_uart = self.driver.find_element('XPATH', locators.confirm_uart_trcbp_100k)
        if status:
            status = self.driver.is_visible(confirm_uart)
            print("UART mode, TRCBP, 100K is set accordingly")
        return status

    def dut_uart_mode_100k_data_transfer_ios(self):
        print("Start the Data transfer from the DUT side <PC Tool>")
        serialPort = self.ComportSet(com_port, baud_rate)
        status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        self.TxEntry_100(serialPort, text_file1)
        time.sleep(25)
        serialPort.close()

    def uart_mode_results_100k_RX_ios(self):
        status = False
        result_str = ""
        status, uart_RX_throughput_result = self.driver.find_element('XPATH', ioslocators.throughput_result_rx)
        assert status, "Failed to find the locator for UART RX throughput result"
        throughput_result_field = self.driver.get_text(uart_RX_throughput_result)
        throughput_value_RX = throughput_result_field.strip("Uplink:")
        status1, logmessage = self.driver.find_element('XPATH', ioslocators.logmessage)
        assert status1, "Failed to find log message"
        log_text = self.driver.get_text(logmessage)
        transmission_time_rx = ''
        if "Transmission elapsed time" in log_text:
            for line in log_text.split("\n"):
                if "Transmission elapsed time" in line:
                    transmission_time_rx = line.split("Transmission elapsed time = ")[1]
        else:
            print("Transmission time is not present in the log")
        fail_result = "UART Mode - Uplink Test Results\nTest Failed with following data:\nRx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_rx, throughput=throughput_value_RX)
        if (uart_comparepass_text in log_text) and (text_100k in log_text):
            print("In the loop")
            result_str = "UART Mode - Uplink Test Results (DUT to Mobile App):\nTest Passed with following data:\nRx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_rx, throughput=throughput_value_RX)
            print(result_str)
            status = True
        else:
            status = False
            result_str = fail_result
            print(result_str)
        return status, result_str

    def uart_mode_results_100k_TX_display_ios(self):
        time.sleep(5)
        status, result_str = self.uart_mode_results_TX_100_ios(receive_serial_str)
        return status, result_str

    def uart_mode_results_TX_100_ios(self, msg):
        status = False
        message = ''
        print("printing msg", msg)
        result_str = "File transfer is complete!, Total Bytes transfer = 100008"
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
        fail_result = "UART Mode - Downlink test results (Mobile App to DUT):\nTest Failed with following data:\nTx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_tx, throughput=throughput_value_TX)
        if (result_str in log_text) and (msg == "Compare PASS"):
            message = "UART Mode - Downlink test results (Mobile App to DUT):\nTest Passed with following data:\nTx Size, Time and Throughput: {file_size},{time},{throughput}\n\n".format(file_size= "500004 B", time=transmission_time_tx, throughput=throughput_value_TX)
            print(message)
            status = True
        else:
            print("Comparison Failed from the DUT side or matching string not found")
            message = fail_result
            print(message)
            status = False
        return status, message

    def confirm_100k_uart_mode_ios(self):
        status = False
        uart_comparepass_text_100K = "UART ,Profile : TRCBP, Text file : 500k.txt"
        status, confirm_uart_100k = self.driver.find_element('XPATH', ioslocators.confirm_modes)
        ble_data_value = self.driver.get_text(confirm_uart_100k)
        if ble_data_value == uart_comparepass_text_100K:
            print("UART mode, TRCBP, 500K is set accordingly")
        return status

    def verify_ios_app_open(self):
        status = False
        status, dashboard_text = self.driver.find_element('XPATH', ioslocators.dashboard_text)
        if status:
            status = self.driver.is_visible(dashboard_text)
            print("MBD Application opened.")
        return status

    def ios_scan_and_connect_dut(self, dut_friendly_name):
        self.ios_open_ble_uart_scanner()
        time.sleep(15)
        self.ios_search_and_select_dut(dut_friendly_name)

    def ios_connect_and_disconnect_dut(self, dut_friendly_name):
        self.ios_search_and_select_dut(dut_friendly_name)
        print("Verifying the connection stability for 2 minutes")
        # Adding delay of 120 secs
        time.sleep(120)
        status = self.ios_verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        print("Disconnect the DUT")
        self.status, back_button = self.driver.find_element('XPATH', ioslocators.back_button)
        assert status, "Failed to find back icon"
        status = self.driver.click_element(back_button)
        assert status, "Failed to click on back icon"
        print("Verifying the disconnection status for 1 minute")
        # Adding delay of 60 secs
        time.sleep(60)

    def ios_open_ble_uart_scanner(self):
        error_msg = ""
        time.sleep(2)
        print("Click BLE Uart\n\n")
        status, ble_uart_icon = self.driver.find_element('XPATH', ioslocators.ble_uart_icon)
        assert status, "BLE Uart Icon not found"
        time.sleep(1)
        status = self.driver.click_element(ble_uart_icon)
        assert status, "Failed to open BLE Uart page"
        time.sleep(1)
        status, device_scanner = self.driver.find_element('XPATH', ioslocators.device_scanner)
        assert status, "PIC32CXBZ option not found"
        time.sleep(1)
        status = self.driver.click_element(device_scanner)
        assert status, "Failed to open BLE Uart page"
        time.sleep(1)
        status, scan_button = self.driver.find_element('XPATH', ioslocators.start_scan_button)
        assert status, "Start button not found"
        time.sleep(1)
        status = self.driver.click_element(scan_button)
        assert status, "Failed to open scan page"

    def ios_click_start_scan(self):
        status, start_scan_button = self.driver.find_element('XPATH', ioslocators.start_scan_button)
        assert status, "Scan button not found"
        status = self.driver.click_element(start_scan_button)
        assert status, "Failed to click start scan button on screen"

    def ios_search_and_select_dut(self, dut_friendly_name):
        status, dut_to_select = self.driver.find_element('XPATH', ioslocators.text_view_place_holder.format(dut_friendly_name))
        assert status, "Failed to find text view matching DUT name:{}".format(dut_friendly_name)
        status = self.driver.click_element(dut_to_select)
        assert status, "Failed to click DUT name to pair"

    def ios_verify_dut_name_visibility(self,dut_friendly_name):
        status = False
        status, dut_name = self.driver.find_element('XPATH', ioslocators.dut_name.format(dut_friendly_name))
        assert status, "Failed to find dut name locator"
        status = self.driver.is_visible(dut_name)
        if status:
            status = True
        else:
            assert status, "DUT is not connected"
        return status

    def ios_verify_scan_page_visiblity(self):
        status = False
        status, scan_page = self.driver.find_element('XPATH', ioslocators.scan_button)
        assert status, "Failed to find the scan icon element in the mobile app"
        status = self.driver.is_visible(scan_page)
        if status:
            print("SCAN page is visible")
        else:
            assert status, "SCAN page is not visible"
        return status

    def ios_verify_ota_scan_page_visiblity(self):
        status = False
        status, scan_page = self.driver.find_element('XPATH', ioslocators.ota_scan_button)
        assert status, "Failed to find the scan icon element in the mobile app"
        status = self.driver.is_visible(scan_page)
        if status:
            print("SCAN page is visible")
        else:
            assert status, "SCAN page is not visible"
        return status

    def verify_raw_data_mode_ios(self):
        status, text_mode_icon = self.driver.find_element('XPATH', ioslocators.raw_data_icon)
        assert status, "Failed to find the raw data icon"
        status = self.driver.click_element(text_mode_icon)
        assert status, "Failed to click on the raw data icon"
        #time.sleep(10)

    def confirm_raw_data_mode_trcbp_ios(self):
        status = False
        status, confirm_raw_trcbp = self.driver.find_element('XPATH', ioslocators.confirm_raw_data_trcbp)
        if status:
            status = self.driver.is_visible(confirm_raw_trcbp)
            print("Raw data - TRCBP is set accordingly")
        return status
    def confirm_raw_data_mode_trp_ios(self):
        status = False
        status, confirm_raw_trp = self.driver.find_element('XPATH', ioslocators.confirm_raw_data_trp)
        if status:
            status = self.driver.is_visible(confirm_raw_trp)
            print("Raw data - TRP is set accordingly")
        return status
    def switch_raw_data_to_burst_mode_ios(self):
        status, burst_mode_icon = self.driver.find_element('XPATH', ioslocators.burst_mode_icon)
        assert status, "Failed to find the burst mode icon"
        status = self.driver.click_element(burst_mode_icon)
        assert status, "Failed to switch to burst mode icon from text mode"
        time.sleep(5)

    def confirm_raw_data_loopbackmode_trp_ios(self):
        status = False
        status, confirm_raw_loopback = self.driver.find_element('XPATH', ioslocators.raw_data_loopback_confirm_trp)
        if status:
            status = self.driver.is_visible(confirm_raw_loopback)
            print("Raw data, TRP - Loopback mode is set accordingly")
        return status

    def confirm_raw_data_loopbackmode_trcbp_ios(self):
        status = False
        status, confirm_raw_loopback = self.driver.find_element('XPATH', ioslocators.raw_data_loopback_confirm_trcbp)
        if status:
            status = self.driver.is_visible(confirm_raw_loopback)
            print("Raw data, TRCBP - Loopback mode is set accordingly")
        return status
		
    def send_raw_data_loopback_mode_ios(self):
        input_data0 = "RAW Data Tests"
        input_data1 = "1234567890"
        input_data2 = "ABCDEFGHIJKLMNOPQ!@#$%^&*()\n"
        input_data3 = "Areyoulookingforonlinereadingactivities?\
                       Howaboutinteractivepracticeactivitiestargetingspecificreadingskills?"
        input_data4 = "BLE UART Feature RAW DATA"
        status, raw_text_field = self.driver.find_element('XPATH', ioslocators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        assert status, "Failed to find the raw data text field to input"
        self.driver.send_keys(raw_text_field, input_data2)
        time.sleep(2)
        status = self.send_data_ios(input_data2)
        assert status, "Test Fails as the comparison is not successful"
        return status
    def send_raw_data_loopback_mode_stresstest_ios(self, input_data):
        time.sleep(2)
        status, raw_text_field = self.driver.find_element('XPATH', ioslocators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        assert status, "Failed to find the raw data text field to input"
        self.driver.send_keys(raw_text_field, input_data)
        time.sleep(5)
        status = self.send_data_ios(input_data)
        assert status, "Test Fails as the comparison is not successful"
        time.sleep(5)
        status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.raw_clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        return status
    def confirm_raw_data_uart_trp_ios(self):
        status = False
        status, confirm_raw_uart = self.driver.find_element('XPATH', ioslocators.raw_data_uart_confirm_trp)
        if status:
            status = self.driver.is_visible(confirm_raw_uart)
            print("Raw data - UART mode, TRP is set accordingly")
        return status

    def confirm_raw_data_uart_trcbp_ios(self):
        status = False
        status, confirm_raw_uart = self.driver.find_element('XPATH', ioslocators.raw_data_uart_confirm_trcbp)
        if status:
            status = self.driver.is_visible(confirm_raw_uart)
            print("Raw data - UART mode, TRCBP is set accordingly")
        return status
    def send_raw_data_uart_mode_app_to_dut_ios(self):
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
    def send_raw_data_uart_mode_dut_to_app_ios(self):
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

    def send_raw_data_uart_mode_app_to_dut_stress_test_ios(self, input_data):
        status, raw_text_field = self.driver.find_element('XPATH', ioslocators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        assert status, "Failed to find the raw data text field to input"
        time.sleep(5)
        serialPort = self.ComportSet(com_port, baud_rate)
        self.driver.send_keys(raw_text_field, input_data)
        read_data = self.read_serial_port_data(serialPort, input_data)
        print(read_data)
        status = self.send_data_uart_ios(input_data)
        assert status, "Test Fails as the comparison is not successful"
        status_clear, clear_text = self.driver.find_element('XPATH', ioslocators.raw_clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        if read_data in input_data:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        serialPort.close()
        return status

    def send_raw_data_uart_mode_dut_to_app_stress_test_ios(self, input_data):
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
		
    def send_data_ios(self, input_data):
        status = False
        pass_string = "Compare data: PASS"
        TX_string = "[TX] - "+input_data
        RX_string = "[RX] - "+input_data
        result_status, pass_status = self.driver.find_element('XPATH', ioslocators.raw_data_log_message)
        assert result_status, "Failed to find the raw data log message"
        pass_status_get_text = self.driver.get_text(pass_status)
        print(pass_status_get_text)
        if (TX_string in pass_status_get_text) and (RX_string in pass_status_get_text):
            print("TX input is matching with RX input")
            if pass_string in pass_status_get_text:
                status = True
                print("Comparision Success")
            else:
                status = False
                print("Comparison has failed")
        else:
            status = False
            print("TX does not match with RX")
        return status
    def send_data_uart_ios(self, input_data):
        status = False
        TX_string = "[TX] - "+input_data
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
		
    def ios_verify_dut_name_non_visibility(self,dut_friendly_name):
        status = False
        result_string = ""
        status, dut_name = self.driver.find_element('XPATH', ioslocators.dut_name.format(dut_friendly_name))
        if not status:
            print("DUT is not connected")
            result_string = "DUT is not connected, Kill MBD App successful"
            status = True
        else:
            result_string = "DUT is connected, Test case failed"
        return status, result_string

    def verify_fw_rev_ios(self, FWVerValue):
        status = False
        fail_text = "Firmware version is not mentioned"
        text = "Firmware Version does not match"
        status, device_info = self.driver.find_element('XPATH', ioslocators.device_info)
        if status:
            visible = self.driver.is_visible(device_info)
            if visible:
                print("Collect the device information")
                status1, firmware_version = self.driver.find_element('XPATH', ioslocators.firmware_version)
                assert status1, "Failed to find the element on FW version section"
                fw_text = self.driver.get_text(firmware_version)
                if  fw_text in FWVerValue:
                    status = True
                    print("Firmware Version meets expectations")
                    FWVerValue_text = "Firmware Version is: {}".format(FWVerValue)
                    return status, FWVerValue_text
                else:
                    status = False
                    print("FW version is not displayed correctly")
                    return status, text
        else:
            status = False
            return status, fail_text

    def ios_disconnect_dut(self):
        print("Disconnect the DUT")
        status, back_button = self.driver.find_element('XPATH', ioslocators.back_button)
        assert status, "Failed to find back icon"
        status = self.driver.click_element(back_button)
        assert status, "Failed to click on back icon"


    def go_back(self):
        self.ios_disconnect_dut()


    def verify_disconnection(self):

        print("Checking if last connected is disconnected")
        result_status, pass_status = self.driver.find_element('XPATH', ioslocators.logmessage)
        assert result_status, "Failed to find the raw data log message"
        status_get_text = self.driver.get_text(pass_status)
        if "disconnected" or "Disconnected" in status_get_text:
            result_status = True
        else:
            result_status = False
        return result_status

    def loopback_mode_trp_ios(self):
        self.verify_mode_loopback_ios()
        self.save_settings_ios()
        self.confirm_loopback_mode_ios()

    def loopback_mode_trp_with_response_ios(self):
        self.verify_mode_loopback_ios()
        self.enable_write_with_response_ios()
        self.save_settings_ios()
        self.confirm_loopback_mode_ios()

    def loopback_mode_trcbp_ios(self):
        self.verify_mode_loopback_ios()
        self.switch_to_trcbp_ios()
        self.save_settings_ios()
        self.confirm_loopback_mode_trcbp_ios()

    def loopback_mode_trcbp_with_response_ios(self):
        self.verify_mode_loopback_ios()
        self.switch_to_trcbp_ios()
        self.enable_write_with_response_ios()
        self.save_settings_ios()
        self.confirm_loopback_mode_trcbp_ios()

    def loopback_mode_raw_trp_ios(self):
        self.verify_raw_data_mode_ios()
        self.click_settings_icon_ios()
        self.change_mode_ios()
        self.loopback_mode_ios()
        self.save_settings_ios()
        mode_set_trp = self.confirm_raw_data_loopbackmode_trp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"

    def loopback_mode_raw_trcbp_ios(self):
        self.verify_raw_data_mode_ios()
        self.click_settings_icon_ios()
        self.change_mode_ios()
        self.loopback_mode_ios()
        self.switch_to_trcbp_ios()
        self.save_settings_ios()
        mode_set_trp = self.confirm_raw_data_loopbackmode_trcbp_ios()
        assert mode_set_trp, "Raw data, TRCBP is not set accordingly"


    def set_receive_timeout_ios(self):
        delay = "3 sec"
        print("set_receive_timeout_ios.{}".format(delay))

        print("perform_scroll_down_ios")
        self.driver.perform_scroll_down_ios()
        time.sleep(3)
        print("perform_scroll_down_ios")
        self.driver.perform_scroll_down_ios()
        time.sleep(3)
        status,timeout_button = self.driver.find_element('XPATH',ioslocators.receive_data_timeout_button)
        assert status, "Failed to find the Multilink configuration button"
        status = self.driver.click_element(timeout_button)
        assert status, "unable to click the Multilink configuration button"
        time.sleep(2)
        status,timeout_field = self.driver.find_element('XPATH',ioslocators.set_timeout_field.format(delay))
        if status:
            status= self.driver.click_element(timeout_field)
            # assert status,"Unable to click the timeout field"
            # self.driver.send_keys(timeout_field,"5000")
            # status, set_timeout_button = self.driver.find_element('XPATH',ioslocators.set_timeout_button)
            # assert status, "Unable to set the timeout"
            # status = self.driver.click_element(set_timeout_button)
            assert status,"Unable to click the button"
        else:
            status, timeout_field = self.driver.find_element('XPATH', ioslocators.set_timeout_field.format(delay))
            if status:
                print("Timeout already set to 5000")
                status, set_timeout_button = self.driver.find_element('XPATH', ioslocators.set_timeout_button)
                assert status, "Unable to set the timeout"
                status = self.driver.click_element(set_timeout_button)
                assert status, "Unable to click the button"
        #self.driver.perform_scroll_down_ios()
        time.sleep(1)

    def ios_start_scan(self):
        status, scan_page = self.driver.find_element('XPATH', ioslocators.scan_button)
        assert status, "Failed to find the scan icon element in the mobile app"
        status = self.driver.click_element(scan_page)
        assert status, "Unable to click scan button"


    def ios_find_stop_transfer(self):
        status, scan_page = self.driver.find_element('XPATH', ioslocators.stop_data_transfer)
        assert status, "Failed to find the stop icon element in the mobile app"

    def ios_goback_main(self):
        print("Disconnect the DUT")
        status, back_button = self.driver.find_element('XPATH', ioslocators.back_to_main_page)
        assert status, "Failed to find back icon"
        status = self.driver.click_element(back_button)
        assert status, "Failed to click on back icon"

    def lightblue_start_scan(self):
        print('lightblue_start_scan')
        if sd.mobile_platform == 'mac':
            status, scan_page = self.driver.find_element('XPATH', 'XCUIElementTypeButton[@label="ArrowsClockwise"]')
        else:
            status, scan_page = self.driver.find_element('XPATH', 'XCUIElementTypeButton[@name="ArrowsClockwise"]')
        assert status, "Failed to find the scan icon element"
        status = self.driver.click_element(scan_page)
        assert status, "Unable to click scan button"

    def lightblue_filter_peripherals(self, name):
        print('lightblue_filter_peripherals')
        status, text_field = self.driver.find_element('XPATH', '//XCUIElementTypeTextField')
        assert status, "Failed to find the textfield"
        self.driver.send_keys(text_field, name)

    def lightblue_connect(self, dut_name):
        print('lightblue_connect: {}'.format(dut_name))
        #ioslocators.dut_name.format(dut_friendly_name)
        #status, peripheral = self.driver.find_element('XPATH', '//XCUIElementTypeStaticText[@label="BLE_UART_CDDF_H"]')
        status, peripheral = self.driver.find_element('XPATH', ioslocators.dut_name.format(dut_name))
        #assert status, "Failed to find the peripheral"
        if not status:
            print("Failed to find the peripheral.Fail retry.")
            if dut_name == 'Direct A':
                new_dut_name = 'Direct Adv'
            else:
                new_dut_name = 'Direct A'
            status, peripheral = self.driver.find_element('XPATH', ioslocators.dut_name.format(new_dut_name))
            assert status, "Failed to find the peripheral"
        if sd.mobile_platform == 'mac':
            status, connect_button = self.driver.find_element('XPATH', '//XCUIElementTypeButton[@label="Connect"]')
        else:
            status, connect_button = self.driver.find_element('XPATH', '//XCUIElementTypeButton[@name="Connect"]')
        assert status, "Failed to find the connect button"
        status = self.driver.click_element(connect_button)
        assert status, "Unable to click connect button"

    def lightblue_scroll_gesture(self, delta_y):
        print('lightblue_scroll_gesture.{}'.format(delta_y))
        if sd.mobile_platform == 'mac':
            status, dis_element = self.driver.find_element('XPATH', '//XCUIElementTypeStaticText[@label="Device Information"]')
        else:
            status, dis_element = self.driver.find_element('XPATH', '//XCUIElementTypeStaticText[@name="Device Information"]')
        assert status, "Failed to find the element."
        time.sleep(2)
        #self.driver.perform_scroll_down_macos(dis, -400)
        self.driver.perform_scroll_macos(dis_element.id, delta_y)
        time.sleep(3)

    def lightblue_verify_ble_connected(self):
        print('lightblue_verify_ble_connected')
        if sd.mobile_platform == 'mac':
            status, element = self.driver.find_element('XPATH','//XCUIElementTypeStaticText[@label="Connected"]')
        else:
            status, element = self.driver.find_element('XPATH', '//XCUIElementTypeStaticText[@name="Connected"]')
        assert status, "Failed to find the element. Connected"

    def lightblue_get_device_info_data(self):
        print('lightblue_get_device_info_data')
        self.driver.find_ios_collection_view_element(range_start=4, range_end=8)

    def lightblue_verify_ble_services_and_characteristics(self, start_service=""):
        print('lightblue_verify_ble_services_and_characteristics.{}'.format(start_service))

        if sd.mobile_platform == 'mac':
            locator = "//XCUIElementTypeStaticText[@label='{}']"
        else:
            locator = "//XCUIElementTypeStaticText[@name='{}']"

        device_information_service = 'Device Information'
        device_information_characteristics = ['Manufacturer Name String','Model Number String','Firmware Revision String']

        mchp_transparent_service = '0x49535343-FE7D-4AE5-8FA9-9FAFD205E455'
        mchp_transparent_characteristics = ['0x49535343-1E4D-4BD9-BA61-23C647249616','0x49535343-8841-43F4-A8D4-ECBE34729BB3','0x49535343-4C8A-39B3-2F49-511CFF073B7E']

        mchp_ota_service = '0x4D434850-253D-46B3-9923-E61B8E8215D7'
        mchp_ota_characteristics = ['0x4D434850-22E4-4246-AF03-0C4A2F906358','0x4D434850-34D9-40A6-BA7E-56F57C8CD478','0x4D434850-9327-45DE-8882-C97F39028A76']

        services = [device_information_service,mchp_transparent_service,mchp_ota_service]
        characteristics = {device_information_service:device_information_characteristics, mchp_transparent_service:mchp_transparent_characteristics, mchp_ota_service:mchp_ota_characteristics}

        result = True
        discover_service = ""

        for service in services:
            if start_service != "" and service != start_service:
                continue
            print("verify ble service.{}".format(service))
            discover_service = service
            status, element = self.driver.find_element('XPATH', locator.format(service))
            #assert status, "Failed to find the service"
            if not status:
                print("Failed to find the service.")
                result = False
                break
            char_array = characteristics.get(service)
            #assert char_array is not None , "Failed to find the character array"
            time.sleep(2)
            for char in char_array:
                print("verify ble characteristic.{}".format(char))
                status, element = self.driver.find_element('XPATH', locator.format(char))
                #assert status, "Failed to find the service"
                if not status:
                    print("Failed to find the characteristic.")
                    result = False
                    break
                else:
                    time.sleep(2)
            if not result:
                break

        return result, discover_service

    def lightblue_enter_characteristic_scene(self, characteristic):
        print('lightblue_characteristic_control.{}'.format(characteristic))
        if sd.mobile_platform == 'mac':
            locator = "//XCUIElementTypeStaticText[@label='{}']"
        else:
            locator = "//XCUIElementTypeStaticText[@name='{}']"

        status, element = self.driver.find_element('XPATH', locator.format(characteristic))
        assert status, "Failed to find the characteristic."
        time.sleep(2)
        element.click()
        return status

    def lightblue_characteristic_screen_goback(self):
        print('lightblue_characteristic_screen.goback')
        if sd.mobile_platform == 'mac':
            status, element = self.driver.find_element('XPATH', '//XCUIElementTypeButton[@label=\"Peripheral\"]')
        else:
            status, element = self.driver.find_element('XPATH', '//XCUIElementTypeButton[@name=\"Peripheral\"]')

        assert status, "Failed to find the back button."
        time.sleep(2)
        element.click()
        return status

    def lightblue_ble_disconnect(self):
        print('lightblue_ble_disconnect')
        if sd.mobile_platform == 'mac':
            status, element = self.driver.find_element('XPATH', '//XCUIElementTypeButton[@label=\"Back\"]')
        else:
            status, element = self.driver.find_element('XPATH', '//XCUIElementTypeButton[@name=\"Back\"]')
        assert status, "Failed to find the back button(ble disconnect)."
        time.sleep(2)
        element.click()
        return status

    def lightblue_characteristic_action(self, characteristic ,action):
        print('lightblue_characteristic_action.char = {}.{}'.format(characteristic, action))
        if action == "Subscribe" or action == "Unsubscribe":
            if sd.mobile_platform == 'mac':
                locator = "//XCUIElementTypeButton[@label='{}']"
            else:
                locator = "//XCUIElementTypeButton[@name='{}']"
            status, element = self.driver.find_element('XPATH', locator.format(action))
            assert status, "Failed to find the action button."
            time.sleep(2)
            element.click()
            time.sleep(3)
            #print("Check state")
            new_state = ""
            if action == 'Subscribe':
                new_state = 'Unsubscribe'
            elif action == 'Unsubscribe':
                new_state = 'Subscribe'
            print("Check button: {} state".format(new_state))
            status, btn_element = self.driver.find_element('XPATH', locator.format(new_state))
            assert status, "Failed to find the action button."
            print("Success")
            time.sleep(2)
            return status, new_state
        else:
            return False
        #elif action == "Read":

    def lightblue_characteristic_write(self, characteristic, hex_data):
        print('lightblue_characteristic_write.char = {}.data = {}'.format(characteristic, hex_data))
        if sd.mobile_platform == 'mac':
            locator = "//XCUIElementTypeButton[@label='{}']"
        else:
            locator = "//XCUIElementTypeButton[@name=\"{}\"]"
        status, element = self.driver.find_element('XPATH', locator.format('Write new value'))
        assert status, "Failed to find the write button."
        time.sleep(2)
        element.click()
        time.sleep(3)
        status, text_field = self.driver.find_element('XPATH', '//XCUIElementTypeTextField')
        assert status, "Failed to find the textfield"
        time.sleep(2)
        self.driver.send_keys(text_field, hex_data)
        print("send kex :{}".format(hex_data))
        time.sleep(3)
        status, element = self.driver.find_element('XPATH', locator.format('Send'))
        time.sleep(2)
        assert status, "Failed to find the send button."
        element.click()
        time.sleep(3)
        '''
        status, element = self.driver.find_element('XPATH', locator.format('Characteristic'))
        assert status, "Failed to find the back button."
        time.sleep(2)
        element.click()
        time.sleep(3)
        '''

    def lightblue_characteristic_read(self, characteristic):
        print('lightblue_characteristic_read.char = {}.{}'.format(characteristic, characteristic))
        self.driver.find_ios_collection_view_element(range_start=7, range_end=8)

    def lightblue_pairing(self):
        print('lightblue_pairing')
        #self.driver.find_pairing_alert1()
        self.driver.find_pairing_alert2()











