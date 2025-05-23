
import pytest
import time
from datetime import datetime

from ...CommonSupportLib.BleUARTPairingFeatureSupport import BLEUartPairingSupport
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
from ...CommonSupportLib.RNBDMBDFeatureSupport import RNBDFeatureSupport
from ...CommonSupportLib.RNBDPairingandLightBlueFeatureSupport import RNBDvsPhoneFeatureSupport
from ...CommonSupportLib.AppScanAndConnect import ScanningandConnection
from ...CommonSupportLib.IOControl_LEDStatus import IOControlLEDStatus
from ...CommonSupportLib.StationData import stationData
from ...CommonSupportLib.SoderaSupport import SoderaSupport
from ...BaseWrappers.BaseDriver import BaseDriver
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    PHONE_BT_ADDRESS_K, COM_PORT_K, BAUD_RATE_K, DUT_ADD_K

sd = stationData()

@pytest.fixture(scope="class", autouse=True)
def default_class_fixture(request):
    mobile_to_use = sd.config.mobile_data_config.get(sd.platform)
    # Multiple drivers for mobiles
    driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                        mobile_to_use.get(PHONE_UDID_K),
                        mobile_to_use.get(PLATFORM_NAME_K),
                        mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                        sd.config.app_package, sd.config.app_activity)
    sd.mobile_driver = driver
    request.cls.scanandconnect = ScanningandConnection()
    request.cls.bleuartfeature = BLEUARTFeatureSupport()
    request.cls.iocontrolledstatus = IOControlLEDStatus()
    request.cls.bleuartpairingfeature = BLEUartPairingSupport()
    request.cls.rnbdvsphonefeature = RNBDvsPhoneFeatureSupport()
    request.cls.rnbdfeature = RNBDFeatureSupport()
    time.sleep(3)
    if sd.config.capture_sodera_logs:
        request.cls.sodera = SoderaSupport(sd.config.sodera_server_ip, sd.config.sodera_server_port)
        request.cls.sodera.Open_Sodera(sd.config.sodera_fts_path)
        request.cls.sodera.Set_BT_Add(mobile_to_use.get(PHONE_BT_ADDRESS_K),DUT_ADD_K)
        request.cls.sodera.Start_Record()
        request.cls.sodera.Start_Analyze()
    def class_finalizer():
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
        status = sd.mobile_driver.close_app()
        assert status, "Failed to close application"
        status = sd.mobile_driver.launch_app()
        assert status, "Failed to open application"
        print("Verify MBD App is open")
        app_open = request.cls.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        print("Scan for the DUT and pair")
        request.cls.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        status = sd.mobile_driver2.launch_app()
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
