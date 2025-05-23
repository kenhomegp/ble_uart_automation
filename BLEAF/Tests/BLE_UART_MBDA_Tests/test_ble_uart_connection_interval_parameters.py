import pytest
import time
from ...CommonSupportLib.StationData import stationData
from ...StationConfig import conf_file

sd = stationData()
dut_friendly_name = conf_file.dut_friendly_name

conn_interval_param = [{'min_int': '0014', 'max_int': '0014', 'latency': '0000', 'supervision_timeout': '02D0'},
                       {'min_int': '003C', 'max_int': '003C', 'latency': '0000', 'supervision_timeout': '07D0'},
                       {'min_int': '0078', 'max_int': '0078', 'latency': '0000', 'supervision_timeout': '07D0'}]

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

class TestBLEUARTConnInterval:
    @pytest.mark.parametrize('each_set', conn_interval_param)
    @pytest.mark.skip("CONNECTION_INTERVAL_PARAMETER_TEST_SET1_SET2_SET3", 'MBDA')
    def test_ble_uart_connection_interval_parameter_set1_set2_set3(self, each_set):
        print("{0}Test to verify Connection interval parameters with different sets of values {0}".format('=' * 20))
        minimum_int = each_set['min_int']
        print("Minimum interval value :",minimum_int)
        maximum_int = each_set['max_int']
        print("Maximum interval value :",maximum_int)
        latency_val = each_set['latency']
        print("Latency value :",latency_val)
        sup_timeout = each_set['supervision_timeout']
        print("Supervision timeout :",sup_timeout)
        print("Verify MBD App is open")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        print("{0}Test to verify the connection interval parameters {0}".format('=' * 20))
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
        duration_conn_test = 60 * 25  # Seconds
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