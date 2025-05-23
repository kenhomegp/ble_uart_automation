import pytest
import os
import fnmatch
from ...CommonSupportLib.BleUARTPairingFeatureSupport import BLEUartPairingSupport
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
from ...CommonSupportLib.RNBDPairingandLightBlueFeatureSupport import RNBDvsPhoneFeatureSupport
from ...CommonSupportLib.AppScanAndConnect import ScanningandConnection
from ...CommonSupportLib.IOControl_LEDStatus import IOControlLEDStatus
from ...CommonSupportLib.StationData import stationData
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    PHONE_BT_ADDRESS_K, COM_PORT_K, BAUD_RATE_K, DUT_ADD_K

sd = stationData()

@pytest.fixture(scope="class", autouse=True)
def default_class_fixture(request):
    print("calling Test_scripts class fixture")
    request.cls.test_string = "This is Test_script class fixture"
    request.cls.scanandconnect = ScanningandConnection()
    request.cls.bleuartfeature = BLEUARTFeatureSupport()
    request.cls.iocontrolledstatus = IOControlLEDStatus()
    request.cls.bleuartpairingfeature = BLEUartPairingSupport()
    request.cls.rnbdvsphonefeature = RNBDvsPhoneFeatureSupport()

@pytest.fixture(scope="function")
def non_default_function_fixture():
    print("calling Test_script function fixture. This is optional and executed only when called.")

def get_tests_to_execute(tp_name):
    tests_to_execute = sd.test_link.get_tests_to_execute(tp_name)
    return tests_to_execute

def pytest_configure(config):
    config.addinivalue_line("markers",
                            "test_id(id): marker with test id corresponding to testlink test case")
    test_plan_name = config.getoption('tp_name')
    listfiles = []
    if "Pairing" in test_plan_name:
        for root, dirs, files in os.walk(sd.config.fwfolderpath):
            for filename in fnmatch.filter(files, '*.hex'):
               listfiles.append(filename)
        for each in listfiles:
            if "pair" in each:
                sd.fw_folder = each
    else:
        for root, dirs, files in os.walk(sd.config.fwfolderpath):
            for filename in fnmatch.filter(files, '*.hex'):
                listfiles.append(filename)
        for each in listfiles:
            if "pair" not in each:
                sd.fw_folder = each