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
    print("Launch MBD Application\n\n")
    app_package = sd.mobile_driver.get_capability('appPackage')
    status = sd.mobile_driver.close_app(app_package)
    assert status, "Failed to close application"
    time.sleep(5)
    status = sd.mobile_driver.launch_app(app_package)
    assert status, "Failed to launch application"
    print("App Launched")
    time.sleep(10)
    def function_finalizer():
        print("Local function finalizer")
    request.addfinalizer(function_finalizer)


class TestBLEUartSimpleIOP:
    @pytest.mark.test_id("BLE_UART_SIMPLE_IOP_ANDROID_TRP", 'MBDA')
    def test_ble_uart_simple_iop_android_trp(self):
        status = True
        test_status = True
        print("{0}Test to verify different modes of data transfer in TRP mode {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        print("{0}Test to execute BLE UART Simple IOP {0}".format('=' * 20))
        time.sleep(10)
        try:
            print("{0}Test to verify data transfer in Checksum Mode in TRP Mode {0}".format('=' * 20))
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
        except:
            errormsg = "Checksum Mode test failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        time.sleep(10)
        try:
            print("{0}Test to verify data transfer in Loopback mode in TRP Mode {0}".format('=' * 20))
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
            time.sleep(5)
        except:
            errormsg = "Loopback Mode test failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        time.sleep(10)
        try:
            print("{0}Test to verify data transfer in Fixed Pattern Mode in TRP Mode {0}".format('=' * 20))
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
        except:
            errormsg = "Fixed Pattern Mode test failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        time.sleep(10)
        try:
            print(
                "{0}Test to verify unidirectional (Uplink) data transfer in UART Mode in TRP Mode {0}".format(
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
            print("Initialize COM Port")
            self.bleuartfeature.initialize_com_port()
            print("Start the Data transfer from DUT side")
            self.bleuartfeature.dut_uart_mode_data_transfer()
            time.sleep(5)
            status, msg = self.bleuartfeature.uart_mode_results_RX()
            assert status, msg
            self.note += msg
            time.sleep(5)
        except:
            errormsg = "Unidirectional (Uplink) data transfer in UART Mode failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        time.sleep(10)
        try:
            print(
                "{0}Test to verify unidirectional (Downlink) data transfer in UART Mode in TRP Mode {0}".format(
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
            print("Initialize COM Port")
            self.bleuartfeature.initialize_com_port()
            print("Start the Data transfer from DUT side")
            self.bleuartfeature.app_uart_mode_data_transfer()
            time.sleep(5)
            status, msg = self.bleuartfeature.uart_mode_results_TX_display()
            assert status, msg
            self.note += msg
            time.sleep(5)
        except:
            errormsg = "Unidirectional (Downlink) data transfer in UART Mode failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        time.sleep(10)
        try:
            print("{0}Test to verify UART mode of bidirectional data transfer in TRP Mode {0}".format(
                '=' * 20))
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
            errormsg = "Bidirectional data transfer in UART Mode failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        # self.bleuartfeature.close_mbd_app()
            assert test_status, self.note
        self.test_result = True

    @pytest.mark.test_id("BLE_UART_SIMPLE_IOP_ANDROID_TRCBP", 'MBDA')
    def test_ble_uart_simple_iop_android_trcbp(self):
        status = True
        test_status = True
        print("{0}Test to verify different modes of data transfer in TRCBP modes {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        print("{0}Test to execute BLE UART Simple IOP {0}".format('=' * 20))
        time.sleep(10)
        try:
            print("{0}Test to verify data transfer in Checksum Mode in TRCBP Modes {0}".format('=' * 20))
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
        except:
            errormsg = "Checksum Mode test failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        time.sleep(10)
        try:
            print("{0}Test to verify data transfer in Loopback mode in TRCBP Modes {0}".format('=' * 20))
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
            time.sleep(5)
        except:
            errormsg = "Loopback Mode test failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        time.sleep(10)
        try:
            print("{0}Test to verify data transfer in Fixed Pattern Mode in TRCBP Modes {0}".format('=' * 20))
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
        except:
            errormsg = "Fixed Pattern Mode test failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        time.sleep(10)
        try:
            print(
                "{0}Test to verify unidirectional (Uplink) data transfer in UART Mode in TRCBP Modes {0}".format(
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
            print("Initialize COM Port")
            self.bleuartfeature.initialize_com_port()
            print("Start the Data transfer from DUT side")
            self.bleuartfeature.dut_uart_mode_data_transfer()
            time.sleep(5)
            status, msg = self.bleuartfeature.uart_mode_results_RX()
            assert status, msg
            self.note += msg
            time.sleep(5)
        except:
            errormsg = "Unidirectional (Uplink) data transfer in UART Mode failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        time.sleep(10)
        try:
            print(
                "{0}Test to verify unidirectional (Downlink) data transfer in UART Mode in TRCBP Modes {0}".format(
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
            print("Initialize COM Port")
            self.bleuartfeature.initialize_com_port()
            print("Start the Data transfer from DUT side")
            self.bleuartfeature.app_uart_mode_data_transfer()
            time.sleep(5)
            status, msg = self.bleuartfeature.uart_mode_results_TX_display()
            assert status, msg
            self.note += msg
            time.sleep(5)
        except:
            errormsg = "Unidirectional (Downlink) data transfer in UART Mode failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        time.sleep(10)
        try:
            print("{0}Test to verify UART mode of bidirectional data transfer in TRCBP Modes {0}".format(
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
            print("Initialize COM Port")
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
        except:
            errormsg = "Bidirectional data transfer in UART Mode failed \n\n"
            self.note += errormsg
            print("Continue the execution\n")
            test_status = False
        # self.bleuartfeature.close_mbd_app()
            assert test_status, self.note
        self.test_result = True

    @pytest.mark.test_id("BLE_UART_OVERNIGHT_CONN_TEST", 'MBDA')
    def test_ble_uart_overnight_connection_test(self):
        print("{0}Test to verify overnight connection tests {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect\n")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        duration_conn_test = 60 * 480  # Seconds
        t_end = time.time() + duration_conn_test
        while (True):
            print("Check for connection for long hour\n")
            status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
            assert status, "Connection test failed"
            if (time.time() > t_end):
                print("Completed long hour connection test")
                msg = "Connection test verified for time {} seconds".format(duration_conn_test)
                print(msg)
                self.note += msg
                break
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("BLE_UART_OVERNIGHT_LOOPBACK_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_overnight_loopback_test_trcbp(self):
        end_of_test_string = ""
        msg = ""
        test_status = True
        status_TX = True
        status_RX = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect\n")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify loopback mode of data transfer in TRCBP for long hour{0}".format('=' * 20))
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
        try:
            duration_conn_test = 60 * 480  # Seconds
            t_end = time.time() + duration_conn_test
            count = 1
            while (True):
                print("Starting loopback tests")
                print("Stress Test for multiple iterations, Iteration", count)
                self.bleuartfeature.loopback_mode_data_transfer()
                self.note += "Stress test for count {}\n".format(count)
                status_TX, msg = self.bleuartfeature.loopback_mode_results_TX()
                assert status_TX, "Test failed for iteration {}".format(count)
                self.note += msg
                status_RX, msg = self.bleuartfeature.loopback_mode_results_RX()
                assert status_RX, "Test failed for iteration {}".format(count)
                self.note += msg
                count = count + 1
                if (time.time() > t_end):
                    print("Completed long hour loopback tests")
                    end_of_test_string = "Loopback tests verified for time {} seconds".format(duration_conn_test)
                    print(end_of_test_string)
                    self.note += end_of_test_string
                    break
        except:
            errormsg = "Test failed in iteration {}. Loopback Data transfer has failed.\n\n".format(count)
            self.note += errormsg
            print("Continue the execution\n")
            count = count + 1
            test_status = False
        assert test_status, self.note
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("BLE_UART_OVERNIGHT_LOOPBACK_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_overnight_loopback_test_trp(self):
        end_of_test_string = ""
        msg = ""
        test_status = True
        status_TX = True
        status_RX = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect\n")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify loopback mode of data transfer in TRP for long hour{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_loopback()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 500K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        count = 1
        for count in range(count, 802):
            try:
                print("Starting loopback tests")
                print("Stress Test for multiple iterations, Iteration", count)
                self.bleuartfeature.loopback_mode_data_transfer()
                self.note += "Stress test for count {}\n".format(count)
                status_TX, msg = self.bleuartfeature.loopback_mode_results_TX()
                assert status_TX, "Test failed for iteration {}".format(count)
                self.note += msg
                status_RX, msg = self.bleuartfeature.loopback_mode_results_RX()
                assert status_RX, "Test failed for iteration {}".format(count)
                self.note += msg
            except:
                errormsg = "Test failed in iteration {}. Loopback Data transfer has failed.\n\n".format(count)
                self.note += errormsg
                print("Continue the execution\n")
                test_status = False
        assert test_status, self.note
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_BIDIRECTIONAL_OVERNIGHT_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_overnight_UART_Bidirectional_test_trcbp(self):
        end_of_test_string = ""
        msg = ""
        test_status = True
        status_TX = True
        status_RX = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify long hour bidirectional data transfer in UART Mode  {0}".format('=' * 20))
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
        count = 1
        for count in range(count, 701):
            try:
                print("Starting UART Bidirectional tests")
                print("Stress Test for multiple iterations, Iteration", count)
                receive_str = self.bleuartfeature.verify_mode_uart_birectional_data_transfer()
                self.note += "Stress test for count {}\n".format(count)
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status_TX, msg = self.bleuartfeature.uart_mode_results_TX(receive_str)
                assert status_TX, "Test failed for iteration {}".format(count)
                self.note += msg
                status_RX, msg = self.bleuartfeature.uart_mode_results_RX()
                assert status_RX, "Test failed for iteration {}".format(count)
                self.note += msg
            except:
                errormsg = "Test failed in iteration {}. UART Bidirectional  Data transfer has failed.\n\n".format(count)
                self.note += errormsg
                print("Continue the execution\n")
                test_status = False
        assert test_status, self.note
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_BIDIRECTIONAL_OVERNIGHT_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_overnight_UART_Bidirectional_test_trp(self):
        end_of_test_string = ""
        msg = ""
        test_status = True
        status_TX = True
        status_RX = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify long hour bidirectional data transfer in UART Mode  {0}".format('=' * 20))
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
        try:
            duration_conn_test = 60 * 480  # Seconds
            t_end = time.time() + duration_conn_test
            count = 1
            while (True):
                print("Starting UART Bidirectional tests")
                print("Stress Test for multiple iterations, Iteration", count)
                receive_str = self.bleuartfeature.verify_mode_uart_birectional_data_transfer()
                self.note += "Stress test for count {}\n".format(count)
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status_TX, msg = self.bleuartfeature.uart_mode_results_TX(receive_str)
                assert status_TX, "Test failed for iteration {}".format(count)
                self.note += msg
                status_RX, msg = self.bleuartfeature.uart_mode_results_RX()
                assert status_RX, "Test failed for iteration {}".format(count)
                self.note += msg
                count = count + 1
                if (time.time() > t_end):
                    print("Completed long hour UART bidirectional  tests")
                    end_of_test_string = "UART Bidirectional tests verified for time {} seconds".format(duration_conn_test)
                    print(end_of_test_string)
                    self.note += end_of_test_string
                    break
        except:
            errormsg = "Test failed in iteration {}. UART Bidirectinal  Data transfer has failed.\n\n".format(count)
            self.note += errormsg
            print("Continue the execution\n")
            count = count + 1
            test_status = False
        assert test_status, self.note
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_UNI-DIRECTIONAL_OVERNIGHT_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_uart_mode_overnight_unidirectional_trcbp(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode of unidirectional data transfer - Uplink and Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_100K_uart()
        self.bleuartfeature.switch_to_trcbp()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trcbp = self.bleuartfeature.confirm_uart_mode_100k_trcbp()
        assert mode_set_trcbp, "UART mode, TRCBP and 100K not set accordingly"
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        i = 1
        for i in range(i, 9):
            try:
                print("UART mode of unidirectional data transfer - Uplink and Downlink, Iteration", i)
                print("Start the Data transfer from DUT side")
                self.bleuartfeature.dut_uart_mode_100k_data_transfer()
                time.sleep(5)
                status, msg = self.bleuartfeature.uart_mode_results_100k_RX()
                assert status, msg
                self.note += msg
                duration_conn_test = 60 * 25  # 1800 Seconds
                t_end = time.time() + duration_conn_test
                print("Wait for 30 mins")
                while (True):
                    if (time.time() > t_end):
                        end_of_test_string = "Waited for {} seconds".format(duration_conn_test)
                        print(end_of_test_string)
                        self.note += end_of_test_string
                        break
                print("Start the Data transfer from APP side")
                self.bleuartfeature.app_uart_mode_data_transfer()
                time.sleep(5)
                status, msg = self.bleuartfeature.uart_mode_results_100k_TX_display()
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
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("UART_MODE_UNI-DIRECTIONAL_OVERNIGHT_DATA_TRANSFER_TRP", 'MBDA')
    def test_uart_mode_overnight_unidirectional_trp(self):
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
            "{0}Test to verify UART mode of unidirectional data transfer-TRP-Uplink and Downlink {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_100K_uart()
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_100k_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 100K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.initialize_com_port()
        i = 1
        for i in range(i, 9):
            try:
                print("UART mode of unidirectional data transfer - Uplink and Downlink, Iteration", i)
                print("Start the Data transfer from DUT side")
                self.bleuartfeature.dut_uart_mode_100k_data_transfer()
                time.sleep(5)
                status, msg = self.bleuartfeature.uart_mode_results_100k_RX()
                assert status, msg
                self.note += msg
                duration_conn_test = 60 * 25  # 1800 Seconds
                t_end = time.time() + duration_conn_test
                print("Wait for 30 mins")
                while (True):
                    if (time.time() > t_end):
                        end_of_test_string = "Waited for {} seconds".format(duration_conn_test)
                        print(end_of_test_string)
                        self.note += end_of_test_string
                        break
                print("Start the Data transfer from APP side")
                self.bleuartfeature.app_uart_mode_data_transfer()
                time.sleep(5)
                status, msg = self.bleuartfeature.uart_mode_results_100k_TX_display()
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
        # self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.test_id("SCAN_AND_CONNECT_DISCONNECT_OVERNIGHT_TEST", 'MBDA')
    def test_ble_uart_overnight_scan_connect_disconnect(self):
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
