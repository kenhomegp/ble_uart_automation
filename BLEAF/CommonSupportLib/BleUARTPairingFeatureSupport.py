import time
from . import android_locators as locators
from .StationData import stationData
from .AppScanAndConnect import ScanningandConnection
from ..CommonSupportLib.StationData import stationData
from ..StationConfig import conf_file
from ..CommonSupportLib.Serial_Implementaiton import SerialSuppport
sd = stationData()
import sys
import serial
import serial.tools.list_ports
import binascii

dut_friendly_name = conf_file.dut_friendly_name
baud_rate = conf_file.baud_rate
serialPort = ''
flagReadSerialData = True
SERIAL_TIMEOUT_RESP = "TIMEOUT: NO RESPONSE "
com_port = conf_file.com_port
# Wrong Passkey value
wrong_passkey = 123456

class BLEUartPairingSupport:
    def __init__(self, driver=sd.mobile_driver):
        if not driver:
            sd = stationData()
            self.driver = sd.mobile_driver
            print("Driver-##############################################", self.driver)
        else:
            self.driver = driver
            print("Driver-##############################################", self.driver)
        self.scanandconnect = ScanningandConnection()
        self.serialdriver = SerialSuppport()

    def close_settings(self):
        self.driver.close_app()

    def SMP_Event_Parsing(self, dat):
        global receive_serial_str
        print(dat)

        i = 0
        k = 0
        qEvent = []

        while i < len(dat):
            if dat[i] == 0xaa and dat[i + 1] == 0x00:
                j = dat[i + 2]
                i += j + 2 + 1
            if dat[i] == 0xff and dat[i + 1] == 0xff:
                i += 2
                qEvent.append(dat[k:i])
                k = i
            if i == len(dat):
                i += 1

        smpResponse = False
        smpResponseData = ""

        for index in range(len(qEvent)):
            eventBytes = qEvent[index]
            print("event data = " + ''.join('{:02x}'.format(x) for x in eventBytes))

            if eventBytes[3] == 0x50 and eventBytes[4] == 0x80 and eventBytes[5] == 0x03:  # print("SMP Event")
                if eventBytes[6] == 0x05:
                    print("SMP Gen Passkey")
                    ss = eventBytes[9:15]
                    smpResponseData = str(ss, encoding='utf-8')
                    print("PIN CODE = " + smpResponseData)
                    print("SMP Gen Passkey = " + smpResponseData)
                    smpResponse = True
                    break
                elif eventBytes[6] == 0x0a or eventBytes[6] == 0x00:
                    receive_serial_str = ''.join('{:02x}'.format(x) for x in eventBytes)
            elif eventBytes[3] == 0x50 and eventBytes[4] == 0x03 and eventBytes[5] == 0x02:
                print("Display compare value")
                ss = eventBytes[8:14]
                smpResponseData = str(ss, encoding='utf-8')
                print("PIN CODE = " + smpResponseData)
                print("Device display Passkey = " + smpResponseData)
                smpResponse = True
                break
            elif eventBytes[3] == 0x50 and eventBytes[4] == 0x80 and eventBytes[5] == 0x42:
                if eventBytes[6] == 0x03:
                    print("command complete")
                elif eventBytes[6] == 0x04:
                    print("SMP command complete. DevicePairedList = " + str(eventBytes[9]))
                    smpResponseData = str(eventBytes[9])
                    smpResponse = True

        if smpResponse:
            return smpResponseData
        else:
            return smpResponse

    def delete_paired_record_from_phone(self):
        if sd.platform == "OppoR15":
            print("Access Mobile Settings Page")        
            time.sleep(5)            
            print("Access the Bluetooth settings page")                                                           
            status, bluetooth_page = self.driver.find_element('XPATH', locators.oppoR15_bluetooth_settings)
            print("bluetooth_page", status)
            assert status, "Failed to find Bluetooth setting page"           
            status = self.driver.click_element(bluetooth_page)
            print(status)
            assert status, "Failed to click on Bluetooth Page"
            time.sleep(5)
            status, bt_on_off = self.driver.find_element('XPATH', locators.oppoR15_bluetooth_on_off_button)
            assert status, "Failed to locate BT On OFF Button"
            time.sleep(5)
            bt_turn_on_off_status = self.driver.get_text(bt_on_off)
            print("bt_turn_on_off_status", bt_turn_on_off_status)
            if "On" in bt_turn_on_off_status:
                print("Bluetooth is already turned ON")
            else:
                status = self.driver.click_element(bt_on_off)
                assert status, "Failed to click on Bluetooth Turn ON OFF element"
            status, bt_device_forget = self.driver.find_element('XPATH', locators.oppo_R15_bt_device_setting)
            if status:
                print("Unpair the Paired Device")
                status = self.driver.click_element(bt_device_forget)
                assert status, "Failed to click on the device element"
                time.sleep(5)
                status, dut_unpair = self.driver.find_element('XPATH', locators.oppo_R15_forget_device)
                assert status, "Unable to find the Unpair Button"
                if status:
                    print("Click on Unpair")
                    status = self.driver.click_element(dut_unpair)
                    assert status, "Failed to click on Unpair icon"
                    time.sleep(5)
            else:
                print("No Paired record found")

        elif sd.platform == "GooglePixel3A":
            time.sleep(2)
            print("Access Connections in the Settings Page")
            status, connections_page = self.driver.find_element('XPATH', locators.pixel3a_connected_devices)
            assert status, "Failed to find Connections icon"
            status = self.driver.click_element(connections_page)
            time.sleep(2)
            assert status, "Failed to click on Connections icon"
            print("Access Connection preferences in the Settings Page")
            status, connections_preferences = self.driver.find_element('XPATH', locators.pixel3a_connection_preferences)
            assert status, "Failed to find Connections icon"
            status = self.driver.click_element(connections_preferences)
            assert status, "Failed to click on Connection preferences icon"
            status, bluetooth_icon = self.driver.find_element('XPATH', locators.pixel3a_bluetooth_icon)
            print("=== Bluetooth icon Status ===", status)
            assert status, "Failed to find the Bluetooth icon"
            status = self.driver.click_element(bluetooth_icon)
            assert status, "Failed to click Bluetooth Icon"
            time.sleep(5)
            status, bt_on_off = self.driver.find_element('XPATH', locators.pixel3a_bluetooth_on_off_button)
            assert status, "Failed to locate BT On OFF Button"
            time.sleep(5)
            # bt_turn_on_off_status = self.driver.get_text(bt_on_off)
            # if "ON" in bt_turn_on_off_status:
                # print("Bluetooth is already turned ON")
            # else:
                # status = self.driver.click_element(bt_on_off)
                # assert status, "Failed to click on Bluetooth Turn ON OFF element"
            status, bt_back_button = self.driver.find_element('XPATH', locators.pixel3a_back_button)
            assert status, "Failed to find back button"
            status = self.driver.click_element(bt_back_button)
            assert status, "Failed to click on back button"
            time.sleep(5)
            status, bt_back_button = self.driver.find_element('XPATH', locators.pixel3a_back_button)
            assert status, "Failed to find back button"
            status = self.driver.click_element(bt_back_button)
            assert status, "Failed to click on back button"
            status, bt_device_forget = self.driver.find_element('XPATH', locators.pixel3a_bt_device_setting)
            if status:
                print("Unpair the Paired Device")
                device_text = self.driver.get_text(bt_device_forget)
                print(device_text)
                time.sleep(5)
                status = self.driver.click_element(bt_device_forget)
                assert status, "Failed to click on the device element"
                time.sleep(5)
                status, dut_unpair = self.driver.find_element('XPATH', locators.pixel3a_forget_device)
                assert status, "Unable to find the forget Button"
                if status:
                    print("Click on forget")
                    status = self.driver.click_element(dut_unpair)
                    assert status, "Failed to click on forget icon"
                    time.sleep(5)
                    print("Click on forget device")
                    status, bt_confirm_forget = self.driver.find_element('XPATH', locators.pixel3a_confirm_forget_device)
                    assert status, "Failed to find forget device button"
                    status = self.driver.click_element(bt_confirm_forget)
                    assert status, "Failed to click on forget device button"
            else:
                print("No Paired record found")
                
        elif sd.platform == "SamsungS10":
            print("Access Mobile Settings Page")
            print("Access Connections in the Settings Page")
            status, connections_page = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_connected_devices)
            assert status, "Failed to find Connections icon"
            status = self.driver.click_element(connections_page)
            assert status, "Failed to click on Connections icon"
            status, bluetooth_icon = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_bluetooth_icon)
            print("=== Bluetooth icon Status ===", status)
            assert status, "Failed to find the Bluetooth icon"
            status = self.driver.click_element(bluetooth_icon)
            assert status, "Failed to click Bluetooth Icon"
            time.sleep(10)
            status, bt_on_off = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_bluetooth_on_off_button)
            assert status, "Failed to locate BT On OFF Button"
            time.sleep(5)
            bt_turn_on_off_status = self.driver.get_text(bt_on_off)
            print(bt_turn_on_off_status)
            if "On" in bt_turn_on_off_status:
                print("Bluetooth is already turned ON")
            else:
                status = self.driver.click_element(bt_on_off)
                assert status, "Failed to click on Bluetooth Turn ON OFF element"
            status, bt_device_forget = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_bt_device_setting)
            print(status)
            if status:
                status = self.driver.click_element(bt_device_forget)
                print(status)
                assert status, "Failed to click on the device element"
                time.sleep(5)
                status, dut_unpair = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_forget_device)
                assert status, "Unable to find the Unpair Button"
                if status:
                    print("Click on Unpair")
                    time.sleep(5)
                    status = self.driver.click_element(dut_unpair)
                    assert status, "Failed to click on Unpair icon"
                    time.sleep(5)
                    status, dut_unpair_device = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_unpair_device)
                    assert status, "Unable to find the Unpair Button"
                    status = self.driver.click_element(dut_unpair_device)
                    assert status, "Failed to click on Unpair icon"
                    time.sleep(5)                    
            else:
                print("No Paired record found")

        elif sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            print("Access Mobile Settings Page")
            print("Access Connections in the Settings Page")
            status, connections_page = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_connected_devices)
            assert status, "Failed to find Connections icon"
            status = self.driver.click_element(connections_page)
            assert status, "Failed to click on Connections icon"
            status, bluetooth_icon = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_bluetooth_icon)
            print("=== Bluetooth icon Status ===", status)
            assert status, "Failed to find the Bluetooth icon"
            status = self.driver.click_element(bluetooth_icon)
            assert status, "Failed to click Bluetooth Icon"
            time.sleep(10)
            status, bt_on_off = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_bluetooth_on_off_button)
            assert status, "Failed to locate BT On OFF Button"
            time.sleep(5)
            bt_turn_on_off_status = self.driver.get_text(bt_on_off)
            print(bt_turn_on_off_status)
            if "On" in bt_turn_on_off_status:
                print("Bluetooth is already turned ON")
            else:
                status = self.driver.click_element(bt_on_off)
                assert status, "Failed to click on Bluetooth Turn ON OFF element"
            status, bt_device_forget = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_bt_device_setting)
            if status:
                print("Unpair the Paired Device")
                device_text = self.driver.get_text(bt_device_forget)
                print(device_text)
                time.sleep(5)
                status = self.driver.click_element(bt_device_forget)
                assert status, "Failed to click on the device element"
                time.sleep(5)
                status, dut_unpair = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_forget_device)
                assert status, "Unable to find the Unpair Button"
                status = self.driver.click_element(dut_unpair)
                assert status, "Failed to click on Unpair icon"
                status, unpair_button = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_unpair_device)
                assert status, "Unable to find the Unpair pop up"
                if status:
                    print("Click on Unpair")
                    time.sleep(5)
                    status = self.driver.click_element(unpair_button)
                    assert status, "Failed to click on Unpair icon"
                    time.sleep(5)
            else:
                print("No Paired record found")
                
        elif sd.platform == "VivoV11":
            print("Access Mobile Settings Page")
            print("Access Connections in the Settings Page")
            status, connections_page = self.driver.find_element('XPATH', locators.vivoV11_connected_devices)
            assert status, "Failed to find Connections icon"
            status = self.driver.click_element(connections_page)
            assert status, "Failed to click on Connections icon"
            status, bluetooth_icon = self.driver.find_element('XPATH', locators.vivoV11_bluetooth_icon)
            print("=== Bluetooth icon Status ===", status)
            assert status, "Failed to find the Bluetooth icon"
            status = self.driver.click_element(bluetooth_icon)
            assert status, "Failed to click Bluetooth Icon"
            time.sleep(10)
            status, bt_on_off = self.driver.find_element('XPATH', locators.vivoV11_bluetooth)
            assert status, "Failed to locate BT On OFF Button"
            time.sleep(5)
            bt_turn_on_off_status = self.driver.select_checkbox(bt_on_off)
            print("Check for the BT on/off status",bt_turn_on_off_status)
            time.sleep(2)
            status, bt_device_forget = self.driver.find_element('XPATH', locators.vivoV11_bt_device_setting)
            print("DUT element found", status)
            if status:
                status2 = self.driver.click_element(bt_device_forget)
                print(status2)
                assert status2, "Failed to click on the device element"
                print("Unpair the Paired Device")
                time.sleep(10)
                if status:
                    status, dut_unpair = self.driver.find_element('XPATH', locators.vivoV11_forget_device)
                    if status:
                        print("Click on Unpair")
                        time.sleep(5)
                        status3 = self.driver.click_element(dut_unpair)
                        assert status3, "Failed to click on Unpair icon"
                        time.sleep(5)
                    else:
                        print("No Need to unpair because it went to other device field so come back using back button")
                        status3, press_back = self.driver.find_element('XPATH', locators.vivoV11_back_button)
                        status3 = self.driver.click_element(press_back)
                else:
                    print("Unpair the device is not required")
                    print("No Paired record found for the searching DUT device")
                    time.sleep(5)
        else:
            print("\nThe specified platform is not available in the list\n")
        self.close_settings()

    def CloseSerialPort(self, ser):
        print("CloseSerialPort")
        global flagReadSerialData
        flagReadSerialData = False
        ser.close()

    def delete_all_paired_records_from_dut(self):
        status = False
        delete_pairing_record = "AA 00 03 40 42 03 FF"
        delete_pairing_record_resp = "AA0006508042030000FFFF"
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Send command", delete_pairing_record)
        serialPort.write(bytes.fromhex(delete_pairing_record))
        time.sleep(5)
        print("Read data from Serial Port")
        reading = serialPort.read_all()
        time.sleep(5)
        reading = binascii.hexlify(reading).decode('utf-8')
        time.sleep(5)
        serialPort.close()
        print("Data from Serial Port", reading)
        if reading in delete_pairing_record_resp.lower():
            status = True
            print("Deleting All paired records successful.")
        else:
            assert status, "Error in Response"

    def verify_ble_uart_dut_pairing_smp_central_role(self):
        status = False
        smp_central_role = "AA 00 06 40 03 0A 00 00 00 FF"
        smp_central_role_resp = "AA00065080030A0000FFFF"
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Send command", smp_central_role)
        time.sleep(5)
        serialPort.write(bytes.fromhex(smp_central_role))
        print("Read data from Serial Port")
        time.sleep(5)
        reading = serialPort.read_all()
        print("Data from Serial Port", reading)
        time.sleep(5)
        reading = binascii.hexlify(reading).decode('utf-8')
        print("Data from Serial Port", reading)
        serialPort.close()
        if reading in smp_central_role_resp.lower():
            status = True
            print("Central Role SMP command invoked successfully")
        else:
            assert status, "Error in reponse"

    def verify_ble_uart_dut_pairing_smp_peripheral_role(self):
        status = False
        smp_peripheral_role = "AA 00 06 40 03 0A 00 00 01 FF"
        smp_peripheral_role_resp = "AA00065080030A0000FFFF"
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Send command", smp_peripheral_role)
        serialPort.write(bytes.fromhex(smp_peripheral_role))
        time.sleep(5)
        print("Read data from Serial Port")
        reading = serialPort.read_all()
        time.sleep(5)
        reading = binascii.hexlify(reading).decode('utf-8')
        time.sleep(5)
        serialPort.close()
        print("Data from Serial Port", reading)
        if reading in smp_peripheral_role_resp.lower():
            status = True
            print("Peripheral Role SMP command invoked successfully")
        else:
            assert status, "Error in reponse"

    def verify_ble_uart_no_input_no_output_mode(self):
        status = False
        smp_noinput_nooutput = "AA 00 05 40 03 00 03 00 FF"
        smp_noinput_nooutput_resp = "AA0006508003000000FFFF"
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Send command", smp_noinput_nooutput)
        serialPort.write(bytes.fromhex(smp_noinput_nooutput))
        time.sleep(5)
        print("Read data from Serial Port")
        reading = serialPort.read_all()
        time.sleep(5)
        reading = binascii.hexlify(reading).decode('utf-8')
        time.sleep(5)
        print("Data from Serial Port for NoInput No Output", reading)
        if reading in smp_noinput_nooutput_resp.lower():
            print("No Input No Output SMP command invoked successfully")
            status = True
        else:
            assert status, "Error in reponse"
        serialPort.close()

    def verify_ble_uart_display_only_pairing_mode(self, method, key_status):
        status = False
        smp_display_only = "AA 00 05 40 03 00 00 00 FF"
        smp_display_only_resp = "AA0006508003000000FFFF"
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Send command", smp_display_only)
        cmd = bytes([0xaa, 0x00, 0x05, 0x40, 0x03, 0x00, 0x00, 0x00, 0xff])
        serialPort.write(cmd)
        time.sleep(5)
        reading = serialPort.read_all()
        time.sleep(5)
        reading = binascii.hexlify(reading).decode('utf-8')
        time.sleep(5)
        print("Data from Serial Port for Display Only", reading)
        if reading in smp_display_only_resp.lower():
            print("Display Only SMP command invoked successfully")
            status = True
        else:
            assert status, "Error in reponse"
        print("Launch MBD Application")
        status = sd.mobile_driver.launch_app()
        assert status, "Failed to launch application"
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        if method == "peripheral":
            if sd.platform == "SamsungS21" or sd.platform == "SamsungS10" or sd.platform == "SamsungS22":
                bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("First Pairing pop up Displayed")
                    self.pair_device()
            elif sd.platform == "OppoR15":
                bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("First Pairing pop up Displayed")
                    self.pair_device()
            elif sd.platform == "VivoV11":
                status = self.driver.scroll_notification_bar()
                bt_status, bt_text = self.driver.find_element('XPATH', locators.vivoV11_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                    status = self.driver.click_element(bt_text)
                    print("First Pairing pop up Displayed")
                    self.pair_device()
        status = False
        smpData = ''
        Passkey = ''
        print("Read data from Serial Port")
        output_chars = []
        timeout_seconds = 1
        timeout = time.time() + timeout_seconds
        command = ''
        while True:
            # Avoid breaking in the middle of reading a line due to a timeout.
            # If data is available wait for line_terminator or cmd_prompt to break,
            # else break on timeout if no data is available.
            if serialPort.inWaiting():
                read = serialPort.read_all()
                time.sleep(5)
                output_chars.append(read)
                cmdtemp = bytearray()
                for each in output_chars:
                    cmdtemp += bytearray(each)
                command = bytes(cmdtemp)
            elif time.time() > timeout:
                break
        print(command)
        if len(command) >= 6:
            for x in range(len(command)):
                if x != 0 and x + 2 > len(command):
                    break
                if (x + 2) == len(command) and command[x] == 0xff and command[x + 1] == 0xff:
                    smpData = self.SMP_Event_Parsing(command)
                    if type(smpData) is bool and smpData is False:
                        output_chars.clear()
                    elif type(smpData) is str:
                        if len(smpData) == 6:
                            Passkey = smpData
                            print("Passkey", Passkey)
                        else:
                            DevicePairedList = int(smpData)
                            print("Device Paired List", DevicePairedList)
                        output_chars.clear()
                    break
        #Proceed for Passkey Entry
            if sd.platform == "SamsungS21" or sd.platform == "SamsungS10" or sd.platform == "SamsungS22":
                bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                status, passkey_entry_field = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_passkey_entry)
                assert status, "Failed to find the passkey entry field"
                status = self.driver.click_element(passkey_entry_field)
                assert status, "Failed to click on the passkey entry field"
                if key_status == False:
                    print("Enter the wrong key in the passkey field")
                    self.driver.send_keys(passkey_entry_field, wrong_passkey)
                else:
                    print("Enter the correct key in the passkey field")
                    self.driver.send_keys(passkey_entry_field, Passkey)
            elif sd.platform == "VivoV11":
                status = self.driver.scroll_notification_bar()
                bt_status, bt_text = self.driver.find_element('XPATH', locators.vivoV11_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                    status = self.driver.click_element(bt_text)
                status, passkey_entry_field = self.driver.find_element('XPATH', locators.vivoV11_passkey_entry)
                assert status, "Failed to find the passkey entry field"
                status = self.driver.click_element(passkey_entry_field)
                assert status, "Failed to click on the passkey entry field"
                if key_status == False:
                    print("Enter the wrong key in the passkey field")
                    self.driver.send_keys(passkey_entry_field, wrong_passkey)
                else:
                    print("Enter the correct key in the passkey field")
                    self.driver.send_keys(passkey_entry_field, Passkey)
            elif sd.platform == "OppoR15":
                bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                status, passkey_entry_field = self.driver.find_element('XPATH', locators.oppo_R15_passkey_entry)
                assert status, "Failed to find the passkey entry field"
                status = self.driver.click_element(passkey_entry_field)
                assert status, "Failed to click on the passkey entry field"
                if key_status == False:
                    print("Enter the wrong key in the passkey field")
                    self.driver.send_keys(passkey_entry_field, wrong_passkey)
                else:
                    print("Enter the correct key in the passkey field")
                    self.driver.send_keys(passkey_entry_field, Passkey)
        print("Closing the serial port")
        serialPort.close()

    def verify_ble_uart_display_only_pairing_timeout_peripheral(self):
        status = False
        smp_display_only = "AA 00 05 40 03 00 00 00 FF"
        smp_display_only_resp = "AA0006508003000000FFFF"
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Send command", smp_display_only)
        cmd = bytes([0xaa, 0x00, 0x05, 0x40, 0x03, 0x00, 0x00, 0x00, 0xff])
        serialPort.write(cmd)
        time.sleep(5)
        reading = serialPort.read_all()
        time.sleep(5)
        reading = binascii.hexlify(reading).decode('utf-8')
        time.sleep(5)
        print("Closing the serial port")
        serialPort.close()
        print("Data from Serial Port for Display Only", reading)
        if reading in smp_display_only_resp.lower():
            print("Display Only SMP command invoked successfully")
            status = True
        else:
            assert status, "Error in reponse"
        print("Launch MBD Application")
        status = sd.mobile_driver.launch_app()
        assert status, "Failed to launch application"
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)

    def verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(self, mode, method, numeric_comp):
        status = False
        smp_display_yes_no = "AA 00 05 40 03 00 01 00 FF"
        smp_display_yes_no_resp = "AA0006508003000000FFFF"
        smp_keyboard_display = "AA 00 05 40 03 00 04 00 FF"
        smp_keyboard_display_resp = "AA0006508003000000FFFF"
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        if mode == "display_yes_no":
            print("Send command", smp_display_yes_no)
            cmd = bytes([0xaa, 0x00, 0x05, 0x40, 0x03, 0x00, 0x01, 0x00, 0xff])
            serialPort.write(cmd)
            time.sleep(5)
            reading = serialPort.read_all()
            time.sleep(5)
            reading = binascii.hexlify(reading).decode('utf-8')
            time.sleep(5)
            print("Data from Serial Port for mode", mode, reading)
            if reading in smp_display_yes_no_resp.lower():
                print("Display Yes No SMP command invoked successfully")
                status = True
            else:
                assert status, "Error in reponse"
        elif mode == "keyboard_display":
            print("Send command", smp_keyboard_display)
            cmd = bytes([0xaa, 0x00, 0x05, 0x40, 0x03, 0x00, 0x04, 0x00, 0xff])
            serialPort.write(cmd)
            time.sleep(5)
            reading = serialPort.read_all()
            time.sleep(5)
            reading = binascii.hexlify(reading).decode('utf-8')
            time.sleep(5)
            print("Data from Serial Port for {} mode", mode, reading)
            if reading in smp_keyboard_display_resp.lower():
                print("Keyboard Display SMP command invoked successfully")
                status = True
            else:
                assert status, "Error in reponse"
        print("Launch MBD Application")
        status = sd.mobile_driver.launch_app()
        assert status, "Failed to launch application"
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        if method == "peripheral":
            if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
                bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("First Pairing pop up Displayed")
                    self.pair_device()
            elif sd.platform == "OppoR15":
                bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("First Pairing pop up Displayed")
                    self.pair_device()
            if sd.platform == "VivoV11":
                self.vivoV11_pair_device_peripheral()
        #Proceed to read serial Data
        smpData = ''
        Passkey = ''
        print("Read data from Serial Port")
        output_chars = []
        timeout_seconds = 1
        timeout = time.time() + timeout_seconds
        command = ''
        while True:
            # Avoid breaking in the middle of reading a line due to a timeout.
            # If data is available wait for line_terminator or cmd_prompt to break,
            # else break on timeout if no data is available.
            if serialPort.inWaiting():
                read = serialPort.read_all()
                time.sleep(10)
                output_chars.append(read)
                cmdtemp = bytearray()
                for each in output_chars:
                    cmdtemp += bytearray(each)
                command = bytes(cmdtemp)
            elif time.time() > timeout:
                break
        print(command)

        if len(command) >= 6:
            for x in range(len(command)):
                if x != 0 and x + 2 > len(command):
                    break
                if (x + 2) == len(command) and command[x] == 0xff and command[x + 1] == 0xff:
                    smpData = self.SMP_Event_Parsing(command)
                    if type(smpData) is bool and smpData is False:
                        output_chars.clear()
                    elif type(smpData) is str:
                        if len(smpData) == 6:
                            Passkey = smpData
                            print("Passkey", Passkey)
                        else:
                            DevicePairedList = int(smpData)
                            print("Device Paired List", DevicePairedList)
                        output_chars.clear()
                    break
            if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
                bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                status, passkey_field = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_display_yes_no_passkey)
                assert status, "Failed to find the passkey text field"
                capture_passkey = self.driver.get_text(passkey_field)
                print("Text", capture_passkey)
                self.compare_passkey(serialPort,Passkey,capture_passkey,numeric_comp)
            elif sd.platform == "OppoR15":
                bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                status, passkey_field = self.driver.find_element('XPATH', locators.oppo_R15_display_yes_no_passkey)
                assert status, "Failed to find the passkey text field"
                capture_passkey = self.driver.get_text(passkey_field)
                print("Text", capture_passkey)
                self.compare_passkey(serialPort, Passkey, capture_passkey, numeric_comp)
            elif sd.platform == "VivoV11": 
                status = self.driver.scroll_notification_bar()
                bt_status, bt_text = self.driver.find_element('XPATH', locators.vivoV11_displayonly_pairing_req_text)
                assert bt_status, "Failed to find the pairing request pop up"
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                    status = self.driver.click_element(bt_text)
                    status, passkey_field = self.driver.find_element('XPATH',locators.vivoV11_display_yes_no_passkey)
                    assert status, "Failed to find the passkey text field"
                    print(passkey_field) 
                    passkey_field_text = self.driver.get_text(passkey_field)
                    print(passkey_field_text)
                    capture_passkey = passkey_field_text.replace('"','')
                    print("Text", capture_passkey)
                    self.compare_passkey(serialPort, Passkey, capture_passkey, numeric_comp)
        print("Closing the serial port")
        serialPort.close()

    def verify_ble_uart_displayyesno_keyboarddisplay_pairing_timeout(self, mode):
        status = False
        test_status = False
        smp_display_yes_no = "AA 00 05 40 03 00 01 00 FF"
        smp_display_yes_no_resp = "AA0006508003000000FFFF"
        smp_keyboard_display = "AA 00 05 40 03 00 04 00 FF"
        smp_keyboard_display_resp = "AA0006508003000000FFFF"
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        if mode == "display_yes_no":
            print("Send command", smp_display_yes_no)
            cmd = bytes([0xaa, 0x00, 0x05, 0x40, 0x03, 0x00, 0x01, 0x00, 0xff])
            serialPort.write(cmd)
            time.sleep(5)
            reading = serialPort.read_all()
            time.sleep(5)
            reading = binascii.hexlify(reading).decode('utf-8')
            time.sleep(5)
            print("Data from Serial Port for mode", mode, reading)
            if reading in smp_display_yes_no_resp.lower():
                print("Display Yes No SMP command invoked successfully")
                status = True
            else:
                assert status, "Error in reponse"
        elif mode == "keyboard_display":
            print("Send command", smp_keyboard_display)
            cmd = bytes([0xaa, 0x00, 0x05, 0x40, 0x03, 0x00, 0x04, 0x00, 0xff])
            serialPort.write(cmd)
            time.sleep(5)
            reading = serialPort.read_all()
            time.sleep(5)
            reading = binascii.hexlify(reading).decode('utf-8')
            time.sleep(5)
            print("Data from Serial Port for {} mode", mode, reading)
            if reading in smp_keyboard_display_resp.lower():
                print("Keyboard Display SMP command invoked successfully")
                status = True
            else:
                assert status, "Error in reponse"
        print("Launch MBD Application")
        status = sd.mobile_driver.launch_app()
        assert status, "Failed to launch application"
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify for Pairing Timeout")
        time.sleep(30)        
        serialPort.close()

    def verify_ble_uart_keyboard_only_pairing_mode(self, method, key_status):
        status = False
        test_status = False
        wrong_key = '123456'
        smp_keyboard_only = "AA 00 05 40 03 00 02 00 FF"
        smp_keyboard_only_resp = "AA0006508003000000FFFF"
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Send command", smp_keyboard_only)
        cmd = bytes([0xaa, 0x00, 0x05, 0x40, 0x03, 0x00, 0x02, 0x00, 0xff])
        serialPort.write(cmd)
        time.sleep(5)
        reading = serialPort.read_all()
        time.sleep(5)
        reading = binascii.hexlify(reading).decode('utf-8')
        time.sleep(5)
        print("Data from Serial Port for Display Only", reading)
        if reading in smp_keyboard_only_resp.lower():
            print("Keyboard Only SMP command invoked successfully")
            status = True
        else:
            assert status, "Error in reponse"
        print("Launch MBD Application")
        status = sd.mobile_driver.launch_app()
        assert status, "Failed to launch application"
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        if method == "peripheral":
            if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
                bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("First Pairing pop up Displayed")
                    self.pair_device()
            elif sd.platform == "OppoR15":
                bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("First Pairing pop up Displayed")
                    self.pair_device()
            elif sd.platform == "VivoV11":
                self.vivoV11_pair_device_peripheral()
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
            if bt_status:
                status = self.driver.is_visible(bt_text)
                print("Pairing pop up Displayed")
            status, passkey_field = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_keyboard_only_passkey)
            assert status, "Failed to find the passkey text field"
            capture_passkey = self.driver.get_text(passkey_field)
            print("Text", capture_passkey)
            if "Enter " in capture_passkey:
                test_status = True
                pos = capture_passkey.find("Enter")
                print(pos)
                app_display_pin_code = capture_passkey[(pos + 6):(pos + 12)]
                print(app_display_pin_code)
                print("Send passkey")
                self.compare_passkeystatus(serialPort, key_status, app_display_pin_code)
            else:
                print("Passkey is not visible")
                assert test_status, "Passkey is not visible"
        elif sd.platform == "OppoR15":
            bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
            if bt_status:
                status = self.driver.is_visible(bt_text)
                print("Pairing pop up Displayed")
            status, passkey_field = self.driver.find_element('XPATH', locators.oppo_R15_keyboard_only_passkey)
            assert status, "Failed to find the passkey text field"
            capture_passkey = self.driver.get_text(passkey_field)
            print("Text", capture_passkey)
            if "enter: " in capture_passkey:
                test_status = True
                pos = capture_passkey.find("enter:")
                app_display_pin_code = capture_passkey[(pos + 8):(pos + 14)]
                print(app_display_pin_code)
                print("Send passkey")
                self.compare_passkeystatus(serialPort, key_status, app_display_pin_code)
            else:
                print("Passkey is not visible")
                assert test_status, "Passkey is not visible"
        elif sd.platform == "VivoV11":
            status = self.driver.scroll_notification_bar()
            bt_status, bt_text = self.driver.find_element('XPATH', locators.vivoV11_displayonly_pairing_req_text)
            print(bt_text)
            if bt_status:
                status = self.driver.is_visible(bt_text)
                status = self.driver.click_element(bt_text)
                print("Pairing pop up Displayed")
            status, passkey_field = self.driver.find_element('XPATH', locators.vivoV11_keyboard_only_passkey)
            assert status, "Failed to find the passkey text field"
            print(passkey_field) 
            passkey_field_text = self.driver.get_text(passkey_field)
            print(passkey_field_text)
            passkey_str = passkey_field_text.replace('"','')
            capture_passkey = " ".join(passkey_str.split())
            print("Text", capture_passkey)
            if "key in " in capture_passkey:
                test_status = True
                print("Get the code which is shown on the phone")
                pos = capture_passkey.find("key in")
                print(pos)
                app_display_pin_code = capture_passkey[(pos + 7):(pos + 13)]
                print(app_display_pin_code)
                print("Send passkey")
                self.compare_passkeystatus(serialPort, key_status, app_display_pin_code)
            else:
                print("Passkey is not visible")
                assert test_status, "Passkey is not visible"
        print("Closing the serial port")
        serialPort.close()

    def verify_ble_uart_keyboard_only_pairing_mode_cancel_timeout_pairing(self):
        status = False
        test_status = False
        smp_keyboard_only = "AA 00 05 40 03 00 02 00 FF"
        smp_keyboard_only_resp = "AA0006508003000000FFFF"
        serialPort = self.serialdriver.ComportSet(com_port, baud_rate)
        print("Send command", smp_keyboard_only)
        cmd = bytes([0xaa, 0x00, 0x05, 0x40, 0x03, 0x00, 0x02, 0x00, 0xff])
        serialPort.write(cmd)
        time.sleep(5)
        reading = serialPort.read_all()
        time.sleep(5)
        reading = binascii.hexlify(reading).decode('utf-8')
        time.sleep(5)
        print("Data from Serial Port for Display Only", reading)
        if reading in smp_keyboard_only_resp.lower():
            print("Keyboard Only SMP command invoked successfully")
            status = True
        else:
            assert status, "Error in reponse"
        print("Launch MBD Application")
        status = sd.mobile_driver.launch_app()
        assert status, "Failed to launch application"
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        serialPort.close()
        
    def compare_passkey(self,serialPort, passkey, capture_passkey,numeric_comp):
        test_status = False
        if passkey in capture_passkey:
            test_status = True
            if numeric_comp == "yes":
                print("Write command for Numeric Comparison Yes if the Passkey matches")
                mumeric_comparison_yes_cmd = bytes([0xaa, 0x00, 0x06, 0x40, 0x03, 0x03, 0x00, 0x00, 0x00, 0xff])
                serialPort.write(mumeric_comparison_yes_cmd)
                self.pair_device()
            elif numeric_comp == "no":
                print("Write command for Numeric Comparison NO")
                mumeric_comparison_no_cmd = bytes([0xaa, 0x00, 0x06, 0x40, 0x03, 0x03, 0x00, 0x00, 0x01, 0xff])
                serialPort.write(mumeric_comparison_no_cmd)
            else:
                print("Neither Yes nor No, Attempting to cancel the Pairing Request via Phone")
        else:
            print("Passkey does not match")
            assert test_status, "Passkey does not match"

    def compare_passkeystatus(self, serialPort, key_status, app_display_pin_code):
        wrong_key = '123456'
        if key_status == False:
            cmdTmp = bytearray(b'\xaa\x00\x0b@\x03\x01ww')
            cmdTmp += bytearray(wrong_key.encode('utf-8'))
            cmdTmp.append(255)
            print('Write command: ' + ''.join('{:02x}'.format(x) for x in cmdTmp))
            print('Send SMP command: Wrong Passkey')
            print("Enter the wrong key in the passkey field")
            serialPort.write(cmdTmp)
        else:
            cmdTmp = bytearray(b'\xaa\x00\x0b@\x03\x01ww')
            cmdTmp += bytearray(app_display_pin_code.encode('utf-8'))
            cmdTmp.append(255)
            print('Write command: ' + ''.join('{:02x}'.format(x) for x in cmdTmp))
            print('Send SMP command: Passkey')
            print("Enter the correct key in the passkey field")
            serialPort.write(cmdTmp)
            time.sleep(3)

    def vivoV11_pair_device(self):
        print("scroll notification bar")
        # status = self.driver.scroll_notification_bar()
        # status, pair_device = self.driver.find_element('XPATH', locators.vivoV11_displayonly_pairing_req_text)
        # assert status, "Pairing request icon not found"
        # status = self.driver.click_element(pair_device)
        status, pair_device1 = self.driver.find_element('XPATH', locators.vivoV11_ok_button)
        assert status, "Pair icon not found"
        status = self.driver.click_element(pair_device1)
        assert status, "Unable to click on the Pair icon"

    def device_pair_ok_peripheral(self):
        status, pair_device = self.driver.find_element('XPATH', locators.vivoV11_ok_button)
        assert status, "Pair icon not found"
        status = self.driver.click_element(pair_device)
        assert status, "Unable to click on the Pair icon"

    def vivoV11_pair_device_peripheral(self):
        print("scroll notification bar")
        status = self.driver.scroll_notification_bar()
        status, pair_device = self.driver.find_element('XPATH', locators.vivoV11_displayonly_pairing_req_text)
        assert status, "Pairing request icon not found"
        status = self.driver.click_element(pair_device)
        status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
        assert status, "Pair icon not found"
        status = self.driver.click_element(pair_device)
        assert status, "Unable to click on the Pair icon"

    def vivoV11_device_cancel_pair(self):
        status = self.driver.scroll_notification_bar()
        bt_status, bt_text = self.driver.find_element('XPATH', locators.vivoV11_displayonly_pairing_req_text)
        status = self.driver.click_element(bt_text)
        status, cancel_pair = self.driver.find_element('XPATH', locators.device_cancel_pair)
        assert status, "Cancel icon not found"
        status = self.driver.click_element(cancel_pair)
        assert status, "Unable to click on the Cancel icon"

    def vivoV11_peripherial_cancel_pair(self):
        status, cancel_pair = self.driver.find_element('XPATH', locators.device_cancel_pair)
        assert status, "Cancel icon not found"
        status = self.driver.click_element(cancel_pair)
        assert status, "Unable to click on the Cancel icon"

    def pair_device(self):
        status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
        assert status, "Pair icon not found"
        status = self.driver.click_element(pair_device)
        assert status, "Unable to click on the Pair icon"

    def cancel_pair(self):
        status, cancel_pair = self.driver.find_element('XPATH', locators.device_cancel_pair)
        assert status, "Cancel icon not found"
        status = self.driver.click_element(cancel_pair)
        assert status, "Unable to click on the Cancel icon"

    def samsungs10_s21_s22_pair_device_peripheral(self):
        status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
        assert status, "Pair icon not found"
        status = self.driver.click_element(pair_device)
        assert status, "Unable to click on the Pair icon"
        time.sleep(3)
        # Pair pop up will appear another time
        status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
        assert status, "Pair icon not found"
        time.sleep(3)
        status = self.driver.click_element(pair_device)
        assert status, "Unable to click on the Pair icon"