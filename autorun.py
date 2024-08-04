import os
import time
import subprocess
import psutil

RED = '\033[91m'
GREEN = '\033[92m'
toCheck = True

while(True):
    usb_info = os.popen("wmic logicaldisk where drivetype=2 get description,deviceid,volumename").read()

    if toCheck:
        if "USB" in usb_info:
            print(GREEN + "USB Connected")
            toCheck = False

            time.sleep(3)

            #Run file
            script_name = "AUTO\\autorun.exe"
            available_drives = [drive.device[:2] for drive in psutil.disk_partitions()]
            script_path = None
            for drive in available_drives:
                possible_path = os.path.join(drive + "\\", script_name)
                print(possible_path)
                
                if os.path.exists(possible_path):
                    script_path = possible_path
                    break

            if script_path:
                try:
                    print("Running file")
                    subprocess.run(script_path)
                    print("Action completed successfully.")
                except Exception as e:
                    print(f"Error: {e}")

        else:
            print(RED + "No USB stick is connected.")
    else:
        if not "USB" in usb_info:
            print(RED + "No USB stick is connected.")
            toCheck = True
    
    time.sleep(1)