import collections
from time import sleep

import pytest
import time

import concurrent.futures
import datetime

import serial

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

from ...MCP2200.MCP2200 import Mcp2200
from ...StationConfig import conf_file

from ...CommonSupportLib.iOS_BluetoothSupport import iOSBluetoothSupport
from ...CommonSupportLib.iOS_BLEPairingSupport import iOSBLEPairingSupport
from ...BaseWrappers.NewBaseDriver import NewBaseDriver

sd = stationData()
dut_friendly_name = conf_file.dut_friendly_name

bleState = "Disconnected"
operate_characteristic = ""

RESET_PIN = 0x02
BTN_CTRL_PIN = 0x04

MCU = Mcp2200()

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
    if test_func_name == "test_zephyr_peripheral_hid_ble_bonded":
        print("Fixture is being used by test_zephyr_peripheral_hid_ble_bonded")
        '''
        mobile_to_use = sd.config.mobile_data_config.get(sd.platform)
        driver = NewBaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.ios_settings_app_package, fresh_env=False)
        time.sleep(2)
        iOSpairingsupport = iOSBluetoothSupport(driver)
        print("new iOSBluetoothSupport driver")
        '''


    def function_finalizer():
        print("Local function finalizer")
        # print("Close App")
        if sd.mobile_platform == "iOS" or sd.mobile_platform == 'mac':
            if test_func_name == "test_zephyr_peripheral_hid_ble_bonded":
                sd.mobile_driver.close_app(sd.config.ios_lightblue_app_package)
        else:
            app_package = sd.mobile_driver.get_capability('appPackage')
            print("Close app")
            sd.mobile_driver.close_app(app_package)
        time.sleep(3)

    request.addfinalizer(function_finalizer)

class TestZephyrApp:

    @pytest.mark.skip(reason="Zephyr test reset")
    #@pytest.mark.test_id("Zephyr test reset", 'Putty')
    def test_zephyr_reset(self):
        print('test_zephyr_reset')
        #MCU = Mcp2200()
        #time.sleep(1)
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        print('Open Putty')
        time.sleep(20)

        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(10)
        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
        time.sleep(10)

    #@pytest.mark.order(3)
    @pytest.mark.skip(reason="test_zephyr_peripheral_hid_forget_pairing")
    #@pytest.mark.test_id("Zephyr Peripheral HID Forget Pairing", '')
    def test_zephyr_peripheral_hid_forget_pairing(self):
        print("test_zephyr_peripheral_hid_forget_pairing")
        sd.mobile_driver.app_activate(sd.config.ios_settings_app_package)
        time.sleep(5)
        pairing = iOSBLEPairingSupport()
        pairing.ios_delete_pairing_record('Test HoG mouse')
        time.sleep(5)
        self.iocontrolledstatus.Zephyr_IO_Default(MCU)
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

        status = iOSpairingsupport.check_dut_paired_connected('Test HoG mouse')
        assert status == 'Connected', "Failed to find the paired device: Test HoG mouse"
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

    #@pytest.mark.test_id("Zephyr Direct Advertising", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_hid")
    def test_zephyr_peripheral_hid_1(self):
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
    #@pytest.mark.test_id("Zephyr Direct Advertising Scan Connect", '')
    @pytest.mark.skip(reason="test_zephyr_direct_advertising")
    def test_zephyr_direct_advertising_pairing_connect(self):
        print("Testing Zephyr Direct Advertising Pairing Connect")
        global bleState
        global operate_characteristic
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        time.sleep(2)
        # 3 option for pairing
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
            time.sleep(2)
            self.bleuartfeature.ble_smart_characteristic_write('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef2', '1234')
            if i == 0:
                action = 'timeout'
            elif i == 1:
                action = 'cancel'
            elif i == 2:
                action = 'accept'
            self.bleuartfeature.ble_smart_pairing_google_phone('Direct A', action)
            if i == 2:
                time.sleep(60)
                print('Pairing complete')


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

    #@pytest.mark.order(1)
    #@pytest.mark.test_id("Zephyr Direct Advertising Data Read/Write", '')
    @pytest.mark.skip(reason="test_zephyr_direct_advertising")
    def test_zephyr_direct_advertising_gatt_read_write(self):
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
        self.scanandconnect.verify_app_open()
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

    #@pytest.mark.test_id("Zephyr peripheral v1 rc5", '')
    @pytest.mark.skip(reason="test_lightblue_peripheral_scroll")
    def test_zephyr_peripheral_scroll_up(self):
        print('test_zephyr_peripheral_scroll_up')
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
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
        # self.bleuartfeature.lightblue_connect('Zephyr Peripheral Sample Long Name')
        time.sleep(10)
        self.bleuartfeature.lightblue_verify_ble_connected()
        time.sleep(3)

        self.bleuartfeature.lightblue_scroll_test1('up')
        time.sleep(5)

        self.bleuartfeature.lightblue_scroll_test1('up')
        time.sleep(5)

    #@pytest.mark.order(1)
    @pytest.mark.test_id("Zephyr peripheral application v1 rc5", '')
    #@pytest.mark.skip(reason="test_zephyr_peripheral_rc5")
    def test_zephyr_peripheral_application(self):
        print('test_zephyr_peripheral_application_v1_rc5')
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
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
        self.bleuartfeature.lightblue_verify_ble_services_characteristics()
        time.sleep(3)
        self.bleuartfeature.lightblue_scroll_gesture('0', scroll_element='Immediate Alert', direction='down')
        time.sleep(3)
        self.bleuartfeature.lightblue_scroll_gesture('0', scroll_element='Device Information', direction='down')
        time.sleep(3)
        self.bleuartfeature.lightblue_get_device_info_data()
        time.sleep(3)
        self.bleuartfeature.lightblue_ble_disconnect()

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










