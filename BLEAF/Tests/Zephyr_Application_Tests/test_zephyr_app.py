import collections
from time import sleep

import pytest
import time

import concurrent.futures
import datetime

import serial
import logging
import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from collections import OrderedDict
from ...CommonSupportLib.AppScanAndConnect import ScanningandConnection
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
from ...CommonSupportLib.StationData import stationData
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    PHONE_BT_ADDRESS_K, COM_PORT_K, BAUD_RATE_K
from ...CommonSupportLib.BLEUARTFeatureSupportiOS import BLEUARTFeatureSupportiOS
from ...CommonSupportLib.RNBDPairingandLightBlueFeatureSupport import RNBDvsPhoneFeatureSupport

from ...MCP2200.MCP2200 import Mcp2200
from ...StationConfig import conf_file

from ...CommonSupportLib.iOS_BluetoothSupport import iOSBluetoothSupport
from ...CommonSupportLib.iOS_BLEPairingSupport import iOSBLEPairingSupport
from ...BaseWrappers.NewBaseDriver import NewBaseDriver
from ...BaseWrappers.SSHSupport import ShellHandler

sd = stationData()
dut_friendly_name = conf_file.dut_friendly_name

RESET_PIN = 0x02
BTN_CTRL_PIN = 0x04

MCU = Mcp2200()

#phone_list = ["SamsungS21", "GooglePixel5", "OPPO Reno", "SamsungS10", "GooglePixel3A", "VivoV11"]

@pytest.fixture(scope="class", autouse=True)
def define_class_attributes(request, default_class_fixture):
    print("this is local specific class fixture")

    # if (isinstance(request.cls.bleuartfeature, BLEUARTFeatureSupport)):
    #    print("Android: Init MCP2200")
    #    request.cls.bleuartfeature.initialize_com_port()

    def class_finalizer():
        print("Local Class finalizer")

    request.addfinalizer(class_finalizer)


@pytest.fixture(scope="function", autouse=True)
def local_function_fixture(request):
    print("Local function fixture")
    # print("Launch MBD Application")

    test_func_name = request.node.name
    print(f"Fixture {local_function_fixture.__name__} is being used by test: {test_func_name}")

    def function_finalizer():
        print("Local function finalizer")
        # print("Close App")
        if sd.mobile_platform == "iOS" or sd.mobile_platform == 'mac':
            if test_func_name == "test_zephyr_peripheral_hid_ble_bonded":
                sd.mobile_driver.close_app(sd.config.ios_lightblue_app_package)
        else:
            if test_func_name != 'test_zephyr_peripheral_identity':
                app_package = sd.mobile_driver.get_capability('appPackage')
                print(f"Close app.{app_package}")
                sd.mobile_driver.close_app(app_package)
                time.sleep(3)

    request.addfinalizer(function_finalizer)

@pytest.fixture
def remote_appium_handler():
    #assert len(sd.config.multilink_phone_list) > 1, 'Multilink mobile phones config error'
    assert len(sd.config.multilink_phone_list) > 0, 'Multilink mobile phones config error'
    print("ssh_handler fixture")
    ssh_handler = ShellHandler(sd.config.remote_appium_server_ip, sd.config.remote_appium_username,
                               sd.config.remote_appium_pwd)

    multiple_server = True
    if multiple_server:
        print('Running multiple appium server')
        for i in range(sd.config.multilink_phone_list):
            appium_server_logs = "appium_server_logs_{}_{}".format(sd.config.remote_appium_server_ip+i, datetime.datetime.now().strftime(
                "%Y-%m-%d_%H_%M_%S"))
            ip_addr = sd.config.remote_appium_server_ip
            port_num = int(sd.config.remote_appium_server_port)
            start_server_cmd = 'appium -a {} -p {} --relaxed-security > {}.txt &'.format(
                ip_addr, str(port_num+i), appium_server_logs)
            sh_in, sh_out, sh_error = ssh_handler.execute(start_server_cmd)
            if not sh_error:
                print("Remote appium server started successfully. cmd = {}".format(start_server_cmd))
                time.sleep(2)
            else:
                assert False, "Failed to start remote appium server. Command output: {}".format(sh_out)

    else:
        tt = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        ip_addr = sd.config.remote_appium_server_ip
        port_num = sd.config.remote_appium_server_port
        print("start_remote_appium_server. ip = {}, port = {}, time = {}".format(ip_addr, port_num, tt))
        appium_server_logs = "appium_server_logs_{}".format(tt)
        start_server_cmd = 'appium -a {} -p {} --relaxed-security > {}.txt &'.format(ip_addr, port_num,
                                                                                 appium_server_logs)
        sh_in, sh_out, sh_error = ssh_handler.execute(start_server_cmd)
        if not sh_error:
            print("Remote appium server started successfully.")
        else:
            assert False, "Failed to start remote appium server. Command output: {}".format(sh_out)

    yield ssh_handler

    print('Kill remote appium server')
    sh_in, sh_out, sh_error = ssh_handler.execute("ps -a")
    pids = []
    print("List process:")
    for line in sh_out:
        print(line)
        if 'node' in line:
            match = re.match(r'\s*(\d+)', line)
            if match:
                pid = match.group(1)
                pids.append(pid)
                print(f"PID: {pid}")
            else:
                print("PID not found.")

    print("Appium server. PID.count = {}".format(len(pids)))

    if len(pids) != 0:
        for pid in pids:
            print('killing appium process,pid = {}'.format(pid))
            cmd = 'kill -9 {}'.format(pid)
            sh_in, sh_out, sh_error = ssh_handler.execute(cmd)
            if not sh_error:
                print("Appium Process Killed Successfully. cmd = {}".format(cmd))
            else:
                assert False, "Failed to kill currently running appium. " \
                              "Please kill the process manually and restart execution. cmd output: {}".format(sh_out)

@pytest.fixture
def multilink_mobile_drivers(remote_appium_handler):
    print("Initial multilink_drivers")
    time.sleep(15)
    app_package = sd.config.app_package
    app_activity = sd.config.app_activity
    #for phone in sd.config.multilink_phone_list:
    for i in range(sd.config.multilink_phone_list):
        #print('mobile phone = {}'.format(phone))
        phone = sd.config.multilink_phone_list[i]
        mobile_to_use = sd.config.mobile_data_config.get(phone)
        port = sd.config.remote_appium_server_port
        driver = NewBaseDriver(sd.config.remote_appium_server_ip, str(port+i),
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            app_package, app_activity,
                            fresh_env=False)
        print(f'Create driver for mobile phone:{phone}')
        app_package = driver.get_capability('appPackage')
        print("app_package: {0}".format(app_package))
        driver.close_app(app_package)
        time.sleep(5)
        status = driver.launch_app(app_package)
        time.sleep(3)
        assert status, "Failed to launch application"
        mobile_data_dic = {}
        mobile_data_dic['driver'] = driver
        mobile_data_dic['phone'] = phone
        sd.multilink_mobile_driver.append(mobile_data_dic)
    #sd.mobile_driver = driver
    tt = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    print(f"complete.time = {tt}")

    yield sd.multilink_mobile_driver

    print('multilink quit drivers')
    for index, dat in enumerate(sd.multilink_mobile_driver):
        m_driver = dat['driver']
        m_driver.quit_driver()

class TestZephyrApp:
    bleState = "Disconnected"
    operate_characteristic = ""
    hid_dut_name = ""
    test_procedure = ""

    #@pytest.mark.order(3)
    @pytest.mark.skip(reason="test_zephyr_peripheral_hid_forget_device")
    #@pytest.mark.test_id("Zephyr Peripheral HID Forget Device", '')
    def test_zephyr_peripheral_hid_forget_device(self):
        print("test_zephyr_peripheral_hid_forget_device")
        sd.mobile_driver.app_activate(sd.config.ios_settings_app_package)
        time.sleep(5)
        pairing = iOSBLEPairingSupport()
        #pairing.ios_delete_pairing_record('Test HoG mouse')
        print('HID dut = {}'.format(TestZephyrApp.hid_dut_name))
        pairing.check_dut_is_paired_connected(TestZephyrApp.hid_dut_name, delete=True)
        time.sleep(5)
        status = self.iocontrolledstatus.Zephyr_IO_Default(MCU)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)
        #status = pairing.check_and_forget('Test HoG mouse')
        #assert status, 'Remove pairing: Failed'

    #@pytest.mark.order(1)
    # @pytest.mark.test_id("Zephyr Peripheral HID Pairing", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_hid_pairing")
    def test_zephyr_peripheral_hid_pairing_connect(self):
        print("test_zephyr_peripheral_hid_pairing_connect")
        print('Active app = {}'.format(sd.config.ios_lightblue_app_package))
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        time.sleep(2)
        print('DUT Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        sd.mobile_driver.app_activate(sd.config.ios_lightblue_app_package)
        scan_time = 6
        time.sleep(scan_time)
        print('scan time = {}'.format(scan_time))
        TestZephyrApp.hid_dut_name = 'Test HoG mouse'
        self.bleuartfeature.lightblue_filter_peripherals('Test HoG mouse')
        time.sleep(3)
        print("Connect")
        passkey = self.bleuartfeature.lightblue_pairing_connect('Test HoG mouse')
        #time.sleep(10)
        try:
            print('Pairing...')
            wait = WebDriverWait(sd.mobile_driver.driver, 5, poll_frequency=0.5)
            wait.until(EC.alert_is_present())
            print("Alert is present")
            if len(passkey) == 6:
                self.bleuartfeature.pairing_alert_sendkey('Test HoG mouse', passkey)
            else:
                print("Bluetooth Pairing is failed")
            time.sleep(5)
        except WebDriverException:
            print('WebDriverException')

        status = sd.mobile_driver.close_app(sd.config.ios_lightblue_app_package)
        assert status, "Failed to close application"
        print("Close lightblue app")

    #@pytest.mark.order(1)
    #@pytest.mark.test_id("Zephyr Peripheral HID Pairing", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_hid_pairing")
    def test_zephyr_peripheral_hid_pairing_connect_1(self):
        print("test_zephyr_peripheral_hid_pairing_connect")
        print('Active app = {}'.format(sd.config.ios_settings_app_package))
        sd.mobile_driver.app_activate(sd.config.ios_settings_app_package)
        time.sleep(5)
        sd.mobile_driver.close_app(sd.config.ios_settings_app_package)
        time.sleep(5)
        sd.mobile_driver.launch_app(sd.config.ios_settings_app_package)
        #print('Scanning...')
        time.sleep(5)
        pairing = iOSBLEPairingSupport()

        print("Verify Settings App is open")
        app_open = pairing.verify_settings_open()
        assert app_open, "Failed to open Settings application"
        time.sleep(3)

        #MCU = Mcp2200()
        #time.sleep(1)
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        time.sleep(2)

        print('DUT Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(3)

        print("Open Bluetooth Page")
        bt_open = pairing.open_bluetooth()
        assert bt_open, "Failed to Open Bluetooth page"
        scan_time = 10
        print('Scanning...time={}'.format(scan_time))
        time.sleep(scan_time)

        passkey = pairing.get_dut_pair_passkey('Test HoG mouse')
        try:
            print('Pairing...')
            wait = WebDriverWait(sd.mobile_driver.driver, 5, poll_frequency=0.5)
            wait.until(EC.alert_is_present())
            print("Alert is present")
            if len(passkey) == 6:
                pairing.pairing_alert_sendkey('Test HoG mouse', passkey)
            else:
                print("Bluetooth Pairing is failed")
            time.sleep(5)
        except WebDriverException:
            print('WebDriverException')

    #@pytest.mark.order(2)
    #@pytest.mark.test_id("Zephyr Peripheral HID", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_hid")
    def test_zephyr_peripheral_hid_mouse_click(self):
        print("Testing Zephyr Peripheral HID Mouse click. BLE Bonded")
        print("Make sure all of the paired devices are deleted")
        if sd.mobile_platform == "iOS":
            sd.mobile_driver.app_activate(sd.config.ios_settings_app_package)
            time.sleep(5)
            sd.mobile_driver.close_app(sd.config.ios_settings_app_package)
            time.sleep(5)
            sd.mobile_driver.launch_app(sd.config.ios_settings_app_package)
        else:
            print('Platform "Android" not supported')
        time.sleep(5)
        print('Launch ios setting, Check BLE connection')

        #MCU = Mcp2200()
        #time.sleep(1)
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        time.sleep(1)

        iOSpairingsupport = iOSBLEPairingSupport(sd.mobile_driver)

        print("Verify Settings App is open")
        app_open = iOSpairingsupport.verify_settings_open()
        assert app_open, "Failed to open Settings application"
        time.sleep(5)

        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(3)

        print("Open Bluetooth Page")
        bt_open = iOSpairingsupport.open_bluetooth()
        assert bt_open, "Failed to Open Bluetooth page"
        time.sleep(3)

        iOSpairingsupport.check_dut_is_paired_connected(TestZephyrApp.hid_dut_name)
        #status = iOSpairingsupport.check_dut_paired_connected('Test HoG mouse')
        #assert status == 'Connected', "Failed to find the paired device: Test HoG mouse"
        time.sleep(3)

        print('Launch HID test app')
        sd.mobile_driver.app_activate('com.microchip.MBDtest')

        print('Test HoG mouse. click test')

        status, click_button = sd.mobile_driver.find_element('id', 'zephyr_hid_test')
        assert status, "Failed to find the element id"
        time.sleep(1)
        state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(state))
        time.sleep(1)

        print('Click button 3 times.')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)

        new_state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(new_state))

        status = sd.mobile_driver.close_app('com.microchip.MBDtest')
        assert status, "Failed to close application"
        time.sleep(5)

        assert state != new_state, "HID test failed"
        print('Remove paired device: Test HoG mouse')

    #@pytest.mark.order(1)
    #@pytest.mark.test_id("Zephyr Peripheral Android HID Pairing", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_android_hid_pairing")
    def test_zephyr_peripheral_android_hid_pairing_connect(self):
        print('test_zephyr_peripheral_android_hid_pairing_connect')
        TestZephyrApp.test_procedure = ''
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(2)
        sd.mobile_driver.close_app('com.android.settings')
        time.sleep(5)
        print("Launch setting app")
        sd.mobile_driver.launch_app('com.android.settings')
        time.sleep(5)
        print('DUT Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(3)
        print('Settings ==> Connected Devices')
        status, connected_device = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Connected devices"]')
        assert status, "Failed to find the element."
        connected_device.click()
        time.sleep(3)
        status, id_1 = sd.mobile_driver.find_element('ID', 'Connected devices')
        assert status, "Failed to find the ID:Connected devices"
        print('Connected Devices ==> Pair new device')
        status, pair_device = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Pair new device"]')
        assert status, "Failed to find the element."
        pair_device.click()
        time.sleep(5)
        status, id_2 = sd.mobile_driver.find_element('ID', 'Pair new device')
        assert status, "Failed to find the ID:Pair new device"
        print('Pair new device ==> Discover and connect')
        status, dut = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Test HoG mouse"]')
        assert status, "Failed to find the Test HoG mouse."
        passkey = self.bleuartfeature.get_serial_data_passkey(dut)
        #print('Click. Test HoG mouse')
        #dut.click()
        time.sleep(1)
        status, alert = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.android.settings:id/alertTitle"]')
        assert status, "Failed to find the alert title."
        if 'Pair with Test HoG mouse' in alert.text:
            time.sleep(1)
            assert len(passkey) == 6, 'Passkey error!'
            print(f'Pairing. passkey={passkey}')
            status, edit = sd.mobile_driver.find_element('XPATH', '//android.widget.EditText[@resource-id="com.android.settings:id/text"]')
            assert status, "Failed to find the edit text."
            edit.send_keys(passkey)
            #edit.send_keys('727816')
            #print('Send passkey:727816')
            #edit.send_keys('123456')
            #print('Send passkey:123456')
            time.sleep(3)

        status, button = sd.mobile_driver.find_element('XPATH', '//android.widget.Button[@resource-id="android:id/button1"]')
        assert status, "Failed to find the element."
        if 'OK' in button.text:
            print(f'press ok button')
            button.click()
            time.sleep(15)

        #Check pairing success
        status, id_1 = sd.mobile_driver.find_element('ID', 'Connected devices')
        assert status, "Failed to find the ID:Connected devices"
        print('Pair new device == > Connected Devices')
        time.sleep(1)
        status, paired_dut = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Test HoG mouse"]')
        assert status, "Failed to find the Test HoG mouse."
        print('Pairing success')
        time.sleep(1)
        sd.mobile_driver.close_app('com.android.settings')
        time.sleep(5)
        TestZephyrApp.test_procedure = 'android_hid_pairing_connect'

    #@pytest.mark.order(2)
    #@pytest.mark.test_id("Zephyr Peripheral HID Android", '')
    @pytest.mark.skip(reason="test_zephyr_android_peripheral_hid")
    def test_zephyr_peripheral_android_hid_mouse_click(self):
        if TestZephyrApp.test_procedure != 'android_hid_pairing_connect':
            print('Unknown state:test_zephyr_peripheral_android_hid_mouse_click')
            return
        else:
            TestZephyrApp.test_procedure = ''

        print("Testing Zephyr Peripheral Android HID Mouse click. BLE Bonded")

        #self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        #time.sleep(1)

        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(3)

        print('Launch HID test app')
        sd.mobile_driver.app_activate('com.microchip.zephyrtest')
        #sd.mobile_driver.launch_app('com.microchip.zephyrtest')
        time.sleep(5)

        print('Test HoG mouse. click test')

        status, click_button = sd.mobile_driver.find_element('id', 'zephyr_hid_test')
        assert status, "Failed to find the element id"
        time.sleep(1)

        state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(state))
        time.sleep(1)

        print('Click button 3 times.')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)

        new_state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(new_state))
        time.sleep(1)

        #assert state != new_state, "HID test failed"
        assert int(new_state)-int(state) == 3, 'HID test failed'
        #print('Remove paired device: Test HoG mouse')

        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(5)

        state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(state))
        time.sleep(1)

        print('Click button 2 times.')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)

        new_state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(new_state))
        time.sleep(1)

        # assert state != new_state, "HID test failed"
        assert int(new_state) - int(state) == 2, 'HID test failed'
        #print('Remove paired device: Test HoG mouse')

        TestZephyrApp.test_procedure = 'android_hid_mouse_click'
        time.sleep(1)

    #@pytest.mark.order(3)
    @pytest.mark.skip(reason="test_zephyr_peripheral_android_hid_forget_device")
    #@pytest.mark.test_id("Zephyr Peripheral HID Android Forget device", '')
    def test_zephyr_peripheral_android_hid_forget_device(self):
        if TestZephyrApp.test_procedure != 'android_hid_mouse_click':
            print('Unknown state:test_zephyr_peripheral_android_hid_forget_device')
            return
        else:
            TestZephyrApp.test_procedure = ''

        print('test_zephyr_peripheral_android_hid_forget_device')

        print('Activate settings app')
        sd.mobile_driver.app_activate('com.android.settings')

        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(3)

        print('Settings ==> Connected Devices')
        status, connected_device = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Connected devices"]')
        assert status, "Failed to find the element."
        connected_device.click()
        time.sleep(3)

        status, id = sd.mobile_driver.find_element('ID', 'Connected devices')
        assert status, "Failed to find the ID:Connected devices"
        print('Connected Devices')
        time.sleep(1)

        status, paired_dut = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Test HoG mouse"]')
        assert status, "Failed to find the Test HoG mouse."
        paired_dut.click()
        time.sleep(3)

        status, dev_details = sd.mobile_driver.find_element('ID', 'Device details')
        assert status, "Failed to find the ID:Device details."
        print(f"Connected Devices ==> {dev_details.text}")
        time.sleep(2)

        status, forget_button = sd.mobile_driver.find_element('XPATH', '//android.widget.Button[@resource-id="com.android.settings:id/button1"]')
        assert status, "Failed to find the Forget button."
        time.sleep(1)
        #print(f'Find button: {forget_button.text}')
        assert forget_button.text == 'Forget', 'Failed to find the Forget'
        print(f'Find Forget button')
        forget_button.click()
        time.sleep(3)

        #status, alert = sd.mobile_driver.find_element('ID', 'com.android.settings:id/alertTitle')
        status, alert = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.android.settings:id/alertTitle"]')
        assert status, "Failed to find the alert title."
        time.sleep(1)
        assert alert.text == 'Forget device?', "Alert title: Error"
        time.sleep(1)

        status, button = sd.mobile_driver.find_element('XPATH', '//android.widget.Button[@resource-id="android:id/button1"]')
        assert status, "Failed to find the Alert Forget button."
        time.sleep(1)
        assert button.text == 'Forget device', "Alert Forget device not found"
        time.sleep(1)
        button.click()
        print('Click Forget device button')
        time.sleep(2)

        status = self.iocontrolledstatus.Zephyr_IO_Default(MCU)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

    @pytest.mark.test_id("Zephyr peripheral identity", '')
    #@pytest.mark.skip(reason="test_zephyr_peripheral_identity")
    def test_zephyr_peripheral_identity(self, multilink_mobile_drivers):
        print('test_zephyr_peripheral_identity')
        assert len(sd.multilink_mobile_driver) == len(sd.config.multilink_phone_list), 'Fail to create drivers'
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(2)

        zephyr_test = []
        test_result = {}
        for index, dat in enumerate(sd.multilink_mobile_driver):
            if index == 0:
                print('I/O Reset. Firmware reset')
                self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
            m_driver = dat['driver']
            m_phone = dat['phone']
            mbd_ble_smart_featuresupport = RNBDvsPhoneFeatureSupport(driver=m_driver)
            time.sleep(1)
            mbd_ble_smart_featuresupport.open_ble_smart_scanner()
            time.sleep(6)
            mbd_ble_smart_featuresupport.ble_smart_filter_peripherals('Zephyr', search_icon=True)
            time.sleep(2)
            mbd_ble_smart_featuresupport.ble_smart_connect('Zephyr Peripheral')
            print('Ble connecting..')
            time.sleep(3)
            connection, bt_address = mbd_ble_smart_featuresupport.ble_smart_connect_and_get_info('Zephyr Peripheral', m_phone)
            print('test phone:{}, ble:{}, bt_address:{}'.format(m_phone, connection, bt_address))
            assert connection == 'Connected', 'test phone {}. Failed to connect to the device'.format(m_phone)
            test_result[m_phone] = connection + ',' + bt_address
            zephyr_test.append(mbd_ble_smart_featuresupport)
            time.sleep(2)
        print(f'test result: {test_result}')
        test_time = 60
        print(f'Long-term idle test. test time = {test_time}')

        '''
        app_drivers = []
        elements = []
        for i in range(len(sd.multilink_mobile_driver)):
            phone_driver = sd.multilink_mobile_driver[i]
            m_driver = phone_driver['driver']
            app_drivers.append(m_driver)
            #m_phone = phone_driver['phone']
            status, state_element = m_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.microchip.bluetooth.data:id/connection_state"]')
            assert status, "Failed to find the state_element"
            elements.append(state_element)
        print(f'Get driver.element. len = {len(app_drivers)}')

        for i in range(test_time):
            for j in range(len(app_drivers)):
                app_driver = app_drivers[j]
                element = elements[j]
                state = app_driver.get_text(element)
                print(f'time:{i}, app_index{j}, ble state: {state}')
                time.sleep(1)
        print('multilink long-term idle test complete')
        '''
        status = self.iocontrolledstatus.Zephyr_IO_Default(MCU)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        #for index, dat in enumerate(sd.multilink_mobile_driver):
        #    m_driver = dat['driver']
        #    m_driver.quit_driver()
        print('test complete')


    #@pytest.mark.test_id("Zephyr peripheral hid demo", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_hid")
    def test_zephyr_peripheral_hid_demo(self):
        print("Testing Zephyr Peripheral HID. BLE Bonded")
        print("Make sure all of the paired devices are deleted")
        if sd.mobile_platform == "iOS":
            sd.mobile_driver.close_app(sd.config.ios_lightblue_app_package)
            time.sleep(10)
        else:
            print('Platform "Android" not supported')
        time.sleep(5)
        print('Launch ios setting, Check BLE connection')
        mobile_to_use = sd.config.mobile_data_config.get(sd.platform)
        driver = NewBaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.ios_settings_app_package, fresh_env=False)
        time.sleep(5)
        iOSpairingsupport = iOSBluetoothSupport(driver)
        print("new iOSBluetoothSupport driver")
        #status = driver.launch_app(sd.config.ios_settings_app_package)
        #assert status, "Failed to launch application"
        #time.sleep(1)
        status = driver.close_app(sd.config.ios_settings_app_package)
        assert status, "Failed to close setting app"
        time.sleep(5)
        status = driver.launch_app(sd.config.ios_settings_app_package)
        assert status, "Failed to launch setting app"
        time.sleep(5)
        print("Verify Settings App is open")
        app_open = iOSpairingsupport.verify_settings_open()
        assert app_open, "Failed to open Settings application"
        time.sleep(5)
        print("Open Bluetooth Page")
        bt_open = iOSpairingsupport.open_bluetooth()
        assert bt_open, "Failed to Open Bluetooth page"
        time.sleep(3)
        status = iOSpairingsupport.check_dut_paired_connected('Test HoG mouse')
        assert status, "Failed to find the paired device"
        time.sleep(3)
        status = driver.close_app(sd.config.ios_settings_app_package)
        assert status, "Failed to close application"
        time.sleep(5)
        print('Launch HID test app')
        driver = NewBaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            'com.microchip.MBDtest', fresh_env=False)
        time.sleep(5)
        status = driver.close_app('com.microchip.MBDtest')
        assert status, "Failed to close HID test app"
        time.sleep(5)
        status = driver.launch_app('com.microchip.MBDtest')
        assert status, "Failed to launch HIS test app"
        time.sleep(5)
        print('Test HoG mouse. click test')
        time.sleep(5)
        status, click_button = driver.find_element('id', 'zephyr_hid_test')
        assert status, "Failed to find the element id"
        time.sleep(1)
        state = driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(state))
        time.sleep(5)
        status = driver.close_app('com.microchip.MBDtest')
        assert status, "Failed to close application"
        time.sleep(5)

    #@pytest.mark.order(1)
    #@pytest.mark.test_id("Zephyr Direct Advertising Pairing Connect", '')
    @pytest.mark.skip(reason="test_zephyr_direct_advertising Pairing Connect")
    def test_zephyr_direct_advertising_pairing_connect(self):
        print("Testing Zephyr Direct Advertising Pairing Connect")
        assert sd.mobile_platform == "Android", 'Test test case is only or Android phones'
        TestZephyrApp.test_procedure = ''
        print('ble state = {}'.format(TestZephyrApp.bleState))
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(2)
        # 3 option for pairing. (pairing timeout, pairing cancel, pairing accept)
        for i in range(3):
            if i in range(3):
                app_package = sd.mobile_driver.get_capability('appPackage')
                print("app package= {}".format(app_package))
                sd.mobile_driver.close_app(app_package)
                time.sleep(5)
                print("Launch app")
                sd.mobile_driver.launch_app(app_package)
                time.sleep(5)
                self.scanandconnect.verify_app_open()
                assert status, 'MBD open fail'
                time.sleep(3)
                print('DUT Reset. Firmware reset')
                self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
                print("open_ble_smart_scanner")
                self.scanandconnect.open_ble_smart_scanner()
                time.sleep(10)
            else:
                self.bleuartfeature.ble_smart_go_back()
                print('DUT Reset. Firmware reset')
                self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
                time.sleep(3)

            self.bleuartfeature.ble_smart_filter_peripherals('Direct', search_icon=True)
            time.sleep(2)
            self.bleuartfeature.ble_smart_connect('Direct A')
            print('Ble connecting..')
            time.sleep(3)
            connection_state = self.bleuartfeature.ble_smart_verify_ble_connected('Direct A')
            assert connection_state == "Connected", 'Error, failed to connect to dut'
            TestZephyrApp.bleState = connection_state
            time.sleep(2)
            self.bleuartfeature.ble_smart_characteristic_write('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef2', '1234')
            if i == 0:
                action = 'timeout'
            elif i == 1:
                action = 'cancel'
            elif i == 2:
                action = 'accept'
            result = self.bleuartfeature.ble_smart_pairing_google_phone('Direct A', action)

            if i == 2:
                time.sleep(60)
                assert result, "[SMP_accept_pairing]Failed to parse the serial output data."
                TestZephyrApp.bleState = 'Pairing complete.Reset'
                print('Pairing complete')
                time.sleep(1)
            else:
                assert result, '[SMP_pairing_timeout_cancel]Failed to parse the serial output data.'

            '''
            #These code doesn't work on Google Pixel
            time.sleep(2)
            try:
                if i == 0:
                    action = 'timeout'
                elif i == 1:
                    action = 'cancel'
                elif i == 2:
                    action = 'accept'
                print('Pairing...')
                wait = WebDriverWait(sd.mobile_driver.driver, 5, poll_frequency=0.5)
                wait.until(EC.alert_is_present())
                print("Alert is present")
                result = self.bleuartfeature.ble_smart_pairing('Direct A', action)
                if result:
                    print('test result: PASS')
                else:
                    print('test result: FAIL')
                if action == 'accept':
                    print('Device reboot. Direct advertising start')
                    time.sleep(60)
                else:
                    time.sleep(5)
                #result = self.bleuartfeature.ble_smart_pairing('Direct A', 'timeout')
                #result = self.bleuartfeature.ble_smart_pairing('Direct A', 'accept')
            except WebDriverException:
                print('WebDriverException. Pairing alert ')
            '''

    #@pytest.mark.order(2)
    #@pytest.mark.test_id("Zephyr Direct Advertising Data Read/Write", '')
    @pytest.mark.skip(reason="test_zephyr_direct_advertising_gatt_read_write")
    def test_zephyr_direct_advertising_gatt_read_write(self):
        if TestZephyrApp.bleState != 'Pairing complete.Reset':
            print("test_zephyr_direct_advertising_gatt_read_write. Unknown state:{}".format(TestZephyrApp.bleState))
            return
        else:
            print('test_zephyr_direct_advertising_gatt_read_write')
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        time.sleep(2)
        print('Activate lightblue app')
        sd.mobile_driver.app_activate(sd.config.lightblue_app_package)
        time.sleep(10)
        app_package = sd.mobile_driver.get_capability('appPackage')
        print("app package= {}".format(app_package))
        sd.mobile_driver.close_app(sd.config.lightblue_app_package)
        time.sleep(3)
        print("Launch lightblue app")
        sd.mobile_driver.launch_app(sd.config.lightblue_app_package)
        time.sleep(3)
        self.bleuartfeature.ble_lightblue_Bonded('Direct A')
        time.sleep(1)
        sd.mobile_driver.close_app(sd.config.lightblue_app_package)
        time.sleep(3)
        print('Activate MBD app')
        sd.mobile_driver.app_activate(sd.config.app_package)
        time.sleep(3)
        status = self.scanandconnect.verify_app_open()
        assert status, "MBD open fail"
        time.sleep(3)
        print('DUT Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        print("open_ble_smart_scanner")
        self.scanandconnect.open_ble_smart_scanner()
        time.sleep(10)
        self.bleuartfeature.ble_smart_filter_peripherals('Direct', search_icon=True)
        time.sleep(3)
        self.bleuartfeature.ble_smart_connect('Direct A')
        print('Ble connecting..')
        time.sleep(3)
        connection_state = self.bleuartfeature.ble_smart_verify_ble_connected('Direct A')
        assert connection_state == "Connected - Bonded", 'Error, failed to connect to dut'
        TestZephyrApp.bleState = connection_state
        print('state = {}'.format(TestZephyrApp.bleState))
        time.sleep(2)
        write_data = '12345678'
        self.bleuartfeature.ble_smart_characteristic_write('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef2', write_data)
        time.sleep(2)
        self.bleuartfeature.ble_smart_go_back()
        time.sleep(5)
        read_data = self.bleuartfeature.ble_smart_characteristic_read('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef1')
        time.sleep(2)
        self.bleuartfeature.ble_smart_go_back()
        time.sleep(5)
        write_data = '09abcdef'
        self.bleuartfeature.ble_smart_characteristic_write('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef2', write_data, char_found=True)
        time.sleep(2)
        self.bleuartfeature.ble_smart_go_back()
        time.sleep(5)
        read_data = self.bleuartfeature.ble_smart_characteristic_read('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef1')
        time.sleep(2)
        self.bleuartfeature.ble_smart_go_back()
        time.sleep(5)
        TestZephyrApp.bleState = self.bleuartfeature.ble_smart_disconnect()
        print('ble state = {}'.format(TestZephyrApp.bleState))
        time.sleep(5)
        if TestZephyrApp.bleState == 'Disconnected - Bonded':
            print('test_zephyr_direct_advertising_unbond')
            state = self.bleuartfeature.ble_smart_unbond()
            print('ble state = {}'.format(state))
            time.sleep(3)
        else:
            print('test_zephyr_direct_advertising_unbond. Unknown state: {}'.format(TestZephyrApp.bleState))
            time.sleep(1)
        status = self.iocontrolledstatus.Zephyr_IO_Default(MCU)
        assert status, "[MCP2200 I/O state] Failed to restore to default"
        time.sleep(1)

    #@pytest.mark.order(1)
    #@pytest.mark.test_id("Zephyr peripheral application v1 rc5", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_rc5")
    def test_zephyr_peripheral_application(self):
        sd.mobile_driver.close_app(sd.config.ios_lightblue_app_package)
        time.sleep(5)
        print("Close app and launch again")
        sd.mobile_driver.launch_app(sd.config.ios_lightblue_app_package)
        time.sleep(5)
        print('test_zephyr_peripheral_application_v1_rc5')
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(1)
        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(3)
        print("Search peripherals by name")
        time.sleep(3)
        self.bleuartfeature.lightblue_filter_peripherals('Zephyr Peripheral')
        time.sleep(3)
        print("Connect")
        self.bleuartfeature.lightblue_connect('Zephyr Peripheral Sample Long')
        #self.bleuartfeature.lightblue_connect('Zephyr Peripheral Sample Long Name')
        time.sleep(10)
        self.bleuartfeature.lightblue_verify_ble_connected()
        time.sleep(3)
        self.bleuartfeature.lightblue_get_device_info_data()
        time.sleep(3)
        self.bleuartfeature.lightblue_verify_ble_services_characteristics()
        time.sleep(3)
        #self.bleuartfeature.lightblue_scroll_gesture('0', scroll_element='Immediate Alert', direction='down')
        #time.sleep(3)
        #self.bleuartfeature.lightblue_scroll_gesture('0', scroll_element='Device Information', direction='down')
        #time.sleep(3)
        #self.bleuartfeature.lightblue_get_device_info_data()
        #time.sleep(3)
        self.bleuartfeature.lightblue_ble_disconnect()
        status = self.iocontrolledstatus.Zephyr_IO_Default(MCU)
        assert status, "[MCP2200 I/O state] Failed to restore to default"
        time.sleep(1)


################################################################################################

    @pytest.mark.skip(reason="Zephyr test reset")
    # @pytest.mark.test_id("Zephyr test reset", 'Putty')
    def test_zephyr_reset(self):
        print('test_zephyr_reset')
        # MCU = Mcp2200()
        # time.sleep(1)
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        print('Open Putty')
        time.sleep(20)

        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(10)
        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(10)

    #@pytest.mark.test_id("Mac_lightblue_scan_and_connect", '')
    @pytest.mark.skip(reason="Used for BLE_UART firmware")
    def test_mac_lightblue_scan_and_connect(self):
        print("test_lightblue_ble_uart_application")
        print("Search peripherals by name")
        time.sleep(3)
        self.bleuartfeature.lightblue_filter_peripherals('CDDF')
        time.sleep(3)
        print("Connect")
        self.bleuartfeature.lightblue_connect('BLE_UART_CDDF')
        time.sleep(10)
        self.bleuartfeature.lightblue_verify_ble_connected()
        time.sleep(5)
        #self.bleuartfeature.lightblue_get_device_info_data()
        #time.sleep(5)
        self.bleuartfeature.lightblue_verify_ble_services_characteristics()
        time.sleep(5)
        '''
        status, service = self.bleuartfeature.lightblue_verify_ble_services_and_characteristics()
        if not status:
            print("Failed to verify ble services and characteristics. service={}".format(service))
            self.bleuartfeature.lightblue_scroll_gesture(-500)
            time.sleep(2)
            status, service = self.bleuartfeature.lightblue_verify_ble_services_and_characteristics(start_service=service)
            if status:
                print("lightblue_verify_ble_services_and_characteristics: PASS")
                time.sleep(5)
        else:
            print("lightblue_verify_ble_services_and_characteristics: PASS")
            time.sleep(5)
        '''
        '''
        print('Discover MCHP Transparent services and characteristics')
        self.bleuartfeature.lightblue_enter_characteristic_scene('0x49535343-4C8A-39B3-2F49-511CFF073B7E')
        time.sleep(5)
        self.bleuartfeature.lightblue_characteristic_action('0x49535343-4C8A-39B3-2F49-511CFF073B7E', 'Subscribe')
        time.sleep(5)
        self.bleuartfeature.lightblue_characteristic_write('0x49535343-4C8A-39B3-2F49-511CFF073B7E', '0x14')
        time.sleep(5)
        self.bleuartfeature.lightblue_characteristic_read('0x49535343-4C8A-39B3-2F49-511CFF073B7E')
        time.sleep(5)
        self.bleuartfeature.lightblue_characteristic_action('0x49535343-4C8A-39B3-2F49-511CFF073B7E', 'Unsubscribe')
        time.sleep(5)
        self.bleuartfeature.lightblue_characteristic_screen_goback()
        time.sleep(5)
        '''
        self.bleuartfeature.lightblue_ble_disconnect()

    @pytest.mark.skip(reason="test_appium_my_test")
    #@pytest.mark.test_id("test_appium_function", '')
    def test_appium_my_test(self):
        print("test_appium_my_test")
        if sd.mobile_platform == "iOS":
            sd.mobile_driver.app_activate(sd.config.ios_settings_app_package)
            time.sleep(5)
            sd.mobile_driver.close_app(sd.config.ios_settings_app_package)
            time.sleep(5)
            sd.mobile_driver.launch_app(sd.config.ios_settings_app_package)
        else:
            print('Platform "Android" not supported')
        time.sleep(5)
        print('Launch ios setting, Check BLE connection')

        iOSpairingsupport = iOSBLEPairingSupport(sd.mobile_driver)

        print("Verify Settings App is open")
        app_open = iOSpairingsupport.verify_settings_open()
        assert app_open, "Failed to open Settings application"
        time.sleep(5)

        print("Open Bluetooth Page")
        bt_open = iOSpairingsupport.open_bluetooth()
        assert bt_open, "Failed to Open Bluetooth page"
        time.sleep(3)

        status = iOSpairingsupport.check_dut_is_paired_connected('ADDON APOLLO 2.0', delete=True)
        #status = iOSpairingsupport.check_dut_is_paired_connected('ADDON APOLLO 2.0')
        #assert status == 'Connected', "Failed to find paired device"
        time.sleep(30)

    @pytest.mark.skip(reason="test_remote_mcp2200_feature")
    #@pytest.mark.test_id("test_remote_mcp2200_feature", '')
    def test_remote_mcp2200_feature(self):
        print("test_remote_mcp2200_feature")
        time.sleep(3)
        self.mcp2200manager.run()
        print('mcp2200manager. Running')
        time.sleep(5)
        #time.sleep(30)
        #print("Wait 30 seconds")
        #self.mcp2200manager.stop()
        print('Send data to server')
        self.mcp2200manager.send_to_server("Hello mcp2200")
        time.sleep(5)
        self.mcp2200manager.send_to_server("stop")
        time.sleep(5)
        #self.mcp2200manager.shutdown()
        #time.sleep(5)









