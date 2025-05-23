import pytest
import time
from ...CommonSupportLib.StationData import stationData
from ...StationConfig import conf_file
from ...MCP2200.MCP2200 import Mcp2200
sd = stationData()
MCU = Mcp2200()
dut_friendly_name = conf_file.dut_friendly_name
comport = conf_file.com_port
RNBD_FW_Version = conf_file.FW_Version

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
    app_package = sd.mobile_driver.get_capability('appPackage')
    status = sd.mobile_driver.close_app(app_package)
    assert status, "Failed to close application"
    time.sleep(5)
    status = sd.mobile_driver.launch_app(app_package)
    assert status, "Failed to launch application"
    # time.sleep(5)
    # def function_finalizer():
        # print("Local function finalizer")
        # print("Close App")
    # request.addfinalizer(function_finalizer)

class TestRNBD45xFeature:
    @pytest.mark.skip("RNBD_SCAN_AND_CONNECT", 'MBDA')
    def test_rnbd_connect_ble_uart(self):
        print("{0}Test to verify RNBD Device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_SCAN_AND_CONNECT_STRESS_TEST", 'MBDA')
    def test_rnbd_ble_uart_connect_disconnect(self):
        test_status = True
        print("{0}Test to verify RNBD Device Discovery, connection and disconnection  {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_disconnect_dut(dut_friendly_name)
        time.sleep(10)
        for i in range(1, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                self.scanandconnect.scan_and_connect_disconnect_dut_stresstest(dut_friendly_name)
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                test_status = False
        time.sleep(5)
        assert test_status
        #self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_APP_DEVICE_INFO_FW_VERSION_DISPLAY", 'MBDA')
    def test_rnbd_collect_device_info(self):
        print("{0}Test to verify RNBD firmware version information {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        status = self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.bleuartfeature.click_setting_onepluspro()
        else:
            self.bleuartfeature.click_settings_icon()        
        time.sleep(10)
        status, msg = self.scanandconnect.verify_fw_rev(RNBD_FW_Version)
        assert status, msg
        self.note += msg
        #self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_RAW_DATA_UART_APP_TO_DUT_TEST_TRP", 'MBDA')
    def test_rnbd_ble_uart_raw_data_uartmode_app_to_dut(self):
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        self.scanandconnect.verify_raw_data_mode()
        time.sleep(5)
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.bleuartfeature.click_setting_onepluspro()
        else:
            self.bleuartfeature.click_settings_icon()  
        time.sleep(5)
        self.bleuartfeature.change_mode()
        time.sleep(5)
        self.bleuartfeature.uart_mode()
        time.sleep(10)
        self.bleuartfeature.go_back()
        time.sleep(7)
        mode_set_trp = self.scanandconnect.confirm_raw_data_uart_trp()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        status = self.scanandconnect.send_raw_data_uart_mode_app_to_dut()
        assert status, "Test case failed as comparison is not successful"
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_RAW_DATA_UART_DUT_TO_APP_TEST_TRP", 'MBDA')
    def test_rnbd_ble_uart_raw_data_uartmode_dut_to_app(self):
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        self.scanandconnect.verify_raw_data_mode()
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.bleuartfeature.click_setting_onepluspro()
        else:
            self.bleuartfeature.click_settings_icon()  
        time.sleep(5)
        self.bleuartfeature.change_mode()
        time.sleep(5)
        self.bleuartfeature.uart_mode()
        time.sleep(10)
        self.bleuartfeature.go_back()
        time.sleep(5)
        mode_set_trp = self.scanandconnect.confirm_raw_data_uart_trp()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        time.sleep(5)
        status = self.scanandconnect.send_raw_data_uart_mode_dut_to_app()
        assert status, "Test case failed as comparison is not successful"
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_RAW_DATA_UART_APP_TO_DUT_TRP_STRESS_TEST", 'MBDA')
    def test_rnbd_ble_uart_raw_data_uartmode_app_to_dut_stress_test(self):
        status = True
        test_status = True
        input_data0 = "RAW DATA TESTS"
        input_data1 = "1234567890"
        input_data2 = "ABCDEFGHIJKLMNOPQ!@#$%^&*()"
        input_data3 = "Areyoulookingforonlinereadingactivities?\
                                   Howaboutinteractivepracticeactivitiestargetingspecificreadingskills?"
        input_data4 = "BLE UART Feature RAW DATA"
        input_list = [input_data0, input_data1, input_data2, input_data3, input_data4]
        print("{0}Test to verify RNBD Device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        self.scanandconnect.verify_raw_data_mode()
        time.sleep(5)
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.bleuartfeature.click_setting_onepluspro()
        else:
            self.bleuartfeature.click_settings_icon()  
        time.sleep(5)
        self.bleuartfeature.change_mode()
        time.sleep(5)
        self.bleuartfeature.uart_mode()
        time.sleep(10)
        self.bleuartfeature.go_back()
        time.sleep(5)
        mode_set_trp = self.scanandconnect.confirm_raw_data_uart_trp()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        print("Verify the stress tests for 5 iterations")
        for each in input_list:
            try:
                print("Testing the {} input string".format(each))
                status = self.scanandconnect.send_raw_data_uart_mode_app_to_dut_stress_test(each)
                assert status, "Test case failed as comparison is not successful"
                time.sleep(5)
            except:
                errormsg = "Test failed for input string {}. Data transfer has failed.\n".format(each)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        time.sleep(5)
        assert test_status, self.note
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_RAW_DATA_UART_DUT_TO_APP_TRP_STRESS_TEST", 'MBDA')
    def test_rnbd_ble_uart_raw_data_uartmode_dut_to_app_stress_test(self):
        status = True
        test_status = True
        input_data0 = "RAW DATA TESTS"
        input_data1 = "1234567890"
        input_data2 = "ABCDEFGHIJKLMNOPQ!@#$%^&*()"
        input_data3 = "Areyoulookingforonlinereadingactivities?\
                                           Howaboutinteractivepracticeactivitiestargetingspecificreadingskills?"
        input_data4 = "BLE UART Feature RAW DATA"
        input_list = [input_data0, input_data1, input_data2, input_data3, input_data4]
        print("{0}Test to verify RNBD device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        self.scanandconnect.verify_raw_data_mode()
        if sd.platform == 'OnePlus10Pro':
            print("Click on settings icon")
            status1 = self.bleuartfeature.click_setting_onepluspro()
        else:
            self.bleuartfeature.click_settings_icon()  
        time.sleep(5)
        self.bleuartfeature.change_mode()
        time.sleep(5)
        self.bleuartfeature.uart_mode()
        time.sleep(10)
        self.bleuartfeature.go_back()
        time.sleep(5)
        mode_set_trp = self.scanandconnect.confirm_raw_data_uart_trp()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        print("Verify the stress tests for 5 iterations")
        for each in input_list:
            try:
                print("Testing the {} input string".format(each))
                status = self.scanandconnect.send_raw_data_uart_mode_dut_to_app_stress_test(each)
                assert status, "Test case failed as comparison is not successful"
                time.sleep(5)
            except:
                errormsg = "Test failed for input string {}. Data transfer has failed.\n".format(each)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        time.sleep(5)
        assert test_status, self.note
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_DUT_TO_APP_DATA_TRANSFER_TRP_115200", 'MBDA')
    def test_rnbd_uart_mode_dut_to_app_unidirectional_trp_115200(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Set up RNBD DUT for Data transfer")
        step_result = []
        step_descript = []
        test_status = True
        error_msg = ""
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_115200_SET')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify RNBD UART mode unidirectional data transfer - Uplink - TRP mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        print("Initialize COM Port")
        self.rnbdfeature.init_com_port('115200')
        print("Start the Data transfer from DUT side")
        self.rnbdfeature.rnbd_uart_mode_data_transfer('115200')
        time.sleep(10)
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_DUT_TO_APP_DATA_TRANSFER_STRESS_TEST_TRP_115200", 'MBDA')
    def test_rnbd_uart_mode_dut_to_app_unidirectional_stress_test_trp_115200(self):
        test_status = True
        status = True
        error_msg = ""
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Set up RNBD DUT for Data transfer")
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_115200_SET')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify RNBD UART mode unidirectional data transfer - Uplink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.rnbdfeature.init_com_port('115200')
                print("Start the Data transfer from DUT side")
                self.rnbdfeature.rnbd_uart_mode_data_transfer('115200')
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeature.uart_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        assert test_status
        time.sleep(5)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_APP_TO_DUT_DATA_TRANSFER_TRP_115200", 'MBDA')
    def test_rnbd_uart_mode_app_to_dut_unidirectional_trp_115200(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Set up RNBD DUT for Data transfer")
        step_result = []
        step_descript = []
        test_status = True
        error_msg = ""
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_115200_SET')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify RNBD UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('115200')
        print("Start the Data transfer from App side")
        self.rnbdfeature.rnbd_app_uart_mode_data_transfer('115200')
        time.sleep(5)
        status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX_display()
        assert status, msg
        self.note += msg
        time.sleep(5)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_APP_TO_DUT_DATA_TRANSFER_STRESS_TEST_TRP_115200", 'MBDA')
    def test_rnbd_uart_mode_app_to_dut_unidirectional_trp_stress_test_115200(self):
        test_status = True
        status = True
        error_msg = ""
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Set up RNBD DUT for Data transfer")
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_115200_SET')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify RNBD UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.rnbdfeature.init_com_port('115200')
                print("Start the Data transfer from App side")
                self.rnbdfeature.rnbd_app_uart_mode_data_transfer('115200')
                time.sleep(5)
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX_display()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        assert test_status
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_TRP_115200", 'MBDA')
    def test_rnbd_uart_mode_bidirectional_data_transfer_trp_115200(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Set up RNBD DUT for Data transfer")
        step_result = []
        step_descript = []
        test_status = True
        error_msg = ""
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_115200_SET')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP Mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('115200')
        receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer('115200')
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX(receive_str)
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_STRESS_TEST_TRP_115200", 'MBDA')
    def test_rnbd_uart_mode_bidirectional_data_transfer_trp_stress_test_115200(self):
        test_status = True
        status = True
        error_msg = ""
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Set up RNBD DUT for Data transfer")
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_115200_SET')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP mode - Stress Test {0}".format('=' * 10))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.rnbdfeature.init_com_port('115200')
                print("Start the Data transfer from DUT side and the App side at the same time")
                receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer('115200')
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX(receive_str)
                assert status, msg
                self.note += msg
                status, msg = self.bleuartfeature.uart_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        assert test_status
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_DUT_TO_APP_DATA_TRANSFER_TRP_921600", 'MBDA')
    def test_rnbd_uart_mode_dut_to_app_unidirectional_trp_921600(self):
        step_result = []
        step_result1 = []
        step_result2 = []
        step_descript = []
        step_descrip = []
        step_desc = []
        test_status = True
        error_msg = ""
        error_msg1 = ""
        error_msg2 = ""
        print("Set up RNBD DUT for Data transfer with 921600 baud rate")
        print("Change baud rate from 115200 to 921600")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_921600')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_descrip = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600')
        for step_dsc in step_descrip:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify RNBD UART mode unidirectional data transfer - Uplink - TRP mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('921600')
        print("Start the Data transfer from DUT side")
        self.rnbdfeature.rnbd_uart_mode_data_transfer('921600')
        time.sleep(5)
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        print("Change back the baud rate to default 115200")
        step_result2, step_desc = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600_to_115200_CHANGE')
        for step_descp in step_desc:
            self.note += "Command mode results: \n" + str(step_descp) + "\n"
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        if False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg2
        assert test_status, error_msg2
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_DUT_TO_APP_DATA_TRANSFER_STRESS_TEST_TRP_921600", 'MBDA')
    def test_rnbd_uart_mode_dut_to_app_unidirectional_stress_test_trp_921600(self):
        test_status = True
        status = True
        step_result = []
        step_result1 = []
        step_result2 = []
        step_descript = []
        step_descrip = []
        step_desc = []
        error_msg = ""
        error_msg1 = ""
        error_msg2 = ""
        print("Set up RNBD DUT for Data transfer with 921600 baud rate")
        print("Change baud rate from 115200 to 921600")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_921600')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_descrip = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600')
        for step_dsc in step_descrip:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify RNBD UART mode unidirectional data transfer - Uplink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from DUT side")
                self.rnbdfeature.init_com_port('921600')
                print("Start the Data transfer from DUT side")
                self.rnbdfeature.rnbd_uart_mode_data_transfer('921600')
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeature.uart_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        time.sleep(5)
        assert test_status

        print("Change back the baud rate to default 115200")
        step_result2, step_desc = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600_to_115200_CHANGE')
        for step_descp in step_desc:
            self.note += "Command mode results: \n" + str(step_descp) + "\n"
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        if False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg2
        assert test_status, error_msg2
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_APP_TO_DUT_DATA_TRANSFER_TRP_921600", 'MBDA')
    def test_rnbd_uart_mode_app_to_dut_unidirectional_trp_921600(self):
        step_result = []
        step_result1 = []
        step_result2 = []
        step_descript = []
        step_descrip = []
        step_desc = []
        test_status = True
        error_msg = ""
        error_msg1 = ""
        error_msg2 = ""
        print("Set up RNBD DUT for Data transfer with 921600 baud rate")
        print("Change baud rate from 115200 to 921600")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_921600')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_descrip = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600')
        for step_dsc in step_descrip:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify RNBD UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('921600')
        print("Start the Data transfer from DUT side")
        self.rnbdfeature.rnbd_app_uart_mode_data_transfer('921600')
        time.sleep(5)
        status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX_display()
        assert status, msg
        self.note += msg
        print("Change back the baud rate to default 115200")
        step_result2, step_desc = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600_to_115200_CHANGE')
        for step_descp in step_desc:
            self.note += "Command mode results: \n" + str(step_descp) + "\n"
        time.sleep(5)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        if False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg2
        assert test_status, error_msg2
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_APP_TO_DUT_DATA_TRANSFER_STRESS_TEST_TRP_921600", 'MBDA')
    def test_rnbd_uart_mode_app_to_dut_unidirectional_trp_stress_test_921600(self):
        test_status = True
        status = True
        step_result = []
        step_result1 = []
        step_result2 = []
        step_descript = []
        step_descrip = []
        step_desc = []
        error_msg = ""
        error_msg1 = ""
        error_msg2 = ""
        print("Set up RNBD DUT for Data transfer with 921600 baud rate")
        print("Change baud rate from 115200 to 921600")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_921600')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_descrip = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600')
        for step_dsc in step_descrip:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify RNBD UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.rnbdfeature.init_com_port('921600')
                print("Start the Data transfer from DUT side")
                self.rnbdfeature.rnbd_app_uart_mode_data_transfer('921600')
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX_display()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        time.sleep(5)
        assert test_status
        print("Change back the baud rate to default 115200")
        step_result2, step_desc = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600_to_115200_CHANGE')
        for step_descp in step_desc:
            self.note += "Command mode results: \n" + str(step_descp) + "\n"
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        if False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg2
        assert test_status, error_msg2
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_TRP_921600", 'MBDA')
    def test_rnbd_uart_mode_bidirectional_data_transfer_trp_921600(self):
        step_result = []
        step_result1 = []
        step_result2 = []
        step_descript = []
        step_descrip = []
        step_desc = []
        test_status = True
        error_msg = ""
        error_msg1 = ""
        error_msg2 = ""
        print("Set up RNBD DUT for Data transfer with 921600 baud rate")
        print("Change baud rate from 115200 to 921600")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_921600')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_descrip = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600')
        for step_dsc in step_descrip:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP Mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('921600')
        receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer('921600')
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX(receive_str)
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)

        print("Change back the baud rate to default 115200")
        step_result2, step_desc = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600_to_115200_CHANGE')
        for step_descp in step_desc:
            self.note += "Command mode results: \n" + str(step_descp) + "\n"
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        if False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg2
        assert test_status, error_msg2
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_STRESS_TEST_TRP_921600", 'MBDA')
    def test_rnbd_uart_mode_bidirectional_data_transfer_trp_stress_test_921600(self):
        test_status = True
        status = True
        step_result = []
        step_result1 = []
        step_result2 = []
        step_descript = []
        step_descrip = []
        step_desc = []
        error_msg = ""
        error_msg1 = ""
        error_msg2 = ""
        print("Set up RNBD DUT for Data transfer with 921600 baud rate")
        print("Change baud rate from 115200 to 921600")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_921600')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_descrip = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600')
        for step_dsc in step_descrip:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP mode - Stress Test {0}".format(
            '=' * 10))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.rnbdfeature.init_com_port('921600')
                print("Start the Data transfer from DUT side and App side at the same time")
                receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer('921600')
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX(receive_str)
                assert status, msg
                self.note += msg
                status, msg = self.bleuartfeature.uart_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        time.sleep(5)
        assert status
        print("Change back the baud rate to default 115200")
        step_result2, step_desc = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600_to_115200_CHANGE')
        for step_descp in step_desc:
            self.note += "Command mode results: \n" + str(step_descp) + "\n"
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        if False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg2
        assert test_status, error_msg2
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_BLE_UART_OVERNIGHT_CONN_TEST", 'MBDA')
    def test_rnbd_connect_ble_uart_overnight_connection_test(self):
        print("{0}Test to verify overnight stability of RNBD Device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        duration_conn_test = 60 * 480  # Seconds
        t_end = time.time() + duration_conn_test
        while (True):
            print("Check for connection for long hour\n")
            status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
            assert status, "Connection test failed"
            time.sleep(5)
            
            if (time.time() > t_end):
                print("Completed long hour connection test")
                msg = "Connection test verified for time {} seconds".format(duration_conn_test)
                print(msg)
                self.note += msg
                break
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_SCAN_AND_CONNECT_DISCONNECT_OVERNIGHT_TEST", 'MBDA')
    def test_rnbd_overnight_scan_connect_disconnect(self):
        test_status = True
        print("{0}Test to verify ble uart device Discovery, connection and disconnection  {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_disconnect_dut(dut_friendly_name)
        time.sleep(10)
        for i in range(1, 161):
            try:
                print("Overnight Test for 161 iterations, Iteration", i)
                iter_msg = "Overnight Test for Iteration {}\n".format(i)
                self.note += iter_msg
                self.scanandconnect.scan_and_connect_disconnect_dut_stresstest(dut_friendly_name)
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                test_status = False
        time.sleep(5)
        assert test_status
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True


    @pytest.mark.skip("RNBD_UART_MODE_BIDIRECTIONAL_OVERNIGHT_DATA_TRANSFER_TRP_921600", 'MBDA')
    def test_rnbd_uart_mode_bidirectional_data_transfer_overnight_test_921600(self):
        test_status = True
        status = True
        step_result = []
        step_result1 = []
        step_result2 = []
        step_descript = []
        step_descrip = []
        step_desc = []
        error_msg = ""
        error_msg1 = ""
        error_msg2 = ""
        print("Set up RNBD DUT for Data transfer with 921600 baud rate")
        print("Change baud rate from 115200 to 921600")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_921600')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_descrip = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600')
        for step_dsc in step_descrip:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP mode - Stress Test {0}".format(
            '=' * 10))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
		#For RNBD451 please change no of iterations to 501.
		#For RNBD350 please change no of iterations to 170.
        for i in range(i, 210):
            try:
                print("Stress Test for 500 iterations, Iteration", i)
                self.rnbdfeature.init_com_port('921600')
                print("Start the Data transfer from DUT side and App side at the same time")
                receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer('921600')
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX(receive_str)
                assert status, msg
                self.note += msg
                status, msg = self.bleuartfeature.uart_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        time.sleep(5)
        assert status
        print("Change back the baud rate to default 115200")
        step_result2, step_desc = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600_to_115200_CHANGE')
        for step_descp in step_desc:
            self.note += "Command mode results: \n" + str(step_descp) + "\n"
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        if False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg2
        assert test_status, error_msg2
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_UNI-DIRECTIONAL_OVERNIGHT_DATA_TRANSFER_TRP_921600", 'MBDA')
    def test_rnbd_uart_mode_unidirectional_data_transfer_overnight_test_921600(self):
        step_result = []
        step_result1 = []
        step_result2 = []
        step_descript = []
        step_descrip = []
        step_desc = []
        error_msg = ""
        error_msg1 = ""
        error_msg2 = ""
        test_status = True
        status = True
        print("Set up RNBD DUT for Data transfer with 921600 baud rate")
        print("Change baud rate from 115200 to 921600")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_921600')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_descrip = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600')
        for step_dsc in step_descrip:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print(
            "{0}Test to verify RNBD UART mode unidirectional overnight data transfer - Uplink & Downlink - TRP mode {0}".format(
                '=' * 20))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('921600')
        i = 1
        for i in range(i, 9):
            try:
                print("UART mode of unidirectional data transfer - Uplink and Downlink, Iteration", i)
                print("Start the Data transfer from DUT side - Uplink Data Transfer")
                self.rnbdfeature.rnbd_uart_mode_data_transfer('921600')
                time.sleep(5)
                status, msg = self.bleuartfeature.uart_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
                duration_conn_test = 60 * 25  # 1800 Seconds
                t_end = time.time() + duration_conn_test
                print("Wait for 30 mins")
                while (True):
                    if (time.time() > t_end):
                        end_of_test_string = "Waited for {} seconds".format(duration_conn_test)
                        print(end_of_test_string)
                        self.note += end_of_test_string
                        break
                print("Start the Data transfer from APP side - Downlink Data Transfer")
                print("Start the Data transfer from App side")
                self.rnbdfeature.rnbd_app_uart_mode_data_transfer('921600')
                time.sleep(5)
                status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX_display()
                assert status, msg
                self.note += msg
                t_end = time.time() + duration_conn_test
                print("Wait for 30 mins")
                while (True):
                    if (time.time() > t_end):
                        end_of_test_string = "Waited for {} seconds".format(duration_conn_test)
                        print(end_of_test_string)
                        self.note += end_of_test_string
                        break
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        print("Change back the baud rate to default 115200")
        step_result2, step_desc = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600_to_115200_CHANGE')
        for step_descp in step_desc:
            self.note += "Command mode results: \n" + str(step_descp) + "\n"
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        if False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg2
        assert test_status, error_msg2
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_VS_PHONE_SLEEP_MODE_TEST", 'MBDA')
    def test_rnbd_sleep_mode_conn_interval_parameters_uart(self):
        print("{0}Test to RNBD Sleep mode Feature {0}".format('=' * 20))
        print("Set up RNBD DUT for Data transfer")
        step_result = []
        step_descript = []
        step_result1 = []
        step_descript1 = []
        step_result2 = []
        step_descript2 = []
        step_results = []
        step_description = []
        test_status = True
        error_msg = ""
        print("======== Start Sleep Mode Tests ====")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Sleepmode_Enable_Test')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        self.rnbdfeature.WakeupFromSleep(MCU)
        step_results, step_description = self.rnbdfeature.Read_json_file('RNBD_115200_Sleep_Mode')
        for step_dest in step_description:
            self.note += "Command mode results: \n" + str(step_dest) + "\n"
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        time.sleep(10)
        print("{0}Test to verify RNBD UART mode unidirectional data transfer - Uplink - TRP mode {0}".format('=' * 20))
        trp_result = "Uplink - UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('115200')
        print("Start the Data transfer from DUT side")
        self.rnbdfeature.rnbd_uart_mode_data_transfer("115200")
        time.sleep(10)
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)

        print("{0}Test to verify RNBD UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        trp_result = "Downlink - UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('115200')
        print("Start the Data transfer from DUT side")
        self.rnbdfeature.rnbd_app_uart_mode_data_transfer("115200")
        time.sleep(5)
        status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX_display()
        assert status, msg
        self.note += msg
        time.sleep(5)
        print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP Mode {0}".format('=' * 20))
        trp_result = "Bidirectional - UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('115200')
        receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer("115200")
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        print("Wait for 10 mins")
        time.sleep(600)
        step_result1, step_descript1 = self.rnbdfeature.Read_json_file('RNBD_Conn_Interval_Param_Set1')
        for step_desc in step_descript1:
            self.note += "Command mode results: \n" + str(step_desc) + "\n"
        print("Verify the UART mode")
        time.sleep(10)
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        time.sleep(10)
        print("{0}Test to verify RNBD UART mode unidirectional data transfer - Uplink - TRP mode {0}".format('=' * 20))
        trp_result = "Uplink - UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('115200')
        print("Start the Data transfer from DUT side")
        self.rnbdfeature.rnbd_uart_mode_data_transfer("115200")
        time.sleep(10)
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)

        print("{0}Test to verify RNBD UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        trp_result = "Downlink - UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('115200')
        print("Start the Data transfer from DUT side")
        self.rnbdfeature.rnbd_app_uart_mode_data_transfer("115200")
        time.sleep(5)
        status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX_display()
        assert status, msg
        self.note += msg
        time.sleep(5)
        print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP Mode {0}".format('=' * 20))
        trp_result = "Bidirectional - UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('115200')
        receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer("115200")
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        print("Wait for 10 mins")
        time.sleep(600)
        step_result2, step_descript2 = self.rnbdfeature.Read_json_file('RNBD_Sleepmode_Disable_Test')
        for step_descr in step_descript2:
            self.note += "Command mode results: \n" + str(step_descr) + "\n"
        self.rnbdfeature.SleepFromWakeup(MCU)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_CONNECTION_STABILITY_TEST_24HOURS", 'MBDA')
    def test_rnbd_connect_ble_uart_overnight_connection_test_24_hours(self):
        print("{0}Test to verify RNBD Device Discovery and connection stability for 24 hours {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        duration_conn_test = 60 * 1440  # Seconds
        t_end = time.time() + duration_conn_test
        while (True):
            print("Check for connection for long hour\n")
            status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
            assert status, "Connection test failed"
            if (time.time() > t_end):
                print("Completed 24 hours connection test")
                msg = "Connection test verified for time {} seconds".format(duration_conn_test)
                print(msg)
                self.note += msg
                break
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_ADV_OVER_24HOURS_AND_CONNECT", 'MBDA')
    def test_rnbd_connect_ble_uart_overnight_adv_over_24_hours_and_connect(self):
        print("{0}Test to verify RNBD Device Discovery and connection after 24 hours{0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        self.scanandconnect.open_ble_uart_scanner()
        Adv_duration = 60 * 1440  # Seconds
        t_end = time.time() + Adv_duration
        while (True):
            print("Check for RNBD advertising for long hour\n")
            status = self.rnbdfeature.search_for_dut(dut_friendly_name)
            assert status, "Unable to find the dut name"
            if (time.time() > t_end):
                print("Completed long hour advertising test")
                msg = "RNBD advertising verified for 86400 seconds"
                print(msg)
                self.note += msg + "\n"
                break
        time.sleep(5)
        print("Scan for the DUT and connect")
        self.rnbdfeature.connect_ble_uart_dut(dut_friendly_name)
        time.sleep(60)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Connection test failed"
        msg1 = "San and connect successfully after 24 hour of RNBD advertising"
        self.note += msg1 + "\n"
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_STRESS_TEST_24HOURS", 'MBDA')
    def test_rnbd_uart_mode_bidirectional_data_transfer_24_hours_test(self):
        test_status = True
        status = True
        step_result = []
        step_result1 = []
        step_result2 = []
        step_descript = []
        step_descrip = []
        step_desc = []
        error_msg = ""
        error_msg1 = ""
        error_msg2 = ""
        print("Set up RNBD DUT for Data transfer with 921600 baud rate")
        print("Change baud rate from 115200 to 921600")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_921600')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_descrip = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600')
        for step_dsc in step_descrip:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print(
            "{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP mode - Stress Test for 24 hours {0}".format(
                '=' * 10))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i,851):
            try:
                print("Stress Test for Iteration", i)
                self.rnbdfeature.init_com_port('921600')
                print("Start the Data transfer from DUT side and App side at the same time")
                receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer('921600')
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX(receive_str)
                assert status, msg
                self.note += msg
                status, msg = self.bleuartfeature.uart_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        time.sleep(5)
        assert status
        print("Change back the baud rate to default 115200")
        step_result2, step_desc = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600_to_115200_CHANGE')
        for step_descp in step_desc:
            self.note += "Command mode results: \n" + str(step_descp) + "\n"
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        if False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg2
        assert test_status, error_msg2
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_SCAN_AND_CONNECT_STRESS_TEST_24HOURS", 'MBDA')
    def test_rnbd_ble_uart_connect_disconnect_test_24_hours(self):
        test_status = True
        print("{0}Test to verify RNBD Device Discovery, connection and disconnection for 24 hours {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_disconnect_dut(dut_friendly_name)
        time.sleep(10)
        for i in range(1, 412):
            try:
                print("Stress Test for Iteration", i)
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                self.scanandconnect.scan_and_connect_disconnect_dut_stresstest(dut_friendly_name)
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                test_status = False
        time.sleep(5)
        assert test_status
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("RNBD451_vS_PHONE_SLEEP_MODE_CONNECTION_DISCONNECTION_RELIABILITY_TEST", 'MBDA')
    def test_rnbd_sleep_mode_connection_disconnection_reliability_test(self):
        print("{0}Test to RNBD Sleep mode Feature {0}".format('=' * 20))
        print("Set up RNBD DUT for Data transfer")
        test_status = True
        error_msg = ""
        print("======== Start Sleep Mode Tests ====")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Sleepmode_Enable_Test')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        self.rnbdfeature.init_com_port('115200')
        time.sleep(5)
        self.rnbdfeature.WakeupFromSleep()
        time.sleep(5)
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        self.scanandconnect.open_ble_uart_scanner()
        i = 1
        for i in range(i, 201):
            print("############ Sleep mode Stress Test for multiple iterations ############, Iteration", i)
            iter_msg = "Sleep mode Stress Test for Iteration {}\n".format(i)
            self.note += iter_msg
            print("Put the DUT to advertising mode")
            time.sleep(5)
            print("Scan for the DUT and connect")
            self.scanandconnect.click_start_scan()
            time.sleep(45)
            self.scanandconnect.click_cancel_button()
            time.sleep(2)
            self.scanandconnect.search_and_select_dut(dut_friendly_name)
            time.sleep(2)
            status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
            assert status, "Unable to scan and connect to DUT"
            print("Verify the UART mode")
            time.sleep(5)
            self.bleuartfeature.verify_mode_uart()
            time.sleep(3)
            print("Go back to Previous Screen")
            self.bleuartfeature.go_back()
            mode_set_trp = self.bleuartfeature.confirm_uart_mode()
            assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
            time.sleep(10)
            print("{0}Test to verify RNBD UART mode unidirectional data transfer - Uplink - TRP mode {0}".format('=' * 20))
            trp_result = "Uplink - UART Mode, TRP Mode Data Transfer Results \n"
            print(trp_result)
            self.note += trp_result
            time.sleep(5)
            print("Start the Data transfer from DUT side")
            self.rnbdfeature.rnbd_uart_mode_data_transfer("115200")
            time.sleep(10)
            status, msg = self.bleuartfeature.uart_mode_results_RX()
            assert status, msg
            self.note += msg
            time.sleep(5)
            print("{0}Test to verify RNBD UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
            trp_result = "Downlink - UART Mode, TRP Mode Data Transfer Results \n"
            print(trp_result)
            self.note += trp_result
            time.sleep(5)
            print("Start the Data transfer from DUT side")
            self.rnbdfeature.rnbd_app_uart_mode_data_transfer("115200")
            time.sleep(5)
            status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX_display()
            assert status, msg
            self.note += msg
            time.sleep(5)
            print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP Mode {0}".format('=' * 20))
            trp_result = "Bidirectional - UART Mode, TRP Mode Data Transfer Results \n"
            print(trp_result)
            self.note += trp_result
            time.sleep(5)
            receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer("115200")
            print("Message ", receive_str)
            self.note += "UART Bidirectional data transfer test results \n\n"
            time.sleep(5)
            status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX(receive_str)
            assert status, msg
            self.note += msg
            time.sleep(5)
            status, msg = self.bleuartfeature.uart_mode_results_RX()
            assert status, msg
            self.note += msg
            print("Wait for 10 mins")
            msg = "Wait for 10 mins"
            self.note += msg
            time.sleep(600)
            step_result1, step_descript1 = self.rnbdfeature.Read_json_file('RNBD_Conn_Interval_Param_Set1')
            for step_desc in step_descript1:
                self.note += "Command mode results: \n" + str(step_desc) + "\n"
            time.sleep(10)
            print("{0}Test to verify RNBD UART mode unidirectional data transfer after Conn_Interval_Param_Set1 - Uplink - TRP mode {0}".format('=' * 20))
            trp_result = "Uplink - UART Mode, TRP Mode Data Transfer Results \n"
            print(trp_result)
            self.note += trp_result
            time.sleep(5)
            print("Start the Data transfer from DUT side")
            self.rnbdfeature.rnbd_uart_mode_data_transfer("115200")
            time.sleep(10)
            status, msg = self.bleuartfeature.uart_mode_results_RX()
            assert status, msg
            self.note += msg
            time.sleep(15)
            print("{0}Test to verify RNBD UART mode of unidirectional data transfer after Conn_Interval_Param_Set1- Downlink {0}".format('=' * 20))
            trp_result = "Downlink - UART Mode, TRP Mode Data Transfer Results \n"
            print(trp_result)
            self.note += trp_result
            time.sleep(5)
            print("Start the Data transfer from DUT side")
            self.rnbdfeature.rnbd_app_uart_mode_data_transfer("115200")
            time.sleep(5)
            status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX_display()
            assert status, msg
            self.note += msg
            time.sleep(5)
            print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP Mode after Conn_Interval_Param_Set1 {0}".format('=' * 20))
            trp_result = "Bidirectional - UART Mode, TRP Mode Data Transfer Results \n"
            print(trp_result)
            self.note += trp_result
            time.sleep(5)
            receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer("115200")
            print("Message ", receive_str)
            time.sleep(5)
            self.note += "UART Bidirectional data transfer test results \n\n"
            status, msg = self.rnbdfeature.rnbd_uart_mode_results_TX(receive_str)
            assert status, msg
            self.note += msg
            time.sleep(5)
            status, msg = self.bleuartfeature.uart_mode_results_RX()
            assert status, msg
            self.note += msg
            time.sleep(5)
            self.bleuartfeature.go_back()
            self.scanandconnect.verify_scan_page_visiblity()
            time.sleep(60)
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Sleepmode_Disable_Test')
        for step_descr in step_descript:
            self.note += "Command mode results: \n" + str(step_descr) + "\n"
        self.rnbdfeature.SleepFromWakeup()
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD451_vS_PHONE_SLEEP_MODE_CONNECTION_STABILITY_WITH_DIFFERENT_SET_OF_CONNECTION_PARAMETER_TEST", 'MBDA')
    def test_rnbd_sleep_mode_connection_stability_test_for_three_diffrent_connection_parameter_set(self):
        print("{0}Test to RNBD Sleep mode Feature {0}".format('=' * 20))
        print("Set up RNBD DUT for Data transfer")
        test_status = True
        error_msg = ""
        print("======== Start Sleep Mode Tests ====")
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Sleepmode_Enable_command')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        self.rnbdfeature.init_com_port('115200')
        self.rnbdfeature.WakeupFromSleep()
        time.sleep(5)
        # step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Sleepmode_Disable_Test')
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        self.scanandconnect.open_ble_uart_scanner()
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT and connect")
        self.scanandconnect.click_start_scan()
        time.sleep(5)
        self.scanandconnect.click_cancel_button()
        self.scanandconnect.search_and_select_dut(dut_friendly_name)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        step_result1, step_descript1 = self.rnbdfeature.Read_json_file('Sleep_Mode_Conn_Interval_Param_Set1')
        for step_desc in step_descript1:
            self.note += "Command mode results: \n" + str(step_desc) + "\n"
            time.sleep(10)
        print("{0}Test to verify RNBD connection stability with Conn_Interval_Param_Set1 {0}".format('=' * 20))
        duration_conn_test = 60 * 60  # Seconds
        t_end = time.time() + duration_conn_test
        while (True):
            print("Check for connection for 1 hour\n")
            status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
            assert status, "Connection test failed"
            if (time.time() > t_end):
                print("Completed long hour connection test")
                msg = "Connection test verified for time {} seconds".format(duration_conn_test)
                print(msg)
                self.note += msg
                break
        step_result2, step_descript2 = self.rnbdfeature.Read_json_file('Sleep_Mode_Conn_Interval_Param_Set2')
        for step_desc in step_descript2:
            self.note += "Command mode results: \n" + str(step_desc) + "\n"
            time.sleep(10)
        print("{0}Test to verify RNBD connection stability with Conn_Interval_Param_Set2 {0}".format('=' * 20))
        duration_conn_test = 60 * 60  # Seconds
        t_end = time.time() + duration_conn_test
        while (True):
            print("Check for connection for 1 hour\n")
            status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
            assert status, "Connection test failed"
            if (time.time() > t_end):
                print("Completed long hour connection test")
                msg2 = "Connection test verified for time {} seconds".format(duration_conn_test)
                print(msg2)
                self.note += msg2
                break
        step_result3, step_descript3 = self.rnbdfeature.Read_json_file('Sleep_Mode_Conn_Interval_Param_Set3')
        for step_desc in step_descript3:
            self.note += "Command mode results: \n" + str(step_desc) + "\n"
            time.sleep(10)
        print("{0}Test to verify RNBD connection stability with Conn_Interval_Param_Set3 {0}".format('=' * 20))
        duration_conn_test = 60 * 60  # Seconds
        t_end = time.time() + duration_conn_test
        while (True):
            print("Check for connection for 1 hour\n")
            status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
            assert status, "Connection test failed"
            if (time.time() > t_end):
                print("Completed long hour connection test")
                msg3 = "Connection test verified for time {} seconds".format(duration_conn_test)
                print(msg3)
                self.note += msg3
                break
        step_result4, step_descript4 = self.rnbdfeature.Read_json_file('RNBD_Sleepmode_Disable_Test')
        for step_descr in step_descript4:
            self.note += "Command mode results: \n" + str(step_descr) + "\n"
        self.rnbdfeature.SleepFromWakeup()
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result2:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result3:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result4:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more details.\n"
            self.note += error_msg
        assert test_status, error_msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True