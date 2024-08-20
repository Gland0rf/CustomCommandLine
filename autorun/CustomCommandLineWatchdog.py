import win32serviceutil
import win32service
import win32event
import time
import subprocess
import os

executable_path = r"C:\\Code Files\\Python\\CustomCommandLine\\autorun\\CommandLineAutoRun.exe"
executable_name = "CommandLineAutoRun.exe"

os.chdir(r"C:\\Code Files\\Python\\CustomCommandLine\\autorun")

log_file = open(r"C:\\Code Files\\Python\\CustomCommandLine\\autorun\\log.txt", "a")

class CommandLineWatchdogService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CommandLineWatchdogService"
    _svc_display_name_ = "Custom Command line Watchdog Service"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        log_file.write("Program up and running.\n")
        log_file.flush()
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.is_running = False
        log_file.write("Program stopped.\n")
        log_file.flush()
        
    def SvcDoRun(self):
        while self.is_running:
            if not is_running("CommandLineAutoRun.exe"):
                log_file.write("Program not running, starting it again.\n")
                log_file.flush()
                print("Program not running, starting it again.")
                start_program()
            time.sleep(5)

def is_running(executable_name):
    try:
        output = subprocess.check_output(f"tasklist /FI \"IMAGENAME eq {executable_name}\"", shell=True)
        return executable_name in str(output)
    except subprocess.CalledProcessError:
        return False
    
def start_program():
    log_file.write("Attempting to start the program...\n")
    log_file.flush()
    subprocess.Popen(executable_path)
        
if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(CommandLineWatchdogService)