import os
from ..CommonSupportLib.StationDefines import DEVICE_NAME_K, PLATFORM_NAME_K, PLATFORM_VERSION_K, PHONE_UDID_K,\
    APP_PACKAGE_K, APP_ACTIVITY_K, MOBILE_TO_USE, COM_PORT_K, BAUD_RATE_K,MEDC, RPI_CLIENT, MOBILE_CLIENT_MBDA, \
    MOBILE_CLIENT_WTA, PHONE_BT_ADDRESS_K

#dut_friendly_name = "BLE_UART_824B"
#dut_friendly_name = "MBD_PERIPHERAL"
dut_friendly_name = "Direct A"
#===========================================
#   Zephyr test config
com_port = "COM24"
baud_rate = "115200"
zephyr_test_project = "BZ6_128M"
zephyr_test_version = "v1.0.0-rc5"
#zephyr_dut1_flashtool = "WBZ653002198"
#zephyr_dut2_flashtool = "WBZ653002023"
zephyr_dut1_flashtool = "WBZ653002200"
zephyr_dut2_flashtool = "WBZ653002198"
zephyr_dut2_com_port = "COM18"
zephyr_special_test_case = True
#===========================================
#com_port = '/dev/tty.usbmodem00159523561'
#baud_rate = "115200"
FW_Version = "0.9.0.6"
ota_upgrade_fw_version = "1.2.0.7"
ota_downgrade_fw_version = "1.2.0.6"
fw_ver_throughput = "wbz653_ble_uart_128_1.2.0.2_common.hex"
mbd_ver_android = "MBD_6.99.02"
mbd_ver_ios = "MBD_3.9.5"
ota_upgrade_bin_file = "wbz653_ble_uart_128_0.9.0.4_common.bin"
ota_downgrade_bin_file = "wbz653_ble_uart_128_0.9.0.3_common.bin"
ota_illegal_bin_file = "wbz351_ble_uart_1.1.0.1_common.bin"
HB_DUTS = {
    "DUT1": {
        COM_PORT_K: "COM80",
        BAUD_RATE_K: "921600",
        "Multilink_LED": "Disable",
        "FW_Version": "0.9.0.6",
        "BT_Address": "8CDE52E00C3B",
        "FlashTool": "RYN231900129",
        "VID_PID": "00DF",
        "USB_HUB": "YK25256",
        "USB_SLOT": "1"
    },
    "DUT2": {
        COM_PORT_K: "COM31",
        BAUD_RATE_K: "921600",
        "BT_Address": "3481F4AE0EC3",
        "FlashTool": "-TSMTI000000547",
        "VID_PID": "00DD",
        "USB_HUB": "YK25256",
        "USB_SLOT": "2"
    },
    "DUT3": {
        COM_PORT_K: "COM25",
        BAUD_RATE_K: "921600",
        "BT_Address": "3481F4AE0EC6",
        "FlashTool": "-TSMTI000000547",
        "VID_PID": "00D9",
        "USB_HUB": "YK25256",
        "USB_SLOT": "3"
    },
    "DUT4": {
        COM_PORT_K: "COM49",
        BAUD_RATE_K: "921600",
        "BT_Address": "3481F4AE0EBC",
        "FlashTool": "-TSMTI000000547",
        "VID_PID": "00DA",
        "USB_HUB": "YK25362",
        "USB_SLOT": "1"
    },
    "DUT5": {
        COM_PORT_K: "COM40",
        BAUD_RATE_K: "921600",
        "BT_Address": "3481F4AE0EBC",
        "FlashTool": "-TSMTI000000547",
        "VID_PID": "00DC",
        "USB_HUB": "YK25362",
        "USB_SLOT": "2"
    },
    "DUT6": {
        COM_PORT_K: "COM43",
        BAUD_RATE_K: "921600",
        "BT_Address": "3481F4AE0EBC",
        "FlashTool": "-TSMTI000000547",
        "VID_PID": "00DE",
        "USB_HUB": "YK25362",
        "USB_SLOT": "3"
    },
    "DUT7": {
        COM_PORT_K: "COM28",
        BAUD_RATE_K: "921600",
        "BT_Address": "3481F4AE0EBC",
        "FlashTool": "WBZ653002192",
        "VID_PID": "00DF",
        "USB_HUB": "YK25253",
        "USB_SLOT": "1"
    },
    "DUT8": {
        COM_PORT_K: "COM24",
        BAUD_RATE_K: "921600",
        "BT_Address": "3481F4AE0EBC",
        "FlashTool": "-TSMTI000000547",
        "VID_PID": "00DF",
        "USB_HUB": "YK25253",
        "USB_SLOT": "2"
    },
    "DUT9": {
        COM_PORT_K: "COM24",
        BAUD_RATE_K: "921600",
        "BT_Address": "3481F4AE0EBC",
        "FlashTool": "-TSMTI000000547",
        "VID_PID": "00DF",
        "USB_HUB": "YK25253",
        "USB_SLOT": "2"
    }
}

appium_config = {
    "appium_server_config": {
        #"appium_server_ip": "127.0.0.1",
        "appium_server_ip":  "10.160.59.64",
        #"appium_server_ip": "172.20.10.6",
        #"appium_server_ip":  "10.160.56.74",
        "appium_server_port": "4723",
        "use_remote_appium": True,
        "remote_appium_server_ip":  "10.160.59.59",
        "remote_appium_server_port": "4723",
        #"remote_appium_username": "WSGAppDev",
        #"remote_appium_pwd" : 'Amchp17217',
        "remote_appium_username": "Minglung",
        "remote_appium_pwd" : 'a6j3939b',
        #"remote_appium_username": "MCHP",
        #"remote_appium_pwd" : 'mchp',
        "usb_hubs" : ['20-2.1', '20-2.2']
    },

    "mobile_data_config": {
        "MyMac":    {DEVICE_NAME_K  : "MyMac",
                    PHONE_UDID_K : "f7e49f0799d364921337d742842e3f3a0274fb6d",
                    PLATFORM_NAME_K : "mac",
                    PLATFORM_VERSION_K : "16.2"
        },
        "MyiPhone": {DEVICE_NAME_K  : "iPhone12 Pro",
                    PHONE_UDID_K : "00008101-000C54E83ED8001E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "17.4.1"
        },
        "MyiPad": {DEVICE_NAME_K  : "iPad",
                    PHONE_UDID_K : "00008101-0011645C3428801E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "18"
        },
        "iPadAir5": {DEVICE_NAME_K  : "iPad",
                    PHONE_UDID_K : "00008103-0001583C2E63401E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "15.6"
        },
        "iPhone8": {DEVICE_NAME_K  : "iPhone8",
                    PHONE_UDID_K : "f7e49f0799d364921337d742842e3f3a0274fb6d",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "16.2"
        },
        "iPhoneSE": {DEVICE_NAME_K  : "iPhoneSE",
                    PHONE_UDID_K : "00008030-000545023EF3802E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "16.2"
        },
        "iPhone13": {DEVICE_NAME_K  : "iPhone13",
                    PHONE_UDID_K : "00008120-00084D3E2261A01E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "16.2"
        },
        "iPhone14": {DEVICE_NAME_K  : "iPhone14",
                    PHONE_UDID_K : "00008110-000E10C90AE1401E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "16.2"
        },
        "iPhone 15": {DEVICE_NAME_K  : "iPhone 15",
                    PHONE_UDID_K : "00008120-00084D3E2261A01E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "18.1.1"
        },
        "iPhone 16": {DEVICE_NAME_K  : "iPhone 16",
                    PHONE_UDID_K : "00008140-00165DDE3E2B001C",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "26"
        },
        "iPhone XR": {DEVICE_NAME_K  : "iPhone XR",
                    PHONE_UDID_K : "00008020-001658643485002E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "15.7"
        },
        "iPhone11": {DEVICE_NAME_K  : "iPhone 11",
                    PHONE_UDID_K : "00008030-001570A01182402E",
                    PLATFORM_NAME_K : "iOS",
                    PLATFORM_VERSION_K : "15.7"
        },
        "iPhoneX": {DEVICE_NAME_K  : "iPhone X",
                    PHONE_UDID_K : "f84c62ee08fc8de199e52b02e8a0119815d56843",
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
        "GooglePixel5a": {DEVICE_NAME_K: "GooglePixel5a",
                   PHONE_UDID_K: "1B271JEG500672",
                   PLATFORM_NAME_K:"Android",
                   PLATFORM_VERSION_K: "12",
                   PHONE_BT_ADDRESS_K :"60b76e0ce11b",
        },
        "GooglePixel8": {DEVICE_NAME_K: "GooglePixel8",
                   PHONE_UDID_K: "39051FDJH001RT",
                   PLATFORM_NAME_K:"Android",
                   PLATFORM_VERSION_K: "12",
                   PHONE_BT_ADDRESS_K :"60b76e0ce11b",
        },
        "GooglePixel8Pro": {DEVICE_NAME_K: "GooglePixel8Pro",
                   PHONE_UDID_K: "3B111FDJG002Q4",
                   PLATFORM_NAME_K:"Android",
                   PLATFORM_VERSION_K: "12",
                   PHONE_BT_ADDRESS_K :"60b76e0ce11b",
        },
        "VivoV11": {DEVICE_NAME_K: "VivoV11",
                   PHONE_UDID_K: "cbc2460f",
                   PLATFORM_NAME_K:"Android",
                   PLATFORM_VERSION_K: "10",
                   PHONE_BT_ADDRESS_K :"4466fc8eb57a",
        },
        "VivoV9": {DEVICE_NAME_K: "VivoV9",
                    PHONE_UDID_K: "c6f4ca80",
                    PLATFORM_NAME_K: "Android",
                    PLATFORM_VERSION_K: "10",
                    PHONE_BT_ADDRESS_K: "4466fc8eb57a",
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
        "Vivo X100": {DEVICE_NAME_K: "Vivo X100",
                        PHONE_UDID_K: "10BE2N1J3L000CH",
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
        "Oppo F27 Pro": {DEVICE_NAME_K: "Oppo F27 Pro",
                       PHONE_UDID_K: "PFV8WSBYGAON8HNR",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "11",
                       },
        "SamsungS21": {DEVICE_NAME_K: "SamsungS21",
                      PHONE_UDID_K: "R5CRA1Q8G7Y",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "12",
                      },
        "Pixel3XL": {DEVICE_NAME_K: "pixel3",
                       PHONE_UDID_K: "8AHY0L87L",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "11",
                       },
        "Pixel7": {DEVICE_NAME_K: "Pixel 7",
                      PHONE_UDID_K: "28101FDH2005ML",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "14",
                      PHONE_BT_ADDRESS_K: "A8798DA59882",
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
        "Oneplus7T": {DEVICE_NAME_K: "Oneplus7T",
                       PHONE_UDID_K: "7ed78464",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "12",
                       PHONE_BT_ADDRESS_K :"A8798DA59882",
                       },
        "Oneplus7": {DEVICE_NAME_K: "Oneplus7",
                       PHONE_UDID_K: "906af0b3",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "12",
                       PHONE_BT_ADDRESS_K :"A8798DA59882",
                       },
        "SamsungS8": {DEVICE_NAME_K: "SamsungS8",
                      PHONE_UDID_K: "ce011821c459252804",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "12",
                      PHONE_BT_ADDRESS_K: "A8798DA59882",
                      },
        "SamsungA51": {DEVICE_NAME_K: "SamsungA51",
                      PHONE_UDID_K: "RZCX90H9BNY",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "13",
                      PHONE_BT_ADDRESS_K: "A8798DA59882",
                      },
        "SamsungA54": {DEVICE_NAME_K: "SamsungA54",
                       PHONE_UDID_K: "R5CW321G69K",
                       PLATFORM_NAME_K: "Android",
                       PLATFORM_VERSION_K: "14",
                       PHONE_BT_ADDRESS_K :"F85B6E51B67B",
                       },
        "SamsungM34": {DEVICE_NAME_K: "SamsungM34",
                      PHONE_UDID_K: "RZCX5226ARL",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "13",
                      PHONE_BT_ADDRESS_K: "A8798DA59882",
                      },
        "SamsungS24": {DEVICE_NAME_K: "SamsungS24",
                      PHONE_UDID_K: "RZCX90H9KEA",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "13",
                      PHONE_BT_ADDRESS_K: "A8798DA59882",
                      },
        "Samsung_S24": {DEVICE_NAME_K: "Samsung_S24",
                      PHONE_UDID_K: "RZCX90H9BNY",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "13",
                      PHONE_BT_ADDRESS_K: "A8798DA59882",
                      },
        "Galaxy_Z_Flip6": {DEVICE_NAME_K: "Galaxy_Z_Flip6",
                      PHONE_UDID_K: "R5CX717787Y",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "15",
                      PHONE_BT_ADDRESS_K: "A8798DA59882",
                      },
        "Galaxy_Z_Flip7": {DEVICE_NAME_K: "Galaxy_Z_Flip7",
                      PHONE_UDID_K: "R5CY71ENLVH",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "16",
                      PHONE_BT_ADDRESS_K: "A8798DA59882",
                      },
        "Nokia": {DEVICE_NAME_K: "Nokia 7.2",
                      PHONE_UDID_K: "J0AA002438K12702783",
                      PLATFORM_NAME_K: "Android",
                      PLATFORM_VERSION_K: "12",
                      PHONE_BT_ADDRESS_K: "A8798DA59882",
                      },
        "Nokia72": {DEVICE_NAME_K: "Nokia 7.2",
                  PHONE_UDID_K: "J0AA002436JA0702290",
                  PLATFORM_NAME_K: "Android",
                  PLATFORM_VERSION_K: "12",
                  PHONE_BT_ADDRESS_K: "A8798DA59882",
                  },
        "WBZ451": {DEVICE_NAME_K: "WBZ451",
                    PLATFORM_NAME_K: "Chimera",
                    },
        "WBZ351": {DEVICE_NAME_K: "WBZ451",
                   PLATFORM_NAME_K: "Buckland",
                   },
        "WBZ653": {DEVICE_NAME_K: "WBZ653",
                   PLATFORM_NAME_K: "BigBuck",
                   },
        "Vivo V9": {DEVICE_NAME_K: "Vivo V9",
                   PHONE_UDID_K: "c6f4ca80",
                   PLATFORM_NAME_K:"Android",
                   PLATFORM_VERSION_K: "9",
                   PHONE_BT_ADDRESS_K :"3CA616BE9794",
        },

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
    "ios_lightblue_application":{
        APP_PACKAGE_K: "com.PunchThrough.LightBlue"
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
    MOBILE_TO_USE: "Galaxy_Z_Flip7",
    "server":"DUT1",
    "client":"DUT2"
}

multilink_phone_config = {
    MOBILE_TO_USE: "Pixel7"
    #MOBILE_TO_USE: "Pixel7/SamsungS23/Pixel17217"
    #MOBILE_TO_USE: "SamsungA54/Pixel7/iPhone15/Pixel17217/SamsungS23"
}

DUT_ADD_K = "001167939393"
client = MEDC
mcpfolderpath = r'C:\BLEAF\ExternalDependencies\MCP2210CLI'
fwfolderpath = os.getcwd() + '\\Test firmware\\Zephyr\\'
capture_sodera_logs = False
sedora_logs_folder_path = r"D:\A\Automation\Humming Bird\hummingbird_scripts\BLEAF\Logs"
RpiIpAddress = "192.168.0.100"
RpiUserName = "pi"
RpiPassword = "raspberrybleaf"
sodera_server_ip = '10.41.33.34'
sodera_server_port = 22901
sodera_fts_path = "C:\Program Files (x86)\Teledyne LeCroy Wireless\Wireless Protocol Suite 1.60\Executables\Core;Sodera"
sodera_server_path = "C:\Program Files (x86)\Teledyne LeCroy Wireless\Wireless Protocol Suite 1.60\Executables\Core\FTSAutoServer"
wps_path = r"C:\Program Files (x86)\Teledyne LeCroy Wireless\Wireless Protocol Suite 2.60"
duts_to_be_flashed = "DUT1"
dut_list = "DUT1,DUT2,DUT3,DUT4"
peripheral_dut_list = "DUT2,DUT3"
central_multilink_peripheral_list = ["DUT2"]
usb_hubs = ["YK25256","YK25362","YK25253"]
pid = "00D8"
#multilink_phone_list = ["SamsungS22","SamsungS24","GooglePixel5","GooglePixel3A","SamsungS10","SamsungM34"]
multilink_phone_list = ['iPhone 16', 'Pixel7']
#multilink_phone_list = ['Pixel7', 'SamsungA54', 'iPhone 16']
#multilink_phone_list = ['iPhone 16']
multirole_phone_list = ["SamsungS21"]
throughput_phone_list = "Vivo X100"
testlink_project = "BigBuck"
testlink_devkey = "29b1991c2f36a6e9e8cab12e502c47cf"
#mplab_path = "C:/Program Files/Microchip/MPLABX/v6.25/mplab_platform/mplab_ipe/ipecmd.exe"
mplab_path = "C:\\Program Files\\Microchip\\MPLABX\\v6.25\\mplab_platform\\mplab_ipe\\ipecmd.exe"

###### HUT CODE TESTS CONFIG ######


dut_config = {
  "Project": "Chimera",
  "Comport": "COM50",
  "Baudrate": "115200",
  "given_dev_addr" : "9C956E400E45",
  "fw_version" : "v5.1"
}

read_clk_values = {
  "clock_64" : "0090D003",
  "clock_32" : "0048e801",
  "clock_16" : "0024F400",
  "clock_8"  : "00127A00",
  "clock_48" : "006cdc02",
  "clock_24" : "00366e01",
  "clock_12"  : "001bb700"
}

memory_values = {
  "write_memory" : "22001413",
  "wr_mem_32" : "2122330F"
}

pmu_write_values = {
  "reg_14" : "6B85",
  "reg_15" : "2367",
  "reg_16" : "2e6f",
  "reg_17" : "063E",
  "reg_18" : "063E"
}

#PTA configuration
ttl_com_port ="COM94"
ttl_baud_rate = "230400"
pta_wifi_name = "ASUS_6F_Lab"
pta_security_type = "2"
pta_security_key = "microchip" # password
pta_channel = "6"

test_status = {"state": "not started"}
pta_tx_transfer = None
pta_rx_transfer = None