import pytest
import time
from ...CommonSupportLib.StationData import stationData
from ...StationConfig import conf_file
sd = stationData()
dut_friendly_name = conf_file.dut_friendly_name
conn_interval_param = [{'min_int': '0028', 'max_int': '0028', 'latency': '0000', 'supervision_timeout': '00C8'},
                       {'min_int': '0040', 'max_int': '0040', 'latency': '0000', 'supervision_timeout': '00C8'},
                       {'min_int': '0078', 'max_int': '0078', 'latency': '0000', 'supervision_timeout': '01F4'}]

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
        assert status, "Failed to close application"
    request.addfinalizer(function_finalizer)

class TestBLEUartDeepSleepMode:
    @pytest.mark.skip("DEEP_SLEEP_MODE_SCAN_AND_CONNECT_STRESS_TEST", 'MBDA')
    def test_ble_uart_deep_sleep_mode_connect_disconnect(self):
        test_status = True
        print("{0}Test to verify BLE UART Deep sleep mode Discovery, connection and disconnection  {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(10)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_disconnect_dut(dut_friendly_name)
        time.sleep(5)
        for i in range(1, 101):
            try:
                print("Stress Test for 100 iterations, Iteration", i)
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("DEEP_SLEEP_MODE_LONGHOUR_CONN_TEST", 'MBDA')
    def test_ble_uart_overnight_connection_test(self):
        print("{0}Test to Verify BLE UART Deep sleep mode connection stability for one hour {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect\n")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        duration_conn_test = 60 * 60  # Seconds
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

    @pytest.mark.skip("CHIMERA_DEEP_SLEEP_MODE", 'MBDA')
    def test_ble_uart_deep_sleep_mode(self):
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
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
        print("{0}Test to verify Connection interval parameters with different sets of values {0}".format('=' * 20))
        print ("Execute loop back mode data transfer")
        i =1
        for i in range(1,6):
            for each_set in conn_interval_param:
                minimum_int = each_set['min_int']
                print("Minimum interval value :",minimum_int)
                maximum_int = each_set['max_int']
                print("Maximum interval value :",maximum_int)
                latency_val = each_set['latency']
                print("Latency value :",latency_val)
                sup_timeout = each_set['supervision_timeout']
                print("Supervision timeout :",sup_timeout)
                print("Switch to raw data mode [text mode]")
                self.scanandconnect.verify_raw_data_mode()
                print("Click on Connection parameter")
                self.bleuartfeature.click_connectionparam_icon()
                time.sleep(5)
                connpram_set = self.scanandconnect.confirm_connparm_page()
                assert connpram_set, "Raw data, Connection parameter update page is not found"
                time.sleep(10)
                status = self.scanandconnect.set_connection_interval_parameters(minimum_int, maximum_int, latency_val,
                                                                                sup_timeout)
                assert status, "Failed to update connection interval parameter"
                time.sleep(5)
                print("Switch to burst mode")
                self.scanandconnect.switch_raw_data_to_burst_mode()
                print("Able to switch to burst mode")
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
                time.sleep(10)
                duration_conn_test = 60 * 2  # Seconds
                t_end = time.time() + duration_conn_test
                while (True):
                    if (time.time() > t_end):
                        print("Completed long hour connection test")
                        msg = "Connection test verified for time {} seconds".format(duration_conn_test)
                        print(msg)
                        self.note += msg
                        break
        self.bleuartfeature.close_mbd_app()
        self.test_result = True