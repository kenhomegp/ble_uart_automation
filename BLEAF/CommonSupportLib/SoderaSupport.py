import socket
import time
import subprocess
import csv
import os
from ..CommonSupportLib.StationData import stationData

sd = stationData()

class SoderaSupport:
    
    def __init__(self, host_ip, port='22901'):
        print("Setting Up Sodera Support Object")
        os.system("taskkill /F /IM FTSAutoServer.exe")
        self.sodera_server = subprocess.Popen(sd.config.sodera_server_path, shell=True)
        self.host_ip = host_ip
        self.port = port
    
    def kill_sodera_server(self):
        print("Closing sodera server")
        os.system("taskkill /F /IM FTSAutoServer.exe")
        self.sodera_server.kill()
    
    def Open_Capture(self, capture_file):
        sodera_socket = socket.socket()
        sodera_socket.connect((self.host_ip, self.port))
        while True:
            print('[BLEAF]:Please wait, it may take few seconds')
            cmd = "Open Capture File;" + str(capture_file) + "\r\n"
            c = cmd.encode()
            sodera_socket.send(c)
            # time.sleep(30)
            Receive = sodera_socket.recv(1024)
            # print(Receive)
            if b"OPEN CAPTURE FILE;SUCCEEDED" in Receive:
                # print('[BLEAF]:[Debug Message Received] :', Receive)
                print('[BLEAF]:[Open Capture Command Success]')
                sodera_socket.close()
                return True
            else:
                print('[BLEAF]:Open Capture Failed')
                sodera_socket.close()
                self.Close_Sodera()
                return False
    
    def Export_Logs(self, csv_file):
        sodera_socket = socket.socket()
        sodera_socket.connect((self.host_ip, self.port))
        while True:
            cmd = "Export;File=" + str(csv_file) + "\r\n"
            # print(cmd)
            c = cmd.encode()
            sodera_socket.send(c)
            # time.sleep(5)
            Receive = sodera_socket.recv(1024)
            if b"SUCCEEDED" in Receive:
                # print('[BLEAF]:[Debug Message Received] :', Receive)
                print('[BLEAF]:[Export Capture Command Success]')
                # print('Please wait, it may take few seconds')
                sodera_socket.close()
                return True
            else:
                print('[BLEAF]:Export Capture Failed')
                sodera_socket.close()
                self.Close_Sodera()
                exit()
                return False
    
    def Open_Sodera(self, fts_path):
        sodera_socket = socket.socket()
        sodera_socket.connect((self.host_ip, self.port))
        while True:
            cmd = "Start FTS;" + str(fts_path) + "\r\n"
            # print(cmd)
            c = cmd.encode()
            sodera_socket.send(c)
            time.sleep(5)
            Receive = sodera_socket.recv(1024)
            for c in range(10):
                if b"START FTS;SUCCEEDED" in Receive:
                    print('[BLEAF]:[Debug Message Received] :', Receive)
                    print('[BLEAF]:[FTS Start Command Success]')
                    print('Please wait, it may take few seconds')
                    sodera_socket.close()
                    return True
                if b"START FTS;FAILED" in Receive:
                    print('[BLEAF]:FTS Failed to Start')
                    sodera_socket.close()
                    self.Close_Sodera()
                    exit()
                    return False
                c += 1
                print('[BLEAF]:[Debug Message Received] :', Receive)
                Receive = sodera_socket.recv(1024)
            print('[BLEAF]:FTS Failed to Start')
            sodera_socket.close()
            self.Close_Sodera()
            exit()
            return False
    
    def Set_BT_Add(self, BT_Add, DUT_Add):
        sodera_socket = socket.socket()
        sodera_socket.connect((self.host_ip, self.port))
        while True:
            cmd = "CONFIG SETTINGS;IOParameters;Sodera;Master=0x" + BT_Add + "\r\n;Slave=0x" + DUT_Add+""
            print("$$$$$$$$$$$$$$$$",cmd)
            c = cmd.encode()
            sodera_socket.send(c)
            time.sleep(5)
            Receive = sodera_socket.recv(1024)
            for c in range(5):
                if b"CONFIG SETTINGS;SUCCEEDED" in Receive:
                    print('[BLEAF]:[Debug Message Received] :', Receive)
                    print('[BLEAF]:[BT Address of phone is configured to Sodera]')
                    # print('Please wait, it may take few seconds')
                    sodera_socket.close()
                    return True
                if b"CONFIG SETTINGS;FAILED" in Receive:
                    print('[BLEAF]:Failed to Configure BT Address')
                    sodera_socket.close()
                    self.Close_Sodera()
                    exit()
                    return False
                c += 1
                Receive = sodera_socket.recv(1024)
            print('[BLEAF]:Failed to Configure BT Address')
            sodera_socket.close()
            self.Close_Sodera()
            exit()
            return False
    
    def Start_Record(self):
        sodera_socket = socket.socket()
        sodera_socket.connect((self.host_ip, self.port))
        while True:
            cmd = "Start Record" + "\r\n"
            # print(cmd)
            c = cmd.encode()
            sodera_socket.send(c)
            time.sleep(5)
            Receive = sodera_socket.recv(1024)
            for c in range(5):
                if b"START RECORD;SUCCEEDED" in Receive:
                    print('[BLEAF]:[Debug Message Received] :', Receive)
                    print('[BLEAF]:[Start Record Successful]')
                    # print('Please wait, it may take few seconds')
                    sodera_socket.close()
                    return True
                if b"START RECORD;FAILED" in Receive:
                    print('[BLEAF]:Failed to Start Record')
                    sodera_socket.close()
                    self.Close_Sodera()
                    exit()
                    return False
                c += 1
                Receive = sodera_socket.recv(1024)
            print('[BLEAF]:Failed to Start Record')
            sodera_socket.close()
            self.Close_Sodera()
            exit()
            return False
    
    def Start_Analyze(self):
        sodera_socket = socket.socket()
        sodera_socket.connect((self.host_ip, self.port))
        while True:
            cmd = "Start Analyze" + "\r\n"
            # print(cmd)
            c = cmd.encode()
            sodera_socket.send(c)
            time.sleep(5)
            Receive = sodera_socket.recv(1024)
            for c in range(5):
                if b"START ANALYZE;SUCCEEDED" in Receive:
                    print('[BLEAF]:[Debug Message Received] :', Receive)
                    print('[BLEAF]:[Start Analyze is successful]')
                    # print('Please wait, it may take few seconds')
                    sodera_socket.close()
                    return True
                if b"START ANALYZE;FAILED" in Receive:
                    print('[BLEAF]:Failed to Start Analyze')
                    sodera_socket.close()
                    self.Close_Sodera()
                    exit()
                    return False
                c += 1
                Receive = sodera_socket.recv(1024)
            print('[BLEAF]:Failed to Start Analyze')
            sodera_socket.close()
            self.Close_Sodera()
            exit()
            return False
    
    def Stop_Analyze(self):
        sodera_socket = socket.socket()
        sodera_socket.connect((self.host_ip, self.port))
        while True:
            cmd = "Stop Analyze" + "\r\n"
            # print(cmd)
            c = cmd.encode()
            sodera_socket.send(c)
            time.sleep(5)
            Receive = sodera_socket.recv(1024)
            for c in range(5):
                if b"STOP ANALYZE;SUCCEEDED" in Receive:
                    print('[BLEAF]:[Debug Message Received] :', Receive)
                    print('[BLEAF]:[Stop Analyze is successful]')
                    # print('Please wait, it may take few seconds')
                    sodera_socket.close()
                    return True
                if b"STOP ANALYZE;FAILED" in Receive:
                    print('[BLEAF]:Failed to Stop ANALYZE')
                    sodera_socket.close()
                    self.Close_Sodera()
                    exit()
                    return False
                c += 1
                Receive = sodera_socket.recv(1024)
            print('[BLEAF]:Failed to Stop Analyze')
            sodera_socket.close()
            self.Close_Sodera()
            exit()
            return False
    
    def Stop_Record(self):
        sodera_socket = socket.socket()
        sodera_socket.connect((self.host_ip, self.port))
        while True:
            cmd = "Stop Record" + "\r\n"
            # print(cmd)
            c = cmd.encode()
            sodera_socket.send(c)
            time.sleep(5)
            Receive = sodera_socket.recv(1024)
            for c in range(5):
                if b"STOP RECORD;SUCCEEDED" in Receive:
                    print('[BLEAF]:[Debug Message Received] :', Receive)
                    print('[BLEAF]:[Stop RECORD is successful]')
                    # print('Please wait, it may take few seconds')
                    sodera_socket.close()
                    return True
                if b"STOP RECORD;FAILED" in Receive:
                    print('[BLEAF]:Failed to Stop Record')
                    sodera_socket.close()
                    self.Close_Sodera()
                    exit()
                    return False
                c += 1
                Receive = sodera_socket.recv(1024)
            print('[BLEAF]:Failed to Stop Record')
            sodera_socket.close()
            self.Close_Sodera()
            exit()
            return False
    
    def Save_Capture(self, CFA_Name):
        print("Save_Capture")
        sodera_socket = socket.socket()
        sodera_socket.connect((self.host_ip, self.port))
        while True:
            cmd = "Save Capture;F:\Repo_Copy_1\Repo_Copy\BLEAF_Template_Chimera\BLEAF\Airlog\\" + CFA_Name + ".cfa\r\n"
            # print(cmd)
            c = cmd.encode()
            sodera_socket.send(c)
            time.sleep(5)
            Receive = sodera_socket.recv(1024)
            for c in range(5):
                if b"SAVE CAPTURE;SUCCEEDED" in Receive:
                    print('[BLEAF]:[Debug Message Received] :', Receive)
                    print('[BLEAF]:[Save Capture is successful]')
                    # print('Please wait, it may take few seconds')
                    sodera_socket.close()
                    return True
                if b"SAVE CAPTURE;FAILED" in Receive:
                    print('[BLEAF]:Failed to Save Capture')
                    sodera_socket.close()
                    self.Close_Sodera()
                    exit()
                    return False
                c += 1
                Receive = sodera_socket.recv(1024)
            print('[BLEAF]:Failed to Save Capture')
            sodera_socket.close()
            self.Close_Sodera()
            exit()
            return False

    def Close_Sodera(self):
        sodera_socket = socket.socket()
        sodera_socket.connect((self.host_ip, self.port))
        while True:
            sodera_socket.send(b"Stop FTS\r\n")
            # time.sleep(5)
            # receive data from the server
            Receive = sodera_socket.recv(1024)
            print('[BLEAF]:[Debug Message Received] :', Receive)
            for c in range(5):
                if b"STOP FTS;SUCCEEDED" in Receive:
                    print('[BLEAF]:[Debug Message Received] :', Receive)
                    print('[BLEAF]:[FTS Closed successfully]')
                    # print('Please wait, it may take few seconds')
                    sodera_socket.close()
                    return True
                if b"STOP FTS;FAILED" in Receive:
                    print('[BLEAF]:Failed to properly close FTS')
                    sodera_socket.close()
                    exit()
                    return False
                c += 1
                Receive =  sodera_socket.recv(1024)
            print('[BLEAF]:Failed to Stop FTS')
            sodera_socket.close()
            exit()
            return False

# Host_IpAddress = '192.168.43.83'
# Port = 22901
# cfa_path = "D:\A\Automation\Humming Bird\Log Analysis\\"
# Blood_Pressure_UUID_String = 'Blood Pressure Monitor'
# Heart_Rate_UUID_String = 'Heart Rate Monitor'
# Weight_Scale_UUID_String = 'Weight Scale'
# Health_Thermometer_UUID_String = 'Health Thermometer'
# Pulse_Oximeter_UUID_String = 'Pulse Oximiter'
# Glucose_UUID_String = 'Glucose'
# Error = {'NaN':'0x07FF', 'NRes':'0x0800', '+ INFINITY':'0x07FE', '– INFINITY':'0x0802'}
# fts_path = "C:\Program Files (x86)\Teledyne LeCroy Wireless\Wireless Protocol Suite 1.30\Executables\Core;Sodera"
# server_path = "C:\Program Files (x86)\Teledyne LeCroy Wireless\Wireless Protocol Suite 1.30\Executables\Core\FTSAutoServer.exe"
# BT_Add = 'f0d7aae0e60d'
# test_id = "FIT_APP_001"
#
# sodera = SoderaSupport(Host_IpAddress, Port)
# sodera.Open_Sodera(fts_path)
# sodera.Set_BT_Add(BT_Add)
# sodera.Start_Record()
# sodera.Start_Analyze()
# sodera.Stop_Analyze()
# sodera.Stop_Record()
# sodera.Save_Capture(test_id)

