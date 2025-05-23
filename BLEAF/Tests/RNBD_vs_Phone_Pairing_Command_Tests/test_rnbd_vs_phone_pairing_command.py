import pytest
import time

from ...CommonSupportLib.StationData import stationData
from ...StationConfig import conf_file
from ...CommonSupportLib.Serial_Implementaiton import SerialSuppport
sd = stationData()
serialdriver = SerialSuppport()

dut_friendly_name = conf_file.dut_friendly_name
comport = conf_file.com_port
baudrate = conf_file.baud_rate

@pytest.fixture(scope="function", autouse=True)
def local_function_fixture(request, remove_dut_paired_record):
    print("Local function fixture")
    remove_dut_paired_record()
    def function_finalizer():
        print("Local function finalizer")
    request.addfinalizer(function_finalizer)

class TestPhonevsRNBD45xPairingFeature:
    @pytest.mark.skip("RNBD_SA,0(No Input No Output with Bonding)_vs_Phone_Pairing", 'MBDA')
    def test_rnbd_pairing_noinput_nooutput_with_bonding(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_IO_Capability_NoInputNoOutput_With_Bonding')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Pairing tests {0}".format('=' * 20))
        print("{0}No Input No Output With Bonding Tests {0}".format('=' * 20))
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Proceed to pair the Device")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.samsungs10_s21_s22_pair_device_peripheral()
        elif sd.platform == "OppoR15":
            self.bleuartpairingfeature.pair_device()
        elif sd.platform == "GooglePixel3A":
            self.rnbdvsphonefeature.google_pixel_pair_device()                                                                                  
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        list_bonded_device = self.rnbdvsphonefeature.list_bonded_device()
        self.note += "Displaying the List of bonded devices:\n"
        self.note += list_bonded_device +'\n'
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        self.bleuartfeature.close_mbd_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        assert test_status, error_msg
        self.test_result = True

    @pytest.mark.skip("RNBD_SA,1(DisplayYesNo)_vs_Phone_Pairing", 'MBDA')
    def test_rnbd_pairing_display_yes_no(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_IO_Capability_DisplayYesNo')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Pairing tests  {0}".format('=' * 20))
        print("{0}Display Yes/No - Numeric Comparison Yes Tests {0}".format('=' * 20))
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)                                                                                                                
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Proceed to pair the Device")
        self.rnbdvsphonefeature.verify_rnbd_displayyesno_keyboarddisplay_pairing_mode()
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        list_bonded_device = self.rnbdvsphonefeature.list_bonded_device()
        self.note += "Displaying the List of bonded devices:\n"
        self.note += list_bonded_device +'\n'
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        self.bleuartfeature.close_mbd_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        assert test_status, error_msg
        self.test_result = True

    @pytest.mark.skip("RNBD_SA,2(NoInputNoOutput)_vs_Phone_Pairing", 'MBDA')
    def test_rnbd_pairing_noinput_nooutput_without_bonding(self):
        error_msg = ""
        test_status = True
        LB_status = False
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_IO_Capability_NoInputNoOutput_Withoutbond')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Pairing tests {0}".format('=' * 20))
        print("{0}No Input No Output without bonding Tests {0}".format('=' * 20))
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Sending Bonding Command B")
        self.rnbdvsphonefeature.bond_device()
        print("Proceed to pair the Device")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.samsungs10_s21_s22_pair_device_peripheral()
        elif sd.platform == "OppoR15":
            self.bleuartpairingfeature.pair_device()
        elif sd.platform == "GooglePixel3A":
            self.rnbdvsphonefeature.google_pixel_pair_device()                                     
        time.sleep(5)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to pair and connect to DUT"
        lb_cmd = str('LB\r').encode()
        serialPort = self.serialdriver.ComportSet(comport, baudrate)
        print("List Bonded Divice")
        serialPort.write(lb_cmd)
        list_bonded_device = serialPort.readlines()
        time.sleep(5)
        if 'END' in str(list_bonded_device) :
            LB_status = True
        else:
            LB_status = False
        assert LB_status, "No record of bonded device"
        self.rnbdvsphonefeature.CloseSerialPort(serialPort)
        print(str(list_bonded_device))
        self.note += "Displaying the List of bonded devices:\n"
        self.note += str(list_bonded_device)+'\n'
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        self.bleuartfeature.close_mbd_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        assert test_status, error_msg
        self.test_result = True

    @pytest.mark.skip("RNBD_SA,3(KeyboardOnly)_vs_Phone_Pairing", 'MBDA')
    def test_rnbd_pairing_Keyboard_only(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_IO_Capability_KeyboardOnly')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Pairing tests {0}".format('=' * 20))
        print("{0}Keyboard Only Pairing Tests {0}".format('=' * 20))
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Proceed to pair the Device")
        self.rnbdvsphonefeature.verify_rnbd_keyboard_only_pairing_mode()
        time.sleep(5)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        list_bonded_device = self.rnbdvsphonefeature.list_bonded_device()
        self.note += "Displaying the List of bonded devices:\n"
        self.note += list_bonded_device+'\n'
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        self.bleuartfeature.close_mbd_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        assert test_status, error_msg
        self.test_result = True

    @pytest.mark.skip("RNBD_SA,4(DisplayOnly)_vs_Phone_Pairing", 'MBDA')
    def test_rnbd_pairing_displayonly(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_IO_Capability_DisplayOnly')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Pairing tests {0}".format('=' * 20))
        print("{0} Display Only Pairing Tests {0}".format('=' * 20))
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Proceed to pair the Device")
        self.rnbdvsphonefeature.verify_rnbd_display_only_pairing_mode()
        time.sleep(5)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        list_bonded_device = self.rnbdvsphonefeature.list_bonded_device()
        self.note += "Displaying the List of bonded devices:\n"
        self.note += list_bonded_device+'\n'
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        self.bleuartfeature.close_mbd_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        assert test_status, error_msg
        self.test_result = True

    @pytest.mark.skip("RNBD_SA,5(Keyboard Display)_vs_Phone_Pairing", 'MBDA')
    def test_rnbd_pairing_keyboard_display(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_IO_Capability_Keyboard_Display')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        print("{0}Test to verify RNBD Pairing tests {0}".format('=' * 20))
        print("{0}Keyboard Display pairing Tests {0}".format('=' * 20))
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Proceed to pair the Device")
        self.rnbdvsphonefeature.verify_rnbd_displayyesno_keyboarddisplay_pairing_mode()
        time.sleep(5)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        list_bonded_device = self.rnbdvsphonefeature.list_bonded_device()
        self.note += "Displaying the List of bonded devices:\n"
        self.note += list_bonded_device+'\n'
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        self.bleuartfeature.close_mbd_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        assert test_status, error_msg
        self.test_result = True

    @pytest.mark.skip("RNBD_BLE_UART_OVERNIGHT_SECURITY_CONN_TEST", 'MBDA')
    def test_rnbd_connect_ble_uart_overnight_connection_test(self):
        error_msg = ""
        test_status = True
        step_result = []
        step_descript = []
        step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_Set_IO_Capability_NoInputNoOutput_With_Bonding')
        for step_des in step_descript:
            self.note += "Command mode results: \n" + str(step_des) + "\n"
        print("{0}Test to verify overnight stability of RNBD Device Discovery and connection {0}".format('=' * 20))
        print("{0}No Input No Output With Bonding Tests {0}".format('=' * 20))
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(2)
        print("Proceed to pair the Device")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.samsungs10_s21_s22_pair_device_peripheral()
        time.sleep(8)            
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
        list_bonded_device = self.rnbdvsphonefeature.list_bonded_device()
        self.note += "Displaying the List of bonded devices:\n"
        self.note += list_bonded_device +'\n'
        print("Step Results", step_result)
        if False in step_result:
            test_status = False
            error_msg = "Few of the commands have failed. Please refer step discription for more details\n"
        self.note += error_msg
        self.bleuartfeature.close_mbd_app()
        step_result1, step_descript1 = self.rnbdvsphonefeature.Read_json_file('RNBD_Reboot')
        assert test_status, error_msg
        self.test_result = True






