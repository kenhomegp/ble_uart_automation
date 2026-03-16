import pytest
import time
from datetime import datetime
import sys

from ...CommonSupportLib.BleUARTPairingFeatureSupport import BLEUartPairingSupport
from ...CommonSupportLib.BLEUARTFeatureSupportiOS import BLEUARTFeatureSupportiOS
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
from ...CommonSupportLib.AppScanAndConnect import ScanningandConnection
from ...CommonSupportLib.IOControl_LEDStatus import IOControlLEDStatus
from ...CommonSupportLib.StationData import stationData
#from ...CommonSupportLib.SoderaSupport import SoderaSupport
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    PHONE_BT_ADDRESS_K, COM_PORT_K, BAUD_RATE_K, DUT_ADD_K
from ...CommonSupportLib.RNBDPairingandLightBlueFeatureSupport import RNBDvsPhoneFeatureSupport
from ...CommonSupportLib.Serial_Implementaiton import SerialSuppport

from ...BaseWrappers.SSHSupport import ShellHandler

from ...BaseWrappers.NewBaseDriver import NewBaseDriver

from ...CommonSupportLib.RemoteMCP2200FeatureSupport import WebSocketManager

sd = stationData()

@pytest.fixture(scope="class", autouse=True)
def default_class_fixture(request):
    print("BLE_UART_MBDA_Tests\conftest]")
    multilink = request.config.getoption('--multilink')
    if multilink:
        print("multilink option = enabled")

    #if multilink is not None and multilink == 'no':
    if not multilink:
        print(f"sd.platform = {sd.platform}")
        mobile_to_use = sd.config.mobile_data_config.get(sd.platform)
        assert mobile_to_use is not None, "Mobile phone config error."
        print("Appium Server Config data:")
        print(mobile_to_use)

    #print(sd.config.multilink_phone_config)
    #phone_list = sd.config.multilink_phone_config.split("/")
    phone_list = sd.config.multilink_phone_list
    phones_len = len(phone_list)
    print("Multilink phone . len = {}".format(phones_len))

    #print(sd.config.app_package)
    #print(sd.config.ios_mbda_app_package)
    #print(sd.config.appium_server_ip)
    # Multiple drivers for mobiles

    app = request.config.getoption('--mobile_app')
    if app is not None:
        print('mobile app option = {}'.format(app))
        if app == 'lightblue':
            # ios_perioheral_hid
            ios_test_app_package = sd.config.ios_lightblue_app_package
        elif app == 'mbd':
            ios_test_app_package = sd.config.ios_mbda_app_package
        elif app == 'zephyr_hid':
            print('Zephyr HID test')
    else:
        print('mobile app option: none')
        ios_test_app_package = sd.config.ios_mbda_app_package

    remote_appium = sd.config.use_remote_appium

    #if multilink is not None and multilink != 'no':
    if multilink:
        platform = 'multilink'
        sd.mobile_platform = 'multilink'
        print(f'multilink = {multilink}')
    else:
        platform = mobile_to_use.get(PLATFORM_NAME_K)
        sd.mobile_platform = platform

    if platform == "mac":
        print("Platform: Mac ")
        use_remote_appium = False
        if remote_appium:
            appium_ip = sd.config.remote_appium_server_ip
            use_remote_appium = True
        else:
            appium_ip = sd.config.appium_server_ip

        driver = NewBaseDriver(appium_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            ios_test_app_package, sd.config.app_activity, remote_appium=use_remote_appium)
    elif platform == 'iOS':
        #sd.config.app_package = sd.config.ios_mbda_app_package
        #print("platform = iOS. app package={}".format(sd.config.ios_mbda_app_package))
        print("platform = iOS. app package={}".format(ios_test_app_package))
        if remote_appium:
            driver = NewBaseDriver(sd.config.remote_appium_server_ip, sd.config.remote_appium_server_port,
                                mobile_to_use.get(PHONE_UDID_K),
                                mobile_to_use.get(PLATFORM_NAME_K),
                                mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                ios_test_app_package, sd.config.app_activity, remote_appium=sd.config.use_remote_appium)
        else:
            driver = NewBaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                                mobile_to_use.get(PHONE_UDID_K),
                                mobile_to_use.get(PLATFORM_NAME_K),
                                mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                ios_test_app_package, sd.config.app_activity)
    elif platform == 'Android':
        if app == 'zephyr_hid':
            app_package = 'com.microchip.zephyrtest'
            app_activity = 'com.microchip.zephyrtest.MainActivity'
        elif app == 'setting':
            app_package = 'com.android.settings'
            app_activity = 'com.android.settings.Settings'
        elif app == 'lightblue':
            app_package = 'com.punchthrough.lightblueexplorer'
            app_activity = 'com.punchthrough.lightblueexplorer.MainActivity'
        else:
            app_package = sd.config.app_package
            app_activity = sd.config.app_activity

        if remote_appium:
            print("platform = Android. Use Remote appium")
            driver = NewBaseDriver(sd.config.remote_appium_server_ip, sd.config.remote_appium_server_port,
                                   mobile_to_use.get(PHONE_UDID_K),
                                   mobile_to_use.get(PLATFORM_NAME_K),
                                   mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                   app_package, app_activity,
                                   remote_appium=sd.config.use_remote_appium)
            #driver = NewBaseDriver(sd.config.remote_appium_server_ip, sd.config.remote_appium_server_port,
            #                    mobile_to_use.get(PHONE_UDID_K),
            #                    mobile_to_use.get(PLATFORM_NAME_K),
            #                    mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
            #                    sd.config.app_package, sd.config.app_activity, remote_appium=sd.config.use_remote_appium)
        else:
            print("platform = Android MBD:{}, {}".format(sd.config.app_package, sd.config.app_activity))
            driver = NewBaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                                mobile_to_use.get(PHONE_UDID_K),
                                mobile_to_use.get(PLATFORM_NAME_K),
                                mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                sd.config.app_package, sd.config.app_activity)
    else:
        print('conftest.py: platform: {}'.format(platform))

    #if multilink is None:
    #if multilink == 'no':
    if not multilink:
        mobile_data_dic = {}
        dev_name = mobile_to_use.get(DEVICE_NAME_K)
        mobile_data_dic['driver'] = driver
        mobile_data_dic['phone'] = dev_name
        sd.multilink_mobile_driver.append(mobile_data_dic)
        sd.mobile_driver = driver

        request.cls.scanandconnect = ScanningandConnection()
        if platform == 'iOS' or platform == 'mac':
            request.cls.bleuartfeature = BLEUARTFeatureSupportiOS()
        elif platform == 'Android':
            request.cls.bleuartfeature = RNBDvsPhoneFeatureSupport()

        request.cls.iocontrolledstatus = IOControlLEDStatus()
        request.cls.bleuartpairingfeature = BLEUartPairingSupport()
        request.cls.serialdriver = SerialSuppport()
        time.sleep(3)
    else:
        request.cls.iocontrolledstatus = IOControlLEDStatus()
        request.cls.serialdriver = SerialSuppport()
        time.sleep(1)

    def class_finalizer():
        #sd.mobile_driver.kill_appium_server()
        #if sd.mobile_driver.platform == "Windows":

        if(len(sd.multilink_mobile_driver) >= 1):
            print("Close app and kill appium server ")

            #android_udid_list = []
            for phone_info_dic in sd.multilink_mobile_driver:
                phone_name = phone_info_dic['phone']
                print("phone_name = {}.Close test app".format(phone_name))
                mobile_driver = phone_info_dic['driver']
                iDevice = False
                if "iphone" in phone_name.lower():
                    iDevice = True
                elif "mymac" in phone_name.lower():
                    iDevice = True
                elif "ipad" in phone_name.lower():
                    iDevice = True

                #if "iphone" in phone_name.lower() or "mymac" in phone_name.lower():
                if iDevice:
                    app_package = mobile_driver.get_capability('bundleId')
                else:
                    app_package = mobile_driver.get_capability('appPackage')
                time.sleep(3)
                #pid = mobile_driver.get_android_app_pid('R5CW321G69K')

                #if "iphone" in phone_name.lower() or "mymac" in phone_name.lower():
                #if iDevice:
                #    print("[iPhone]Get adb log. not supported")
                #else:
                #    mobile_info = sd.config.mobile_data_config.get(phone_name)
                #    udid = mobile_info.get(PHONE_UDID_K)
                #    android_udid_list.append(udid)

                #status = mobile_driver.close_app(app_package)
                #time.sleep(3)
                #assert status, "Failed to close application"

            for phone_info_dic in sd.multilink_mobile_driver:
                #phone_name = phone_info_dic['phone']
                #print("phone_name = {}.Close MBD app".format(phone_name))
                mobile_driver = phone_info_dic['driver']
                #if not sd.remote_mac_server:
                print(mobile_driver)
                if not remote_appium:
                    if sys.platform.startswith('darwin'):
                        if mobile_driver.appium_service is not None:
                            print("[MacOS]kill local appium server")
                            mobile_driver.appium_service.stop()
                    else:
                        print("[Windows]kill local appium server")
                        mobile_driver.kill_appium_server()
                else:
                    if not multilink:
                        if mobile_driver.ssh_handler is not None:
                            print("[MacOS]kill remote appium server")
                            sd.mobile_driver.kill_remote_appium_server()

    request.addfinalizer(class_finalizer)

@pytest.fixture(scope="function")
def default_function_fixture():
    print("calling Test_script function fixture")

@pytest.fixture(scope="function")
def non_default_function_fixture():
    print("calling Test_script function fixture. This is optional and executed only when called.")

@pytest.fixture(scope="class", autouse=True)
def connect_and_pair_dut(request):
    def launch_app_and_connect_dut(dut_friendly_name):
        app_package = sd.mobile_driver.get_capability('appPackage')
        status = sd.mobile_driver.close_app('appPackage')
        assert status, "Failed to close application"
        status = sd.mobile_driver.launch_app(app_package)
        assert status, "Failed to open application"
        print("Verify MBD App is open")
        app_open = request.cls.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        print("Scan for the DUT and pair")
        request.cls.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        status = sd.mobile_driver2.launch_app(app_package)
        assert status, "Failed to open application"
        print("Verify MBD App is open")
        app_open = request.cls.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        print("Scan for the DUT and pair")
        request.cls.scanandconnect.scan_and_connect_dut(dut_friendly_name)

    def class_finalizer():
        print("Local Class finalizer")
    
    request.addfinalizer(class_finalizer)
    return launch_app_and_connect_dut
