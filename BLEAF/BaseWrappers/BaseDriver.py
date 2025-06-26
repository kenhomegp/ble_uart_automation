import platform
import time
import os
import subprocess

import re

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote import errorhandler
from selenium.common.exceptions import WebDriverException
from appium.common.exceptions import NoSuchContextException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
#from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.appium_service import AppiumService
from appium.options.android import UiAutomator2Options

import datetime
from ..CommonSupportLib import android_locators as locators
from ..CommonSupportLib import ios_locators as ioslocators
from .SSHSupport import ShellHandler
from ..CommonSupportLib.StationData import stationData

from .AppiumServer import AppiumServer

sd = stationData()

class BaseDriver:
    def __init__(self, ip_addr, port_num, udid, platform_name, platform_verion,
                 device_name, app_package, app_activity=None, fresh_env=True, remote_appium=0):
        #print("remote_appium. Start")
        #print(fresh_env)
        #print(remote_appium)

        #self.ssh_handler = ShellHandler("10.160.54.60", "WSGAppDev", "Amchp17217")
        #self.kill_remote_appium_server()
        #self.start_remote_appium_server(ip_addr, port_num)
        #time.sleep(10)
        #print("remote_appium. Done")
        checkOS = platform.system()
        self.platform = checkOS

        if fresh_env:
            if remote_appium == 0:
                appium_server_logs = "appium_server_logs_{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
                start_server_cmd = 'appium -a {} -p {} > "{}.txt'.format(ip_addr, port_num, appium_server_logs)
                time.sleep(5)
                #checkOS = platform.system()
                print("OS type is {}".format(self.platform))

                if self.platform == "Windows":
                    #os.system("taskkill /F /IM node.exe")
                    self.appium_service = AppiumServer()
                    #appium_start_args = ['--address', '127.0.0.1', '-p']
                    appium_start_args = ['--address']
                    appium_start_args.append(ip_addr)
                    appium_start_args.append('-p')
                    appium_start_args.append(port_num)
                    print(appium_start_args)
                    print(os.getcwd())
                    appium_server_log_stdout = "Appium_log_{}.log".format(
                        datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
                    appium_server_logs_stderr = "Appium_log_err_{}.log".format(
                        datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
                    self.appium_service.start(args=appium_start_args, stdout_file=appium_server_log_stdout,
                                              stderr_file=appium_server_logs_stderr)
                    print("[Windows]Successfully Started Appium Server")
                    time.sleep(5)
                else:
                    print("Kill appium server if needed")
                    #self.kill_remote_appium_server()
                    if port_num == '4723' or port_num == '4724':
                        #self.appium_service = AppiumService()
                        self.appium_service = AppiumServer()
                        #self.appium_service.start()
                        #self.appium_service.start(args=['--address', '127.0.0.1', '-p', '4723', '--base-path', '/wd/hub'])
                        appium_start_args = ['--address', '127.0.0.1', '-p']
                        appium_start_args.append(port_num)
                        #self.appium_service.start(args=['--address', '127.0.0.1', '-p', '4723'], stdout_file='appium_stdout.log', stderr_file='appium_stderr.log')
                        print(appium_start_args)
                        print(os.getcwd())
                        #self.appium_service.start(args= appium_start_args)
                        appium_server_log_stdout = "Appium_log_{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
                        appium_server_logs_stderr = "Appium_log_err_{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
                        #self.appium_service.start(args=appium_start_args, stdout_file='appium_stdout.log', stderr_file='appium_stderr.log')
                        self.appium_service.start(args= appium_start_args, stdout_file= appium_server_log_stdout, stderr_file= appium_server_logs_stderr)
                        #print(appium_start_args)
                        print("[MacOS]Successfully Started Appium Server")
                        time.sleep(5)
            else:
                if not sd.remote_mac_server:
                    print("Remote appium,ip = {}".format(ip_addr))
                    print("port = {}".format(port_num))
                    self.ssh_handler = ShellHandler(ip_addr, sd.config.remote_appium_username, sd.config.remote_appium_pwd)
                    self.kill_remote_appium_server()
                    self.start_remote_appium_server(ip_addr, port_num)
                else:
                    if port_num == '4723':
                        print("[Remote multi-server] appium,ip = {}".format(ip_addr))
                        print("port = {}".format(port_num))
                        self.ssh_handler = ShellHandler(ip_addr, sd.config.remote_appium_username, sd.config.remote_appium_pwd)
                        self.kill_remote_appium_server()
                        #self.start_remote_appium_server(ip_addr, port_num, multiple_appium_server=2)
                        self.start_remote_appium_server(ip_addr, port_num, multiple_appium_server=remote_appium)
                    else:
                        self.ssh_handler = None
                time.sleep(10)

        desired_caps = {}
        desired_caps['platformName'] = platform_name
        desired_caps['platformVersion'] = platform_verion
        desired_caps['deviceName'] = device_name
        desired_caps['udid'] = udid
        #desired_caps['automationName'] = 'uiautomator2'
        #desired_caps['appPackage'] = app_package
        #desired_caps['appActivity'] = "com.microchip.bleanalyser.SplashScreen"
        #desired_caps['noReset'] = True

        if "android" in platform_name.lower():
            # desired_caps['automationName'] = 'uiautomator1'
            desired_caps['automationName'] = 'uiautomator2'
            desired_caps['appPackage'] = app_package
            desired_caps['appActivity'] = "com.microchip.bleanalyser.SplashScreen"
            desired_caps['noReset'] = True
        elif "ios" in platform_name.lower():
            print("iOS.desired_caps ")
            desired_caps['automationName'] = "XCUITest"
            # desired_caps['appPackage'] = app_package
            desired_caps['bundleId'] = app_package
            desired_caps['noReset'] = False
            desired_caps['xcodeOrgId'] = 'K3G2PB8DXV'
            desired_caps['xcodeSigningId'] = "Apple Developer"
            desired_caps['updatedWDABundleId'] = 'com.microchip.DevOps.WebDriverAgentRunner'
            desired_caps['showXcodeLog'] = False

        desired_caps['newCommandTimeout'] = 60 * 30
        ip_addr = str(ip_addr)
        port_num = str(port_num)
        appium_addr = "http://" + ip_addr + ":" + port_num
        #appium_addr = "http://" + ip_addr + ":" + port_num + "/wd/hub"
        capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)
        try:
            time.sleep(15)
            print("Create webDriver.appium addr = {}".format(appium_addr))
            print(capabilities_options)
            self.driver = webdriver.Remote(appium_addr, options=capabilities_options)
        except WebDriverException as e:
            print("Unable to create WebDriver . Error: {}".format(e))
            assert False, "Failed to create appium driver object. Error: {}".format(e)

    def kill_remote_appium_server(self):
        sh_in, sh_out, sh_error = self.ssh_handler.execute("ps -a")
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
                #pid = line.split(' ')[0]
                #pids.append(pid)

        print("Appium PID.count = {}".format(len(pids)))

        if len(pids) == 1:
            print("pid = {}".format(pids[0]))

        if len(pids) != 0:
            for pid in pids:
                print('killing appium process,pid = {}'.format(pid))
                cmd = 'kill -9 {}'.format(pid)
                sh_in, sh_out, sh_error = self.ssh_handler.execute(cmd)
                if not sh_error:
                    print("Appium Process Killed Successfully. cmd = {}".format(cmd))
                else:
                    assert False, "Failed to kill currently running appium. " \
                                  "Please kill the process manually and restart execution. cmd output: {}".format(
                        sh_out)
                    break
        '''
        if sd.remote_mac_server:
            pids = []
            print("List process:")
            for line in sh_out:
                print(line)
                if 'node' in line:
                    pid = line.split(' ')[0]
                    pids.append(pid)

            print("pids.count = {}".format(len(pids)))
            if len(pids) != 0:
                for pid in pids:
                    print('killing appium process,pid = {}'.format(pid))
                    cmd = 'kill -9 {}'.format(pid)
                    sh_in, sh_out, sh_error = self.ssh_handler.execute(cmd)
                    if not sh_error:
                        print("Appium Process Killed Successfully. cmd = {}".format(cmd))
                    else:
                        assert False, "Failed to kill currently running appium. " \
                                      "Please kill the process manually and restart execution. cmd output: {}".format(sh_out)
                        break
        else:
            pid = ''
            for line in sh_out:
                if 'node' in line:
                    pid = line.split(' ')[0]

            if pid:
                print('killing appium process,pid = {}'.format(pid))
                cmd = 'kill -9 {}'.format(pid)
                sh_in, sh_out, sh_error = self.ssh_handler.execute(cmd)
                if not sh_error:
                    print("Appium Process Killed Successfully")
                else:
                    assert False, "Failed to kill currently running appium. " \
                                  "Please kill the process manually and restart execution. cmd output: {}".format(sh_out)
            else:
                print("No running appium process. ")
        '''
    def start_remote_appium_server(self, ip_addr, port_num, multiple_appium_server=0):
        if multiple_appium_server == 0:
            appium_server_logs = "appium_server_logs_{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
            start_server_cmd = 'appium -a {} -p {} --relaxed-security > {}.txt &'.format(ip_addr, port_num,
                                                                                     appium_server_logs)
            sh_in, sh_out, sh_error = self.ssh_handler.execute(start_server_cmd)
            if not sh_error:
                print("Remote appium server started successfully.")
            else:
                assert False, "Failed to start remote appium server. Command output: {}".format(sh_out)
        else:
            port = int(port_num)
            for i in range(multiple_appium_server):
                appium_server_logs = "appium_server_logs_{}_{}".format(i+1, datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
                #start_server_cmd = 'appium -a {} -p {} --relaxed-security > {}.txt &'.format(ip_addr, str(port), appium_server_logs)
                start_server_cmd = 'appium -a {} -p {} --relaxed-security > ./Chimera_BLEAF_Log/Appium/{}.txt &'.format(ip_addr, str(port), appium_server_logs)
                sh_in, sh_out, sh_error = self.ssh_handler.execute(start_server_cmd)
                if not sh_error:
                    print("Remote appium server started successfully. cmd = {}".format(start_server_cmd))
                    port += 1
                    time.sleep(2)
                else:
                    assert False, "Failed to start remote appium server. Command output: {}".format(sh_out)
                    break

    def start_remote_test_appium_server(self, ip_addr, port_num):
        if port_num == '4723':
            appium_server_logs = "appium_server_logs_1_{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
            start_server_cmd = 'appium -a {} -p {} --relaxed-security > {}.txt &'.format(ip_addr, port_num,
                                                                                     appium_server_logs)
            sh_in, sh_out, sh_error = self.ssh_handler.execute(start_server_cmd)
            if not sh_error:
                print("Remote appium server1 started successfully.")
            else:
                assert False, "Failed to start remote appium server1. Command output: {}".format(sh_out)

            time.sleep(2)

            appium_server_logs2 = "appium_server_logs_2_{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
            start_server_cmd2 = 'appium -a {} -p {} --relaxed-security > {}.txt &'.format(ip_addr, '4724',
                                                                                         appium_server_logs2)
            sh_in1, sh_out1, sh_error1 = self.ssh_handler.execute(start_server_cmd2)
            if not sh_error1:
                print("Remote appium server2 started successfully.")
            else:
                assert False, "Failed to start remote appium server2. Command output: {}".format(sh_out)

    def kill_appium_server(self):
        print("Kill Appium Server")
        os.system("taskkill /F /IM node.exe")
        self.appium_process.terminate()

    def get_android_app_pid(self, device_id):
        adb_cmd = 'adb -s {} shell pidof -s com.microchip.bluetooth.data &'.format(device_id)
        sh_in, sh_out, sh_error = self.ssh_handler.execute(adb_cmd)
        ll = []
        pid = ''
        for line in sh_out:
            #print("get_android_app_pid command execute. result = {}".format(line))
            ll.append(line)

        if len(ll) == 3:
            #print("pid info = {}".format(ll[1]))
            print(ll[1])
            pid = ll[1].split(' ')[1].replace('\n', '')

        print("get_android_app_pid = {}".format(pid))
        return pid

    def get_android_adb_log(self, device_id, pid=''):
        adb_logs = "adb_logs_{}_{}".format(pid, datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
        #adb_cmd = 'adb -s {} logcat -d --pid={} > ./Chimera_BLEAF_Log/Android/{}.txt'.format(device_id, pid, adb_logs)
        adb_cmd = 'adb -s {} logcat -d > ./Chimera_BLEAF_Log/Android/{}.txt'.format(device_id, adb_logs)
        sh_in, sh_out, sh_error = self.ssh_handler.execute(adb_cmd)
        if not sh_error:
            print("Get adb log successfully.cmd = {}".format(adb_cmd))
            print("Android log file = {}".format(adb_logs))
        else:
            assert False, "Failed to execute adb command. Command output: {}".format(sh_out)

    def find_element(self, by, locator, timeout=30):
        element = []
        found = False
        start_time = time.time()
        if "XPATH" in by.upper():
            #start_time = time.time()
            while time.time() < start_time + timeout:
                try:
                    element = self.driver.find_element(By.XPATH, locator)
                    if element:
                        found = True
                        break
                except NoSuchElementException:
                    print("Element not found. Trying again")
                    time.sleep(2)
            if not element:
                screenshot_file_name = "Failed_screenshot_{}.png".format(
                    datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
                print("Failed to find matching elements. Failed screenshot: {}".format(screenshot_file_name))
                self.driver.save_screenshot(screenshot_file_name)
        return found, element

    def find_elements(self, by, locator, timeout=30):
        elements = []
        found = False
        if "XPATH" in by.upper():
            start_time = time.time()
            while time.time() < start_time + timeout:
                try:
                    elements = self.driver.find_elements(By.XPATH, locator)
                    if elements:
                        found = True
                        break
                except NoSuchElementException:
                    print("Element not found. Trying again")
                    time.sleep(2)
            if not elements:
                screenshot_file_name = "Failed_screenshot_{}.png".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
                print("Failed to find matching elements. Failed screenshot: {}".format(screenshot_file_name))
                self.driver.save_screenshot(screenshot_file_name)
        return found, elements
    

    def click_element(self, element):
        clicked = False
        try:
            element.click()
            clicked = True
        except Exception as e:
            print("Failed to click on element.")
        return clicked

    def is_visible(self, element):
        visible = False
        visible = element.is_displayed()
        return visible

    def send_keys(self, element, keys):
        element.clear()
        element.send_keys(keys)
        
    def get_text(self, element):
        return element.text
    
    def get_value(self, element):
        return element.get_attribute('value')
    
    def get_location(self, element):
        return element.location
    
    def select_checkbox(self, element):
        status = False
        print("checked: {}".format(element.get_attribute('checked')))
        if not element.get_attribute('checked') == 'true':
            status = self.click_element(element)
        else:
            print("Checkbox already checked.")
            status = True
        return status
    
    def launch_app(self,package):
        launch_flag = False
        try:
            self.driver.activate_app(package)
            launch_flag = True
        except Exception as e:
            print("Failed to launch Application. Error: {}".format(e))
        return launch_flag
    
    
    def close_app(self,package):
        close_flag = False
        try:
            self.driver.terminate_app(package)
            close_flag = True
        except Exception as e:
            print("Failed to close Application. Error: {}".format(e))
        return close_flag


    def click_back_button(self, count=1):
        error_msg = ""
        status = False
        for i in range(count):
            status, back_button = self.find_element('XPATH', locators.back_button)
            if status:
                status = self.click_element(back_button)
                if not status:
                    error_msg = "Failed to click on back button"
                    break
            else:
                error_msg = "Element not found."
                break
            time.sleep(3)
        return status, error_msg

    def click_notify_button(self):
        status = False
        notify_button = None
        try:
            print("Trying")
            status, notify_button = self.find_element('XPATH', locators.notify_button)
            status = self.click_element(notify_button)
        except Exception as e:
            print("Trying again")
            print("Failed to get element. Trying again")
            time.sleep(3)
            status, notify_button = self.find_element('XPATH', locators.notify_button)
            status = self.click_element(notify_button)
        assert status, "Failed to click Notify button"

    def click_indicate_button(self):
        status = False
        indicate_button = None
        try:
            status, indicate_button = self.find_element('XPATH', locators.indicate_button)
            status = self.click_element(indicate_button)
        except Exception as e:
            print("Failed to get element. Trying again")
            time.sleep(2)
            status, indicate_button = self.find_element('XPATH', locators.indicate_button)
            status = self.click_element(indicate_button)
        assert status, "Failed to click Indicate button"

    def click_read_button(self):
        print("Click Read button")
        read_button = None
        status = False
        try:
            status, read_button = self.find_element('XPATH', locators.read_button)
            status = self.click_element(read_button)
        except Exception as e:
            print("Failed to get element. Trying again")
            time.sleep(2)
            status, read_button = self.find_element('XPATH', locators.read_button)
            status = self.click_element(read_button)
        assert status, "Failed to click Read button"
        
    def click_write_button(self):
        status = False
        write_button = None
        try:
            status, write_button = self.find_element('XPATH', locators.write_button)
            status = self.click_element(write_button)
        except Exception as e:
            print("Failed to get element. Trying again")
            time.sleep(2)
            status, write_button = self.find_element('XPATH', locators.write_button)
            status = self.click_element(write_button)
        assert status, "Failed to click Write button"
        
    def get_hex_value(self):
        status, hex_text = self.find_element('XPATH', locators.hex_value_edittext)
        assert status, "Failed to find element for Intermediate cuff pressure hex"
        return self.get_text(hex_text)
    
    def perform_bottom_to_up_swipe(self):
        """
        Perform vertical swipe from bottom to up direction
        :param driver: appium driver (obj)
        :return: None
        """
        window_size = self.driver.get_window_size()
        max_width = window_size["width"] - 1
        max_height = window_size["height"] - 1
        start_y = (int)(max_height * 0.80)
        end_y = (int(max_height * 0.50))
        start_x = max_width / 2
        self.driver.swipe(start_x, start_y, start_x, end_y, 3000)

    def perform_top_to_bottom_swipe(self):
        """
        Perform vertical swipe from bottom to up direction
        :param driver: appium driver (obj)
        :return: None
        """
        window_size = self.driver.get_window_size()
        max_width = window_size["width"] - 1
        max_height = window_size["height"] - 1
        start_y = (int)(max_height * 0.8)
        end_y = (int(max_height * 0.5))
        start_x = max_width / 2
        self.driver.swipe(start_x, end_y, start_x, start_y, 3000)

    def perform_scroll(self, start, end):
        start_x = start['x']
        start_y = start['y']
        end_x = end['x']
        end_y = end['x']
        self.driver.swipe(start_x, start_y, start_x, end_y, 3000)

    def go_back(self):
        self.driver.back()

    #def scroll_notification_bar_old(self):
    #    touch = TouchAction(self.driver)
    #    touch.press(x=487, y=25).move_to(x=497, y=1060).release().perform()
        
    def scroll_notification_bar(self):
        """
        Perform vertical swipe from bottom to up direction
        :param driver: appium driver (obj)
        :return: None
        """
        window_size = self.driver.get_window_size()
        max_width = window_size["width"] - 106
        max_height = window_size["height"] - 1
        start_y = (int)(max_height * 0.01) + 4
        end_y = (int(max_height * 0.8))
        start_x = (int(max_width / 2)) + 10
        end_x = (int(max_width / 2)) + 10
        # self.driver.swipe(start_y, start_x, end_x, end_y, 3000)
        # self.driver.swipe(start_x, start_y, end_x, end_y, 3000)
        self.driver.swipe(start_x, start_y, start_x, end_y, 3000)

    def get_capability(self,capability):
        cap= self.driver.capabilities
        d_cap = cap[capability]
        return d_cap

    def quit_driver(self):
        self.driver.quit()
       
    def click_setting_oneplus(self):
        status, start_scan_button = self.find_element('XPATH', locators.settings_icon)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", status)
        time.sleep(4)
        assert status, "Settings icon not found"
        #touch = TouchAction(self.driver)
        #time.sleep(4)
        #touch.tap(start_scan_button).perform()
        #time.sleep(5)
       
    def click_dut_name_opporeno(self):
        status, click_dut_name = self.find_element('XPATH', locators.text_view_place_holder.format(sd.config.dut_friendly_name))
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", status)
        time.sleep(4)
        assert status, "Settings icon not found"
        #touch = TouchAction(self.driver)
        #time.sleep(4)
        #touch.tap(click_dut_name).perform()
        #time.sleep(5)

