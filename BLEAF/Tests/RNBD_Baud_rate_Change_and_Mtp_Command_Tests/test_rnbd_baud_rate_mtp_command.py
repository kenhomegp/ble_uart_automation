import pytest
import time
from ...CommonSupportLib.StationData import stationData
from ...StationConfig import conf_file
from ...CommonSupportLib.Serial_Implementaiton import SerialSuppport
sd = stationData()
#global com
dut_friendly_name = conf_file.dut_friendly_name
comport = conf_file.com_port
#global serialPort
#global maincommand

@pytest.fixture(scope="function", autouse=True)
def local_function_fixture(request):
    print("Local function fixture")
    print("Launch MBD Application")
    app_package = sd.mobile_driver.get_capability('appPackage')
    status = sd.mobile_driver.close_app(app_package)
    assert status, "Failed to close application"
    time.sleep(5)
    status = sd.mobile_driver.launch_app(app_package)
    def function_finalizer():
        print("Local function finalizer")
        print("Close App")
    request.addfinalizer(function_finalizer)

class TestPhonevsRNBD45xFeature:
    @pytest.mark.skip("RNBD_BAUDRATE_CHANGE_TEST_FROM_115200_TO_921600", 'MBDA')
    def test_rnbd_connect_ble_uart_chnage_buadrate_test_to_921600(self):
        step_result = []
        step_descript = []
        step_result1 = []
        step_description = []
        test_status = True
        error_msg = ""
        error_msg1 = ""
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_921600')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result2, step_description = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600')
        for step_dsc in step_description:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify  data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        open_serial_port = self.serialdriver.ComportSet(comport, '921600')
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        read_from_serial = open_serial_port.readlines()
        print("Connection log")
        print(read_from_serial)
        open_serial_port.close()
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP Mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_100K_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_100k_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 100K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('921600')
        receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer_100k('921600')
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.bleuartfeature.uart_mode_results_TX_100(receive_str)
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.uart_mode_results_100k_RX()
        assert status, msg
        self.note += msg
        open_serial_port = self.serialdriver.ComportSet(comport, '921600')
        self.bleuartfeature.go_back()
        time.sleep(10)
        read_from_serial = open_serial_port.readlines()
        print("Disconnection log")
        print(read_from_serial)
        open_serial_port.close()
        time.sleep(10)
        print("step result", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more detailes.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more detailes.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_BAUDRATE_CHANGE_TEST_FROM_921600_TO_115200", 'MBDA')
    def test_rnbd_connect_ble_uart_chnage_buadrate_test_to_115200(self):
        step_result = []
        step_descript = []
        step_result1 = []
        step_description = []
        test_status = True
        error_msg = ""
        error_msg1 = ""
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_921600_to_115200_CHANGE')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_description = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200')
        for step_dsc in step_description:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify  data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        open_serial_port = self.serialdriver.ComportSet(comport, '115200')
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        read_from_serial = open_serial_port.readlines()
        print("Connection log")
        print(read_from_serial)
        open_serial_port.close()
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP Mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_100K_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_100k_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 100K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('115200')
        receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer_100k('115200')
        time.sleep(10)
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.bleuartfeature.uart_mode_results_TX_100(receive_str)
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.uart_mode_results_100k_RX()
        assert status, msg
        self.note += msg
        open_serial_port = self.serialdriver.ComportSet(comport, '115200')
        self.bleuartfeature.go_back()
        time.sleep(10)
        read_from_serial = open_serial_port.readlines()
        print("Disconnection log")
        print(read_from_serial)
        open_serial_port.close()
        time.sleep(10)
        print("step result", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more detailes.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more detailes.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_BAUDRATE_CHANGE_TEST_FROM_115200_TO_2400", 'MBDA')
    def test_rnbd_connect_ble_uart_chnage_buadrate_test_to_2400(self):
        step_result = []
        step_descript = []
        step_result1 = []
        step_result2 = []
        step_description = []
        test_status = True
        error_msg = ""
        error_msg1 = ""
        error_msg2 = ""
        step_dscr = []
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_Baudrate_115200_to_2400')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        step_result1, step_description = self.rnbdfeature.Read_json_file('RNBD_Baudate_2400')
        for step_dsc in step_description:
            self.note += "Command mode results: \n" + str(step_dsc) + "\n"
        print("{0}Test to verify  data transfer {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        open_serial_port = self.serialdriver.ComportSet(comport, '2400')
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        read_from_serial = open_serial_port.readlines()
        print("Connection log")
        print(read_from_serial)
        open_serial_port.close()
        print("Verify the UART mode")
        time.sleep(10)
        print("{0}Test to verify bidirectional data transfer in RNBD UART Mode in TRP Mode {0}".format('=' * 20))
        self.bleuartfeature.verify_mode_100K_uart()
        time.sleep(3)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_100k_uart_mode()
        assert mode_set_trp, "UART Mode, TRP and 100K not set accordingly"
        trp_result = "UART Mode, TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.rnbdfeature.init_com_port('2400')
        receive_str = self.rnbdfeature.verify_rnbd_mode_uart_birectional_data_transfer_100k('2400')
        time.sleep(10)
        print("Message ", receive_str)
        self.note += "UART Bidirectional data transfer test results \n\n"
        status, msg = self.bleuartfeature.uart_mode_results_TX_100(receive_str)
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.uart_mode_results_100k_RX()
        assert status, msg
        self.note += msg
        open_serial_port = self.serialdriver.ComportSet(comport, '2400')
        self.bleuartfeature.go_back()
        time.sleep(10)
        read_from_serial = open_serial_port.readlines()
        print("Disconnection log")
        print(read_from_serial)
        open_serial_port.close()
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        step_result2, step_dscr = self.rnbdfeature.Read_json_file('RNBD_Baudrate_2400_to_115200')
        for step_dsr  in step_dscr:
            self.note += "Command mode results: \n" + str(step_dsr) + "\n"
        print("step result", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more detailes.\n"
            self.note += error_msg
        assert test_status, error_msg
        if False in step_result1:
            test_status = False
            error_msg1 = "Few of the commands have failed. Please refer step description for more detailes.\n"
            self.note += error_msg1
        assert test_status, error_msg1
        if False in step_result2:
            test_status = False
            error_msg2 = "Few of the commands have failed. Please refer step description for more detailes.\n"
            self.note += error_msg2
        assert test_status, error_msg2
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("RNBD_MTP_COMMAND_TEST", 'MBDA')
    def test_rnbd_mtp_test(self):
        step_result = []
        step_descript = []
        test_status = True
        error_msg = ""
        step_result, step_descript = self.rnbdfeature.Read_json_file('RNBD_MTP_Command_Test')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        print("{0}Test to verify to read local power value  {0}".format('=' * 20))
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        open_serial_port = self.serialdriver.ComportSet(comport, '115200')
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        read_from_serial = str(open_serial_port.readlines())
        print("Connection log")
        print(read_from_serial)
        self.note += "Device Connection Log:" + read_from_serial + "\n"
        connection_log = read_from_serial
        print(connection_log)
        mtpcommand = self.rnbdfeature.Parsingphyupdatestring(connection_log)
        print("mtpcommand:", mtpcommand)
        cmd = '$$$'
        cmd1 = str(cmd).encode()
        self.note += " Command Mode:" + cmd + "\n"
        mtp_cmd = mtpcommand +'\r'
        print(mtp_cmd)
        mtp_cmd1 = str(mtp_cmd).encode()
        self.note += " MTP Command:" + mtp_cmd + "\n"
        open_serial_port.write(cmd1)
        cmd_mode = open_serial_port.readlines()
        print(cmd_mode)
        mtp_phy = open_serial_port.write(mtp_cmd1)
        print(mtp_phy)
        time.sleep(10)
        read_phy = str(open_serial_port.readlines())
        print(read_phy)
        if '0D,0D' in read_phy:
            status = True
        else:
            status = False
        assert status, read_phy
        self.note += "MTP Command Result:" + read_phy + "\n"
        open_serial_port.close()
        open_serial_port = self.serialdriver.ComportSet(comport, '115200')
        self.bleuartfeature.go_back()
        time.sleep(10)
        read_from_serial = str(open_serial_port.readlines())
        print("%%%  Device Disconnection log %%%")
        print(read_from_serial)
        self.note += "Device Disonnection Log:" + read_from_serial + "\n"
        open_serial_port.close()
        time.sleep(10)
        print("step result", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step description for more detailes.\n"
            self.note += error_msg
        assert test_status, error_msg
        self.bleuartfeature.close_mbd_app()
        self.test_result = True
        self.note




