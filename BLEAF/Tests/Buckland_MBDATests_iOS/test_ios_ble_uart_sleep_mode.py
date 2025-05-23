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
        assert status, "Failed to close application"

    request.addfinalizer(function_finalizer)

class TestBLEUARTDeepSleepModeiOS:
    @pytest.mark.test_id("DEEP_SLEEP_MODE_SCAN_AND_CONNECT_STRESS_TEST_iOS", 'MBDA')
    def test_ble_uart_deep_sleep_mode_connect_disconnect_ios(self):
        test_status = True
        print("{0}Test to verify Chimera Deep sleep mode Discovery, connection and disconnection  {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT")
        self.bleuartfeatureiOS.ios_open_ble_uart_scanner()
        time.sleep(5)
        for i in range(1, 101):
            try:
                print("Stress Test for 100 iterations, Iteration", i)
                iter_msg = "Stress Test for Iteration {}\n".format(i)
                self.note += iter_msg
                self.bleuartfeatureiOS.ios_connect_and_disconnect_dut(dut_friendly_name)
                time.sleep(5)
            except:
                errormsg = "Test failed in iteration {}\n\n".format(i)
                self.note += errormsg
                print("Continue the execution\n")
                test_status = False
        time.sleep(5)
        assert test_status
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("DEEP_SLEEP_MODE_LONGHOUR_CONN_TEST_iOS", 'MBDA')
    def test_chimera_ble_uart_overnight_connection_test(self):
        print("{0}Test to Chimera Deep sleep mode connection stability for one hour {0}".format('=' * 20))
        print("Verify MBD App is open")
        app_open = self.bleuartfeatureiOS.verify_ios_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(5)
        print("Scan for the DUT and connect")
        self.bleuartfeatureiOS.ios_scan_and_connect_dut(dut_friendly_name)
        status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        duration_conn_test = 60 * 60  # Seconds
        t_end = time.time() + duration_conn_test
        while (True):
            print("Check for connection for long hour\n")
            status = self.bleuartfeatureiOS.ios_verify_dut_name_visibility(dut_friendly_name)
            assert status, "Connection test failed"
            if (time.time() > t_end):
                print("Completed long hour connection test")
                msg = "Connection test verified for time {} seconds".format(duration_conn_test)
                print(msg)
                self.note += msg
                break
        self.bleuartfeatureiOS.close_mbd_app()
        self.test_result = True







