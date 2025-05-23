import pytest
import time
from datetime import datetime
from ...CommonSupportLib.AppScanAndConnect import ScanningandConnection
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
from ...CommonSupportLib.BleUARTPairingFeatureSupport import BLEUartPairingSupport
from ...CommonSupportLib.BleUARTOTADFUFeatureSupport import BLEUartOTADFUSupport
from ...CommonSupportLib.IOControl_LEDStatus import IOControlLEDStatus
from ...CommonSupportLib.StationData import stationData
from ...CommonSupportLib.SoderaSupport import SoderaSupport
from ...BaseWrappers.BaseDriver import BaseDriver
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    PHONE_BT_ADDRESS_K, COM_PORT_K, BAUD_RATE_K
sd = stationData()

@pytest.fixture(scope="function")
def default_function_fixture(request):
    print("Calling Test_script function fixture")
    # Multiple drivers for mobiles
    mobile_to_use = sd.config.mobile_data_config.get(sd.platform)
    driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                         mobile_to_use.get(PHONE_UDID_K),
                         mobile_to_use.get(PLATFORM_NAME_K),
                         mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                         sd.config.mobile_setting_app_package, sd.config.mobile_setting_app_activity)
    sd.mobile_driver = driver1
    print("*_*_*_*__*_*_Launched Settings page *__*_*_*_*_*_*_*_*_*")
    print(sd.mobile_driver)
    time.sleep(2)
    request.cls.bleuartpairingfeature = BLEUartPairingSupport()
    time.sleep(1)
    
    
    
    request.cls.bleuartpairingfeature.delete_paired_record_from_phone()    # one assert
    time.sleep(2)
    mobile_to_use = sd.config.mobile_data_config.get(sd.platform)
    driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity)
    sd.mobile_driver = driver
    print("*_*_*_*__*_*_*__*_*_*_*_*_*_*_*_*")
    print(sd.mobile_driver)
    request.cls.scanandconnect = ScanningandConnection()
    request.cls.bleuartfeature = BLEUARTFeatureSupport()
    # request.cls.deviceinfo = DeviceInfoSupport()
    request.cls.iocontrolledstatus = IOControlLEDStatus()
    request.cls.bleuartpairingfeature = BLEUartPairingSupport()
    request.cls.bleuartotadfufeature = BLEUartOTADFUSupport()


    def function_finalizer():
        print("Local Class finalizer")
    
    request.addfinalizer(function_finalizer)
    # return remove_paired_record_phone

    if sd.config.capture_sodera_logs:
        request.cls.sodera = SoderaSupport(sd.config.sodera_server_ip, sd.config.sodera_server_port)
        request.cls.sodera.Open_Sodera(sd.config.sodera_fts_path)
        request.cls.sodera.Set_BT_Add(mobile_to_use.get(PHONE_BT_ADDRESS_K))
        request.cls.sodera.Start_Record()
        request.cls.sodera.Start_Analyze()
    
    def function_finalizer():
        sd.mobile_driver.kill_appium_server()
        if sd.config.capture_sodera_logs:
            test_class_name = request.cls.__name__
            request.cls.sodera.Stop_Analyze()
            request.cls.sodera.Stop_Record()
            sodera_logs_file_name = "{0}_{1}_{2}".format("Sodera_Capture", test_class_name,
                                                         datetime.now().strftime("%d-%m-%Y_%I-%M-%S"))
            request.cls.sodera.Save_Capture(sodera_logs_file_name)
            request.cls.sodera.Close_Sodera()
            request.cls.sodera.kill_sodera_server()
        
        print("Switch on client DUT")
        #  request.cls.rpi.switch_on_dut(sd.config.client_dut)
        time.sleep(3)
    request.addfinalizer(function_finalizer)

@pytest.fixture(scope="function")
def non_default_function_fixture():
    print("calling Test_script function fixture. This is optional and executed only when called.")

# @pytest.fixture(scope="function", autouse=True)
# def remove_dut_paired_record(request):
    # def remove_paired_record_phone():
        # request.cls.bleuartpairingfeature.delete_paired_record_from_phone()
        # mobile_to_use = sd.config.mobile_data_config.get(sd.platform)
        # driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            # mobile_to_use.get(PHONE_UDID_K),
                            # mobile_to_use.get(PLATFORM_NAME_K),
                            # mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            # sd.config.app_package, sd.config.app_activity)
        # sd.mobile_driver = driver
        # print("*_*_*_*__*_*_*__*_*_*_*_*_*_*_*_*")
        # print(sd.mobile_driver)
        # request.cls.scanandconnect = ScanningandConnection()
        # request.cls.bleuartfeature = BLEUARTFeatureSupport()
        # # request.cls.deviceinfo = DeviceInfoSupport()
        # request.cls.iocontrolledstatus = IOControlLEDStatus()
        # request.cls.bleuartpairingfeature = BLEUartPairingSupport()
        # request.cls.bleuartotadfufeature = BLEUartOTADFUSupport()


    # def function_finalizer():
        # print("Local Class finalizer")
    
    # request.addfinalizer(function_finalizer)
    # return remove_paired_record_phone

