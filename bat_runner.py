import os
import subprocess

class BatRunner:
    """ Initialises Docker container and loads env data"""
    def __init__(self):
        self.bat_file = os.path.join(os.path.dirname(__file__), "run_docker.bat")
    def bat_runner(self, file):
        """ Runs bat file conatining Docker container init """
        try:
            subprocess.run([file], check= True)
            # subprocess.run(["cmd.exe", "/c", file])
        except Exception as e :
            message = f"[❌][DEBUG][bat_runner.py] --> Error at running {file}, err msg: {e}!"
            print(message)
