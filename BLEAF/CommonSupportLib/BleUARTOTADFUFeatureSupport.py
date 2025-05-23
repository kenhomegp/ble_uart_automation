import struct
import datetime
import time
import os
import sys
import serial
import serial.tools.list_ports
import binascii
from struct import pack
from ..BaseWrappers.BaseDriver import BaseDriver
from . import android_locators as locators
from .StationData import stationData
from .AppScanAndConnect import ScanningandConnection
from ..CommonSupportLib.StationData import stationData
from ..StationConfig import conf_file
from ..CommonSupportLib.Serial_Implementaiton import SerialSuppport
sd = stationData()
     
class BLEUartOTADFUSupport:
    def __init__(self, driver=sd.mobile_driver):
        if not driver:
            sd = stationData()
            self.driver = sd.mobile_driver
            print("Driver-##############################################", self.driver)
        else:
            self.driver = driver
            print("Driver-##############################################", self.driver)
        self.scanandconnect = ScanningandConnection()

    def open_ble_ota_scanner(self):
        error_msg = ""
        print("Click BLE OTA\n\n")
        status, ble_ota_icon = self.driver.find_element('XPATH', locators.ble_ota_icon)
        assert status, "BLE OTA Icon not found"
        
        status = self.driver.click_element(ble_ota_icon)
        assert status, "Failed to open BLE OTA page"
        
        status, scan_button = self.driver.find_element('XPATH', locators.scan_button)
        assert status, "Scan button not found"
        
        status = self.driver.is_visible(scan_button)
        assert status, "Scan button not visible"
        
    def ble_ota_scan_and_connect_dut(self, dut_friendly_name):
        ble_ota = self.open_ble_ota_scanner()

        self.scanandconnect.click_start_scan()
        time.sleep(15)

        self.scanandconnect.search_and_select_dut(dut_friendly_name)
        time.sleep(10)

    def ble_ota_select_image_upgrade(self):
        status, ble_ota_select_image = self.driver.find_element('XPATH', locators.ota_select_image)
        assert status, "BLE Select Image Icon not found"
        
        otaselectimage1 = "Click on the select image icon to select the .bin image \n\n" 
        print(otaselectimage1)
        
        status = self.driver.click_element(ble_ota_select_image)
        assert status, "Failed to open BLE Uart page"
        
        status, ble_ota_binimage1 = self.driver.find_element('XPATH', locators.ota_fw_binfile1)
        assert status, "Bin file image not found"
        
        otabinfile2 = "Select the OTA DFU .bin image \n\n"
        print(otabinfile2)
        
        status = self.driver.is_visible(ble_ota_binimage1)
        assert status, "Bin file image not visible"
        
        status = self.driver.click_element(ble_ota_binimage1)
        assert status, "Failed to click on the BLE OTA Bin File image"  
        
        otaupgrade = "OTA .bin image is selected and Upgrade test starts \n\n"
        
        otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion = self.ota_updowngrade() 
        
        return otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion
        

    def ble_ota_select_image_downgrade(self):
        print("Click on the select image icon to select the .bin image \n\n" )
        status, ble_ota_select_image = self.driver.find_element('XPATH', locators.ota_select_image)
        assert status, "BLE Select Image Icon not found"
        
        status = self.driver.click_element(ble_ota_select_image)
        assert status, "Failed to open BLE Uart page"
              
        print("Select the OTA DFU .bin image \n\n")
        status, ble_ota_binimage2 = self.driver.find_element('XPATH', locators.ota_fw_binfile2)
        assert status, "Bin file image not found"
        
        status = self.driver.is_visible(ble_ota_binimage2)
        assert status, "Bin file image not visible"
        
        status = self.driver.click_element(ble_ota_binimage2)
        assert status, "Failed to click on the BLE OTA Bin File image"  
        
        time.sleep(2)        
        
        print("OTA .bin image is selected and Downgrade test starts \n\n")
        
        otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion = self.ota_updowngrade()
        
        return otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion
                    
    def get_ota_version_details(self): 
        print("Get the Current Version text for the OTA update Screen \n\n")
        status, ble_ota_current_version = self.driver.find_element('XPATH', locators.ota_current_version)
        assert status, "Current Version Text is not found" 
        
        status, self.driver.is_visible(ble_ota_current_version)
        assert status, "Current Version Text is Not Visible"
        
        print("Check for the Current Version with vesion text on the pop up screen \n\n" )
        
        status, ble_ota_current_version_no = self.driver.find_element('XPATH', locators.ota_current_version_no)
        assert status, "Current Version Text is not found" 
        
        status, self.driver.is_visible(ble_ota_current_version_no)
        assert status, "Current Version with version text is Not Visible"   
        
        ble_ota_current_version_no_text = self.driver.get_text(ble_ota_current_version_no)
        
        otacurrentversionnotext = "Get the Current Version Number text for the OTA update Screen --- " + str(ble_ota_current_version_no_text) + "\n\n"
        print(otacurrentversionnotext)
        
        print("Check for the Update Version text on the pop up screen \n\n" )
         
        status, ble_ota_update_version = self.driver.find_element('XPATH', locators.ota_update_version)
        assert status, "Update Version Text is not found"
        
        status, self.driver.is_visible(ble_ota_update_version)
        assert status, "Update Version Text is Not Visible"
        
        print("Check for the Update Version with vesion text on the pop up screen \n\n")
        
        status, ble_ota_update_version_no = self.driver.find_element('XPATH', locators.ota_update_version_no)
        assert status, "Update Version Text is not found"
        
        status, self.driver.is_visible(ble_ota_update_version_no)
        assert status, "Update Version with version text is Not Visible"
        
        ble_ota_update_version_no_text = self.driver.get_text(ble_ota_update_version_no) 
        
        otaupdateversionnotext = "Get the Update Version text for the OTA update Screen --- " + str(ble_ota_update_version_no_text) + "\n\n" 
        print(otaupdateversionnotext)
        
        print("Click on the OK icon after selecting the OTA .bin file \n \n" )
         
        status, ble_ota_ok = self.driver.find_element('XPATH', locators.pixel3a_ok_button)
        assert status, "OK icon not found"
        
        status = self.driver.click_element(ble_ota_ok)
        assert status, "Failed to click on the BLE OTA Bin File image" 
        
        return otacurrentversionnotext,otaupdateversionnotext
                
    def get_ota_updown_version_details(self): 
        print("Check for OTA Update Successfully text and click on OK \n\n")
        status, ble_ota_update = self.driver.find_element('XPATH', locators.ota_update_success)
        assert status, "OTA updated successfully string not found"
        
        status = self.driver.is_visible(ble_ota_update)
        assert status, "OTA updated successfully string not visible"
        
        status, ble_ota_fw_version = self.driver.find_element('XPATH', locators.ota_fw_version)
        assert status, "OTA Firmware Version is not found on the screen"
        
        status = self.driver.is_visible(ble_ota_fw_version)
        assert status, "OTA Firmware Version is not visible on the screen"
        
        ble_ota_fw_version_text = self.driver.get_text(ble_ota_fw_version)
        
        otafwversion = "Get the FW version text from the OTA update Screen --- " + str(ble_ota_fw_version_text) + "\n\n"
        print(otafwversion)
        
        status, ble_ota_ok = self.driver.find_element('XPATH', locators.pixel3a_ok_button)
        assert status, "OK icon not found"
        
        status = self.driver.click_element(ble_ota_ok)
        assert status, "Failed to click on the BLE OTA Bin File image"
        time.sleep(10)
        
        return otafwversion
        
    def ota_updowngrade(self): 
        otadefverison = "Getting the OTA default version details \n \n"  
        
        otacurrentversionnotext,otaupdateversionnotext = self.get_ota_version_details()
        
        otaupdowngrade = "Please wait and observe the OTA upgrade/downgrade is happening on the mobile MBD app \n\n"
        print(otaupdowngrade)        
        
        time.sleep(15)
        
        otaupdateverison = "Getting the OTA updated version details \n\n"
        
        otafwversion = self. get_ota_updown_version_details()  
        
        return otacurrentversionnotext,otaupdateversionnotext,otadefverison,otaupdowngrade,otaupdateverison,otafwversion
        
    def ble_ota_select_image_bt_off(self, otaupdate):        
        if otaupdate == "Downgrade":         
            print("Click on the select image icon to select the .bin image \n\n" )
            
            status, ble_ota_select_image = self.driver.find_element('XPATH', locators.ota_select_image)
            assert status, "BLE Select Image Icon not found"
        
            status = self.driver.click_element(ble_ota_select_image)
            assert status, "Failed to open BLE Uart page"
        
            print("Select the OTA DFU .bin image \n\n")
              
            status, ble_ota_binimage2 = self.driver.find_element('XPATH', locators.ota_fw_binfile2)
            assert status, "Bin file image not found"
            
            status = self.driver.is_visible(ble_ota_binimage2)
            assert status, "Bin file image not visible"
        
            status = self.driver.click_element(ble_ota_binimage2)
            assert status, "Failed to click on the BLE OTA Bin File image"  
        
            time.sleep(2) 
            
        else:        
            print("Click on the select image icon to select the .bin image \n\n" )
            
            status, ble_ota_select_image = self.driver.find_element('XPATH', locators.ota_select_image)
            assert status, "BLE Select Image Icon not found"
        
            status = self.driver.click_element(ble_ota_select_image)
            assert status, "Failed to open BLE Uart page"
        
            print("Select the OTA DFU .bin image \n\n")
        
            status, ble_ota_binimage1 = self.driver.find_element('XPATH', locators.ota_fw_binfile1)
            assert status, "Bin file image not found"
        
            status = self.driver.is_visible(ble_ota_binimage1)
            assert status, "Bin file image not visible"
        
            status = self.driver.click_element(ble_ota_binimage1)
            assert status, "Failed to click on the BLE OTA Bin File image"                     
            time.sleep(2)           
                    
        otacurrentversionnotext,otaupdateversionnotext = self.get_ota_version_details()
        
        time.sleep(2)
        
        otabtoff = "Please wait and observe the OTA upgrade/downgrade is happening and turn off BT while updating \n\n"
        print(otabtoff)
        
        status = self.driver.perform_swipe_top_bottom()
        
        btoff = "Turn OFF BT while OTA update happening\n\n"
        print(btoff)
        status, ble_ota_bt_off = self.driver.find_element('XPATH', locators.ota_bt_off)
        assert status, "Bluetooth icon not found"
        
        status = self.driver.click_element(ble_ota_bt_off)
        assert status, "Failed to click on the Bluetooth Icon"
        
        status = self.driver.perform_swipe()
        
        btisoff = "BT is offed while OTA update happening\n\n"
        print(btisoff)        
        status, ble_ota_bt_is_off = self.driver.find_element('XPATH', locators.ota_bt_is_off)
        assert status, "Bluetooth icon not found"
        
        status = self.driver.is_visible(ble_ota_bt_is_off)
        assert status, "Failed to click on the Bluetooth Icon"
        
        status, ble_ota_ok = self.driver.find_element('XPATH', locators.pixel3a_ok_button)
        assert status, "OK icon not found"
        
        status = self.driver.click_element(ble_ota_ok)
        assert status, "Failed to click on the BLE OTA Bin File image"        
        
        btison = "Turn ON BT \n\n"
        print(btison)             
        status, ble_ota_bt_on = self.driver.find_element('XPATH', locators.ota_bt_on)
        assert status, "Bluetooth icon not found"
        
        status = self.driver.is_visible(ble_ota_bt_on)
        assert status, "Failed to click on the Bluetooth Icon"
                
        status, ble_ota_ok = self.driver.find_element('XPATH', locators.pixel3a_ok_button)
        assert status, "OK icon not found"
        
        status = self.driver.click_element(ble_ota_ok)
        assert status, "Failed to click on the BLE OTA Bin File image"
        
        confirmbton = "Confirm the BT is ON \n\n"
        print(confirmbton)        
        status, ble_ota_bt_on_confirm = self.driver.find_element('XPATH', locators.ota_bt_on_confirm)
        assert status, "Bluetooth icon not found"
        
        status = self.driver.is_visible(ble_ota_bt_on_confirm)
        assert status, "Failed to click on the Bluetooth Icon"
                
        status, ble_ota_allow = self.driver.find_element('XPATH', locators.ota_bt_on_allow)
        assert status, "OK icon not found"
        
        status = self.driver.click_element(ble_ota_allow)
        assert status, "Failed to click on the BLE OTA Bin File image"        
        time.sleep(10)      
        
        return otacurrentversionnotext,otaupdateversionnotext,otabtoff,btoff,btisoff,btison,confirmbton
        

    def ble_ota_select_image_reset_dut(self, otaupdate):      
        if otaupdate == "Downgrade": 
            self.ble_ota_select_image_downgrade()        
            time.sleep(2)
        else:          
            self.ble_ota_select_image_upgrade()                     
            time.sleep(2)           
                    
        self.get_ota_version_details()
        
        time.sleep(2)
                
        print("Please wait and observe the OTA upgrade/downgrade is happening and turn off BT while updating \n\n")
        
        print("Reset DUT while OTA update happening\n")
        
        self.firm.reset_dut()
        
        print("Check for the Current Version text on the pop up screen \n")  
        status, ble_ota_reset_error = self.driver.find_element('XPATH', locators.ota_error)
        assert status, "Current Version Text is not found"
        
        status, self.driver.is_visible(ble_ota_reset_error)
        assert status, "Current Version Text is Not Visible"
        
        print("Check for the Current Version with vesion text on the pop up screen \n") 
        status, ble_ota_abnormal_disconnect = self.driver.find_element('XPATH', locators.ota_abnormal_disconnect)
        assert status, "Current Version Text is not found"
        
        status, self.driver.is_visible(ble_ota_abnormal_disconnect)
        assert status, "Current Version with version text is Not Visible"   
        
        ble_ota_reset_error_text = self.driver.get_text(ble_ota_reset_error)
        print("Get the Current Version text for the OTA update Screen --- ", ble_ota_reset_error_text)   
               
        ble_ota_abnormal_disconnect_text = self.driver.get_text(ble_ota_abnormal_disconnect)
        print("Get the Update Version text for the OTA update Screen --- ", ble_ota_abnormal_disconnect_text)
        
        print("\nClick on the OK icon after selecting the OTA .bin file\n") 
        status, ble_ota_ok = self.driver.find_element('XPATH', locators.pixel3a_ok_button)
        assert status, "OK icon not found"
        
        status = self.driver.click_element(ble_ota_ok)
        assert status, "Failed to click on the BLE OTA Bin File image"
        
        time.sleep(10)
        

    def ble_ota_select_illegal_image(self):
        selectimage = "Click on the select image icon to select the .bin image \n\n"
        print(selectimage)
        status, ble_ota_select_image = self.driver.find_element('XPATH', locators.ota_select_image)
        assert status, "BLE Select Image Icon not found"
        
        status = self.driver.click_element(ble_ota_select_image)
        assert status, "Failed to open BLE Uart page"
        
        selectota = "Select the OTA DFU .bin image \n\n"
        print(selectota)
        status, ble_ota_binimage3 = self.driver.find_element('XPATH', locators.ota_fw_binfile3)
        assert status, "Bin file image not found"
            
        status = self.driver.is_visible(ble_ota_binimage3)
        assert status, "Bin file image not visible"
        
        status = self.driver.click_element(ble_ota_binimage3)
        assert status, "Failed to click on the BLE OTA Bin File image"        
                   
        time.sleep(2)           
                    
        cmderrortext = "Check for the Command error: 2 on the pop up screen \n\n"
        print(cmderrortext)
        status, ble_ota_command_error = self.driver.find_element('XPATH', locators.ota_Command_error)
        assert status, "Current Version Text is not found"
        
        status, self.driver.is_visible(ble_ota_command_error)
        assert status, "Current Version Text is Not Visible"
        
        resultcodetext = "Check for the result code text on the pop up screen \n\n"
        print(resultcodetext)
        status, ble_ota_result_code = self.driver.find_element('XPATH', locators.ota_result_code)
        assert status, "Current Version Text is not found"
        
        status, self.driver.is_visible(ble_ota_result_code)
        assert status, "Current Version with version text is Not Visible"   
        
        
        ble_ota_command_error_text = self.driver.get_text(ble_ota_command_error)
        getcmderrortext = "Get the Command error: 2 text on the pop up screen --- " + str(ble_ota_command_error_text) + "\n\n"
        print(getcmderrortext)   
         
        
        ble_ota_result_code_text = self.driver.get_text(ble_ota_result_code)
        getresultcodetext = "Get the result code text on the pop up screen --- " + str(ble_ota_result_code_text) + "\n\n"
        print(getresultcodetext)
        
        otaok ="Click on the OK icon after selecting the OTA .bin file\n\n"
        print(otaok)
        status, ble_ota_ok = self.driver.find_element('XPATH', locators.pixel3a_ok_button)
        assert status, "OK icon not found"
        
        status = self.driver.click_element(ble_ota_ok)
        assert status, "Failed to click on the BLE OTA Bin File image"        
        time.sleep(10)  

        return selectimage,selectota,cmderrortext,resultcodetext,getcmderrortext,getresultcodetext,otaok
        
    def ble_ota_pair_cancel_timeout(self):
        otaerror = "Check for the OTA Error text on the pop up screen \n\n" 
        print(otaerror)
        status, ble_ota_error = self.driver.find_element('XPATH', locators.ota_error)
        assert status, "OTA Error Text is not found"
        
        status, self.driver.is_visible(ble_ota_error)
        assert status, "OTA Error Text is Not Visible"
        
        otapairfail = "Check for the Pairing fail text on the pop up screen \n\n"
        print(otapairfail)        
        status, ble_ota_pair_fail = self.driver.find_element('XPATH', locators.ota_pairing_fail)
        assert status, "Pairing fail! Text is not found"
        
        status, self.driver.is_visible(ble_ota_pair_fail)
        assert status, "Pairing fail! text is Not Visible"   
        
        ble_ota_error_text = self.driver.get_text(ble_ota_error)
        otaerrortext = "Get the OTA Error text text on the pop up screen --- " + str(ble_ota_error_text) + "\n\n"
        print(otaerrortext)
               
        ble_ota_pair_fail_text = self.driver.get_text(ble_ota_pair_fail)
        otapairfailtext = "Get the Pairing fail! text text on the pop up screen --- " + str(ble_ota_pair_fail_text) + "\n\n"
        
        otaok = "Click on the OK icon \n\n"
        print(otaok)
        status, ble_ota_ok = self.driver.find_element('XPATH', locators.pixel3a_ok_button)
        assert status, "OK icon not found"
        
        status = self.driver.click_element(ble_ota_ok)
        assert status, "Failed to click on the BLE OTA Bin File image"
        time.sleep(10)
        
        return otaerror,otapairfail,otaerrortext,otapairfailtext,otaok
        

        