import collections
import pytest
import time
from collections import OrderedDict

from ...BaseWrappers.BaseDriver import BaseDriver
from ...CommonSupportLib.AppScanAndConnect import ScanningandConnection
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
from ...CommonSupportLib.RNBDPairingandLightBlueFeatureSupport import RNBDvsPhoneFeatureSupport
from ...CommonSupportLib.StationData import stationData
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    PHONE_BT_ADDRESS_K, COM_PORT_K, BAUD_RATE_K

from ...MCP2200.MCP2200 import Mcp2200
from ...StationConfig import conf_file
sd = stationData()
MCU = Mcp2200()
dut_friendly_name = conf_file.dut_friendly_name
comport = conf_file.com_port
baudrate = conf_file.baud_rate

phone_list = ["SamsungS21","GooglePixel5","OPPO Reno","SamsungS10","GooglePixel3A","VivoV11"]
mobile_obj_list = []

@pytest.fixture(scope="class", autouse=True)
def define_class_attributes(request, default_class_fixture):
    print("this is local specific class fixture")
    def class_finalizer():
        print("Local Class finalizer")
    request.addfinalizer(class_finalizer)

@pytest.fixture(scope="function", autouse=True)
def local_function_fixture(request):
    print("Local function fixture")
    print("Launch MBD Application")
    def function_finalizer():
        print("Local function finalizer")
    request.addfinalizer(function_finalizer)

class TestRNBDConnectBLEUartMultilink:
    @pytest.mark.skip("RNBD451_MULTILINK_SCAN_AND_CONNECT", 'MBDA')
    def test_rnbd_ble_uart_multilink_scan_and_connect(self):
        error_msg1, error_msg2, error_msg3, error_msg4, error_msg5, error_msg6 = "","","","","",""
        test_status = True
        step_descript = []
        print("{0}Test to verify RNBD Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan and Connect with 6 Android phones {0}".format('=' * 20))
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use1)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use1.get(PHONE_UDID_K),
                            mobile_to_use1.get(PLATFORM_NAME_K),
                            mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        rnbdvsphonefeature = RNBDvsPhoneFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        step_result1, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result2, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        rnbdvsphonefeature1 = RNBDvsPhoneFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result3, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        rnbdvsphonefeature2 = RNBDvsPhoneFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result4, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        rnbdvsphonefeature3 = RNBDvsPhoneFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result5, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        rnbdvsphonefeature4 = RNBDvsPhoneFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result6, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use6 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use6)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use6.get(PHONE_UDID_K),
                             mobile_to_use6.get(PLATFORM_NAME_K),
                             mobile_to_use6.get(PLATFORM_VERSION_K), mobile_to_use6.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        rnbdvsphonefeature5 = RNBDvsPhoneFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        bleuartfeature.close_mbd_app()
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()

        print("Step Results", step_result1,step_result2,step_result3,step_result4,step_result5,step_result6)
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step discription of Phone1 for more details\n"
        elif False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step discription of Phone2 for more details\n"
        elif False in step_result3:
            test_status = False
            error_msg3 = "Few of the commands have failed. Please refer step discription of Phone3 for more details\n"
        elif False in step_result4:
            test_status = False
            error_msg4 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
        elif False in step_result5:
            test_status = False
            error_msg5 = "Few of the commands have failed. Please refer step discription of Phone5 for more details\n"
        elif False in step_result6:
            test_status = False
            error_msg6 = "Few of the commands have failed. Please refer step discription of Phone6 for more details\n"
        self.note += error_msg1
        self.note += error_msg2
        self.note += error_msg3
        self.note += error_msg4
        self.note += error_msg5
        self.note += error_msg6
        assert test_status, error_msg1
        assert test_status, error_msg2
        assert test_status, error_msg3
        assert test_status, error_msg4
        assert test_status, error_msg5
        assert test_status, error_msg6
        self.test_result = True

    @pytest.mark.skip("RNBD451_MULTILINK_CONNECT_AND_DISCONNECT", 'MBDA')
    def test_rnbd_ble_uart_multilink_scan_connect_disconnect(self):
        error_msg1, error_msg2, error_msg3, error_msg4, error_msg5, error_msg6 = "","","","","",""
        test_status = True
        step_result = []
        step_descript = []
        print("{0}Test to verify RNBD Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan, Connect & Disconnect with 6 Android phones {0}".format('=' * 20))
        mobile_data_dic = {}
        phone_obj_list = {}
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        step_result1, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result2, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result3, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result4, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result5, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result6, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        time.sleep(10)
        print("Disconnect All phones")
        bleuartfeature.go_back()
        bleuartfeature1.go_back()
        bleuartfeature2.go_back()
        bleuartfeature3.go_back()
        bleuartfeature4.go_back()
        bleuartfeature5.go_back()
        time.sleep(2)
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        print("Step Results", step_result)
        print("Step Results", step_result1, step_result2, step_result3, step_result4, step_result5, step_result6)
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step discription of Phone1 for more details\n"
        elif False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step discription of Phone2 for more details\n"
        elif False in step_result3:
            test_status = False
            error_msg3 = "Few of the commands have failed. Please refer step discription of Phone3 for more details\n"
        elif False in step_result4:
            test_status = False
            error_msg4 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
        elif False in step_result5:
            test_status = False
            error_msg5 = "Few of the commands have failed. Please refer step discription of Phone5 for more details\n"
        elif False in step_result6:
            test_status = False
            error_msg6 = "Few of the commands have failed. Please refer step discription of Phone6 for more details\n"
        self.note += error_msg1
        self.note += error_msg2
        self.note += error_msg3
        self.note += error_msg4
        self.note += error_msg5
        self.note += error_msg6
        assert test_status, error_msg1
        assert test_status, error_msg2
        assert test_status, error_msg3
        assert test_status, error_msg4
        assert test_status, error_msg5
        assert test_status, error_msg6
        self.test_result = True

    @pytest.mark.skip("RNBD451_MULTILINK_DISCONNECT_LAST_CONNECTED_DEVICE", 'MBDA')
    def test_rnbd_disconnect_last_connected_device(self):
        error_msg1, error_msg2, error_msg3, error_msg4, error_msg5, error_msg6, error_msg7 = "","","","","","",""
        test_status = True
        step_result = []
        step_descript = []
        print("{0}Test to verify RNBD Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan and Connect with 6 Android phones and disconnect last connected device{0}".format('=' * 20))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity,fresh_env=False, remote_appium=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        rnbdvsphonefeature = RNBDvsPhoneFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        step_result1, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result2, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity,fresh_env=False, remote_appium=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        rnbdvsphonefeature1 = RNBDvsPhoneFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result3, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity,fresh_env=False, remote_appium=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        rnbdvsphonefeature2 = RNBDvsPhoneFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result4, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        rnbdvsphonefeature3 = RNBDvsPhoneFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result5, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        rnbdvsphonefeature4 = RNBDvsPhoneFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result6, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(10)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity,fresh_env=False, remote_appium=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        rnbdvsphonefeature5 = RNBDvsPhoneFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result7, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Disconnect_Last_Connected_Device')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        status = rnbdvsphonefeature5.verify_scan_page()
        time.sleep(10)
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        print("Step Results", step_result1, step_result2, step_result3, step_result4, step_result5, step_result6)
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step discription of Phone1 for more details\n"
        elif False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step discription of Phone2 for more details\n"
        elif False in step_result3:
            test_status = False
            error_msg3 = "Few of the commands have failed. Please refer step discription of Phone3 for more details\n"
        elif False in step_result4:
            test_status = False
            error_msg4 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
        elif False in step_result5:
            test_status = False
            error_msg5 = "Few of the commands have failed. Please refer step discription of Phone5 for more details\n"
        elif False in step_result6:
            test_status = False
            error_msg6 = "Few of the commands have failed. Please refer step discription of Phone6 for more details\n"
        elif False in step_result7:
            test_status = False
            error_msg7 = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg1
        self.note += error_msg2
        self.note += error_msg3
        self.note += error_msg4
        self.note += error_msg5
        self.note += error_msg6
        self.note += error_msg7
        assert test_status, error_msg1
        assert test_status, error_msg2
        assert test_status, error_msg3
        assert test_status, error_msg4
        assert test_status, error_msg5
        assert test_status, error_msg6
        assert test_status, error_msg7
        self.test_result = True

    @pytest.mark.skip("RNBD451_MULTILINK_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_WITH_COMMAND_RESPONSE", 'MBDA')
    def test_rnbd_ble_uart_multilink_bidirectional_data_transfer(self):
        error_msg1, error_msg2, error_msg3, error_msg4, error_msg5, error_msg6, error_msg7 = "","","","","","",""
        test_status = True
        step_result = []
        step_descript = []
        print("{0}Test to verify RNBD Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Multilink Bidirectional data transfer with 6 Android phones {0}".format('=' * 20))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        rnbdvsphonefeature = RNBDvsPhoneFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        step_result1, step_descript = rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        scanandconnect.verify_raw_data_mode()
        mode_set_trp = scanandconnect.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result2, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        rnbdvsphonefeature1 = RNBDvsPhoneFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        scanandconnect1.verify_raw_data_mode()
        mode_set_trp = scanandconnect1.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result3, step_descript = rnbdvsphonefeature1.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        rnbdvsphonefeature2 = RNBDvsPhoneFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        scanandconnect2.verify_raw_data_mode()
        mode_set_trp = scanandconnect2.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result4, step_descript = rnbdvsphonefeature2.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        rnbdvsphonefeature3 = RNBDvsPhoneFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        scanandconnect3.verify_raw_data_mode()
        mode_set_trp = scanandconnect3.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result5, step_descript = rnbdvsphonefeature3.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        rnbdvsphonefeature4 = RNBDvsPhoneFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        scanandconnect4.verify_raw_data_mode()
        mode_set_trp = scanandconnect4.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result6, step_descript = rnbdvsphonefeature4.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        rnbdvsphonefeature5 = RNBDvsPhoneFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        scanandconnect5.verify_raw_data_mode()
        mode_set_trp = scanandconnect5.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        data_transfer, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Data_Transmission_Command_Set')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        status, data_from_rnbd = rnbdvsphonefeature.send_raw_data_uart_mode_rnbd_to_app()
        assert status, "Test case failed as comparison is not successful in Phone 1"
        self.note += "Data received in Phone1 App :" + (data_from_rnbd) + "\n"
        status1, data_from_rnbd = rnbdvsphonefeature1.send_raw_data_uart_mode_rnbd_to_app()
        assert status1, "Test case failed as comparison is not successful in Phone 2"
        self.note += "Data received in Phone2 App :" + (data_from_rnbd) + "\n"
        status2, data_from_rnbd = rnbdvsphonefeature2.send_raw_data_uart_mode_rnbd_to_app()
        assert status2, "Test case failed as comparison is not successfulin Phone 3"
        self.note += "Data received in Phone3 App :" + (data_from_rnbd) + "\n"
        status3, data_from_rnbd = rnbdvsphonefeature3.send_raw_data_uart_mode_rnbd_to_app()
        assert status3, "Test case failed as comparison is not successful in Phone 4"
        self.note += "Data received in Phone4 App :" + (data_from_rnbd) + "\n"
        status4, data_from_rnbd = rnbdvsphonefeature4.send_raw_data_uart_mode_rnbd_to_app()
        assert status4, "Test case failed as comparison is not successful in Phone 5"
        self.note += "Data received in Phone5 App :" + (data_from_rnbd) + "\n"
        status5, data_from_rnbd = rnbdvsphonefeature5.send_raw_data_uart_mode_rnbd_to_app()
        assert status5, "Test case failed as comparison is not successful in Phone 6"
        self.note += "Data received in Phone6 App :" + (data_from_rnbd) + "\n"
        time.sleep(5)
        status, data_from_app = rnbdvsphonefeature.send_raw_data_uart_mode_app_to_rnbd("%DATA:0071,0008,3132333435363738%")
        assert status, "Test case failed as comparison is not successful in Phone 1"
        self.note += "Data received in RNBD from Phone 1:" + (data_from_app) + "\n"
        status1, data_from_app = rnbdvsphonefeature1.send_raw_data_uart_mode_app_to_rnbd("%DATA:0072,0008,3132333435363738%")
        assert status1, "Test case failed as comparison is not successful in Phone 2"
        self.note += "Data received in RNBD from Phone 2:" + (data_from_app) + "\n"
        status2, data_from_app = rnbdvsphonefeature2.send_raw_data_uart_mode_app_to_rnbd("%DATA:0073,0008,3132333435363738%")
        assert status2, "Test case failed as comparison is not successful in Phone 3"
        self.note += "Data received in RNBD from Phone 3:" + (data_from_app) + "\n"
        status3, data_from_app = rnbdvsphonefeature3.send_raw_data_uart_mode_app_to_rnbd("%DATA:0074,0008,3132333435363738%")
        assert status3, "Test case failed as comparison is not successful in Phone 4"
        self.note += "Data received in RNBD from Phone 4:" + (data_from_app) + "\n"
        status4, data_from_app = rnbdvsphonefeature4.send_raw_data_uart_mode_app_to_rnbd("%DATA:0075,0008,3132333435363738%")
        assert status4, "Test case failed as comparison is not successful in Phone 5"
        self.note += "Data received in RNBD from Phone 5:" + (data_from_app) + "\n"
        status5, data_from_app = rnbdvsphonefeature5.send_raw_data_uart_mode_app_to_rnbd("%DATA:0076,0008,3132333435363738%")
        assert status5, "Test case failed as comparison is not successful in Phone 6"
        self.note += "Data received in RNBD from Phone 6:" + (data_from_app) + "\n"
        time.sleep(10)
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        print("Step Results", step_result)
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step discription of Phone1 for more details\n"
        elif False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step discription of Phone2 for more details\n"
        elif False in step_result3:
            test_status = False
            error_msg3 = "Few of the commands have failed. Please refer step discription of Phone3 for more details\n"
        elif False in step_result4:
            test_status = False
            error_msg4 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
        elif False in step_result5:
            test_status = False
            error_msg5 = "Few of the commands have failed. Please refer step discription of Phone5 for more details\n"
        elif False in step_result6:
            test_status = False
            error_msg6 = "Few of the commands have failed. Please refer step discription of Phone6 for more details\n"
        elif False in data_transfer:
            test_status = False
            error_msg8 = "Few of the commands have failed. Please refer step discription of Multilink data transfer for more details\n"
        self.note += error_msg1
        self.note += error_msg2
        self.note += error_msg3
        self.note += error_msg4
        self.note += error_msg5
        self.note += error_msg6
        self.note += error_msg7
        assert test_status, error_msg1
        assert test_status, error_msg2
        assert test_status, error_msg3
        assert test_status, error_msg4
        assert test_status, error_msg5
        assert test_status, error_msg6
        assert test_status, error_msg7
        self.test_result = True

    @pytest.mark.skip("RNBD451_VS_6PHONES_OVERNIGHT_CONNECTION_STABILITY", 'MBDA')
    def test_rnbd_ble_uart_multilink_overnight_connection_stability(self):
        error_msg1, error_msg2, error_msg3, error_msg4, error_msg5, error_msg6 = "","","","","",""
        test_status = True
        print("{0}Test to verify RNBD BLE UART Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan and Connect & Overnight Connection Stability with 6 Android phones {0}".format(
            '=' * 10))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        step_result1, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result2, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity,fresh_env=False, remote_appium=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result3, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False,remote_appium=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result4, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity,fresh_env=False, remote_appium=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result5, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity,fresh_env=False, remote_appium=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result6, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False,remote_appium=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        duration_conn_test = 60 * 60 # Seconds
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
        print("Step Results", step_result1, step_result2, step_result3, step_result4)
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step discription of Phone1 for more details\n"
        elif False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step discription of Phone2 for more details\n"
        elif False in step_result3:
            test_status = False
            error_msg3 = "Few of the commands have failed. Please refer step discription of Phone3 for more details\n"
        elif False in step_result4:
            test_status = False
            error_msg4 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
        elif False in step_result5:
            test_status = False
            error_msg5 = "Few of the commands have failed. Please refer step discription of Phone5 for more details\n"
        elif False in step_result6:
            test_status = False
            error_msg6 = "Few of the commands have failed. Please refer step discription of Phone6 for more details\n"
        self.note += error_msg1
        self.note += error_msg2
        self.note += error_msg3
        self.note += error_msg4
        self.note += error_msg5
        self.note += error_msg6
        assert test_status, error_msg1
        assert test_status, error_msg2
        assert test_status, error_msg3
        assert test_status, error_msg4
        assert test_status, error_msg5
        assert test_status, error_msg6
        self.test_result = True

    @pytest.mark.skip("RNBD451_MULTILINK_KILL_MBD_APP", 'MBDA')
    def test_rnbd_multilink_kill_mbd_app(self):
        error_msg1, error_msg2, error_msg3, error_msg4, error_msg5, error_msg6 = "","","","","",""
        test_status = True
        print("{0}Test to verify RNBD Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Kill MBD APP in all 6 Connected Phones {0}".format('=' * 20))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        step_result1, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result2, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result3, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result4, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result5, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result6, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        time.sleep(10)
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = scanandconnect.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful in Phone1"
        assert status, msg
        self.note += msg
        status1, msg1 = scanandconnect1.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful in Phone2"
        assert status1, msg1
        self.note += msg1
        status2, msg2 = scanandconnect2.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful in Phone3"
        assert status2, msg2
        self.note += msg2
        status3, msg3 = scanandconnect3.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful in Phone4"
        assert status3, msg3
        self.note += msg3
        status4, msg4 = scanandconnect4.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful in Phone5"
        assert status4, msg4
        self.note += msg4
        status5, msg5 = scanandconnect5.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful in Phone6"
        assert status5, msg5
        self.note += msg5
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step discription of Phone1 for more details\n"
            assert test_status, error_msg1
            self.note += error_msg1
        elif False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step discription of Phone2 for more details\n"
            assert test_status, error_msg2
            self.note += error_msg2
        elif False in step_result3:
            test_status = False
            error_msg3 = "Few of the commands have failed. Please refer step discription of Phone3 for more details\n"
            assert test_status, error_msg3
            self.note += error_msg3
        elif False in step_result4:
            test_status = False
            error_msg4 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
            assert test_status, error_msg4
            self.note += error_msg4
        elif False in step_result5:
            test_status = False
            error_msg4 = "Few of the commands have failed. Please refer step discription of Phone5 for more details\n"
            assert test_status, error_msg5
            self.note += error_msg5
        elif False in step_result6:
            test_status = False
            error_msg4 = "Few of the commands have failed. Please refer step discription of Phone6 for more details\n"
            assert test_status, error_msg6
            self.note += error_msg6
            self.test_result = True


    @pytest.mark.skip("RNBD451_SINGLE_LINK_BIDIRECTIONAL_DATA_TRANSMISSION_WITH_COMMAND_RESPONSE", 'MBDA')
    def test_rnbd_ble_uart_singlelink_bidirectional_data_transfer(self):
        error_msg1, error_msg2 = "",""
        test_status = True
        step_result = []
        step_descript = []
        print("{0}Test to verify RNBD Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan and Connect 1 Android phone {0}".format('=' * 20))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        rnbdvsphonefeature = RNBDvsPhoneFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        step_result1, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        scanandconnect.verify_raw_data_mode()
        mode_set_trp = scanandconnect.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result2, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Single_Link_Data_Transmission_Command_Set')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        status, data_from_rnbd = rnbdvsphonefeature.send_raw_data_uart_mode_rnbd_to_app()
        assert status, "Test case failed as comparison is not successful in Phone 1"
        self.note += "Data received in App :" + (data_from_rnbd) + "\n"
        status, data_from_app = rnbdvsphonefeature.send_raw_data_uart_mode_app_to_rnbd("%DATA:0071,0008,3132333435363738%")
        assert status, "Test case failed as comparison is not successful in Phone 1"
        self.note += "Data received in RNBD :" + (data_from_app) + "\n"
        bleuartfeature.close_mbd_app()
        print("Step Results", step_result)
        print("Step Results", step_result1, step_result2)
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step discription of Phone1 for more details\n"
        elif False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step discription of Phone2 for more details\n"
        self.note += error_msg1
        self.note += error_msg2
        assert test_status, error_msg1
        assert test_status, error_msg2
        self.test_result = True

    @pytest.mark.skip("RNBD451_MULTILINK_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_WITHOUT_COMMAND_RESPONSE", 'MBDA')
    def test_rnbd_ble_uart_multilink_bidirectional_data_transfer_without_command_response(self):
        error_msg1, error_msg2, error_msg3, error_msg4, error_msg5, error_msg6, error_msg7 = "", "", "", "", "", "", ""
        test_status = True
        step_result = []
        step_descript = []
        print("{0}Test to verify RNBD Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Multilink Bidirectional data transfer with 6 Android phones {0}".format('=' * 20))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        rnbdvsphonefeature = RNBDvsPhoneFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        step_result1, step_descript = rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        scanandconnect.verify_raw_data_mode()
        mode_set_trp = scanandconnect.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result2, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        rnbdvsphonefeature1 = RNBDvsPhoneFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        scanandconnect1.verify_raw_data_mode()
        mode_set_trp = scanandconnect1.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result3, step_descript = rnbdvsphonefeature1.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        rnbdvsphonefeature2 = RNBDvsPhoneFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        scanandconnect2.verify_raw_data_mode()
        mode_set_trp = scanandconnect2.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result4, step_descript = rnbdvsphonefeature2.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        rnbdvsphonefeature3 = RNBDvsPhoneFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        scanandconnect3.verify_raw_data_mode()
        mode_set_trp = scanandconnect3.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result5, step_descript = rnbdvsphonefeature3.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        rnbdvsphonefeature4 = RNBDvsPhoneFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        scanandconnect4.verify_raw_data_mode()
        mode_set_trp = scanandconnect4.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result6, step_descript = rnbdvsphonefeature4.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        rnbdvsphonefeature5 = RNBDvsPhoneFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        scanandconnect5.verify_raw_data_mode()
        mode_set_trp = scanandconnect5.confirm_raw_data_mode_trp()
        assert mode_set_trp, "Raw data is not set accordingly"
        time.sleep(5)
        step_result7, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Disable_Command_Response')
        self.rnbdvsphonefeature.send_rnbd_to_app("IE,0071,0008,3132333435363738\r")
        self.rnbdvsphonefeature.send_rnbd_to_app("IE,0072,0008,3132333435363738\r")
        self.rnbdvsphonefeature.send_rnbd_to_app("IE,0073,0008,3132333435363738\r")
        self.rnbdvsphonefeature.send_rnbd_to_app("IE,0074,0008,3132333435363738\r")
        self.rnbdvsphonefeature.send_rnbd_to_app("IE,0075,0008,3132333435363738\r")
        self.rnbdvsphonefeature.send_rnbd_to_app("IE,0076,0008,3132333435363738\r")
        status, data_from_rnbd = rnbdvsphonefeature.send_raw_data_uart_mode_rnbd_to_app()
        assert status, "Test case failed as comparison is not successful in Phone 1"
        self.note += "Data received in Phone1 App :" + (data_from_rnbd) + "\n"
        status1, data_from_rnbd = rnbdvsphonefeature1.send_raw_data_uart_mode_rnbd_to_app()
        assert status1, "Test case failed as comparison is not successful in Phone 2"
        self.note += "Data received in Phone2 App :" + (data_from_rnbd) + "\n"
        status2, data_from_rnbd = rnbdvsphonefeature2.send_raw_data_uart_mode_rnbd_to_app()
        assert status2, "Test case failed as comparison is not successfulin Phone 3"
        self.note += "Data received in Phone3 App :" + (data_from_rnbd) + "\n"
        status3, data_from_rnbd = rnbdvsphonefeature3.send_raw_data_uart_mode_rnbd_to_app()
        assert status3, "Test case failed as comparison is not successful in Phone 4"
        self.note += "Data received in Phone4 App :" + (data_from_rnbd) + "\n"
        status4, data_from_rnbd = rnbdvsphonefeature4.send_raw_data_uart_mode_rnbd_to_app()
        assert status4, "Test case failed as comparison is not successful in Phone 5"
        self.note += "Data received in Phone5 App :" + (data_from_rnbd) + "\n"
        status5, data_from_rnbd = rnbdvsphonefeature5.send_raw_data_uart_mode_rnbd_to_app()
        assert status5, "Test case failed as comparison is not successful in Phone 6"
        self.note += "Data received in Phone6 App :" + (data_from_rnbd) + "\n"
        time.sleep(5)
        status, data_from_app = rnbdvsphonefeature.send_raw_data_uart_mode_app_to_rnbd(
            "%DATA:0071,0008,3132333435363738%")
        assert status, "Test case failed as comparison is not successful in Phone 1"
        self.note += "Data received in RNBD from Phone 1:" + (data_from_app) + "\n"
        status1, data_from_app = rnbdvsphonefeature1.send_raw_data_uart_mode_app_to_rnbd(
            "%DATA:0072,0008,3132333435363738%")
        assert status1, "Test case failed as comparison is not successful in Phone 2"
        self.note += "Data received in RNBD from Phone 2:" + (data_from_app) + "\n"
        status2, data_from_app = rnbdvsphonefeature2.send_raw_data_uart_mode_app_to_rnbd("%DATA:0073,0008,3132333435363738%")
        assert status2, "Test case failed as comparison is not successful in Phone 3"
        self.note += "Data received in RNBD from Phone 3:" + (data_from_app) + "\n"
        status3, data_from_app = rnbdvsphonefeature3.send_raw_data_uart_mode_app_to_rnbd("%DATA:0074,0008,3132333435363738%")
        assert status3, "Test case failed as comparison is not successful in Phone 4"
        self.note += "Data received in RNBD from Phone 4:" + (data_from_app) + "\n"
        status4, data_from_app = rnbdvsphonefeature4.send_raw_data_uart_mode_app_to_rnbd("%DATA:0075,0008,3132333435363738%")
        assert status4, "Test case failed as comparison is not successful in Phone 5"
        self.note += "Data received in RNBD from Phone 5:" + (data_from_app) + "\n"
        status5, data_from_app = rnbdvsphonefeature5.send_raw_data_uart_mode_app_to_rnbd("%DATA:0076,0008,3132333435363738%")
        assert status5, "Test case failed as comparison is not successful in Phone 6"
        self.note += "Data received in RNBD from Phone 6:" + (data_from_app) + "\n"
        time.sleep(10)
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step discription of Phone1 for more details\n"
        elif False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step discription of Phone2 for more details\n"
        elif False in step_result3:
            test_status = False
            error_msg3 = "Few of the commands have failed. Please refer step discription of Phone3 for more details\n"
        elif False in step_result4:
            test_status = False
            error_msg4 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
        elif False in step_result5:
            test_status = False
            error_msg5 = "Few of the commands have failed. Please refer step discription of Phone5 for more details\n"
        elif False in step_result6:
            test_status = False
            error_msg6 = "Few of the commands have failed. Please refer step discription of Phone6 for more details\n"
        elif False in step_result7:
            test_status = False
            error_msg7 = "Few of the commands have failed. Please refer step discription of Multilink data transfer without command response command for more details\n"
        self.note += error_msg1
        self.note += error_msg2
        self.note += error_msg3
        self.note += error_msg4
        self.note += error_msg5
        self.note += error_msg6
        self.note += error_msg7
        assert test_status, error_msg1
        assert test_status, error_msg2
        assert test_status, error_msg3
        assert test_status, error_msg4
        assert test_status, error_msg5
        assert test_status, error_msg6
        assert test_status, error_msg7
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD451_MULTILINK_CONNECT_AND_DISCONNECT_STRESS_TEST", 'MBDA')
    def test_rnbd_ble_uart_multilink_scan_connect_disconnect_stress_test(self):
        error_msg1, error_msg2, error_msg3, error_msg4, error_msg5, error_msg6 = "", "", "", "","",""
        test_status = True
        step_result = []
        step_descript = []
        print("{0}Test to verify RNBD Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan, Connect & Disconnect with 6 Android phones {0}".format('=' * 20))
        mobile_data_dic = {}
        phone_obj_list = {}
        for i in range(1, 2):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
                print(mobile_to_use)
                driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                                    mobile_to_use.get(PHONE_UDID_K),
                                    mobile_to_use.get(PLATFORM_NAME_K),
                                    mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                                    sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
                scanandconnect = ScanningandConnection(driver)
                bleuartfeature = BLEUARTFeatureSupport(driver)
                driver.launch_app()
                print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
                print("Verify MBD App is open")
                app_open = scanandconnect.verify_app_open()
                assert app_open, "Failed to open MBD Application"
                print("Put the DUT to advertising mode")
                step_result1, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
                for step_des in step_descript:
                    self.note += "Command mode results: \n" + str(step_des) + "\n"
                time.sleep(5)
                print("Scan for the DUT and connect")
                scanandconnect.scan_and_connect_dut(dut_friendly_name)
                time.sleep(5)
                status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
                print("DUT is connected with Phone:")
                assert status, "Unable to scan and connect to DUT"
                time.sleep(2)
                step_result2, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
                for step_des in step_descript:
                    self.note += "Command mode results: \n" + str(step_des) + "\n"
                mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
                print(mobile_to_use1)
                # Multiple drivers for mobiles
                driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                                     mobile_to_use1.get(PHONE_UDID_K),
                                     mobile_to_use1.get(PLATFORM_NAME_K),
                                     mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                                     sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
                scanandconnect1 = ScanningandConnection(driver1)
                bleuartfeature1 = BLEUARTFeatureSupport(driver1)
                driver1.launch_app()
                print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
                print("Verify MBD App is open")
                app_open = scanandconnect1.verify_app_open()
                assert app_open, "Failed to open MBD Application"
                print("Put the DUT to advertising mode")
                time.sleep(5)
                print("Scan for the DUT and connect")
                scanandconnect1.scan_and_connect_dut(dut_friendly_name)
                time.sleep(5)
                status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
                print("DUT is connected with Phone:")
                assert status, "Unable to scan and connect to DUT"
                time.sleep(2)
                step_result3, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
                for step_des in step_descript:
                    self.note += "Command mode results: \n" + str(step_des) + "\n"
                time.sleep(5)
                mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
                print(mobile_to_use2)
                # Multiple drivers for mobiles
                driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                                     mobile_to_use2.get(PHONE_UDID_K),
                                     mobile_to_use2.get(PLATFORM_NAME_K),
                                     mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                                     sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
                scanandconnect2 = ScanningandConnection(driver2)
                bleuartfeature2 = BLEUARTFeatureSupport(driver2)
                driver2.launch_app()
                print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
                step_result4, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
                for step_des in step_descript:
                    self.note += "Command mode results: \n" + str(step_des) + "\n"
                time.sleep(5)
                mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
                print(mobile_to_use3)
                # Multiple drivers for mobiles
                driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                                     mobile_to_use3.get(PHONE_UDID_K),
                                     mobile_to_use3.get(PLATFORM_NAME_K),
                                     mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                                     sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
                scanandconnect3 = ScanningandConnection(driver3)
                bleuartfeature3 = BLEUARTFeatureSupport(driver3)
                driver3.launch_app()
                print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
                step_result5, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
                for step_des in step_descript:
                    self.note += "Command mode results: \n" + str(step_des) + "\n"
                time.sleep(5)
                mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
                print(mobile_to_use4)
                # Multiple drivers for mobiles
                driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                                     mobile_to_use4.get(PHONE_UDID_K),
                                     mobile_to_use4.get(PLATFORM_NAME_K),
                                     mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                                     sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
                scanandconnect4 = ScanningandConnection(driver4)
                bleuartfeature4 = BLEUARTFeatureSupport(driver4)
                driver4.launch_app()
                print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
                step_result6, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
                for step_des in step_descript:
                    self.note += "Command mode results: \n" + str(step_des) + "\n"
                time.sleep(5)
                mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
                print(mobile_to_use5)
                # Multiple drivers for mobiles
                driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                                     mobile_to_use5.get(PHONE_UDID_K),
                                     mobile_to_use5.get(PLATFORM_NAME_K),
                                     mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                                     sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
                scanandconnect5 = ScanningandConnection(driver5)
                bleuartfeature5 = BLEUARTFeatureSupport(driver5)
                driver5.launch_app()
                print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
                time.sleep(10)
                print("Disconnect All phones")
                bleuartfeature.go_back()
                bleuartfeature1.go_back()
                bleuartfeature2.go_back()
                bleuartfeature3.go_back()
                bleuartfeature4.go_back()
                bleuartfeature5.go_back()
                time.sleep(10)
                print("Step Results", step_result)
                print("Step Results", step_result1, step_result2, step_result3, step_result4, step_result5, step_result6)
                if False in step_result1:
                    test_status = False
                    error_msg1 = "Few of the commands have failed. Please refer step discription of Phone1 for more details\n"
                elif False in step_result2:
                    test_status = False
                    error_msg2 = "Few of the commands have failed. Please refer step discription of Phone2 for more details\n"
                elif False in step_result3:
                    test_status = False
                    error_msg3 = "Few of the commands have failed. Please refer step discription of Phone3 for more details\n"
                elif False in step_result4:
                    test_status = False
                    error_msg4 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
                elif False in step_result5:
                    test_status = False
                    error_msg5 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
                elif False in step_result6:
                    test_status = False
                    error_msg6 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
                self.note += error_msg1
                self.note += error_msg2
                self.note += error_msg3
                self.note += error_msg4
                self.note += error_msg5
                self.note += error_msg6
                assert test_status, error_msg1
                assert test_status, error_msg2
                assert test_status, error_msg3
                assert test_status, error_msg4
                assert test_status, error_msg5
                assert test_status, error_msg6
            except:
                errormsg = "Test failed in iteration {}\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                test_status = False
        time.sleep(5)
        assert test_status
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD451_MULTILINK_DISCONNECT_ALL_THE_CONNECTED_DEVICE_FROM_DUT", 'MBDA')
    def test_rnbd_disconnect_all_the_connected_device_from_dut(self):
        error_msg1, error_msg2, error_msg3, error_msg4, error_msg5, error_msg6 = "", "", "", "", "", ""
        test_status = True
        step_result = []
        step_descript = []
        print("{0}Test to verify RNBD Multilink Feature {0}".format('=' * 20))
        print("{0}Test to verify Scan and Connect with 6 Android phones and disconnect all the connected device from DUT{0}".format(
            '=' * 20))
        mobile_to_use = sd.config.mobile_data_config.get(phone_list[0])
        print(mobile_to_use)
        driver = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect = ScanningandConnection(driver)
        bleuartfeature = BLEUARTFeatureSupport(driver)
        rnbdvsphonefeature = RNBDvsPhoneFeatureSupport(driver)
        driver.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        step_result1, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result2, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Baudrate_115200')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        mobile_to_use1 = sd.config.mobile_data_config.get(phone_list[1])
        print(mobile_to_use1)
        # Multiple drivers for mobiles
        driver1 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use1.get(PHONE_UDID_K),
                             mobile_to_use1.get(PLATFORM_NAME_K),
                             mobile_to_use1.get(PLATFORM_VERSION_K), mobile_to_use1.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect1 = ScanningandConnection(driver1)
        bleuartfeature1 = BLEUARTFeatureSupport(driver1)
        rnbdvsphonefeature1 = RNBDvsPhoneFeatureSupport(driver1)
        driver1.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = scanandconnect1.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT and connect")
        scanandconnect1.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = scanandconnect1.verify_dut_name_visibility(dut_friendly_name)
        print("DUT is connected with Phone:")
        assert status, "Unable to scan and connect to DUT"
        time.sleep(2)
        step_result3, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use2 = sd.config.mobile_data_config.get(phone_list[2])
        print(mobile_to_use2)
        # Multiple drivers for mobiles
        driver2 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use2.get(PHONE_UDID_K),
                             mobile_to_use2.get(PLATFORM_NAME_K),
                             mobile_to_use2.get(PLATFORM_VERSION_K), mobile_to_use2.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect2 = ScanningandConnection(driver2)
        bleuartfeature2 = BLEUARTFeatureSupport(driver2)
        rnbdvsphonefeature2 = RNBDvsPhoneFeatureSupport(driver2)
        driver2.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result4, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use3 = sd.config.mobile_data_config.get(phone_list[3])
        print(mobile_to_use3)
        # Multiple drivers for mobiles
        driver3 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use3.get(PHONE_UDID_K),
                             mobile_to_use3.get(PLATFORM_NAME_K),
                             mobile_to_use3.get(PLATFORM_VERSION_K), mobile_to_use3.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect3 = ScanningandConnection(driver3)
        bleuartfeature3 = BLEUARTFeatureSupport(driver3)
        rnbdvsphonefeature3 = RNBDvsPhoneFeatureSupport(driver3)
        driver3.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result5, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use4 = sd.config.mobile_data_config.get(phone_list[4])
        print(mobile_to_use4)
        # Multiple drivers for mobiles
        driver4 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use4.get(PHONE_UDID_K),
                             mobile_to_use4.get(PLATFORM_NAME_K),
                             mobile_to_use4.get(PLATFORM_VERSION_K), mobile_to_use4.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect4 = ScanningandConnection(driver4)
        bleuartfeature4 = BLEUARTFeatureSupport(driver4)
        rnbdvsphonefeature4 = RNBDvsPhoneFeatureSupport(driver4)
        driver4.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result6, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Start_Advertising')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        mobile_to_use5 = sd.config.mobile_data_config.get(phone_list[5])
        print(mobile_to_use5)
        # Multiple drivers for mobiles
        driver5 = BaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                             mobile_to_use5.get(PHONE_UDID_K),
                             mobile_to_use5.get(PLATFORM_NAME_K),
                             mobile_to_use5.get(PLATFORM_VERSION_K), mobile_to_use5.get(DEVICE_NAME_K),
                             sd.config.app_package, sd.config.app_activity, fresh_env=False, remote_appium=False)
        scanandconnect5 = ScanningandConnection(driver5)
        bleuartfeature5 = BLEUARTFeatureSupport(driver5)
        rnbdvsphonefeature5 = RNBDvsPhoneFeatureSupport(driver5)
        driver5.launch_app()
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
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
        step_result7, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Disconnect_Last_Connected_Device')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        status = rnbdvsphonefeature5.verify_scan_page()
        step_result8, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Disconnect_Last_Connected_Device')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        status = rnbdvsphonefeature4.verify_scan_page()
        step_result9, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Disconnect_Last_Connected_Device')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        status = rnbdvsphonefeature3.verify_scan_page()
        step_result10, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Disconnect_Last_Connected_Device')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        status = rnbdvsphonefeature2.verify_scan_page()
        step_result11, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Disconnect_Last_Connected_Device')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        status = rnbdvsphonefeature1.verify_scan_page()
        step_result12, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Disconnect_Last_Connected_Device')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        time.sleep(5)
        status = rnbdvsphonefeature.verify_scan_page()
        time.sleep(10)
        bleuartfeature5.close_mbd_app()
        bleuartfeature4.close_mbd_app()
        bleuartfeature3.close_mbd_app()
        bleuartfeature2.close_mbd_app()
        bleuartfeature1.close_mbd_app()
        bleuartfeature.close_mbd_app()
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step discription of Phone1 for more details\n"
        elif False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step discription of Phone2 for more details\n"
        elif False in step_result3:
            test_status = False
            error_msg3 = "Few of the commands have failed. Please refer step discription of Phone3 for more details\n"
        elif False in step_result4:
            test_status = False
            error_msg4 = "Few of the commands have failed. Please refer step discription of Phone4 for more details\n"
        elif False in step_result5:
            test_status = False
            error_msg5 = "Few of the commands have failed. Please refer step discription of Phone5 for more details\n"
        elif False in step_result6:
            test_status = False
            error_msg6 = "Few of the commands have failed. Please refer step discription of Phone6 for more details\n"
        self.note += error_msg1
        self.note += error_msg2
        self.note += error_msg3
        self.note += error_msg4
        self.note += error_msg5
        self.note += error_msg6
        assert test_status, error_msg1
        assert test_status, error_msg2
        assert test_status, error_msg3
        assert test_status, error_msg4
        assert test_status, error_msg5
        assert test_status, error_msg6
        self.test_result = True




