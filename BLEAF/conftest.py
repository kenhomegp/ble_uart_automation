import sys

import pytest
import os

#from soupsieve.util import lower

from .CommonSupportLib.StationData import stationData
from .CommonSupportLib.ConfigReader import ConfigReader
from .CommonSupportLib.TestLinkAPI import TestLink
from .BaseWrappers.SSHSupport import ShellHandler

import subprocess
import time
sd = stationData()
conf = ConfigReader()
sd.config = conf
current_path = os.getcwd()
fwfolderpath_Chimera = current_path + '/BLE_UART_FW/' + 'FW_Chimera/'
fwfolderpath_Buckland = current_path + '/BLE_UART_FW/' + 'FW_Buckland/'
global fwfolderpath_Bigbuck
fwfolderpath_Bigbuck = current_path + '/BLE_UART_FW/' + 'FW_Bigbuck/'
rerun_list = []
def setup_test_link():
    sd.test_link = TestLink()

def get_tests_to_execute(tp_name):
    tests_to_execute = sd.test_link.get_tests_to_execute(tp_name)
    return tests_to_execute

def pytest_addoption(parser):
    parser.addoption(
        "--tp_name",
        action="store",
        metavar="SAMPLE_TEST_PLAN",
        help="only run tests matching the environment NAME.",
    )
    parser.addoption(
        "--rerun",
        action="store",
        metavar="RERUN TEST CASES",
        help="if y or yes in present, previously passed TC in the test plan will not be executed",
        default="no"
    )
    parser.addoption(
        "--mobile_app",
        action="store",
        metavar="Test mobile app",
        help="Mobile app option",
        default="no"
    )
    parser.addoption(
        "--multilink",
        action="store_true",
        help="New option for Zephyr identity",
        default=False
    )
    parser.addoption(
        "--dfu",
        action="store_true",
        help="Device firmware upgrade",
        default=False
    )

def pytest_configure(config):
    config.addinivalue_line("markers",
                            "test_id(id): marker with test id corresponding to testlink test case")
    sd.test_link = None
    sd.tc_list = []
    sd.tc_values = []
    #sd.platform = 'SamsungA54'
    sd.platform = sd.config.mobile_to_use
    print("pytest_configure.sd.platform = {}".format(sd.platform))

    '''
    test_plan_name = config.getoption('tp_name')
    rerun = config.getoption('rerun')
    setup_test_link()
    sd.tp_id = sd.test_link.get_test_plan_id(test_plan_name)
    tc_dict = get_tests_to_execute(test_plan_name)
    sd.test_cases_dict = tc_dict
    sd.tc_list = list(sd.test_cases_dict.keys())
    sd.tc_values = list(sd.test_cases_dict.values())
    if lower(rerun) == 'yes' or lower(rerun) == 'y':
        for tc in sd.tc_list:
            tc_res = sd.test_cases_dict.get(tc)['exec_status']
            if "p" in tc_res:
                tc_dict.pop(tc)
    platform = ''
    sd.tc_list = list(sd.test_cases_dict.keys())
    sd.tc_values = list(sd.test_cases_dict.values())
    try:
        platform = tc_dict.get(sd.tc_list[0])['platforms'][0]
        firmware_update(test_plan_name)
    except KeyError:
        print("Platform not specified in test plan. Default platform will be used.")
    available_platforms = list(sd.config.mobile_data_config.keys()) + ['MEDC', 'RPI_4B']
    if platform:
        assert platform in available_platforms,  "The platform provided in test plan: " \
                                                "{} is not among available platforms: {}".format(platform, available_platforms)
        sd.platform = platform
    else:
        sd.platform = sd.config.mobile_to_use
    # testbed_controls(test_plan_name)
    '''

def pytest_collection_modifyitems(session, config, items):
    selected_items = []
    if sd.platform == 'RPI_4B':
        for item in items:
            marker_list = item.iter_markers()
            #print("Selected tests for execution1")
            for mark in marker_list:
                if mark.name == "test_id":
                    test_id = mark.args[0]
                    if test_id in sd.tc_list and mark.args[1] == 'RPI_4B':
                        selected_items.append(item)
    else:
        for item in items:
            marker_list = item.iter_markers()
            #print("Selected tests for execution1")
            for mark in marker_list:
                print(mark.name)
                selected_items.append(item)
                print("Selected tests for execution")
            '''
            for mark in marker_list:
                if mark.name == "test_id":
                    test_id = mark.args[0]
                    if test_id in sd.tc_list and mark.args[1] != 'RPI_4B':
                        # print(sd.test_cases_dict.get(test_id)['exec_status'])
                        # if sd.test_cases_dict.get(test_id)['exec_status']  != 'p':
                            selected_items.append(item)
                            print("Selected tests for execution")
            '''
    items[:] = selected_items


def pytest_runtest_setup(item):
    print("Execute collected tests")

@pytest.fixture(scope="session", autouse=True)
def create_station_data():
    print("calling session fixture")
    sd = stationData()
    conf = ConfigReader()
    sd.config = conf
    print("station data object initialized: {}".format(sd))
    pytest.sd = sd

@pytest.fixture(scope="class", autouse=True)
def default_class_fixture(request):
    print("calling default class fixture")
    request.cls.test_string = "This is default class fixture"

    def class_finalizer():
        print("This is class finalizer")
        # slot_turn_off_cmd = "uhubctl -l {0} -p {1} -a 0"
        # for hubs in conf.usb_hubs:
        #     hub_slot = 0
        #     while hub_slot <= 6:
        #         print(slot_turn_off_cmd.format(hubs, hub_slot))
        #         hub_slot += 1
        #         sh_in, sh_out, sh_error = sd.ssh_handler.execute(slot_turn_off_cmd.format(hubs, hub_slot))
        #         if sh_error:
        #             assert False, "Failed to turn on the USB hub slot. Command output: {}".format(sh_out)
        #
        # sh_in, sh_out, sh_error = sd.ssh_handler.execute("uhubctl -l {}".format(hubs))
        # power_count = 0
        # for line in sh_out:
        #     if "off" in line:
        #         power_count += 1
        #
        # if power_count == 7:
        #     print("Powered Off the hub")
    request.addfinalizer(class_finalizer)


@pytest.fixture(scope="function", autouse=True)
def default_function_fixture_main(request):
    print("calling default function fixture")
    request.cls.test_result = False
    request.cls.test_output = ""
    request.cls.note = ""
    def function_finalizer():
        test_marker = request.node.get_closest_marker('test_id')
        if test_marker is not None:
            test_id = test_marker.args[0]
            print("test_id = {}".format(test_id))
        #external_id = sd.test_cases_dict.get(test_id)['id']
        #build_id = sd.test_cases_dict.get(test_id)['build']
        result = 'f'
        test_name = request.node.name
        request.instance.note += "\nTest script: {}.\n Executed on mobile: {}.\n Test Bed: {}.\n" \
            .format(test_name, sd.platform, sd.config.host_name)
        print(request.instance.note)
        print("Actual Status", request.instance.test_result)
        if request.instance.test_result:
            result = 'p'
            print("result:: {}".format(result))
        platform = ''
        '''
        try:
            platform = sd.test_cases_dict.get(sd.tc_list[0])['platforms'][0]
        except KeyError:
            print("Platform not specified in test plan. Updating test result without platform")
        sd.test_link.post_test_result(testcaseid=external_id, testplanid=sd.tp_id, status=result, notes= request.instance.note, overwrite=False, build_id=build_id, platformname=platform)
        '''
    request.addfinalizer(function_finalizer)


def testbed_controls(tp_name):
    ssh_handler = ShellHandler(conf.remote_appium_server_ip, conf.remote_appium_username, conf.remote_appium_pwd)
    sd.ssh_handler = ssh_handler
    phone_list = conf.multilink_phone_list
    mobile_config = conf.mobile_data_config
    slot_turn_on_cmd = "uhubctl -l {0} -p {1} -a 1"
    slot_turn_off_cmd = "uhubctl -l {0} -p {1} -a 0"
    usb_hub_list = "uhubctl -l {0} -p {1}"
    touch_cmd = "adb -s {} shell input tap 100 100"
    adb_remove_server = "adb -s {} uninstall io.appium.uiautomator2.server"
    adb_remove_server_test = "adb -s {} uninstall io.appium.uiautomator2.server.test"

    print(sd.platform)
    if "WBZ" in sd.platform:

        for hubs in conf.usb_hubs:
            hub_slot = 0
            while hub_slot <= 7:
                print(slot_turn_on_cmd.format(hubs,hub_slot))
                hub_slot += 1
                sh_in, sh_out, sh_error = ssh_handler.execute(slot_turn_on_cmd.format(hubs,hub_slot))
                if sh_error:
                    assert False, "Failed to turn on the USB hub slot. Command output: {}".format(sh_out)
    else:
        for hubs in conf.usb_hubs:
            hub_slot = 0
            while hub_slot <= 7:
                print(slot_turn_on_cmd.format(hubs,hub_slot))

                sh_in, sh_out, sh_error = ssh_handler.execute(slot_turn_on_cmd.format(hubs,hub_slot))
                if sh_error:
                    assert False, "Failed to turn on the USB hub slot. Command output: {}".format(sh_out)
                time.sleep(1)
                sh_in, sh_out, sh_error = ssh_handler.execute(slot_turn_off_cmd.format(hubs, hub_slot))
                if sh_error:
                    assert False, "Failed to turn off the USB hub slot. Command output: {}".format(sh_out)
                time.sleep(1)
                sh_in, sh_out, sh_error = ssh_handler.execute(slot_turn_on_cmd.format(hubs, hub_slot))
                if sh_error:
                    assert False, "Failed to turn on the USB hub slot. Command output: {}".format(sh_out)
                sh_in, sh_out, sh_error = ssh_handler.execute(usb_hub_list.format(hubs, hub_slot))
                if sh_error:
                    assert False, "Failed to turn on the USB hub slot. Command output: {}".format(sh_out)
                if (mobile_config.get(sd.platform).get('udid')) not in sh_out[1]:
                    sh_in, sh_out, sh_error = ssh_handler.execute(slot_turn_off_cmd.format(hubs, hub_slot))
                    if sh_error:
                        assert False, "Failed to turn off the USB hub slot. Command output: {}".format(sh_out)
                hub_slot += 1

    print("Rebooting all the connected phones of the testbed")
    for dut in phone_list:
        print("Rebooting the phones {}".format(dut))
        reboot_phone_cmd = "adb -s {} reboot".format(mobile_config.get(dut).get('udid'))
        sh_in, sh_out, sh_error = ssh_handler.execute(reboot_phone_cmd)
        if sh_error:
            print("Unable to reboot the phone : {}".format(dut))

    time.sleep(60)

    for dut in phone_list:
        sh_in, sh_out, sh_error = ssh_handler.execute(touch_cmd.format(mobile_config.get(dut).get('udid')))
        if sh_error:
            print("Unable to click the phone : {}".format(dut))
        sh_in, sh_out, sh_error = ssh_handler.execute(adb_remove_server.format(mobile_config.get(dut).get('udid')))
        if sh_error:
            print("Unable to uninstall the uiautomator2 on the phone : {}".format(dut))
        sh_in, sh_out, sh_error = ssh_handler.execute(adb_remove_server_test.format(mobile_config.get(dut).get('udid')))
        if sh_error:
            print("Unable to uninstall the uiautomator2 test on the phone : {}".format(dut))


def firmware_update(tp_name):
    listfiles = []
    status = False
    fw_folder = ' '
    print(tp_name)
    if "Chimera" in tp_name:
        for file_name in os.listdir(fwfolderpath_Chimera):
            if file_name.endswith('.hex'):
                listfiles.append(file_name)

            if "without_Pairing" in tp_name or "Full_IOP" in tp_name or "Without_Pairing" in tp_name:
                for each in listfiles:
                    if "common.unified" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Common Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Pairing" in tp_name or "With_Pairing" in tp_name or "pairing" in tp_name:
                for each in listfiles:
                    if "privacy.unified" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Privacy Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Extended_Adv" in tp_name or "Ext_Adv" in tp_name or "ExtAdv" in tp_name:
                for each in listfiles:
                    if "extadv.unified" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Extended Advertising Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Single_Peri_High" in tp_name:
                for each in listfiles:
                    if "single_peri_high.unified" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Stack Memory single link Peripheral High throughput Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Multi_Peri_High" in tp_name:
                for each in listfiles:
                    if "multi_peri_high.unified" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Stack Memory single link Peripheral High throughput Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "POSC" in tp_name:
                for each in listfiles:
                    if "posc" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Low Power Mode POSC Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "SOSC" in tp_name:
                for each in listfiles:
                    if "sosc" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Low Power Mode SOSC Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "pta" in tp_name.lower():
                for each in listfiles:
                    if "pta" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected PTA Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "multi_beacon" in tp_name.lower() or "multiple_beacon" in tp_name.lower():
                for each in listfiles:
                    if "multi_beacon" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Multi Beacon Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "peri_low" in tp_name.lower() or "peripheral_low" in tp_name.lower():
                for each in listfiles:
                    if "peri_low" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Low Throughput Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        if '.hex' in fw_folder:
            print(" ", end='\n')
            print("===================== The Firmware will be flashed to the DUT =====================", fw_folder)
            print(" ", end='\n')
            status = False
            FWImage = False
            for dut in conf.duts_to_be_flashed:
                if "Chimera" in tp_name:
                    if os.path.isfile(fwfolderpath_Chimera + fw_folder):
                        FWImage = True
                        if FWImage:
                            print("********************************************************")
                            print("*                 Flash firmware image                 *")
                            print("********************************************************")
                            print(" ", end='\n')
                            print("\nFirmware update is progress Please wait\n")
                            print(" ", end='\n')
                            print("========== Chimera DUT is getting flashed ==========")
                            print(" ", end='\n')
                            # process = subprocess.Popen('"C:/Program Files/Microchip/MPLABX/v6.20/mplab_platform/mplab_ipe/ipecmd.exe" -P32CX1012BZ25048 -M -OL -OAS0 -OK -TSRYN231900129 -F'+ fw_folder, cwd=fwfolderpath_Chimera, stdout=subprocess.PIPE, universal_newlines=True)
                            # process = subprocess.Popen('"C:/Program Files/Microchip/MPLABX/v6.05/mplab_platform/mplab_ipe/ipecmd.exe" -TSMTI000000543 -P32CX1012BZ25048 -OWD\"PIC32CX-BZ_DFP,1.0.107,Microchip\" -M -OL -F'+ fw, cwd=fwfolderpath_Chimera, stdout=subprocess.PIPE, universal_newlines=True)
                            flashpath = sd.config.mplab_path + ' -P32CX1012BZ25048 -M -OL -OAS0 -OK -TS' + \
                                        sd.config.dut_serial[dut]
                            process = subprocess.Popen(flashpath + ' -F' + fw_folder, cwd=fwfolderpath_Chimera,
                                                       stdout=subprocess.PIPE, universal_newlines=True)
                            output_list = process.stdout.readlines()
                            output = ' '.join(map(str, output_list))
                            print(output)
                            if "Program Succeeded" in output:
                                time.sleep(3)
                                print("********************************************************")
                                print(
                                    "*              [BLEAF Flasher Handler] : Firmware Flashing is successfull                 *")
                                print("********************************************************")
                                print(" ", end='\n')
                                status = True
                            else:
                                print("********************************************************")
                                print(
                                    "*              [BLEAF Flasher Handler] : Firmware flashing is Failed                 *")
                                print("********************************************************")
                                print(" ", end='\n')
                                status = False
                            process.kill()
                        else:
                            print(
                                "#####################################    [FW image] : file not exist    #####################################")
                            status = False

    elif "bigbuck" in tp_name.lower():
        if "64" in tp_name.lower():
            global fwfolderpath_Bigbuck
            fwfolderpath_Bigbuck = fwfolderpath_Bigbuck + '/64/'
            clock_freq = "64"
        elif "128" in tp_name.lower():
            fwfolderpath_Bigbuck = fwfolderpath_Bigbuck + '/128/'
            clock_freq = "128"

        for file_name in os.listdir(fwfolderpath_Bigbuck):
            if file_name.endswith('.hex'):
                listfiles.append(file_name)

            if "without_pairing" in tp_name.lower() or "full_iop" in tp_name.lower():
                for each in listfiles:
                    if "common.signed" in each and clock_freq in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Common Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Pairing" in tp_name or "With_Pairing" in tp_name or "pairing" in tp_name:
                for each in listfiles:
                    if "privacy.signed" in each and clock_freq in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Privacy Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Extended_Adv" in tp_name or "Ext_Adv" in tp_name or "ExtAdv" in tp_name or "EXT_ADV" in tp_name:
                for each in listfiles:
                    if "extadv" in each and clock_freq in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Extended Advertising Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Single_Peri_High" in tp_name:
                for each in listfiles:
                    if "single_peri_high" in each and clock_freq in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Stack Memory single link Peripheral High throughput Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Multi_Peri_High" in tp_name:
                for each in listfiles:
                    if "multi_peri_high" in each and clock_freq in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Stack Memory single link Peripheral High throughput Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "POSC" in tp_name:
                for each in listfiles:
                    if "posc" in each and clock_freq in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Low Power Mode POSC Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "SOSC" in tp_name:
                for each in listfiles:
                    if "sosc" in each and clock_freq in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Low Power Mode SOSC Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "pta" in tp_name.lower():
                for each in listfiles:
                    if "pta" in each and clock_freq in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected PTA Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "multi_beacon" in tp_name.lower() or "multiple_beacon" in tp_name.lower():
                for each in listfiles:
                    if "multi_beacon" in each and clock_freq in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Multi Beacon Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "peri_low" in tp_name.lower() or "peripheral_low" in tp_name.lower():
                for each in listfiles:
                    if "peri_low" in each and clock_freq in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Low Throughput Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        if '.hex' in fw_folder:
            print(" ", end='\n')
            print("===================== The Firmware will be flashed to the DUT =====================",
                  fw_folder)
            print(" ", end='\n')
            status = False
            FWImage = False
            for dut in conf.duts_to_be_flashed:

                if "bigbuck" in tp_name.lower():
                    if os.path.isfile(fwfolderpath_Bigbuck + fw_folder):
                        FWImage = True
                        if FWImage:
                            print("********************************************************")
                            print("*                 Flash firmware image                 *")
                            print("********************************************************")
                            print(" ", end='\n')
                            print("\nFirmware update is progress Please wait\n")
                            print(" ", end='\n')
                            print("========== BigBuck DUT is getting flashed ==========")
                            print(" ", end='\n')
                            # process = subprocess.Popen('"C:/Program Files/Microchip/MPLABX/v6.20/mplab_platform/mplab_ipe/ipecmd.exe" -P32CX1012BZ25048 -M -OL -OAS0 -OK -TSRYN231900129 -F'+ fw_folder, cwd=fwfolderpath_Chimera, stdout=subprocess.PIPE, universal_newlines=True)
                            # process = subprocess.Popen('"C:/Program Files/Microchip/MPLABX/v6.05/mplab_platform/mplab_ipe/ipecmd.exe" -TSMTI000000543 -P32CX1012BZ25048 -OWD\"PIC32CX-BZ_DFP,1.0.107,Microchip\" -M -OL -F'+ fw, cwd=fwfolderpath_Chimera, stdout=subprocess.PIPE, universal_newlines=True)
                            flashpath = sd.config.mplab_path + ' -P32WM_BZ6204 -M -OL -OAS0 -OK -TS' + \
                                        sd.config.dut_serial[dut]
                            process = subprocess.Popen(flashpath + ' -F' + fw_folder, cwd=fwfolderpath_Bigbuck,
                                                       stdout=subprocess.PIPE, universal_newlines=True)
                            output_list = process.stdout.readlines()
                            output = ' '.join(map(str, output_list))
                            print(output)
                            if "Program Succeeded" in output:
                                time.sleep(3)
                                print("********************************************************")
                                print(
                                    "*              [BLEAF Flasher Handler] : Firmware Flashing is successfull                 *")
                                print("********************************************************")
                                print(" ", end='\n')
                                status = True
                            else:
                                print("********************************************************")
                                print(
                                    "*              [BLEAF Flasher Handler] : Firmware flashing is Failed                 *")
                                print("********************************************************")
                                print(" ", end='\n')
                                status = False
                            process.kill()
                        else:
                            print(
                                "#####################################    [FW image] : file not exist    #####################################")
    elif "buckland" in tp_name.lower():
        for file_name in os.listdir(fwfolderpath_Buckland):
            if file_name.endswith('.hex'):
                listfiles.append(file_name)

            if "without_Pairing" in tp_name or "Full_IOP" in tp_name or "Without_Pairing" in tp_name:
                for each in listfiles:
                    if "common.unified" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Common Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Pairing" in tp_name or "With_Pairing" in tp_name or "pairing" in tp_name:
                for each in listfiles:
                    if "privacy.unified" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Privacy Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Extended_Adv" in tp_name or "Ext_Adv" in tp_name or "ExtAdv" in tp_name:
                for each in listfiles:
                    if "extadv.unified" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Extended Advertising Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Single_Peri_High" in tp_name:
                for each in listfiles:
                    if "single_peri_high.unified" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Stack Memory single link Peripheral High throughput Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "Multi_Peri_High" in tp_name:
                for each in listfiles:
                    if "multi_peri_high.unified" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Stack Memory single link Peripheral High throughput Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "POSC" in tp_name:
                for each in listfiles:
                    if "posc" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Low Power Mode POSC Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "SOSC" in tp_name:
                for each in listfiles:
                    if "sosc" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Low Power Mode SOSC Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "pta" in tp_name.lower():
                for each in listfiles:
                    if "pta" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected PTA Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "multi_beacon" in tp_name.lower() or "multiple_beacon" in tp_name.lower():
                for each in listfiles:
                    if "multi_beacon" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Multi Beacon Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            elif "peri_low" in tp_name.lower() or "peripheral_low" in tp_name.lower():
                for each in listfiles:
                    if "peri_low" in each:
                        fw_folder = each
                        print(
                            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Selected Low Throughput Test Image   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        if '.hex' in fw_folder:
            print(" ", end='\n')
            print("===================== The Firmware will be flashed to the DUT =====================",
                  fw_folder)
            print(" ", end='\n')
            status = False
            FWImage = False
            for dut in conf.duts_to_be_flashed:

                if "bigbuck" in tp_name.lower():
                    if os.path.isfile(fwfolderpath_Buckland + fw_folder):
                        FWImage = True
                        if FWImage:
                            print("********************************************************")
                            print("*                 Flash firmware image                 *")
                            print("********************************************************")
                            print(" ", end='\n')
                            print("\nFirmware update is progress Please wait\n")
                            print(" ", end='\n')
                            print("========== Chimera DUT is getting flashed ==========")
                            print(" ", end='\n')
                            # process = subprocess.Popen('"C:/Program Files/Microchip/MPLABX/v6.20/mplab_platform/mplab_ipe/ipecmd.exe" -P32CX1012BZ25048 -M -OL -OAS0 -OK -TSRYN231900129 -F'+ fw_folder, cwd=fwfolderpath_Chimera, stdout=subprocess.PIPE, universal_newlines=True)
                            # process = subprocess.Popen('"C:/Program Files/Microchip/MPLABX/v6.05/mplab_platform/mplab_ipe/ipecmd.exe" -TSMTI000000543 -P32CX1012BZ25048 -OWD\"PIC32CX-BZ_DFP,1.0.107,Microchip\" -M -OL -F'+ fw, cwd=fwfolderpath_Chimera, stdout=subprocess.PIPE, universal_newlines=True)
                            flashpath = sd.config.mplab_path + ' -P32CX5109BZ31048 -M -OL -OAS0 -OK -TS' + \
                                        sd.config.dut_serial[dut]
                            process = subprocess.Popen(flashpath + ' -F' + fw_folder, cwd=fwfolderpath_Buckland,
                                                       stdout=subprocess.PIPE, universal_newlines=True)
                            output_list = process.stdout.readlines()
                            output = ' '.join(map(str, output_list))
                            print(output)
                            if "Program Succeeded" in output:
                                time.sleep(3)
                                print("********************************************************")
                                print(
                                    "*              [BLEAF Flasher Handler] : Firmware Flashing is successfull                 *")
                                print("********************************************************")
                                print(" ", end='\n')
                                status = True
                            else:
                                print("********************************************************")
                                print(
                                    "*              [BLEAF Flasher Handler] : Firmware flashing is Failed                 *")
                                print("********************************************************")
                                print(" ", end='\n')
                                status = False
                            process.kill()
                        else:
                            print(
                                "#####################################    [FW image] : file not exist    #####################################")

        else:
            print(
                "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    No .hex required file is available and Firmware is Not flashed    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    else:
        print(" Please check Test Plan name in Testlink, keywords is not properly mentioned as defined ")

    if status == False:
        print("Unable to flash the FW on the DUT, Exiting the tests.")
        sys.exit(1)