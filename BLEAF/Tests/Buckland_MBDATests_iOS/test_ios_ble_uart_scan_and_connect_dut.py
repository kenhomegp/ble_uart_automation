import pytest
import time

from ...CommonSupportLib.StationData import stationData

from ...StationConfig import conf_file
sd = stationData()

dut_friendly_name = conf_file.dut_friendly_name

FW_Version = conf_file.FW_Version


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
    app_package = sd.mobile_driver.get_capability('bundleId')

    status = sd.mobile_driver.close_app(app_package)
    time.sleep(5)
    status = sd.mobile_driver.launch_app(app_package)
    print(status)
    time.sleep(2)
    assert status, "Failed to launch application"

    def function_finalizer():
        print("Local function finalizer")
        #print("Close App")
        #status = sd.mobile_driver.close_app(app_package)
        assert status, "Failed to close application"

    request.addfinalizer(function_finalizer)


class TestConnectBLEUart:
    #@pytest.mark.skip("iOS_SCAN_AND_CONNECT", 'MBDA')
    @pytest.mark.test_id("iOS_SCAN_AND_CONNECT", 'MBDA')
    def test_ble_uart_scan_and_connect_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        #status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility('iPhone') #iPhone MBD PERIPHERAL
        assert status, "Unable to scan and connect to DUT"
        #self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_APP_DEVICE_INFO_FW_VERSION_DISPLAY", 'MBDA')
    def test_ble_uart_collect_device_info_ios(self):
        print("{0}Test to verify device firmware version information {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("Click on settings icon")
        status1 = self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        status, msg = self.bleuartfeatureiOS.verify_fw_rev_ios(FW_Version)
        assert status, msg
        self.note += msg
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_SCAN_AND_CONNECT_STRESS_TEST", 'MBDA')
    def test_ble_uart_connection_disconnection_stress_test_ios(self):
        test_status = True
        print("{0}Test to verify device Discovery, connection and disconnection  {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        for i in range(1, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                self.bleuartfeatureiOS.ios_connect_and_disconnect_dut(dut_friendly_name)
                time.sleep(10)
            except:
                errormsg = "Test failed in iteration {}\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                test_status = False
        time.sleep(5)
        assert test_status
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_TEST_TRP", 'MBDA')
    def test_ble_uart_raw_data_trp_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data mode in TRP {0}".format('=' * 20))
        print("Switch to raw data mode [text mode]")
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_raw_data_mode_trp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_TEST_TRCBP", 'MBDA')
    def test_ble_uart_raw_data_trcbp_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data mode in TRCBP {0}".format('=' * 20))
        print("Switch to raw data mode [text mode]")
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        self.bleuartfeatureiOS.click_settings_icon_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_raw_data_mode_trcbp_ios()
        assert mode_set_trcbp, "Raw data, TRCBP is not set accordingly"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_BURST_MODE_SWITCH_TRP", 'MBDA')
    def test_ble_uart_switching_raw_data_to_burst_mode_trp_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data mode in TRP Mode {0}".format('=' * 20))
        print("Switch to raw data mode [text mode]")
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_raw_data_mode_trp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        print("Able to switch to RAW Data mode")
        print("Switch to burst mode")
        self.bleuartfeatureiOS.switch_raw_data_to_burst_mode_ios()
        print("Able to switch to burst mode")
        print("Switch to Raw mode again")
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_raw_data_mode_trp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        print("Able to verify the text mode and burst mode switch")
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_BURST_MODE_SWITCH_TRCBP", 'MBDA')
    def test_ble_uart_switching_raw_data_to_burst_mode_trcbp_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data mode in TRCBP Mode {0}".format('=' * 20))
        print("Switch to raw data mode [text mode]")
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        self.bleuartfeatureiOS.click_settings_icon_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_raw_data_mode_trcbp_ios()
        assert mode_set_trcbp, "Raw data, TRCBP is not set accordingly"
        time.sleep(5)
        print("Able to switch to RAW Data mode")
        print("Switch to burst mode")
        self.bleuartfeatureiOS.switch_raw_data_to_burst_mode_ios()
        print("Able to switch to burst mode")
        print("Switch to Raw mode again")
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_raw_data_mode_trcbp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        print("Able to verify the text mode and burst mode switch")
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_LOOPBACK_TEST_TRP", 'MBDA')
    def test_ble_uart_raw_data_loopbackmode_trp_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data loopback mode test in TRP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.loopback_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trp = self.bleuartfeatureiOS.confirm_raw_data_loopbackmode_trp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        status = self.bleuartfeatureiOS.send_raw_data_loopback_mode_ios()
        assert status, "Test case failed as comparison is not successful"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_LOOPBACK_TEST_TRCBP", 'MBDA')
    def test_ble_uart_raw_data_loopbackmode_trcbp_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data loopback mode test in TRCBP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.loopback_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_raw_data_loopbackmode_trcbp_ios()
        assert mode_set_trcbp, "Raw data, TRCBP is not set accordingly"
        time.sleep(5)
        status = self.bleuartfeatureiOS.send_raw_data_loopback_mode_ios()
        assert status, "Test case failed as comparison is not successful"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_LOOPBACK_TEST_TRP_STRESS_TEST", 'MBDA')
    def test_ble_uart_raw_data_loopbackmode_stresstest_trp_ios(self):
        status = True
        test_status = True
        input_data0 = "RAW DATA TESTS\n"
        input_data1 = "1234567890\n"
        input_data2 = "ABCDEFGHIJKLMNOPQ!@#$%^&*()\n"
        input_data3 = "Areyoulookingforonlinereadingactivities?\
                           Howaboutinteractivepracticeactivitiestargetingspecificreadingskills?\n"
        input_data4 = "BLE UART Feature RAW DATA\n"
        input_list = [input_data0, input_data1, input_data2, input_data3, input_data4]
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("Switch to raw data [text mode] loopback mode in TRP mode - Stress test for multiple iterations")
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.loopback_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trp = self.bleuartfeatureiOS.confirm_raw_data_loopbackmode_trp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        print("Verify the stress tests for 5 iterations")
        for each in input_list:
            try:
                print("Testing the {} input string".format(each))
                status = self.bleuartfeatureiOS.send_raw_data_loopback_mode_stresstest_ios(each)
                assert status, "Test case failed as comparison is not successful"
                time.sleep(5)
            except:
                errormsg = "Test failed for input string {}. Data transfer has failed.\n".format(each)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        assert test_status, self.note
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_LOOPBACK_TEST_TRCBP_STRESS_TEST", 'MBDA')
    def test_ble_uart_raw_data_loopbackmode_stresstest_trcbp_ios(self):
        status = True
        test_status = True
        input_data0 = "RAW DATA TESTS\n"
        input_data1 = "1234567890\n"
        input_data2 = "ABCDEFGHIJKLMNOPQ!@#$%^&*()\n"
        input_data3 = "Areyoulookingforonlinereadingactivities?\
                               Howaboutinteractivepracticeactivitiestargetingspecificreadingskills?\n"
        input_data4 = "BLE UART Feature RAW DATA\n"
        input_list = [input_data0, input_data1, input_data2, input_data3, input_data4]
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("Switch to raw data [text mode] loopback mode in TRCBP mode - Stress test for multiple iterations")
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.loopback_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_raw_data_loopbackmode_trcbp_ios()
        assert mode_set_trcbp, "Raw data, TRCBP is not set accordingly"
        time.sleep(5)
        print("Verify the stress tests for 5 iterations")
        for each in input_list:
            try:
                print("Testing the {} input string".format(each))
                status = self.bleuartfeatureiOS.send_raw_data_loopback_mode_stresstest_ios(each)
                assert status, "Test case failed as comparison is not successful"
                time.sleep(5)
            except:
                errormsg = "Test failed for input string {}. Data transfer has failed.\n".format(each)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        assert test_status, self.note
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_UART_APP_TO_DUT_TEST_TRP", 'MBDA')
    def test_ble_uart_raw_data_uartmode_app_to_dut_trp_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data UART mode APP to DUT test in TRP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.uart_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trp = self.bleuartfeatureiOS.confirm_raw_data_uart_trp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        status = self.bleuartfeatureiOS.send_raw_data_uart_mode_app_to_dut_ios()
        assert status, "Test case failed as comparison is not successful"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_UART_APP_TO_DUT_TEST_TRCBP", 'MBDA')
    def test_ble_uart_raw_data_uartmode_app_to_dut_trcbp_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data UART mode APP to DUT test in TRCBP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.uart_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_raw_data_uart_trcbp_ios()
        assert mode_set_trcbp, "Raw data, TRCBP is not set accordingly"
        time.sleep(5)
        status = self.bleuartfeatureiOS.send_raw_data_uart_mode_app_to_dut_ios()
        assert status, "Test case failed as comparison is not successful"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_UART_DUT_TO_APP_TEST_TRP", 'MBDA')
    def test_ble_uart_raw_data_uartmode_dut_to_app_trp_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data UART mode DUT to APP test in TRP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.uart_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trp = self.bleuartfeatureiOS.confirm_raw_data_uart_trp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        time.sleep(5)
        status = self.bleuartfeatureiOS.send_raw_data_uart_mode_dut_to_app_ios()
        assert status, "Test case failed as comparison is not successful"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_UART_DUT_TO_APP_TEST_TRCBP", 'MBDA')
    def test_ble_uart_raw_data_uartmode_dut_to_app_trcbp_ios(self):
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data UART mode DUT to APP test in TRCBP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.uart_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_raw_data_uart_trcbp_ios()
        assert mode_set_trcbp, "Raw data, TRCBP is not set accordingly"
        time.sleep(5)
        status = self.bleuartfeatureiOS.send_raw_data_uart_mode_dut_to_app_ios()
        assert status, "Test case failed as comparison is not successful"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_UART_APP_TO_DUT_TRP_STRESS_TEST", 'MBDA')
    def test_ble_uart_raw_data_uartmode_app_to_dut_stress_test_trp_ios(self):
        status = True
        test_status = True
        input_data0 = "RAW DATA TESTS\n"
        input_data1 = "1234567890\n"
        input_data2 = "ABCDEFGHIJKLMNOPQ!@#$%^&*()\n"
        input_data3 = "Areyoulookingforonlinereadingactivities?\
                                   Howaboutinteractivepracticeactivitiestargetingspecificreadingskills?\n"
        input_data4 = "BLE UART Feature RAW DATA\n"
        input_list = [input_data0, input_data1, input_data2, input_data3, input_data4]
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data UART mode APP to DUT stress test in TRP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.uart_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trp = self.bleuartfeatureiOS.confirm_raw_data_uart_trp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        print("Verify the stress tests for 5 iterations")
        for each in input_list:
            try:
                print("Testing the {} input string".format(each))
                status = self.bleuartfeatureiOS.send_raw_data_uart_mode_app_to_dut_stress_test_ios(each)
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_UART_APP_TO_DUT_TRCBP_STRESS_TEST", 'MBDA')
    def test_ble_uart_raw_data_uartmode_app_to_dut_stress_test_trcbp_ios(self):
        status = True
        test_status = True
        input_data0 = "RAW DATA TESTS\n"
        input_data1 = "1234567890\n"
        input_data2 = "ABCDEFGHIJKLMNOPQ!@#$%^&*()\n"
        input_data3 = "Areyoulookingforonlinereadingactivities?\
                                       Howaboutinteractivepracticeactivitiestargetingspecificreadingskills?\n"
        input_data4 = "BLE UART Feature RAW DATA\n"
        input_list = [input_data0, input_data1, input_data2, input_data3, input_data4]
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data UART mode APP to DUT stress test in TRCBP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.uart_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_raw_data_uart_trcbp_ios()
        assert mode_set_trcbp, "Raw data, TRCBP is not set accordingly"
        time.sleep(5)
        print("Verify the stress tests for 5 iterations")
        for each in input_list:
            try:
                print("Testing the {} input string".format(each))
                status = self.bleuartfeatureiOS.send_raw_data_uart_mode_app_to_dut_stress_test_ios(each)
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_UART_DUT_TO_APP_TRP_STRESS_TEST", 'MBDA')
    def test_ble_uart_raw_data_uartmode_dut_to_app_stress_test_trp_ios(self):
        status = True
        test_status = True
        input_data0 = "RAW DATA TESTS\n"
        input_data1 = "1234567890\n"
        input_data2 = "ABCDEFGHIJKLMNOPQ!@#$%^&*()\n"
        input_data3 = "Areyoulookingforonlinereadingactivities?\
                                           Howaboutinteractivepracticeactivitiestargetingspecificreadingskills?\n"
        input_data4 = "BLE UART Feature RAW DATA\n"
        input_list = [input_data0, input_data1, input_data2, input_data3, input_data4]
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data UART mode DUT to APP stress test in TRP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.uart_mode_ios()
        time.sleep(10)
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trp = self.bleuartfeatureiOS.confirm_raw_data_uart_trp_ios()
        assert mode_set_trp, "Raw data, TRP is not set accordingly"
        time.sleep(5)
        print("Verify the stress tests for 5 iterations")
        for each in input_list:
            try:
                print("Testing the {} input string".format(each))
                status = self.bleuartfeatureiOS.send_raw_data_uart_mode_dut_to_app_stress_test_ios(each)
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_RAW_DATA_UART_DUT_TO_APP_TRCBP_STRESS_TEST", 'MBDA')
    def test_ble_uart_raw_data_uartmode_dut_to_app_stress_test_trcbp_ios(self):
        status = True
        test_status = True
        input_data0 = "RAW DATA TESTS\n"
        input_data1 = "1234567890\n"
        input_data2 = "ABCDEFGHIJKLMNOPQ!@#$%^&*()\n"
        input_data3 = "Areyoulookingforonlinereadingactivities?\
                                               Howaboutinteractivepracticeactivitiestargetingspecificreadingskills?\n"
        input_data4 = "BLE UART Feature RAW DATA\n"
        input_list = [input_data0, input_data1, input_data2, input_data3, input_data4]
        print("{0}Test to verify device Discovery and connection {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("{0}Test to verify Raw data UART mode DUT to APP stress test in TRCBP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_raw_data_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.click_settings_icon_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.change_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.uart_mode_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_raw_data_uart_trcbp_ios()
        assert mode_set_trcbp, "Raw data, TRCBP is not set accordingly"
        time.sleep(5)
        print("Verify the stress tests for 5 iterations")
        for each in input_list:
            try:
                print("Testing the {} input string".format(each))
                status = self.bleuartfeatureiOS.send_raw_data_uart_mode_dut_to_app_stress_test_ios(each)
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True