
import os
import time
import json

import threading

from . import android_locators as locators
from ..CommonSupportLib.StationData import stationData
from ..StationConfig import conf_file
from ..CommonSupportLib.Serial_Implementaiton import SerialSuppport
from ..CommonSupportLib.BleUARTPairingFeatureSupport import BLEUartPairingSupport

from datetime import datetime

sd = stationData()

baudrate = conf_file.baud_rate
comport = conf_file.com_port

flagReadSerialData = True
passkey = ""

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
        json_file = os.getcwd() + "\BLEAF\Tests\RNBD45x_JSON_File\RNBD45x_vs_Phone_Command_Set.json"
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
        self.driver.press_keycode(66)
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
        read_value = read_firmware_revision.find_element_by_xpath(locators.text_view)
        FWVerValue = self.driver.get_text(read_value)
        print(FWVerValue)
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


    def read_again(self,value):
        status = False
        text = "Appearance value does not match"
        self.driver.perform_bottom_to_up_swipe()
        time.sleep(2)
        status, appearance = self.driver.find_element('XPATH', locators.appearance)
        assert status, "Failed the appearance text"
        status = self.driver.click_element(appearance)
        assert status, "Failed to click on serial number field"
        time.sleep(2)
        status, read_again = self.driver.find_element('XPATH', locators.lightblue_read_again_button)
        assert status, "Failed find the read again button"
        status = self.driver.click_element(read_again)
        assert status, "Failed to click on read again button"
        status, read_again_value = self.driver.find_element('XPATH',locators.read_again_value.format(value))
        read_val = self.driver.get_text(read_again_value)
        return read_val

    # Pairing feature support
    def google_pixel_pair_device(self):
        if "Vivo" not in sd.platform:
            print("scroll notification bar")
            status = self.driver.scroll_notification_bar()
            time.sleep(1)
            bt_status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
            if bt_status:
                status = self.driver.is_visible(bt_text)
                print("Pairing pop up Displayed")
            status, pair_and_connect = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
            print(status)
            assert status, "Failed to find pair and connect field"
            time.sleep(2)
            print("click on pair and connect")
            status = self.driver.click_element(pair_and_connect)
            assert status, "Failed to click on pair and connect"
        time.sleep(1)
        status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
        assert status, "Pair icon not found"
        time.sleep(1)
        status = self.driver.click_element(pair_device)
        #assert status, "Unable to click on the Pair icon"

        #if self.driver.get_capability("deviceModel") == "Pixel 3a":
        if status:
            status, pair_device = self.driver.find_element('XPATH', locators.device_pair,timeout=5)
            if status:
                status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
                assert status, "Pair icon not found"
                status = self.driver.click_element(pair_device)
                assert status, "Unable to click on the Pair icon"
            else:
                print("scroll notification bar")
                time.sleep(1)
                status = self.driver.scroll_notification_bar()
                time.sleep(1)
                bt_status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text,timeout=5)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                    status, pair_and_connect = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
                    if status:
                        print("click on pair and connect")
                        status = self.driver.click_element(pair_and_connect)
                        status, pair_device = self.driver.find_element('XPATH', locators.device_pair)
                        assert status, "Pair icon not found"
                        status = self.driver.click_element(pair_device)
                        assert status, "Unable to click on the Pair icon"
                else:
                    print("No Second pop up")
                    self.driver.go_back()




    def google_pixel_pair_cancel(self):
        status, pair_device = self.driver.find_element('XPATH', locators.device_cancel_pair,timeout=10)
        if not status:
            if "Vivo" not in sd.platform:
                print("scroll notification bar")
                status = self.driver.scroll_notification_bar()
                time.sleep(1)
                bt_status, bt_text = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
                if bt_status:
                    status = self.driver.is_visible(bt_text)
                    print("Pairing pop up Displayed")
                status, pair_and_connect = self.driver.find_element('XPATH', locators.pixel3a_displayonly_pairing_req_text)
                assert status, "Failed to find pair and connect field"
                time.sleep(2)
                print("click on pairing pop up")
                status = self.driver.click_element(pair_and_connect)
                assert status, "Failed to click on Pair and connect"
        time.sleep(1)
        status, cancel_pair = self.driver.find_element('XPATH', locators.device_cancel_pair)
        assert status, "Cancel icon not found"
        time.sleep(1)
        status = self.driver.click_element(cancel_pair)
        assert status, "Failed to click on Cancel"

    def google_pixel_pairing_ok(self):
        status, ok_pair = self.driver.find_element('XPATH', locators.pixel3a_ok_button)
        assert status, "Failed to find OK button"
        time.sleep(1)
        print("click on OK")
        status = self.driver.click_element(ok_pair)
        assert status, "Failed to click on OK button"

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
        # cmd = '$$$'
        # cmd = str(cmd).encode()
        bond_cmd = 'B\r'
        bond_cmd = str(bond_cmd).encode()
        v_cmd = 'V\r'
        v_cmd = str(v_cmd).encode()

        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        serialPort.write(bond_cmd)
        serial_read = serialPort.readlines()
        print(serial_read)

        serialPort.write(v_cmd)
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
        time.sleep(2)
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
        if len(serial_read) == 0:
            status = True
        else:
            status = False
            print(serial_read)
        time.sleep(5)
        self.CloseSerialPort(serialPort)

    def Read_json_file_1(self,command_set,comport):
        step_result = []
        step_descript = []
        json_file = os.getcwd() + "\BLEAF\Tests\RNBD45x_JSON_File\RNBD45x_vs_Phone_Command_Set.json"
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


    def send_data_rnbd_to_rnbd(self,data_to_send):
        cmd = '$$$'
        cmd = str(cmd).encode()
        cmd_to_send = str(data_to_send).encode()
        v_cmd = 'V\r'
        v_cmd = str(v_cmd).encode()

        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        serialPort.write(cmd)
        serial_read = serialPort.readlines()
        print(serial_read)

        serialPort.write(v_cmd)
        serial_read = serialPort.readlines()
        print(serial_read)

        serialPort.write(cmd_to_send)
        time.sleep(5)
        serial_read = serialPort.readlines()
        print(serial_read)
        self.CloseSerialPort(serialPort)
        return serial_read


    def send_data_rnbd_to_rnbd_multirole(self,data_to_send,comport):
        cmd = '$$$'
        cmd = str(cmd).encode()
        cmd_to_send = str(data_to_send).encode()
        v_cmd = 'V\r'
        v_cmd = str(v_cmd).encode()

        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        serialPort.write(cmd)
        serial_read = serialPort.readlines()
        print(serial_read)

        serialPort.write(v_cmd)
        serial_read = serialPort.readlines()
        print(serial_read)

        serialPort.write(cmd_to_send)
        time.sleep(5)
        serial_read = serialPort.readlines()
        print(serial_read)
        self.CloseSerialPort(serialPort)
        return serial_read

    def lightblue_filter_peripherals(self, name):
        print('lightblue_filter_peripherals')
        status, text_field = self.driver.find_element('XPATH', '//android.widget.EditText')
        assert status, "Failed to find the textfield"
        self.driver.send_keys(text_field, name)

    def open_ble_smart_scanner(self):
        status, ble_uart_icon = self.driver.find_element('XPATH', locators.bluetooth_smart_icon)
        assert status, "BLE Smart Icon not found"
        status = self.driver.click_element(ble_uart_icon)
        assert status, "Failed to open BLE Smart page"

    def ble_smart_filter_peripherals(self, name, search_icon=False):
        print('ble_smart_filter_peripherals')
        if search_icon:
            status, search_icon = self.driver.find_element('XPATH', locators.search_icon)
            assert status, "Failed to find the search icon"
            time.sleep(2)
            search_icon.click()
            time.sleep(2)
        status, search_field = self.driver.find_element('XPATH', locators.search_field)
        assert status, "Failed to find the search field"
        self.driver.send_keys(search_field, name)

    def ble_smart_connect(self, dut_name):
        print('ble_smart_connect')
        status, scan_button = self.driver.find_element('XPATH', '//android.widget.Button[@resource-id="com.microchip.bluetooth.data:id/menu_scan"]')
        assert status, "Failed to find the scan button"
        button_text = scan_button.get_attribute('text')
        print('button_text = {}'.format(button_text))
        if button_text == 'STOP SCAN':
            scan_button.click()
            print("Stop scan")
        time.sleep(1)
        peripheral = None
        locator = '//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/device_name" and @text="{}"]'
        status, peripheral = self.driver.find_element('XPATH', locator.format(dut_name))
        if not status:
            print("Failed to find the peripheral.Fail retry.")
            if dut_name == 'Direct A':
                new_dut_name = 'Direct Adv'
            else:
                new_dut_name = 'Direct A'
            time.sleep(2)
            status, peripheral = self.driver.find_element('XPATH', locator.format(new_dut_name))
        print("Find the peripheral")
        time.sleep(1)
        status = self.driver.click_element(peripheral)
        assert status, "Unable to click the dut"

    def lightblue_connect(self, dut_name):
        locator = "//android.widget.TextView[@text='{}']"
        print('lightblue_connect: {}'.format(dut_name))
        #ioslocators.dut_name.format(dut_friendly_name)
        #status, peripheral = self.driver.find_element('XPATH', '//XCUIElementTypeStaticText[@label="BLE_UART_CDDF_H"]')
        status, peripheral = self.driver.find_element('XPATH', locator.format(dut_name))
        #assert status, "Failed to find the peripheral"
        if not status:
            print("Failed to find the peripheral.Fail retry.")
            if dut_name == 'Direct A':
                new_dut_name = 'Direct Adv'
            else:
                new_dut_name = 'Direct A'
            status, peripheral = self.driver.find_element('XPATH', locator.format(new_dut_name))
            assert status, "Failed to find the peripheral"
        status, connect_button = self.driver.find_element('XPATH', "//android.widget.TextView[@text='Connect']")
        assert status, "Failed to find the connect button"
        status = self.driver.click_element(connect_button)
        assert status, "Unable to click connect button"

    def lightblue_verify_ble_connected(self):
        print('lightblue_verify_ble_connected')
        status, element = self.driver.find_element('XPATH', "//android.widget.TextView[@text='Connected']")
        assert status, "Failed to find the element. Connected"
        self.driver.perform_bottom_to_up_swipe()
        self.driver.perform_bottom_to_up_swipe()

    def ble_smart_connection_long_term_test(self, test_time):
        print('ble_smart_connection_long_term_test')
        status, state = self.driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/connection_state"]')
        assert status, "Failed to find the connection state"
        for i in range(test_time):
            print(f'index: {i}')
            ble_state = self.driver.get_text(state)
            print('ble state = {}'.format(ble_state))

    def ble_smart_connect_and_get_info(self, dut_name, test_phone):
        print(f'ble_smart_connect_and_get_info. test phone:{test_phone}')
        ble_state = 'Disconnected'
        bt_addr = ''
        status, dut = self.driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/device_name"]')
        assert status, "Failed to find the dut"
        time.sleep(1)
        assert self.driver.get_text(dut) == dut_name, 'Fail to find the dut'

        status, state = self.driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/connection_state"]')
        assert status, "Failed to find the connection state"

        status, connect_button = self.driver.find_element('XPATH', '//android.widget.Button[@resource-id="com.microchip.bluetooth.data:id/menu_connect"]')
        assert status, "Failed to find the connection state"

        status, bt_address = self.driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/device_address"]')
        assert status, "Failed to find the bt_address"

        connect_fail_retry = 0
        while ble_state == 'Disconnected' and connect_fail_retry < 3:
            connect_button.click()
            print('click connect button')
            time.sleep(5)
            ble_state = self.driver.get_text(state)
            print('ble state = {}'.format(ble_state))
            if ble_state == 'Disconnected':
                connect_fail_retry += 1
                print(f'Connect fail. retry = {connect_fail_retry}')
                time.sleep(3)
            else:
                start_time = time.time()
                while ble_state == 'Connected' and time.time() < start_time + 30:
                    #print('Connected. get state')
                    time.sleep(5)
                    ble_state = self.driver.get_text(state)
                    print(f"Get state: {ble_state}")
                if ble_state == 'Connected':
                    print('Connected for 30 sec')

        bt_addr = self.driver.get_text(bt_address)
        return ble_state, bt_addr

    def ble_smart_verify_ble_connected(self, dut_name):
        print('ble_smart_verify_ble_connected')
        global flagReadSerialData
        serial_recv = ''
        flagReadSerialData = True

        def ble_connect():
            status1, connect_button = self.driver.find_element('XPATH','//android.widget.Button[@resource-id="com.microchip.bluetooth.data:id/menu_connect"]')
            assert status1, "Failed to find the connect button"
            time.sleep(1)
            connect_button.click()
            print('Click connect button')
            #time.sleep(10)
            #status2, conn_state = self.driver.find_element('XPATH','//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/connection_state"]')
            #assert status2, "Failed to find the connection state"
            #state = conn_state.get_attribute('text')
            #print('ble_state = {}'.format(state))

        status, dut = self.driver.find_element('XPATH',
                                               '//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/device_name"]')
        assert status, "Failed to find the dut name"
        name = dut.get_attribute('text')
        print('dut name = {}'.format(name))
        assert name == dut_name, "Failed to find the dut name"
        time.sleep(2)

        serial_port = self.serialdriver.ComportSet(comport, baudrate)
        t0 = threading.Thread(target=self.read_serial_data, args=(serial_port, serial_recv))
        t0.start()
        t1 = threading.Thread(target=ble_connect, args=())
        t1.start()
        t1.join()
        print('work thread complete')
        t0.join(80)
        print("serial thread complete.serial_recv = {}".format(serial_recv))

        status, state = self.driver.find_element('XPATH','//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/connection_state"]')
        assert status, "Failed to find the connection state"
        ble_state = state.get_attribute('text')
        print('ble_state = {}'.format(ble_state))
        #assert ble_state == 'Connected', "Failed to connect"
        if ble_state == 'Disconnected':
            for i in range(5):
                print("Connect fail. retry: {}".format(i))
                time.sleep(5)
                ble_connect()
                time.sleep(10)
                #t0 = threading.Thread(target=self.read_serial_data, args=(serial_port, serial_recv))
                #t0.start()
                #t1 = threading.Thread(target=ble_connect, args=())
                #t1.start()
                #t1.join()
                #print('work thread complete')
                #t0.join(10)
                #if t0.is_alive():
                #    print('serial thread is still alive')
                #print("serial thread complete.serial_recv = {}".format(serial_recv))
                status, state = self.driver.find_element('XPATH','//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/connection_state"]')
                assert status, "Failed to find the connection state"
                ble_state = state.get_attribute('text')
                if ble_state == 'Connected':
                    #read_data = self.read_serial_data(serial_port)
                    self.CloseSerialPort(serial_port)
                    return ble_state
            print('Fail retry. done')
            if t0.is_alive():
                print('serial port: timeout')
            self.CloseSerialPort(serial_port)
            return ble_state
        else:
            #read_data = self.read_serial_data(serial_port)
            self.CloseSerialPort(serial_port)
            return ble_state

    def ble_smart_characteristic_write(self, service_uuid, char_uuid, data, char_found=False):
        print('ble_smart_characteristic_write data: {}'.format(data))
        locator = '//android.widget.TextView[@resource-id="android:id/text2" and @text="{}"]'
        #12345678-1234-5678-1234-56789abcdef0
        #status, service = self.driver.find_element('XPATH','//android.widget.TextView[@resource-id="android:id/text2" and @text="12345678-1234-5678-1234-56789abcdef0"]')
        status, service = self.driver.find_element('XPATH', locator.format(service_uuid))
        assert status, "Failed to find the service"
        time.sleep(1)
        if not char_found:
            service.click()
            print('Tap service uuid')
            time.sleep(3)
        #12345678-1234-5678-1234-56789abcdef2
        status, char = self.driver.find_element('XPATH', locator.format(char_uuid))
        assert status, "Failed to find the characteristic"
        #print('characteristic uuid found')
        char.click()
        print('Tap characteristic uuid')
        time.sleep(3)
        #//android.widget.EditText[@resource-id="com.microchip.bluetooth.data:id/characteristic_write"]
        status, text_field = self.driver.find_element('XPATH', '//android.widget.EditText[@resource-id="com.microchip.bluetooth.data:id/characteristic_write"]')
        assert status, "Failed to find the text field"
        #self.driver.send_keys(text_field, '12345678')
        self.driver.send_keys(text_field, data)
        time.sleep(2)
        status, write_button = self.driver.find_element('XPATH','//android.widget.Button[@resource-id="com.microchip.bluetooth.data:id/characteristic_write_button"]')
        assert status, "Failed to find the text field"
        write_button.click()

    def ble_smart_characteristic_read(self, service_uuid, char_uuid):
        print('ble_smart_characteristic_read')
        locator = '//android.widget.TextView[@resource-id="android:id/text2" and @text="{}"]'
        #12345678-1234-5678-1234-56789abcdef2
        status, char = self.driver.find_element('XPATH', locator.format(char_uuid))
        assert status, "Failed to find the characteristic"
        char.click()
        time.sleep(3)
        #//android.widget.EditText[@resource-id="com.microchip.bluetooth.data:id/characteristic_write"]
        status, char_read = self.driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/characteristic_read"]')
        assert status, "Failed to find the text"
        text = self.driver.get_text(char_read)
        print('read characteristic: {}'.format(text))
        return text

    def ble_smart_pairing_google_phone(self, dut_name, action):
        print('ble_smart_pairing_google_phone,action: {}'.format(action))
        global flagReadSerialData
        serial_recv = ''
        flagReadSerialData = True

        serial_port = self.serialdriver.ComportSet(comport, baudrate)

        def handle_pairing():
            if action == 'timeout':
                print("pairing timeout")
            elif action == 'cancel':
                self.google_pixel_pair_cancel()
            elif action == 'accept':
                self.google_pixel_pair_device()

        t0 = threading.Thread(target=self.read_serial_data, args=(serial_port, serial_recv))
        t0.start()
        t1 = threading.Thread(target=handle_pairing, args=())
        t1.start()
        t1.join()
        print('work thread complete')
        if action == 'timeout' or action == 'accept':
            t0.join(60)
        else:
            t0.join(10)

        print('time = {}'.format(datetime.now().strftime("%d-%m-%Y_%I-%M-%S")))
        #self.CloseSerialPort(serial_port)

        if t0.is_alive():
            print('Read serial data: Unknown data.')
            self.CloseSerialPort(serial_port)
            return False
        else:
            print("serial thread complete.serial_recv = {}".format(serial_recv))
            self.CloseSerialPort(serial_port)
            return True

    def ble_smart_pairing(self, dut_name, action):
        print('ble_smart_pairing,action: {}'.format(action))
        global flagReadSerialData
        serial_recv = ''
        flagReadSerialData = True

        serial_port = self.serialdriver.ComportSet(comport, baudrate)
        def handle_pairing():
            self.driver.handle_pairing_alert(dut_name, action)

        t0 = threading.Thread(target=self.read_serial_data, args=(serial_port, serial_recv))
        t0.start()
        t1 = threading.Thread(target=handle_pairing, args=())
        t1.start()
        t1.join()
        print('work thread complete')
        if action == 'timeout' or action == 'accept':
            t0.join(60)
        else:
            t0.join(10)

        #print('time = {}'.format(datetime.now().strftime("%d-%m-%Y_%I-%M-%S")))
        #self.CloseSerialPort(serial_port)

        if t0.is_alive():
            print('Read serial data: Unknown data.')
            print('time = {}'.format(datetime.now().strftime("%d-%m-%Y_%I-%M-%S")))
            self.CloseSerialPort(serial_port)
            return False
        else:
            print("serial thread complete.serial_recv = {}".format(serial_recv))
            print('time = {}'.format(datetime.now().strftime("%d-%m-%Y_%I-%M-%S")))
            self.CloseSerialPort(serial_port)
            return True

    def ble_smart_go_back(self):
        print('ble_smart_go_back')
        status, back_button = self.driver.find_element('XPATH', '//android.widget.ImageView[@resource-id="android:id/up"]')
        assert status, "Failed to find the back button"
        time.sleep(1)
        back_button.click()
        print('click backbutton')

    def ble_smart_scan_start_stop(self):
        print('ble_smart_scan_start_stop')
        locator = '//android.widget.Button[@resource-id="com.microchip.bluetooth.data:id/menu_scan"]'
        status, button = self.driver.find_element('XPATH', locator)
        assert status, "Failed to find the button"
        time.sleep(1)
        button_text = self.driver.get_text(button)
        print('state = {}'.format(button_text))
        button.click()
        print('click button')

    def ble_smart_disconnect(self):
        print('ble_smart_disconnect')
        locator = '//android.widget.Button[@resource-id="com.microchip.bluetooth.data:id/menu_disconnect"]'
        status, button = self.driver.find_element('XPATH', locator)
        assert status, "Failed to find the button"
        button.click()
        time.sleep(5)
        print('Disconnect. click')
        status, state = self.driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/connection_state"]')
        assert status, "Failed to find the connection state"
        ble_state = state.get_attribute('text')
        #print('ble_state = {}'.format(ble_state))
        return ble_state

    def ble_smart_unbond(self):
        print('ble_smart_unbond')
        locator = '//android.widget.Button[@resource-id="com.microchip.bluetooth.data:id/menu_more"]'
        status, button = self.driver.find_element('XPATH', locator)
        assert status, "Failed to find the button"
        time.sleep(1)
        button.click()
        time.sleep(3)
        status, bond = self.driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title"]')
        assert status, "Failed to find the bond element"
        text = self.driver.get_text(bond)
        print('text = {}'.format(text))
        time.sleep(1)
        ble_state = 'Unknown state'
        if text == 'UnBond':
            bond.click()
            print('click UnBond button')
            time.sleep(5)
            status, state = self.driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/connection_state"]')
            assert status, "Failed to find the connection state"
            ble_state = state.get_attribute('text')

        return ble_state


    def read_serial_data(self, ser, received_data):
        global flagReadSerialData

        reading =''
        print("read_serial_data")
        while flagReadSerialData:
            while ser.inWaiting():
                if ser.inWaiting() > 0:
                    reading += ser.readline(ser.inWaiting()).decode()
                    received_data += reading
                    #print("*{}".format(reading))
                    if 'Connected' in reading:
                        #print('Ble connected')
                        print("Read serial data: {}".format(reading))
                        flagReadSerialData = False
                    elif 'pairing failed' in reading:
                        #print('Pairing failed')
                        #print("Read serial data: {}".format(reading))
                        flagReadSerialData = False
                    elif 'SMP Timeout' in reading:
                        #print('SMP Timeout')
                        #print("Read serial data: {}".format(reading))
                        flagReadSerialData = False
                    elif 'Pairing completed' in reading:
                        print("Read serial data: {}".format(reading))
                        reading = ''
                        #print('Pairing success,Check more information')
                        #flagReadSerialData = False
                    elif 'Direct advertising to' in reading:
                        #print('Direct advertising to XX')
                        if 'Rebooting in 5 seconds' in reading:
                            #print('Rebooting in 5 seconds...')

                            search_substring = 'Direct advertising to'
                            start_index = reading.find(search_substring)
                            if start_index != -1:
                                flagReadSerialData = False
                                end_index = start_index + len(search_substring)
                                result = reading[start_index:end_index]
                                reading = ''
                                print("Read serial data: {}".format('Rebooting in 5 seconds...' + result))

                        #print("Receive serial data: {}".format(reading))
                        #flagReadSerialData = False

        print("read_serial_data.complete. serial data = {}".format(reading))
        return reading

    def get_serial_data_passkey(self, dut_element):
        global flagReadSerialData
        global passkey

        def click_dut():
            dut_element.click()
            print('time = {}'.format(datetime.now().strftime("%d-%m-%Y_%I-%M-%S")))

        fail_retry = 0
        passkey = ""
        serial_port = self.serialdriver.ComportSet(comport, baudrate)

        while passkey == "" and fail_retry < 3:
            flagReadSerialData = True
            t0 = threading.Thread(target=self.read_pairing_passkey, args=(serial_port,))
            t0.start()
            t1 = threading.Thread(target=click_dut, args=())
            t1.start()
            t1.join()
            print('Click dut: Test Hog mouse')
            t0.join(3)
            if t0.is_alive():
                print('Read serial data: 15 seconds timeout')
                flagReadSerialData = False
                fail_retry += 1

            print(f"Read serial thread complete. passkey={passkey}")

        self.CloseSerialPort(serial_port)
        print('Get passkey, time = {}'.format(datetime.now().strftime("%d-%m-%Y_%I-%M-%S")))
        return passkey

    def read_pairing_passkey(self, ser):
        global flagReadSerialData
        global passkey

        reading = ''
        print("start read_serial_data")
        while flagReadSerialData:
            while ser.inWaiting():
                if ser.inWaiting() > 0:
                    reading += ser.readline(ser.inWaiting()).decode()
                    if 'Passkey for' in reading:
                        reading = ''
                        #passkey = 'Passkey for'
                    if len(reading) > 8:
                        passkey_str = reading[-8:-2]
                        if passkey_str.isdigit():
                            print(f'The 6 digit number is {passkey_str}')
                            reading = ''
                            flagReadSerialData = False
                            passkey = passkey_str

        print("read_passkey.complete")
        #passkey_str = reading[-8:-2]
        #passkey += reading
        #return passkey

    def ble_lightblue_Bonded(self, dut_name):
        print('ble_lightblue_Bonded. dut = {}'.format(dut_name))
        dut_locator = "//android.widget.TextView[@text='{}']"
        status, Bonded_icon = self.driver.find_element('XPATH', '//android.widget.TextView[@text="Bonded"]')
        assert status, "Failed to find the Bonded_icon"
        time.sleep(1)
        Bonded_icon.click()
        print('click Bonded')
        time.sleep(3)
        status, Bonded_List = self.driver.find_element('XPATH', '//android.widget.TextView[@text="Bonded Devices"]')
        assert status, "Failed to find the Bonded Devices"
        time.sleep(3)
        status, Bonded_dut = self.driver.find_element('XPATH', dut_locator.format(dut_name))
        assert status, "Failed to find the Bonded device"
        print('{} is bonded'.format(dut_name))















