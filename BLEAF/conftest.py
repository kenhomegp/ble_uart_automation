import pytest

from .CommonSupportLib.StationData import stationData
from .CommonSupportLib.ConfigReader import ConfigReader
from .CommonSupportLib.TestLinkAPI import TestLink

sd = stationData()
conf = ConfigReader()
sd.config = conf

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

def pytest_configure(config):
    config.addinivalue_line("markers",
                            "test_id(id): marker with test id corresponding to testlink test case")
    print("[conftest]pytest_configure. Skip the testPlan initial process")
    sd.test_link = None
    sd.tc_list = []
    sd.tc_values = []
    #sd.platform = 'SamsungA54'
    sd.platform = sd.config.mobile_to_use

    '''
    test_plan_name = config.get_option('tp_name')
    setup_test_link()
    sd.tp_id = sd.test_link.get_test_plan_id(test_plan_name)
    tc_dict = get_tests_to_execute(test_plan_name)
    sd.test_cases_dict = tc_dict
    sd.tc_list = list(sd.test_cases_dict.keys())
    sd.tc_values = list(sd.test_cases_dict.values())
    platform = ''
    try:
        platform = tc_dict.get(sd.tc_list[0])['platforms'][0]
    except KeyError:
        print("Platform not specified in test plan. Default platform will be used.")
    available_platforms = list(sd.config.mobile_data_config.keys()) + ['MEDC', 'RPI_4B']
    if platform:
        assert platform in available_platforms,  "The platform provided in test plan: " \
                                                "{} is not among available platforms: {}".format(platform, available_platforms)
        sd.platform = platform
    else:
        sd.platform = sd.config.mobile_to_use
    '''
def pytest_collection_modifyitems(session, config, items):
    selected_items = []
    if sd.platform == 'RPI_4B':
        for item in items:
            marker_list = item.iter_markers()   
            #print("Selected tests for execution 1")
            for mark in marker_list:
                if mark.name == "test_id":
                    test_id = mark.args[0]
                    if test_id in sd.tc_list and mark.args[1] == 'RPI_4B':
                        selected_items.append(item)
    else:
        for item in items:
            marker_list = item.iter_markers()
            #print("Selected tests for execution 2")
            for mark in marker_list:
                print(mark.name)
                selected_items.append(item)
                print("Selected tests for execution")
            '''
            for mark in marker_list:
                print(mark)
                if mark.name == "test_id":
                    test_id = mark.args[0]
                    if test_id in sd.tc_list and mark.args[1] != 'RPI_4B':
                        selected_items.append(item)
                        print("Selected tests for execution 3")
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

@pytest.fixture(scope="class")
def default_class_fixture(request):
    print("calling default class fixture")
    request.cls.test_string = "This is default class fixture"

@pytest.fixture(scope="function", autouse=True)
def default_function_fixture_main(request):
    print("calling default function fixture")
    request.cls.test_result = False
    request.cls.test_output = ""
    request.cls.note = ""
    def function_finalizer():
        test_marker = request.node.get_closest_marker('test_id')
        test_id = test_marker.args[0]
        print("test_id = {}".format(test_id))
        #external_id = sd.test_cases_dict.get(test_id)['id']
        #build_id = sd.test_cases_dict.get(test_id)['build']
        external_id = None
        build_id = None
        result = 'f'
        test_name = request.node.name
        #request.instance.note += "\nTest script: {}.\n Executed on mobile: {}.\n Test Bed: {}.\n Execution Type: {}.\n" \
        #    .format(test_name, sd.platform, sd.config.server_dut, "DBDT")
        #print(request.instance.note)
        request.instance.note += "\nTest script: {}.\n Executed on mobile: {}.\n Test Bed: {}.\n Execution Type: {}.\n" \
            .format(test_name, "", sd.config.server_dut, "DBDT")
        print(request.instance.note)
        print("Actual Status", request.instance.test_result)
        if request.instance.test_result:
            result = 'p'
            print("result:: {}".format(result))
        '''
        platform = ''
        try:
            platform = sd.test_cases_dict.get(sd.tc_list[0])['platforms'][0]
        except KeyError:
            print("Platform not specified in test plan. Updating test result without platform")
        sd.test_link.post_test_result(testcaseid=external_id, testplanid=sd.tp_id, status=result, notes= request.instance.note, overwrite=False, build_id=build_id, platformname=platform)
        '''
    request.addfinalizer(function_finalizer)