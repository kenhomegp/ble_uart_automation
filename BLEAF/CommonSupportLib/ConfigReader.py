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
        self.use_remote_appium = appium_server_details.get("use_remote_appium")
        self.usb_hubs = appium_server_details.get("usb_hubs")

        ios_mbda_app = conf.appium_config.get("ios_mbda_application")
        self.ios_mbda_app_package = ios_mbda_app.get(APP_PACKAGE_K)

        ios_lightblue_app = conf.appium_config.get("ios_lightblue_application")
        self.ios_lightblue_app_package = ios_lightblue_app.get(APP_PACKAGE_K)

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
        self.mplab_path = conf.mplab_path

        self.evbName = {"DUT1": conf.HB_DUTS.get("DUT"), "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "","DUT8":"","DUT9":""}
        self.comport = {"DUT1": "", "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "","DUT8":"","DUT9":""}
        self.ver_DUT_FW = {"DUT1": "", "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "","DUT8":"","DUT9":""}
        self.Support_LED_Multilink = {"DUT1": "", "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "","DUT8":"","DUT9":""}
        self.DUT_BT_Addr = {"DUT1": "", "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "","DUT8":"","DUT9":""}
        self.DUT_VID_PID = {"DUT1": "", "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "","DUT8":"","DUT9":""}
        self.DUT_FLOW = {"DUT1": False, "DUT2": False, "DUT3": False, "DUT4": False, "DUT5": False, "DUT6": False,
                    "DUT7": False,"DUT8":False,"DUT9":False}
        self.g_Com_DUT = {"DUT1": "", "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "","DUT8":"","DUT9":""}
        self.sbi_baudrate = {"DUT1": 115200, "DUT2": 115200, "DUT3": 115200, "DUT4": 115200, "DUT5": 115200, "DUT6": 115200,
                        "DUT7": 115200,"DUT8": 115200,"DUT9":115200}
        self.sb_baudrate = {"DUT1": 115200, "DUT2": 115200, "DUT3": 115200, "DUT4": 115200, "DUT5": 115200, "DUT6": 115200,
                       "DUT7": 115200,"DUT8": 115200,"DUT9":115200}
        self.usb_hub = {"DUT1": "", "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "","DUT8": "","DUT9":""}
        self.usb_slot = {"DUT1": "", "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "","DUT8": "","DUT9":""}
        self.dut_address = {"DUT1": "", "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "","DUT8": "","DUT9":""}
        self.dut_serial = {"DUT1": "", "DUT2": "", "DUT3": "", "DUT4": "", "DUT5": "", "DUT6": "", "DUT7": "",
                            "DUT8": "", "DUT9": ""}
        self.dut_list = str(conf.dut_list).split(",")
        self.peripheral_dut_list = str(conf.peripheral_dut_list).split(",")
        self.central_multilink_peripheral_list = str(conf.central_multilink_peripheral_list).split(",")
        self.thoughput_phone_list = str(conf.throughput_phone_list).split(",")
        for dut in self.dut_list:
            if dut != "":
                self.comport[dut] = conf.HB_DUTS.get(dut).get(COM_PORT_K)
                self.DUT_VID_PID[dut] = conf.HB_DUTS.get(dut).get('VID_PID')
                self.usb_hub[dut]=conf.HB_DUTS.get(dut).get('USB_HUB')
                self.usb_slot[dut]=conf.HB_DUTS.get(dut).get('USB_SLOT')
                self.dut_address[dut] = conf.HB_DUTS.get(dut).get('BT_Address')
                self.dut_serial[dut] = conf.HB_DUTS.get(dut).get('FlashTool')
        self.hub_list = conf.usb_hubs
        self.multilink_phone_list = conf.multilink_phone_list
        self.multirole_phone_list = conf.multirole_phone_list
        self.host_name = os.system("hostname")
        self.duts_to_be_flashed = str(conf.duts_to_be_flashed).split(",")








