import pytest
import time
from ...CommonSupportLib.BleUARTOTADFUFeatureSupport import BLEUartOTADFUSupport
from ...CommonSupportLib.AppScanAndConnect import ScanningandConnection
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
from ...CommonSupportLib.BleUARTPairingFeatureSupport import BLEUartPairingSupport
from ...CommonSupportLib.StationData import stationData
from ...BaseWrappers.BaseDriver import BaseDriver
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    PHONE_BT_ADDRESS_K, COM_PORT_K, BAUD_RATE_K
from ...StationConfig import conf_file

sd = stationData()
dut_friendly_name = conf_file.dut_friendly_name
ota_upgrade_fw_version = conf_file.ota_upgrade_fw_version
ota_downgrade_fw_version = conf_file.ota_downgrade_fw_version

class TestBLEUartOTADFU:  
    @pytest.mark.usefixtures("default_function_fixture")
    @pytest.mark.test_id("BLE_UART_OTA_DFU_SCAN_AND_CONNECT", 'MBDA')
    def test_chimera_ble_uart_ota_dfu_scan_and_connect(self):
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n")  
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n\n"     
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)  
        self.note += "Performs the bottom to top swipe to click on OTA DFU icon\n\n"      
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        self.note += "Starts the BLE OTA Scan and Connect test\n\n"
        dut_name = self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name) 
        self.note += "Proceed to pair the DUT Device \n\n"
        print("Proceed to pair the Device \n ")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device() 
            self.note += "Pairing is successful with the DUT device \n\n"
        time.sleep(10) 
        ota_msg = "BLE OTA Scan and Connect test is successful \n\n"
        print(ota_msg)
        self.note += ota_msg  
        self.bleuartfeature.go_back()
        time.sleep(2)  
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        self.note += "Verfiy the scan page visibility\n\n" 
        time.sleep(5)
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.note += "MBD App is Closed\n\n"
        self.test_result = True 
        
        
    @pytest.mark.usefixtures("default_function_fixture")
    @pytest.mark.test_id("BLE_UART_OTA_DFU_UPGRADE_FW_VERSION", 'MBDA')
    def test_ble_uart_ota_dfu_upgrade_fw_version(self):
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)          
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        print("Starts the BLE OTA Scan and Connect test\n")
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n \n")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device()
        time.sleep(5)
        otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion = self.bleuartotadfufeature.ble_ota_select_image_upgrade()        
        self.note += otacurrentversionnotext
        self.note += otaupdateversionnotext
        self.note += otadefverison
        self.note += otaupdowngrade
        self.note += otaupdateverison
        self.note += otafwversion
        time.sleep(2)
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        time.sleep(2)
        self.bleuartfeature.go_back()
        time.sleep(2)  
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        status1 = self.bleuartfeature.click_settings_icon()
        time.sleep(10)
        status, msg = self.scanandconnect.verify_fw_rev(ota_upgrade_fw_version)
        assert status, msg
        self.note += msg     
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.test_result = True  
        
        
    @pytest.mark.usefixtures("default_function_fixture")        
    @pytest.mark.test_id("BLE_UART_OTA_DFU_DOWNGRADE_FW_VERSION", 'MBDA')
    def test_ble_uart_ota_dfu_downgrade_fw_version_new(self):
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)     
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n\n ")
        self.note += "Proceed to pair the DUT Device \n\n"
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device()
        time.sleep(2)
        otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion = self.bleuartotadfufeature.ble_ota_select_image_downgrade()
        self.note += otacurrentversionnotext
        self.note += otaupdateversionnotext
        self.note += otadefverison
        self.note += otaupdowngrade
        self.note += otaupdateverison
        self.note += otafwversion
        time.sleep(2)
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        time.sleep(2)
        self.bleuartfeature.go_back()
        time.sleep(2)   
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan and connect for the DUT device in BLE UART \n \n")
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        time.sleep(10)
        print("Click on settings icon to check the FW Version")
        self.bleuartfeature.click_settings_icon()
        time.sleep(10)
        status, msg = self.scanandconnect.verify_fw_rev(ota_downgrade_fw_version)
        assert status, msg
        self.note += msg     
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.test_result = True 
        
        
    @pytest.mark.usefixtures("default_function_fixture")                
    @pytest.mark.test_id("BLE_UART_OTA_DFU_DOWNGRADE_BT_OFF_DATA_TRANSFER", 'MBDA')
    def test_chimera_ble_uart_ota_dfu_downgrade_bt_off_data_transfer(self):
        otaupdate = "Downgrade"
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n") 
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)      
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n \n")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device()
        time.sleep(10)
        otacurrentversionnotext,otaupdateversionnotext,otabtoff,btoff,btisoff,btison,confirmbton = self.bleuartotadfufeature.ble_ota_select_image_bt_off(otaupdate)
        self.note += otacurrentversionnotext
        self.note += otaupdateversionnotext
        self.note += otabtoff
        self.note += btoff
        self.note += btisoff
        self.note += btison
        self.note += confirmbton
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_100K_loopback()
        time.sleep(5)
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_100k_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 100K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_RX()
        assert status, msg
        self.note += msg      
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.test_result = True
        
        
    @pytest.mark.usefixtures("default_function_fixture")       
    @pytest.mark.test_id("BLE_UART_OTA_DFU_UPGRADE_BT_OFF_DATA_TRANSFER", 'MBDA')
    def test_chimera_ble_uart_ota_dfu_upgrade_bt_off_data_transfer(self):
        otaupdate = ""
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n") 
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)       
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n ")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device()
        time.sleep(10)
        otacurrentversionnotext,otaupdateversionnotext,otabtoff,btoff,btisoff,btison,confirmbton = self.bleuartotadfufeature.ble_ota_select_image_bt_off(otaupdate)
        self.note += otacurrentversionnotext
        self.note += otaupdateversionnotext
        self.note += otabtoff
        self.note += btoff
        self.note += btisoff
        self.note += btison
        self.note += confirmbton 
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_100K_loopback()
        time.sleep(5)
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_100k_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 100K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_RX()
        assert status, msg
        self.note += msg      
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.note += "Mobile MBD App is closed\n\n"
        self.test_result = True 
        
        
    @pytest.mark.usefixtures("default_function_fixture")        
    @pytest.mark.test_id("BLE_UART_OTA_DFU_ILLEGAL_IMAGE_DATA_TRANSFER", 'MBDA')
    def test_chimera_ble_uart_ota_dfu_downgrade_illegal_image_data_transfer(self):
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n") 
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)          
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n ")
        self.note += "Proceed to pair the DUT Device \n"
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device()
        time.sleep(10)
        cmderrortext,resultcodetext,getcmderrortext,getresultcodetext,otaok = self.bleuartotadfufeature.ble_ota_select_illegal_image()
        self.note += cmderrortext
        self.note += resultcodetext
        self.note += getcmderrortext
        self.note += getresultcodetext
        self.note += otaok
        print("Verify the scan page visibility \n\n")
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        time.sleep(2)
        print("Press go back to Mobile MBD App Main page\n\n")
        self.bleuartfeature.go_back()
        time.sleep(2)   
        print("Put the DUT to advertising mode")
        time.sleep(20)
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(10)
        self.bleuartfeature.verify_mode_100K_loopback()
        time.sleep(5)
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_100k_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 100K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_RX()
        assert status, msg
        self.note += msg      
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.test_result = True 
        
        
    @pytest.mark.usefixtures("default_function_fixture")       
    @pytest.mark.test_id("BLE_UART_OTA_DFU_PAIR_TIMEOUT_DATA_TRANSFER", 'MBDA')
    def test_ble_uart_ota_dfu_pair_timeout(self):
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n")
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)         
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n \n")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            time.sleep(30)
        otaerror,otapairfail,otaerrortext,otapairfailtext,otaok = self.bleuartotadfufeature.ble_ota_pair_cancel_timeout()
        self.note += otaerror
        self.note += otapairfail
        self.note += otaerrortext
        self.note += otapairfailtext
        self.note += otaok
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        time.sleep(2)
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.test_result = True  
        
        
    @pytest.mark.usefixtures("default_function_fixture")
    @pytest.mark.test_id("BLE_UART_OTA_DFU_CANCEL_PAIR", 'MBDA')
    def test_ble_uart_ota_dfu_cancel_pair(self):
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n") 
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)       
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2)
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n ")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.cancel_pair()
            time.sleep(3)
        otaerror,otapairfail,otaerrortext,otapairfailtext,otaok = self.bleuartotadfufeature.ble_ota_pair_cancel_timeout()
        self.note += otaerror
        self.note += otapairfail
        self.note += otaerrortext
        self.note += otapairfailtext
        self.note += otaok
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        time.sleep(5)
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.test_result = True  
 
    @pytest.mark.usefixtures("default_function_fixture")
    @pytest.mark.test_id("BLE_UART_OTA_DFU_SCAN_AND_CONNECT_STRESS_TEST", 'MBDA')
    @pytest.mark.parametrize("test",range(10))
    def test_chimera_ble_uart_ota_dfu_scan_and_connect_stress_test(self,test):
        test_status = True
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n") 
        print("Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n" )
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(5)  
        print("Performs the bottom to top swipe to click on OTA DFU icon\n \n" ) 
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2)
        print("Starts the BLE OTA Scan and Connect test\n")
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n ")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device() 
        print("Pairing is successful with the DUT device \n\n")                                                          
        time.sleep(5)   
        msg = "Check Connection stability for 120 secs \n"
        self.note += msg
        print(msg)
        time.sleep(120)
        print("Click on back button to go scan page\n\n")
        self.bleuartfeature.go_back()
        time.sleep(1)
        print("Checking for Scan Page visibility \n\n ")
        self.scanandconnect.verify_scan_page_visiblity() 
        time.sleep(1)    
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        time.sleep(2)
        assert test_status
        self.test_result = True 
        
    @pytest.mark.usefixtures("default_function_fixture")
    @pytest.mark.test_id("BLE_UART_OTA_DFU_SCAN_CONNECT_UPGRADE_DOWNGRADE_DATA_TRANSFER_STRESS_TEST", 'MBDA')
    @pytest.mark.parametrize("test",range(10))
    def test_ble_uart_ota_dfu_scan_connect_upgrade_downgrade_data_transfer_stress_test(self,test):
        test_status = True
        otaupdate = "downgrade"
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n")  
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n" 
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(5)  
        self.note += "Performs the bottom to top swipe to click on OTA DFU icon\n \n"  
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2)
        self.note += "Starts the BLE OTA Scan and Connect test\n"
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n ")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device() 
            self.note += "Pairing is successful with the DUT device \n\n"                                                          
            time.sleep(5) 
        self.note += "Verify the DUT device is connected successfully \n\n"
        self.note += "Click on Select Image option and select the OTA bin image file\n\n" 
        print(" Click on Select Image option and select the OTA bin image file \n")
        if otaupdate == "downgrade":
            otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion = self.bleuartotadfufeature.ble_ota_select_image_downgrade()        
            self.note += otacurrentversionnotext
            self.note += otaupdateversionnotext
            self.note += otadefverison
            self.note += otaupdowngrade
            self.note += otaupdateverison
            self.note += otafwversion
            otaupdate = "upgrade"
        elif otaupdate == "upgrade":
            otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion = self.bleuartotadfufeature.ble_ota_select_image_upgrade()        
            self.note += otacurrentversionnotext
            self.note += otaupdateversionnotext
            self.note += otadefverison
            self.note += otaupdowngrade
            self.note += otaupdateverison
            self.note += otafwversion
            otaupdate = "downgrade"
        time.sleep(2)
        self.note += "Verify the scan page visibility \n\n"
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        self.note += "Press go back to Mobile MBD App Main page\n\n"
        time.sleep(5)
        self.bleuartfeature.go_back()
        time.sleep(2)
        self.note += "BLE OTA DFU Up/Down grade is completed and BLE UART data transfer test starts\n \n"
        print("Put the DUT to advertising mode")
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n"
        time.sleep(20)
        self.note += "Scan and connect for the DUT device in BLE UART \n \n"
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(5)
        self.note += "After Connection,Go to setting page and select 100K file, loopback mode, trp \n \n"
        self.bleuartfeature.verify_mode_100K_loopback()
        time.sleep(10)
        print("Go back to Previous Screen")
        self.bleuartfeature.go_back()
        time.sleep(2)
        mode_set_trp = self.bleuartfeature.confirm_100k_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 100K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n\n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_RX()
        assert status, msg
        self.note += msg    
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        time.sleep(2)
        assert test_status
        self.test_result = True   
 
    @pytest.mark.usefixtures("default_function_fixture")
    @pytest.mark.test_id("BLE_UART_OTA_DFU_SCAN_CONNECT_UPGRADE_DOWNGRADE_STRESS_TEST", 'MBDA')
    @pytest.mark.parametrize("test",range(10))
    def test_chimera_ble_uart_ota_dfu_scan_and_connect_upgrade_downgrade_stress_test(self,test):
        test_status = True
        otaupdate = "downgrade"
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n")  
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n" 
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(5)  
        self.note += "Performs the bottom to top swipe to click on OTA DFU icon\n \n"  
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2)
        self.note += "Starts the BLE OTA Scan and Connect test\n"
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n ")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device() 
            self.note += "Pairing is successful with the DUT device \n\n"                                                          
            time.sleep(5) 
        self.note += "Verify the DUT device is connected successfully \n\n"
        self.note += "Click on Select Image option and select the OTA bin image file\n\n" 
        print(" Click on Select Image option and select the OTA bin image file \n")
        if otaupdate == "downgrade":
            otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion = self.bleuartotadfufeature.ble_ota_select_image_downgrade()        
            self.note += otacurrentversionnotext
            self.note += otaupdateversionnotext
            self.note += otadefverison
            self.note += otaupdowngrade
            self.note += otaupdateverison
            self.note += otafwversion
            otaupdate = "upgrade"
        elif otaupdate == "upgrade":
            otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion = self.bleuartotadfufeature.ble_ota_select_image_upgrade()        
            self.note += otacurrentversionnotext
            self.note += otaupdateversionnotext
            self.note += otadefverison
            self.note += otaupdowngrade
            self.note += otaupdateverison
            self.note += otafwversion
            otaupdate = "downgrade"
        time.sleep(2)
        self.note += "Verify the scan page visibility \n\n"
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        self.note += "Press go back to Mobile MBD App Main page\n\n"
        self.bleuartfeature.go_back()
        time.sleep(2)   
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        time.sleep(5)
        assert test_status
        self.test_result = True   
 
    @pytest.mark.usefixtures("default_function_fixture")
    @pytest.mark.test_id("BLE_UART_OTA_DFU_SCAN_CONNECT_UPGRADE_DOWNGRADE_STRESS_TEST_DATA_TRANSFER", 'MBDA')
    @pytest.mark.parametrize("test",range(10)) 
    def test_ble_uart_ota_dfu_scan_and_connect_upgrade_downgrade_stress_test_data_transfer(self,test):
        test_status = True
        otaupdate = "downgrade"
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n")  
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n" 
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(5)  
        self.note += "Performs the bottom to top swipe to click on OTA DFU icon\n \n"  
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2)
        self.note += "Starts the BLE OTA Scan and Connect test\n"
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n ")
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device() 
            self.note += "Pairing is successful with the DUT device \n\n"                                                          
            time.sleep(5) 
        self.note += "Verify the DUT device is connected successfully \n\n"
        self.note += "Click on Select Image option and select the OTA bin image file\n\n" 
        print(" Click on Select Image option and select the OTA bin image file \n")
        if otaupdate == "downgrade":
            otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion = self.bleuartotadfufeature.ble_ota_select_image_downgrade()        
            self.note += otacurrentversionnotext
            self.note += otaupdateversionnotext
            self.note += otadefverison
            self.note += otaupdowngrade
            self.note += otaupdateverison
            self.note += otafwversion
            otaupdate = "upgrade"
        elif otaupdate == "upgrade":
            otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion = self.bleuartotadfufeature.ble_ota_select_image_upgrade()        
            self.note += otacurrentversionnotext
            self.note += otaupdateversionnotext
            self.note += otadefverison
            self.note += otaupdowngrade
            self.note += otaupdateverison
            self.note += otafwversion
            otaupdate = "downgrade"
        time.sleep(2)
        self.note += "Verify the scan page visibility \n\n"
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        self.note += "Press go back to Mobile MBD App Main page\n\n"
        self.bleuartfeature.go_back()
        time.sleep(2)                  
        self.note += "BLE OTA DFU Up/Down grade is completed and BLE UART data transfer test starts\n \n"
        print("Put the DUT to advertising mode")
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n"
        time.sleep(20)
        self.note += "Scan and connect for the DUT device in BLE UART \n \n"
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(10)
        self.note += "After Connection,Go to setting page and select 100K file, loopback mode, trp \n \n"
        self.bleuartfeature.verify_mode_100K_loopback()
        time.sleep(5)
        msg = "Go back to Previous Screen \n \n"
        self.note += msg
        self.note += "Press back button \n \n"
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_100k_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 100K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_RX()
        assert status, msg
        self.note += msg      
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.note += "Mobile MBD App is closed\n\n"
        time.sleep(5)
        assert test_status
        self.test_result = True    
 
    @pytest.mark.usefixtures("default_function_fixture")                
    @pytest.mark.test_id("BLE_UART_OTA_DFU_DOWNGRADE_BT_OFF_DOWNGRADE_DATA_TRANSFER", 'MBDA')
    def test_chimera_ble_uart_ota_dfu_downgrade_bt_off_downgrade_data_transfer(self):
        otaupdate = "Downgrade"
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n")
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n"   
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)   
        self.note += "Performs the bottom to top swipe to click on OTA DFU icon\n \n"        
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        self.note += "Starts the BLE OTA Scan and Connect test\n\n"
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n \n")
        self.note += "Proceed to pair the DUT Device \n\n"
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device()
            self.note += "Pairing is successful with the DUT device \n\n"
        time.sleep(10)
        msg = " Click on Select Image option and select the OTA bin image file \n\n"
        print(msg)
        self.note += msg
        otaselectimage1,otabinfile2,otaupdowngrade,otacurrentversion,otacurrentversionno,otacurrentversionnotext,otaupdateversion,otaupdateversionno,otaupdateversionnotext,otaupdatok,otabtoff,btoff,btisoff,btison,confirmbton = self.bleuartotadfufeature.ble_ota_select_image_bt_off(otaupdate)
        self.note += otaselectimage1
        self.note += otabinfile2
        self.note += otaupdowngrade
        self.note += otacurrentversion
        self.note += otacurrentversionno
        self.note += otacurrentversionnotext
        self.note += otaupdateversion
        self.note += otaupdateversionno
        self.note += otaupdateversionnotext
        self.note += otaupdatok
        self.note += otabtoff
        self.note += btoff
        self.note += btisoff
        self.note += btison
        self.note += confirmbton
        self.note += "BLE OTA DFU BT Off test is completed and BLE UART data transfer test starts\n \n"
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n"   
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)   
        self.note += "Performs the bottom to top swipe to click on OTA DFU icon\n \n"        
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        self.note += "Starts the BLE OTA Scan and Connect test\n"
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n\n ")
        self.note += "Proceed to pair the DUT Device \n\n"
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device()
            self.note += "Pairing is successful with the DUT device \n\n"
        time.sleep(2)
        msg = " Click on Select Image option and select the OTA bin image file \n\n"
        self.note += msg
        print(msg)
        otaselectimage1,otabinfile2,otadowngrade,otacurrentversion,otacurrentversionno,otacurrentversionnotext,otaupdateversion,otaupdateversionno,otaupdateversionnotext,otaupdatok,otadefverison,otaupdowngrade,otaupdateverison,otaupdate,otafwversion = self.bleuartotadfufeature.ble_ota_select_image_downgrade()
        self.note += otaselectimage1
        self.note += otabinfile2
        self.note += otadowngrade
        self.note += otacurrentversion
        self.note += otacurrentversionno
        self.note += otacurrentversionnotext
        self.note += otaupdateversion
        self.note += otaupdateversionno
        self.note += otaupdateversionnotext
        self.note += otaupdatok
        self.note += otadefverison
        self.note += otaupdowngrade
        self.note += otaupdateverison
        self.note += otaupdate
        self.note += otafwversion
        time.sleep(2)
        self.note += "Verify the scan page visibility \n\n"
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        time.sleep(2)
        self.note += "Press go back to Mobile MBD App Main page\n\n"
        self.bleuartfeature.go_back()
        time.sleep(2)
        print("Put the DUT to advertising mode")
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n"
        time.sleep(20)
        self.note += "Scan and connect for the DUT device in BLE UART \n \n"
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(10)
        self.note += "After Connection,Go to setting page and select 100K file, loopback mode, trp \n \n"
        self.bleuartfeature.verify_mode_100K_loopback()
        time.sleep(5)
        msg = "Go back to Previous Screen \n \n"
        self.note += msg
        self.note += "Press back button \n \n"
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_100k_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 100K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_RX()
        assert status, msg
        self.note += msg      
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.note += "Mobile MBD App is closed\n\n"
        self.test_result = True   
 
    @pytest.mark.usefixtures("default_function_fixture")        
    @pytest.mark.test_id("BLE_UART_OTA_DFU_UPGRADE_BT_OFF_DATA_TRANSFER", 'MBDA')
    def test_chimera_ble_uart_ota_dfu_upgrade_bt_off_upgrade_data_transfer(self):
        otaupdate = ""
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n")
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n"   
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)   
        self.note += "Performs the bottom to top swipe to click on OTA DFU icon\n \n"        
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        self.note += "Starts the BLE OTA Scan and Connect test\n"
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n ")
        self.note += "Proceed to pair the DUT Device \n"
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device()
            self.note += "Pairing is successful with the DUT device \n\n"
        time.sleep(10)
        msg = " Click on Select Image option and select the OTA bin image file \n\n"
        self.note+=msg
        print(msg)
        otaselectimage1,otabinfile2,otaupdowngrade,otacurrentversion,otacurrentversionno,otacurrentversionnotext,otaupdateversion,otaupdateversionno,otaupdateversionnotext,otaupdatok,otabtoff,btoff,btisoff,btison,confirmbton = self.bleuartotadfufeature.ble_ota_select_image_bt_off(otaupdate)
        self.note += otaselectimage1
        self.note += otabinfile2
        self.note += otaupdowngrade
        self.note += otacurrentversion
        self.note += otacurrentversionno
        self.note += otacurrentversionnotext
        self.note += otaupdateversion
        self.note += otaupdateversionno
        self.note += otaupdateversionnotext
        self.note += otaupdatok
        self.note += otabtoff
        self.note += btoff
        self.note += btisoff
        self.note += btison
        self.note += confirmbton    
        self.note += "BLE OTA DFU BT Off test is completed and BLE UART data transfer test starts\n \n"
        print("Put the DUT to advertising mode \n")
        print("Scan for the DUT and connect \n")
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n"   
        app_open = self.scanandconnect.verify_app_open()
        assert app_open, "Failed to open MBD Application"
        time.sleep(10)   
        self.note += "Performs the bottom to top swipe to click on OTA DFU icon\n \n"        
        self.bleuartpairingfeature.driver.perform_bottom_to_up_swipe()
        time.sleep(2) 
        self.note += "Starts the BLE OTA Scan and Connect test\n"
        self.bleuartotadfufeature.ble_ota_scan_and_connect_dut(dut_friendly_name)
        print("Proceed to pair the Device \n \n")
        self.note += "Proceed to pair the DUT Device\n \n"
        if sd.platform == "SamsungS10" or sd.platform == "SamsungS21":
            self.bleuartpairingfeature.pair_device()
            self.note += "Pairing is successful with the DUT device \n\n"
        time.sleep(5)
        msg = " Click on Select Image option and select the OTA bin image file \n\n"
        print(msg)
        self.note += msg
        otaselectimage1,otabinfile2,otaupgrade,otacurrentversion,otacurrentversionno,otacurrentversionnotext,otaupdateversion,otaupdateversionno,otaupdateversionnotext,otaupdatok,otadefverison,otaupdowngrade,otaupdateverison,otaupdate,otafwversion = self.bleuartotadfufeature.ble_ota_select_image_upgrade()        
        self.note += otaselectimage1
        self.note += otabinfile2
        self.note += otaupgrade
        self.note += otacurrentversion
        self.note += otacurrentversionno
        self.note += otacurrentversionnotext
        self.note += otaupdateversion
        self.note += otaupdateversionno
        self.note += otaupdateversionnotext
        self.note += otaupdatok
        self.note += otadefverison
        self.note += otaupdowngrade
        self.note += otaupdateverison
        self.note += otaupdate
        self.note += otafwversion
        time.sleep(2)
        self.note += "Verify the scan page visibility \n\n"
        scanpage = self.scanandconnect.verify_scan_page_visiblity()
        time.sleep(2)
        self.note += "Press go back to Mobile MBD App Main page\n\n"
        self.bleuartfeature.go_back()
        time.sleep(2)         
        print("Put the DUT to advertising mode")
        self.note += "Put the DUT device to advertising mode. And verify the Mobile MBD App is launched\n \n"
        time.sleep(20)
        self.note += "Scan and connect for the DUT device in BLE UART \n \n"
        print("Scan for the DUT and connect")
        self.scanandconnect.scan_and_connect_dut(dut_friendly_name)
        print("{0}Test to verify data transfer in loopback mode{0}".format('=' * 20))
        time.sleep(10)
        self.note += "After Connection,Go to setting page and select 100K file, loopback mode, trp \n \n"
        self.bleuartfeature.verify_mode_100K_loopback()
        time.sleep(5)
        msg = "Go back to Previous Screen \n \n"
        self.note += msg
        self.note += "Press back button \n \n"
        self.bleuartfeature.go_back()
        mode_set_trp = self.bleuartfeature.confirm_100k_loopback_mode()
        assert mode_set_trp, "Loopback mode, TRP and 100K not set accordingly"
        trp_result = "Loopback Mode TRP Mode Data Transfer Results \n"
        print(trp_result)
        self.note += trp_result
        time.sleep(5)
        self.bleuartfeature.loopback_mode_data_transfer()
        time.sleep(5)
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_TX()
        assert status, msg
        self.note += msg
        status, msg = self.bleuartfeature.loopback_mode_100Kresults_RX()
        assert status, msg
        self.note += msg      
        print("@@@@@@@@@@@@@@@@@@ Closing App @@@@@@@@@@@@@@@@@@@@ \n")
        self.bleuartfeature.close_mbd_app()
        self.note += "Mobile MBD App is closed\n\n"
        self.test_result = True  