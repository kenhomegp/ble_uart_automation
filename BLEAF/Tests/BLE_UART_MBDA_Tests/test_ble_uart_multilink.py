import collections
import pytest
import time

import concurrent.futures

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
#phone_list = ["SamsungS10","Pixel3","VivoV11","GooglePixel5", "GooglePixel3A", "SamsungA51"]
phone_list = []
#phone_list = ["iPhone15", "SamsungA54"]
#phone_list = ["SamsungA54", "Pixel7"]
#phone_list = ["SamsungA54", "iPhone15", "Pixel7"]
#mobile_obj_list = []

@pytest.fixture(scope="class", autouse=True)
def define_class_attributes(request, default_class_fixture):
    print("this is local specific class fixture")

    #if (isinstance(request.cls.bleuartfeature, BLEUARTFeatureSupport)):
    #    print("Android: Init MCP2200")
    #    request.cls.bleuartfeature.initialize_com_port()

    def class_finalizer():
        print("Local Class finalizer")
    request.addfinalizer(class_finalizer)

@pytest.fixture(scope="function", autouse=True)
def local_function_fixture(request):
    print("Local function fixture")
    #print("Launch MBD Application")

    test_func_name = request.node.name
    print(f"Fixture {local_function_fixture.__name__} is being used by test: {test_func_name}")
    if len(sd.multilink_mobile_driver) == 1:
        if(test_func_name == "test_chimera_scan_stop_dut"):
            #print(request.cls.bleuartfeature)
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
        #print("Close App")
    request.addfinalizer(function_finalizer)

class TestChimeraConnectBLEUartMultilink:
    #@pytest.mark.test_id("MULTILINK_SCAN_STOP_DUT", 'MBDA')
    #def test_chimera_scan_stop_dut(self, local_function_fixture):
    @pytest.mark.parametrize("test_iteration, scan_time", [(15, 10), (15, 9)])
    def test_chimera_scan_stop_dut(self, test_iteration, scan_time):
        #test_iteration = 15
        #scan_time = 6
        print("stress_test_scan_dut.{}.{}".format(test_iteration, scan_time))

        for i in range(test_iteration):
            print("ble_scan_stop_stress. iteration = {}".format(i))
            self.bleuartfeature.stress_test_scan_dut(dut_friendly_name, scan_time)
            print("duts:{} found".format(dut_friendly_name))

        #phone_default = ""
        '''
        if len(sd.multilink_mobile_driver) == 1:
            mobile_dic = sd.multilink_mobile_driver[0]
            phone_default = mobile_dic.get('phone')
            phone_default_driver = mobile_dic.get('driver')
            print("Phone default: {0}".format(phone_default))
            print(self.bleuartfeature)

            if (isinstance(self.bleuartfeature, BLEUARTFeatureSupport)):
                app_package = phone_default_driver.get_capability('appPackage')
            else:
                app_package = phone_default_driver.get_capability('bundleId')

            print("app_package: {0}".format(app_package))
            status = sd.mobile_driver.close_app(app_package)
            time.sleep(5)
            status = sd.mobile_driver.launch_app(app_package)
            #print("[Default mobile phone]App Launched")
            time.sleep(3)
            assert status, "Failed to launch application"

            if (isinstance(self.bleuartfeature, BLEUARTFeatureSupport)):
                app_open = self.bleuartfeature.verify_app_open()
                print("[Default mobile phone]Launch Android MBD")
            else:
                app_open = self.bleuartfeature.verify_ios_app_open()
                print("[Default mobile phone]Launch iOS MBD")
            assert app_open, "Failed to open MBD Application"

            time.sleep(1)
            self.bleuartfeature.open_ble_uart_scanner()

            time.sleep(1)
            for i in range(test_iteration):
                print("ble_scan_stop_stress. iteration = {}".format(i))
                self.bleuartfeature.stress_test_scan_dut(dut_friendly_name, scan_time)
                print("duts:{} found".format(dut_friendly_name))
        '''

    @pytest.mark.skip("MULTILINK_SCAN_AND_CONNECT", 'MBDA')
    #@pytest.mark.test_id("MULTILINK_SCAN_AND_CONNECT", 'MBDA')
    def test_chimera_connect_ble_uart_multilink_scan_and_connect(self):
        print("{0}Test to verify Chimera BLE UART Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan and Connect with 6 Android phones {0}".format('=' * 20))

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
            #print("[Default mobile phone]App Launched")
            time.sleep(3)
            assert status, "Failed to launch application"

            if (isinstance(self.bleuartfeature, BLEUARTFeatureSupport)):
                app_open = self.bleuartfeature.verify_app_open()
                print("[Default mobile phone]Launch Android MBD")
            else:
                app_open = self.bleuartfeature.verify_ios_app_open()
                print("[Default mobile phone]Launch iOS MBD")
            assert app_open, "Failed to open MBD Application"

        #Create driver and launch MBD
        for phone in mobile_phone_list:
            if phone != phone_default:
                mobile_to_use = sd.config.mobile_data_config.get(phone)
                print("Appium Server Config data:")
                print(mobile_to_use)
                mobile_platform = mobile_to_use.get(PLATFORM_NAME_K)

                remote_appium = sd.remote_mac_server

                if mobile_platform == "Android":
                    driver = BaseDriver(sd.config.appium_server_ip, str(4723 + len(sd.multilink_mobile_driver)),
                                        mobile_to_use.get(PHONE_UDID_K),
                                        mobile_to_use.get(PLATFORM_NAME_K),
                                        mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                        sd.config.app_package, sd.config.app_activity, fresh_env=True,
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
            #if i == 1:
            #    dut_name = "BLE_UART_CDDF"
            #else:
            #    dut_name = dut_friendly_name
            dut_name = dut_friendly_name

            #print("MCP2200 IO control. Press DUT button")
            #self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
            #time.sleep(5)

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
            if(i+1) != len(bleuartfeature_obj):
                print("MCP2200 IO control. Press DUT button")
                self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
                time.sleep(3)

        print("multilink_scan_and_connect. Done. ")

        for i in range(len(bleuartfeature_obj)):
            bleuartfeature = bleuartfeature_obj[i]
            if (isinstance(bleuartfeature, BLEUARTFeatureSupport)):
                if i == 0:
                    #bleuartfeature.verify_mode_loopback(multilink=True, target_phone=True)
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
                bleuartfeature.verify_mode_loopback_ios()
                time.sleep(5)
                bleuartfeature.save_settings_ios()
                mode_set_trp = bleuartfeature.confirm_loopback_mode_ios()
                assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
                trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
                print(trp_result)
                time.sleep(5)
        print("multilink_Loopback_mode_trp_500k. Done. ")

        def ble_throughput_test(bleuartfeature_executor, phone):
            #print("BLEUART multilink test.target = {}".format(phone_default))
            print("BLEUART multilink test.test phone = {}".format(phone))

            j = 10
            for i in range(j):
                if (isinstance(bleuartfeature_executor, BLEUARTFeatureSupport)):
                    bleuartfeature_executor.multilink_data_transfer_START()
                else:
                    bleuartfeature_executor.data_transfer_START_mobile_app_ios()

                time.sleep(4)
                #delay = 0
                if (isinstance(bleuartfeature_executor, BLEUARTFeatureSupport)):
                    print("Android phone : {}, iterative testing : {}".format(phone, i))
                else:
                    print("iPhone : {}, iterative testing : {}".format(phone, i))

                msg_tx = bleuartfeature_executor.get_TX_throughput_value()
                print(msg_tx)
                msg_rx = bleuartfeature_executor.get_RX_throughput_value()
                print(msg_rx)
                delay = (500 / int(msg_rx)) - 3
                print("Data Transmission time = {}".format(delay))

                time.sleep(delay)
                timeoutError = ""

                if (isinstance(bleuartfeature_executor, BLEUARTFeatureSupport)):
                    status, msg = bleuartfeature_executor.loopback_mode_results_TX()
                    assert status, msg
                    status, msg = bleuartfeature_executor.loopback_mode_results_RX()
                    assert status, msg
                    print("Test phone = {}".format(phone))
                    if msg == "TRANSACTION Timeout error":
                        timeoutError = msg
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

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(len(bleuartfeature_obj)):
                bleuartfeature = bleuartfeature_obj[i]
                phone_dic = sd.multilink_mobile_driver[i]
                phone = phone_dic['phone']
                app = executor.submit(ble_throughput_test, bleuartfeature, phone)
                futures.append(app)
            #futures = [executor.submit(ble_throughput_test, bleuart_executor) for bleuart_executor in bleuartfeature_obj]
            print("futures: {}".format(futures))
            concurrent.futures.wait(futures)

        print("Loopback_mode_trp_500k. Data Transfer Done. Display throughput value")
        time.sleep(5)

        '''
        if len(sd.multilink_mobile_driver) == 1:
            if delay != 0:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(ble_throughput_test, bleuartfeature_obj[0], delay)
                    concurrent.futures.wait([future])
                
                time.sleep(delay)
                bleuartfeature = bleuartfeature_obj[0]
                if (isinstance(bleuartfeature, BLEUARTFeatureSupport)):
                    status, msg = bleuartfeature.loopback_mode_results_TX()
                    assert status, msg
                    status, msg = bleuartfeature.loopback_mode_results_RX()
                    assert status, msg
                else:
                    status, msg = bleuartfeature.loopback_mode_results_TX_ios()
                    assert status, msg
                    status, msg = bleuartfeature.loopback_mode_results_RX_ios()
                    assert status, msg
            else:
                time.sleep(25)
            print("Loopback_mode_trp_500k. Data Transfer Done. Display throughput value")
            time.sleep(5)
        else:
            time.sleep(200)
            print("multilink_Loopback_mode_trp_500k. Data Transfer Done. ")
        '''

        #sd.second_mobile_driver.close_app('com.microchip.bluetooth.data')
        #time.sleep(20)
        #self.bleuartfeature.close_mbd_app()
        #self.test_result = True

    @pytest.mark.skip("MULTILINK_CONNECT_AND_DISCONNECT", 'MBDA')
    def test_chimera_connect_ble_uart_multilink_scan_connect_disconnect(self):
        print("{0}Test to verify Chimera Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan, Connect & Disconnect with 6 Android phones {0}".format('=' * 20))
        print("{0}Test to verify Chimera Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Loopback Data Transfer with 6 Android phones {0}".format('=' * 20))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect2.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect2.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect2.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect3.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect3.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect3.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect4.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect4.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect4.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect5.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect5.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect5.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        # Disconnect all phones
        print("Disconnect All phones")
        bleuartfeature.go_back()
        bleuartfeature1.go_back()
        bleuartfeature2.go_back()
        bleuartfeature3.go_back()
        bleuartfeature4.go_back()
        bleuartfeature5.go_back()
        time.sleep(10)
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("MULTILINK_LOOPBACK_MODE_DATA_TRANSFER_TRP", 'MBDA')
    def test_chimera_connect_ble_uart_multilink_loopback_data_transfer_trp(self):
        print("{0}Test to verify Chimera Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Loopback Data Transfer with 6 Android phones - TRP {0}".format('=' * 20))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect2.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect2.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect2.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect3.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect3.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect3.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect4.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect4.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect4.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect5.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect5.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect5.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        bleuartfeature.verify_mode_loopback()
        bleuartfeature.go_back()
        time.sleep(5)
        mode_set_trp = bleuartfeature.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        bleuartfeature1.verify_mode_loopback()
        bleuartfeature1.go_back()
        time.sleep(5)
        mode_set_trp = bleuartfeature1.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        bleuartfeature2.verify_mode_loopback()
        bleuartfeature2.go_back()
        time.sleep(5)
        mode_set_trp = bleuartfeature2.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        bleuartfeature3.verify_mode_loopback()
        bleuartfeature3.go_back()
        time.sleep(5)
        mode_set_trp = bleuartfeature3.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        bleuartfeature4.verify_mode_loopback()
        bleuartfeature4.go_back()
        time.sleep(5)
        mode_set_trp = bleuartfeature4.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        bleuartfeature5.verify_mode_loopback()
        bleuartfeature5.go_back()
        time.sleep(5)
        mode_set_trp = bleuartfeature5.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        # Start Data Transfer in all phones
        bleuartfeature.multilink_data_transfer_START()
        bleuartfeature1.multilink_data_transfer_START()
        bleuartfeature2.multilink_data_transfer_START()
        bleuartfeature3.multilink_data_transfer_START()
        bleuartfeature4.multilink_data_transfer_START()
        bleuartfeature5.multilink_data_transfer_START()
        time.sleep(200)
        status, msg = bleuartfeature.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature1.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature1.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature2.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature2.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature3.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature3.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature4.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature4.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature5.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature5.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(20)
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("MULTILINK_LOOPBACK_MODE_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_chimera_connect_ble_uart_multilink_loopback_data_transfer_trcbp(self):
        print("{0}Test to verify Chimera Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Loopback Data Transfer with 6 Android phones - TRCBP {0}".format('=' * 20))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect2.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect2.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect2.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect3.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect3.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect3.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect4.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect4.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect4.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect5.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        scanandconnect5.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect5.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        bleuartfeature.verify_mode_loopback()
        bleuartfeature.switch_to_trcbp()
        bleuartfeature.go_back()
        time.sleep(5)
        mode_set_trcbp = bleuartfeature.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        bleuartfeature1.verify_mode_loopback()
        bleuartfeature1.switch_to_trcbp()
        bleuartfeature1.go_back()
        time.sleep(5)
        mode_set_trcbp = bleuartfeature1.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        bleuartfeature2.verify_mode_loopback()
        bleuartfeature2.switch_to_trcbp()
        bleuartfeature2.go_back()
        time.sleep(5)
        mode_set_trcbp = bleuartfeature2.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        bleuartfeature3.verify_mode_loopback()
        bleuartfeature3.switch_to_trcbp()
        bleuartfeature3.go_back()
        time.sleep(5)
        mode_set_trcbp = bleuartfeature3.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        bleuartfeature4.verify_mode_loopback()
        bleuartfeature4.switch_to_trcbp()
        bleuartfeature4.go_back()
        time.sleep(5)
        mode_set_trcbp = bleuartfeature4.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        bleuartfeature5.verify_mode_loopback()
        bleuartfeature5.switch_to_trcbp()
        bleuartfeature5.go_back()
        time.sleep(5)
        mode_set_trcbp = bleuartfeature5.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        # Start Data Transfer in all phones
        bleuartfeature.multilink_data_transfer_START()
        bleuartfeature1.multilink_data_transfer_START()
        bleuartfeature2.multilink_data_transfer_START()
        bleuartfeature3.multilink_data_transfer_START()
        bleuartfeature4.multilink_data_transfer_START()
        bleuartfeature5.multilink_data_transfer_START()
        time.sleep(200)
        status, msg = bleuartfeature.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature1.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature1.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature2.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature2.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature3.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature3.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature4.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature4.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature5.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = bleuartfeature5.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(20)
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("MULTILINK_CHIMERA_VS_6PHONES_OVERNIGHT_CONNECTION_STABILITY", 'MBDA')
    def test_chimera_connect_ble_uart_multilink_overnight_connection_stability(self):
        print("{0}Test to verify Chimera BLE UART Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan and Connect & Overnight Connection Stability with 6 Android phones {0}".format(
            '=' * 10))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        driver.launch_app()
        print("App launced++++++++++++++++++++")
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect2.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect2.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect2.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect3.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect3.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect3.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect4.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect4.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect4.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        self.iocontrolledstatus.IOCtrl(MCU, BTN_CTRL_PIN, 0.2)
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify Chimera device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect5.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(15)
        print("Scan for the DUT and connect")
        scanandconnect5.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect5.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("Start the long hour tests")
        duration_conn_test = 60 * 5 # Seconds
        t_end = time.time() + duration_conn_test
        while (True):
            print("Check for connection for long hour for all 6 links \n")
            status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
            print("Status of the Phone1 connection", status)
            status1 = self.scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
            print("Status of the Phone2 connection", status1)
            status2 = self.scanandconnect2.verify_dut_name_visibility(dut_friendly_name)
            print("Status of the Phone3 connection", status2)
            status3 = self.scanandconnect3.verify_dut_name_visibility(dut_friendly_name)
            print("Status of the Phone4 connection", status3)
            status4 = self.scanandconnect4.verify_dut_name_visibility(dut_friendly_name)
            print("Status of the Phone5 connection", status4)
            status5 = self.scanandconnect5.verify_dut_name_visibility(dut_friendly_name)
            print("Status of the Phone6 connection", status5)
            assert status, "Connection test failed in Phone 1"
            assert status1, "Connection test failed in Phone 2"
            assert status2, "Connection test failed in Phone 3"
            assert status3, "Connection test failed in Phone 4"
            assert status4, "Connection test failed in Phone 5"
            assert status5, "Connection test failed in Phone 6"
            if (time.time() > t_end):
                print("Completed long hour connection test")
                msg = "Connection test verified for time {} seconds".format(duration_conn_test)
                print(msg)
                self.note += msg
                break
        time.sleep(10)
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        self.test_result = True