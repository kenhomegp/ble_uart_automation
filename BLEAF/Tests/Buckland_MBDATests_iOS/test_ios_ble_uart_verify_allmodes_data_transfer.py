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
    status = sd.mobile_driver.launch_app()
    assert status, "Failed to launch application"
    def function_finalizer():
        print("Local function finalizer")
        print("Close App")
#        status = sd.mobile_driver.close_app()
        #assert status, "Failed to close application"
    request.addfinalizer(function_finalizer)

class TestBLEUartVerifyAllModes:

    @pytest.mark.skip("iOS_CHECKSUM_MODE_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_checksum_mode_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
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

        print("{0}Test to verify data transfer in checksum mode TRCBP {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_checksum_mode_trcbp_ios()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeatureiOS.checksum_mode_data_transfer_ios()
        status, msg = self.bleuartfeatureiOS.checksum_mode_results_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_CHECKSUM_MODE_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_checksum_mode_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
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

        print("{0}Test to verify data transfer in checksum mode TRP {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trp = self.bleuartfeatureiOS.confirm_checksum_mode_ios()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        self.bleuartfeatureiOS.checksum_mode_data_transfer_ios()
        status, msg = self.bleuartfeatureiOS.checksum_mode_results_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_LOOPBACK_MODE_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_loopback_mode_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"

        print("{0}Test to verify data transfer in loopback mode TRCBP {0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_loopback_mode_trcbp_ios()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeatureiOS.loopback_mode_data_transfer_ios()
        time.sleep(10)
        status, msg = self.bleuartfeatureiOS.loopback_mode_results_TX_ios()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeatureiOS.loopback_mode_results_RX_ios()
        assert status, msg
        self.note += msg
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_LOOPBACK_MODE_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_loopback_mode_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("{0}Test to verify data transfer in loopback mode{0}".format('=' * 20))

        time.sleep(10)
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_loopback_mode_ios()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.loopback_mode_data_transfer_ios()
        time.sleep(5)
        status, msg = self.bleuartfeatureiOS.loopback_mode_results_TX_ios()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeatureiOS.loopback_mode_results_RX_ios()
        assert status, msg
        self.note += msg
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_FIXED_PATTERN_MODE_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_fixed_pattern_mode_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
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
        print("{0}Test to verify data transfer in Fixed Pattern mode {0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeatureiOS.verify_mode_fixed_pattern_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_fixed_pattern_mode_ios()
        assert mode_set_trp, "Fixed Pattern Mode, TRP and 500K not set accordingly"
        trp_result = "Fixed Pattern Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.fixed_pattern_mode_data_transfer_ios()
        status, msg = self.bleuartfeatureiOS.fixed_pattern_mode_results_RX_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_FIXED_PATTERN_MODE_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_fixed_pattern_mode_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
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
        print("{0}Test to verify data transfer in Fixed Pattern TRCBP mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_fixed_pattern_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_fixed_pattern_mode_trcbp_ios()
        assert mode_set_trcbp, "Fixed Pattern mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Fixed Pattern Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)

        self.bleuartfeatureiOS.fixed_pattern_mode_data_transfer_ios()
        status, msg = self.bleuartfeatureiOS.fixed_pattern_mode_results_RX_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_APP_TO_DUT_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_unidirectional_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
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
        print("{0}Test to verify UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        print("Start the Data transfer from APP side")
        self.bleuartfeatureiOS.uart_mode_data_transfer_from_ios_app()
        time.sleep(5)
        status, msg = self.bleuartfeatureiOS.uart_mode_results_TX_display_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_APP_TO_DUT_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_unidirectional_trcbp_ios(self):
        test_status = True
        status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
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
        print("{0}Test to verify UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_uart_mode_trcbp_ios()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        print("Start the Data transfer from APP side")
        self.bleuartfeatureiOS.uart_mode_data_transfer_from_ios_app()
        time.sleep(5)
        status, msg = self.bleuartfeatureiOS.uart_mode_results_TX_display_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_DUT_TO_APP_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_dut_to_app_uart_mode_unidirectional_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
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
        print("{0}Test to verify UART mode unidirectional data transfer - Uplink - TRP modes {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeatureiOS.dut_uart_mode_data_transfer_ios()
        time.sleep(5)
        status, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_DUT_TO_APP_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_dut_to_app_uart_mode_unidirectional_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
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
        print("{0}Test to verify UART mode unidirectional data transfer - Uplink - TRCBP modes {0}".format(
            '=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_uart_mode_trcbp_ios()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeatureiOS.dut_uart_mode_data_transfer_ios()
        time.sleep(5)
        status, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_bidirectional_uart_mode_data_transfer_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
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
        print("{0}Test to verify bidirectional data transfer in UART Mode in TRP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        receive_str = self.bleuartfeatureiOS.verify_mode_uart_birectional_data_transfer_ios()
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.bleuartfeatureiOS.uart_mode_results_TX_ios(receive_str)
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_bidirectional_uart_mode_data_transfer_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
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
        print("{0}Test to verify bidirectional data transfer in UART Mode in TRCBP Mode {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_uart_mode_trcbp_ios()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        receive_str = self.bleuartfeatureiOS.verify_mode_uart_birectional_data_transfer_ios()
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.bleuartfeatureiOS.uart_mode_results_TX_ios(receive_str)
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_CHECKSUM_MODE_STRESS_TEST_TRP", 'MBDA')
    def test_ble_uart_checksum_mode_stress_test_trp_ios(self):
        status = True
        msg = ""
        test_status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in checksum mode (TRP) multiple times{0}".format('=' * 15))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_checksum_mode_ios()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.bleuartfeatureiOS.clear_text_ios()
                self.bleuartfeatureiOS.checksum_mode_data_transfer_ios()
                status, msg = self.bleuartfeatureiOS.checksum_mode_results_ios()
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_CHECKSUM_MODE_STRESS_TEST_TRCBP", 'MBDA')
    def test_ble_uart_checksum_mode_stress_test_trcbp_ios(self):
        status = True
        msg = ""
        test_status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in checksum mode (TRCBP) multiple times{0}".format('=' * 15))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_checksum_mode_trcbp_ios()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)

        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.bleuartfeatureiOS.clear_text_ios()
                self.bleuartfeatureiOS.checksum_mode_data_transfer_ios()
                status, msg = self.bleuartfeatureiOS.checksum_mode_results_ios()
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_LOOPBACK_MODE_STRESS_TEST_TRP", 'MBDA')
    def test_ble_uart_loopback_mode_stresstest_trp_ios(self):
        status = True
        test_status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("{0}Test to verify data transfer in loopback mode multiple times {0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_loopback_mode_ios()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.bleuartfeatureiOS.clear_text_ios()
                self.bleuartfeatureiOS.loopback_mode_data_transfer_ios()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeatureiOS.loopback_mode_results_TX_ios()
                assert status, msg
                self.note += msg
                status, msg = self.bleuartfeatureiOS.loopback_mode_results_RX_ios()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_LOOPBACK_MODE_STRESS_TEST_TRCBP", 'MBDA')
    def test_ble_uart_loopback_mode_stresstest_trcbp_ios(self):
        status = True
        test_status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("{0}Test to verify data transfer in loopback mode multiple times {0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_loopback_mode_trcbp_ios()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)

        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.bleuartfeatureiOS.clear_text_ios()
                self.bleuartfeatureiOS.loopback_mode_data_transfer_ios()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeatureiOS.loopback_mode_results_TX_ios()
                assert status, msg
                self.note += msg
                status, msg = self.bleuartfeatureiOS.loopback_mode_results_RX_ios()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_FIXED_PATTERN_STRESS_TEST_TRP", 'MBDA')
    def test_ble_uart_fixed_pattern_mode_stresstest_trp_ios(self):
        test_status = True
        status = True
        print("{0}Test to verify different modes of data transfer multiple times {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the Fixed Pattern mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in Fixed Pattern mode multiple times {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_fixed_pattern_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_fixed_pattern_mode_ios()
        assert mode_set_trp, "Fixed Pattern Mode, TRP and 500K not set accordingly"
        trp_result = "Fixed Pattern Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.bleuartfeatureiOS.clear_text_ios()
                self.bleuartfeatureiOS.fixed_pattern_mode_data_transfer_ios()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeatureiOS.fixed_pattern_mode_results_RX_ios()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_FIXED_PATTERN_STRESS_TEST_TRCBP", 'MBDA')
    def test_ble_uart_fixed_pattern_mode_stresstest_trcbp_ios(self):
        test_status = True
        status = True
        print("{0}Test to verify different modes of data transfer multiple times {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the Fixed Pattern mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in Fixed Pattern mode multiple times {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_fixed_pattern_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_fixed_pattern_mode_trcbp_ios()
        assert mode_set_trcbp, "Fixed Pattern mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Fixed Pattern Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)

        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                self.bleuartfeatureiOS.clear_text_ios()
                self.bleuartfeatureiOS.fixed_pattern_mode_data_transfer_ios()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeatureiOS.fixed_pattern_mode_results_RX_ios()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_DUT_TO_APP_DATA_TRANSFER_STRESS_TEST_TRP", 'MBDA')
    def test_ble_uart_dut_to_app_uart_mode_unidirectional_stress_test_trp_ios(self):
        test_status = True
        status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode unidirectional data transfer - Uplink {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from DUT side")
                self.bleuartfeatureiOS.dut_uart_mode_data_transfer_ios()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_DUT_TO_APP_DATA_TRANSFER_STRESS_TEST_TRCBP", 'MBDA')
    def test_ble_uart_dut_to_app_uart_mode_unidirectional_stress_test_trcbp_ios(self):
        test_status = True
        status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode unidirectional data transfer - Uplink {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_uart_mode_trcbp_ios()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from DUT side")
                self.bleuartfeatureiOS.dut_uart_mode_data_transfer_ios()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_APP_TO_DUT_DATA_TRANSFER_STRESS_TEST_TRP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_unidirectional_trp_stress_test_ios(self):
        test_status = True
        status = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")

        time.sleep(10)
        print("{0}Test to verify UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from APP side")
                self.bleuartfeatureiOS.uart_mode_data_transfer_from_ios_app()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeatureiOS.uart_mode_results_TX_display_ios()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_APP_TO_DUT_DATA_TRANSFER_STRESS_TEST_TRCBP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_unidirectional_trcbp_stress_test_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode of unidirectional data transfer - Downlink {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_uart_mode_trcbp_ios()
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
                self.bleuartfeatureiOS.ios_app_uart_mode_data_transfer()
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                status, msg = self.bleuartfeatureiOS.uart_mode_results_TX_display_ios()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_TRP_STRESS_TEST", 'MBDA')
    def test_ble_uart_bidirectional_uart_mode_data_transfer_trp_stress_test_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in UART Mode in TRP modes - Stress Test {0}".format(
            '=' * 10))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from DUT side")
                receive_str = self.bleuartfeatureiOS.verify_mode_uart_birectional_data_transfer_ios()
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status, msg = self.bleuartfeatureiOS.uart_mode_results_TX_ios(receive_str)
                assert status, msg
                self.note += msg
                status, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_BIDIRECTIONAL_DATA_TRANSFER_TRCBP_STRESS_TEST", 'MBDA')
    def test_ble_uart_bidirectional_uart_mode_data_transfer_trcbp_stress_test_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print(
            "{0}Test to verify bidirectional data transfer in UART Mode in TRCBP modes - Stress Test {0}".format(
                '=' * 10))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_uart_mode_trcbp_ios()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)

        self.bleuartfeatureiOS.initialize_com_port()
        i = 1
        for i in range(i, 11):
            try:
                print("Stress Test for 10 iterations, Iteration", i)
                print("Start the Data transfer from DUT side")
                receive_str = self.bleuartfeatureiOS.verify_mode_uart_birectional_data_transfer_ios()
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status, msg = self.bleuartfeatureiOS.uart_mode_results_TX_ios(receive_str)
                assert status, msg
                self.note += msg
                status, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
                assert status, msg
                self.note += msg
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}. Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_WRITE_WITH_RESPONSE_CHECKSUM_MODE_TRP", 'MBDA')
    def test_ble_uart_checksum_mode_write_with_response_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the checksum mode")
        time.sleep(10)
        print("{0}Test to verify checksum mode of data transfer by enabling write with response-TRP {0}".format('=' * 10))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.enable_write_with_response_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_checksum_mode_ios()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode, Write With Response Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.checksum_mode_data_transfer_ios()
        # Adding delay since write with reponse takes more to complete data transfer
        time.sleep(100)
        status, msg = self.bleuartfeatureiOS.checksum_mode_results_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_WRITE_WITH_RESPONSE_LOOPBACK_MODE_TRP", 'MBDA')
    def test_ble_uart_loopback_mode_write_with_response_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the Loopback mode")
        time.sleep(10)
        print("{0}Test to verify data transfer in loopback mode - Write with Response - TRP {0}".format('=' * 10))
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        self.bleuartfeatureiOS.enable_write_with_response_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_loopback_mode_ios()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode, Write with Response, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.loopback_mode_data_transfer_ios()
        # Adding delay since write with reponse takes more to complete data transfer
        time.sleep(100)
        status, msg = self.bleuartfeatureiOS.loopback_mode_results_TX_ios()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeatureiOS.loopback_mode_results_RX_ios()
        assert status, msg
        self.note += msg
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_WRITE_WITH_RESPONSE_UART_MODE_DUT_TO_APP_TRP", 'MBDA')
    def tes_ble_uart_dut_to_app_uart_mode_write_with_response_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode unidirectional data transfer-Uplink-Write with Response-TRP modes {0}".format('=' * 6))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.enable_write_with_response_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeatureiOS.dut_uart_mode_data_transfer_ios()
        time.sleep(5)
        status, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_WRITE_WITH_RESPONSE_UART_MODE_APP_TO_DUT_TRP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_write_with_response_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode of unidirectional data transfer-Downlink-Write with Response-TRP {0}".format(
            '=' * 6))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.enable_write_with_response_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        print("Initialize COM Port")
        self.bleuartfeatureiOS.initialize_com_port()
        self.bleuartfeatureiOS.uart_mode_data_transfer_from_ios_app()
        # Adding delay since write with reponse takes more to complete data transfer
        time.sleep(20)
        status, msg = self.bleuartfeatureiOS.uart_mode_results_TX_display_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_CHECKSUM_MODE_STOP_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_checksum_mode_stop_data_transfer_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the checksum mode")
        time.sleep(5)
        print("{0}Test to verify STOP data transfer in checksum mode (TRP) {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_checksum_mode_ios()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)

        self.bleuartfeatureiOS.start_stop_data_transfer_ios()
        status, msg = self.bleuartfeatureiOS.stop_data_transfer_results_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_CHECKSUM_MODE_STOP_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_checksum_mode_stop_data_transfer_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the checksum mode")
        time.sleep(5)
        print("{0}Test to verify STOP data transfer in checksum mode (TRCBP) {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_checksum_mode_trcbp_ios()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeatureiOS.start_stop_data_transfer_ios()
        status, msg = self.bleuartfeatureiOS.stop_data_transfer_results_ios()
        assert status, msg
        self.note += msg
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_LOOPBACK_MODE_STOP_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_loopback_mode_stop_data_transfer_trp_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_loopback_mode_ios()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.start_stop_data_transfer_ios()
        status, msg = self.bleuartfeatureiOS.stop_data_transfer_results_ios()
        assert status, msg
        self.note += msg + "\n"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_LOOPBACK_MODE_STOP_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_loopback_mode_stop_data_transfer_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_loopback_mode_trcbp_ios()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeatureiOS.start_stop_data_transfer_ios()
        status, msg = self.bleuartfeatureiOS.stop_data_transfer_results_ios()
        assert status, msg
        self.note += msg + "\n"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_UART_MODE_APP_TO_DUT_STOP_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_stop_data_transfer_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(5)
        print("{0}Test to verify stop data transfer in UART mode - Downlink {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        print("Initialize COM Port")
        self.bleuartfeatureiOS.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeatureiOS.start_stop_data_transfer_ios()
        status, msg = self.bleuartfeatureiOS.stop_data_transfer_results_ios()
        assert status, msg
        self.note += msg +"\n"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_UART_MODE_APP_TO_DUT_STOP_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_stop_data_transfer_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(5)
        print("{0}Test to verify stop data transfer in UART mode - Downlink {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_uart_mode_trcbp_ios()
        assert mode_set_trcbp, "UART mode, TRCBP and 500K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)

        print("Initialize COM Port")
        self.bleuartfeatureiOS.initialize_com_port()
        print("Start the Data transfer from DUT side")
        self.bleuartfeatureiOS.start_stop_data_transfer_ios()
        status, msg = self.bleuartfeatureiOS.stop_data_transfer_results_ios()
        assert status, msg
        self.note += msg + "\n"
        time.sleep(5)
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_CHECKSUM_MODE_STOP_DATA_TRANSFER_TRP_STRESS_TEST", 'MBDA')
    def test_ble_uart_checksum_mode_stop_data_transfer_stress_test_trp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the checksum mode")

        time.sleep(10)
        print("{0}Test to verify STOP data transfer  in checksum mode (TRP) for multiple times{0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_checksum_mode_ios()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        trp_result = "Checksum Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 6):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeatureiOS.start_stop_data_transfer_ios()
                status, msg = self.bleuartfeatureiOS.stop_data_transfer_results_ios()
                assert status, msg
                self.note += msg +"\n"
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}.  stop Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_CHECKSUM_MODE_STOP_DATA_TRANSFER_TRCBP_STRESS_TEST", 'MBDA')
    def test_ble_uart_checksum_mode_stop_data_transfer_stress_test_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the checksum mode")
        time.sleep(5)
        print("{0}Test to verify STOP data transfer  in checksum mode (TRCBP) for multiple times{0}".format(
            '=' * 20))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_checksum_mode_trcbp_ios()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Checksum Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)

        i = 1
        for i in range(i, 6):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeatureiOS.start_stop_data_transfer_ios()
                status, msg = self.bleuartfeatureiOS.stop_data_transfer_results_ios()
                assert status, msg
                self.note += msg +"\n"
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}.  stop Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_LOOPBACK_MODE_STOP_DATA_TRANSFER_TRP_STRESS_TEST", 'MBDA')
    def test_ble_uart_loopback_mode_stop_data_transfer_trp_stress_test_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("{0}Test to verify stop data transfer in loopback mode for multiple times{0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_loopback_mode_ios()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        i = 1
        for i in range(i, 6):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeatureiOS.start_stop_data_transfer_ios()
                status, msg = self.bleuartfeatureiOS.stop_data_transfer_results_ios()
                assert status, msg
                self.note += msg + "\n"
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}.  stop Data transfer has failed.\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_LOOPBACK_MODE_STOP_DATA_TRANSFER_TRCBP_STRESS_TEST", 'MBDA')
    def test_ble_uart_loopback_mode_stop_data_transfer_trcbp_stress_test_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("{0}Test to verify stop data transfer in loopback mode for multiple times{0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_loopback_mode_trcbp_ios()
        assert mode_set_trcbp, "Loopback mode, TRCBP and 500K not set accordingly"
        trcbp_result = "Loopback Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)

        i = 1
        for i in range(i, 6):
            try:
                print("Stress Test for 5 iterations, Iteration", i)
                self.bleuartfeatureiOS.start_stop_data_transfer_ios()
                status, msg = self.bleuartfeatureiOS.stop_data_transfer_results_ios()
                assert status, msg
                self.note += msg + "\n"
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}.  stop Data transfer has failed.\n\n".format(i)
                self.note += errormsg + "\n"
                print("Continue the execution\n")
                status = False
                test_status = False
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("iOS_KILL_MBD_APP_DATA_TRANSFER_CHECKSUM_MODE_TRP", 'MBDA')
    def test_ble_uart_checksum_mode_trp_kill_ios_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in Checksum Mode{0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the checksum mode")
        time.sleep(5)
        print("{0}Test to verify verify Kill MBD APP while data transfer in checksum mode (TRP) {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_checksum_mode_ios()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        time.sleep(5)

        self.bleuartfeatureiOS.data_transfer_START_mobile_app_ios()
        time.sleep(1)
        self.bleuartfeatureiOS.close_mbd_app()
        # To verify if killing the MBD app is successful\
        print("Check dut name visibility")
        status, msg = self.bleuartfeatureiOS.ios_verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("iOS_KILL_MBD_APP_DATA_TRANSFER_CHECKSUM_MODE_TRCBP", 'MBDA')
    def test_ble_uart_checksum_mode_trcbp_kill_ios_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in Checksum Mode{0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the checksum mode")
        time.sleep(5)
        print("{0}Test to verify verify Kill MBD APP while data transfer in checksum mode (TRP and TRCBP) {0}".format(
            '=' * 20))
        self.bleuartfeatureiOS.verify_mode_checksum_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_checksum_mode_trcbp_ios()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        time.sleep(5)
        self.bleuartfeatureiOS.data_transfer_START_mobile_app_ios()
        time.sleep(1)
        self.bleuartfeatureiOS.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.bleuartfeatureiOS.ios_verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("iOS_KILL_MBD_APP_DATA_TRANSFER_LOOPBACK_MODE_TRP", 'MBDA')
    def test_ble_uart_loopback_mode_trp_kill_ios_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in loopback Mode{0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the loopback mode")
        time.sleep(5)
        print("{0}Test to verify verify Kill MBD APP while data transfer in loopback mode (TRP and TRCBP) {0}".format(
            '=' * 20))
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_loopback_mode_ios()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        time.sleep(5)
        self.bleuartfeatureiOS.data_transfer_START_mobile_app_ios()
        time.sleep(1)
        self.bleuartfeatureiOS.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.bleuartfeatureiOS.ios_verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("iOS_KILL_MBD_APP_DATA_TRANSFER_LOOPBACK_MODE_TRCBP", 'MBDA')
    def test_ble_uart_loopback_mode_trcbp_kill_ios_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in loopback Mode{0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the loopback mode")
        time.sleep(5)
        print("{0}Test to verify verify Kill MBD APP while data transfer in loopback mode (TRCBP) {0}".format(
            '=' * 20))
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_loopback_mode_trcbp_ios()
        assert mode_set_trcbp, "Checksum mode, TRCBP and 500K not set accordingly"
        time.sleep(5)
        self.bleuartfeatureiOS.data_transfer_START_mobile_app_ios()
        time.sleep(1)
        self.bleuartfeatureiOS.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.bleuartfeatureiOS.ios_verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("iOS_KILL_MBD_APP_DATA_TRANSFER_UART_APP_TO_DUT_TRP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_trp_kill_ios_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in UART Mode App to Dut{0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(5)
        print("{0}Test to verify Kill MBD APP while data transfer in UART mode App to Dut (TRP) {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "Checksum mode, TRP and 500K not set accordingly"
        time.sleep(5)
        self.bleuartfeatureiOS.data_transfer_START_mobile_app_ios()
        time.sleep(1)
        print("kill MBD App")
        self.bleuartfeatureiOS.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.bleuartfeatureiOS.ios_verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True

    @pytest.mark.test_id("iOS_KILL_MBD_APP_DATA_TRANSFER_UART_APP_TO_DUT_TRCBP", 'MBDA')
    def test_ble_uart_app_to_dut_uart_mode_trcbp_kill_ios_mbd_app(self):
        print("{0}Test to verify killing MBD App during data transfer in UART Mode App to Dut{0}".format('=' * 20))
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and pair")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(5)
        print("{0}Test to verify Kill MBD APP while data transfer in UART mode App to Dut (TRCBP) {0}".format(
            '=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_uart_mode_trcbp_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.data_transfer_START_mobile_app_ios()
        time.sleep(1)
        print("kill MBD App")
        self.bleuartfeatureiOS.close_mbd_app()
        # To verify if killing the MBD app is successful
        status, msg = self.bleuartfeatureiOS.ios_verify_dut_name_non_visibility()
        assert status, "DUT is visible, kill MBD App unsuccessful"
        assert status, msg
        self.note += msg
        self.test_result = True




