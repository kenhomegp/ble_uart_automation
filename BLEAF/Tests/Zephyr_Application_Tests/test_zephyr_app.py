import collections
import threading
from time import sleep

import pytest
import time

import concurrent.futures
import datetime

import serial
import logging
import re
import subprocess
import platform

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from collections import OrderedDict
from ...CommonSupportLib.AppScanAndConnect import ScanningandConnection
from ...CommonSupportLib.BLEUARTFeatureSupport import BLEUARTFeatureSupport
from ...CommonSupportLib.StationData import stationData
from ...CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    PHONE_BT_ADDRESS_K, COM_PORT_K, BAUD_RATE_K
from ...CommonSupportLib.BLEUARTFeatureSupportiOS import BLEUARTFeatureSupportiOS
from ...CommonSupportLib.RNBDPairingandLightBlueFeatureSupport import RNBDvsPhoneFeatureSupport

from ...MCP2200.MCP2200 import Mcp2200
from ...StationConfig import conf_file

from ...CommonSupportLib.iOS_BluetoothSupport import iOSBluetoothSupport
from ...CommonSupportLib.iOS_BLEPairingSupport import iOSBLEPairingSupport

from ...CommonSupportLib.IOControl_LEDStatus import IOControlLEDStatus
from ...CommonSupportLib.SerialReader import SerialReader

from ...BaseWrappers.NewBaseDriver import NewBaseDriver
from ...BaseWrappers.SSHSupport import ShellHandler

import inspect

sd = stationData()
dut_friendly_name = conf_file.dut_friendly_name

RESET_PIN = 0x02
BTN_CTRL_PIN = 0x04

#MCU = Mcp2200(PID='0x00dc')
#serial_data = ''

#phone_list = ["SamsungS21", "GooglePixel5", "OPPO Reno", "SamsungS10", "GooglePixel3A", "VivoV11"]
'''
zephyr_execute_test = ['test_zephyr_broadcaster_observer_1',
                       'test_zephyr_broadcaster_observer_2',
                       'test_zephyr_central_gatt_write_1',
                       'test_zephyr_central_gatt_write_2',
                       'test_zephyr_central_gatt_write_3',
                       'test_zephyr_direct_advertising_gatt_read_write',
                       'test_zephyr_direct_advertising_pairing_connect',
                       'test_zephyr_observer_application',
                       'test_zephyr_peripheral_android_hid_forget_device',
                       'test_zephyr_peripheral_android_hid_mouse_click',
                       'test_zephyr_peripheral_android_hid_pairing_connect',
                       'test_zephyr_peripheral_application',
                       'test_zephyr_peripheral_hid_forget_device',
                       'test_zephyr_peripheral_hid_mouse_click',
                       'test_zephyr_peripheral_hid_pairing_connect',
                       'test_zephyr_peripheral_hid_pairing_connect_1',
                       'test_zephyr_peripheral_identity']
'''
zephyr_execute_test = ['test_zephyr_peripheral_application']

@pytest.fixture(scope="class", autouse=True)
def define_class_attributes(request, default_class_fixture):
    print(f"this is local specific class fixture. {conf_file.zephyr_dut_only_test_case}")

    zephyr_functions = [
        func_name for func_name, _ in inspect.getmembers(TestZephyrApp, predicate=inspect.isfunction)
        if 'zephyr' in func_name
    ]
    print(zephyr_functions)
    # if (isinstance(request.cls.bleuartfeature, BLEUARTFeatureSupport)):
    #    print("Android: Init MCP2200")
    #    request.cls.bleuartfeature.initialize_com_port()

    #baud_rate = conf_file.baud_rate
    #status = request.cls.iocontrolledstatus.Zephyr_InitMCP2200(baud_rate, MCU)
    #assert status, "Failed to initialize the MCP2200"

    if not conf_file.zephyr_dut_only_test_case and platform.system() == "Windows":
        _MCU = Mcp2200(PID='0x00dc')
        request.cls.MCU = _MCU
        request.cls.iocontrolledstatus.Zephyr_InitMCP2200('115200', _MCU)
        serial_runner = SerialReader(conf_file.com_port, baudrate=115200)
        time.sleep(1)

        def dut_reset():
            print('DUT Reset. Firmware reset')
            request.cls.iocontrolledstatus.Zephyr_IOCtrl(_MCU, RESET_PIN, 0.3)
            return 'reset_dut'

        result, serial_data = serial_runner.execute(dut_reset)
        print(f'task = {result}, data = {serial_data}')
        assert 'Booting Zephyr OS' in serial_data, 'Reboot device: fail'
        fw_version = conf_file.zephyr_test_version
        assert fw_version in serial_data, 'Firmware version is not correct'
        print(f'zephyr test version : {fw_version}')

    def class_finalizer():
        print("Local Class finalizer")

    request.addfinalizer(class_finalizer)

@pytest.fixture(scope="function", autouse=True)
def local_function_fixture(request):
    print("Local function fixture")
    # print("Launch MBD Application")

    test_func_name = request.node.name
    print(f"Fixture {local_function_fixture.__name__} is being used by test: {test_func_name}")

    def function_finalizer():
        print("Local function finalizer")
        # print("Close App")
        print(f'mobile platform = {sd.mobile_platform}')
        if sd.mobile_platform == "iOS" or sd.mobile_platform == 'mac':
            if test_func_name == "test_zephyr_peripheral_hid_ble_bonded":
                sd.mobile_driver.close_app(sd.config.ios_lightblue_app_package)
        else:
            if 'zephyr' in test_func_name and test_func_name != 'test_zephyr_peripheral_identity':
                if not conf_file.zephyr_dut_only_test_case:
                    app_package = sd.mobile_driver.get_capability('appPackage')
                    print(f"Close app.{app_package}")
                    sd.mobile_driver.close_app(app_package)
                    time.sleep(3)

    request.addfinalizer(function_finalizer)

@pytest.fixture
def remote_appium_handler(zephyr_flash_firmware):
    assert zephyr_flash_firmware, 'Flashing test firmware : Failed'

    #assert len(sd.config.multilink_phone_list) > 1, 'Multilink mobile phones config error'
    assert len(sd.config.multilink_phone_list) > 0, 'Multilink mobile phones config error'
    print("ssh_handler fixture")
    ssh_handler = ShellHandler(sd.config.remote_appium_server_ip, sd.config.remote_appium_username,
                               sd.config.remote_appium_pwd)

    multiple_server = True
    if multiple_server:
        print('Running multiple appium server')
        for i in range(len(sd.config.multilink_phone_list)):
            ip_addr = sd.config.remote_appium_server_ip
            port_num = int(sd.config.remote_appium_server_port)
            appium_server_logs = "appium_server_logs_{}_{}".format(port_num+i, datetime.datetime.now().strftime(
                "%Y-%m-%d_%H_%M_%S"))
            start_server_cmd = 'appium -a {} -p {} --relaxed-security > {}.txt &'.format(
                ip_addr, str(port_num+i), appium_server_logs)
            print("start_remote_appium_server. ip = {}, port = {}".format(ip_addr, port_num+i))
            sh_in, sh_out, sh_error = ssh_handler.execute(start_server_cmd)
            if not sh_error:
                print("Remote appium server started successfully. cmd = {}".format(start_server_cmd))
                time.sleep(2)
            else:
                assert False, "Failed to start remote appium server. Command output: {}".format(sh_out)

    else:
        tt = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        ip_addr = sd.config.remote_appium_server_ip
        port_num = sd.config.remote_appium_server_port
        print("start_remote_appium_server. ip = {}, port = {}, time = {}".format(ip_addr, port_num, tt))
        appium_server_logs = "appium_server_logs_{}".format(tt)
        start_server_cmd = 'appium -a {} -p {} --relaxed-security > {}.txt &'.format(ip_addr, port_num,
                                                                                 appium_server_logs)
        sh_in, sh_out, sh_error = ssh_handler.execute(start_server_cmd)
        if not sh_error:
            print("Remote appium server started successfully.")
        else:
            assert False, "Failed to start remote appium server. Command output: {}".format(sh_out)

    yield ssh_handler

    print('Kill remote appium server')
    sh_in, sh_out, sh_error = ssh_handler.execute("ps -a")
    pids = []
    print("List process:")
    for line in sh_out:
        print(line)
        if 'node' in line:
            match = re.match(r'\s*(\d+)', line)
            if match:
                pid = match.group(1)
                pids.append(pid)
                print(f"PID: {pid}")
            else:
                print("PID not found.")

    print("Appium server. PID.count = {}".format(len(pids)))

    if len(pids) != 0:
        for pid in pids:
            print('killing appium process,pid = {}'.format(pid))
            cmd = 'kill -9 {}'.format(pid)
            sh_in, sh_out, sh_error = ssh_handler.execute(cmd)
            if not sh_error:
                print("Appium Process Killed Successfully. cmd = {}".format(cmd))
            else:
                assert False, "Failed to kill currently running appium. " \
                              "Please kill the process manually and restart execution. cmd output: {}".format(sh_out)

@pytest.fixture
def multilink_mobile_drivers(remote_appium_handler):
    print("Initial multilink_drivers")
    time.sleep(15)
    #Android MBD
    #app_package = sd.config.app_package
    #app_activity = sd.config.app_activity

    #Android lightblue
    #app_package = sd.config.lightblue_app_package
    #app_activity = sd.config.lightblue_app_activity

    #for phone in sd.config.multilink_phone_list:
    for i in range(len(sd.config.multilink_phone_list)):
        #print('mobile phone = {}'.format(phone))
        phone = sd.config.multilink_phone_list[i]
        mobile_to_use = sd.config.mobile_data_config.get(phone)
        print('mobile_to_use = {}'.format(mobile_to_use))
        platform = mobile_to_use.get(PLATFORM_NAME_K)
        if platform == 'Android':
            app_package = sd.config.lightblue_app_package
            app_activity = sd.config.lightblue_app_activity
        else:
            app_package = sd.config.ios_lightblue_app_package
            app_activity = sd.config.app_activity
        port = int(sd.config.remote_appium_server_port)
        driver = NewBaseDriver(sd.config.remote_appium_server_ip, str(port+i),
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            app_package, app_activity,
                            fresh_env=False)
        print(f'Create driver for mobile phone:{phone}')
        mobile_data_dic = {'driver': driver, 'phone': phone + '_' + platform}

        sd.multilink_mobile_driver.append(mobile_data_dic)

    t1 = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    print(f"complete.time = {t1}")

    yield sd.multilink_mobile_driver

    print('multilink quit drivers')
    for index, dat in enumerate(sd.multilink_mobile_driver):
        m_driver = dat['driver']
        m_driver.quit_driver()

@pytest.fixture
def zephyr_flash_firmware(request):
    #print(f'zephyr_flash_firmware.{os.getcwd()}')
    #print(f'zephyr_flash_firmware. test case : {request.node.name}')

    #dfu = request.config.getoption('--dfu')
    #fw_update = dfu
    fw_update = True
    fw_update_dut2 = False

    #test_image = request.param
    func_name = request.node.name
    #print(f'zephyr_flash_firmware. test image: {test_image}')
    print(f'zephyr_flash_firmware. func_name: {func_name}')
    #if 'test_flash_firmware' in func_name:
    #    fw_update = True

    #if test_image:
    #    print(f'config data = {test_image}')

    #print(f'dut1_flash_tool = {conf_file.zephyr_dut1_flashtool}')
    #print(f'dut2_flash_tool = {conf_file.zephyr_dut2_flashtool}')

    if fw_update:
        #func_name = request.node.name
        print(f'zephyr_flash_firmware. test case : {func_name}')
        #print(f'fwfolderpath = {sd.config.fwfolderpath}')
        fwfolderpath = sd.config.fwfolderpath
        fwfolderpath += conf_file.zephyr_test_project
        fwfolderpath += "\\"
        print(f'zephyr_test_project = {conf_file.zephyr_test_project}')

        ipecmd = sd.config.mplab_path
        #tool = '-TSWBZ653002198'
        tool = '-TS' + conf_file.zephyr_dut1_flashtool
        if 'BZ6' in conf_file.zephyr_test_project:
            deviceid = '-P32WM_BZ6204'
            print('device: PIC32WM_BZ6204')
        elif 'BZ2' in conf_file.zephyr_test_project:
            deviceid = '-PWBZ451'
            print('device: WBZ451')
        elif 'BZ2' in conf_file.zephyr_test_project:
            deviceid = '-PWBZ351'
            print('device: WBZ351')
        else:
            deviceid = '-P32WM_BZ6204'

        print(f'dut1_flash_tool = {conf_file.zephyr_dut1_flashtool}')
        print(f'dut2_flash_tool = {conf_file.zephyr_dut2_flashtool}')

        erase = '-E'
        flashtype = '-M'
        reset = "-OL"
        verifyprogrammemory = "-YP"
        #flashfile = '-Fzephyr_signed.hex'
        flashfile = '-F.\\Test firmware\\Zephyr\\Peripheral_identity\\zephyr_signed.hex'
        #fwfolderpath += 'Peripheral_identity\\'

        if 'identity' in func_name.lower():
            flashfile = '-F.\\Test firmware\\Zephyr\\Peripheral_identity\\zephyr_signed.hex'
            fwfolderpath += 'Peripheral_identity\\'
        elif 'hid_pairing' in func_name.lower():
            flashfile = '-F.\\Test firmware\\Zephyr\\Peripheral_hid\\zephyr_signed.hex'
            fwfolderpath += 'Peripheral_hid\\'
        elif 'direct_advertising_pairing' in func_name.lower():
            flashfile = '-F.\\Test firmware\\Zephyr\\Direct advertising\\zephyr_signed.hex'
            fwfolderpath += 'Direct advertising\\'
        elif 'peripheral_application' in func_name.lower():
            flashfile = '-F.\\Test firmware\\Zephyr\\Peripheral_application\\zephyr_signed.hex'
            fwfolderpath += 'Peripheral_application\\'
        elif 'observer_application' in func_name.lower():
            fwfolderpath += 'Observer\\'
        elif 'broadcaster_observer' in func_name.lower():
            fwfolderpath += 'Multiple broadcaster\\'
            fw_update_dut2 = True
        elif 'central_gatt_write' in func_name.lower():
            fwfolderpath += 'Central Gatt Write\\'
            fw_update_dut2 = True

        #if test_image:
        #    print(f'test image = {test_image}')
        #    fwfolderpath += test_image
        #    fwfolderpath += '\\'

        print(f'fwfolderpath = {fwfolderpath}')
        print('DUT1 firmware update\n')

        ipe_comd = "C:\\Program Files\\Microchip\\MPLABX\\v6.25\\mplab_platform\\mplab_ipe\\ipecmd.exe -P32WM_BZ6204 -E -M -OL -TSWBZ653002198 -Fzephyr_signed.hex"
        #fw_path = 'C:\\Work\\Microchip\\Project\\Automation\\GitHub\\Test firmware\\Zephyr\\Peripheral_identity\\'
        ipe_cmds = [conf_file.mplab_path, deviceid, "-E -M -OL", tool, "-Fzephyr_signed.hex"]
        new_ipe_cmd = " ".join(ipe_cmds)
        print(f"new ipe comd = {new_ipe_cmd}")
        #process = subprocess.Popen(ipe_comd, cwd=fwfolderpath, stdout=subprocess.PIPE, universal_newlines=True)
        process = subprocess.Popen(new_ipe_cmd, cwd=fwfolderpath, stdout=subprocess.PIPE, universal_newlines=True)
        output_list = process.stdout.readlines()
        output = ' '.join(map(str, output_list))
        print(output)
        #if 'Program Succeeded' in output:
        #    print('Program Succeeded')
        #    time.sleep(2)
        #    if not fw_update_dut2:
        #        return True
        #    print('Update dut2...')

        if 'Program Succeeded' in output and not fw_update_dut2:
            print('Program Succeeded')
            return True
        else:
            return False

        print('DUT2 firmware update\n')

        fwfolderpath = sd.config.fwfolderpath
        fwfolderpath += conf_file.zephyr_test_project
        fwfolderpath += "\\"
        print(f'zephyr_test_project = {conf_file.zephyr_test_project}')

        if 'broadcaster_observer' in func_name.lower():
            fwfolderpath += 'Observer_extended\\'
        elif 'central_gatt_write' in func_name.lower():
            fwfolderpath += 'Central Peripheral test\\'

        print(f'fwfolderpath = {fwfolderpath}')

        tool = '-TS' + conf_file.zephyr_dut2_flashtool

        ipe_cmds = [conf_file.mplab_path, deviceid, "-E -M -OL", tool, "-Fzephyr_signed.hex"]
        new_ipe_cmd = " ".join(ipe_cmds)
        print(f"new ipe comd = {new_ipe_cmd}")
        # process = subprocess.Popen(ipe_comd, cwd=fwfolderpath, stdout=subprocess.PIPE, universal_newlines=True)
        process = subprocess.Popen(new_ipe_cmd, cwd=fwfolderpath, stdout=subprocess.PIPE, universal_newlines=True)
        output_list = process.stdout.readlines()
        output = ' '.join(map(str, output_list))
        print(output)
        if 'Program Succeeded' in output:
            print('Program Succeeded')
            time.sleep(2)
            return True
        else:
            return False

        '''
        bool_ipecmd_erase = subprocess.run([ipecmd, tool, deviceid, erase], capture_output=True)

        if bool_ipecmd_erase.returncode != 0:
            print(f'Erase fail:{str(bool_ipecmd_erase.stderr)}')
            #message('e ' + str(bool_ipecmd.stderr))
            return False
        else:
            print('Erase pass')
            time.sleep(2)

        bool_ipecmd_program = subprocess.run([ipecmd, tool, deviceid, flashtype, reset, flashfile], capture_output=True)

        if bool_ipecmd_program.returncode != 0:
            print(f'Program fail:{str(bool_ipecmd_program.stderr)}')
            #message('e ' + str(bool_ipecmd.stderr))
            return False
        else:
            print('Program pass')
            time.sleep(2)
            return True
        '''
    else:
        print(f'skip_flash_firmware. test case : {request.node.name}')
        return True

class TestZephyrApp:
    bleState = "Disconnected"
    operate_characteristic = ""
    hid_dut_name = ""
    test_procedure = ""

    def google_pixel_forget_device(self):
        print('google_pixel_forget_device')

    def Samsung_galaxy_settings(self, pair_unpair):
        print('Samsung_galaxy_forget_device.Settings ==> Connections')

        status, connections = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Connections"]')
        assert status, "Failed to find the element."
        connections.click()
        time.sleep(3)

        print('Connections ==> Bluetooth')
        status, bt = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Bluetooth"]')
        assert status, "Failed to find the element."
        bt.click()
        time.sleep(3)

        if pair_unpair == 'pair':
            print('Pairing...')
            status, dut_to_pair = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Test HoG mouse"]')
            assert status, "Failed to find the dut"
            time.sleep(1)
            dut_to_pair.click()
            print('Tap dut')
        else:
            status, dut = sd.mobile_driver.find_element('XPATH', '//android.widget.ImageView[@content-desc="Test HoG mouse, Device settings"]')
            assert status, "Failed to find the Test HoG mouse."
            dut.click()
            time.sleep(3)

            status, button = sd.mobile_driver.find_element('XPATH', '//android.widget.Button[@content-desc="Unpair"]')
            assert status, "Failed to find the unpair button"
            button.click()
            time.sleep(3)

            #print('Pairing alert message..')
            status, pairing = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.android.settings:id/alertTitle"]')
            assert status, "Failed to find the title"
            txt = pairing.text
            print(f'Pairing alert message: {txt}')
            time.sleep(3)

            status, unpair_button = sd.mobile_driver.find_element('XPATH', '//android.widget.Button[@resource-id="android:id/button1"]')
            assert status, "Failed to find the unpair button"
            unpair_button
            time.sleep(3)

    ################################################################################################
    #   Android phone test case
    ################################################################################################

    #@pytest.mark.order(1)
    #@pytest.mark.test_id("Zephyr Peripheral Android HID Pairing", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_android_hid_pairing")
    def test_zephyr_peripheral_android_hid_pairing_connect(self, zephyr_flash_firmware):
        print('test_zephyr_peripheral_android_hid_pairing_connect')
        TestZephyrApp.test_procedure = ''
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', self.MCU)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(2)
        sd.mobile_driver.close_app('com.android.settings')
        time.sleep(5)
        print("Launch setting app")
        sd.mobile_driver.launch_app('com.android.settings')
        time.sleep(5)
        print('DUT Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
        time.sleep(3)
        print('Settings ==> Connected Devices')
        status, connected_device = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Connected devices"]')
        assert status, "Failed to find the element."
        connected_device.click()
        time.sleep(3)
        status, id_1 = sd.mobile_driver.find_element('ID', 'Connected devices')
        assert status, "Failed to find the ID:Connected devices"
        print('Connected Devices ==> Pair new device')
        status, pair_device = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Pair new device"]')
        assert status, "Failed to find the element."
        pair_device.click()
        time.sleep(5)
        status, id_2 = sd.mobile_driver.find_element('ID', 'Pair new device')
        assert status, "Failed to find the ID:Pair new device"
        print('Pair new device ==> Discover and connect')
        status, dut = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Test HoG mouse"]')
        assert status, "Failed to find the Test HoG mouse."
        passkey = self.bleuartfeature.get_serial_data_passkey(dut)
        #print('Click. Test HoG mouse')
        #dut.click()
        time.sleep(1)
        status, alert = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.android.settings:id/alertTitle"]')
        assert status, "Failed to find the alert title."
        if 'Pair with Test HoG mouse' in alert.text:
            time.sleep(1)
            assert len(passkey) == 6, 'Passkey error!'
            print(f'Pairing. passkey={passkey}')
            status, edit = sd.mobile_driver.find_element('XPATH', '//android.widget.EditText[@resource-id="com.android.settings:id/text"]')
            assert status, "Failed to find the edit text."
            edit.send_keys(passkey)
            #edit.send_keys('727816')
            #print('Send passkey:727816')
            #edit.send_keys('123456')
            #print('Send passkey:123456')
            time.sleep(3)

        status, button = sd.mobile_driver.find_element('XPATH', '//android.widget.Button[@resource-id="android:id/button1"]')
        assert status, "Failed to find the element."
        if 'OK' in button.text:
            print(f'press ok button')
            button.click()
            time.sleep(15)

        #Check pairing success
        status, id_1 = sd.mobile_driver.find_element('ID', 'Connected devices')
        assert status, "Failed to find the ID:Connected devices"
        print('Pair new device == > Connected Devices')
        time.sleep(1)
        status, paired_dut = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Test HoG mouse"]')
        assert status, "Failed to find the Test HoG mouse."
        print('Pairing success')
        time.sleep(1)
        sd.mobile_driver.close_app('com.android.settings')
        time.sleep(5)
        TestZephyrApp.test_procedure = 'android_hid_pairing_connect'

    #@pytest.mark.order(2)
    #@pytest.mark.test_id("Zephyr Peripheral HID Android", '')
    @pytest.mark.skip(reason="test_zephyr_android_peripheral_hid")
    def test_zephyr_peripheral_android_hid_mouse_click(self):
        if TestZephyrApp.test_procedure != 'android_hid_pairing_connect':
            print('Unknown state:test_zephyr_peripheral_android_hid_mouse_click')
            return
        else:
            TestZephyrApp.test_procedure = ''

        print("Testing Zephyr Peripheral Android HID Mouse click. BLE Bonded")

        #self.iocontrolledstatus.Zephyr_InitMCP2200('115200', MCU)
        #time.sleep(1)

        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
        time.sleep(3)

        print('Launch HID test app')
        sd.mobile_driver.app_activate('com.microchip.zephyrtest')
        #sd.mobile_driver.launch_app('com.microchip.zephyrtest')
        time.sleep(5)

        print('Test HoG mouse. click test')

        status, click_button = sd.mobile_driver.find_element('id', 'zephyr_hid_test')
        assert status, "Failed to find the element id"
        time.sleep(1)

        state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(state))
        time.sleep(1)

        print('Click button 3 times.')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)

        new_state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(new_state))
        time.sleep(1)

        #assert state != new_state, "HID test failed"
        assert int(new_state)-int(state) == 3, 'HID test failed'
        #print('Remove paired device: Test HoG mouse')

        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
        time.sleep(5)

        state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(state))
        time.sleep(1)

        print('Click button 2 times.')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)

        new_state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(new_state))
        time.sleep(1)

        # assert state != new_state, "HID test failed"
        assert int(new_state) - int(state) == 2, 'HID test failed'
        #print('Remove paired device: Test HoG mouse')

        TestZephyrApp.test_procedure = 'android_hid_mouse_click'
        time.sleep(1)

    #@pytest.mark.order(3)
    @pytest.mark.skip(reason="test_zephyr_peripheral_android_hid_forget_device")
    #@pytest.mark.test_id("Zephyr Peripheral HID Android Forget device", '')
    def test_zephyr_peripheral_android_hid_forget_device(self):
        if TestZephyrApp.test_procedure != 'android_hid_mouse_click':
            print('Unknown state:test_zephyr_peripheral_android_hid_forget_device')
            return
        else:
            TestZephyrApp.test_procedure = ''

        print('test_zephyr_peripheral_android_hid_forget_device')

        self.google_pixel_forget_device()

        print('Activate settings app')
        sd.mobile_driver.app_activate('com.android.settings')

        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
        time.sleep(3)

        print('Settings ==> Connected Devices')
        status, connected_device = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Connected devices"]')
        assert status, "Failed to find the element."
        connected_device.click()
        time.sleep(3)

        status, id = sd.mobile_driver.find_element('ID', 'Connected devices')
        assert status, "Failed to find the ID:Connected devices"
        print('Connected Devices')
        time.sleep(1)

        status, paired_dut = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="android:id/title" and @text="Test HoG mouse"]')
        assert status, "Failed to find the Test HoG mouse."
        paired_dut.click()
        time.sleep(3)

        status, dev_details = sd.mobile_driver.find_element('ID', 'Device details')
        assert status, "Failed to find the ID:Device details."
        print(f"Connected Devices ==> {dev_details.text}")
        time.sleep(2)

        status, forget_button = sd.mobile_driver.find_element('XPATH', '//android.widget.Button[@resource-id="com.android.settings:id/button1"]')
        assert status, "Failed to find the Forget button."
        time.sleep(1)
        #print(f'Find button: {forget_button.text}')
        assert forget_button.text == 'Forget', 'Failed to find the Forget'
        print(f'Find Forget button')
        forget_button.click()
        time.sleep(3)

        #status, alert = sd.mobile_driver.find_element('ID', 'com.android.settings:id/alertTitle')
        status, alert = sd.mobile_driver.find_element('XPATH', '//android.widget.TextView[@resource-id="com.android.settings:id/alertTitle"]')
        assert status, "Failed to find the alert title."
        time.sleep(1)
        assert alert.text == 'Forget device?', "Alert title: Error"
        time.sleep(1)

        status, button = sd.mobile_driver.find_element('XPATH', '//android.widget.Button[@resource-id="android:id/button1"]')
        assert status, "Failed to find the Alert Forget button."
        time.sleep(1)
        assert button.text == 'Forget device', "Alert Forget device not found"
        time.sleep(1)
        button.click()
        print('Click Forget device button')
        time.sleep(2)

        status = self.iocontrolledstatus.Zephyr_IO_Default(self.MCU)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

    #@pytest.mark.order(4)
    #@pytest.mark.test_id("Zephyr Direct Advertising Pairing Connect", '')
    @pytest.mark.skip(reason="test_zephyr_direct_advertising Pairing Connect")
    def test_zephyr_direct_advertising_pairing_connect(self, zephyr_flash_firmware):
        print("Testing Zephyr Direct Advertising Pairing Connect")
        assert sd.mobile_platform == "Android", 'Test test case is only or Android phones'
        TestZephyrApp.test_procedure = ''
        print('ble state = {}'.format(TestZephyrApp.bleState))
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', self.MCU)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(2)
        # 3 option for pairing. (pairing timeout, pairing cancel, pairing accept)
        for i in range(3):
            if i in range(3):
                app_package = sd.mobile_driver.get_capability('appPackage')
                print("app package= {}".format(app_package))
                sd.mobile_driver.close_app(app_package)
                time.sleep(5)
                print("Launch app")
                sd.mobile_driver.launch_app(app_package)
                time.sleep(5)
                self.scanandconnect.verify_app_open()
                assert status, 'MBD open fail'
                time.sleep(3)
                print('DUT Reset. Firmware reset')
                self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
                print("open_ble_smart_scanner")
                self.scanandconnect.open_ble_smart_scanner()
                time.sleep(10)
            else:
                self.bleuartfeature.ble_smart_go_back()
                print('DUT Reset. Firmware reset')
                self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
                time.sleep(3)

            self.bleuartfeature.ble_smart_filter_peripherals('Direct A', search_icon=True)
            time.sleep(2)
            self.bleuartfeature.ble_smart_connect('Direct A')
            print('DeviceScan ==> Device')
            time.sleep(3)
            connection_state = self.bleuartfeature.ble_smart_verify_ble_connected('Direct A')
            assert connection_state == "Connected", 'Error, failed to connect to dut'
            TestZephyrApp.bleState = connection_state
            time.sleep(2)
            self.bleuartfeature.ble_smart_characteristic_write('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef2', '1234')
            if i == 0:
                action = 'timeout'
            elif i == 1:
                action = 'cancel'
            elif i == 2:
                action = 'accept'

            if 'Galaxy' in sd.platform and i == 2:
                print(f'Galaxy_platform = {sd.platform}')
                wait = WebDriverWait(sd.mobile_driver.driver, 5, poll_frequency=0.5)
                wait.until(EC.alert_is_present())
                print("Alert is present")
                result = self.bleuartfeature.ble_smart_pairing('Direct A', action)
            else:
                result = self.bleuartfeature.ble_smart_pairing_google_phone('Direct A', action)

            if i == 2:
                time.sleep(60)
                assert result, "[SMP_accept_pairing]Failed to parse the serial output data."
                TestZephyrApp.bleState = 'Pairing complete.Reset'
                print('Pairing complete')
                time.sleep(1)
            else:
                assert result, '[SMP_pairing_timeout_cancel]Failed to parse the serial output data.'

            '''
            #These code doesn't work on Google Pixel
            time.sleep(2)
            try:
                if i == 0:
                    action = 'timeout'
                elif i == 1:
                    action = 'cancel'
                elif i == 2:
                    action = 'accept'
                print('Pairing...')
                wait = WebDriverWait(sd.mobile_driver.driver, 5, poll_frequency=0.5)
                wait.until(EC.alert_is_present())
                print("Alert is present")
                result = self.bleuartfeature.ble_smart_pairing('Direct A', action)
                if result:
                    print('test result: PASS')
                else:
                    print('test result: FAIL')
                if action == 'accept':
                    print('Device reboot. Direct advertising start')
                    time.sleep(60)
                else:
                    time.sleep(5)
                #result = self.bleuartfeature.ble_smart_pairing('Direct A', 'timeout')
                #result = self.bleuartfeature.ble_smart_pairing('Direct A', 'accept')
            except WebDriverException:
                print('WebDriverException. Pairing alert ')
            '''

    #@pytest.mark.order(5)
    #@pytest.mark.test_id("Zephyr Direct Advertising Data Read/Write", '')
    @pytest.mark.skip(reason="test_zephyr_direct_advertising_gatt_read_write")
    def test_zephyr_direct_advertising_gatt_read_write(self):
        if TestZephyrApp.bleState != 'Pairing complete.Reset':
            print("test_zephyr_direct_advertising_gatt_read_write. Unknown state:{}".format(TestZephyrApp.bleState))
            return
        else:
            print('test_zephyr_direct_advertising_gatt_read_write')
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', self.MCU)
        time.sleep(2)
        print('Activate lightblue app')
        sd.mobile_driver.app_activate(sd.config.lightblue_app_package)
        time.sleep(10)
        app_package = sd.mobile_driver.get_capability('appPackage')
        print("app package= {}".format(app_package))
        sd.mobile_driver.close_app(sd.config.lightblue_app_package)
        time.sleep(3)
        print("Launch lightblue app")
        sd.mobile_driver.launch_app(sd.config.lightblue_app_package)
        time.sleep(3)
        self.bleuartfeature.ble_lightblue_Bonded('Direct A')
        time.sleep(1)
        sd.mobile_driver.close_app(sd.config.lightblue_app_package)
        time.sleep(3)
        print('Activate MBD app')
        sd.mobile_driver.app_activate(sd.config.app_package)
        time.sleep(3)
        status = self.scanandconnect.verify_app_open()
        assert status, "MBD open fail"
        time.sleep(3)
        print('DUT Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
        print("open_ble_smart_scanner")
        self.scanandconnect.open_ble_smart_scanner()
        time.sleep(10)
        self.bleuartfeature.ble_smart_filter_peripherals('Direct', search_icon=True)
        time.sleep(3)
        self.bleuartfeature.ble_smart_connect('Direct A')
        print('Ble connecting..')
        time.sleep(3)
        connection_state = self.bleuartfeature.ble_smart_verify_ble_connected('Direct A')
        assert connection_state == "Connected - Bonded", 'Error, failed to connect to dut'
        TestZephyrApp.bleState = connection_state
        print('state = {}'.format(TestZephyrApp.bleState))
        time.sleep(2)
        write_data = '12345678'
        self.bleuartfeature.ble_smart_characteristic_write('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef2', write_data)
        time.sleep(2)
        self.bleuartfeature.ble_smart_go_back()
        time.sleep(5)
        read_data = self.bleuartfeature.ble_smart_characteristic_read('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef1')
        time.sleep(2)
        self.bleuartfeature.ble_smart_go_back()
        time.sleep(5)
        write_data = '09abcdef'
        self.bleuartfeature.ble_smart_characteristic_write('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef2', write_data, char_found=True)
        time.sleep(2)
        self.bleuartfeature.ble_smart_go_back()
        time.sleep(5)
        read_data = self.bleuartfeature.ble_smart_characteristic_read('12345678-1234-5678-1234-56789abcdef0', '12345678-1234-5678-1234-56789abcdef1')
        time.sleep(2)
        self.bleuartfeature.ble_smart_go_back()
        time.sleep(5)
        TestZephyrApp.bleState = self.bleuartfeature.ble_smart_disconnect()
        print('ble state = {}'.format(TestZephyrApp.bleState))
        time.sleep(5)
        if TestZephyrApp.bleState == 'Disconnected - Bonded':
            print('test_zephyr_direct_advertising_unbond')
            state = self.bleuartfeature.ble_smart_unbond()
            print('ble state = {}'.format(state))
            time.sleep(3)
        else:
            print('test_zephyr_direct_advertising_unbond. Unknown state: {}'.format(TestZephyrApp.bleState))
            time.sleep(1)
        status = self.iocontrolledstatus.Zephyr_IO_Default(self.MCU)
        assert status, "[MCP2200 I/O state] Failed to restore to default"
        time.sleep(1)

    #@pytest.mark.test_id("Zephyr peripheral identity", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_identity")
    def test_zephyr_peripheral_identity(self, multilink_mobile_drivers):
        print('test_zephyr_peripheral_identity')
        assert len(sd.multilink_mobile_driver) == len(sd.config.multilink_phone_list), 'Fail to create drivers'
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', self.MCU)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(2)

        test_phones = []
        zephyr_test = []
        bt_address_arr = []
        for index, dat in enumerate(sd.multilink_mobile_driver):
            if index == 0:
                print('I/O Reset. Firmware reset')
                self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
            m_driver = dat['driver']
            m_phone = dat['phone']
            if 'Android' in m_phone:
                app = sd.config.lightblue_app_package
                lightblue_featuresupport = RNBDvsPhoneFeatureSupport(driver=m_driver)
                time.sleep(1)
            else:
                app = sd.config.ios_lightblue_app_package
                lightblue_featuresupport = BLEUARTFeatureSupportiOS(driver=m_driver)
                time.sleep(1)

            #app_package = m_driver.get_capability('appPackage')
            #print("app_package: {0}".format(app_package))
            #m_driver.close_app(app_package)
            m_driver.close_app(app)
            print(f'app restart. close app:{app}')
            time.sleep(5)
            #status = m_driver.launch_app(app_package)
            status = m_driver.launch_app(app)
            print('app restart')
            time.sleep(5)
            assert status, "Failed to launch lightblue app"
            time.sleep(2)

            lightblue_featuresupport.lightblue_filter_peripherals('Zephyr Peripheral')
            time.sleep(2)

            print(f'test phone: {m_phone}')
            ble_state = lightblue_featuresupport.lightblue_connect_and_verify_connected('Zephyr Peripheral')
            assert ble_state, 'Ble connect fail!'
            print('ble state: connected')
            '''
            lightblue_featuresupport.lightblue_connect('Zephyr Peripheral')
            print('Ble connecting..')
            time.sleep(5)

            status = lightblue_featuresupport.lightblue_verify_ble_connected()
            if not status:
                time.sleep(2)
                lightblue_featuresupport.lightblue_connect('Zephyr Peripheral')
                print('Ble connecting..again')
                time.sleep(5)
                status = lightblue_featuresupport.lightblue_verify_ble_connected()
                assert status, f'test phone: {m_phone}, connect fail'
            '''

            if 'Android' in m_phone:
                bt_address = m_driver.android_get_textview_bt_address()
                if bt_address != '':
                    print(f'BT address = {bt_address}')
                    bt_address_arr.append(bt_address)
            else:
                bt_address_arr.append('XX:XX:XX:XX:XX:XX')

            zephyr_test.append(lightblue_featuresupport)
            test_phones.append(m_phone)
            time.sleep(2)

        assert len(bt_address_arr) == len(sd.config.multilink_phone_list), 'Fail to find the bt address'
        assert len(bt_address_arr) == len(set(bt_address_arr)), print(f'Duplicate BT address')

        t1 = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        test_loop = 60  #145 sec
        #test_loop = 120  #294 sec
        print(f'Long-term idle test. test time = {t1}')
        idle_test_connected = True
        for i in range(test_loop):
            print(f'Running test:{i}')
            for j in range(len(zephyr_test)):
                app_driver = zephyr_test[j]
                status = app_driver.lightblue_verify_ble_connected()
                print(f'app:{j}, verify_ble_connected')
                if not status:
                    print(f'app:{j}, disconnect')
                    idle_test_connected = False
                    break
                time.sleep(1)
            if not idle_test_connected:
                break
        t1 = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        print(f'multilink long-term idle test complete. time = {t1}')

        status = self.iocontrolledstatus.Zephyr_IO_Default(self.MCU)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        assert idle_test_connected, 'BLE idle long-term test: Fail'

    ################################################################################################
    #   iOS iPhone test case
    ################################################################################################

    #@pytest.mark.order(3)
    #@pytest.mark.skip(reason="test_zephyr_peripheral_hid_forget_device")
    @pytest.mark.test_id("Zephyr Peripheral HID Forget Device", '')
    def test_zephyr_peripheral_hid_forget_device(self):
        print("test_zephyr_peripheral_hid_forget_device")
        sd.mobile_driver.app_activate(sd.config.ios_settings_app_package)
        time.sleep(5)
        pairing = iOSBLEPairingSupport()
        #pairing.ios_delete_pairing_record('Test HoG mouse')
        print('HID dut = {}'.format(TestZephyrApp.hid_dut_name))
        pairing.check_dut_is_paired_connected(TestZephyrApp.hid_dut_name, delete=True)
        time.sleep(5)
        status = self.iocontrolledstatus.Zephyr_IO_Default(self.MCU)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)
        #status = pairing.check_and_forget('Test HoG mouse')
        #assert status, 'Remove pairing: Failed'

    #@pytest.mark.order(1)
    @pytest.mark.test_id("Zephyr Peripheral HID Pairing", '')
    #@pytest.mark.skip(reason="test_zephyr_peripheral_hid_pairing")
    def test_zephyr_peripheral_hid_pairing_connect(self, zephyr_flash_firmware):
        print("test_zephyr_peripheral_hid_pairing_connect")
        print('Active app = {}'.format(sd.config.ios_lightblue_app_package))
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', self.MCU)
        time.sleep(2)
        print('DUT Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
        sd.mobile_driver.app_activate(sd.config.ios_lightblue_app_package)
        scan_time = 6
        time.sleep(scan_time)
        print('scan time = {}'.format(scan_time))
        TestZephyrApp.hid_dut_name = 'Test HoG mouse'
        self.bleuartfeature.lightblue_filter_peripherals('Test HoG mouse')
        time.sleep(3)
        print("Connect")
        passkey = self.bleuartfeature.lightblue_pairing_connect('Test HoG mouse')
        #time.sleep(10)
        try:
            print('Pairing...')
            wait = WebDriverWait(sd.mobile_driver.driver, 5, poll_frequency=0.5)
            wait.until(EC.alert_is_present())
            print("Alert is present")
            if len(passkey) == 6:
                self.bleuartfeature.pairing_alert_sendkey('Test HoG mouse', passkey)
            else:
                print("Bluetooth Pairing is failed")
            time.sleep(5)
        except WebDriverException:
            print('WebDriverException')

        status = sd.mobile_driver.close_app(sd.config.ios_lightblue_app_package)
        assert status, "Failed to close application"
        print("Close lightblue app")

    #@pytest.mark.order(1)
    #@pytest.mark.test_id("Zephyr Peripheral HID Pairing", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_hid_pairing")
    def test_zephyr_peripheral_hid_pairing_connect_1(self):
        print("test_zephyr_peripheral_hid_pairing_connect")
        print('Active app = {}'.format(sd.config.ios_settings_app_package))
        sd.mobile_driver.app_activate(sd.config.ios_settings_app_package)
        time.sleep(5)
        sd.mobile_driver.close_app(sd.config.ios_settings_app_package)
        time.sleep(5)
        sd.mobile_driver.launch_app(sd.config.ios_settings_app_package)
        #print('Scanning...')
        time.sleep(5)
        pairing = iOSBLEPairingSupport()

        print("Verify Settings App is open")
        app_open = pairing.verify_settings_open()
        assert app_open, "Failed to open Settings application"
        time.sleep(3)

        #MCU = Mcp2200()
        #time.sleep(1)
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', self.MCU)
        time.sleep(2)

        print('DUT Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
        time.sleep(3)

        print("Open Bluetooth Page")
        bt_open = pairing.open_bluetooth()
        assert bt_open, "Failed to Open Bluetooth page"
        scan_time = 10
        print('Scanning...time={}'.format(scan_time))
        time.sleep(scan_time)

        passkey = pairing.get_dut_pair_passkey('Test HoG mouse')
        try:
            print('Pairing...')
            wait = WebDriverWait(sd.mobile_driver.driver, 5, poll_frequency=0.5)
            wait.until(EC.alert_is_present())
            print("Alert is present")
            if len(passkey) == 6:
                pairing.pairing_alert_sendkey('Test HoG mouse', passkey)
            else:
                print("Bluetooth Pairing is failed")
            time.sleep(5)
        except WebDriverException:
            print('WebDriverException')

    #@pytest.mark.order(2)
    @pytest.mark.test_id("Zephyr Peripheral HID", '')
    #@pytest.mark.skip(reason="test_zephyr_peripheral_hid")
    def test_zephyr_peripheral_hid_mouse_click(self):
        print("Testing Zephyr Peripheral HID Mouse click. BLE Bonded")
        print("Make sure all of the paired devices are deleted")
        if sd.mobile_platform == "iOS":
            sd.mobile_driver.app_activate(sd.config.ios_settings_app_package)
            time.sleep(5)
            sd.mobile_driver.close_app(sd.config.ios_settings_app_package)
            time.sleep(5)
            sd.mobile_driver.launch_app(sd.config.ios_settings_app_package)
        else:
            print('Platform "Android" not supported')
        time.sleep(5)
        print('Launch ios setting, Check BLE connection')

        #MCU = Mcp2200()
        #time.sleep(1)
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', self.MCU)
        time.sleep(1)

        iOSpairingsupport = iOSBLEPairingSupport(sd.mobile_driver)

        print("Verify Settings App is open")
        app_open = iOSpairingsupport.verify_settings_open()
        assert app_open, "Failed to open Settings application"
        time.sleep(5)

        print('I/O Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
        time.sleep(3)

        print("Open Bluetooth Page")
        bt_open = iOSpairingsupport.open_bluetooth()
        assert bt_open, "Failed to Open Bluetooth page"
        time.sleep(3)

        iOSpairingsupport.check_dut_is_paired_connected(TestZephyrApp.hid_dut_name)
        #status = iOSpairingsupport.check_dut_paired_connected('Test HoG mouse')
        #assert status == 'Connected', "Failed to find the paired device: Test HoG mouse"
        time.sleep(3)

        print('Launch HID test app')
        sd.mobile_driver.app_activate('com.microchip.MBDtest')

        print('Test HoG mouse. click test')

        status, click_button = sd.mobile_driver.find_element('id', 'zephyr_hid_test')
        assert status, "Failed to find the element id"
        time.sleep(1)
        state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(state))
        time.sleep(1)

        print('Click button 3 times.')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, BTN_CTRL_PIN, 0.3)
        time.sleep(3)

        new_state = sd.mobile_driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(new_state))

        status = sd.mobile_driver.close_app('com.microchip.MBDtest')
        assert status, "Failed to close application"
        time.sleep(5)

        assert state != new_state, "HID test failed"
        #print('Remove paired device: Test HoG mouse')
        assert int(new_state) - int(state) == 3, 'HID test failed'

    #@pytest.mark.order(1)
    @pytest.mark.test_id("Zephyr peripheral application", '')
    #@pytest.mark.skip(reason="test_zephyr_peripheral_rc5")
    #def test_zephyr_peripheral_application(self, zephyr_flash_firmware):
    def test_zephyr_peripheral_application(self):
        print("Testing Zephyr Peripheral application.")
        sd.mobile_driver.close_app(sd.config.ios_lightblue_app_package)
        time.sleep(5)
        print("Close app and launch again")
        sd.mobile_driver.launch_app(sd.config.ios_lightblue_app_package)
        time.sleep(5)
        print('test_zephyr_peripheral_application_v1_rc5')
        if platform.system() == "Windows":
            status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', self.MCU)
            assert status, "Failed to initialize the MCP2200"
            time.sleep(1)
            print('I/O Reset. Firmware reset')
            self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)
            time.sleep(3)
        print("Search peripherals by name")
        time.sleep(3)
        self.bleuartfeature.lightblue_filter_peripherals('Zephyr Peripheral')
        time.sleep(3)
        print("Connect")
        self.bleuartfeature.lightblue_connect('Zephyr Peripheral Sample Long')
        #self.bleuartfeature.lightblue_connect('Zephyr Peripheral Sample Long Name')
        time.sleep(10)
        self.bleuartfeature.lightblue_verify_ble_connected()
        time.sleep(3)
        self.bleuartfeature.lightblue_get_device_info_data()
        time.sleep(3)
        self.bleuartfeature.lightblue_verify_ble_services_characteristics()
        time.sleep(3)
        #self.bleuartfeature.lightblue_scroll_gesture('0', scroll_element='Immediate Alert', direction='down')
        #time.sleep(3)
        #self.bleuartfeature.lightblue_scroll_gesture('0', scroll_element='Device Information', direction='down')
        #time.sleep(3)
        #self.bleuartfeature.lightblue_get_device_info_data()
        #time.sleep(3)
        self.bleuartfeature.lightblue_ble_disconnect()
        if platform.system() == "Windows":
            status = self.iocontrolledstatus.Zephyr_IO_Default(self.MCU)
            assert status, "[MCP2200 I/O state] Failed to restore to default"
            time.sleep(1)

    ################################################################################################
    #   DUT only test case
    ################################################################################################

    @pytest.mark.skip(reason="test_zephyr_observer")
    #@pytest.mark.test_id("Zephyr observer application", '')
    def test_zephyr_observer_application(self, zephyr_flash_firmware):
        assert zephyr_flash_firmware, 'zephyr flash firmware: Fail'
        time.sleep(1)
        print('test_zephyr_observer_application')
        dut_mcu = Mcp2200(PID='0x00dc')
        print(f'dut_mcp2200.PID = {dut_mcu.pid}')
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', dut_mcu)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(1)

        serial_runner = SerialReader(conf_file.com_port, baudrate=115200)
        time.sleep(1)

        def dut_reset():
            print('DUT Reset. Firmware reset')
            self.iocontrolledstatus.Zephyr_IOCtrl(dut_mcu, RESET_PIN, 1)
            return 'reset_dut'

        serial_runner.settings(15)
        result, serial_data = serial_runner.execute(dut_reset)
        # print(f'task = {result}, data = {serial_data}')
        assert len(serial_data) != 0, "Can't get the serial data"
        if len(serial_data) > 20:
            print(f'task = {result}\n')
            for i in range(20):
                print(f'{serial_data[i]}')
        else:
            dd = ''.join(serial_data)
            print(f'task = {result}, data = {dd}')
        #dd = ''.join(serial_data)
        #print(f'task = {result}, data = {dd}')

        status = self.iocontrolledstatus.Zephyr_IO_Default(dut_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        expected_data = ["Starting Observer Demo",
                         "Started scanning..."
                         ]
        print(f'parsing serial data. len = {len(serial_data)}')

        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        assert len(expected_result) != 0, "The test result did not meet expectations "
        # print("Success")

        # Device found: CF:2D:0E:1B:06:C3 (random) (RSSI -85), type 0, AD data len 24
        pattern = r"Device found: (?:[0-9A-F]{2}:){5}[0-9A-F]{2} \(random\) \(RSSI -?\d+\), type \d+, AD data len \d+"

        print('Scan Device')
        pattern_test_result = serial_runner.search_test_pattern_1(serial_data, pattern, count=5)
        assert len(pattern_test_result) >= 3, "The test result did not meet expectations "
        print("Pass")

    #@pytest.mark.order(1)
    # @pytest.mark.test_id("Zephyr broadcaster observer 1", '')
    @pytest.mark.skip(reason="test_zephyr_broadcaster_observer_1")
    def test_zephyr_broadcaster_observer_1(self, zephyr_flash_firmware):
        assert zephyr_flash_firmware, 'zephyr flash firmware: Fail'
        time.sleep(1)
        print('test_zephyr_broadcaster_observer_1')
        dut_mcu = Mcp2200(PID='0x00dc')
        print(f'dut_mcp2200.PID = {dut_mcu.pid}')
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', dut_mcu)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(1)

        serial_runner = SerialReader(conf_file.com_port, baudrate=115200)
        time.sleep(1)

        def dut_reset():
            print('DUT Reset. Firmware reset')
            self.iocontrolledstatus.Zephyr_IOCtrl(dut_mcu, RESET_PIN, 1)
            return 'reset_dut'

        serial_runner.settings(15)
        result, serial_data = serial_runner.execute(dut_reset)
        assert len(serial_data) != 0, "Can't get the serial data"
        dd = ''.join(serial_data)
        print(f'task = {result}, data = {dd}')
        status = self.iocontrolledstatus.Zephyr_IO_Default(dut_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        # Broadcaster role
        expected_data = ["Started Extended Advertising Set 0",
                         "Started Extended Advertising Set 1"]

        #print(f'parsing serial data. len = {len(serial_data)}')
        print('Started Extended Advertising')

        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        assert len(expected_result) != 0, "The test result did not meet expectations"
        print("Success")

    #@pytest.mark.order(2)
    # @pytest.mark.test_id("Zephyr broadcaster observer 2", '')
    @pytest.mark.skip(reason="test_zephyr_broadcaster_observer_2")
    def test_zephyr_broadcaster_observer_2(self):
        print('test_zephyr_broadcaster_observer_2')
        dut_mcu = Mcp2200(PID='0x00da')
        print(f'dut_mcp2200.PID = {dut_mcu.pid}')
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', dut_mcu)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(1)

        serial_runner = SerialReader(conf_file.zephyr_dut2_com_port, baudrate=115200)
        time.sleep(1)

        def dut_reset():
            print('DUT Reset. Firmware reset')
            self.iocontrolledstatus.Zephyr_IOCtrl(dut_mcu, RESET_PIN, 1)
            return 'reset_dut'

        serial_runner.settings(15)
        result, serial_data = serial_runner.execute(dut_reset)
        assert len(serial_data) != 0, "Can't get the serial data"
        if len(serial_data) > 20:
            print(f'task = {result}\n')
            for i in range(20):
                print(f'{serial_data[i]}')
        else:
            dd = ''.join(serial_data)
            print(f'task = {result}, data = {dd}')
        status = self.iocontrolledstatus.Zephyr_IO_Default(dut_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        # observer_extended role
        expected_data = ["Starting Observer Demo",
                         "Registered scan callback",
                         "Started scanning"
                         ]
        #print(f'parsing serial data. len = {len(serial_data)}')

        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        assert len(expected_result) != 0, "The test result did not meet expectations "

        # [DEVICE]: 34:79:6D:7C:C5:5E (random), AD evt type 5, Tx Pwr: 127, RSSI -25 Data status: 0, AD data len: 31 Name: Broadcaster Multiple C:0 S:0 D:0 SR:0 E:1 Pri PHY: LE 1M, Sec PHY: LE 2M, Interval: 0x0000 (0 ms), SID: 0
        # [DEVICE]: 1E:97:9E:BF:51:31 (random), AD evt type 5, Tx Pwr: 127, RSSI -25 Data status: 0, AD data len: 31 Name: Broadcaster Multiple C:0 S:0 D:0 SR:0 E:1 Pri PHY: LE 1M, Sec PHY: LE 2M, Interval: 0x0000 (0 ms), SID: 1
        print("Started scanning\n")

        pattern_sid = (
            r"\[DEVICE\]: (?:[0-9A-F]{2}:){5}[0-9A-F]{2} \(\w+\), "
            r"AD evt type \d+, Tx Pwr: -?\d+, RSSI -?\d+ "
            r"Data status: \d+, AD data len: \d+ "
            r"Name: Broadcaster Multiple "
            r"C:\d+ S:\d+ D:\d+ SR:\d+ E:\d+ "
            r"Pri PHY: [\w\s]+, Sec PHY: [\w\s]+, "
            r"Interval: 0x[0-9A-F]+ \(\d+ ms\), SID: \d+"
        )

        expected_data = ["SID: 0", "SID: 1"]
        pattern_test_result = serial_runner.search_test_pattern_with_keyword(serial_data, pattern_sid, expected_data)
        assert len(pattern_test_result) == len(expected_data), "The test result did not meet expectations "
        # print("Test pattern_sid_0_1: Pass ")
        print("Scan result: \n")
        for result in pattern_test_result:
            print(f"{result}")

    #@pytest.mark.order(3)
    # @pytest.mark.test_id("Zephyr central gatt write 1", '')
    @pytest.mark.skip(reason="test_zephyr_central_gatt_write_1")
    def test_zephyr_central_gatt_write_1(self, zephyr_flash_firmware):
        assert zephyr_flash_firmware, 'zephyr flash firmware: Fail'
        time.sleep(1)
        print('test_zephyr_central_gatt_write_1')
        dut_mcu = Mcp2200(PID='0x00dc')
        print(f'dut_mcp2200.PID = {dut_mcu.pid}')
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', dut_mcu)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(1)

        serial_runner = SerialReader(conf_file.com_port, baudrate=115200)
        time.sleep(1)

        def dut_reset():
            print('DUT Reset. Firmware reset')
            self.iocontrolledstatus.Zephyr_IOCtrl(dut_mcu, RESET_PIN, 1)
            return 'reset_dut'

        serial_runner.settings(10)
        result, serial_data = serial_runner.execute(dut_reset)
        assert len(serial_data) != 0, "Can't get the serial data"
        dd = ''.join(serial_data)
        print(f'task = {result}, data = {dd}')
        status = self.iocontrolledstatus.Zephyr_IO_Default(dut_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        # Central role
        expected_data = ["start_scan: Scanning successfully started"]

        #print(f'parsing serial data. len = {len(serial_data)}')

        print("Central: start")
        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        assert len(expected_result) != 0, "The test result did not meet expectations"
        print("Scanning successfully")

    #@pytest.mark.order(4)
    # @pytest.mark.test_id("Zephyr central gatt write 2", '')
    @pytest.mark.skip(reason="test_zephyr_central_gatt_write_2")
    def test_zephyr_central_gatt_write_2(self):
        print('test_zephyr_central_gatt_write_2')
        dut_mcu = Mcp2200(PID='0x00da')
        print(f'dut_mcp2200.PID = {dut_mcu.pid}')
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', dut_mcu)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(1)

        serial_runner = SerialReader(conf_file.zephyr_dut2_com_port, baudrate=115200)
        time.sleep(1)

        def dut_reset():
            print('DUT Reset. Firmware reset')
            self.iocontrolledstatus.Zephyr_IOCtrl(dut_mcu, RESET_PIN, 1)
            return 'reset_dut'

        serial_runner.settings(15)
        result, serial_data = serial_runner.execute(dut_reset)
        assert len(serial_data) != 0, "Can't get the serial data"
        dd = ''.join(serial_data)
        print(f'task = {result}, data = {dd}')
        status = self.iocontrolledstatus.Zephyr_IO_Default(dut_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        # peripheral role
        expected_data = ["Advertising successfully started",
                         "Connected",
                         "Updated MTU: TX: 247 RX: 247 bytes"
                         ]
        #print(f'parsing serial data. len = {len(serial_data)}')

        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        assert len(expected_result) != 0, "The test result did not meet expectations"
        print("peripheral log: \n")
        for result in expected_result:
            print(f"{result}")

    #@pytest.mark.order(5)
    # @pytest.mark.test_id("Zephyr central gatt write 3", '')
    @pytest.mark.skip(reason="test_zephyr_central_gatt_write_3")
    def test_zephyr_central_gatt_write_3(self):
        print('test_zephyr_central_gatt_write_3')
        dut_mcu = Mcp2200(PID='0x00dc')
        print(f'dut1_mcp2200.PID = {dut_mcu.pid}')
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', dut_mcu)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(1)

        serial_runner = SerialReader(conf_file.com_port, baudrate=115200)
        time.sleep(1)

        def dut_reset():
            print('DUT Reset. Firmware reset')
            # self.iocontrolledstatus.Zephyr_IOCtrl(dut2_mcu, RESET_PIN, 0.3)
            self.iocontrolledstatus.Zephyr_IOCtrl(dut_mcu, RESET_PIN, 1)
            return 'reset_dut'

        serial_runner.settings(10)
        result, serial_data = serial_runner.execute(dut_reset)
        # print(f'task = {result}, data = {serial_data}')

        status = self.iocontrolledstatus.Zephyr_IO_Default(dut_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        dd = ''.join(serial_data)
        print(f'task = {result}, data = {dd}')

        pattern = r"write_cmd_cb: count= \d+, len= \d+, rate= \d+ bps"
        pattern_test_result = serial_runner.search_test_pattern_1(serial_data, pattern, count=3)
        assert len(pattern_test_result) == 3, "The test result did not meet expectations "
        for result in pattern_test_result:
            print(f"{result}")
        print("Central gatt write: success")

    ################################################################################################

    @pytest.mark.skip(reason="test_serial_parser")
    #@pytest.mark.test_id("test_serial_parser", '')
    def test_serial_parser(self):
        print('test_dut_serial')
        serial_runner = SerialReader('COM24', baudrate=115200)
        time.sleep(1)

        serial_data = ["Hello world", "Devops test automation"]
        #serial_data = ["Hello world"]

        expected_data = ["Hello",
                         "world",
                         "abcd"]

        print(f'parsing serial data. len = {len(serial_data)}')

        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        print(f"result = {expected_result}")
        #assert len(expected_result) != 0, "The test result did not meet expectations"
        #print("Success")

    @pytest.mark.skip(reason="test_dut_serial")
    #@pytest.mark.test_id("test dut serial", '')
    def test_dut_serial(self):
        print('test_dut_serial')
        serial_runner = SerialReader('COM24', 'COM18', baudrate=115200, dut_only=True)
        time.sleep(1)

        def dut_reset():
            print('DUT1,DUT2 Reset. Firmware reset')
            print('Reset dut manually')
            return 'reset_dut1_dut2'

        print(f'time = {datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}')
        serial_runner.settings(60)
        result, data = serial_runner.dut_execute(dut_reset)
        print(f'time = {datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}')
        #print(f'serial_data1 = {data[0]}')
        #print(f'serial_data2 = {data[1]}')

        time.sleep(3)

        #serial_runner = SerialReader('COM24', baudrate=115200)
        #time.sleep(1)

        #serial_runner.settings(30)
        #result, data = serial_runner.execute(dut_reset)
        #print(f'serial_data = {data}')

        #print('parsing serial data.')
        data_lines = data[0]
        keyword_sets = ["start_scan: scanning successfully started", "mtu_exchange_cb: mtu exchange successful"]
        print(f'parsing serial data. len = {len(data_lines)}')

        serial_runner.search_keyword_sets_ordered(data_lines, keyword_sets)

        #result = serial_runner.search_keyword_sets_ordered(data_lines, keyword_sets)
        #for i, res in enumerate(result):
        #    if res != -1:
        #        print(f"Set {i + 1} first found at line {res + 1}: {data_lines[res]}")
        #    else:
        #        print(f"Set {i + 1} not found after previous matches.")

        '''
        data_lines = [
            "The quick brown fox jumps over the lazy dog",
            "The dog jumps over the quick fox quickly",
            "Somewhere later the quick brown fox appears again",
            "Finally, all the keywords are collected together",
        ]

        #start_scan: Scanning successfully started
        keyword_sets = [
            ["quick", "fox"],  # first set
            ["dog", "quick"],  # second set (must come *after* the first fox)
            ["collected", "keywords"]  # third set
        ]


        result = serial_runner.search_keyword_sets_ordered(data_lines, keyword_sets)
        for i, res in enumerate(result):
            if res != -1:
                print(f"Set {i + 1} first found at line {res + 1}: {data_lines[res]}")
            else:
                print(f"Set {i + 1} not found after previous matches.")
        '''

    @pytest.mark.skip(reason="test android setting app")
    #@pytest.mark.test_id("test_android_iop_settings_app", '')
    def test_android_iop_settings_app(self):
        print(f'test_android_iop_settings_app. platform = {sd.platform}')
        sd.mobile_driver.close_app('com.android.settings')
        time.sleep(5)
        print("Launch setting app")
        sd.mobile_driver.launch_app('com.android.settings')
        time.sleep(5)

        com_port = conf_file.com_port

        serial_runner = SerialReader(com_port, baudrate=115200)
        serial_runner.settings(10)
        time.sleep(1)

        status, connections = sd.mobile_driver.find_element('XPATH',
                                                            '//android.widget.TextView[@resource-id="android:id/title" and @text="Connections"]')
        assert status, "Failed to find the element."
        connections.click()
        time.sleep(3)

        print('DUT Reset. Firmware reset')
        self.iocontrolledstatus.Zephyr_IOCtrl(self.MCU, RESET_PIN, 0.3)

        print('Connections ==> Bluetooth')
        status, bt = sd.mobile_driver.find_element('XPATH',
                                                   '//android.widget.TextView[@resource-id="android:id/title" and @text="Bluetooth"]')
        assert status, "Failed to find the element."
        bt.click()

        time.sleep(5)

        def dut_tap():
            status, button = sd.mobile_driver.find_element('XPATH', '//android.widget.Button[@text="Stop"]')
            assert status, "Failed to find the stop button"
            button.click()
            print('Scan stop')
            time.sleep(3)
            tap_status = sd.mobile_driver.android_listactivity_tap_dut('Test HoG mouse')
            assert tap_status, "Failed to find the dut"
            return 'Tap dut'

        result, serial_data = serial_runner.execute(dut_tap)
        print(f'task = {result}, data = {serial_data}')

    @pytest.mark.skip(reason="test central gatt write")
    #@pytest.mark.test_id("test central gatt write", '')
    def test_central_gatt_write(self):
        print('test_central_gatt_write')
        time.sleep(1)
        # dut1: ble central
        # dut2: ble peripheral
        dut2_mcu = Mcp2200(PID='0x00da')

        #dut1_serial_runner = SerialReader(conf_file.com_port, baudrate=115200)
        dut2_serial_runner = SerialReader(conf_file.zephyr_dut2_com_port, baudrate=115200)
        time.sleep(1)

        def dut1_reset():
            print('DUT 1 Reset. Firmware reset')
            #self.iocontrolledstatus.Zephyr_IOCtrl(MCU, RESET_PIN, 0.3)
            return 'reset_dut1'

        self.iocontrolledstatus.Zephyr_InitMCP2200(conf_file.baud_rate, dut2_mcu)
        time.sleep(0.5)

        def dut2_reset():
            print('DUT 2 Reset. Firmware reset')
            self.iocontrolledstatus.Zephyr_IOCtrl(dut2_mcu, RESET_PIN, 0.3)
            return 'reset_dut2'

        result, serial_data2 = dut2_serial_runner.execute(dut2_reset)
        print(f'task = {result}, data = {serial_data2}')

    @pytest.mark.skip(reason="test_dut1_2 io reset")
    #@pytest.mark.test_id("test dut1_2 io reset", '')
    def test_dut_1_2_io_reset(self):
        dut1_mcu = Mcp2200(PID='0x00dc')
        status = self.iocontrolledstatus.Zephyr_IO_Default(dut1_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(2)
        dut2_mcu = Mcp2200(PID='0x00da')
        status = self.iocontrolledstatus.Zephyr_IO_Default(dut2_mcu)
        assert status, "Failed to set MCP2200 I/O default"

    @pytest.mark.skip(reason="test_dut_special_test")
    #@pytest.mark.test_id("test dut special test", '')
    def test_dut_special_test(self):
        print('test_dut1_dut2_reset')
        time.sleep(1)
        #dut1: broadcaster, central
        #dut2: observer, peripheral
        dut1_mcu = Mcp2200(PID='0x00dc')
        self.iocontrolledstatus.Zephyr_InitMCP2200('115200', dut1_mcu)
        #dut2_mcu = Mcp2200(PID='0x00da')

        dut1_serial_runner = SerialReader(conf_file.com_port, baudrate=115200)
        dut2_serial_runner = SerialReader(conf_file.zephyr_dut2_com_port, baudrate=115200)
        time.sleep(1)

        def dut1_reset():
            print('DUT 1 Reset. Firmware reset')
            #self.iocontrolledstatus.Zephyr_IOCtrl(dut1_mcu, RESET_PIN, 0.3)
            self.iocontrolledstatus.Zephyr_IOCtrl(dut1_mcu, RESET_PIN, 1)
            return 'reset_dut1'

        print(f'time = {datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}')
        dut1_serial_runner.settings(5)
        result, serial_data1 = dut1_serial_runner.execute(dut1_reset)
        print(f'task = {result}, data = {serial_data1}')
        print(f'time = {datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}')

        status = self.iocontrolledstatus.Zephyr_IO_Default(dut1_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(3)

        #status = self.iocontrolledstatus.Zephyr_IO_Default(dut1_mcu)
        #assert status, "Failed to set MCP2200 I/O default"
        #time.sleep(1)
        dut1_mcu.Release()
        time.sleep(1)
        del dut1_mcu
        time.sleep(1)

        dut2_mcu = Mcp2200(PID='0x00da')
        self.iocontrolledstatus.Zephyr_InitMCP2200(conf_file.baud_rate, dut2_mcu)
        time.sleep(2)

        def dut2_reset():
            print('DUT 2 Reset. Firmware reset')
            #self.iocontrolledstatus.Zephyr_IOCtrl(dut2_mcu, RESET_PIN, 0.3)
            self.iocontrolledstatus.Zephyr_IOCtrl(dut2_mcu, RESET_PIN, 1)
            return 'reset_dut2'

        print(f'time = {datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}')
        dut2_serial_runner.settings(5)
        result, serial_data2 = dut2_serial_runner.execute(dut2_reset)
        print(f'task = {result}, data = {serial_data2}')
        print(f'time = {datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}')

        status = self.iocontrolledstatus.Zephyr_IO_Default(dut2_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        dut2_mcu.Release()
        time.sleep(1)
        del dut2_mcu
        time.sleep(1)

    @pytest.mark.skip(reason="test flash firmware")
    #@pytest.mark.test_id("test flash firmware", '')
    #@pytest.mark.parametrize('zephyr_flash_firmware', [conf_file.zephyr_dut1_flashtool + "_" + 'Peripheral_hid'], indirect=True)
    #@pytest.mark.order(1)
    #def test_flash_firmware_broadcaster_observer(self, zephyr_flash_firmware):
    def test_flash_firmware_central_gatt_write(self, zephyr_flash_firmware):
    #def test_flash_firmware_hid_pairing(self, zephyr_flash_firmware):
        #print('test_flash_firmware.broadcaster_observer')
        #print('test_flash_firmware.hid_pairing')
        print('test_flash_firmware_central_gatt_write')
        time.sleep(1)
        assert zephyr_flash_firmware, 'Test flash firmware: Fail'
        print('Success')

    @pytest.mark.skip(reason="test_dut2_reset")
    #@pytest.mark.test_id("test_dut2_reset", '')
    #@pytest.mark.order(2)
    def test_dut2_reset(self):
        print('test_dut2_reset')
        dut2_mcu = Mcp2200(PID='0x00da')
        print(f'dut2_mcp2200.PID = {dut2_mcu.pid}')
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', dut2_mcu)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(1)

        serial_runner = SerialReader('COM18', baudrate=115200)
        time.sleep(1)

        def dut_reset():
            print('DUT Reset. Firmware reset')
            #self.iocontrolledstatus.Zephyr_IOCtrl(dut2_mcu, RESET_PIN, 0.3)
            self.iocontrolledstatus.Zephyr_IOCtrl(dut2_mcu, RESET_PIN, 1)
            return 'reset_dut2'

        serial_runner.settings(30)
        result, serial_data = serial_runner.execute(dut_reset)
        #print(f'task = {result}, data = {serial_data}')

        status = self.iocontrolledstatus.Zephyr_IO_Default(dut2_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        dd = ''.join(serial_data)
        print(f'task = {result}, data = {dd}')

        '''
        # observer_extended role
        expected_data = ["Starting Observer Demo",
                         "Registered scan callback",
                         "Started scanning"
                         ]
        print(f'parsing serial data. len = {len(serial_data)}')

        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        assert len(expected_result) != 0, "The test result did not meet expectations "

        #[DEVICE]: 34:79:6D:7C:C5:5E (random), AD evt type 5, Tx Pwr: 127, RSSI -25 Data status: 0, AD data len: 31 Name: Broadcaster Multiple C:0 S:0 D:0 SR:0 E:1 Pri PHY: LE 1M, Sec PHY: LE 2M, Interval: 0x0000 (0 ms), SID: 0
        #[DEVICE]: 1E:97:9E:BF:51:31 (random), AD evt type 5, Tx Pwr: 127, RSSI -25 Data status: 0, AD data len: 31 Name: Broadcaster Multiple C:0 S:0 D:0 SR:0 E:1 Pri PHY: LE 1M, Sec PHY: LE 2M, Interval: 0x0000 (0 ms), SID: 1
        print("keyword: Pass")

        pattern_sid = (
            r"\[DEVICE\]: (?:[0-9A-F]{2}:){5}[0-9A-F]{2} \(\w+\), "
            r"AD evt type \d+, Tx Pwr: -?\d+, RSSI -?\d+ "
            r"Data status: \d+, AD data len: \d+ "
            r"Name: Broadcaster Multiple "
            r"C:\d+ S:\d+ D:\d+ SR:\d+ E:\d+ "
            r"Pri PHY: [\w\s]+, Sec PHY: [\w\s]+, "
            r"Interval: 0x[0-9A-F]+ \(\d+ ms\), SID: \d+"
        )

        expected_data = ["SID: 0", "SID: 1"]
        pattern_test_result = serial_runner.search_test_pattern_with_keyword(serial_data, pattern_sid, expected_data)
        assert len(pattern_test_result) == len(expected_data), "The test result did not meet expectations "
        #print("Test pattern_sid_0_1: Pass ")
        print("Test result: \n")
        for result in pattern_test_result:
            print(f"{result}")
        #print("Test pattern_SID_0_1: Pass ")
        '''
        '''
        # observer role
        expected_data = ["Starting Observer Demo",
                         "Started scanning..."
                         ]
        print(f'parsing serial data. len = {len(serial_data)}')

        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        assert len(expected_result) != 0, "The test result did not meet expectations "
        #print("Success")

        #Device found: CF:2D:0E:1B:06:C3 (random) (RSSI -85), type 0, AD data len 24
        pattern = r"Device found: (?:[0-9A-F]{2}:){5}[0-9A-F]{2} \(random\) \(RSSI -?\d+\), type \d+, AD data len \d+"

        pattern_test_result = serial_runner.search_test_pattern(serial_data, pattern, count=10)
        assert len(pattern_test_result) != 0, "The test result did not meet expectations "
        print("Pass")
        '''


        #peripheral role
        expected_data = ["Advertising successfully started",
                        "Connected",
                        "Updated MTU: TX: 247 RX: 247 bytes"
                        ]
        print(f'parsing serial data. len = {len(serial_data)}')

        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        assert len(expected_result) != 0, "The test result did not meet expectations "
        print("Success")

        #assert 'Booting Zephyr OS' in serial_data, 'Reboot device: fail'
        #fw_version = 'v1.0.0-rc5'
        #assert fw_version in serial_data, 'Firmware version is not correct'
        #print(f'zephyr test version : {fw_version}')

    @pytest.mark.skip(reason="Zephyr dut1 reset")
    #@pytest.mark.test_id("Zephyr dut1 reset", '')
    #@pytest.mark.order(1)
    def test_dut1_reset(self):
        print('test_dut1_reset')
        dut2_mcu = Mcp2200(PID='0x00dc')
        print(f'dut1_mcp2200.PID = {dut2_mcu.pid}')
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', dut2_mcu)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(1)

        serial_runner = SerialReader('COM24', baudrate=115200)
        time.sleep(1)

        def dut_reset():
            print('DUT Reset. Firmware reset')
            #self.iocontrolledstatus.Zephyr_IOCtrl(dut2_mcu, RESET_PIN, 0.3)
            self.iocontrolledstatus.Zephyr_IOCtrl(dut2_mcu, RESET_PIN, 1)
            return 'reset_dut1'

        serial_runner.settings(10)
        result, serial_data = serial_runner.execute(dut_reset)
        #print(f'task = {result}, data = {serial_data}')

        status = self.iocontrolledstatus.Zephyr_IO_Default(dut2_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        dd = ''.join(serial_data)
        print(f'task = {result}, data = {dd}')

        '''
        # Broadcaster role
        expected_data = ["Started Extended Advertising Set 0",
                         "Started Extended Advertising Set 1"]

        print(f'parsing serial data. len = {len(serial_data)}')

        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        assert len(expected_result) != 0, "The test result did not meet expectations"
        print("Success")
        '''

        #Central role
        expected_data = ["start_scan: Scanning successfully started"]

        print(f'parsing serial data. len = {len(serial_data)}')

        expected_result = serial_runner.search_keyword_sets_ordered(serial_data, expected_data)
        assert len(expected_result) != 0, "The test result did not meet expectations"
        print("Success")

        #assert 'Booting Zephyr OS' in serial_data, 'Reboot device: fail'
        #fw_version = 'v1.0.0-rc5'
        #assert fw_version in serial_data, 'Firmware version is not correct'
        #print(f'zephyr test version : {fw_version}')

    @pytest.mark.skip(reason="Zephyr dut step3")
    # @pytest.mark.test_id("Zephyr dut step3", '')
    #@pytest.mark.order(3)
    def test_dut_step3(self):
        print('test_dut_step3')
        dut2_mcu = Mcp2200(PID='0x00dc')
        print(f'dut1_mcp2200.PID = {dut2_mcu.pid}')
        status = self.iocontrolledstatus.Zephyr_InitMCP2200('115200', dut2_mcu)
        assert status, "Failed to initialize the MCP2200"
        time.sleep(1)

        serial_runner = SerialReader('COM24', baudrate=115200)
        time.sleep(1)

        def dut_reset():
            print('DUT Reset. Firmware reset')
            # self.iocontrolledstatus.Zephyr_IOCtrl(dut2_mcu, RESET_PIN, 0.3)
            self.iocontrolledstatus.Zephyr_IOCtrl(dut2_mcu, RESET_PIN, 1)
            return 'reset_dut'

        serial_runner.settings(10)
        result, serial_data = serial_runner.execute(dut_reset)
        # print(f'task = {result}, data = {serial_data}')

        status = self.iocontrolledstatus.Zephyr_IO_Default(dut2_mcu)
        assert status, "Failed to set MCP2200 I/O default"
        time.sleep(1)

        dd = ''.join(serial_data)
        print(f'task = {result}, data = {dd}')

        pattern = r"write_cmd_cb: count= \d+, len= \d+, rate= \d+ bps"
        pattern_test_result = serial_runner.search_test_pattern_1(serial_data, pattern, count=3)
        assert len(pattern_test_result) == 3, "The test result did not meet expectations "
        for result in pattern_test_result:
            print(f"{result}")
        print("Pass")

    #@pytest.mark.test_id("Zephyr peripheral hid demo", '')
    @pytest.mark.skip(reason="test_zephyr_peripheral_hid")
    def test_peripheral_hid_demo(self):
        print("Testing Zephyr Peripheral HID. BLE Bonded")
        print("Make sure all of the paired devices are deleted")
        if sd.mobile_platform == "iOS":
            sd.mobile_driver.close_app(sd.config.ios_lightblue_app_package)
            time.sleep(10)
        else:
            print('Platform "Android" not supported')
        time.sleep(5)
        print('Launch ios setting, Check BLE connection')
        mobile_to_use = sd.config.mobile_data_config.get(sd.platform)
        driver = NewBaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            sd.config.ios_settings_app_package, fresh_env=False)
        time.sleep(5)
        iOSpairingsupport = iOSBluetoothSupport(driver)
        print("new iOSBluetoothSupport driver")
        #status = driver.launch_app(sd.config.ios_settings_app_package)
        #assert status, "Failed to launch application"
        #time.sleep(1)
        status = driver.close_app(sd.config.ios_settings_app_package)
        assert status, "Failed to close setting app"
        time.sleep(5)
        status = driver.launch_app(sd.config.ios_settings_app_package)
        assert status, "Failed to launch setting app"
        time.sleep(5)
        print("Verify Settings App is open")
        app_open = iOSpairingsupport.verify_settings_open()
        assert app_open, "Failed to open Settings application"
        time.sleep(5)
        print("Open Bluetooth Page")
        bt_open = iOSpairingsupport.open_bluetooth()
        assert bt_open, "Failed to Open Bluetooth page"
        time.sleep(3)
        status = iOSpairingsupport.check_dut_paired_connected('Test HoG mouse')
        assert status, "Failed to find the paired device"
        time.sleep(3)
        status = driver.close_app(sd.config.ios_settings_app_package)
        assert status, "Failed to close application"
        time.sleep(5)
        print('Launch HID test app')
        driver = NewBaseDriver(sd.config.appium_server_ip, sd.config.appium_server_port,
                            mobile_to_use.get(PHONE_UDID_K),
                            mobile_to_use.get(PLATFORM_NAME_K),
                            mobile_to_use.get(PLATFORM_VERSION_K), mobile_to_use.get(DEVICE_NAME_K),
                            'com.microchip.MBDtest', fresh_env=False)
        time.sleep(5)
        status = driver.close_app('com.microchip.MBDtest')
        assert status, "Failed to close HID test app"
        time.sleep(5)
        status = driver.launch_app('com.microchip.MBDtest')
        assert status, "Failed to launch HIS test app"
        time.sleep(5)
        print('Test HoG mouse. click test')
        time.sleep(5)
        status, click_button = driver.find_element('id', 'zephyr_hid_test')
        assert status, "Failed to find the element id"
        time.sleep(1)
        state = driver.get_text(click_button)
        print("Test HoG mouse state: {}".format(state))
        time.sleep(5)
        status = driver.close_app('com.microchip.MBDtest')
        assert status, "Failed to close application"
        time.sleep(5)

    #@pytest.mark.test_id("Mac_lightblue_scan_and_connect", '')
    @pytest.mark.skip(reason="Used for BLE_UART firmware")
    def test_mac_lightblue_scan_and_connect(self):
        print("test_lightblue_ble_uart_application")
        print("Search peripherals by name")
        time.sleep(3)
        self.bleuartfeature.lightblue_filter_peripherals('CDDF')
        time.sleep(3)
        print("Connect")
        self.bleuartfeature.lightblue_connect_for_Mac('BLE_UART_CDDF')
        time.sleep(10)
        self.bleuartfeature.lightblue_verify_ble_connected_for_Mac()
        time.sleep(5)
        #self.bleuartfeature.lightblue_get_device_info_data()
        #time.sleep(5)
        self.bleuartfeature.lightblue_verify_ble_services_characteristics()
        time.sleep(5)
        '''
        status, service = self.bleuartfeature.lightblue_verify_ble_services_and_characteristics()
        if not status:
            print("Failed to verify ble services and characteristics. service={}".format(service))
            self.bleuartfeature.lightblue_scroll_gesture(-500)
            time.sleep(2)
            status, service = self.bleuartfeature.lightblue_verify_ble_services_and_characteristics(start_service=service)
            if status:
                print("lightblue_verify_ble_services_and_characteristics: PASS")
                time.sleep(5)
        else:
            print("lightblue_verify_ble_services_and_characteristics: PASS")
            time.sleep(5)
        '''
        '''
        print('Discover MCHP Transparent services and characteristics')
        self.bleuartfeature.lightblue_enter_characteristic_scene('0x49535343-4C8A-39B3-2F49-511CFF073B7E')
        time.sleep(5)
        self.bleuartfeature.lightblue_characteristic_action('0x49535343-4C8A-39B3-2F49-511CFF073B7E', 'Subscribe')
        time.sleep(5)
        self.bleuartfeature.lightblue_characteristic_write('0x49535343-4C8A-39B3-2F49-511CFF073B7E', '0x14')
        time.sleep(5)
        self.bleuartfeature.lightblue_characteristic_read('0x49535343-4C8A-39B3-2F49-511CFF073B7E')
        time.sleep(5)
        self.bleuartfeature.lightblue_characteristic_action('0x49535343-4C8A-39B3-2F49-511CFF073B7E', 'Unsubscribe')
        time.sleep(5)
        self.bleuartfeature.lightblue_characteristic_screen_goback()
        time.sleep(5)
        '''
        self.bleuartfeature.lightblue_ble_disconnect()

    @pytest.mark.skip(reason="test_appium_my_test")
    #@pytest.mark.test_id("test_appium_function", '')
    def test_appium_my_test(self):
        print("test_appium_my_test")
        if sd.mobile_platform == "iOS":
            sd.mobile_driver.app_activate(sd.config.ios_settings_app_package)
            time.sleep(5)
            sd.mobile_driver.close_app(sd.config.ios_settings_app_package)
            time.sleep(5)
            sd.mobile_driver.launch_app(sd.config.ios_settings_app_package)
        else:
            print('Platform "Android" not supported')
        time.sleep(5)
        print('Launch ios setting, Check BLE connection')

        iOSpairingsupport = iOSBLEPairingSupport(sd.mobile_driver)

        print("Verify Settings App is open")
        app_open = iOSpairingsupport.verify_settings_open()
        assert app_open, "Failed to open Settings application"
        time.sleep(5)

        print("Open Bluetooth Page")
        bt_open = iOSpairingsupport.open_bluetooth()
        assert bt_open, "Failed to Open Bluetooth page"
        time.sleep(3)

        status = iOSpairingsupport.check_dut_is_paired_connected('ADDON APOLLO 2.0', delete=True)
        #status = iOSpairingsupport.check_dut_is_paired_connected('ADDON APOLLO 2.0')
        #assert status == 'Connected', "Failed to find paired device"
        time.sleep(30)

    @pytest.mark.skip(reason="test_remote_mcp2200_feature")
    #@pytest.mark.test_id("test_remote_mcp2200_feature", '')
    def test_remote_mcp2200_feature(self):
        print("test_remote_mcp2200_feature")
        time.sleep(3)
        self.mcp2200manager.run()
        print('mcp2200manager. Running')
        time.sleep(5)
        #time.sleep(30)
        #print("Wait 30 seconds")
        #self.mcp2200manager.stop()
        print('Send data to server')
        self.mcp2200manager.send_to_server("Hello mcp2200")
        time.sleep(5)
        self.mcp2200manager.send_to_server("stop")
        time.sleep(5)
        #self.mcp2200manager.shutdown()
        #time.sleep(5)









