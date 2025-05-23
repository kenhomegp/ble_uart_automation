import os
import time
import json

from . import android_locators as locators
from ..CommonSupportLib.StationData import stationData
from ..StationConfig import conf_file
from ..CommonSupportLib.Serial_Implementaiton import SerialSuppport
from ..CommonSupportLib.BleUARTPairingFeatureSupport import BLEUartPairingSupport

sd = stationData()

baudrate = conf_file.baud_rate
comport = conf_file.com_port

class RNBDvsPhoneFeatureSupport:
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
        self.bleuartpairingfeature = BLEUartPairingSupport()

    def Send_Receive_Msg(self,comport,sendmsg,recmsg,timeout=1):
        result =""
        timecnt = 0
        try:
            if self.serialdriver.ComportCheck(comport) == False:
                print('Com Port Connect fail , Please Check the Port status')
                return False

            com = self.serialdriver.ComportSet(comport,baudrate)
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

    def Read_json_file(self,command_set):
        step_result = []
        step_descript = []
        json_file = os.getcwd() + "\Tests\RNBD45x_JSON_File\RNBD45x_vs_Phone_Command_Set.json"
        with open(json_file) as f:
            testSet = json.load(f)
        f.close()
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

    def verify_lightblue_app_open(self):
        status = False
        status, dashboard_text = self.driver.find_element('XPATH', locators.lightblue_dashboard_text)
        if status:
            status = self.driver.is_visible(dashboard_text)
            print("LightBlue Application opened.")
        return status

    def lightblue_scan_and_connect_dut(self, dut_friendly_name):
        status, more_icon = self.driver.find_element('XPATH', locators.lightblue_more_icon)
        status = self.driver.click_element(more_icon)
        assert status, "Failed to click on more icon"
        status, refresh_page = self.driver.find_element('XPATH', locators.lightblue_refresh_page)
        status = self.driver.click_element(refresh_page)
        assert status, "Failed to click on refresh"
        print("click on search icon")
        status, search_icon = self.driver.find_element('XPATH', locators.lightblue_serach_icon)
        assert status, "Failed to find the search icon in the mobile app"
        status = self.driver.click_element(search_icon)
        assert status, "Failed to click on search"
        print("click on search field and enter DUT name")
        if sd.platform == "GooglePixel3A" or sd.platform == "OppoR15":
            status, search_field = self.driver.find_element('XPATH', locators.pixel3A_lightblue_serach_field)
        else:
            status, search_field = self.driver.find_element('XPATH', locators.lightblue_serach_field)
        time.sleep(5)
        self.driver.send_keys(search_field, dut_friendly_name)
        status, dut_to_select = self.driver.find_element('XPATH',
                                                         locators.text_view_place_holder.format(dut_friendly_name))
        assert status, "Failed to find text view matching DUT name:{}".format(dut_friendly_name)
        status, connect_dut = self.driver.find_element('XPATH', locators.lightblue_connect_icon)
        assert status, "Failed to find the connect icon in the mobile app"
        status = self.driver.click_element(connect_dut)
        assert status, "Failed to click on connect"

    def verify_rnbd_dut_name_visibility(self,dut_friendly_name):
        status = False
        status, dut_name = self.driver.find_element('XPATH', locators.ble_uart_dut_name.format(dut_friendly_name))
        assert status, "Failed to find dut name locator"
        status = self.driver.is_visible(dut_name)
        if status:
            status = True
            print("DUT is connected")
        else:
            assert status, "DUT is not connected"
        return status

    def close_lightblue_app(self):
        self.driver.close_app()

    def read_fw_information(self, SetFWVerValue):
        status = False
        text = "Firmware Version does not match"
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        status, firmware_version = self.driver.find_element('XPATH', locators.firmware_revision_version)
        assert status, "Failed to find the firmware revision version text"
        time.sleep(5)
        status = self.driver.click_element(firmware_version)
        assert status, "Failed to click on firmware revision field"
        self.driver.perform_bottom_to_up_swipe()
        time.sleep(3)
        status, data_format = self.driver.find_element('XPATH', locators.data_format_field)
        assert status, "Failed to find the data format"
        print("select the data format as UTF-8 String")
        status, data_format_selection = self.driver.find_element('XPATH', locators.data_format_dropdown)
        assert status, "Failed to find data format dropdown opton"
        status = self.driver.click_element(data_format_selection)
        assert status, "Failed to click on data format dropdown"
        time.sleep(5)
        status, UTF8_string = self.driver.find_element('XPATH', locators.select_UTF8_string)
        assert status, "Failed to find UTF-8 string option"
        time.sleep(5)
        status = self.driver.click_element(UTF8_string)
        assert status, "Failed to select UTF-8 string format"
        status, firmware_read_button = self.driver.find_element('XPATH', locators.lightblue_read_button)
        assert status, "Failed to find read button"
        status = self.driver.click_element(firmware_read_button)
        assert status, "Failed to click on read button"
        status, read_firmware_revision = self.driver.find_element('XPATH', locators.device_info_revision_string)
        assert status, "Failed to find firmware revison string"
        read_value = read_firmware_revision.text
        print(read_value)
        # FWVerValue = self.driver.get_text(read_value)
        # print(FWVerValue)
        if FWVerValue == SetFWVerValue:
            status = True
            print("Comparison Successful")
            FWVerValue_text = "Firmware Version is: {}".format(FWVerValue)
        else:
            status = False
            print("Comparison Failed")
            return status, text
        return status, FWVerValue_text

    def read_hw_information(self, SetHwVerValue):
        status = False
        text = "Hardware Version does not match"
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        status, hardware_version = self.driver.find_element('XPATH', locators.hardware_revision_version)
        assert status, "Failed to find the hardware revision version text"
        status = self.driver.click_element(hardware_version)
        assert status, "Failed to click on Hardware revision field"
        self.driver.perform_bottom_to_up_swipe()
        status, data_format = self.driver.find_element('XPATH', locators.data_format_field)
        assert status, "Failed to find the data format"
        print("select the data format as UTF-8 String")
        status, data_format_selection = self.driver.find_element('XPATH', locators.data_format_dropdown)
        assert status, "Failed to find data format dropdown opton"
        status = self.driver.click_element(data_format_selection)
        assert status, "Failed to click on data format dropdown"
        time.sleep(5)
        status, UTF8_string = self.driver.find_element('XPATH', locators.select_UTF8_string)
        assert status, "Failed to find UTF-8 string option"
        time.sleep(5)
        status = self.driver.click_element(UTF8_string)
        assert status, "Failed to select UTF-8 string format"
        status, read_button = self.driver.find_element('XPATH', locators.lightblue_read_button)
        assert status, "Failed to find read button"
        status = self.driver.click_element(read_button)
        assert status, "Failed to click on read button"
        status, read_hardware_revision = self.driver.find_element('XPATH', locators.device_info_revision_string)
        assert status, "Failed to find hardware revison string"
        read_value = read_hardware_revision.find_element_by_xpath(locators.text_view)
        HWVerValue = self.driver.get_text(read_value)
        print(HWVerValue)
        if HWVerValue == SetHwVerValue:
            status = True
            print("Comparison Successful")
            HWVerValue_text = "Hardware Version is: {}".format(HWVerValue)
        else:
            status = False
            print("Comparison Failed")
            return status, text
        return status, HWVerValue_text

    def read_model_string(self, setmodelstring):
        status = False
        text = "Model Number string does not match"
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        status, model_string = self.driver.find_element('XPATH', locators.model_string)
        assert status, "Failed to find the model string text"
        status = self.driver.click_element(model_string)
        assert status, "Failed to click on model string field"
        self.driver.perform_bottom_to_up_swipe()
        status, data_format = self.driver.find_element('XPATH', locators.data_format_field)
        assert status, "Failed to find the data format"
        print("select the data format as UTF-8 String")
        status, data_format_selection = self.driver.find_element('XPATH', locators.data_format_dropdown)
        assert status, "Failed to find data format dropdown opton"
        status = self.driver.click_element(data_format_selection)
        assert status, "Failed to click on data format dropdown"
        time.sleep(5)
        status, UTF8_string = self.driver.find_element('XPATH', locators.select_UTF8_string)
        assert status, "Failed to find UTF-8 string option"
        time.sleep(5)
        status = self.driver.click_element(UTF8_string)
        assert status, "Failed to select UTF-8 string format"
        status, read_button = self.driver.find_element('XPATH', locators.lightblue_read_button)
        assert status, "Failed to find read button"
        status = self.driver.click_element(read_button)
        assert status, "Failed to click on read button"
        status, read_model_string = self.driver.find_element('XPATH', locators.device_info_revision_string)
        assert status, "Failed to find model string"
        read_value = read_model_string.find_element_by_xpath(locators.text_view)
        model_number_string = self.driver.get_text(read_value)
        print(model_number_string)
        if model_number_string == setmodelstring:
            status = True
            print("Comparison Successful")
            Modelstring_text = "Model Number String is: {}".format(model_number_string)
        else:
            status = False
            print("Comparison Failed")
            return status, text
        return status, Modelstring_text

    def read_manufacturer_name(self, setmanufacturername):
        status = False
        text = "Manufacturer Name does not match"
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        status, manufacturer_name = self.driver.find_element('XPATH', locators.manufacturer_name)
        assert status, "Failed to find the model string text"
        status = self.driver.click_element(manufacturer_name)
        assert status, "Failed to click on model string field"
        self.driver.perform_bottom_to_up_swipe()
        status, data_format = self.driver.find_element('XPATH', locators.data_format_field)
        assert status, "Failed to find the data format"
        print("select the data format as UTF-8 String")
        status, data_format_selection = self.driver.find_element('XPATH', locators.data_format_dropdown)
        assert status, "Failed to find data format dropdown opton"
        status = self.driver.click_element(data_format_selection)
        assert status, "Failed to click on data format dropdown"
        time.sleep(5)
        status, UTF8_string = self.driver.find_element('XPATH', locators.select_UTF8_string)
        assert status, "Failed to find UTF-8 string option"
        time.sleep(5)
        status = self.driver.click_element(UTF8_string)
        assert status, "Failed to select UTF-8 string format"
        status, read_button = self.driver.find_element('XPATH', locators.lightblue_read_button)
        assert status, "Failed to find read button"
        status = self.driver.click_element(read_button)
        assert status, "Failed to click on read button"
        status, read_manufacturer_name = self.driver.find_element('XPATH', locators.device_info_revision_string)
        assert status, "Failed to find manufacturer name"
        read_value = read_manufacturer_name.find_element_by_xpath(locators.text_view)
        manufacturer_name_string = self.driver.get_text(read_value)
        print(manufacturer_name_string)
        if manufacturer_name_string == setmanufacturername:
            status = True
            print("Comparison Successful")
            Manufacture_name_text = "Manufacturer Name is: {}".format(manufacturer_name_string)
        else:
            status = False
            print("Comparison Failed")
            return status, text
        return status, Manufacture_name_text

    def read_software_revision_version(self, setsoftwareversion):
        status = False
        text = "Software revision Version does not match"
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()
        status, software_version = self.driver.find_element('XPATH', locators.software_revision_version)
        assert status, "Failed to find the software revision version text"
        time.sleep(5)
        status = self.driver.click_element(software_version)
        assert status, "Failed to click on software revision field"
        self.driver.perform_bottom_to_up_swipe()
        status, data_format = self.driver.find_element('XPATH', locators.data_format_field)
        assert status, "Failed to find the data format"
        print("select the data format as UTF-8 String")
        status, data_format_selection = self.driver.find_element('XPATH', locators.data_format_dropdown)
        assert status, "Failed to find data format dropdown opton"
        status = self.driver.click_element(data_format_selection)
        assert status, "Failed to click on data format dropdown"
        time.sleep(5)
        status, UTF8_string = self.driver.find_element('XPATH', locators.select_UTF8_string)
        assert status, "Failed to find UTF-8 string option"
        time.sleep(5)
        status = self.driver.click_element(UTF8_string)
        assert status, "Failed to select UTF-8 string format"
        status, read_button = self.driver.find_element('XPATH', locators.lightblue_read_button)
        assert status, "Failed to find read button"
        status = self.driver.click_element(read_button)
        assert status, "Failed to click on read button"
        status, read_software_revision = self.driver.find_element('XPATH', locators.device_info_revision_string)
        assert status, "Failed to find software revision string"
        read_value = read_software_revision.find_element_by_xpath(locators.text_view)
        software_revison_version = self.driver.get_text(read_value)
        print(software_revison_version)
        if software_revison_version == setsoftwareversion:
            status = True
            print("Comparison Successful")
            software_revision_text = "Software Revision is: {}".format(software_revison_version)
        else:
            status = False
            print("Comparison Failed")
            return status, text
        return status, software_revision_text

    def read_serial_number(self, setserialnumber):
        status = False
        text = "Serial Number does not match"
        if sd.platform == "SamsungS22":
            self.driver.perform_bottom_to_up_swipe()
            self.driver.perform_bottom_to_up_swipe()
            self.driver.perform_bottom_to_up_swipe()
            self.driver.perform_bottom_to_up_swipe()
            # self.driver.perform_bottom_to_up_swipe()
        else:            
            self.driver.perform_bottom_to_up_swipe()
            self.driver.perform_bottom_to_up_swipe()
            self.driver.perform_bottom_to_up_swipe()
            self.driver.perform_bottom_to_up_swipe()
            self.driver.perform_bottom_to_up_swipe()
        status, serial_number = self.driver.find_element('XPATH', locators.serial_number)
        assert status, "Failed to find the serial number text"
        status = self.driver.click_element(serial_number)
        assert status, "Failed to click on serial number field"
        self.driver.perform_bottom_to_up_swipe()
        status, data_format = self.driver.find_element('XPATH', locators.data_format_field)
        assert status, "Failed to find the data format"
        print("select the data format as UTF-8 String")
        status, data_format_selection = self.driver.find_element('XPATH', locators.data_format_dropdown)
        assert status, "Failed to find data format dropdown opton"
        status = self.driver.click_element(data_format_selection)
        assert status, "Failed to click on data format dropdown"
        time.sleep(5)
        status, UTF8_string = self.driver.find_element('XPATH', locators.select_UTF8_string)
        assert status, "Failed to find UTF-8 string option"
        time.sleep(5)
        status = self.driver.click_element(UTF8_string)
        assert status, "Failed to select UTF-8 string format"
        status, read_button = self.driver.find_element('XPATH', locators.lightblue_read_button)
        assert status, "Failed to find read button"
        status = self.driver.click_element(read_button)
        assert status, "Failed to click on read button"
        status, read_serial_number = self.driver.find_element('XPATH', locators.device_info_revision_string)
        assert status, "Failed to find serial number string"
        read_value = read_serial_number.find_element_by_xpath(locators.text_view)
        serial_number_string = self.driver.get_text(read_value)
        print(serial_number_string)
        if serial_number_string == setserialnumber:
            status = True
            print("Comparison Successful")
            serial_number_text = "Serial Number is: {}".format(serial_number_string)
        else:
            status = False
            print("Comparison Failed")
            return status, text
        return status, serial_number_text

    def read_appearance(self, setappearance):
        status = False
        text = "Appearance value does not match"
        self.driver.perform_bottom_to_up_swipe()
        status, appearance = self.driver.find_element('XPATH', locators.appearance)
        assert status, "Failed the appearance text"
        status = self.driver.click_element(appearance)
        assert status, "Failed to click on serial number field"
        if sd.platform == "SamsungS22":
            print("No need to swipeup")
        else:
            self.driver.perform_bottom_to_up_swipe()        
        status, read_button = self.driver.find_element('XPATH', locators.lightblue_read_button)
        assert status, "Failed to find read button"
        status = self.driver.click_element(read_button)
        assert status, "Failed to click on read button"
        status, read_serial_number = self.driver.find_element('XPATH', locators.device_info_revision_string)
        assert status, "Failed to find appearance"
        read_value = read_serial_number.find_element_by_xpath(locators.text_view)
        appearance_string = self.driver.get_text(read_value)
        print(appearance_string)
        if appearance_string == setappearance:
            status = True
            print("Comparison Successful")
            appearance_text = "Appearance Value is: {}".format(appearance_string)
        else:
            status = False
            print("Comparison Failed")
            return status, text
        return status, appearance_text

    # Pairing feature support
    def google_pixel_pair_device(self):
        print("scroll notification bar")
        time.sleep(2)
        status = self.driver.scroll_notification_bar()
        time.sleep(5)
        bt_status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
        if bt_status:
            status = self.driver.is_visible(bt_text)
            print("Pairing pop up Displayed")
        status, pair_and_connect = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
        print(status)
        assert status, "Failed to find pair and connect field"
        print("click on pair and connect")
        status = self.driver.click_element(pair_and_connect)
        assert status, "Failed to click on pair and connect"
        status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
        assert status, "Pair icon not found"
        status = self.driver.click_element(pair_device)
        assert status, "Unable to click on the Pair icon"
        print("scroll notification bar")
        time.sleep(2)
        status = self.driver.scroll_notification_bar()
        time.sleep(5)
        bt_status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
        if bt_status:
            status = self.driver.is_visible(bt_text)
            print("Pairing pop up Displayed")
        status, pair_and_connect = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
        print(status)
        assert status, "Failed to find pair and connect field"
        print("click on pair and connect")
        status = self.driver.click_element(pair_and_connect)
        assert status, "Failed to click on pair and connect"
        status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
        assert status, "Pair icon not found"
        status = self.driver.click_element(pair_device)
        assert status, "Unable to click on the Pair icon"

    def CloseSerialPort(self, ser):
        print("CloseSerialPort")
        global flagReadSerialData
        flagReadSerialData = False
        ser.close()

    def verify_rnbd_displayyesno_keyboarddisplay_pairing_mode(self):
        status = False
        test_status = False
        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        if sd.platform == "OppoR15":
            bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
            if bt_status:
                status = self.driver.is_visible(bt_text)
                print("First Pairing pop up Displayed")
                self.bleuartpairingfeature.pair_device()
                time.sleep(2)
                passkey = serialPort.read_all()
                passkey = passkey.decode("utf-8").split(":")[1].strip("%")
                print("Read Passkey from serial :", passkey)
                bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
                assert status, "Failed to find the pairing request pop up"
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                    status, passkey_field = self.driver.find_element('XPATH',
                                                                     locators.oppo_R15_display_yes_no_passkey)
                    assert status, "Failed to find the passkey text field"
                    capture_passkey = self.driver.get_text(passkey_field)
                    print("Text", capture_passkey)
                    if passkey in capture_passkey:
                        test_status = True
                        self.bleuartpairingfeature.pair_device()
                        self.CloseSerialPort(serialPort)
                    else:
                        print("Passkey does not match")
                        assert test_status, "Passkey does not match"
        elif sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
            if bt_status:
                status = self.driver.is_visible(bt_text)
                print("First Pairing pop up Displayed")
                self.bleuartpairingfeature.pair_device()
                time.sleep(2)
                passkey = serialPort.read_all()
                passkey = passkey.decode("utf-8").split(":")[1].strip("%")
                print("Read Passkey from serial :",passkey)
                bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
                assert status, "Failed to find the pairing request pop up"
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                    status, passkey_field = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_display_yes_no_passkey)
                    assert status, "Failed to find the passkey text field"
                    capture_passkey = self.driver.get_text(passkey_field)
                    print("Text", capture_passkey)
                    if passkey in capture_passkey:
                        test_status = True
                        self.bleuartpairingfeature.pair_device()
                        self.CloseSerialPort(serialPort)
                    else:
                        print("Passkey does not match")
                        assert test_status, "Passkey does not match"
        elif sd.platform == "GooglePixel3A":
            status = self.driver.scroll_notification_bar()
            bt_status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
            status = self.driver.click_element(bt_text)
            assert status, "Failed to click on pair and connect"
            status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
            assert status, "Pair icon not found"
            status = self.driver.click_element(pair_device)
            assert status, "Unable to click on the Pair icon"
            time.sleep(2)
            passkey = serialPort.read_all()
            passkey = passkey.decode("utf-8").split(":")[1].strip("%")
            print("Read Passkey from serial :", passkey)
            time.sleep(5)
            status = self.driver.scroll_notification_bar()
            print(status)
            time.sleep(2)
            bt_status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
            assert bt_status, "Failed to find the pairing request pop up"
            status = self.driver.click_element(bt_text)
            assert status, "Failed to click on pair and connect"
            status, passkey_field = self.driver.find_element('XPATH',
                                                                     locators.pixel3a_display_yes_no_passkey)
            assert status, "Failed to find the passkey text field"
            capture_passkey = self.driver.get_text(passkey_field)
            print("Text", capture_passkey)
            if passkey in capture_passkey:
                test_status = True
                status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
                assert status, "Pair icon not found"
                status = self.driver.click_element(pair_device)
                assert status, "Unable to click on the Pair icon"
                self.CloseSerialPort(serialPort)
            else:
                print("Passkey does not match")
                assert test_status, "Passkey does not match"

    def verify_rnbd_display_only_pairing_mode(self):
        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        if sd.platform == "OppoR15":
            bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
            status = self.driver.is_visible(bt_text)
            print("First Pairing pop up Displayed")
            self.bleuartpairingfeature.pair_device()
            time.sleep(2)
            passkey = serialPort.read_all()
            passkey = passkey.decode("utf-8").split(":")[1].strip("%")
            print("Read Passkey from serial :",passkey)
            status, passkey_entry_field = self.driver.find_element('XPATH', locators.oppo_R15_passkey_entry)
            assert status, "Failed to find the passkey entry field"
            status = self.driver.click_element(passkey_entry_field)
            assert status, "Failed to click on the passkey entry field"
            print("Enter the correct key in the passkey field")
            self.driver.send_keys(passkey_entry_field, passkey)
            print("Attempting to pair and connect to the device")
            self.bleuartpairingfeature.pair_device()
            time.sleep(5)
            self.CloseSerialPort(serialPort)
        elif sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
            status = self.driver.is_visible(bt_text)
            print("First Pairing pop up Displayed")
            self.bleuartpairingfeature.pair_device()
            time.sleep(2)
            passkey = serialPort.read_all()
            passkey = passkey.decode("utf-8").split(":")[1].strip("%")
            print("Read Passkey from serial :", passkey)
            status, passkey_entry_field = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_passkey_entry)
            assert status, "Failed to find the passkey entry field"
            status = self.driver.click_element(passkey_entry_field)
            assert status, "Failed to click on the passkey entry field"
            print("Enter the correct key in the passkey field")
            self.driver.send_keys(passkey_entry_field, passkey)
            print("Attempting to pair and connect to the device")
            self.bleuartpairingfeature.pair_device()
            time.sleep(5)
            self.CloseSerialPort(serialPort)
        elif sd.platform == "GooglePixel3A":
            status = self.driver.scroll_notification_bar()
            bt_status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
            print("click on pair and connect")
            time.sleep(2)
            status = self.driver.click_element(bt_text)
            assert status, "Failed to click on pair and connect"
            status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
            assert status, "Pair icon not found"
            status = self.driver.click_element(pair_device)
            assert status, "Unable to click on the Pair icon"
            status = self.driver.scroll_notification_bar()
            status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
            assert status, "Failed to find pair and connect field"
            status = self.driver.click_element(bt_text)
            assert status, "Failed to click on pair and connect"
            time.sleep(2)
            passkey = serialPort.read_all()
            passkey = passkey.decode("utf-8").split(":")[1].strip("%")
            print("Read Passkey from serial :", passkey)
            status, passkey_entry_field = self.driver.find_element('XPATH', locators.pixel3a_passkey_entry)
            assert status, "Failed to find the passkey entry field"
            status = self.driver.click_element(passkey_entry_field)
            assert status, "Failed to click on the passkey entry field"
            print("Enter the correct key in the passkey field")
            self.driver.send_keys(passkey_entry_field, passkey)
            print("Attempting to pair and connect to the device")
            status, pair_device = self.driver.find_element('XPATH', locators.pixel3a_ok_button)
            assert status, "Pair icon not found"
            status = self.driver.click_element(pair_device)
            assert status, "Failed to click on Pair"
            time.sleep(5)
            self.CloseSerialPort(serialPort)

    def verify_rnbd_keyboard_only_pairing_mode(self):
        status = False
        test_status = False
        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        if sd.platform == "OppoR15":
            bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
            if bt_status:
                status = self.driver.is_visible(bt_text)
                print("First Pairing pop up Displayed")
                self.bleuartpairingfeature.pair_device()
            bt_status, bt_text = self.driver.find_element('XPATH', locators.oppo_R15_displayonly_pairing_req_text)
            if bt_status:
                status = self.driver.is_visible(bt_text)
                print("Pairing pop up Displayed")
            status, passkey_field = self.driver.find_element('XPATH', locators.oppo_R15_keyboard_only_passkey)
            assert status, "Failed to find the passkey text field"
            capture_passkey = self.driver.get_text(passkey_field)
            print("Text", capture_passkey)
            if "please enter: " in capture_passkey:
                pos = capture_passkey.find("please enter:")
                app_display_pin_code = capture_passkey[(pos + 15):(pos + 21)]
                print("Send passkey : ",app_display_pin_code)
                pin_code = str(app_display_pin_code+'\r').encode()
                serialPort.write(pin_code)
                serial_read = serialPort.readlines()
                print(serial_read)
                time.sleep(5)
                self.CloseSerialPort(serialPort)
        elif sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
            if bt_status:
                status = self.driver.is_visible(bt_text)
                print("First Pairing pop up Displayed")
                self.bleuartpairingfeature.pair_device()
            bt_status, bt_text = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_displayonly_pairing_req_text)
            if bt_status:
                status = self.driver.is_visible(bt_text)
                print("Pairing pop up Displayed")
            status, passkey_field = self.driver.find_element('XPATH', locators.samsung_S10_S21_S22_keyboard_only_passkey)
            assert status, "Failed to find the passkey text field"
            capture_passkey = self.driver.get_text(passkey_field)
            print("Text", capture_passkey)
            if "Enter " in capture_passkey:
                pos = capture_passkey.find("Enter")
                app_display_pin_code = capture_passkey[(pos + 6):(pos + 12)]
                print("Send passkey : ", app_display_pin_code)
                pin_code = str(app_display_pin_code + '\r').encode()
                serialPort.write(pin_code)
                serial_read = serialPort.readlines()
                print(serial_read)
                time.sleep(5)
                self.CloseSerialPort(serialPort)
            else:
                print("Passkey is not visible")
                assert test_status, "Passkey is not visible"
        elif sd.platform == "GooglePixel3A":
            status = self.driver.scroll_notification_bar()
            bt_status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
            print("click on pair and connect")
            time.sleep(2)
            status = self.driver.click_element(bt_text)
            assert status, "Failed to click on pair and connect"
            status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
            status = self.driver.click_element(pair_device)
            assert status, "Unable to click on the Pair icon"
            status = self.driver.scroll_notification_bar()
            bt_status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
            status = self.driver.click_element(bt_text)
            assert status, "Failed to click on pair and connect"
            status, passkey_field_text = self.driver.find_element('XPATH',
                                                                     locators.pixel3a_keyboard_only_passkey_text)
            assert status, "Failed to find the passkey text field"
            status, passkey_field = self.driver.find_element('XPATH',
                                                                     locators.pixel3a_keyboard_only_passkey)
            assert status, "Failed to find the passkey field"
            capture_passkey_text = self.driver.get_text(passkey_field_text)
            capture_passkey = self.driver.get_text(passkey_field)
            print("Pairing code :",capture_passkey,"\n",capture_passkey_text)
            if "press Return or Enter" in capture_passkey_text:
                print("Send passkey : ", capture_passkey)
                pin_code = str(capture_passkey + '\r').encode()
                serialPort.write(pin_code)
                serial_read = serialPort.readlines()
                print(serial_read)
                time.sleep(5)
                self.CloseSerialPort(serialPort)
            else:
                print("Passkey does not displayed and Pairing pop up not displayed")
                assert test_status, "Passkey does not displayed"


    def bond_device(self):
        cmd = '$$$'
        cmd = str(cmd).encode()
        bond_cmd = 'B\r'
        bond_cmd = str(bond_cmd).encode()
        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        serialPort.write(cmd)
        serial_read = serialPort.readlines()
        print(serial_read)
        serialPort.write(bond_cmd)
        time.sleep(5)
        serial_read = serialPort.readlines()
        print(serial_read)
        self.CloseSerialPort(serialPort)

    def list_bonded_device(self):
        LB_status = False
        cmd = str('$$$').encode()
        lb_cmd = str('LB\r').encode()
        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        print("List Bonded Divice")
        serialPort.write(cmd)
        time.sleep(5)
        serialPort.write(lb_cmd)
        list_bonded_device = serialPort.readlines()
        if 'END' in str(list_bonded_device) :
            LB_status = True
        else:
            LB_status = False
        assert LB_status, "No record of bonded device"
        time.sleep(5)
        print(str(list_bonded_device))
        self.CloseSerialPort(serialPort)
        return str(list_bonded_device)

    def send_data_uart(self, input_data):
        status = False
        TX_string = "[TX]:"+input_data
        status, send_button = self.driver.find_element('XPATH', locators.send_button)
        assert status, "Failed to find the SEND icon element"
        status = self.driver.click_element(send_button)
        assert status, "Failed to click on SEND icon"
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

    def verify_scan_page(self):
        status, scan_button = self.driver.find_element('XPATH', locators.scan_button)
        status = self.driver.is_visible(scan_button)
        print("Last connected device has been disconnected")
        assert status, "Last connected device has not been disconnected"
        return status
    def send_raw_data_uart_mode_rnbd_to_app(self):
        input_data = "12345678"
        result_status, pass_status = self.driver.find_element('XPATH', locators.raw_data_log_message)
        assert result_status, "Failed to find the raw data log message"
        pass_status_get_text = self.driver.get_text(pass_status)
        if input_data in pass_status_get_text:
            print("Data received in APP:",pass_status_get_text)
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        return status, pass_status_get_text

    def send_raw_data_uart_mode_app_to_rnbd(self,output_data):
        input_data = "12345678"
        time.sleep(2)
        status, raw_text_field = self.driver.find_element('XPATH', locators.raw_text_field)
        assert status, "Failed to find the raw data text field"
        status = self.driver.click_element(raw_text_field)
        assert status, "Failed to find the raw data text field to input"
        self.driver.send_keys(raw_text_field, input_data)
        time.sleep(5)
        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        status = self.send_data_uart(input_data)
        assert status, "Test Fails as the comparison is not successful"
        read_data = self.read_serial_port(serialPort, input_data)
        if output_data in read_data:
            status = True
            print("Comparison Successful")
        else:
            status = False
            print("Comparison Failed")
        self.CloseSerialPort(serialPort)
        return status,read_data

    def send_rnbd_to_app(self,raw_data):
        cmd = str(raw_data).encode()
        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        print("Send raw data from RNBD to Mobile")
        serialPort.write(cmd)
        serial_read = serialPort.readlines()
        if serial_read == "[]":
            status = True
        else:
            status = False
            print(serial_read)
        time.sleep(5)
        self.CloseSerialPort(serialPort)













