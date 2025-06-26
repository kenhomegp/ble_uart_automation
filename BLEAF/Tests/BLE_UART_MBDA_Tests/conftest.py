import pytest
import time
from datetime import datetime

from ...CommonSupportLib.BLEUARTFeatureSupportiOS import BLEUARTFeatureSupportiOS
from ...CommonSupportLib.BleUARTPairingFeatureSupport import BLEUartPairingSupport
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
from ...CommonSupportLib.AppScanAndConnect import ScanningandConnection
from ...CommonSupportLib.IOControl_LEDStatus import IOControlLEDStatus
from ...CommonSupportLib.StationData import stationData
#from ...CommonSupportLib.SoderaSupport import SoderaSupport
from ...BaseWrappers.BaseDriver import BaseDriver
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    PHONE_BT_ADDRESS_K, COM_PORT_K, BAUD_RATE_K, DUT_ADD_K

from ...BaseWrappers.SSHSupport import ShellHandler

sd = stationData()

@pytest.fixture(scope="class", autouse=True)
def default_class_fixture(request):
    print("BLE_UART_MBDA_Tests\conftest]")
    mobile_to_use = sd.config.mobile_data_config.get(sd.platform)
    print("Appium Server Config data:")
    print(mobile_to_use)

    #print(sd.config.multilink_phone_config)
    phone_list = sd.config.multilink_phone_config.split("/")
    phones_len = len(phone_list)
    print("Multilink phone . len = {}".format(phones_len))

    #print(sd.config.app_package)
    #print(sd.config.ios_mbda_app_package)
    #print(sd.config.appium_server_ip)
    # Multiple drivers for mobiles

    if sd.config.appium_server_ip == '127.0.0.1':
        remote_appium = False
    else:
        remote_appium = sd.remote_mac_server

    platform = mobile_to_use.get(PLATFORM_NAME_K)
    if platform == 'iOS':
        #sd.config.app_package = sd.config.ios_mbda_app_package
        print("platform = iOS. app package={}".format(sd.config.ios_mbda_app_package))
        sd.mobile_platform = platform

        if remote_appium:
            driver = BaseDriver(sd.config.remote_appium_server_ip, sd.config.remote_appium_server_port,
                                mobile_to_use.get(PHONE_UDID_K),
                                mobile_to_use.get(PLATFORM_NAME_K),
                                mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                sd.config.ios_mbda_app_package, sd.config.app_activity, remote_appium=phones_len)
        else:
            driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                                mobile_to_use.get(PHONE_UDID_K),
                                mobile_to_use.get(PLATFORM_NAME_K),
                                mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                sd.config.ios_mbda_app_package, sd.config.app_activity)

    else:
        if remote_appium:
            driver = BaseDriver(sd.config.remote_appium_server_ip, sd.config.remote_appium_server_port,
                                mobile_to_use.get(PHONE_UDID_K),
                                mobile_to_use.get(PLATFORM_NAME_K),
                                mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                sd.config.app_package, sd.config.app_activity, remote_appium=phones_len)
        else:
            driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                                mobile_to_use.get(PHONE_UDID_K),
                                mobile_to_use.get(PLATFORM_NAME_K),
                                mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                sd.config.app_package, sd.config.app_activity)

    mobile_data_dic = {}
    dev_name = mobile_to_use.get(DEVICE_NAME_K)
    mobile_data_dic['driver'] = driver
    mobile_data_dic['phone'] = dev_name
    sd.multilink_mobile_driver.append(mobile_data_dic)

    sd.mobile_driver = driver
    request.cls.scanandconnect = ScanningandConnection()
    if platform == 'iOS':
        request.cls.bleuartfeature = BLEUARTFeatureSupportiOS()
    else:
        request.cls.bleuartfeature = BLEUARTFeatureSupport()
    request.cls.iocontrolledstatus = IOControlLEDStatus()
    request.cls.bleuartpairingfeature = BLEUartPairingSupport()
    time.sleep(3)

    '''
    if sd.config.capture_sodera_logs:
        request.cls.sodera = SoderaSupport(sd.config.sodera_server_ip, sd.config.sodera_server_port)
        request.cls.sodera.Open_Sodera(sd.config.sodera_fts_path)
        request.cls.sodera.Set_BT_Add(mobile_to_use.get(PHONE_BT_ADDRESS_K),DUT_ADD_K)
        request.cls.sodera.Start_Record()
        request.cls.sodera.Start_Analyze()
    '''

    def class_finalizer():
        #sd.mobile_driver.kill_appium_server()
        #if sd.mobile_driver.platform == "Windows":

        if(len(sd.multilink_mobile_driver) >= 1):
            print("[Multilink]Close app and kill appium server ")

            android_udid_list = []
            for phone_info_dic in sd.multilink_mobile_driver:
                phone_name = phone_info_dic['phone']
                print("phone_name = {}.Close MBD app".format(phone_name))
                mobile_driver = phone_info_dic['driver']
                if "iphone" in phone_name.lower():
                    app_package = mobile_driver.get_capability('bundleId')
                else:
                    app_package = mobile_driver.get_capability('appPackage')
                time.sleep(3)
                #pid = mobile_driver.get_android_app_pid('R5CW321G69K')

                if "iphone" in phone_name.lower():
                    print("[iPhone]Get adb log. not supported")
                else:
                    mobile_info = sd.config.mobile_data_config.get(phone_name)
                    udid = mobile_info.get(PHONE_UDID_K)
                    android_udid_list.append(udid)

                #status = mobile_driver.close_app(app_package)
                #time.sleep(3)
                #assert status, "Failed to close application"

            for phone_info_dic in sd.multilink_mobile_driver:
                #phone_name = phone_info_dic['phone']
                #print("phone_name = {}.Close MBD app".format(phone_name))
                mobile_driver = phone_info_dic['driver']
                #if not sd.remote_mac_server:
                if not remote_appium:
                    print("kill local appium server")
                    mobile_driver.appium_service.stop()
                else:
                    if mobile_driver.ssh_handler is not None:
                        for udid in android_udid_list:
                            mobile_driver.get_android_adb_log(udid)
                            time.sleep(15)
                        sd.mobile_driver.kill_remote_appium_server()
        else:
            if sd.mobile_platform == "Android":
                app_package = sd.mobile_driver.get_capability('appPackage')
            else:
                app_package = sd.mobile_driver.get_capability('bundleId')
            time.sleep(3)
            status = sd.mobile_driver.close_app(app_package)
            time.sleep(3)
            assert status, "Failed to close application"
            if sd.remote_mac_server:
                sd.mobile_driver.kill_remote_appium_server()
            else:
                sd.mobile_driver.appium_service.stop()
                print("[MacOS]kill appium server")

        '''
        if sd.config.capture_sodera_logs:
            test_class_name = request.cls.__name__
            request.cls.sodera.Stop_Analyze()
            request.cls.sodera.Stop_Record()
            sodera_logs_file_name = "{0}_{1}_{2}".format("Sodera_Capture", test_class_name,
                                                         datetime.now().strftime("%d-%m-%Y_%I-%M-%S"))
            request.cls.sodera.Save_Capture(sodera_logs_file_name)
            request.cls.sodera.Close_Sodera()
            request.cls.sodera.kill_sodera_server()
        '''
        print("Switch on client DUT")
        time.sleep(3)
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
