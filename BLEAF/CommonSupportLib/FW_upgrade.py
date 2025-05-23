#Flasher Script for Chimera

import os
import subprocess
import time

from ..CommonSupportLib.StationData import stationData

sd = stationData()

class FirmwareUpdate:
    def firmware_update(self):
        fw = sd.fw_folder
        fwfolderpath = sd.config.fwfolderpath
        status = False
        FWImage = False

        if os.path.isfile(fwfolderpath + fw):
            print('[FW image] : file exist')
            FWImage = True
            if FWImage :
                print("********************************************************")
                print("*                 Flash firmware image                 *")
                print("********************************************************")
                print("Flashing ",fw)
                print("\nFirmware update is progress Please wait\n")
                process = subprocess.Popen('"C:/Program Files/Microchip/MPLABX/v5.50/mplab_platform/mplab_ipe/ipecmd.exe" -P32CX1012BZ25048 -M -OL -OAS0 -TSMTI000000477 -F'+ fw, cwd=fwfolderpath, stdout=subprocess.PIPE, universal_newlines=True)
                output_list = process.stdout.readlines()
                output = ' '.join(map(str,output_list))
                print(output)
                if "Program Succeeded" in output:
                    time.sleep(3)
                    print("[BLEAF Flasher Handler] : Firmware update successfull")
                    status = True
                else:
                    print("[BLEAF Flasher Handler] : Fail to update Firmware")
                    status = False
        else:
            print("[FW image] : file not exist")
            status = False
        return status