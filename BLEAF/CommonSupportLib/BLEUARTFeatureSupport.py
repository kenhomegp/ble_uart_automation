import os
import sys
import threading
import time
from ..MCP2200.MCP2200 import Mcp2200
from . import android_locators as locators
from .StationData import stationData
from ..StationConfig import conf_file
from ..CommonSupportLib.Serial_Implementaiton import SerialSuppport


# Text for result strings for each mode
checksum_comparepass_text = "[TX] - Compare checksum : PASS"
loopback_comparepass_text = "[Loopback] - Compare data : PASS"
fixed_pattern_comparepass_text = "[Fixed data pattern] Compare data : PASS"
uart_comparepass_text = "[UART] - File Receive : Success"
text_500K = "500004"
text_100k = "100008"
text_fixed_pattern = "512000"
baud_rate = conf_file.baud_rate
block_size = '4096'
text_file = '500k'
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
com_port = conf_file.com_port

class BLEUARTFeatureSupport:
    def __init__(self, driver=sd.mobile_driver):
        self.thread = ""
        if not driver:
            sd = stationData()
            self.driver = sd.mobile_driver
            print("Driver-##############################################", self.driver)
        else:
            self.driver = driver
            print("Driver-##############################################", self.driver)
        self.serialdriver = SerialSuppport()
    
    def click_settings_icon(self):
        status, start_scan_button = self.driver.find_element('XPATH', locators.settings_icon)
        assert status, "Settings icon not found"
        status = self.driver.click_element(start_scan_button)
        assert status, "Failed to click on Settings icon"

    def change_mode(self):
        status, start_scan_button = self.driver.find_element('XPATH', locators.change_mode_icon)
        assert status, "Change mode icon not found"
        status = self.driver.click_element(start_scan_button)
        assert status, "Failed to click on change mode icon"

    def switch_to_trcbp(self):
        print("Switch to TRCBP profile")
        status, change_to_trcbp = self.driver.find_element('XPATH', locators.TRCBP_icon)
        assert status, "TRCBP icon not found"
        status = self.driver.click_element(change_to_trcbp)
        assert status, "Failed to click on TRCBP icon"

    def go_back(self):
        self.driver.go_back()

    def enable_write_with_response(self):
        print("Enable write with response")
        status1, enable = self.driver.find_element('XPATH', locators.write_with_response_icon)
        assert status1, "Write with response icon not found"
        status1 = self.driver.click_element(enable)
        assert status1, "Failed to enable Write with response"

    def checksum_mode(self):
        status, start_scan_button = self.driver.find_element('XPATH', locators.ble_uart_mode_checksum)
        assert status, "Checksum mode icon not found"
        status = self.driver.click_element(start_scan_button)
        assert status, "Failed to click on checksum mode icon"
        time.sleep(5)

    def loopback_mode(self):
        status, start_scan_button = self.driver.find_element('XPATH', locators.ble_uart_mode_loopback)
        assert status, "Loopback mode icon not found"
        status = self.driver.click_element(start_scan_button)
        assert status, "Failed to click on Loopback mode icon"
        time.sleep(5)

    def set_500K(self):
        status1, select_file = self.driver.find_element('XPATH', locators.select_500K)
        assert status1, "500K file not found"
        status1 = self.driver.click_element(select_file)
        assert status1, "Failed to select 500K file"
        time.sleep(5)
        status2, click_on_500K = self.driver.find_element('XPATH', locators.select_500K_file)
        assert status2, "500K file not found"
        status2 = self.driver.click_element(click_on_500K)
        assert status2, "Failed to set 500K file"

    def set_100K(self):
        status1, select_file = self.driver.find_element('XPATH', locators.select_100K)
        assert status1, "100K file not found"
        status1 = self.driver.click_element(select_file)
        assert status1, "Failed to select 100K file"
        time.sleep(5)
        status2, click_on_100K = self.driver.find_element('XPATH', locators.select_100K_file)
        assert status2, "100K file not found"
        status2 = self.driver.click_element(click_on_100K)
        assert status2, "Failed to set 100K file"

    def fixed_pattern_mode(self):
        status, start_scan_button = self.driver.find_element('XPATH', locators.ble_uart_mode_fixed_pattern)
        assert status, "Fixed Pattern mode icon not found"
        status = self.driver.click_element(start_scan_button)
        assert status, "Failed to click on Fixed Pattern mode icon"
        time.sleep(5)

    def uart_mode(self):
        status, start_scan_button = self.driver.find_element('XPATH', locators.ble_uart_mode_uart)
        assert status, "UART mode icon not found"
        status = self.driver.click_element(start_scan_button)
        assert status, "Failed to click on UART mode icon"
        time.sleep(5)

    def confirm_checksum_mode(self):
        status = False
        status, confirm_checksum_500K = self.driver.find_element('XPATH', locators.confirm_checksum_500K)
        if status:
            status = self.driver.is_visible(confirm_checksum_500K)
            print("Checksum mode, TRP, 500K is set accordingly")
        return status

    def confirm_loopback_mode(self):
        status = False
        status, confirm_loopback_500K = self.driver.find_element('XPATH', locators.confirm_loopback_500K)
        if status:
            status = self.driver.is_visible(confirm_loopback_500K)
            print("Loopback mode, TRP, 500K is set accordingly")
        return status

    def confirm_100k_loopback_mode(self):
        status = False
        status, confirm_loopback_100K = self.driver.find_element('XPATH', locators.confirm_loopback_100K)
        if status:
            status = self.driver.is_visible(confirm_loopback_100K)
            print("Loopback mode, TRP, 100K is set accordingly")
        return status

    def confirm_fixed_pattern_mode(self):
        status = False
        status, confirm_fixed_pattern = self.driver.find_element('XPATH', locators.confirm_fixed_pattern)
        if status:
            status = self.driver.is_visible(confirm_fixed_pattern)
            print("Fixed Pattern mode, TRP is set accordingly")
        return status

    def confirm_uart_mode(self):
        status = False
        status, confirm_uart = self.driver.find_element('XPATH', locators.confirm_uart)
        if status:
            status = self.driver.is_visible(confirm_uart)
            print("UART mode, TRP is set accordingly")
        return status

    def confirm_100k_uart_mode(self):
        status = False
        status, confirm_uart = self.driver.find_element('XPATH', locators.confirm_uart_100k)
        if status:
            status = self.driver.is_visible(confirm_uart)
            print("UART mode, TRP  and 100k is set accordingly")
        return status

    def confirm_checksum_mode_trcbp(self):
        status = False
        status, confirm_checksum_500K = self.driver.find_element('XPATH', locators.confirm_checksum_500K_trcbp)
        if status:
            status = self.driver.is_visible(confirm_checksum_500K)
            print("Checksum mode, TRCBP and 500K is set accordingly")
        return status

    def confirm_loopback_mode_trcbp(self):
        status = False
        status, confirm_loopback_500K = self.driver.find_element('XPATH', locators.confirm_loopback_500K_trcbp)
        if status:
            status = self.driver.is_visible(confirm_loopback_500K)
            print("Loopback mode, TRCBP and 500K is set accordingly")
        return status

    def confirm_fixed_pattern_mode_trcbp(self):
        status = False
        status, confirm_fixed_pattern = self.driver.find_element('XPATH', locators.confirm_fixed_pattern_trcbp)
        if status:
            status = self.driver.is_visible(confirm_fixed_pattern)
            print("Fixed Pattern mode, TRCBP is set accordingly")
        return status

    def confirm_uart_mode_trcbp(self):
        status = False
        status, confirm_uart = self.driver.find_element('XPATH', locators.confirm_uart_trcbp)
        if status:
            status = self.driver.is_visible(confirm_uart)
            print("UART mode, TRCBP, 500K is set accordingly")
        return status

    def confirm_uart_mode_100k_trcbp(self):
        status = False
        status, confirm_uart = self.driver.find_element('XPATH', locators.confirm_uart_trcbp_100k)
        if status:
            status = self.driver.is_visible(confirm_uart)
            print("UART mode, TRCBP, 100K is set accordingly")
        return status


    def data_transfer_START(self):
        status, transfer_data = self.driver.find_element('XPATH', locators.start_data_transfer)
        assert status, "START icon not found"
        status = self.driver.click_element(transfer_data)
        assert status, "Failed to transfer Data"
        time.sleep(10)

    def data_transfer_START_mobile_app(self):
        status, transfer_data = self.driver.find_element('XPATH', locators.start_data_transfer)
        assert status, "START icon not found"
        status = self.driver.click_element(transfer_data)
        assert status, "Failed to transfer Data"

    def multilink_data_transfer_START(self):
        status, transfer_data = self.driver.find_element('XPATH', locators.start_data_transfer)
        assert status, "START icon not found"
        status = self.driver.click_element(transfer_data)
        assert status, "Failed to transfer Data"

    def data_transfer_START_kill_mbd_app(self):
        status, transfer_data = self.driver.find_element('XPATH', locators.start_data_transfer)
        assert status, "START icon not found"
        status = self.driver.click_element(transfer_data)
        assert status, "Failed to transfer Data"

    def data_transfer_STOP(self):
        status, stop_transfer = self.driver.find_element('XPATH', locators.stop_data_transfer)
        print(status)
        if not status:
            status, stop_transfer = self.driver.find_element('XPATH', locators.stop_data_transfer)
            assert status, "STOP icon not found"
        status = self.driver.click_element(stop_transfer)
        assert status, "Failed to STOP Data transfer"
        time.sleep(2)

    def checksum_mode_results(self):
        result_status = False
        status, checksum_throughput_value = self.driver.find_element('XPATH', locators.checksum_throughput_result)
        assert status, "Failed to find locator for checksum throughput result"
        throughput_value = self.driver.get_text(checksum_throughput_value)
        status1, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status1, "Failed to find log message"
        log_text = self.driver.get_text(logmessage)
        result_str = "Test Failed with following data:\nTx Size, Time and Throughput: {}".format(throughput_value)
        if (text_500K in throughput_value) and (text_500K in log_text) and (checksum_comparepass_text in log_text):
            print("Checking if the transmitted file size matches 500004")
            result_str = "Checksum Mode Test results:\n Test Passed with following data:\nTx Size, Time and Throughput: {}\n\n".format(throughput_value)
            result_status = True
            print(result_str)
        else:
            result_status = False
            print(result_str)
        return result_status, result_str

    def stop_data_transfer_results(self):
        status = True
        result_str = "Data transmission stopped. Zero bytes transferred."
        status, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status, "Failed to see the log message in the mobile App"
        log_text = self.driver.get_text(logmessage)
        fail_result = "File Transfer is complete! 500k.txt"
        if result_str in log_text:
            print("The data transfer has stopped accordingly")
            return status, result_str
        else:
            status = False
        return status, fail_result

    def loopback_mode_results_TX(self):
        result_status = False
        status, loopback_throughput_value_TX = self.driver.find_element('XPATH', locators.loopback_TX_throughput_result)
        assert status, "Failed to find locator for loopback throughput result"
        throughput_value_TX = self.driver.get_text(loopback_throughput_value_TX)
        status1, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status1, "Failed to find the log message"
        log_text = self.driver.get_text(logmessage)
        result_str_TX = "Test Failed with following data:\nTx Size, Time and Throughput: {}".format(throughput_value_TX)
        if ((text_500K in throughput_value_TX) and (text_500K in log_text) and (loopback_comparepass_text in log_text)):
            print("Checking if the transmitted file size matches 500004")
            result_str_TX = "Loopback Mode Test Results(TX):\nTest Passed with following data:\nTx Size, Time and Throughput: {}\n\n".format(throughput_value_TX)
            result_status = True
            print(result_str_TX)
        else:
            result_status = False
            print(result_str_TX)
        return result_status, result_str_TX

    def loopback_mode_100Kresults_TX(self):
        result_status = False
        status, loopback_throughput_value_TX = self.driver.find_element('XPATH', locators.loopback_TX_throughput_result)
        assert status, "Failed to find locator for loopback throughput result"
        throughput_value_TX = self.driver.get_text(loopback_throughput_value_TX)
        status1, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status1, "Failed to find the log message"
        log_text = self.driver.get_text(logmessage)
        result_str_TX = "Test Failed with following data:\nTx Size, Time and Throughput: {}".format(throughput_value_TX)
        if ((text_100k in throughput_value_TX) and (text_100k in log_text) and (loopback_comparepass_text in log_text)):
            print("Checking if the transmitted file size matches 100008")
            result_str_TX = "Loopback Mode Test Results(TX):\nTest Passed with following data:\nTx Size, Time and Throughput: {}\n\n".format(throughput_value_TX)
            result_status = True
            print(result_str_TX)
        else:
            result_status = False
            print(result_str_TX)
        return result_status, result_str_TX

    def loopback_mode_results_RX(self):
        result_status = False
        status, loopback_throughput_value_RX = self.driver.find_element('XPATH', locators.loopback_RX_throughput_result)
        assert status, "Failed to find locator for loopback throughput result"
        throughput_value_RX = self.driver.get_text(loopback_throughput_value_RX)
        status1, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status1, "Failed to find the log message"
        log_text = self.driver.get_text(logmessage)
        result_str_RX = "Test Failed with following data:\nRx Size, Time and Throughput: {}".format(throughput_value_RX)
        if ((text_500K in throughput_value_RX) and (text_500K in log_text) and (loopback_comparepass_text in log_text)):
            print("Checking if the Received file size matches 500004")
            result_str_RX = "Loopback Mode Test Results(RX):\nTest Passed with following data:\nRx Size, Time and Throughput: {}\n\n".format(
                throughput_value_RX)
            result_status = True
            print(result_str_RX)
        else:
            result_status = False
            print(result_str_RX)
        return result_status, result_str_RX

    def loopback_mode_100Kresults_RX(self):
        result_status = False
        status, loopback_throughput_value_RX = self.driver.find_element('XPATH', locators.loopback_RX_throughput_result)
        assert status, "Failed to find locator for loopback throughput result"
        throughput_value_RX = self.driver.get_text(loopback_throughput_value_RX)
        status1, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status1, "Failed to find the log message"
        log_text = self.driver.get_text(logmessage)
        result_str_RX = "Test Failed with following data:\nRx Size, Time and Throughput: {}".format(throughput_value_RX)
        if ((text_100k in throughput_value_RX) and (text_100k in log_text) and (loopback_comparepass_text in log_text)):
            print("Checking if the Received file size matches 500004")
            result_str_RX = "Loopback Mode Test Results(RX):\nTest Passed with following data:\nRx Size, Time and Throughput: {}\n\n".format(
                throughput_value_RX)
            result_status = True
            print(result_str_RX)
        else:
            result_status = False
            print(result_str_RX)
        return result_status, result_str_RX

    def fixed_pattern_mode_results_RX(self):
        result_status = False
        status, fixed_pattern_RX_throughput_result = self.driver.find_element('XPATH', locators.fixed_pattern_RX_throughput_result)
        assert status, "Failed to find the fixed pattern locator"
        throughput_value_RX = self.driver.get_text(fixed_pattern_RX_throughput_result)
        status, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status, "Failed to find the fixed pattern log message"
        log_text = self.driver.get_text(logmessage)
        fail_result = "Test Failed with following data:\nRx Size, Time and Throughput: {}\n\n".format(throughput_value_RX)
        if (text_fixed_pattern in throughput_value_RX) and (text_fixed_pattern in log_text) and (fixed_pattern_comparepass_text in log_text):
            print("Checking if the Received file size matches 512000")
            print("In the loop")
            result_status = True
            result_str = "Fixed Pattern Mode Test Results: \nTest Passed with following data:\nRx Size, Time and Throughput: {}\n\n".format(throughput_value_RX)
            print(result_str)
        else:
            result_status = False
            result_str = fail_result
            print(result_str)
        return result_status, result_str

    def uart_mode_results_RX(self):
        status = False
        result_str = ""
        status, uart_RX_throughput_result = self.driver.find_element('XPATH', locators.uart_RX_throughput_result)
        assert status, "Failed to find the locator for UART RX throughput result"
        throughput_value_RX = self.driver.get_text(uart_RX_throughput_result)
        status1, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status1, "Failed to find the UART log message"
        log_text = self.driver.get_text(logmessage)
        fail_result = "UART Mode - Uplink Test Results\nTest Failed with following data:\nRx Size, Time and Throughput: {}\n\n".format(throughput_value_RX)
        if (uart_comparepass_text in log_text) and (text_500K in throughput_value_RX):
            print("In the loop")
            result_str = "UART Mode - Uplink Test Results (dut to Mobile App):\nTest Passed with following data:\nRx Size, Time and Throughput: {}\n\n".format(throughput_value_RX)
            print(result_str)
            status = True
        else:
            status = False
            result_str = fail_result
            print(result_str)
        return status, result_str

    def uart_mode_results_100k_RX(self):
        status = False
        result_str = ""
        status, uart_RX_throughput_result = self.driver.find_element('XPATH', locators.uart_RX_throughput_result)
        assert status, "Failed to find the locator for UART RX throughput result"
        throughput_value_RX = self.driver.get_text(uart_RX_throughput_result)
        status1, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status1, "Failed to find the UART log message"
        log_text = self.driver.get_text(logmessage)
        fail_result = "UART Mode - Uplink Test Results\nTest Failed with following data:\nRx Size, Time and Throughput: {}\n\n".format(throughput_value_RX)
        if (uart_comparepass_text in log_text) and (text_100k in throughput_value_RX):
            print("In the loop")
            result_str = "UART Mode - Uplink Test Results (dut to Mobile App):\nTest Passed with following data:\nRx Size, Time and Throughput: {}\n\n".format(throughput_value_RX)
            print(result_str)
            status = True
        else:
            status = False
            result_str = fail_result
            print(result_str)
        return status, result_str

    def uart_mode_results_TX(self, msg):
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
        fail_result = "UART Mode - Downlink test results (Mobile App to dut):\nTest Failed with following data:\nTx Size, Time and Throughput: {}\n\n".format(throughput_value_TX)
        if (result_str in log_text) and (msg == "Compare PASS"):
            message = "UART Mode - Downlink test results (Mobile App to dut):\nTest Passed with following data:\nTx Size, Time and Throughput: {}\n\n".format(throughput_value_TX)
            print(message)
            status = True
        else:
            print("Comparison Failed from the DUT side or matching string not found")
            message = fail_result
            print(message)
            status = False
        return status, message

    def uart_mode_results_TX_100(self, msg):
        status = False
        message = ''
        print(msg)
        result_str = "File Transfer is complete! 100k.txt\nBytes transferred = 100008"
        status, uart_TX_throughput_result = self.driver.find_element('XPATH', locators.uart_TX_throughput_result)
        assert status, "Failed to find element for UART TX throughput result"
        throughput_value_TX = self.driver.get_text(uart_TX_throughput_result)
        status1, logmessage = self.driver.find_element('XPATH', locators.mode_logmessage)
        assert status1, "Failed to find the UART mode log message screen"
        log_text = self.driver.get_text(logmessage)
        fail_result = "UART Mode - Downlink test results (Mobile App to dut):\nTest Failed with following data:\nTx Size, Time and Throughput: {}\n\n".format(throughput_value_TX)
        if (result_str in log_text) and (msg == "Compare PASS"):
            message = "UART Mode - Downlink test results (Mobile App to dut):\nTest Passed with following data:\nTx Size, Time and Throughput: {}\n\n".format(throughput_value_TX)
            print(message)
            status = True
        else:
            print("Comparison Failed from the DUT side or matching string not found")
            message = fail_result
            print(message)
            status = False
        return status, message

    def verify_mode_checksum(self):
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.click_setting_onepluspro()
        else:
            self.click_settings_icon()  
        time.sleep(5)
        self.change_mode()
        time.sleep(5)
        print("Select checksum mode in settings")
        self.checksum_mode()
        time.sleep(5)
        print("Select 500K file")
        self.set_500K()
        time.sleep(5)

    def checksum_mode_data_transfer(self):
        print("Start the Data transfer")
        self.data_transfer_START()
        time.sleep(15)

    def verify_mode_loopback(self):
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.click_setting_onepluspro()
        else:
            self.click_settings_icon()  
        time.sleep(5)
        self.change_mode()
        time.sleep(5)
        print("Select Loopback mode and select 500K file")
        self.loopback_mode()
        time.sleep(5)
        self.set_500K()
        time.sleep(5)

    def verify_mode_100_loopback(self):
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.click_setting_onepluspro()
        else:
            self.click_settings_icon()  
        time.sleep(5)
        self.change_mode()
        time.sleep(5)
        print("Select Loopback mode and select 500K file")
        self.loopback_mode()
        time.sleep(5)
        self.set_100K()
        time.sleep(5)

    def loopback_mode_data_transfer(self):
        print("Start the Data transfer")
        self.data_transfer_START()
        time.sleep(25)

    def verify_mode_fixed_pattern(self):
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.click_setting_onepluspro()
        else:
            self.click_settings_icon()  
        time.sleep(5)
        self.change_mode()
        time.sleep(5)
        print("Select Fixed Pattern mode, Do not select any file")
        self.fixed_pattern_mode()
        time.sleep(5)
        self.set_500K()
        time.sleep(5)

    def fixed_pattern_mode_data_transfer(self):
        print("Start the Data transfer")
        self.data_transfer_START()
        time.sleep(5)
        status, result_str = self.fixed_pattern_mode_results_RX()
        return status, result_str

    def verify_mode_uart(self):
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.click_setting_onepluspro()
        else:
            self.click_settings_icon()  
        # self.click_settings_icon()
        time.sleep(5)
        print("Select UART mode")
        self.change_mode()
        time.sleep(5)
        self.uart_mode()
        time.sleep(5)
        print("Select 500K file")
        self.set_500K()
        time.sleep(5)

    def verify_mode_100K_uart(self):
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.click_setting_onepluspro()
        else:
            self.click_settings_icon()  
        time.sleep(5)
        print("Select UART mode")
        self.change_mode()
        time.sleep(5)
        self.uart_mode()
        time.sleep(5)
        print("Select 100K file")
        self.set_100K()
        time.sleep(5)

    def initialize_com_port(self):
        global serialPort
        print ("Initialize com port")
        if not self.IniMCP2200(com_port, baud_rate):
            sys.exit()
        time.sleep(5)

    def dut_uart_mode_data_transfer(self):
        print("Start the Data transfer from the dut side <PC Tool>")
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        self.TxEntry(serialPort, text_file)
        time.sleep(25)
        serialPort.close()

    def dut_uart_mode_100k_data_transfer(self):
        print("Start the Data transfer from the dut side <PC Tool>")
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        status_clear, clear_text = self.driver.find_element('XPATH', locators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        self.TxEntry_100(serialPort, text_file1)
        time.sleep(25)
        serialPort.close()

    def app_uart_mode_data_transfer(self):
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Start the Data transfer from the App side")
        status_clear, clear_text = self.driver.find_element('XPATH', locators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        self.thread = self.RxEntry(serialPort)
        self.data_transfer_START()
        time.sleep(100)
        self.CloseSerialPort(serialPort)

    def uart_mode_results_TX_display(self):
        time.sleep(5)
        status, result_str = self.uart_mode_results_TX(receive_serial_str)
        return status, result_str

    def uart_mode_results_100k_TX_display(self):
        time.sleep(5)
        status, result_str = self.uart_mode_results_TX_100(receive_serial_str)
        return status, result_str

    def IniMCP2200(self, com_port, baud_rate):
        mcu = Mcp2200()
        if not mcu.IsConnected():
            print("The MCP2200 is disconnected")
            return False
        else:
            print("MCP2200 is connected")

        #I/O,Baudrate,RxLED,TxLED,Flow Control,ULOAD,SSPND
        if not mcu.ConfigureMCP2200(0xFF, baud_rate, 0, 0, Flow=True, Uload=False, SSPND=False, Invert=False):
            print("Configure MCP2200 failed")
            return False
        else:
            print("Configure MCP2200 successfully")
        return True

    def LoadFile(self, text_file):
        loadstr = ''
        file = open(os.getcwd() + '\\TextFiles\\' + text_file + '.txt', 'rb')
        for line in file:
            loadstr += line.decode("utf-8")
        file.close()
        return loadstr

    def AddHciUartACLId(self, buf):
        # data = bytes(('02' + buf), encoding='utf-8')
        data = bytes(buf, encoding='utf-8')
        return data

    def RawDataTxSend(self, serialPort, info_,):
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

    def TxEntry(self, serialPort, textFile):
        print("TxEntry, file = " + textFile)
        textStr = self.LoadFile(textFile)
        txSendData = textStr
        TxEnd = False
        BlockSize = int(block_size)
        info = [txSendData, TxEnd, BlockSize]
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
                    #print("500ms")
                    emptyCount += 1

            if len(dat) != 0 and emptyCount > 5:
                emptyCount = 0
                uartData = bytearray()
                for dd in dat:
                    uartData += bytearray(dd)
                rxData = bytes(uartData)
                print("Data transmission timeout.")

                str1 = rxData.decode()
                #print(str1)
                size = str1[-7:-2]  #Get last data
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
        #self.thread.do_run = False
        #self.thread.join()
        serialPort.close()

    def verify_mode_uart_birectional_data_transfer(self):
        t3 = []
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        time.sleep(5)
        status_clear, clear_text = self.driver.find_element('XPATH', locators.clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        print("Start the Data transfer from the App side & dut side <PC Tool> simultaneously")
        t0 = threading.Thread(target=self.read_serial_port, args=(serialPort, q_receiveData,))
        t0.start()
        time.sleep(5)
        t1 = threading.Thread(target=self.data_transfer_START_mobile_app, args=())
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        t2 = threading.Thread(target=self.TxEntry, args=(serialPort, text_file,))
        t3.append(t1)
        t3.append(t2)
        #t1.start()
        #t2.start()
        for eachThread in t3:
            eachThread.start()
            eachThread.join()
        t0.join()
        time.sleep(25)
        self.CloseSerialPort(serialPort)
        time.sleep(5)
        return receive_serial_str

    def start_stop_data_transfer(self):
        print("Start the Data transfer")
        status, transfer_data = self.driver.find_element('XPATH', locators.start_data_transfer)
        assert status, "START icon not found"
        status = self.driver.click_element(transfer_data)
        assert status, "Failed to transfer Data"
        time.sleep(3)
        print("Stop the Data transfer")
        status, stop_transfer = self.driver.find_element('XPATH', locators.stop_data_transfer)
        assert status, "STOP icon not found"
        status = self.driver.click_element(stop_transfer)
        assert status, "Failed to Stop Data Transfer"
        time.sleep(5)

    def set_uart_mode(self):
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        #self.thread = self.RxEntry(serialPort)

    def check_data_transfer_checksum(self):
        print("Start the Data transfer")
        self.data_transfer_START()
        time.sleep(12)
        result_str = self.checksum_mode_results()
        return result_str

    def close_mbd_app(self,app_package):
        self.driver.close_app(app_package)

    def click_connectionparam_icon(self):
        status, start_connParam_button = self.driver.find_element('XPATH', locators.connectionparam_icon)
        assert status, "Connection parameter icon not found"
        status = self.driver.click_element(start_connParam_button)
        # assert status, "Failed to click on Connection parameter icon"
       
    def click_setting_onepluspro(self):
        self.driver.click_setting_oneplus()

    def verify_app_open(self):

        status, dashboard_text = self.driver.find_element('By.XPATH', locators.dashboard_text)

        if status:
            status = self.driver.is_visible(dashboard_text)
            print("MBD Application opened.")
        return status

    def scan_and_connect_dut(self, dut_friendly_name):
        self.open_ble_uart_scanner()
        self.click_start_scan()
        print("Please wait for 15 sec to scan the devices")
        time.sleep(15)
        print("Press Cancel button to stop scanning")
        self.click_cancel_button()

        time.sleep(1)

        self.search_and_select_dut(dut_friendly_name)
        time.sleep(1)

    def open_ble_uart_scanner(self):
        error_msg = ""
        print("Click BLE Uart\n\n")
        status, ble_uart_icon = self.driver.find_element('XPATH', locators.ble_uart_icon)
        assert status, "BLE Uart Icon not found"

        status = self.driver.click_element(ble_uart_icon)
        assert status, "Failed to open BLE Uart page"

        status, ble_uart_scanner = self.driver.find_element('XPATH', locators.ble_uart_scanner)
        assert status, "PIC32CXBZ not found"

        status = self.driver.click_element(ble_uart_scanner)
        assert status, "Failed to open BLE Uart page"

        status, scan_button = self.driver.find_element('XPATH', locators.scan_button)
        assert status, "Scan button not found"

        status = self.driver.is_visible(scan_button)
        assert status, "Scan button not visible"

    def click_start_scan(self):
        status, start_scan_button = self.driver.find_element('XPATH', locators.scan_button)
        assert status, "Scan button not found"
        status = self.driver.click_element(start_scan_button)
        assert status, "Failed to click start scan button on screen"

    def click_cancel_button(self):
        status, start_scan_button = self.driver.find_element('XPATH', locators.cancel_button)
        assert status, "Cancell button not found"
        status = self.driver.click_element(start_scan_button)
        assert status, "Failed to click on Cancel button"

    def search_and_select_dut(self, dut_friendly_name):
        status, dut_to_select = self.driver.find_element('XPATH', locators.text_view_place_holder.format(
            dut_friendly_name))
        assert status, "Failed to find text view matching DUT name:{}".format(dut_friendly_name)
        status = self.driver.click_element(dut_to_select)
        assert status, "Failed to click DUT name to pair"

    def verify_dut_name_visibility(self, dut_friendly_name):
        status = False
        status, dut_name = self.driver.find_element('XPATH', locators.ble_uart_dut_name.format(dut_friendly_name))
        assert status, "Failed to find dut name locator"
        status = self.driver.is_visible(dut_name)
        if status:
            status = True
        else:
            assert status, "DUT is not connected"
        return status