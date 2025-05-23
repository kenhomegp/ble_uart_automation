from singleton_decorator import singleton


@singleton
class stationData:
    def __init__(self):
        self.station_name = "SET_ME"
        print("Creating a constant station data variable: {}".format(self.station_name))
        print("creating Config reader object in station data")
        self.config = None
        self.dut_fit = None
        self.mobile_driver = None
        self.dut1 = None
        self.dut2 = None
        self.mobile_platform = None
        self.multilink_mobile_driver = []
        self.remote_mac_server = True
