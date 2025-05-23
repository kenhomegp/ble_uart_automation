import pytest
from ...CommonSupportLib.StationData import stationData
from ...CommonSupportLib.FW_upgrade import FirmwareUpdate

sd = stationData()

@pytest.fixture(scope="class", autouse=True)
def define_class_attributes(request):
    print("this is local specific class fixture")
    request.cls.firm = FirmwareUpdate()
    def class_finalizer():
        print("Local Class finalizer")
    request.addfinalizer(class_finalizer)

class TestRNBDPDSReliability:
    @pytest.mark.skip("RNBD_PDS_RELIABILITY_TEST_SN_COMMAND", 'MBDA')
    def test_rnbd_pds_reliability_for_sn_command(self):
        error_msg = ""
        test_status = True
        print("{0}Test to verify RNBD PDS Reliability of SN Command for 10000 iteration {0}".format('=' * 20))
        i = 1
        for i in range(i, 5001):
            print("Stress Test for Iteration", i)
            iter_msg = "Stress Test for Iteration {}\n".format(i)
            self.note += iter_msg
            step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_PDS_Reliability_Test_SN_Command')
            for step_des in step_descript:
                self.note += "Command mode results \n" + str(step_des) + "\n"
                if False in step_result:
                    test_status = False
                    error_msg = "Few of the commands have failed. Please refer step description for more details\n"
        self.note += error_msg
        assert test_status, error_msg
        self.test_result = True

    @pytest.mark.skip("RNBD_PDS_RELIABILITY_TEST_SA_COMMAND", 'MBDA')
    def test_rnbd_pds_reliability_for_sa_command(self):
        error_msg = ""
        test_status = True
        print("{0}Test to verify RNBD PDS Reliability of SA Command for 10000 iteration {0}".format('=' * 20))
        i = 1
        for i in range(i, 5001):
            print("Stress Test for Iteration", i)
            iter_msg = "Stress Test for Iteration {}\n".format(i)
            self.note += iter_msg
            step_result, step_descript = self.rnbdvsphonefeature.Read_json_file('RNBD_PDS_Reliability_Test_SA_Command')
            for step_des in step_descript:
                self.note += "Command mode results \n" + str(step_des) + "\n"
                if False in step_result:
                    test_status = False
                    error_msg = "Few of the commands have failed. Please refer step description for more details\n"
        self.note += error_msg
        assert test_status, error_msg
        self.test_result = True