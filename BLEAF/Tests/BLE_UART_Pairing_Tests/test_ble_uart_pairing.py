import pytest
import time
from ...CommonSupportLib.BleUARTPairingFeatureSupport import BLEUartPairingSupport
from ...CommonSupportLib.StationData import stationData
from ...BaseWrappers.BaseDriver import BaseDriver
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K,\
    PHONE_BT_ADDRESS_K
from ...StationConfig import conf_file

sd = stationData()
dut_friendly_name = conf_file.dut_friendly_name

@pytest.fixture(scope="function", autouse=True)
def local_function_fixture(request, remove_dut_paired_record_from_phone):
    print("Local function fixture")
    remove_dut_paired_record_from_phone()
    def function_finalizer():
        print("Local function finalizer")
    request.addfinalizer(function_finalizer)

class TestBLEUartPairing:
    @pytest.mark.test_id("PAIRING_CENTRAL_ROLE_NOINPUT_NOOUTPUT", 'MBDA')
    def test_ble_uart_pairing_noinput_nooutput_central(self):
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role No Input No Output Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_no_input_no_output_mode()
        time.sleep(10)
        print("Put the DUT to advertising mode")
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Proceed to pair the Device")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.pair_device()
        elif sd.platform == "VivoV11" or sd.platform == "OppoR15":
            print("Device is paired and started executing")
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("Verify Loopback Data Transfer")
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_NOINPUT_NOOUTPUT_CANCEL", 'MBDA')
    def test_ble_uart_pairing_noinput_nooutput_central_cancel(self):
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role No Input No Output - Cancel Pair Test {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_no_input_no_output_mode()
        time.sleep(10)
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Launch MBD Application")
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Cancel the Pairing attempt")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.cancel_pair()
        elif sd.platform == "VivoV11" or sd. platform == "OppoR15":
            print("No Pairing Pop up in VivoV11 and Oppo R15 in central role, continue with further actions")
            self.bleuartfeature.go_back()
        time.sleep(10)
        print("Verify if the device has disconnected. Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_NOINPUT_NOOUTPUT_PAIR_TIMEOUT", 'MBDA')
    def test_ble_uart_pairing_noinput_nooutput_central_pair_timeout(self):
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role No Input No Output - Pairing Timeout Test {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_no_input_no_output_mode()
        time.sleep(10)
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Launch MBD Application")
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        #Adding 30 secs delay to verify pairing timeout
        print("Verify for Pairing Timeout")
        time.sleep(30)
        if sd.platform == "VivoV11" or sd. platform == "OppoR15":
            print("No Pair Pop up in VivoV11, OPPO R15 mobile so No pair timeout test")
            self.bleuartfeature.go_back()
        else:
            print("Mobile is not VivoV11 So came out of the if condition")
        print("Verify if the device has disconnected. Verifying scan page visiblity in Mobile App side")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_DISPLAYONLY_CORRECTKEY_CONNECTION", 'MBDA')
    def test_ble_uart_pairing_display_only_central(self):
        method = "central"
        flag = True
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Display Only - Correct Key Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_display_only_pairing_mode(method, flag)
        print("Click on Pair and connect to device")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "OppoR15" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.pair_device()
        if sd.platform == "VivoV11":
            # time.sleep(10)
            print("No Pair Pop up in VivoV11 mobile so No Need to click on Pair directly gets paired with the dut")
            self.bleuartpairingfeature.device_pair_ok_peripheral()
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(5)
        print("Verify Loopback Data Transfer")
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_DISPLAYONLY_WRONGKEY_CONNECTION", 'MBDA')
    def test_ble_uart_pairing_display_only_central_wrong_passkey(self):
        method = "central"
        flag = False
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Display Only - Wrong Key Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_display_only_pairing_mode(method, flag)
        print("Attempting to pair and connect to the device")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "OppoR15" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.pair_device()
        elif sd.platform == "VivoV11":
            # time.sleep(10)
            print("No Pair Pop up in VivoV11 mobile so No Need to click on Pair directly gets paired with the dut")
        time.sleep(10)
        print("Verify if the device has disconnected due to wrong key")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_DISPLAYONLY_CANCEL_PAIRING_REQUEST", 'MBDA')
    def test_ble_uart_pairing_display_only_central_cancel(self):
        method = "central"
        flag = True
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Display Only Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_display_only_pairing_mode(method, flag)
        print("Cancel the Pairing attempt")
        if sd.platform == "SamsungS10" or sd.platform == "OppoR15" or sd.platform == "SamsungS22" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.cancel_pair()
        elif sd.platform == "VivoV11":
            print("No Pair Pop up in VivoV11 mobile so No cancle pair test")
            self.bleuartpairingfeature.vivoV11_peripherial_cancel_pair()
        print("Verify if the device has disconnected due to Pairing cancel")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_DISPLAYONLY_PAIRING_TIMEOUT", 'MBDA')
    def test_ble_uart_pairing_display_only_central_pairing_timeout(self):
        method = "central"
        flag = True
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Display Only - Pairing Timeout Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_display_only_pairing_mode(method, flag)
        # Adding 30 secs delay to verify pairing timeout
        print("Verify for Pairing Timeout")
        time.sleep(30)
        if sd.platform == "VivoV11":
            print("No Pair Pop up in VivoV11 mobile so No pair timeout test")
        print("Verify if the device has disconnected. Verifying scan page visiblity in Mobile App side")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_DISPLAY_YES_NO_NUMERIC_COMPARISON_YES", 'MBDA')
    def test_ble_uart_pairing_display_yes_no_central_numeric_comp_yes(self):
        mode = "display_yes_no"
        method = "central"
        numeric_comp = "yes"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Display Yes/No - Numeric Comparison Yes Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, numeric_comp)
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(10)
        print("Verify Loopback Data Transfer")
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_DISPLAY_YES_NO_NUMERIC_COMPARISON_NO", 'MBDA')
    def test_ble_uart_pairing_display_yes_no_central_numeric_comp_no(self):
        mode = "display_yes_no"
        method = "central"
        numeric_comp = "no"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Display Yes/No - Numeric Comparison No Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, numeric_comp)
        time.sleep(10)
        print("Verify if the device has disconnected due to sending the Numeric Comparison NO Command")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_DISPLAY_YES_NO_CANCEL_VIA_PHONE", 'MBDA')
    def test_ble_uart_pairing_display_yes_no_central_pair_cancel(self):
        mode = "display_yes_no"
        method = "central"
        numeric_comp = "cancel"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Display Yes/No - Cancel Pair Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, numeric_comp)
        print("Cancel the Pairing attempt")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "VivoV11" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.cancel_pair()
        print("Verify if the device has disconnected due to Pairing cancel")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_DISPLAY_YES_NO_PAIRING_TIMEOUT", 'MBDA')
    def test_ble_uart_pairing_display_yes_no_central_pair_timeout(self):
        mode = "display_yes_no"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Display Yes/No - Pairing Timeout Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_timeout(mode)
        print("Verify if the device has disconnected. Verifying scan page visiblity in Mobile App side")
        time.sleep(5)
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(5)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_KEYBOARDONLY_ENTER_CORRECT_PASSKEY", 'MBDA')
    def test_ble_uart_pairing_keyboard_only_central_correct_passkey(self):
        method = "central"
        flag = True
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Keyboard Only - Correct Passkey Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_keyboard_only_pairing_mode(method, flag)
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(10)
        print("Verify Loopback Data Transfer")
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_KEYBOARDONLY_ENTER_WRONG_PASSKEY", 'MBDA')
    def test_ble_uart_pairing_keyboard_only_central_wrong_passkey(self):
        method = "central"
        flag = False
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Keyboard Only - Wrong Passkey Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_keyboard_only_pairing_mode(method, flag)
        time.sleep(10)
        print("Verify if the device has disconnected due to wrong pass key")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_KEYBOARDONLY_PRESS_CANCEL_VIA_PHONE", 'MBDA')
    def test_ble_uart_pairing_keyboard_only_central_cancel_pairing(self):
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Keyboard Only - Cancel Pairing Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_keyboard_only_pairing_mode_cancel_timeout_pairing()
        print("Cancel the Pairing attempt")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "OppoR15" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.cancel_pair()
        elif sd.platform == "VivoV11":
            time.sleep(10)
            self.bleuartpairingfeature.vivoV11_device_cancel_pair()
        print("Verify if the device has disconnected due to Pairing cancel")
        print("Verifying scan page visiblity in Mobile App side")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_KEYBOARD_ONLY_PAIRING_TIMEOUT", 'MBDA')
    def test_ble_uart_pairing_keyboard_only_central_pairing_timeout(self):
        flag = True
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Keyboard Only - Cancel Pairing Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_keyboard_only_pairing_mode_cancel_timeout_pairing()
        # Adding 30 secs delay to verify pairing timeout
        print("Verify for Pairing Timeout")
        time.sleep(30)
        print("Verify if the device has disconnected. Verifying scan page visiblity in Mobile App side")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_KEYBOARD_DISPLAY_NUMERIC_COMPARISON_YES", 'MBDA')
    def test_ble_uart_pairing_keyboard_display_central_numeric_comp_yes(self):
        mode = "keyboard_display"
        method = "central"
        numeric_comp = "yes"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Keyboard Display - Numeric Comparison Yes Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, numeric_comp)
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(10)
        print("Verify Loopback Data Transfer")
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_KEYBOARD_DISPLAY_NUMERIC_COMPARISON_NO", 'MBDA')
    def test_ble_uart_pairing_keyboard_display_central_numeric_comp_no(self):
        mode = "keyboard_display"
        method = "central"
        numeric_comp = "no"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Keyboard Display - Numeric Comparison No Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, numeric_comp)
        time.sleep(10)
        print("Verify if the device has disconnected due to sending the Numeric Comparison NO Command")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_KEYBOARD_DISPLAY_CANCEL_VIA_PHONE", 'MBDA')
    def test_ble_uart_pairing_keyboard_display_central_cancel_pairing(self):
        mode = "keyboard_display"
        method = "central"
        numeric_comp = "cancel"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Keyboard Display - Cancel Pair Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, numeric_comp)
        print("Cancel the Pairing attempt")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.cancel_pair()
        elif sd.platform == "VivoV11": 
            self.bleuartpairingfeature.vivoV11_device_cancel_pair()             
        print("Verify if the device has disconnected due to Pairing cancel")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_CENTRAL_ROLE_KEYBOARD_DISPLAY_PAIRING_TIMEOUT", 'MBDA')
    def test_ble_uart_pairing_keyboard_display_central_pairing_timeout(self):
        mode = "keyboard_display"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Central Role Keyboard Display - Pairing Timeout Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Central Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_central_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_timeout(mode)
        print("Verify if the device has disconnected. Verifying scan page visiblity in Mobile App side")
        time.sleep(5)
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_NOINPUT_NOOUTPUT", 'MBDA')
    def test_ble_uart_pairing_noinput_nooutput_peripheral(self):
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role No Input No Output Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_no_input_no_output_mode()
        time.sleep(10)
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Launch MBD Application")
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.samsungs10_s21_s22_pair_device_peripheral()
        elif sd.platform == "OppoR15":              
            self.bleuartpairingfeature.pair_device()
        elif sd.platform == "VivoV11":
            self.bleuartpairingfeature.vivoV11_pair_device_peripheral()
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(10)
        print("Verify Loopback Data Transfer")
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_NOINPUT_NOOUTPUT_CANCEL_PAIR", 'MBDA')
    def test_ble_uart_pairing_noinput_nooutput_peripheral_pairing_cancel(self):
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role No Input No Output - Pair Cancel Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_no_input_no_output_mode()
        time.sleep(10)
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Launch MBD Application")
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(5)
        print("Cancel the Pairing attempt")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "OppoR15" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.cancel_pair()
        elif sd.platform == "VivoV11":
            print("No Pair Pop up in VivoV11 mobile so No cancle pair test")
            self.bleuartpairingfeature.vivoV11_device_cancel_pair()
        print("Verify if the device has disconnected due to Pairing cancel")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_NOINPUT_NOOUTPUT_PAIRING_TIMEOUT", 'MBDA')
    def test_ble_uart_pairing_noinput_nooutput_peripheral_pairing_timeout(self):
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role No Input No Output - Pairing Timeout Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_no_input_no_output_mode()
        time.sleep(10)
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Launch MBD Application")
        time.sleep(10)
        print("Scan for the DUT and connect")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        # Adding 30 secs delay to verify pairing timeout
        print("Verify for Pairing Timeout")
        time.sleep(30)
        print("Verify if the device has disconnected. Verifying scan page visiblity in Mobile App side")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_DISPLAYONLY_CORRECTKEY_CONNECTION", 'MBDA')
    def test_ble_uart_pairing_displayonly_peripheral_correct_key(self):
        method = "peripheral"
        flag = True
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Display Only - Correct Key Tests {0}".format('=' * 20))

        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_display_only_pairing_mode(method, flag)
        print("Attempting to pair and connect to the device")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "OppoR15" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.pair_device()
        elif sd.platform == "VivoV11":
            self.bleuartpairingfeature.vivoV11_pair_device()                                                     
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(10)
        print("Verify Loopback Data Transfer")
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_DISPLAYONLY_WRONGKEY_CONNECTION", 'MBDA')
    def test_ble_uart_pairing_displayonly_peripheral_wrong_key(self):
        method = "peripheral"
        flag = False
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Display Only - Wrong Key Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_display_only_pairing_mode(method, flag)
        print("Attempting to pair and connect to the device")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "OppoR15" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.pair_device()
        elif sd.platform == "VivoV11":
            self.bleuartpairingfeature.vivoV11_pair_device()                  
        time.sleep(5)
        print("Verify if the device has disconnected due to wrong pass key")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_DISPLAYONLY_CANCEL_PAIRING_REQUEST", 'MBDA')
    def test_ble_uart_pairing_displayonly_peripheral_pairing_cancel(self):
        method = "peripheral"
        flag = True
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Display Only - Pairing Cancel Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_display_only_pairing_mode(method, flag)
        print("Cancel the Pairing attempt")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "OppoR15" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.cancel_pair()
        elif sd.platform == "VivoV11":
            self.bleuartpairingfeature.vivoV11_peripherial_cancel_pair()                                          
        time.sleep(10)
        print("Verify if the device has disconnected due to Pairing cancel")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_DISPLAYONLY_PAIRING_TIMEOUT", 'MBDA')
    def test_ble_uart_pairing_displayonly_peripheral_pairing_timeout(self):
        method = "peripheral"
        flag = True
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Display Only - Pairing Timeout Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_display_only_pairing_timeout_peripheral()
        print("Verify Pairing Timeout")
        #Adding 30 secs delay to verify the poiring timeout
        time.sleep(30)
        print("Verify if the device has disconnected due to Pairing timeout")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_DISPLAYYESNO_NUMERIC_COMPARISON_YES", 'MBDA')
    def test_ble_uart_pairing_display_yes_no_peripheral_numeric_comp_yes(self):
        mode = "display_yes_no"
        method = "peripheral"
        numeric_comp = "yes"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Display Yes/No - Numeric Comparison Yes Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, numeric_comp)
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(10)
        print("Verify Loopback Data Transfer")
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_DISPLAY_YES_NO_NUMERIC_COMPARISON_NO", 'MBDA')
    def test_ble_uart_pairing_display_yes_no_peripheral_numeric_comp_no(self):
        mode = "display_yes_no"
        method = "peripheral"
        numeric_comp = "no"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Display Yes/No - Numeric Comparison NO Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, numeric_comp)
        time.sleep(10)
        print("Verify if the device has disconnected due to sending the Numeric Comparison NO Command")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_DISPLAY_YES_NO_CANCEL_VIA_PHONE", 'MBDA')
    def test_ble_uart_pairing_display_yes_no_peripheral_numeric_comp_cancel_pairing(self):
        mode = "display_yes_no"
        method = "peripheral"
        numeric_comp = "cancel"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Display Yes/No - Pairing Cancel Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, numeric_comp)
        print("Cancel the Pairing Attempt")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "OppoR15" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.cancel_pair()
        elif sd.platform == "VivoV11":
            self.bleuartpairingfeature.vivoV11_peripherial_cancel_pair()
        time.sleep(10)
        print("Verify if the device has disconnected due to Pairing Cancel")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_DISPLAY_YES_NO_PAIRING_TIMEOUT", 'MBDA')
    def test_ble_uart_pairing_display_yes_no_peripheral_pairing_timeout(self):
        mode = "display_yes_no"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Display Yes/No - Pairing Timeout Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_timeout(mode)
        print("Verify if the device has disconnected. Verifying scan page visiblity in Mobile App side")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_KEYBOARDONLY_ENTER_CORRECT_PASSKEY", 'MBDA')
    def test_ble_uart_pairing_keyboard_only_peripheral_correct_key(self):
        method = "peripheral"
        flag = True
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Keyboard Only - Correct Passkey Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_keyboard_only_pairing_mode(method, flag)
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(10)
        print("Verify Loopback Data Transfer")
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_KEYBOARDONLY_ENTER_WRONG_PASSKEY", 'MBDA')
    def test_ble_uart_pairing_keyboard_only_peripheral_wrong_key(self):
        method = "peripheral"
        #Flag is set to False to enter wrong Passkey
        flag = False
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Keyboard Only - Wrong Passkey Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_keyboard_only_pairing_mode(method, flag)
        time.sleep(10)
        print("Verify if the device has disconnected due to wrong pass key")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_KEYBOARDONLY_PRESS_CANCEL_VIA_PHONE", 'MBDA')
    def test_ble_uart_pairing_keyboard_only_peripheral_cancel_pairing(self):
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Keyboard Only - Pairing Cancel Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_keyboard_only_pairing_mode_cancel_timeout_pairing()
        print("Cancel the Pairing attempt")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "OppoR15" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.cancel_pair()
        elif sd.platform == "VivoV11":
            self.bleuartpairingfeature.vivoV11_device_cancel_pair()                                                      
        time.sleep(10)
        print("Verify if the device has disconnected due to Pairing cancel")
        print("Verifying scan page visiblity in Mobile App side")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_KEYBOARD_ONLY_PAIRING_TIMEOUT", 'MBDA')
    def test_ble_uart_pairing_keyboard_only_peripheral_pairing_timeout(self):
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Keyboard Only - Pairing Timeout Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_keyboard_only_pairing_mode_cancel_timeout_pairing()
        # Adding 30 secs delay to verify pairing timeout
        print("Verify for Pairing Timeout")
        time.sleep(30)
        print("Verify if the device has disconnected. Verifying scan page visiblity in Mobile App side")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_KEYBOARD_DISPLAY_NUMERIC_COMPARISON_YES", 'MBDA')
    def test_ble_uart_pairing_keyboard_display_peripheral_numeric_comp_yes(self):
        mode = "keyboard_display"
        method = "peripheral"
        mumeric_comp = "yes"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Keyboard Display - Numeric Comparison Yes Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, mumeric_comp)
        time.sleep(10)
        status = self.scanandconnect.verify_dut_name_visibility(dut_friendly_name)
        assert status, "Unable to scan and connect to DUT"
        time.sleep(10)
        print("Verify Loopback Data Transfer")
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
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_KEYBOARD_DISPLAY_NUMERIC_COMPARISON_NO", 'MBDA')
    def test_ble_uart_pairing_keyboard_display_peripheral_numeric_comp_no(self):
        mode = "keyboard_display"
        method = "peripheral"
        mumeric_comp = "no"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Keyboard Display - Numeric Comparison NO Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, mumeric_comp)
        time.sleep(10)
        print("Verify if the device has disconnected due to sending the Numeric Comparison NO Command")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_KEYBOARD_DISPLAY_CANCEL_VIA_PHONE", 'MBDA')
    def test_ble_uart_pairing_keyboard_display_peripheral_pairing_cancel(self):
        mode = "keyboard_display"
        method = "peripheral"
        mumeric_comp = "cancel"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Keyboard Display - Pairing Cancel Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_mode(mode, method, mumeric_comp)
        time.sleep(5)
        print("Cancel the Pairing Attempt")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21" or sd.platform == "OppoR15" or sd.platform == "SamsungS22":
            self.bleuartpairingfeature.cancel_pair()
        elif sd.platform == "VivoV11":
            self.bleuartpairingfeature.vivoV11_peripherial_cancel_pair()                                                      
        time.sleep(10)
        print("Verify if the device has disconnected due to Pairing Cancel")
        print("Verifying scan page visiblity in Mobile App side ")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True

    @pytest.mark.skip("PAIRING_PERIPHERAL_ROLE_KEYBOARD_DISPLAY_PAIRING_TIMEOUT", 'MBDA')
    def test_ble_uart_pairing_keyboard_display_peripheral_pairing_timeout(self):
        mode = "keyboard_display"
        print("{0}Test to verify BLE UART Pairing tests {0}".format('=' * 20))
        print("{0}Peripheral Role Keyboard Display - Pairing Timeout Tests {0}".format('=' * 20))
        print("Delete all paired records from DUT")
        self.bleuartpairingfeature.delete_all_paired_records_from_dut()
        print("Initiate the pairing commands in Peripheral Role")
        self.bleuartpairingfeature.verify_ble_uart_dut_pairing_smp_peripheral_role()
        time.sleep(10)
        self.bleuartpairingfeature.verify_ble_uart_displayyesno_keyboarddisplay_pairing_timeout(mode)
        print("Verify if the device has disconnected. Verifying scan page visiblity in Mobile App side")
        status = self.scanandconnect.verify_scan_page_visiblity()
        assert status, "Unable to see the SCAN icon on the Mobile App screen"
        time.sleep(10)
        self.bleuartfeature.close_mbd_app()
        self.test_result = True