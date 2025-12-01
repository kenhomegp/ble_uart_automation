import collections
from time import sleep

import pytest
import time

import concurrent.futures
import datetime

import serial

from collections import OrderedDict
from ...BaseWrappers.BaseDriver import BaseDriver
from ...CommonSupportLib.AppScanAndConnect import ScanningandConnection
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
from ...CommonSupportLib.StationData import stationData
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    PHONE_BT_ADDRESS_K, COM_PORT_K, BAUD_RATE_K
from ...CommonSupportLib.BLEUARTFeatureSupportiOS import BLEUARTFeatureSupportiOS

from ...MCP2200.MCP2200 import Mcp2200
from ...StationConfig import conf_file

sd = stationData()
MCU = Mcp2200()
BTN_CTRL_PIN = 0x04
LED_IND_PIN_G = 0x03
LED_IND_PIN_R = 0x05
dut_friendly_name = conf_file.dut_friendly_name
# phone_list = ["SamsungS10","Pixel3","VivoV11","GooglePixel5", "GooglePixel3A", "SamsungA51"]
phone_list = []


# phone_list = ["iPhone15", "SamsungA54"]
# phone_list = ["SamsungA54", "Pixel7"]
# phone_list = ["SamsungA54", "iPhone15", "Pixel7"]
# mobile_obj_list = []

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
    if len(sd.multilink_mobile_driver) == 1:
        # if "test_chimera_scan_stop_dut[10-5]" in test_func_name:
        if "test_chimera_scan_stop_dut_10_7" in test_func_name:
            print(f"Fixture {local_function_fixture.__name__} is being used by test: {test_func_name}")
            mobile_dic = sd.multilink_mobile_driver[0]
            phone_default = mobile_dic.get('phone')
            phone_default_driver = mobile_dic.get('driver')
            print("Phone: {0}".format(phone_default))

            if (isinstance(request.cls.bleuartfeature, BLEUARTFeatureSupport)):
                app_package = phone_default_driver.get_capability('appPackage')
            else:
                app_package = phone_default_driver.get_capability('bundleId')

            print("app_package: {0}".format(app_package))
            status = sd.mobile_driver.close_app(app_package)
            time.sleep(5)
            status = sd.mobile_driver.launch_app(app_package)
            # print("[Default mobile phone]App Launched")
            time.sleep(3)
            assert status, "Failed to launch application"

            if (isinstance(request.cls.bleuartfeature, BLEUARTFeatureSupport)):
                app_open = request.cls.bleuartfeature.verify_app_open()
                print("Launch Android MBD")
            else:
                app_open = request.cls.bleuartfeature.verify_ios_app_open()
                print("[Default mobile phone]Launch iOS MBD")
            assert app_open, "Failed to open MBD Application"

            time.sleep(1)
            request.cls.bleuartfeature.open_ble_uart_scanner()

            time.sleep(1)

    '''
    app_package = sd.mobile_driver.get_capability('appPackage')
    print(app_package)
    status = sd.mobile_driver.close_app(app_package)
    time.sleep(5)
    status = sd.mobile_driver.launch_app(app_package)
    print("[Default mobile phone]App Launched")
    time.sleep(2)
    assert status, "Failed to launch application"
    '''

    def function_finalizer():
        print("Local function finalizer")
        # print("Close App")

    request.addfinalizer(function_finalizer)

class TestMBDApp:

    #@pytest.mark.test_id("BLE_UART", 'MBDA')
    @pytest.mark.skip("BLE_UART", 'MBDA')
    def test_ble_uart_bidirectional_data_transfer(self):
        print("test_ble_uart_bidirectional_data_transfer")
        bleuartfeature_obj = []
        phone_default = ""
        phone_default_driver = None

        mobile_phone_list = sd.config.multilink_phone_config.split("/")
        print("mobile_phone_list = {}".format(len(mobile_phone_list)))

        if len(sd.multilink_mobile_driver) == 1:
            mobile_dic = sd.multilink_mobile_driver[0]
            phone_default = mobile_dic.get('phone')
            phone_default_driver = mobile_dic.get('driver')
            print("Phone default: {0}".format(phone_default))

            if (isinstance(self.bleuartfeature, BLEUARTFeatureSupport)):
                app_package = phone_default_driver.get_capability('appPackage')
            else:
                app_package = phone_default_driver.get_capability('bundleId')

            print("app_package: {0}".format(app_package))
            status = sd.mobile_driver.close_app(app_package)
            time.sleep(5)
            status = sd.mobile_driver.launch_app(app_package)
            # print("[Default mobile phone]App Launched")
            time.sleep(3)
            assert status, "Failed to launch application"

            if (isinstance(self.bleuartfeature, BLEUARTFeatureSupport)):
                app_open = self.bleuartfeature.verify_app_open()
                print("[Default mobile phone]Launch Android MBD")
            else:
                app_open = self.bleuartfeature.verify_ios_app_open()
                print("[Default mobile phone]Launch iOS MBD")
            assert app_open, "Failed to open MBD Application"

        # Create driver and launch MBD
        for phone in mobile_phone_list:
            if phone != phone_default:
                mobile_to_use = sd.config.mobile_data_config.get(phone)
                print("Appium Server Config data:")
                print(mobile_to_use)
                mobile_platform = mobile_to_use.get(PLATFORM_NAME_K)

                remote_appium = sd.remote_mac_server

                if mobile_platform == "Android":
                    '''
                    driver = BaseDriver(sd.config.appium_server_ip, str(4723 + len(sd.multilink_mobile_driver)),
                                        mobile_to_use.get(PHONE_UDID_K),
                                        mobile_to_use.get(PLATFORM_NAME_K),
                                        mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                        sd.config.app_package, sd.config.app_activity, fresh_env=True,
                                        remote_appium=remote_appium)
                    '''
                    driver = BaseDriver(sd.config.appium_server_ip, str(4723),
                                        mobile_to_use.get(PHONE_UDID_K),
                                        mobile_to_use.get(PLATFORM_NAME_K),
                                        mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                        sd.config.app_package, sd.config.app_activity, fresh_env=False,
                                        remote_appium=remote_appium)
                    bleuartfeature = BLEUARTFeatureSupport(driver)
                    bleuartfeature_obj.append(bleuartfeature)
                else:
                    driver = BaseDriver(sd.config.appium_server_ip, str(4723 + len(sd.multilink_mobile_driver)),
                                        mobile_to_use.get(PHONE_UDID_K),
                                        mobile_to_use.get(PLATFORM_NAME_K),
                                        mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                        sd.config.ios_mbda_app_package, remote_appium=remote_appium)
                    bleuartfeature = BLEUARTFeatureSupportiOS(driver)
                    bleuartfeature_obj.append(bleuartfeature)

                mobile_data_dic = {}
                dev_name = mobile_to_use.get(DEVICE_NAME_K)
                mobile_data_dic['driver'] = driver
                mobile_data_dic['phone'] = phone
                print("Save data")
                print(mobile_data_dic)
                sd.multilink_mobile_driver.append(mobile_data_dic)
                time.sleep(3)

                if mobile_platform == "Android":
                    app_package = driver.get_capability('appPackage')
                else:
                    app_package = driver.get_capability('bundleId')

                print("app_package: {0}".format(app_package))
                status = driver.close_app(app_package)
                time.sleep(5)
                status = driver.launch_app(app_package)
                time.sleep(3)
                assert status, "Failed to launch application"

                if mobile_platform == "Android":
                    app_open = bleuartfeature.verify_app_open()
                    print("Launch Android MBD")
                else:
                    app_open = bleuartfeature.verify_ios_app_open()
                    print("Launch iOS MBD")
                assert app_open, "Failed to open MBD Application"
            else:
                print("[Default] bleuartfeature")
                bleuartfeature_obj.append(self.bleuartfeature)
                time.sleep(3)

        print("Multilink WebDriver. len = {}".format(len(sd.multilink_mobile_driver)))
        print(sd.multilink_mobile_driver)
        print("bleuartfeature. len = {}".format(len(bleuartfeature_obj)))

        print("Scan for the DUT and connect. Mobile phone = {}".format(len(bleuartfeature_obj)))
        for i in range(len(bleuartfeature_obj)):
            # if i == 1:
            #    dut_name = "BLE_UART_CDDF"
            # else:
            #    dut_name = dut_friendly_name
            dut_name = dut_friendly_name

            # print("MCP2200 IO control. Press DUT button")
            # self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
            # time.sleep(5)

            bleuartfeature = bleuartfeature_obj[i]
            if (isinstance(bleuartfeature, BLEUARTFeatureSupport)):
                bleuartfeature.scan_and_connect_dut(dut_name)
                time.sleep(3)
                status = bleuartfeature.verify_dut_name_visibility(dut_name)
                print("DUT is connected with Android phone")
                assert status, "Unable to scan and connect to DUT"
            else:
                bleuartfeature.ios_scan_and_connect_dut(dut_name)
                time.sleep(3)
                status = bleuartfeature.ios_verify_dut_name_visibility(dut_name)
                print("DUT is connected with iPhone")
                assert status, "Unable to scan and connect to DUT"
            time.sleep(3)
            if (i + 1) != len(bleuartfeature_obj):
                print("MCP2200 IO control. Press DUT button")
                self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
                time.sleep(3)

        print("multilink_scan_and_connect. Done. ")

        for i in range(len(bleuartfeature_obj)):
            bleuartfeature = bleuartfeature_obj[i]

            bleuartfeature.verify_mode_uart()
            time.sleep(2)
            bleuartfeature.go_back()
            time.sleep(2)

            print("[UART mode] multilink test.test phone = {}".format(phone))
            bleuartfeature.initialize_com_port()
            time.sleep(2)

            #bleuartfeature.dut_uart_mode_data_transfer()
            receive_str = bleuartfeature.verify_mode_uart_birectional_data_transfer()
            print("Message ", receive_str)

            msg_tx = bleuartfeature.get_TX_throughput_value()
            print("UART Tx = {},{}".format(phone, msg_tx))
            msg_rx = bleuartfeature.get_RX_throughput_value()
            print("UART Rx = {},{}".format(phone, msg_rx))

    @pytest.mark.test_id("MacOS_MBD_UART_Mode_Test", 'MBDA')
    def test_mac_mbd_uart_mode(self):
        print("test_mac_mbd_uart_mode")
        print("Scan")
        self.bleuartfeature.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(3)
        print("UART.500k.txt")
        self.bleuartfeature.verify_mode_uart_ios()
        time.sleep(3)
        self.bleuartfeature.save_settings_ios()
        time.sleep(3)
        self.bleuartfeature.verify_raw_data_mode_ios()
        time.sleep(5)
        print("Start")
        self.bleuartfeature.verify_mode_uart_birectional_data_transfer_ios()
        #self.bleuartfeature.data_transfer_START_mobile_app_ios()
        #time.sleep(30)
        #self.bleuartfeature.loopback_mode_results_TX_ios()
        #serial = self.bleuartfeature.ComportSet('/dev/tty.usbmodem00098255751', 921600)
        #self.bleuartfeature.data_transfer_START_mobile_app_ios()
        #self.bleuartfeature.read_serial_port_data(serial, "test")

    #@pytest.mark.test_id("MULTILINK_LOOPBACK", 'MBDA')
    @pytest.mark.skip("MULTILINK_LOOPBACK", 'MBDA')
    def test_ble_uart_multilink_loopback(self):
        print("{0}Test to verify Chimera BLE UART Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan and Connect with 6 Android phones {0}".format('=' * 20))

        bleuartfeature_obj = []
        phone_default = ""
        phone_default_driver = None

        platform = sd.mobile_platform

        test_run = True

        #mobile_phone_list = sd.config.multilink_phone_config.split("/")
        mobile_phone_list = sd.config.multilink_phone_list
        print("mobile_phone_list = {}".format(len(mobile_phone_list)))

        if len(sd.multilink_mobile_driver) == 1:
            mobile_dic = sd.multilink_mobile_driver[0]
            phone_default = mobile_dic.get('phone')
            phone_default_driver = mobile_dic.get('driver')
            print("Phone default: {0}".format(phone_default))

            '''
            if (isinstance(self.bleuartfeature, BLEUARTFeatureSupport)):
                app_package = phone_default_driver.get_capability('appPackage')
            else:
                app_package = phone_default_driver.get_capability('bundleId')

            print("app_package: {0}".format(app_package))
            status = sd.mobile_driver.close_app(app_package)
            time.sleep(5)
            status = sd.mobile_driver.launch_app(app_package)
            time.sleep(3)
            assert status, "Failed to launch application"

            if (isinstance(self.bleuartfeature, BLEUARTFeatureSupport)):
                app_open = self.scanandconnect.verify_app_open()
                print("[Default mobile phone]Launch Android MBD")
            else:
                app_open = self.scanandconnect.verify_ios_app_open()
                print("[Default mobile phone]Launch iOS MBD")
            assert app_open, "Failed to open MBD Application"
            '''

        # Create driver and launch MBD
        for phone in mobile_phone_list:
            if phone != phone_default:
                mobile_to_use = sd.config.mobile_data_config.get(phone)
                print("Appium Server Config data:")
                print(mobile_to_use)
                mobile_platform = mobile_to_use.get(PLATFORM_NAME_K)

                remote_appium = sd.remote_mac_server

                if mobile_platform == "Android":
                    '''
                    driver = BaseDriver(sd.config.appium_server_ip, str(4723 + len(sd.multilink_mobile_driver)),
                                        mobile_to_use.get(PHONE_UDID_K),
                                        mobile_to_use.get(PLATFORM_NAME_K),
                                        mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                        sd.config.app_package, sd.config.app_activity, fresh_env=True,
                                        remote_appium=remote_appium)
                    '''
                    driver = BaseDriver(sd.config.appium_server_ip, str(4723),
                                        mobile_to_use.get(PHONE_UDID_K),
                                        mobile_to_use.get(PLATFORM_NAME_K),
                                        mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                        sd.config.app_package, sd.config.app_activity, fresh_env=False,
                                        remote_appium=remote_appium)
                    bleuartfeature = BLEUARTFeatureSupport(driver)
                    bleuartfeature_obj.append(bleuartfeature)
                else:
                    driver = BaseDriver(sd.config.appium_server_ip, str(4723 + len(sd.multilink_mobile_driver)),
                                        mobile_to_use.get(PHONE_UDID_K),
                                        mobile_to_use.get(PLATFORM_NAME_K),
                                        mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                        sd.config.ios_mbda_app_package, remote_appium=remote_appium)
                    bleuartfeature = BLEUARTFeatureSupportiOS(driver)
                    bleuartfeature_obj.append(bleuartfeature)

                mobile_data_dic = {}
                dev_name = mobile_to_use.get(DEVICE_NAME_K)
                mobile_data_dic['driver'] = driver
                mobile_data_dic['phone'] = phone
                print("Save data")
                print(mobile_data_dic)
                sd.multilink_mobile_driver.append(mobile_data_dic)
                time.sleep(3)

                if mobile_platform == "Android":
                    app_package = driver.get_capability('appPackage')
                else:
                    app_package = driver.get_capability('bundleId')

                print("app_package: {0}".format(app_package))
                status = driver.close_app(app_package)
                time.sleep(5)
                status = driver.launch_app(app_package)
                time.sleep(3)
                assert status, "Failed to launch application"

                if mobile_platform == "Android":
                    app_open = bleuartfeature.verify_app_open()
                    print("Launch Android MBD")
                else:
                    app_open = bleuartfeature.verify_ios_app_open()
                    print("Launch iOS MBD")
                assert app_open, "Failed to open MBD Application"
            else:
                print("[Default] bleuartfeature")
                bleuartfeature_obj.append(self.bleuartfeature)
                time.sleep(3)

        print("Multilink WebDriver. len = {}".format(len(sd.multilink_mobile_driver)))
        print(sd.multilink_mobile_driver)
        print("bleuartfeature. len = {}".format(len(bleuartfeature_obj)))

        print("Scan for the DUT and connect. Mobile phone = {}".format(len(bleuartfeature_obj)))
        for i in range(len(bleuartfeature_obj)):
            # if i == 1:
            #    dut_name = "BLE_UART_CDDF"
            # else:
            #    dut_name = dut_friendly_name
            dut_name = dut_friendly_name

            # print("MCP2200 IO control. Press DUT button")
            # self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
            # time.sleep(5)

            bleuartfeature = bleuartfeature_obj[i]
            if (isinstance(bleuartfeature, BLEUARTFeatureSupport)):
                bleuartfeature.scan_and_connect_dut(dut_name)
                time.sleep(3)
                status = bleuartfeature.verify_dut_name_visibility(dut_name)
                print("DUT is connected with Android phone")
                assert status, "Unable to scan and connect to DUT"
            else:
                bleuartfeature.ios_scan_and_connect_dut(dut_name)
                if sd.mobile_platform != "mac":
                    time.sleep(3)
                    status = bleuartfeature.ios_verify_dut_name_visibility(dut_name)
                    print("DUT is connected with iPhone")
                    assert status, "Unable to scan and connect to DUT"
            time.sleep(3)
            if (i + 1) != len(bleuartfeature_obj):
                #print("MCP2200 IO control. Press DUT button")
                if sd.mobile_platform != "mac":
                    print("MCP2200 IO control. Press DUT button")
                    self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
                    time.sleep(3)

        print("multilink_scan_and_connect. Done. ")

        for i in range(len(bleuartfeature_obj)):
            bleuartfeature = bleuartfeature_obj[i]
            if (isinstance(bleuartfeature, BLEUARTFeatureSupport)):
                if i == 0:
                    # bleuartfeature.verify_mode_loopback(multilink=True, target_phone=True)
                    bleuartfeature.verify_mode_loopback(multilink=True)
                else:
                    bleuartfeature.verify_mode_loopback(multilink=True)
                bleuartfeature.go_back()
                time.sleep(5)
                mode_set_trp = bleuartfeature.confirm_loopback_mode()
                assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
                trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
                print(trp_result)
                time.sleep(5)
            else:
                #bleuartfeature.verify_mode_loopback_ios()
                bleuartfeature.verify_mode_uart_ios()
                time.sleep(5)
                bleuartfeature.save_settings_ios()
                if sd.mobile_platform != "mac":
                    mode_set_trp = bleuartfeature.confirm_loopback_mode_ios()
                    assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
                    trp_result = "Loopback Mode TRP Mode Data Transfer 500K\n"
                    print(trp_result)
                    time.sleep(5)

        print("multilink_Loopback_mode_trp_500k. Done. ")

        def ble_throughput_test(bleuartfeature_executor, phone):
            # print("BLEUART multilink test.target = {}".format(phone_default))
            print("BLEUART multilink test.test phone = {}".format(phone))

            j = 2
            for i in range(j):
                if sd.mobile_platform != "mac":
                    button_state = bleuartfeature_executor.get_start_button()
                    print("button state = {}".format(button_state))

                if (isinstance(bleuartfeature_executor, BLEUARTFeatureSupport)):
                    bleuartfeature_executor.multilink_data_transfer_START()
                else:
                    bleuartfeature_executor.data_transfer_START_mobile_app_ios()

                if sd.mobile_platform != "mac":
                    time.sleep(4)
                # delay = 0
                if (isinstance(bleuartfeature_executor, BLEUARTFeatureSupport)):
                    print("Android phone : {}, iterative testing : {}".format(phone, i))
                else:
                    print("iPhone : {}, iterative testing : {}".format(phone, i))

                if sd.mobile_platform == "mac":
                    print("Data transmission.Wait 30 seconds...")
                    time.sleep(30)
                    bleuartfeature_executor.loopback_mode_results_TX_ios()
                    time.sleep(1)
                    bleuartfeature_executor.loopback_mode_results_RX_ios()
                else:
                    msg_tx = bleuartfeature_executor.get_TX_throughput_value()
                    print("Test phone = {},{}".format(phone, msg_tx))
                    msg_rx = bleuartfeature_executor.get_RX_throughput_value()
                    print("Test phone = {},{}".format(phone, msg_rx))
                    delay = (500 / int(msg_rx)) - 3
                    print("Test phone = {},Data Transmission time = {}".format(phone, delay))

                    while bleuartfeature_executor.get_start_button() != "START":
                        time.sleep(1)
                        print("Data transmission.")

                '''
                timeoutError = ""

                if (isinstance(bleuartfeature_executor, BLEUARTFeatureSupport)):
                    status, msg = bleuartfeature_executor.loopback_mode_results_TX()
                    assert status, msg
                    status, msg = bleuartfeature_executor.loopback_mode_results_RX()
                    assert status, msg
                    # print("Test phone = {}".format(phone))
                    if msg == "TRANSACTION Timeout error":
                        timeoutError = msg
                        print("Test phone = {}.TRANSACTION Timeout error".format(phone))
                    else:
                        print("Test phone = {},{}".format(phone, msg))
                else:
                    status, msg = bleuartfeature_executor.loopback_mode_results_TX_ios()
                    assert status, msg
                    status, msg = bleuartfeature_executor.loopback_mode_results_RX_ios()
                    assert status, msg
                    print("Test phone = {}".format(phone))

                if timeoutError == "TRANSACTION Timeout error":
                    if (isinstance(bleuartfeature_executor, BLEUARTFeatureSupport)):
                        print("Timeout Error. Stop")
                        bleuartfeature_executor.data_transfer_STOP()
                        time.sleep(2)
                        print("Timeout Error. Start")
                        bleuartfeature_executor.multilink_data_transfer_START()
                else:
                    time.sleep(2)
                '''

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(len(bleuartfeature_obj)):
                bleuartfeature = bleuartfeature_obj[i]
                phone_dic = sd.multilink_mobile_driver[i]
                phone = phone_dic['phone']
                app = executor.submit(ble_throughput_test, bleuartfeature, phone)
                futures.append(app)
            # futures = [executor.submit(ble_throughput_test, bleuart_executor) for bleuart_executor in bleuartfeature_obj]
            print("\nfutures: {}".format(futures))
            concurrent.futures.wait(futures)

        print("Loopback_mode_trp_500k. Data Transfer Done. Display throughput value")
        time.sleep(5)

