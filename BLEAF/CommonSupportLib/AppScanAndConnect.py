import time

from lxml.doctestcompare import strip

from . import android_locators as locators
from .StationData import stationData
from ..StationConfig import conf_file
from ..CommonSupportLib.Serial_Implementaiton import SerialSuppport
import threading

import sys
import serial
import serial.tools.list_ports
sd = stationData()
result_str = ""
com_port = conf_file.com_port
baud_rate = conf_file.baud_rate

class ScanningandConnection:
    def __init__(self, driver=sd.mobile_driver):
        if not driver:
            sd = stationData()
            self.driver = sd.mobile_driver
            print("Driver-##############################################", self.driver)
        else:
            self.driver = driver
            print("Driver-##############################################", self.driver)
        self.serialdriver = SerialSuppport()
    
    def verify_app_open(self):
        status = False
        print("Checking if the MBD app is open")
        status, dashboard_text = self.driver.find_element('XPATH', locators.dashboard_text)
        if status:
            status = self.driver.is_visible(dashboard_text)
            print("MBD Application opened.")
        return status
    
    def open_ble_uart_scanner(self):
        error_msg = ""
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

    def open_ble_sensor_scanner(self):
        error_msg = ""
        print("Click BLE Sensor")
        status, ble_sensor_icon = self.driver.find_element('XPATH', locators.ble_sensor_icon)
        assert status, "BLE Sensor Icon not found"

        status = self.driver.click_element(ble_sensor_icon)
        assert status, "Failed to open BLE Sensor page"

        status, ble_uart_sensor_scanner = self.driver.find_element('XPATH', locators.ble_uart_sensor_scanner)
        assert status, "Coming soon option not found"

        status = self.driver.click_element(ble_uart_sensor_scanner)
        assert status, "Failed to open BLE Sensor page"

        status, scan_button = self.driver.find_element('XPATH', locators.scan_button)
        assert status, "Scan button not found"

        status = self.driver.is_visible(scan_button)
        assert status, "Scan button not visible"
        
    def verify_uart_scanner_page(self):
        status, scan_button = self.driver.click_element('XPATH', locators.scan_button)
        assert status, "Scan button not found"
    
        status = self.driver.is_visible(scan_button)
        assert status, "Scan button not visible"
    
        
    def navigate_back(self):
        self.driver.click_back_button()
        print("\n Please wait for 5 secs")
        time.sleep(5)
    
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
        print("Searching for the DUT : {}".format(dut_friendly_name))
        iter = 1
        while iter <= 5:
            iter=iter+1
            status, dut_to_select = self.driver.find_element('XPATH', locators.text_view_place_holder.format(
                dut_friendly_name))
            if not status:
                self.click_start_scan()
                time.sleep(15)
                self.click_cancel_button()
                time.sleep(2)
            if status:
                break
        assert status, "Failed to find text view matching DUT name:{}".format(dut_friendly_name)
        status = self.driver.click_element(dut_to_select)
        assert status, "Failed to click DUT name to pair"

    def verify_dut_paired(self):
        error_msg = ""
        status, service_list_text = self.driver.find_element('XPATH',
                                                             locators.text_view_place_holder.format('Service List'))
        if not status:
            error_msg = "Service List page not found."
        return status, error_msg
    
    def scan_and_connect_dut(self, dut_friendly_name):
        self.open_ble_uart_scanner()
        time.sleep(2)
        self.click_start_scan()
        print("Please wait for 15 sec to scan the devices")
        time.sleep(15)
        print("Press Cancel button to stop scanning")
        self.click_cancel_button()

        self.search_and_select_dut(dut_friendly_name)


    def ble_sensor_scan_and_connect_dut(self, dut_friendly_name):
        self.open_ble_sensor_scanner()

        self.click_start_scan()
        print("\n Please wait for 15 sec to scan the devices") 
        time.sleep(15)
        self.search_and_select_dut(dut_friendly_name)
        print("\n Please wait for 10 secs")
        time.sleep(10)

    def scan_and_connect_disconnect_dut(self, dut_friendly_name):
        self.open_ble_uart_scanner()

        self.click_start_scan()
        print("\n Please wait for 15 sec to scan the devices") 
        time.sleep(15)
        print("\n Press Cancel button to stop scanning")
        self.click_cancel_button()

        self.search_and_select_dut(dut_friendly_name)
        print("\n Please wait for 10 secs")
        time.sleep(10)
        status = self.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        print("Disconnect the DUT")
        self.driver.go_back()
        print("\n Please wait for 10 secs")
        time.sleep(10)

    def scan_and_connect_disconnect_dut_stresstest(self, dut_friendly_name):
        print("Scan and Connect to the DUT")
        self.click_start_scan()
        print("\n Please wait for 15 sec to scan the devices")
        time.sleep(15)
        print("\n Press Cancel button to stop scanning")
        self.click_cancel_button()

        self.search_and_select_dut(dut_friendly_name)
        print("Verifying the connection stability for 2 minutes")
        #Adding delay of 120 secs
        time.sleep(120)
        status = self.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        print("Disconnect the DUT")
        self.driver.go_back()
        print("Verifying the disconnection status for 1 minute\n")
        # Adding delay of 60 secs
        time.sleep(60)

    def verify_raw_data_mode(self):
        status, text_mode_icon = self.driver.find_element('XPATH', locators.raw_data_icon)
        assert status, "Failed to find the raw data icon"
        status = self.driver.click_element(text_mode_icon)
        assert status, "Failed to click on the raw data icon"
        time.sleep(1)

    def confirm_raw_data_mode_trp(self):
        status = False
        status, confirm_raw_trp = self.driver.find_element('XPATH', locators.confirm_raw_data_trp)
        if status:
            status = self.driver.is_visible(confirm_raw_trp)
            print("Raw data - TRP is set accordingly")
        return status

    def confirm_raw_data_mode_trcbp(self):
        status = False
        status, confirm_raw_trcbp = self.driver.find_element('XPATH', locators.confirm_raw_data_trcbp)
        if status:
            status = self.driver.is_visible(confirm_raw_trcbp)
            print("Raw data - TRCBP is set accordingly")
        return status

    def switch_raw_data_to_burst_mode(self):
        status, text_mode_icon = self.driver.find_element('XPATH', locators.raw_data_icon)
        assert status, "Failed to find the raw data icon"
        status = self.driver.click_element(text_mode_icon)
        assert status, "Failed to switch to raw data icon"
        time.sleep(5)
        status, burst_mode_icon = self.driver.find_element('XPATH', locators.burst_mode_icon)
        assert status, "Failed to find the burst mode icon"
        status = self.driver.click_element(burst_mode_icon)
        assert status, "Failed to switch to burst mode icon from text mode"
        time.sleep(5)

    def confirm_raw_data_loopbackmode_trp(self):
        status = False
        status, confirm_raw_loopback = self.driver.find_element('XPATH', locators.raw_data_loopback_confirm_trp)
        if status:
            status = self.driver.is_visible(confirm_raw_loopback)
            print("Raw data, TRP - Loopback mode is set accordingly")
        return status

    def confirm_raw_data_loopbackmode_trcbp(self):
        status = False
        status, confirm_raw_loopback = self.driver.find_element('XPATH', locators.raw_data_loopback_confirm_trcbp)
        if status:
            status = self.driver.is_visible(confirm_raw_loopback)
            print("Raw data, TRCBP - Loopback mode is set accordingly")
        return status

    def confirm_raw_data_uart_trp(self):
        status = False
        status, confirm_raw_uart = self.driver.find_element('XPATH', locators.raw_data_uart_confirm_trp)
        if status:
            status = self.driver.is_visible(confirm_raw_uart)
            print("Raw data - UART mode, TRP is set accordingly")
        return status

    def confirm_raw_data_uart_trcbp(self):
        status = False
        status, confirm_raw_uart = self.driver.find_element('XPATH', locators.raw_data_uart_confirm_trcbp)
        if status:
            status = self.driver.is_visible(confirm_raw_uart)
            print("Raw data - UART mode, TRCBP is set accordingly")
        return status

    def send_raw_data_loopback_mode(self):
        input_data0 = "RAW Data Tests"
        input_data1 = "1234567890"
        input_data2 = "ABCDEFGHIJKLMNOPQ!@#$%^&*()"
        input_data3 = "Areyoulookingforonlinereadingactivities?\
                       Howaboutinteractivepracticeactivitiestargetingspecificreadingskills?"
        input_data4 = "BLE UART Feature RAW DATA"
        status, raw_text_field = self.driver.find_element('XPATH', locators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        assert status, "Failed to find the raw data text field to input"
        self.driver.send_keys(raw_text_field, input_data2)
        time.sleep(5)
        status = self.send_data(input_data2)
        assert status, "Test Fails as the comparison is not successful"
        return status

    def send_data(self, input_data):
        status = False
        pass_string = "Comparison Success"
        TX_string = "[TX]:"+input_data
        RX_string = "[RX]:"+input_data
        status, send_button = self.driver.find_element('XPATH', locators.send_button)
        assert status, "Failed to find the SEND icon element"
        status = self.driver.click_element(send_button)
        assert status, "Failed to click on SEND icon"
        result_status, pass_status = self.driver.find_element('XPATH', locators.raw_data_log_message)
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

    def send_raw_data_loopback_mode_stresstest(self, input_data):
        time.sleep(2)
        status, raw_text_field = self.driver.find_element('XPATH', locators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        assert status, "Failed to find the raw data text field to input"
        self.driver.send_keys(raw_text_field, input_data)
        time.sleep(5)
        status = self.send_data(input_data)
        assert status, "Test Fails as the comparison is not successful"
        time.sleep(5)
        self.driver.go_back()
        status_clear, clear_text = self.driver.find_element('XPATH', locators.raw_clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        return status

    def send_data_uart(self, input_data):
        status = False
        TX_string = "[TX]:"+input_data
        status, send_button = self.driver.find_element('XPATH', locators.send_button)
        assert status, "Failed to find the SEND icon element"
        time.sleep(5)
        status = self.driver.click_element(send_button)
        assert status, "Failed to click on SEND icon"
        time.sleep(5)
        result_status, pass_status = self.driver.find_element('XPATH', locators.raw_data_log_message)
        assert result_status, "Failed to find the raw data log message"
        pass_status_get_text = self.driver.get_text(pass_status)
        if (TX_string in pass_status_get_text):
            print("TX input is matching. Data sent correctly")
            status = True
        else:
            status = False
            print("TX input is not matching. Data mismatch")
        return status

    def read_serial_port(self, ser, input_data):
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
        ser.write(input_data)

    def send_raw_data_uart_mode_app_to_dut(self):
        input_data = "ABCDEFGHIJKLMNOPQ!@#$%^&*()"
        time.sleep(2)
        status, raw_text_field = self.driver.find_element('XPATH', locators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        assert status, "Failed to find the raw data text field to input"
        self.driver.send_keys(raw_text_field, input_data)
        time.sleep(5)
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        status = self.send_data_uart(input_data)
        assert status, "Test Fails as the comparison is not successful"
        read_data = self.read_serial_port(serialPort, input_data)
        print(read_data)
        serialPort.close()
        if read_data == input_data:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        return status


    def send_raw_data_uart_mode_app_to_dut_300(self):
        input_data = "In 2022, the company achieved a remarkable milestone by increasing its revenue by 15%, reaching a total of $5.3 million. This success was driven by the launch of three new products: the X-200, Y-300, and Z-400. Additionally, the team expanded from 50 to 75 employees, enhancing our capacity to serve clients across 12 different countries. #Success #Growth"
        status, raw_text_field = self.driver.find_element('XPATH', locators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        assert status, "Failed to find the raw data text field to input"
        self.driver.send_keys(raw_text_field, input_data)
        time.sleep(5)
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        status = self.send_data_uart(input_data)
        assert status, "Test Fails as the comparison is not successful"
        read_data = self.read_serial_port(serialPort, input_data)
        print(read_data)
        serialPort.close()
        if read_data == input_data:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        return status


    def send_raw_data_uart_mode_app_to_dut_stress_test(self, input_data):
        status, raw_text_field = self.driver.find_element('XPATH', locators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        time.sleep(5)
        assert status, "Failed to find the raw data text field to input"
        self.driver.send_keys(raw_text_field, input_data)
        time.sleep(15)
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        time.sleep(5)
        status = self.send_data_uart(input_data)
        assert status, "Test Fails as the comparison is not successful"
        time.sleep(5)
        read_data = self.read_serial_port(serialPort, input_data)
        print(read_data)
        serialPort.close()
        self.driver.go_back()
        status_clear, clear_text = self.driver.find_element('XPATH', locators.raw_clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        if read_data == input_data:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        return status
        
    def send_raw_data_uart_mode_dut_to_app(self):
        input_data = "ABCDEFGHIJKLMNOPQ!@#$%^&*()"
        time.sleep(2)
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Checking for input string", input_data)
        self.write_serial_port(serialPort, input_data)
        time.sleep(5)
        serialPort.close()
        result_status, pass_status = self.driver.find_element('XPATH', locators.raw_data_log_message)
        assert result_status, "Failed to find the raw data log message"
        pass_status_get_text = self.driver.get_text(pass_status)
        if input_data in pass_status_get_text:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        return status


    def send_raw_data_uart_mode_dut_to_app_300(self):
        input_data = "In 2022, the company achieved a remarkable milestone by increasing its revenue by 15%, reaching a total of $5.3 million. This success was driven by the launch of three new products: the X-200, Y-300, and Z-400. Additionally, the team expanded from 50 to 75 employees, enhancing our capacity to serve clients across 12 different countries. #Success #Growth"
        time.sleep(2)
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Checking for input string", input_data)
        self.write_serial_port(serialPort, input_data)
        time.sleep(5)
        serialPort.close()
        result_status, pass_status = self.driver.find_element('XPATH', locators.raw_data_log_message)

        assert result_status, "Failed to find the raw data log message"
        pass_status_get_text = self.driver.get_text(pass_status)
        print(pass_status_get_text)
        pass_status_get_text = pass_status_get_text.replace('[RX]:','').replace('\n','')
        print(pass_status_get_text)
        if input_data in pass_status_get_text:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        return status, pass_status_get_text


    def send_raw_data_uart_mode_dut_to_app_stress_test(self, input_data):
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Checking for input string", input_data)
        self.write_serial_port(serialPort, input_data)
        time.sleep(5)
        serialPort.close()
        result_status, pass_status = self.driver.find_element('XPATH', locators.raw_data_log_message)
        assert result_status, "Failed to find the raw data log message"
        pass_status_get_text = self.driver.get_text(pass_status)
        time.sleep(1)
        status_clear, clear_text = self.driver.find_element('XPATH', locators.raw_clear_text)
        assert status_clear, "Failed to find the clear icon"
        status_clear = self.driver.click_element(clear_text)
        assert status_clear, "Failed to click on clear icon"
        time.sleep(1)
        if input_data in pass_status_get_text:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        return status

    def verify_dut_name_visibility(self, dut_friendly_name):
        status = False
        status, dut_name = self.driver.find_element('XPATH', locators.ble_uart_dut_name.format(dut_friendly_name))
        assert status, "Failed to find dut name in the page as DUT may not be connected"
        status = self.driver.is_visible(dut_name)
        if status:
            status = True
        else:
            assert status, "DUT is not connected"
        return status

    def verify_dut_name_non_visibility(self,dut_friendly_name):
        status = False
        result_string = ""
        status, dut_name = self.driver.find_element('XPATH', locators.ble_uart_dut_name.format(dut_friendly_name))
        if not status:
            print("DUT is not connected")
            result_string = "DUT is not connected, Kill MBD App successful"
            status = True
        else:
            result_string = "DUT is connected, Test case fail"
            assert status, "DUT is connected, Test case fail"
        return status, result_string

    def confirm_connparm_page(self):
        status = False
        status, confirm_connpar_page = self.driver.find_element('XPATH', locators.confirm_Connparam_page)
        time.sleep(10)
        if status:
            status = self.driver.is_visible(confirm_connpar_page)
            print("Raw data - Connection interval parameter page is open")
        return status

    def set_connection_interval_parameters(self, min_interval, max_interval, latency_value, supervison_value):
        status = False
        print("Update minimum interval value :",min_interval)
        status, mininterval_field = self.driver.find_element('XPATH', locators.min_interval_field)
        assert status, "Failed to find the minimum interval field"
        status = self.driver.click_element(mininterval_field)
        assert status, "Failed to find the minimum interval field to input"
        self.driver.send_keys(mininterval_field, min_interval)
        time.sleep(5)
        print("Update maximum interval value :",max_interval )
        status, maxinterval_field = self.driver.find_element('XPATH', locators.max_interval_field)
        assert status, "Failed to find the maximum interval field"
        status = self.driver.click_element(maxinterval_field)
        assert status, "Failed to find the maximum interval field to input"
        self.driver.send_keys(maxinterval_field, max_interval)
        time.sleep(5)
        print("Update latency value :",latency_value)
        self.driver.go_back()
        status, latencyvalue_field = self.driver.find_element('XPATH', locators.latency_value_field)
        assert status, "Failed to find the latency value field"
        status = self.driver.click_element(latencyvalue_field)
        assert status, "Failed to find the latency value field to input"
        self.driver.send_keys(latencyvalue_field, latency_value)
        time.sleep(5)
        print("Update Supervision timeout value :",supervison_value)
        self.driver.go_back()
        time.sleep(5)
        status, supervisonvalue_field = self.driver.find_element('XPATH', locators.supervison_value_field)
        assert status, "Failed to find the Supervision Value interval field"
        status = self.driver.click_element(supervisonvalue_field)
        assert status, "Failed to find the supervison value interval field to input"
        self.driver.send_keys(supervisonvalue_field, supervison_value)
        self.driver.go_back()
        time.sleep(10)
        status, save_button = self.driver.find_element('XPATH', locators.save_button)
        assert status, "Failed to find the SAVE icon element"
        status = self.driver.click_element(save_button)
        print("click on save")
        assert status, "Failed to click on Save icon"
        time.sleep(10)
        result_status, pass_status = self.driver.find_element('XPATH', locators.raw_data_log_message)
        assert result_status, "Failed to find the raw data log message"
        time.sleep(10)
        pass_status_get_text = self.driver.get_text(pass_status)
        print(pass_status_get_text)
        if "Connection Param Update Success" in pass_status_get_text:
            status = True
            print("Successfuly updated connection interval parameter")
        else:
            status = False
            print("Failed to update connection interval parameter")
        return status

    def verify_scan_page_visiblity(self):
        status = False
        time.sleep(1)
        status, scan_page = self.driver.find_element('XPATH', locators.scan_button)
        assert status, "Failed to find the scan icon element in the mobile app"
        time.sleep(1)
        status = self.driver.is_visible(scan_page)
        if status:
            print("SCAN page is visible")
        else:
            assert status, "SCAN page is not visible"
        return status

    def verify_fw_rev(self, FWVerValue):
        status = False
        fail_text = "Firmware version is not mentioned"
        text = "Firmware Version does not match"
        status, device_info = self.driver.find_element('XPATH', locators.device_info)
        if status:
            visible = self.driver.is_visible(device_info)
            if visible:
                print("Collect the device information")
                status1, firmware_version = self.driver.find_element('XPATH', locators.firmware_version)
                assert status1, "Failed to find the element on FW version section"
                fw_text = self.driver.get_text(firmware_version)
                if str(fw_text) in FWVerValue:
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

    def scan_and_reconnect_dut(self, dut_friendly_name):
        self.click_start_scan()
        print("Please wait for 15 sec to scan the devices")
        time.sleep(15)
        print("Press Cancel button to stop scanning")
        self.click_cancel_button()
        self.search_and_select_dut(dut_friendly_name)
        time.sleep(1)

    def loopback_mode_raw_trp(self):
        self.verify_raw_data_mode()
        self.confirm_raw_data_mode_trp()


    def loopback_mode_raw_trcbp(self):
        self.verify_raw_data_mode()
        self.confirm_raw_data_mode_trp()

    def click_dut_name_opporeno_log(self):
        oppo = self.driver.click_dut_name_opporeno()

    def get_fw_rev(self):
        status = False
        fail_text = "Firmware version is not mentioned"
        text = "Firmware Version does not match"
        status, device_info = self.driver.find_element('XPATH', locators.device_info)
        if status:
            visible = self.driver.is_visible(device_info)
            if visible:
                print("Collect the device information")
                status1, firmware_version = self.driver.find_element('XPATH', locators.firmware_version)
                assert status1, "Failed to find the element on FW version section"
                fw_text = self.driver.get_text(firmware_version)
                return fw_text
            else:
                return False
        else:
            return False

    def open_ble_smart_scanner(self):
        status, ble_uart_icon = self.driver.find_element('XPATH', locators.bluetooth_smart_icon)
        assert status, "BLE Smart Icon not found"
        status = self.driver.click_element(ble_uart_icon)
        assert status, "Failed to open BLE Smart page"