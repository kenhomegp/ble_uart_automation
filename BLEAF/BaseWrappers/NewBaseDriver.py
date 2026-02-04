import time
import os
import subprocess
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote import errorhandler
from selenium.common.exceptions import WebDriverException
from appium.common.exceptions import NoSuchContextException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains                                                             
from appium.options.android import UiAutomator2Options

from appium.webdriver.appium_service import AppiumService                                                        

import datetime
from ..CommonSupportLib import android_locators as locators
from ..CommonSupportLib import ios_locators as ioslocators
from .SSHSupport import ShellHandler
from ..CommonSupportLib.StationData import stationData

sd = stationData()
global localport_start
localport_start = 8100

global android_systemPort_start
android_systemPort_start = 8200

import platform
import re

class NewBaseDriver:

    def __init__(self, ip_addr, port_num, udid, platform_name, platform_version,
                 device_name, app_package, app_activity=None, fresh_env=True, remote_appium=False, system_port=False):
        global localport_start
        global android_systemPort_start
        if fresh_env:
            if not remote_appium:
                if platform.system() == "Darwin":
                    self.appium_service = AppiumService()
                    self.appium_service.start(
                        # Check the output of `appium server --help` for the complete list of
                        # server command line arguments
                        #args=['--address', '127.0.0.1', '-p', str(4723)],
                        #args=['--address', '192.168.0.169', '-p', str(4723)],
                        args=['--address', sd.config.appium_server_ip, '-p', str(4723)],
                        timeout_ms=20000,
                    )
                    #print('Appium server ip:172.20.10.6')
                    print('Appium server ip:{}'.format(sd.config.appium_server_ip))
                else:
                    appium_server_logs = "appium_server_logs_{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
                    start_server_cmd = 'appium -a {} -p {} > "{}.txt'.format(ip_addr, port_num, appium_server_logs)
                    os.system("taskkill /F /IM node.exe")
                    self.appium_process = subprocess.Popen(start_server_cmd, shell=True)

                print("Successfully Started Appium Server")
                time.sleep(20)
            elif remote_appium:
                self.ssh_handler = ShellHandler(sd.config.remote_appium_server_ip, sd.config.remote_appium_username, sd.config.remote_appium_pwd)
                self.kill_remote_appium_server()
                self.start_remote_appium_server(sd.config.remote_appium_server_ip, sd.config.remote_appium_server_port)
                time.sleep(20)
        if system_port:
            print(f'systemPort = {android_systemPort_start}')
        desired_caps = {}
        desired_caps['platformName'] = platform_name
        desired_caps['platformVersion'] = platform_version
        #desired_caps['appium:automationName'] = device_name
        #desired_caps['appium:udid'] = udid

        if "android" in platform_name.lower():
            if system_port:
                desired_caps['appium:systemPort'] = android_systemPort_start + 1
            desired_caps['appium:automationName'] = 'uiautomator2'
            desired_caps['appium:appPackage'] = app_package
            desired_caps['appium:appActivity'] = app_activity
            desired_caps['appium:noReset'] = True
            desired_caps['appium:uiautomator2ServerLaunchTimeout'] = 600000
            desired_caps['appium:uiautomator2ServerInstallTimeout'] = 60000
            desired_caps['ignoreHiddenApiPolicyError'] = True
            desired_caps['df: saveDeviceLogs'] = True
            desired_caps['df: saveVideo'] = True
            desired_caps['appium:udid'] = udid
        elif "ios" in platform_name.lower():
            '''
            desired_caps['deviceName'] = 'iPhone'
            desired_caps['automationName'] = "XCUITest"
            desired_caps['bundleId'] = app_package
            desired_caps['noReset'] = False
            desired_caps['xcodeOrgId'] = 'K3G2PB8DXV'
            desired_caps['xcodeSigningId'] = "Apple Developer"
            desired_caps['updatedWDABundleId'] = 'com.microchip.DevOps.WebDriverAgentRunner'
            desired_caps['showXcodeLog'] = True
            desired_caps['udid'] = udid
            '''

            desired_caps['showXcodeLog'] = True
            desired_caps['automationName'] = "XCUITest"
            desired_caps['bundleId'] = app_package
            desired_caps['noReset'] = False
            desired_caps['wdaLocalPort'] = localport_start
            desired_caps['appium: usePreinstalledWDA'] = True
            desired_caps['appium:udid'] = udid

        elif "mac" in platform_name.lower():
            desired_caps['automationName'] = "Mac2"
            desired_caps['bundleId'] = app_package
            #desired_caps['bundleId'] = 'com.PunchThrough.LightBlue'
            desired_caps['showServerLogs'] = False

        localport_start = localport_start+1
        desired_caps['newCommandTimeout'] = 60 * 300
        ip_addr = str(ip_addr)
        port_num = str(port_num)
        appium_addr = "http://" + ip_addr + ":" + port_num
        capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)

        try:
            time.sleep(10)
            self.driver = webdriver.Remote(appium_addr, options=capabilities_options)
        except WebDriverException as e:
            print("Unable to create WebDriver . Error: {}".format(e))
            assert False, "Failed to create appium driver object. Error: {}".format(e)

        if system_port:
            if "android" in platform_name.lower():
                android_systemPort_start += 1

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
                                  "Please kill the process manually and restart execution. cmd output: {}".format(sh_out)

    def kill_remote_appium_server_1(self):
        sh_in, sh_out, sh_error = self.ssh_handler.execute("ps -a")
        pid = ''
        for line in sh_out:
            if 'node' in line:
                pid = line.split(' ')[0]

        if pid:
            print('killing appium process')
            cmd = 'kill -9 {}'.format(pid)
            sh_in, sh_out, sh_error = self.ssh_handler.execute(cmd)
            if not sh_error:
                print("Appium Process Killed Successfully")
            else:
                assert False, "Failed to kill currently running appium. " \
                              "Please kill the process manually and restart execution. cmd output: {}".format(sh_out)
        else:
            print("No running appium process. ")

    def start_remote_appium_server(self, ip_addr, port_num):
        tt = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        print("start_remote_appium_server. ip = {}, port = {}, time = {}".format(ip_addr, port_num, tt))
        appium_server_logs = "appium_server_logs_{}".format(tt)
        start_server_cmd = 'appium -a {} -p {} --relaxed-security > {}.txt &'.format(ip_addr, port_num,
                                                                                     appium_server_logs)
        sh_in, sh_out, sh_error = self.ssh_handler.execute(start_server_cmd)
        if not sh_error:
            print("Remote appium server started successfully.")
        else:
            assert False, "Failed to start remote appium server. Command output: {}".format(sh_out)

    def kill_appium_server(self):
        print("Kill Appium Server")
        os.system("taskkill /F /IM node.exe")
        self.appium_process.terminate()
        
    def find_element(self, by, locator, timeout=30):
        element = []
        found = False

        if "ID" in by.upper():
            start_time = time.time()
            while time.time() < start_time + timeout:
                try:
                    element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID,locator)
                    if element:
                        found = True
                        break
                except NoSuchElementException:
                    print("Element not found. Trying again")
                    time.sleep(2)
            if not element:
                screenshot_file_name = "Failed_screenshot_{}.png".format(
                    datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
                print(
                    "Failed to find matching elements{0}. Failed screenshot: {1}".format(locator, screenshot_file_name))
                self.driver.save_screenshot(screenshot_file_name)

        if "XPATH" in by.upper():
            start_time = time.time()
            while time.time() < start_time + timeout:
                try:
                    element = self.driver.find_element(AppiumBy.XPATH,locator)
                    if element:
                        found = True
                        break
                except NoSuchElementException:
                    print("Element not found. Trying again")
                    time.sleep(2)
            if not element:
                screenshot_file_name = "Failed_screenshot_{}.png".format(
                    datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
                print("Failed to find matching elements{0}. Failed screenshot: {1}".format(locator, screenshot_file_name))
                self.driver.save_screenshot(screenshot_file_name)

        if "IOSCLASS" in by.upper():
            start_time = time.time()
            while time.time() < start_time + timeout:
                try:
                    element = self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN,locator)
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

        if "IOS_PREDICATE" in by.upper():
            start_time = time.time()
            while time.time() < start_time + timeout:
                try:
                    element = self.driver.find_element(AppiumBy.IOS_PREDICATE, locator)
                    if element:
                        found = True
                        break
                except NoSuchElementException:
                    print("Element not found. Trying again")
                    time.sleep(2)
            if not element:
                screenshot_file_name = "Failed_screenshot_{}.png".format(
                    datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
                print("Failed to find matching elements{0}. Failed screenshot: {1}".format(locator, screenshot_file_name))
                self.driver.save_screenshot(screenshot_file_name)
        return found, element

    def find_elements(self, by, locator, timeout=30):
        elements = []
        found = False
        if "XPATH" in by.upper():
            start_time = time.time()
            while time.time() < start_time + timeout:
                try:
                    elements = self.driver.find_elements(AppiumBy.XPATH,locator)
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
				
        if "IOSCLASS" in by.upper():
            start_time = time.time()
            while time.time() < start_time + timeout:
                try:
                    elements = self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN,locator)
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

        if "CLASS_NAME" in by.upper():
            start_time = time.time()
            while time.time() < start_time + timeout:
                try:
                    #elements = self.driver.find_element(AppiumBy.IOS_CLASS_CHAIN,locator)
                    elements = self.driver.find_element(AppiumBy.CLASS_NAME,locator)
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

    def is_checked(self,element):
        checked = False
        checked = element.get_attribute('checked')
        return checked

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
        time.sleep(2)
        self.driver.back()

    # def scroll_notification_bar_old(self):
    #     touch = TouchAction(self.driver)
    #     touch.press(x=487, y=25).move_to(x=497, y=1060).release().perform()
        
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

    def scroll_up_notification_bar(self):
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
        self.driver.swipe(start_x, end_y, start_x, start_x, 1000)

    def get_capability(self,capability):
        cap= self.driver.capabilities
        d_cap = cap[capability]
        return d_cap

    def quit_driver(self):
        self.driver.quit()

    def press_keycode(self,key):
        self.driver.press_keycode(keycode=key)
        return

    def implicit_find_element_timeout(self,timeout):
        self.driver.implicitly_wait(timeout)

    def click_setting_oneplus(self):
        status, start_scan_button = self.find_element('XPATH', locators.settings_icon)
        time.sleep(2)
        assert status, "Settings icon not found"
        actions = ActionChains(self.driver)
                     
        actions.move_to_element(start_scan_button).click().perform()
        time.sleep(2)

    def click_dut_name_opporeno(self):
        status, click_dut_name = self.find_element('XPATH', locators.mode_logmessage)
        time.sleep(1)
        assert status, "Settings icon not found"
        actions = ActionChains(self.driver)
        actions.move_to_element(click_dut_name).click().perform()
        time.sleep(1)
                                           
                     
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Performed touch action %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


    def get_height_width(self,element):
        return element.size

    def update_respect_alerts(self):
        self.driver.update_settings({"respectSystemAlerts":True})

    def perform_scroll_down_ios(self):
        self.driver.execute_script('mobile: scroll', {'direction': 'down'});

    def perform_scroll_with_element(self, element, dir):
        self.driver.execute_script('mobile: scroll', {'element': element.id, 'direction': dir});

    def perform_swipe_with_element(self, element, dir):
        self.driver.execute_script('mobile: swipe', {'elementId': element.id, 'direction': dir});

    def perform_scroll_to_element(self):
        container_element = self.driver.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView')

        args = {
            "element": container_element.id,
            #"predicateString": "label == 'Device Information'"
            "direction": "down"}

        self.driver.execute_script('mobile: scroll', args);

    def perform_scroll_up_ios(self):
        self.driver.execute_script('mobile: scroll', {'direction': 'up'});

    def perform_scroll_macos(self, element_id, delta_y):
        scroll_object = {
            "elementId": element_id,
            "deltaX": 0,
            "deltaY": delta_y
        }
        self.driver.execute_script('macos: scroll', scroll_object)

    def find_ios_collection_view_element(self, range_start=0, range_end=0, require_scroll=False, scroll_index=0):
        print('find_ios_collection_view_element')   #The cell contains two static text
        element = self.driver.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView')
        time.sleep(2)
        #print("element = {}".format(element))
        all_cell = element.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeCell")
        time.sleep(3)
        #print("len = {}".format(len(all_cell)))

        cell_start = 0
        cell_end = 0
        if range_start != 0 and range_end != 0:
            cell_start = range_start
            cell_end = range_end
        print("range_start = {}, range_end = {}".format(range_start, range_end))

        cell_dic = {}
        cell_title = ''
        cell_subtitle = ''
        for i in range(cell_start, cell_end):
            if range_start == 0 and range_end == 0:
                print("XCUIElementTypeCell:{}".format(i))
            cell = all_cell[i]
            all_ui_text = cell.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText")
            time.sleep(1)

            if len(all_ui_text) == 2:
                for j in range(len(all_ui_text)):
                    print("ui_text_{} = {}".format(j, all_ui_text[j].text))
                    if j == 0:
                        cell_title = all_ui_text[j].text
                    else:
                        cell_subtitle = all_ui_text[j].text
                cell_dic[cell_title] = cell_subtitle

            if require_scroll:
                if i == scroll_index:
                    print('scroll.cell_index={}'.format(scroll_index))
                    self.perform_scroll_down_ios()
                    time.sleep(3)
        return cell_dic

    def find_ios_cell_text(self, cell):
        print('find_ios_cell_details')
        all_ui_text = cell.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText")
        if len(all_ui_text) == 2:
            for j in range(len(all_ui_text)):
                print("ui_text_{} = {}".format(j, all_ui_text[j].text))

    def find_collection_view_cell(self, by, locator, timeout=30):
        #self.find_ios_collection_view_element()

        print('find_collection_view_cell')
        element = []
        all_cell = []
        found = False
        if "XPATH" in by.upper():
            start_time = time.time()
            while time.time() < start_time + timeout:
                try:
                    element = self.driver.find_element(AppiumBy.XPATH,locator)
                    if element:
                        found = True
                        break
                except NoSuchElementException:
                    print("Element not found. Trying again")
                    time.sleep(2)
            if not element:
                screenshot_file_name = "Failed_screenshot_{}.png".format(
                    datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
                print("Failed to find matching elements{0}. Failed screenshot: {1}".format(locator, screenshot_file_name))
                self.driver.save_screenshot(screenshot_file_name)

            if found:
                time.sleep(1)
                all_cell = element.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText")
                time.sleep(2)
        return all_cell

    def find_pairing_alert2(self):
        print('find_pairing_alert2')
        alert = self.driver.switch_to.active_element
        print("alert = {}".format(alert))


    def find_pairing_alert1(self):
        print('find_pairing_alert1')
        alert = self.driver.switch_to.alert
        # Now you can interact with the alert
        alert_text = alert.text
        print(f"Alert text: {alert_text}")
        #alert.dismiss()
        alert.accept()  # or alert.dismiss()

    def find_pairing_alert(self, timeout=30):
        print('find_alert')

        status, element = self.driver.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeAlert')
        assert status, 'Alert not found'
        '''
        element = []
        found = False
        start_time = time.time()
        while time.time() < start_time + timeout:
            try:
                element = self.driver.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeAlert')
                if element:
                    found = True
                    break
            except NoSuchElementException:
                print("Element not found. Trying again")
                time.sleep(2)
        '''
        if not element:
            screenshot_file_name = "Failed_screenshot_{}.png".format(
                datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
            print("Failed to find matching elements{0}. Failed screenshot: {1}".format('Alert', screenshot_file_name))
            self.driver.save_screenshot(screenshot_file_name)

        #all_ui_text = element.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText")
        #for j in range(len(all_ui_text)):
        #    print("ui_text_{} = {}".format(j, all_ui_text[j].text))

        #self.driver.find_element_by_accessibility_id('Cancel').click()
        print("Find Cancel element and click")
        self.driver.find_element('Cancel').click()

    def handle_pairing_alert(self, dut_name, action, passkey=''):
        #print('handle_pairing_alert.action = {}'.format(action))
        alert = self.driver.switch_to.alert
        time.sleep(3)
        # Now you can interact with the alert
        alert_text = alert.text
        if alert_text is not None and alert.text != '':
            print(f"Alert text: {alert_text.lower()}")
            index = alert_text.lower().find('pairing request')
            assert index != -1, "Pairing request not found"
            index = alert_text.lower().find(dut_name.lower())
            assert index != -1, "Dut name not found"

        print('handle_pairing_alert.action = {}'.format(action))
        print('time = "{}"'.format(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")))
        if action == 'accept':
            if passkey != '':
                alert.send_keys(passkey)
                time.sleep(1)
            alert.accept()
        elif action == 'cancel':
            alert.dismiss()

    def app_activate(self, app):
        print('app_activate.app = {}'.format(app))
        self.driver.activate_app(app)

    def android_get_textview_bt_address(self):
        bt_pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
        print('android_get_textview_bt_address')

        textviews = self.driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.TextView")'
        )
        # Check if any matches BT pattern
        for tv in textviews:
            if re.match(bt_pattern, tv.text):
                return tv.text
        return ''

    def android_listactivity_tap_dut(self, dut):
        print('android_listactivity_get_text')

        textviews = self.driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.TextView")'
        )
        for tv in textviews:
            #print(f'text = {tv.text}')
            if dut in tv.text:
                tv.click()
                print('dut found. tap')
                return True
        return False
