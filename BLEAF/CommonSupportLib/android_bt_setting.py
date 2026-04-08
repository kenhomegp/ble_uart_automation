"""
BluetoothSettingsAutomation - Reusable class for Android Bluetooth settings automation
"""

import time
from datetime import datetime
from pathlib import Path

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class BluetoothSettingsAutomation:
    """Automate Android Bluetooth settings pairing/unpairing flows."""

    SETTINGS_APP_PACKAGE = "com.android.settings"

    # Device-specific navigation paths to Bluetooth settings
    DEVICE_NAVIGATION_PATHS = {
        "samsung_or_galaxy": [
            {
                "name": "Connections",
                "locators": [
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Connections")'),
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Connections")'),
                    (AppiumBy.ACCESSIBILITY_ID, "Connections"),
                    (AppiumBy.XPATH, '//*[@text="Connections" or contains(@text,"Connections") or @content-desc="Connections"]'),
                ],
                "timeout": 10,
                "wait_after": 3,
            },
            {
                "name": "Bluetooth",
                "locators": [
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Bluetooth")'),
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Bluetooth")'),
                    (AppiumBy.ACCESSIBILITY_ID, "Bluetooth"),
                    (AppiumBy.XPATH, '//*[@text="Bluetooth" or contains(@text,"Bluetooth") or @content-desc="Bluetooth"]'),
                ],
                "timeout": 10,
                "wait_after": 10,
            },
        ],
        "xiaomi": [
            {
                "name": "Bluetooth",
                "locators": [
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Bluetooth")'),
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Bluetooth")'),
                    (AppiumBy.ACCESSIBILITY_ID, "Bluetooth"),
                    (AppiumBy.XPATH, '//*[@text="Bluetooth" or contains(@text,"Bluetooth") or @content-desc="Bluetooth"]'),
                ],
                "timeout": 6,
                "wait_after": 0,
                "fallback": {
                    "name": "Connection & sharing",
                    "locators": [
                        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Connection & sharing")'),
                        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Connections & sharing")'),
                        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("sharing")'),
                        (AppiumBy.XPATH, '//*[contains(@text,"Connection") and contains(@text,"sharing")]'),
                    ],
                    "timeout": 8,
                    "wait_after": 0,
                },
            },
        ],
        "oppo": [
            {
                "name": "Bluetooth",
                "locators": [
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Bluetooth")'),
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Bluetooth")'),
                    (AppiumBy.ACCESSIBILITY_ID, "Bluetooth"),
                    (AppiumBy.XPATH, '//*[@text="Bluetooth" or contains(@text,"Bluetooth") or @content-desc="Bluetooth"]'),
                ],
                "timeout": 6,
                "wait_after": 0,
                "fallback": {
                    "name": "Connections",
                    "locators": [
                        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Connections")'),
                        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Connections")'),
                        (AppiumBy.XPATH, '//*[@text="Connections" or contains(@text,"Connections")]'),
                    ],
                    "timeout": 8,
                    "wait_after": 0,
                },
            },
        ],
    }

    # Common locators
    SCAN_BUTTON_LOCATORS = [
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Scan")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SCAN")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Refresh")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Scan")'),
        (AppiumBy.ACCESSIBILITY_ID, "Scan"),
        (AppiumBy.XPATH, '//*[@text="Scan" or @text="SCAN" or @text="Refresh" or contains(@text,"Scan") or @content-desc="Scan"]'),
    ]

    PAIRING_MESSAGE_LOCATORS = [
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Pairing")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Pairing")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Pair with")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Pair")'),
        (AppiumBy.XPATH, '//*[contains(@text,"Pairing") or contains(@text,"Pair")]'),
    ]

    PAIRING_TEXT_EDIT_LOCATORS = [
        (AppiumBy.CLASS_NAME, "android.widget.EditText"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")'),
        (AppiumBy.ID, "android:id/edit"),
        (AppiumBy.XPATH, '//android.widget.EditText'),
    ]

    PAIR_BUTTON_LOCATORS = [
        (AppiumBy.ID, "android:id/button1"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Pair")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Pair")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("OK")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SAVE")'),
        (AppiumBy.XPATH, '//*[@text="Pair" or @text="OK" or @text="SAVE" or @content-desc="Pair" or @content-desc="OK"]'),
    ]

    PAIR_BUTTON_LOCATORS_OPPO = [
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SAVE")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("SAVE")'),
        (AppiumBy.XPATH, '//*[@text="SAVE" or @content-desc="SAVE"]'),
        (AppiumBy.ID, "android:id/button1"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Pair")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")'),
        (AppiumBy.XPATH, '//*[@text="SAVE" or @text="Pair" or @text="OK" or @content-desc="SAVE" or @content-desc="Pair" or @content-desc="OK"]'),
    ]

    CANCEL_BUTTON_LOCATORS = [
        (AppiumBy.ID, "android:id/button2"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cancel")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Cancel")'),
        (AppiumBy.XPATH, '//*[@text="Cancel" or @content-desc="Cancel" or @text="CANCEL"]'),
    ]

    UNPAIR_BUTTON_LOCATORS = [
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Unpair")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Unpair")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("UNPAIR")'),
        (AppiumBy.XPATH, '//*[@text="Unpair" or @text="UNPAIR" or @content-desc="Unpair"]'),
    ]

    UNPAIR_CONFIRM_LOCATORS = [
        (AppiumBy.ID, "android:id/button1"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Unpair")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")'),
        (AppiumBy.XPATH, '//*[@text="Unpair" or @text="OK" or @content-desc="Unpair" or @content-desc="OK"]'),
    ]

    def __init__(self, device_type="samsung_or_galaxy", debug_screenshot_prefix="android_bt_setting"):
        """
        Initialize the Bluetooth automation helper.
        
        :param device_type: Device type identifier (samsung_or_galaxy, xiaomi, oppo)
        :param debug_screenshot_prefix: Prefix for debug screenshots
        """
        self.device_type = device_type
        self.debug_screenshot_prefix = debug_screenshot_prefix

    def _save_debug_screenshot(self, driver, suffix=""):
        """Save timestamped screenshot for debugging."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = f"{self.debug_screenshot_prefix}_{suffix}_{ts}" if suffix else self.debug_screenshot_prefix
        file_path = Path.cwd() / f"{prefix}.png"
        try:
            driver.save_screenshot(str(file_path))
            print(f"[SCREENSHOT] saved: {file_path}")
        except Exception as e:
            print(f"[SCREENSHOT] save failed: {e}")

    def _save_debug_page_source(self, driver, suffix=""):
        """Save page source XML for debugging."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = f"{self.debug_screenshot_prefix}_{suffix}_{ts}" if suffix else self.debug_screenshot_prefix
        file_path = Path.cwd() / f"{prefix}.xml"
        try:
            page_source = driver.page_source
            file_path.write_text(page_source, encoding="utf-8")
            print(f"[PAGE_SOURCE] saved: {file_path}")
        except Exception as e:
            print(f"[PAGE_SOURCE] save failed: {e}")

    def _wait_and_tap_first(self, driver, locators, timeout_each=8, step_name=""):
        """Try each locator until one works."""
        for by, value in locators:
            try:
                elem = WebDriverWait(driver, timeout_each).until(
                    EC.element_to_be_clickable((by, value))
                )
                elem.click()
                print(f"[OK] {step_name} clicked by locator: {by}={value}")
                return True
            except TimeoutException:
                continue
        return False

    def _wait_and_type_first(self, driver, locators, text, timeout_each=8, step_name=""):
        """Locate input field, click it, clear it, and enter text."""
        for by, value in locators:
            try:
                elem = WebDriverWait(driver, timeout_each).until(
                    EC.presence_of_element_located((by, value))
                )
                elem.click()
                elem.clear()
                elem.send_keys(text)
                print(f"[OK] {step_name} text entered by locator: {by}={value}")
                return True
            except TimeoutException:
                continue
        return False

    def _wait_for_presence_first(self, driver, locators, timeout_each=8, step_name=""):
        """Check presence without clicking."""
        for by, value in locators:
            try:
                WebDriverWait(driver, timeout_each).until(
                    EC.presence_of_element_located((by, value))
                )
                print(f"[OK] {step_name} found by locator: {by}={value}")
                return True
            except TimeoutException:
                continue
        return False

    def _swipe_device_list_once(self, driver, direction="up"):
        """Swipe the Bluetooth device list."""
        rect = driver.get_window_rect()
        left = rect["x"] + int(rect["width"] * 0.1)
        top = rect["y"] + int(rect["height"] * 0.25)
        width = int(rect["width"] * 0.8)
        height = int(rect["height"] * 0.6)

        try:
            driver.execute_script(
                "mobile: swipeGesture",
                {
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height,
                    "direction": direction,
                    "percent": 0.75,
                },
            )
        except WebDriverException:
            start_x = rect["x"] + rect["width"] // 2
            end_x = start_x
            if direction == "up":
                start_y = rect["y"] + int(rect["height"] * 0.75)
                end_y = rect["y"] + int(rect["height"] * 0.35)
            elif direction == "down":
                start_y = rect["y"] + int(rect["height"] * 0.35)
                end_y = rect["y"] + int(rect["height"] * 0.75)
            else:
                raise ValueError(f"Unsupported swipe direction: {direction}")
            driver.swipe(start_x, start_y, end_x, end_y, 600)

    def _wait_and_tap_with_scroll(self, driver, locators, device_name, step_name="", timeout_each=3, max_scrolls=6):
        """Retry with scrolling to find off-screen elements."""
        for attempt in range(max_scrolls + 1):
            if self._wait_and_tap_first(driver, locators, timeout_each=timeout_each, step_name=step_name):
                return True
            if attempt < max_scrolls:
                print(f"[ACTION] {step_name} not found. Scrolling down (attempt {attempt + 1}/{max_scrolls})...")
                self._swipe_device_list_once(driver, direction="up")
                time.sleep(1)
        return False

    def _wait_and_get_first(self, driver, locators, timeout_each=8, step_name=""):
        """Find an element without clicking, return the element."""
        for by, value in locators:
            try:
                elem = WebDriverWait(driver, timeout_each).until(
                    EC.presence_of_element_located((by, value))
                )
                print(f"[OK] {step_name} found by locator: {by}={value}")
                return elem
            except TimeoutException:
                continue
        return None

    def _wait_and_get_with_scroll(self, driver, locators, step_name="", timeout_each=3, max_scrolls=6):
        """Retry with scrolling to find off-screen elements, return element without clicking."""
        for attempt in range(max_scrolls + 1):
            elem = self._wait_and_get_first(driver, locators, timeout_each=timeout_each, step_name=step_name)
            if elem is not None:
                return elem
            if attempt < max_scrolls:
                print(f"[ACTION] {step_name} not found. Scrolling down (attempt {attempt + 1}/{max_scrolls})...")
                self._swipe_device_list_once(driver, direction="up")
                time.sleep(1)
        return None

    def ensure_settings_home(self, driver, settings_package=None):
        """Restart Settings app to avoid restoring the previous deep page."""
        package = settings_package or self.SETTINGS_APP_PACKAGE
        print("[INFO] Closing and relaunching Settings app...")

        try:
            driver.terminate_app(package)
        except WebDriverException:
            # If terminate fails, still try to relaunch.
            pass

        time.sleep(2)
        driver.activate_app(package)
        time.sleep(4)

    def navigate_to_bluetooth_settings(self, driver):
        """
        方法一: 進入到藍牙裝置掃描頁面
        Navigate to Bluetooth settings using device-specific paths.
        
        :param driver: Appium WebDriver instance
        :raises TimeoutException: If navigation steps fail
        """
        paths = self.DEVICE_NAVIGATION_PATHS.get(self.device_type, [])
        
        for path_step in paths:
            name = path_step["name"]
            locators = path_step["locators"]
            timeout = path_step.get("timeout", 8)
            wait_after = path_step.get("wait_after", 0)
            
            if not self._wait_and_tap_first(driver, locators, timeout_each=timeout, step_name=name):
                fallback = path_step.get("fallback")
                if fallback:
                    fallback_name = fallback["name"]
                    fallback_locators = fallback["locators"]
                    fallback_timeout = fallback.get("timeout", 8)
                    fallback_wait = fallback.get("wait_after", 0)
                    
                    if not self._wait_and_tap_first(driver, fallback_locators, timeout_each=fallback_timeout, step_name=fallback_name):
                        self._save_debug_screenshot(driver, f"not_found_{fallback_name.lower().replace(' ', '_')}")
                        self._save_debug_page_source(driver, f"not_found_{fallback_name.lower().replace(' ', '_')}")
                        raise TimeoutException(f"Cannot find {fallback_name} on {self.device_type} settings")
                    
                    if fallback_wait:
                        time.sleep(fallback_wait)
                    
                    if not self._wait_and_tap_first(driver, locators, timeout_each=timeout, step_name=name):
                        self._save_debug_screenshot(driver, f"not_found_{name.lower()}")
                        self._save_debug_page_source(driver, f"not_found_{name.lower()}")
                        raise TimeoutException(f"Cannot find {name} on {self.device_type} settings (after fallback)")
                else:
                    self._save_debug_screenshot(driver, f"not_found_{name.lower()}")
                    self._save_debug_page_source(driver, f"not_found_{name.lower()}")
                    raise TimeoutException(f"Cannot find {name} on {self.device_type} settings")
            
            if wait_after:
                print(f"Waiting {wait_after} seconds after {name}...")
                time.sleep(wait_after)
        
        print("[OK] Bluetooth settings page reached successfully.")

    def find_device(self, driver, device_name):
        """
        尋找藍牙裝置，不點擊，回傳 element
        Find a Bluetooth device by name and return the element without clicking.
        
        :param driver: Appium WebDriver instance
        :param device_name: Name of the device to find
        :return: WebElement if found, None otherwise
        :raises TimeoutException: If device cannot be found
        """
        # Generic scan button to refresh device list
        if self._wait_and_tap_first(driver, self.SCAN_BUTTON_LOCATORS, timeout_each=5, step_name="Scan/Refresh"):
            print("Scan/Refresh button found and clicked.")
            time.sleep(5)
        else:
            print("Scan/Refresh button not found. Using current device list...")
        
        # Create locators dynamically for the target device name
        device_locators = [
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{device_name}")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{device_name}")'),
            (AppiumBy.XPATH, f'//*[contains(@text, "{device_name}")]'),
            (AppiumBy.XPATH, f'//*[@text="{device_name}"]'),
        ]
        
        print(f"[ACTION] Searching for device: {device_name}")
        element = self._wait_and_get_with_scroll(driver, device_locators, step_name=f"Device {device_name}")
        
        if element is not None:
            print(f"[OK] Device '{device_name}' found.")
            return element
        else:
            self._save_debug_screenshot(driver, f"not_found_device_{device_name}")
            self._save_debug_page_source(driver, f"not_found_device_{device_name}")
            raise TimeoutException(f"Cannot find device '{device_name}' in device list")

    def find_and_tap_device(self, driver, device_name):
        """
        方法二: 尋找裝置並點擊，參數包含裝置名稱
        Find and tap a Bluetooth device by name in the device list.
        
        :param driver: Appium WebDriver instance
        :param device_name: Name of the device to find and tap
        :raises TimeoutException: If device cannot be found
        """
        # Generic scan button to refresh device list
        if self._wait_and_tap_first(driver, self.SCAN_BUTTON_LOCATORS, timeout_each=5, step_name="Scan/Refresh"):
            print("Scan/Refresh button found and clicked.")
            time.sleep(5)
        else:
            print("Scan/Refresh button not found. Using current device list...")
        
        # Create locators dynamically for the target device name
        device_locators = [
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{device_name}")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{device_name}")'),
            (AppiumBy.XPATH, f'//*[contains(@text, "{device_name}")]'),
            (AppiumBy.XPATH, f'//*[@text="{device_name}"]'),
        ]
        
        print(f"[ACTION] Searching for device: {device_name}")
        if self._wait_and_tap_with_scroll(driver, device_locators, device_name, step_name=f"Device {device_name}"):
            print(f"[OK] Device '{device_name}' found and tapped.")
            time.sleep(2)
        else:
            self._save_debug_screenshot(driver, f"not_found_device_{device_name}")
            self._save_debug_page_source(driver, f"not_found_device_{device_name}")
            raise TimeoutException(f"Cannot find device '{device_name}' in device list")

    def handle_pairing(self, driver, pairing_action="accept", pin_code="727816"):
        """
        方法三: 處理藍牙配對，參數包含 pairing action
        Handle Bluetooth pairing dialog with specified action.
        
        :param driver: Appium WebDriver instance
        :param pairing_action: Action to perform ('accept', 'cancel', 'unpair')
        :param pin_code: PIN code for pairing (for 'accept' action)
        :raises TimeoutException: If pairing action fails
        :raises ValueError: If pairing_action is not supported
        """
        pairing_action = pairing_action.lower().strip()
        print(f"[ACTION] Handling pairing with action: {pairing_action}")
        
        if pairing_action == "accept":
            self._handle_pairing_accept(driver, pin_code)
        elif pairing_action == "cancel":
            self._handle_pairing_cancel(driver)
        elif pairing_action == "unpair":
            self._handle_unpair(driver)
        else:
            raise ValueError(f"Unsupported pairing_action: {pairing_action}. Use 'accept', 'cancel', or 'unpair'.")
        
        print(f"[OK] Pairing action '{pairing_action}' completed successfully.")

    def _handle_pairing_accept(self, driver, pin_code="727816"):
        """Internal: Handle pairing accept flow."""
        if not self._wait_for_presence_first(
            driver,
            self.PAIRING_MESSAGE_LOCATORS,
            timeout_each=6,
            step_name="Pairing dialog",
        ):
            self._save_debug_screenshot(driver, "not_found_pairing_dialog")
            self._save_debug_page_source(driver, "not_found_pairing_dialog")
            raise TimeoutException("Pairing dialog did not appear")
        
        if not self._wait_and_type_first(
            driver,
            self.PAIRING_TEXT_EDIT_LOCATORS,
            text=pin_code,
            timeout_each=3,
            step_name="Pairing TextEdit",
        ):
            self._save_debug_screenshot(driver, "not_found_pairing_textedit")
            self._save_debug_page_source(driver, "not_found_pairing_textedit")
            raise TimeoutException("Cannot find TextEdit in pairing dialog")
        
        pair_button_locators = (
            self.PAIR_BUTTON_LOCATORS_OPPO if self.device_type == "oppo" else self.PAIR_BUTTON_LOCATORS
        )
        
        if not self._wait_and_tap_first(
            driver,
            pair_button_locators,
            timeout_each=3,
            step_name="Pair/OK",
        ):
            self._save_debug_screenshot(driver, "not_found_pair_button")
            self._save_debug_page_source(driver, "not_found_pair_button")
            raise TimeoutException("Cannot find Pair/OK button in pairing dialog")

    def _handle_pairing_cancel(self, driver):
        """Internal: Handle pairing cancel flow."""
        if not self._wait_for_presence_first(
            driver,
            self.PAIRING_MESSAGE_LOCATORS,
            timeout_each=6,
            step_name="Pairing dialog",
        ):
            self._save_debug_screenshot(driver, "not_found_pairing_dialog")
            self._save_debug_page_source(driver, "not_found_pairing_dialog")
            raise TimeoutException("Pairing dialog did not appear")
        
        if not self._wait_and_tap_first(
            driver,
            self.CANCEL_BUTTON_LOCATORS,
            timeout_each=3,
            step_name="Cancel",
        ):
            self._save_debug_screenshot(driver, "not_found_cancel_button")
            self._save_debug_page_source(driver, "not_found_cancel_button")
            raise TimeoutException("Cannot find Cancel button in pairing dialog")

    def _handle_unpair(self, driver):
        """Internal: Handle unpair flow with device-specific logic."""
        if self.device_type == "oppo":
            # OPPO: Direct unpair without confirm
            if not self._wait_and_tap_first(
                driver,
                self.UNPAIR_BUTTON_LOCATORS,
                timeout_each=5,
                step_name="Unpair",
            ):
                self._save_debug_screenshot(driver, "not_found_unpair_button")
                self._save_debug_page_source(driver, "not_found_unpair_button")
                raise TimeoutException("Cannot find Unpair button")
            print("[OK] OPPO unpair completed. Skipping confirm dialog.")
            return
        
        elif self.device_type == "samsung_or_galaxy":
            # Samsung: Tap device settings first
            samsung_device_details_locators = [
                (AppiumBy.ID, "com.android.settings:id/deviceDetails"),
                (AppiumBy.ID, "com.android.settings:id/layout_details"),
                (AppiumBy.XPATH, '//*[@resource-id="com.android.settings:id/deviceDetails"]'),
            ]
            if not self._wait_and_tap_first(
                driver,
                samsung_device_details_locators,
                timeout_each=5,
                step_name="Device settings",
            ):
                self._save_debug_screenshot(driver, "not_found_device_details")
                self._save_debug_page_source(driver, "not_found_device_details")
                raise TimeoutException("Cannot find Device settings button")
            time.sleep(1)
            
            unpair_button_locators = [
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Unpair")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Forget")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Remove")'),
                (AppiumBy.XPATH, '//*[@text="Unpair" or @text="Forget" or contains(@text,"Remove")]'),
            ]
            unpair_confirm_locators = [
                (AppiumBy.ID, "android:id/button1"),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")'),
                (AppiumBy.XPATH, '//*[@text="OK" or @text="Unpair" or @text="Confirm"]'),
            ]
        else:
            # Default (Xiaomi, etc.)
            unpair_button_locators = self.UNPAIR_BUTTON_LOCATORS
            unpair_confirm_locators = self.UNPAIR_CONFIRM_LOCATORS
        
        # Tap Unpair button
        if not self._wait_and_tap_first(
            driver,
            unpair_button_locators,
            timeout_each=5,
            step_name="Unpair",
        ):
            self._save_debug_screenshot(driver, "not_found_unpair_button")
            self._save_debug_page_source(driver, "not_found_unpair_button")
            raise TimeoutException("Cannot find Unpair button")
        
        # Try confirmation dialog (optional on some devices)
        if self._wait_and_tap_first(
            driver,
            unpair_confirm_locators,
            timeout_each=2,
            step_name="Unpair confirm",
        ):
            print("[OK] Unpair confirmation clicked.")
        else:
            print("[INFO] Unpair confirmation dialog not shown.")
