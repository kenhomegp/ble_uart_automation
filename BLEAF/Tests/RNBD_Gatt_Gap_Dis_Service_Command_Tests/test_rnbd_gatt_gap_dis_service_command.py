import time
import pytest
from ...CommonSupportLib.StationData import stationData
from ...StationConfig import conf_file
sd = stationData()

dut_friendly_name = conf_file.dut_friendly_name
com_port = conf_file.com_port
baudrate = conf_file.baud_rate
set_firmware_version = '0.99'
set_hardware_version = '2.1'
set_model_string = 'RNBD45x'
set_manufacturer_name = 'MCHP'
set_software_revision_version = '1.0.1'
set_serial_number = '123456789'
set_appearance = '40 03'
connection_log = '%CONNECT'

@pytest.fixture(scope="function", autouse=True)
def local_function_fixture(request):
    print("Local function fixture")
    print("Launch LightBlue Application")
    app_package = sd.mobile_driver.get_capability('appPackage')
    status = sd.mobile_driver.close_app(app_package)
    assert status, "Failed to close application"
    time.sleep(5)
    status = sd.mobile_driver.launch_app(app_package)
    assert status, "Failed to launch application"
    # def function_finalizer():
        # print("Local function finalizer")
        # print("Close App")
        # assert status, "Failed to close application"
    # request.addfinalizer(function_finalizer)

class TestPhonevsRNBD45xFeature:
    @pytest.mark.skip("RNBD_SET_FIRMWARE_VERSION_TEST", 'MBDA')
    def test_RNBD_set_firmware_version(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_Firmware_Version_Test')
        for step_des in step_descript:
            self.note += "Command mode results \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Set Firmware Version {0}".format('=' * 20))
        print("Verify LightBlue App is open")
        app_open = self.rnbdvsphonefeature.verify_lightblue_app_open()
        assert app_open, "Failed to open LightBlue Application"
        print("Scan for the DUT and connect")
        self.rnbdvsphonefeature.lightblue_scan_and_connect_dut(dut_friendly_name)
        status = self.rnbdvsphonefeature.verify_rnbd_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        status, msg = self.rnbdvsphonefeature.read_fw_information(set_firmware_version)
        assert status, msg
        time.sleep(5)
        self.note += "\n" + msg + "\n"
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        self.rnbdvsphonefeature.close_lightblue_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        assert test_status, error_msg
        self.test_result = True

    @pytest.mark.skip("RNBD_SET_HARDWARE_VERSION_TEST", 'MBDA')
    def test_RNBD_set_hardware_version(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_Hardware_Version_Test')
        for step_des in step_descript:
            self.note += "Command mode results \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Set Hardware Version {0}".format('=' * 20))
        print("Verify LightBlue App is open")
        app_open = self.rnbdvsphonefeature.verify_lightblue_app_open()
        assert app_open, "Failed to open LightBlue Application"
        print("Scan for the DUT and connect")
        self.rnbdvsphonefeature.lightblue_scan_and_connect_dut(dut_friendly_name)
        status = self.rnbdvsphonefeature.verify_rnbd_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        print("Read Hardware version in Device Info service")
        status, msg = self.rnbdvsphonefeature.read_hw_information(set_hardware_version)
        assert status, msg
        self.note += "\n" + msg + "\n"
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        assert test_status, error_msg
        self.rnbdvsphonefeature.close_lightblue_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        self.test_result = True

    @pytest.mark.skip("RNBD_SET_MODEL_STRING_TEST", 'MBDA')
    def test_RNBD_set_model_string_version(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_Model_String_Test')
        for step_des in step_descript:
            self.note += "Command mode results \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Set model string {0}".format('=' * 20))
        print("Verify LightBlue App is open")
        app_open = self.rnbdvsphonefeature.verify_lightblue_app_open()
        assert app_open, "Failed to open LightBlue Application"
        print("Scan for the DUT and connect")
        self.rnbdvsphonefeature.lightblue_scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        status = self.rnbdvsphonefeature.verify_rnbd_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        # time.sleep(5)
        print("Read model string in Device Info service")
        status, msg = self.rnbdvsphonefeature.read_model_string(set_model_string)
        assert status, msg
        self.note += "\n" + msg + "\n"
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        assert test_status, error_msg
        self.rnbdvsphonefeature.close_lightblue_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        self.test_result = True

    @pytest.mark.skip("RNBD_SET_MANUFACTURER_NAME_TEST", 'MBDA')
    def test_RNBD_set_manufacuture_name_version(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_Manufacturer_Name_Test')
        for step_des in step_descript:
            self.note += "Command mode results \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Set manufacturer name {0}".format('=' * 20))
        print("Verify LightBlue App is open")
        app_open = self.rnbdvsphonefeature.verify_lightblue_app_open()
        assert app_open, "Failed to open LightBlue Application"
        print("Scan for the DUT and connect")
        self.rnbdvsphonefeature.lightblue_scan_and_connect_dut(dut_friendly_name)
        status = self.rnbdvsphonefeature.verify_rnbd_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        print("Read Manufacturer name in Device Info service")
        status, msg = self.rnbdvsphonefeature.read_manufacturer_name(set_manufacturer_name)
        assert status, msg
        self.note += "\n" + msg + "\n"
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        assert test_status, error_msg
        self.rnbdvsphonefeature.close_lightblue_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        self.test_result = True

    @pytest.mark.skip("RNBD_SET_SOFTWARE_REVISION_VERSION_TEST", 'MBDA')
    def test_RNBD_set_software_revision_version(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_Software_Revision_Version_Test')
        for step_des in step_descript:
            self.note += "Command mode results \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Set Software revision string {0}".format('=' * 20))
        print("Verify LightBlue App is open")
        app_open = self.rnbdvsphonefeature.verify_lightblue_app_open()
        assert app_open, "Failed to open LightBlue Application"
        print("Scan for the DUT and connect")
        self.rnbdvsphonefeature.lightblue_scan_and_connect_dut(dut_friendly_name)
        status = self.rnbdvsphonefeature.verify_rnbd_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        print("Read Software Revsion string")
        status, msg = self.rnbdvsphonefeature.read_software_revision_version(set_software_revision_version)
        assert status, msg
        self.note += "\n" + msg + "\n"
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        assert test_status, error_msg
        self.rnbdvsphonefeature.close_lightblue_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        self.test_result = True

    @pytest.mark.skip("RNBD_SET_SERIAL_NUMBER_TEST", 'MBDA')
    def test_RNBD_set_serial_number(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_Serial_Number_Test')
        for step_des in step_descript:
            self.note += "Command mode results \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Set serial number {0}".format('=' * 20))
        print("Verify LightBlue App is open")
        app_open = self.rnbdvsphonefeature.verify_lightblue_app_open()
        assert app_open, "Failed to open LightBlue Application"
        print("Scan for the DUT and connect")
        self.rnbdvsphonefeature.lightblue_scan_and_connect_dut(dut_friendly_name)
        status = self.rnbdvsphonefeature.verify_rnbd_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        print("Read Manufacturer name in Device Info service")
        status, msg = self.rnbdvsphonefeature.read_serial_number(set_serial_number)
        assert status, msg
        self.note += "\n" + msg + "\n"
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        assert test_status, error_msg
        self.rnbdvsphonefeature.close_lightblue_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        self.test_result = True

    @pytest.mark.skip("RNBD_SET_APPEARANCE_TEST", 'MBDA')
    def test_RNBD_set_appearance(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_Appearance_Test')
        for step_des in step_descript:
            self.note += "Command mode results \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Set appearance {0}".format('=' * 20))
        print("Verify LightBlue App is open")
        app_open = self.rnbdvsphonefeature.verify_lightblue_app_open()
        assert app_open, "Failed to open LightBlue Application"
        print("Scan for the DUT and connect")
        self.rnbdvsphonefeature.lightblue_scan_and_connect_dut(dut_friendly_name)
        status = self.rnbdvsphonefeature.verify_rnbd_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        print("Read Appearance from Generic Access")
        status, msg = self.rnbdvsphonefeature.read_appearance(set_appearance)
        assert status, msg
        self.note += "\n" + msg + "\n"
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        assert test_status, error_msg
        self.rnbdvsphonefeature.close_lightblue_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        self.test_result = True