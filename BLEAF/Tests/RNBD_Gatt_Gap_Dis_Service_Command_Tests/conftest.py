
import pytest
import time
from datetime import datetime

from ...CommonSupportLib.BleUARTPairingFeatureSupport import BLEUartPairingSupport
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
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
                        sd.config.lightblue_app_package, sd.config.lightblue_app_activity)
    sd.mobile_driver = driver
    request.cls.scanandconnect = ScanningandConnection()
    request.cls.bleuartfeature = BLEUARTFeatureSupport()
    request.cls.iocontrolledstatus = IOControlLEDStatus()
    request.cls.bleuartpairingfeature = BLEUartPairingSupport()
    request.cls.rnbdvsphonefeature = RNBDvsPhoneFeatureSupport()
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
        time.sleep(3)
    request.addfinalizer(class_finalizer)

@pytest.fixture(scope="function")
def default_function_fixture():
    print("calling Test_script function fixture")

@pytest.fixture(scope="function")
def non_default_function_fixture():
    print("calling Test_script function fixture. This is optional and executed only when called.")
