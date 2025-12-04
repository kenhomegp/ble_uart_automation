import time
import pytest
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException

from . import ios_locators as locators
from .StationData import stationData

sd = stationData()


class iOSBluetoothSupport:

    def __init__(self,driver=sd.mobile_driver):
        if not driver:
            #sd = stationData()
            self.driver = sd.mobile_driver
            print("Driver-##############################################", self.driver)
        else:
            self.driver = driver
            print("Driver-##############################################", self.driver)

    def verify_settings_open(self):
        status = False
        status, settings_icon = self.driver.find_element('XPATH', locators.settings_icon)
        if status:
            status = self.driver.is_visible(settings_icon)
            print("Settings Application opened.")
        return status

    def open_bluetooth(self):
        error_msg = ""
        status, bt_icon = self.driver.find_element('XPATH',locators.bt_icon)
        if status:
            status = self.driver.click_element(bt_icon)
        else:
            error_msg = "Unable to open Bluetooth page"
        return status,error_msg

    def verify_bt_open(self):
        status = False
        status, bt_toggle = self.driver.find_element('XPATH', locators.bt_toggle)
        if status:
            status = self.driver.is_visible(bt_toggle)
            print("Settings Application opened.")
        return status

    def get_connection_status(self,dut_name):
        status = None
        error_msg = ""
        time.sleep(30)
        status, bt_icon = self.driver.find_element('XPATH', locators.bt_dut.format(dut_name))
        print("elementstatus : ",status)
        if status:
            status = self.driver.get_value(bt_icon)
            print(status)
        else:
            error_msg = "Unable to find DUT"
        return status

    def get_ha_connection_status(self,dut_name):
        status = None
        error_msg = ""
        status, dut_cell = self.driver.find_element('XPATH', locators.DUT_cell.format(dut_name))
        print("elementstatus : ",status)
        if status:
            status,dut_value = dut_cell.find_element('XPATH',locators.conn_status)
            if status:
                status = dut_cell.get_value(dut_value)
            else:
                status = False
            print(status)
        else:
            error_msg = "Unable to find DUT"
        return status


    def click_dut(self,dut_name):
        error_msg = ""
        status, bt_icon = self.driver.find_element('IOSCLASS', locators.bt_dut_text.format(dut_name))
        if status:
            #for i in bt_icon:
            dut_loc= bt_icon.location
            dut_loc_y=dut_loc["y"]
            status,more_info = self.driver.find_element('XPATH',locators.more_info_icon)
            if status:
                # more_loc=more_info.location
                # more_loc_x=more_loc["x"]
                # status=self.driver.click_by_coordinates(more_loc_x,dut_loc_y)
                status=self.driver.click_element(more_info)
            else:
                error_msg = "Unable to find More info button"
        else:
            error_msg = "Unable to find the desired DUT"
        return status,error_msg


    def forget_network(self):
        error_msg = ""
        status,network_forget = self.driver.find_element('XPATH',locators.forget_button)
        if status:
            status = self.driver.click_element(network_forget)
            if status:
                status,forget_confirm = self.driver.find_element('XPATH',locators.forget_confirm)
                if status:
                    status=self.driver.click_element(forget_confirm)
                if not status:
                    error_msg = "Unable to click Forget Network confirm"
            if not status:
                error_msg = "Unable to find Forget network confirm"
        if not status:
            error_msg = "Unable to Find on Forget network"
        return status,error_msg


    def check_and_forget(self,dut_name):
        dut_cleared = False
        connection_status = self.get_connection_status(dut_name)
        print("Status is ",connection_status)
        if connection_status is False:

            print("DUT not found so Forgetting not Required")
            dut_cleared = True
            return  dut_cleared

        if connection_status is None:
            print("Forgetting not required")
            dut_cleared = True

        if connection_status is not None:
            print("Removing old pairing. dut = {}".format(dut_name))
            status= self.click_dut(dut_name)
            if status:
                status,error_msg = self.forget_network()
                if status:
                    dut_cleared = True
        if connection_status is "Not Connected":
            print("Forgetting the old pairings")
            status= self.click_dut(dut_name)
            time.sleep(3)
            if status:
                status,error_msg = self.forget_network()
                if status:
                    dut_cleared = True

        if connection_status is "Connected":
            print("Forgetting the old pairings")
            status= self.click_dut(dut_name)
            time.sleep(3)
            if status:
                status,error_msg = self.forget_network()
                if status:
                    dut_cleared = True

        return dut_cleared

    def ios_delete_pairing_record(self,dut_name):

        status = self.driver.launch_app(sd.config.ios_settings_app_package)
        assert status, "Failed to launch application"
        time.sleep(1)
        status = self.driver.close_app(sd.config.ios_settings_app_package)
        assert status, "Failed to launch application"
        time.sleep(5)
        status = self.driver.launch_app(sd.config.ios_settings_app_package)
        assert status, "Failed to launch application"
        time.sleep(5)

        print("Verify Settings App is open")
        app_open = self.verify_settings_open()
        assert app_open, "Failed to open Settings application"
        time.sleep(3)

        print("Open Bluetooth Page")
        bt_open = self.open_bluetooth()
        assert bt_open, "Failed to Open Bluetooth page"
        time.sleep(3)

        print("Checking and forgetting previous pairings")
        status = self.check_and_forget(dut_name)


    def pair_device_ios(self):
        self.driver.update_respect_alerts()
        print("Checking if there is a pop up to confirm")
        status, popup_button = self.driver.find_element('XPATH', locators.pair)
        if status:
            status = self.driver.click_element(popup_button)
        if not status:
            print("Pairing pop up not shown")
            status = False
        assert status, "Unable to pair the device"

    def cancel_pairing(self):
        self.driver.update_respect_alerts()
        print("Checking if there is a pop up to confirm")
        status, popup_button = self.driver.find_element('XPATH', locators.pair_cancel)
        if status:
            status = self.driver.click_element(popup_button)
        if not status:
            print("Pairing pop up not shown")
            status = False
        assert status, "Unable to cancel the pairing"

    def check_dut_paired_connected(self, dut_name):
        print("Check_paired_connected, DUT = {}".format(dut_name))
        print('Find element = {}'.format(locators.bt_dut.format(dut_name)))
        status, dut_cell = self.driver.find_element('XPATH', locators.bt_dut.format(dut_name))
        time.sleep(2)

        if status:
            print("DUT is found. {}".format(dut_cell))
            time.sleep(2)
            #self.driver.find_ios_cell_text(dut_cell)
            #time.sleep(2)

            '''
            #iPad Air 5/Get exception error
            status = self.driver.get_value(dut_cell)
            print("DUT status: {}".format(status))
            time.sleep(2)

            element_location = dut_cell.location
            x_coordinate = element_location['x']
            y_coordinate = element_location['y']

            element_size = dut_cell.size
            width = element_size['width']
            height = element_size['height']
            print("x,y : {} {}".format(x_coordinate, y_coordinate))
            print("element size : {} {}".format(width, height))
            time.sleep(1)

            if status == 'Not Connected':
                print("BLE not connected")
                return False
            '''
        else:
            print("Device not found")
            return False

        #print("Check more icon. BLE_UART_D55C")
        #status, more_info = self.driver.find_element('XPATH', locators.more_info_icon)
        status, more_info = self.driver.find_element('XPATH', '(//XCUIElementTypeButton[@name="More Info"])[1]')
        if status:
            print("More info button found")
            #time.sleep(1)
            #status = self.driver.click_element(more_info)
            #print("More Info clicked")
        else:
            error_msg = "Unable to find more info button"
            print(error_msg)
            return False
        return True





