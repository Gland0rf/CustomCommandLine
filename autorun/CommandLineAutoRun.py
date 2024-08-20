import os
import time
import subprocess
import configparser

log_file = open(r"C:\\Code Files\\Python\\CustomCommandLine\\autorun\\log.txt", "a")

def main():
    RED = '\033[91m'
    GREEN = '\033[92m'
    toCheck = True
    
    while(True):
        result = subprocess.run(
            ['wmic', 'logicaldisk', 'where', 'drivetype=2', 'get', 'description,deviceid,volumename'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        usb_info = result.stdout
        if toCheck:
            #print(usb_info)
            if "USB" in usb_info:
                log_file.write("USB Detected...\n")
                log_file.flush()
                #print(GREEN + "USB Connected")
                toCheck = False
                
                autorun_path = 'autorun.inf'
                
                #print(f"Running: {program_path}")
                log_file.write("Attempting to run the CLI...\n")
                log_file.flush()
                
                try:
                    subprocess.Popen("startCLI.exe")
                except Exception as e:
                    log_file.write(f"Error during program call: {e}\n")
                    log_file.flush()
                
                log_file.write("Program call complete.\n")
                log_file.flush()

            #else:
                #print(RED + "No USB stick is connected.")
        else:
            if not "USB" in usb_info:
                #print(RED + "No USB stick is connected.")
                toCheck = True
        
        time.sleep(1)
        
if __name__ == '__main__':
    log_file.write("Autorun active.\n")
    log_file.flush()
    main()