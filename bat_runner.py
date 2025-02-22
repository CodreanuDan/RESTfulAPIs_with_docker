import os
import subprocess

class BatRunner:
    ''' Initialises Docker container and loads env data'''
    def __init__(self):
        # self.bat_file = "RESTful/Tema_1_3ApiApelate/run_docker.bat"
        self.bat_file = r"C:\Users\uig37216\Desktop\SCOALA\RESTful\Tema_1_3ApiApelate\run_docker.bat"
    def bat_runner(self):
        ''' Runs bat file conatining Docker container init'''
        file = self.bat_file
        if not os.path.exists(file):
            message = f"[❌]  Bat file {file} not found!"
            print(message)
        else:
            try:
                subprocess.run([file], check= True)
            except Exception as e :
                message = f"[❌] Error at running {file}, err msg: {e}!"
                print(message)
