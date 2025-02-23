import tomllib
import os

class SettingsManager:
    """ Class containing setting manager function """

    def __init__(self):
        self.file_location = os.path.join(os.path.dirname(__file__), "settings.toml")
        self.config = self.load_config(config_file = self.file_location)[1]

    def load_config(self,config_file):
        """ Loads configuration from settings.toml file """
        rc = [0,1] # 0_ok 1_notOk
        with open(config_file, "rb") as cfg_file:
            data = tomllib.load(cfg_file)

        if data == None:
            print(f"[❌][DEBUG][settings_manager.py] --> Could not retrive data from {config_file}, rc: {rc[0]}")
            return (rc[0], None)
        else:
            print(f"[✅][DEBUG][DEBUG][settings_manager.py] --> Loaded data from {config_file}, rc: {rc[1]}")
            return (rc[1], data)
        

