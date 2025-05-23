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
    status = sd.mobile_driver.launch_app()
    assert status, "Failed to launch application"

    def function_finalizer():
        print("Local function finalizer")
        # print("Close App")
        # status = sd.mobile_driver.close_app()
        # assert status, "Failed to close application"

    request.addfinalizer(function_finalizer)

class TestBLEUartOvernightTest:

    @pytest.mark.skip("iOS_BLE_UART_OVERNIGHT_CONN_TEST", 'MBDA')
    def test_ble_uart_overnight_connection_test_ios(self):
        print("{0}Test to verify overnight connection tests {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        duration_conn_test = 60 * 480  # Seconds
        t_end = time.time() + duration_conn_test
        while (True):
            print("Check for connection for long hour\n")
            status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
            assert status, "Connection test failed"
            if (time.time() > t_end):
                print("Completed long hour connection test")
                msg = "Connection test verified for time {} seconds".format(duration_conn_test)
                print(msg)
                self.note += msg
                break
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_BLE_UART_OVERNIGHT_LOOPBACK_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_overnight_loopback_test_trcbp_ios(self):
        end_of_test_string = ""
        msg = ""
        test_status = True
        status_TX = True
        status_RX = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("{0}Test to verify loopback mode of data transfer in TRCBP for long hour{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        time.sleep(5)
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        time.sleep(5)
        mode_set_trcbp = self.bleuartfeatureiOS.confirm_loopback_mode_trcbp_ios()
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
                self.bleuartfeatureiOS.loopback_mode_data_transfer_ios()
                self.note += "Stress test for count {}\n".format(count)
                status_TX, msg = self.bleuartfeatureiOS.loopback_mode_results_TX_ios()
                assert status_TX, "Test failed for iteration {}".format(count)
                self.note += msg
                status_RX, msg = self.bleuartfeatureiOS.loopback_mode_results_RX_ios()
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_BLE_UART_OVERNIGHT_LOOPBACK_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_overnight_loopback_test_trp_ios(self):
        end_of_test_string = ""
        msg = ""
        test_status = True
        status_TX = True
        status_RX = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("{0}Test to verify loopback mode of data transfer in TRP for long hour{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeatureiOS.verify_mode_loopback_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_loopback_mode_ios()
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
                self.bleuartfeatureiOS.loopback_mode_data_transfer_ios()
                self.note += "Stress test for count {}\n".format(count)
                status_TX, msg = self.bleuartfeatureiOS.loopback_mode_results_TX_ios()
                assert status_TX, "Test failed for iteration {}".format(count)
                self.note += msg
                status_RX, msg = self.bleuartfeatureiOS.loopback_mode_results_RX_ios()
                assert status_RX, "Test failed for iteration {}".format(count)
                self.note += msg
            except:
                errormsg = "Test failed in iteration {}. Loopback Data transfer has failed.\n\n".format(count)
                self.note += errormsg
                print("Continue the execution\n")
                #count = count + 1
                test_status = False
        assert test_status, self.note
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_BIDIRECTIONAL_OVERNIGHT_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_overnight_uart_mode_Bidirectional_test_trcbp_ios(self):
        end_of_test_string = ""
        msg = ""
        test_status = True
        status_TX = True
        status_RX = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify long hour bidirectional data transfer in UART Mode  {0}".format('=' * 20))
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
        count = 1
        for count in range(count, 701):
            try:
                print("Starting UART Bidirectional tests")
                print("Stress Test for multiple iterations, Iteration", count)
                receive_str = self.bleuartfeatureiOS.verify_mode_uart_birectional_data_transfer_ios()
                self.note += "Stress test for count {}\n".format(count)
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status_TX, msg = self.bleuartfeatureiOS.uart_mode_results_TX_ios(receive_str)
                assert status_TX, "Test failed for iteration {}".format(count)
                self.note += msg
                status_RX, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
                assert status_RX, "Test failed for iteration {}".format(count)
                self.note += msg
            except:
                errormsg = "Test failed in iteration {}. UART Bidirectional  Data transfer has failed.\n\n".format(count)
                self.note += errormsg
                print("Continue the execution\n")
                test_status = False

        assert test_status, self.note
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_BIDIRECTIONAL_OVERNIGHT_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_overnight_uart_mode_Bidirectional_test_trp_ios(self):
        end_of_test_string = ""
        msg = ""
        test_status = True
        status_TX = True
        status_RX = True
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify long hour bidirectional data transfer in UART Mode  {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_uart_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 500K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        try:
            duration_conn_test = 60 * 480  # Seconds
            t_end = time.time() + duration_conn_test
            count = 1
            while (True):
                print("Starting UART Bidirectional tests")
                print("Stress Test for multiple iterations, Iteration", count)
                receive_str = self.bleuartfeatureiOS.verify_mode_uart_birectional_data_transfer_ios()
                self.note += "Stress test for count {}\n".format(count)
                print("Message ", receive_str)
                self.note += "UART Bidirectional data transfer test results \n\n"
                status_TX, msg = self.bleuartfeatureiOS.uart_mode_results_TX_ios(receive_str)
                assert status_TX, "Test failed for iteration {}".format(count)
                self.note += msg
                status_RX, msg = self.bleuartfeatureiOS.uart_mode_results_RX_ios()
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_UNI-DIRECTIONAL_OVERNIGHT_DATA_TRANSFER_TRCBP", 'MBDA')
    def test_ble_uart_overnight_uart_mode_unidirectional_trcbp_ios(self):
        print("{0}Test to verify different modes of data transfer {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify UART mode of unidirectional data transfer - Uplink and Downlink {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_100K_uart_ios()
        self.bleuartfeatureiOS.switch_to_trcbp_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        trcbp_result = "UART Mode TRCBP Mode Data Transfer Results \n"
        print(trcbp_result)
        self.note += trcbp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        i = 1
        for i in range(i, 9):
            try:
                print("UART mode of unidirectional data transfer - Uplink and Downlink, Iteration", i)
                print("Start the Data transfer from DUT side")
                self.bleuartfeatureiOS.dut_uart_mode_100k_data_transfer_ios()
                time.sleep(5)
                status, msg = self.bleuartfeatureiOS.uart_mode_results_100k_RX_ios()
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
                # self.bleuartfeature.initialize_com_port()
                print("Start the Data transfer from APP side")
                self.bleuartfeatureiOS.uart_mode_data_transfer_from_ios_app()
                time.sleep(5)
                status, msg = self.bleuartfeatureiOS.uart_mode_results_100k_TX_display_ios()
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("iOS_UART_MODE_UNI-DIRECTIONAL_OVERNIGHT_DATA_TRANSFER_TRP", 'MBDA')
    def test_ble_uart_overnight_uart_mode_unidirectional_trp_ios(self):
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility()
        assert status, "Unable to scan and connect to DUT"
        print("Verify the UART mode")
        time.sleep(10)
        print(
            "{0}Test to verify UART mode of unidirectional data transfer-TRP-Uplink and Downlink {0}".format('=' * 20))
        self.bleuartfeatureiOS.verify_mode_100K_uart_ios()
        self.bleuartfeatureiOS.save_settings_ios()
        mode_set_trp = self.bleuartfeatureiOS.confirm_100k_uart_mode_ios()
        assert mode_set_trp, "UART Mode, TRP and 100K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeatureiOS.initialize_com_port()
        i = 1
        for i in range(i, 3):
            try:
                print("UART mode of unidirectional data transfer - Uplink and Downlink, Iteration", i)
                print("Start the Data transfer from DUT side")
                self.bleuartfeatureiOS.dut_uart_mode_100k_data_transfer_ios()
                time.sleep(5)
                status, msg = self.bleuartfeatureiOS.uart_mode_results_100k_RX_ios()
                assert status, msg
                self.note += msg
                duration_conn_test = 60 * 1  # 1800 Seconds
                t_end = time.time() + duration_conn_test
                print("Wait for 30 mins")
                while (True):
                    if (time.time() > t_end):
                        end_of_test_string = "Waited for {} seconds".format(duration_conn_test)
                        print(end_of_test_string)
                        self.note += end_of_test_string
                        break
                print("Start the Data transfer from APP side")
                self.bleuartfeatureiOS.uart_mode_data_transfer_from_ios_app()
                time.sleep(5)
                status, msg = self.bleuartfeatureiOS.uart_mode_results_100k_TX_display_ios()
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
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True
