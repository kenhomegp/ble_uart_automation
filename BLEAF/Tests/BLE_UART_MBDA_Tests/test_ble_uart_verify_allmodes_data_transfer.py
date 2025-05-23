import pytest
import time
from ...CommonSupportLib.StationData import stationData
from ...StationConfig import conf_file
sd = stationData()
dut_friendly_name = conf_file.dut_friendly_name

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
    time.sleep(5)
    def function_finalizer():
        print("Local function finalizer")
    request.addfinalizer(function_finalizer)

class TestBLEUartVerifyAllModes:
    @pytest.mark.test_id("CHECKSUM_MODE_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_checksum_mode_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in checksum mode (TRCBP) {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_checksum()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_checksum_mode_trcbp()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.checksum_mode_data_transfer()
        status, msg = self.bleuartfeature.checksum_mode_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("CHECKSUM_MODE_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_checksum_mode_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in checksum mode (TRP) {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_checksum()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_checksum_mode()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.checksum_mode_data_transfer()
        status, msg = self.bleuartfeature.checksum_mode_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("CHECKSUM_MODE_STRESS_TEST_TRP", 'MBDA')
    def test_ble_uart_checksum_mode_stress_test_trp(self):
        status = True
        msg = ""
        test_status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in checksum mode (TRP) multiple times{0}".format('=' * 15))
        self.bleuartfeature.verify_mode_checksum()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_checksum_mode()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeature.checksum_mode_data_transfer()
                status, msg = self.bleuartfeature.checksum_mode_results()
                assert status, msg
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        assert test_status, self.note
        self.test_result = True

    @pytest.mark.test_id("CHECKSUM_MODE_STRESS_TEST_TRCBP", 'MBDA')
    def test_ble_uart_checksum_mode_stress_test_trcbp(self):
        status = True
        msg = ""
        test_status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in checksum mode (TRCBP) multiple times{0}".format('=' * 15))
        self.bleuartfeature.verify_mode_checksum()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_checksum_mode_trcbp()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeature.checksum_mode_data_transfer()
                status, msg = self.bleuartfeature.checksum_mode_results()
                assert status, msg
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        assert test_status, self.note
        self.test_result = True

    @pytest.mark.test_id("LOOPBACK_MODE_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_loopback_mode_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        time.sleep(5)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("LOOPBACK_MODE_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_loopback_mode_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        time.sleep(5)
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("LOOPBACK_MODE_STRESS_TEST_TRP", 'MBDA')
    def test_ble_uart_loopback_mode_stresstest_trp(self):
        status = True
        test_status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode multiple times {0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        time.sleep(5)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeature.loopback_mode_data_transfer()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeature.loopback_mode_results_TX()
                assert status, msg
                self.note += msg
                status, msg = self.bleuartfeature.loopback_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        assert test_status, self.note
        self.test_result = True

    @pytest.mark.test_id("LOOPBACK_MODE_STRESS_TEST_TRCBP", 'MBDA')
    def test_ble_uart_loopback_mode_stresstest_trcbp(self):
        status = True
        test_status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode multiple times {0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        time.sleep(5)
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeature.loopback_mode_data_transfer()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeature.loopback_mode_results_TX()
                assert status, msg
                self.note += msg
                status, msg = self.bleuartfeature.loopback_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        assert test_status, self.note
        self.test_result = True

    @pytest.mark.test_id("FIXED_PATTERN_MODE_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_fixed_pattern_mode_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the Fixed Pattern mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in Fixed Pattern mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_fixed_pattern()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_fixed_pattern_mode()
        assert mode_set_trp, "Fixed Pattern Mode, TRP and 500K not set accordingly"
        trp_result = "Fixed Pattern Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.fixed_pattern_mode_data_transfer()
        status, msg = self.bleuartfeature.fixed_pattern_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("FIXED_PATTERN_MODE_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_fixed_pattern_mode_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the Fixed Pattern mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in Fixed Pattern mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_fixed_pattern()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_fixed_pattern_mode_trcbp()
        assert mode_set_trcbp, "Fixed Pattern mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Fixed Pattern Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.fixed_pattern_mode_data_transfer()
        status, msg = self.bleuartfeature.fixed_pattern_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("FIXED_PATTERN_STRESS_TEST_TRP", 'MBDA')
    def test_ble_uart_change_fixed_pattern_mode_stresstest_trp(self):
        test_status = True
        status = True
        print("{0}Test to verify different modes of data transfer multiple times {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the Fixed Pattern mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in Fixed Pattern mode multiple times {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_fixed_pattern()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_fixed_pattern_mode()
        assert mode_set_trp, "Fixed Pattern Mode, TRP and 500K not set accordingly"
        trp_result = "Fixed Pattern Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeature.fixed_pattern_mode_data_transfer()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeature.fixed_pattern_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        assert test_status, self.note
        self.test_result = True

    @pytest.mark.test_id("FIXED_PATTERN_STRESS_TEST_TRCBP", 'MBDA')
    def test_ble_uart_change_fixed_pattern_mode_stresstest_trcbp(self):
        test_status = True
        status = True
        print("{0}Test to verify different modes of data transfer multiple times {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the Fixed Pattern mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in Fixed Pattern mode multiple times {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_fixed_pattern()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_fixed_pattern_mode_trcbp()
        assert mode_set_trcbp, "Fixed Pattern mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Fixed Pattern Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeature.fixed_pattern_mode_data_transfer()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeature.fixed_pattern_mode_results_RX()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        assert test_status, self.note
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_DUT_TO_APP_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_dut_to_app_uart_mode_unidirectional_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode unidirectional data transfer - Uplink - TRP modes {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeature.dut_uart_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_DUT_TO_APP_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_dut_to_app_uart_mode_unidirectional_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode unidirectional data transfer - Uplink - TRCBP modes {0}".format(
            '=' * 20))
        self.bleuartfeature.verify_mode_uart()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_trcbp()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeature.dut_uart_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_DUT_TO_APP_DATA_TRANSFER_STRESS_TEST_TRP", 'MBDA')
    def test_ble_uart_dut_to_app_uart_mode_unidirectional_stress_test_trp(self):
        test_status = True
        status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode unidirectional data transfer - Uplink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from DUT side")
                self.bleuartfeature.dut_uart_mode_data_transfer()
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
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_DUT_TO_APP_DATA_TRANSFER_STRESS_TEST_TRCBP", 'MBDA')
    def test_ble_uart_dut_to_app_uart_mode_unidirectional_stress_test_trcbp(self):
        test_status = True
        status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode unidirectional data transfer - Uplink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_trcbp()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from DUT side")
                self.bleuartfeature.dut_uart_mode_data_transfer()
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
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_APP_TO_DUT_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_unidirectional_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        print("Start the Data transfer from APP side")
        self.bleuartfeature.app_uart_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.uart_mode_results_TX_display()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_APP_TO_DUT_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_unidirectional_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_trcbp()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        print("Start the Data transfer from APP side")
        self.bleuartfeature.app_uart_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.uart_mode_results_TX_display()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_APP_TO_DUT_DATA_TRANSFER_STRESS_TEST_TRP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_unidirectional_trp_stress_test(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from APP side")
                self.bleuartfeature.app_uart_mode_data_transfer()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeature.uart_mode_results_TX_display()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_APP_TO_DUT_DATA_TRANSFER_STRESS_TEST_TRCBP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_unidirectional_trcbp_stress_test(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_trcbp()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from APP side")
                self.bleuartfeature.app_uart_mode_data_transfer()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeature.uart_mode_results_TX_display()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("WRITE_WITH_RESPONSE_CHECKSUM_MODE_TRP", 'MBDA')
    def test_ble_uart_verify_checksum_write_with_response_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print(
            "{0}Test to verify checksum mode of data transfer by enabling write with response-TRP {0}".format('=' * 10))
        self.bleuartfeature.verify_mode_checksum()
        self.bleuartfeature.enable_write_with_response()
        time.sleep(5)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_checksum_mode()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode, Write With Response Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.checksum_mode_data_transfer()
        # Adding delay since write with reponse takes more to complete data transfer
        time.sleep(100)
        status, msg = self.bleuartfeature.checksum_mode_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("WRITE_WITH_RESPONSE_CHECKSUM_MODE_TRCBP", 'MBDA')
    def test_ble_uart_verify_checksum_write_with_response_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print(
            "{0}Test to verify checksum mode of data transfer by enabling write with response-TRCBP {0}".format(
                '=' * 10))
        self.bleuartfeature.verify_mode_checksum()
        self.bleuartfeature.enable_write_with_response()
        time.sleep(5)
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_checksum_mode_trcbp()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode, Write With Response Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.checksum_mode_data_transfer()
        # Adding delay since write with reponse takes more to complete data transfer
        time.sleep(100)
        status, msg = self.bleuartfeature.checksum_mode_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("WRITE_WITH_RESPONSE_LOOPBACK_MODE_TRP", 'MBDA')
    def test_ble_uart_verify_loopback_write_with_response_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode - Write with Response - TRP {0}".format('=' * 10))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        time.sleep(5)
        self.bleuartfeature.enable_write_with_response()
        time.sleep(5)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode, Write with Response, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        # Adding delay since write with reponse takes more to complete data transfer
        time.sleep(100)
        status, msg = self.bleuartfeature.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("WRITE_WITH_RESPONSE_LOOPBACK_MODE_TRCBP", 'MBDA')
    def test_ble_uart_verify_loopback_write_with_response_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode - Write with Response - TRCBP {0}".format(
            '=' * 10))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        time.sleep(5)
        self.bleuartfeature.enable_write_with_response()
        time.sleep(5)
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode, Write with Response, TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        # Adding delay since write with reponse takes more to complete data transfer
        time.sleep(100)
        status, msg = self.bleuartfeature.loopback_mode_results_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_results_RX()
        assert status, msg
        self.note += msg
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("WRITE_WITH_RESPONSE_FIXED_PATTERN_MODE_TRP", 'MBDA')
    def test_ble_uart_verify_fixed_pattern_write_with_response_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the Fixed Pattern mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in  Fixed Pattern mode-Write with Response-TRP {0}".format('=' * 10))
        self.bleuartfeature.verify_mode_fixed_pattern()
        time.sleep(5)
        self.bleuartfeature.enable_write_with_response()
        time.sleep(5)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_fixed_pattern_mode()
        assert mode_set_trp, "Fixed Pattern Mode, TRP and 500K not set accordingly"
        trp_result = "Fixed Pattern Mode, Write with Response, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.fixed_pattern_mode_data_transfer()
        status, msg = self.bleuartfeature.fixed_pattern_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("WRITE_WITH_RESPONSE_FIXED_PATTERN_MODE_TRCBP", 'MBDA')
    def test_ble_uart_verify_fixed_pattern_write_with_response_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the Fixed Pattern mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in  Fixed Pattern mode-Write with Response-TRCBP {0}".format('=' * 10))
        self.bleuartfeature.verify_mode_fixed_pattern()
        time.sleep(5)
        self.bleuartfeature.enable_write_with_response()
        time.sleep(5)
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_fixed_pattern_mode_trcbp()
        assert mode_set_trcbp, "Fixed Pattern mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Fixed Pattern Mode, Write with Response, TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.fixed_pattern_mode_data_transfer()
        status, msg = self.bleuartfeature.fixed_pattern_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_bidirectional_uart_mode_data_transfer_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in UART Mode in TRP Mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        receive_str = self.bleuartfeature.verify_mode_uart_birectional_data_transfer()
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.bleuartfeature.uart_mode_results_TX(receive_str)
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_bidirectional_uart_mode_data_transfer_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in UART Mode in TRCBP Mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_trcbp()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        receive_str = self.bleuartfeature.verify_mode_uart_birectional_data_transfer()
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.bleuartfeature.uart_mode_results_TX(receive_str)
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_TRP_STRESS_TEST", 'MBDA')
    def test_ble_uart_bidirectional_uart_mode_data_transfer_trp_stress_test(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in UART Mode in TRP modes - Stress Test {0}".format(
            '=' * 10))
        self.bleuartfeature.verify_mode_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from DUT side")
                receive_str = self.bleuartfeature.verify_mode_uart_birectional_data_transfer()
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status, msg = self.bleuartfeature.uart_mode_results_TX(receive_str)
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
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_TRCBP_STRESS_TEST", 'MBDA')
    def test_ble_uart_bidirectional_uart_mode_data_transfer_trcbp_stress_test(self):
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
            "{0}Test to verify bidirectional data transfer in UART Mode in TRCBP modes - Stress Test {0}".format(
                '=' * 10))
        self.bleuartfeature.verify_mode_uart()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_trcbp()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from DUT side")
                receive_str = self.bleuartfeature.verify_mode_uart_birectional_data_transfer()
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status, msg = self.bleuartfeature.uart_mode_results_TX(receive_str)
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
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("WRITE_WITH_RESPONSE_UART_MODE_DUT_TO_APP_TRP", 'MBDA')
    def test_ble_uart_dut_to_app_uart_mode_write_with_response_trp(self):
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
            "{0}Test to verify UART mode unidirectional data transfer-Uplink-Write with Response-TRP modes {0}".format(
                '=' * 6))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(5)
        self.bleuartfeature.enable_write_with_response()
        time.sleep(5)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        print("Initialize COM Port")
        self.bleuartfeature.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeature.dut_uart_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("WRITE_WITH_RESPONSE_UART_MODE_DUT_TO_APP_TRCBP", 'MBDA')
    def test_ble_uart_dut_to_app_uart_mode_write_with_response_trcbp(self):
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
            "{0}Test to verify UART mode unidirectional data transfer-Uplink-Write with Response-TRCBP modes {0}".format(
                '=' * 6))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(5)
        self.bleuartfeature.enable_write_with_response()
        time.sleep(5)
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_trcbp()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        print("Initialize COM Port")
        self.bleuartfeature.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeature.dut_uart_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.uart_mode_results_RX()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("WRITE_WITH_RESPONSE_UART_MODE_APP_TO_DUT_TRP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_write_with_response_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode of unidirectional data transfer-Downlink-Write with Response-TRP {0}".format(
            '=' * 6))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(5)
        self.bleuartfeature.enable_write_with_response()
        time.sleep(5)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        print("Initialize COM Port")
        self.bleuartfeature.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeature.app_uart_mode_data_transfer()
        # Adding delay since write with reponse takes more to complete data transfer
        time.sleep(100)
        status, msg = self.bleuartfeature.uart_mode_results_TX_display()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("WRITE_WITH_RESPONSE_UART_MODE_APP_TO_DUT_TRCBP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_write_with_response_trcbp(self):
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
            "{0}Test to verify UART mode of unidirectional data transfer-Downlink-Write with Response-TRCBP{0}".format(
                '=' * 6))
        self.bleuartfeature.verify_mode_uart()
        time.sleep(5)
        self.bleuartfeature.enable_write_with_response()
        time.sleep(5)
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_trcbp()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        print("Initialize COM Port")
        self.bleuartfeature.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeature.app_uart_mode_data_transfer()
        # Adding delay since write with reponse takes more to complete data transfer
        time.sleep(100)
        status, msg = self.bleuartfeature.uart_mode_results_TX_display()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("CHECKSUM_MODE_STOP_DATA_TRANSFER_TRP", 'MBDA')
    def test_verify_mode_checksum_stop_data_transfer_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify STOP data transfer in checksum mode (TRP) {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_checksum()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_checksum_mode()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.start_stop_data_transfer()
        status, msg = self.bleuartfeature.stop_data_transfer_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("CHECKSUM_MODE_STOP_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_verify_mode_checksum_stop_data_transfer_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify STOP data transfer in checksum mode (TRCBP) {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_checksum()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_checksum_mode_trcbp()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.start_stop_data_transfer()
        status, msg = self.bleuartfeature.stop_data_transfer_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("LOOPBACK_MODE_STOP_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_loopback_mode_stop_data_transfer_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify stop data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        time.sleep(5)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.start_stop_data_transfer()
        status, msg = self.bleuartfeature.stop_data_transfer_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("LOOPBACK_MODE_STOP_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_loopback_mode_stop_data_transfer_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify stop data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        time.sleep(5)
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.start_stop_data_transfer()
        status, msg = self.bleuartfeature.stop_data_transfer_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("FIXED_PATTERN_MODE_STOP_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_fixed_pattern_mode_stop_data_transfer_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the Fixed Pattern mode")
        time.sleep(10)
        print("{0}Test to verify stop data transfer in Fixed Pattern mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_fixed_pattern()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_fixed_pattern_mode()
        assert mode_set_trp, "Fixed Pattern Mode, TRP and 500K not set accordingly"
        trp_result = "Fixed Pattern Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.start_stop_data_transfer()
        status, msg = self.bleuartfeature.stop_data_transfer_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("FIXED_PATTERN_MODE_STOP_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_fixed_pattern_mode_stop_data_transfer_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the Fixed Pattern mode")
        time.sleep(10)
        print("{0}Test to verify stop data transfer in Fixed Pattern mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_fixed_pattern()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_fixed_pattern_mode_trcbp()
        assert mode_set_trcbp, "Fixed Pattern mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Fixed Pattern Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.start_stop_data_transfer()
        status, msg = self.bleuartfeature.stop_data_transfer_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_APP_TO_DUT_STOP_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_stop_data_transfer_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify stop data transfer in UART mode - Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        print("Initialize COM Port")
        self.bleuartfeature.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeature.set_uart_mode()
        self.bleuartfeature.start_stop_data_transfer()
        status, msg = self.bleuartfeature.stop_data_transfer_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_APP_TO_DUT_STOP_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_stop_data_transfer_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify stop data transfer in UART mode - Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_trcbp()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        print("Initialize COM Port")
        self.bleuartfeature.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeature.set_uart_mode()
        self.bleuartfeature.start_stop_data_transfer()
        status, msg = self.bleuartfeature.stop_data_transfer_results()
        assert status, msg
        self.note += msg
        time.sleep(5)
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("KILL_MBD_APP_DATA_TRANSFER_CHECKSUM_MODE_TRP", 'MBDA')
    def test_ble_uart_checksum_mode_trp_kill_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in Checksum Mode{0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify verify Kill MBD APP while data transfer in checksum mode (TRP) {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_checksum()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_checksum_mode()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.data_transfer_START_kill_mbd_app()
        time.sleep(1)
        # self.bleuartfeature.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.scanandconnect.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("KILL_MBD_APP_DATA_TRANSFER_CHECKSUM_MODE_TRCBP", 'MBDA')
    def test_ble_uart_checksum_mode_trcbp_kill_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in Checksum Mode{0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify verify Kill MBD APP while data transfer in checksum mode (TRP and TRCBP) {0}".format(
            '=' * 20))
        self.bleuartfeature.verify_mode_checksum()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_checksum_mode_trcbp()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.data_transfer_START_kill_mbd_app()
        time.sleep(1)
        # self.bleuartfeature.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.scanandconnect.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("KILL_MBD_APP_DATA_TRANSFER_LOOPBACK_MODE_TRP", 'MBDA')
    def test_ble_uart_loopback_mode_trp_kill_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in loopback Mode{0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify verify Kill MBD APP while data transfer in loopback mode (TRP and TRCBP) {0}".format(
            '=' * 20))
        self.bleuartfeature.verify_mode_loopback()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_loopback_mode()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.data_transfer_START_kill_mbd_app()
        time.sleep(1)
        # self.bleuartfeature.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.scanandconnect.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("KILL_MBD_APP_DATA_TRANSFER_LOOPBACK_MODE_TRCBP", 'MBDA')
    def test_ble_uart_loopback_mode_trcbp_kill_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in loopback Mode{0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify verify Kill MBD APP while data transfer in loopback mode (TRCBP) {0}".format(
            '=' * 20))
        self.bleuartfeature.verify_mode_loopback()

        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.data_transfer_START_kill_mbd_app()
        time.sleep(1)
        # self.bleuartfeature.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.scanandconnect.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("KILL_MBD_APP_DATA_TRANSFER_UART_APP_TO_DUT_TRP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_trp_kill_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in UART Mode App to Dut{0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify Kill MBD APP while data transfer in UART mode App to Dut (TRP) {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_uart_mode()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.data_transfer_START_kill_mbd_app()
        time.sleep(1)
        # self.bleuartfeature.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.scanandconnect.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("KILL_MBD_APP_DATA_TRANSFER_UART_APP_TO_DUT_TRCBP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_trcbp_kill_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in UART Mode App to Dut{0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify Kill MBD APP while data transfer in UART mode App to Dut (TRCBP) {0}".format(
            '=' * 20))
        self.bleuartfeature.verify_mode_uart()

        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_trcbp()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.data_transfer_START_kill_mbd_app()
        time.sleep(1)
        # self.bleuartfeature.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.scanandconnect.verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("CHECKSUM_MODE_STOP_DATA_TRANSFER_TRP_STRESS_TEST", 'MBDA')
    def test_verify_mode_checksum_stop_data_transfer_stress_test_trp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify STOP data transfer  in checksum mode (TRP) for multiple times{0}".format('=' * 20))
        self.bleuartfeature.verify_mode_checksum()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_checksum_mode()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 6):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeature.start_stop_data_transfer()
                status, msg = self.bleuartfeature.stop_data_transfer_results()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}.  stop Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("CHECKSUM_MODE_STOP_DATA_TRANSFER_TRCBP_STRESS_TEST", 'MBDA')
    def test_verify_mode_checksum_stop_data_transfer_stress_test_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify STOP data transfer  in checksum mode (TRCBP) for multiple times{0}".format(
            '=' * 20))
        self.bleuartfeature.verify_mode_checksum()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_checksum_mode_trcbp()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        i = 1
        for i in range(i, 6):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeature.start_stop_data_transfer()
                status, msg = self.bleuartfeature.stop_data_transfer_results()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}.  stop Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("LOOPBACK_MODE_STOP_DATA_TRANSFER_TRP_STRESS_TEST", 'MBDA')
    def test_ble_uart_loopback_mode_stop_data_transfer_trp_stress_test(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify stop data transfer in loopback mode for multiple times{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        time.sleep(5)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 6):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeature.start_stop_data_transfer()
                status, msg = self.bleuartfeature.stop_data_transfer_results()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}.  stop Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("LOOPBACK_MODE_STOP_DATA_TRANSFER_TRCBP_STRESS_TEST", 'MBDA')
    def test_ble_uart_loopback_mode_stop_data_transfer_trcbp_stress_test(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify stop data transfer in loopback mode for multiple times{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        time.sleep(5)
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_loopback_mode_trcbp()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        i = 1
        for i in range(i, 6):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeature.start_stop_data_transfer()
                status, msg = self.bleuartfeature.stop_data_transfer_results()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}.  stop Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True