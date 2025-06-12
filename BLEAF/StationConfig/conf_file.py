import os
from ..CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K,\
    APP_PACKAGE_K, APP_ACTIVITY_K, MOBILE_TO_USE, COM_PORT_K, BAUD_RATE_K,MEDC, RPI_CLIENT, MOBILE_CLIENT_MBDA, MOBILE_CLIENT_WTA, PHONE_BT_ADDRESS_K

# dut_friendly_name = "BLE_UART_D46B_H" #D46B_H, 6C3B
#dut_friendly_name = "BLE_UART_8242"
#dut_friendly_name = "BLE_UART_436F"
dut_friendly_name = "BLE_UART_CDDF_H"
#dut_friendly_name = "MBD_PERIPHERAL"
# com_port = "COM29"
com_port = "COM15"
baud_rate = "115200"
FW_Version = "1.2.0.0"
ota_upgrade_fw_version = "1.1.1.1"
ota_downgrade_fw_version = "1.1.0.5"

appium_config = {
    "appium_server_config": {
        "appium_server_ip":  "127.0.0.1",
        "appium_server_port": "4723",
        "remote_appium_server_ip":  "10.160.54.60",
        "remote_appium_server_port": "4723",
        "remote_appium_username": "WSGAppDev",
        "remote_appium_pwd" : 'Amchp17217'
    },

    "mobile_data_config": {
        "iPhone8": {DEVICE_NAME_K  : "iPhone8",
                    PHONE_UDID_K : "f7e49f0799d364921337d742842e3f3a0274fb6d",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "16.2"
        },
        "iPhone12 Pro": {DEVICE_NAME_K  : "iPhone12 Pro",
                    PHONE_UDID_K : "00008101-000C54E83ED8001E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "17.4.1"
        },
        "iPhone13": {DEVICE_NAME_K  : "iPhone13",
                    PHONE_UDID_K : "00008110-00061D340E11801E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "16.2"
        },
        "iPhone14": {DEVICE_NAME_K  : "iPhone14",
                    PHONE_UDID_K : "00008110-000E10C90AE1401E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "16.2"
        },
        "iPhone15": {DEVICE_NAME_K  : "iPhone15",
                    PHONE_UDID_K : "00008120-0019581E2212201E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "17"
        },
        "iPhone XR": {DEVICE_NAME_K  : "iPhone XR",
                    PHONE_UDID_K : "00008020-001658643485002E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "15.7"
        },
        "GooglePixel3A": {DEVICE_NAME_K: "GooglePixel3A",
                   PHONE_UDID_K: "94JAY0PR7J",
                   PLATFORM_NAME_K:"Android",
                   PLATFORM_VERSION_K: "10",
                   PHONE_BT_ADDRESS_K :"4466fc8eb57a",
        },
        "GooglePixel5": {DEVICE_NAME_K: "GooglePixel5",
                   PHONE_UDID_K: "0A011FDD40033A",
                   PLATFORM_NAME_K:"Android",
                   PLATFORM_VERSION_K: "12",
                   PHONE_BT_ADDRESS_K :"60b76e0ce11b",
        },
        "Pixel7": {DEVICE_NAME_K: "Pixel7",
                   PHONE_UDID_K: "28101FDH2005ML",
                   PLATFORM_NAME_K:"Android",
                   PLATFORM_VERSION_K: "14",
                   PHONE_BT_ADDRESS_K :"60b76e0ce11b",
        },
        "VivoV11": {DEVICE_NAME_K: "VivoV11",
                   PHONE_UDID_K: "cbc2460f",
                   PLATFORM_NAME_K:"Android",
                   PLATFORM_VERSION_K: "10",
                   PHONE_BT_ADDRESS_K :"4466fc8eb57a",
        },
        "SamsungS10": {DEVICE_NAME_K: "SamsungS10",
                     PHONE_UDID_K: "RZ8M30NNGPH",
                     PLATFORM_NAME_K: "Android",
                     PLATFORM_VERSION_K: "11",
        },
        "Vivo X80": {DEVICE_NAME_K: "Vivo X80",
                     PHONE_UDID_K: "1595890050000CT",
                     PLATFORM_NAME_K:"Android",
                     PLATFORM_VERSION_K: "12",
                     PHONE_BT_ADDRESS_K :"90d4736e7c89",
        },
        "OppoR15": {DEVICE_NAME_K: "OppoR15",
                       PHONE_UDID_K: "c4d8a872",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "11",
                       PHONE_BT_ADDRESS_K :"4466fc8eb57a",
        },
        "OPPO Reno": {DEVICE_NAME_K: "OPPO Reno",
                       PHONE_UDID_K: "7bdb6931",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "11",
                       },
        "SamsungS21": {DEVICE_NAME_K: "SamsungS21",
                      PHONE_UDID_K: "R5CRA1Q8G7Y",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "12",
                      },
        "Pixel3": {DEVICE_NAME_K: "pixel3",
                       PHONE_UDID_K: "8AHY0L87L",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "11",
                       },
        "Pixel17217": {DEVICE_NAME_K: "pixel17217",
                       PHONE_UDID_K: "FA6CM0301069",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "10",
                       },
        "Xiaomi12Pro": {DEVICE_NAME_K: "Xiaomi12Pro",
                       PHONE_UDID_K: "be16c1a7",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "12",
                       PHONE_BT_ADDRESS_K :"4ce0db291f55",
                       },
        "OnePlus10Pro": {DEVICE_NAME_K: "OnePlus10Pro",
                       PHONE_UDID_K: "ef205d3e",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "12",
                       PHONE_BT_ADDRESS_K :"487412956a9a",
                       },
        "SamsungS22": {DEVICE_NAME_K: "SamsungS22",
                       PHONE_UDID_K: "R5CT70LTM1L",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "12",
                       PHONE_BT_ADDRESS_K :"A8798DA59882",
                       },
        "SamsungS23": {DEVICE_NAME_K: "SamsungS23",
                       PHONE_UDID_K: "RFCW11ESANK",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "14",
                       PHONE_BT_ADDRESS_K :"F85B6E51B67B",
                       },
        "SamsungA54": {DEVICE_NAME_K: "SamsungA54",
                       PHONE_UDID_K: "R5CW321G69K",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "14",
                       PHONE_BT_ADDRESS_K :"F85B6E51B67B",
                       },
        "Vivo V9": {DEVICE_NAME_K: "Vivo V9",
                   PHONE_UDID_K: "c6f4ca80",
                   PLATFORM_NAME_K:"Android",
                   PLATFORM_VERSION_K: "9",
                   PHONE_BT_ADDRESS_K :"3CA616BE9794",
        }
    },
    "target_application":{
        APP_PACKAGE_K: "com.microchip.bluetooth.data",
        APP_ACTIVITY_K: "com.microchip.bleanalyser.SplashScreen"
    },
    "mobile_settings": {
        APP_PACKAGE_K : "com.android.settings",
        APP_ACTIVITY_K: "com.android.settings.Settings"
    },
    "ios_mbda_application":{
        APP_PACKAGE_K: "com.microchip.MBD"
    },

    "ios_settings":{
        APP_PACKAGE_K : "com.apple.Preferences"
    },
    "lightblue_application":{
        APP_PACKAGE_K: "com.punchthrough.lightblueexplorer",
        APP_ACTIVITY_K: "com.punchthrough.lightblueexplorer.MainActivity"
    }

}

duts_to_use = {
    MOBILE_TO_USE: "SamsungA54",
    "server":"DUT1",
    "client":"DUT2"
}

multilink_phone_config = {
    MOBILE_TO_USE: "SamsungA54"
    #MOBILE_TO_USE: "SamsungA54/Pixel7"
    #MOBILE_TO_USE: "SamsungA54/Pixel7/iPhone15/Pixel17217/SamsungS23"
}

DUT_ADD_K = "001167939393"
client = MEDC
mcpfolderpath = r'C:\BLEAF\ExternalDependencies\MCP2210CLI'
fwfolderpath = os.getcwd() + '\\BLE_UART_FW\\'
capture_sodera_logs = False
sedora_logs_folder_path = r"D:\A\Automation\Humming Bird\hummingbird_scripts\BLEAF\Logs"
RpiIpAddress = "192.168.0.100"
RpiUserName = "pi"
RpiPassword = "raspberrybleaf"
sodera_server_ip = '10.41.33.34'
sodera_server_port = 22901
sodera_fts_path = "C:\Program Files (x86)\Teledyne LeCroy Wireless\Wireless Protocol Suite 1.30\Executables\Core;Sodera"
sodera_server_path = "C:\Program Files (x86)\Teledyne LeCroy Wireless\Wireless Protocol Suite 1.30\Executables\Core\FTSAutoServer"