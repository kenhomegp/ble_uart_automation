import os
from shutil import copy
from .StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K, \
    APP_PACKAGE_K, APP_ACTIVITY_K, MOBILE_TO_USE, COM_PORT_K, BAUD_RATE_K, PHONE_BT_ADDRESS_K

AUTOMATED_SCRIPTS_PATH = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, )))
STATION_CONFIG_DIR = 'D:\\StationConfig'  # Directory in AUTOMATED_SCRIPTS_PATH where configuration files are located
_CONF_FILE_NAME = 'conf_file.py'
_CONF_FILE_FULL_PATH = os.path.join(AUTOMATED_SCRIPTS_PATH, STATION_CONFIG_DIR, _CONF_FILE_NAME)
_CONF_LOCAL_FULL_PATH = os.path.join(STATION_CONFIG_DIR, _CONF_FILE_NAME)


class ConfigReader:
    def __init__(self):
        if os.path.isfile(_CONF_LOCAL_FULL_PATH):
            copy(_CONF_LOCAL_FULL_PATH, _CONF_FILE_FULL_PATH)
        from ..StationConfig import conf_file as conf
        self.appium_server_ip = None
        self.appium_server_port = None
        self.mobile_to_use = None
        self.mobile_device_name = None
        self.mobile_device_udid = None
        self.mobile_platform_name = None
        self.mobile_platform_version = None
        self.app_activity = None
        self.wta_app_activity = None
        self.app_package = None
        self.wta_app_package = None

        self.dut_com_port = None
        self.dut_baud_rate = None
        self.dut_app = None
        self.server_dut = None
        self.server_dut_com_port = None
        self.server_dut_baud_rate = None
        self.client_dut = None
        self.client_dut_com_port = None
        self.client_dut_baud_rate = None
        self.sedora_logs_folder_path = ""
        self.mobile_bt_add = None
        self.client = ""
        self.mcpfolderpath = ""
        self.RpiIpAddress = ""
        self.RpiUserName = ""
        self.RpiPassword = ""

        self.mobile_data_config = {}

        self.mobile_data_config = conf.appium_config.get("mobile_data_config")

        self.mobile_to_use = conf.duts_to_use.get(MOBILE_TO_USE)

        self.multilink_phone_config = conf.multilink_phone_config.get(MOBILE_TO_USE)

        # Add here
        appium_server_details = conf.appium_config.get("appium_server_config")
        self.com_port = conf.com_port
        self.baud_rate = conf.baud_rate
        self.appium_server_ip = appium_server_details.get("appium_server_ip")
        self.appium_server_port = appium_server_details.get("appium_server_port")
        self.remote_appium_server_ip = appium_server_details.get("remote_appium_server_ip")
        self.remote_appium_server_port = appium_server_details.get("remote_appium_server_port")
        self.remote_appium_username = appium_server_details.get("remote_appium_username")
        self.remote_appium_pwd = appium_server_details.get("remote_appium_pwd")

        ios_mbda_app = conf.appium_config.get("ios_mbda_application")
        self.ios_mbda_app_package = ios_mbda_app.get(APP_PACKAGE_K)

        ios_settings_app = conf.appium_config.get("ios_settings")
        self.ios_settings_app_package = ios_settings_app.get(APP_PACKAGE_K)

        mbda_mobile_app = conf.appium_config.get("target_application")
        self.app_package = mbda_mobile_app.get(APP_PACKAGE_K)
        self.app_activity = mbda_mobile_app.get(APP_ACTIVITY_K)

        mobile_setting = conf.appium_config.get("mobile_settings")
        self.mobile_setting_app_package = mobile_setting.get(APP_PACKAGE_K)
        self.mobile_setting_app_activity = mobile_setting.get(APP_ACTIVITY_K)

        lightblue_mobile_app = conf.appium_config.get("lightblue_application")
        self.lightblue_app_package = lightblue_mobile_app.get(APP_PACKAGE_K)
        self.lightblue_app_activity = lightblue_mobile_app.get(APP_ACTIVITY_K)

        self.server_dut = conf.duts_to_use.get("server")
        self.client_dut = conf.duts_to_use.get("client")
        self.client = conf.client
        self.mcpfolderpath = conf.mcpfolderpath
        self.fwfolderpath = conf.fwfolderpath
        self.capture_sodera_logs = conf.capture_sodera_logs
        self.sedora_logs_folder_path = conf.sedora_logs_folder_path
        self.RpiIpAddress = conf.RpiIpAddress
        self.RpiUserName = conf.RpiUserName
        self.RpiPassword = conf.RpiPassword
        self.sodera_server_ip = conf.sodera_server_ip
        self.sodera_server_port = conf.sodera_server_port
        self.sodera_fts_path = conf.sodera_fts_path
        self.sodera_server_path = conf.sodera_server_path
