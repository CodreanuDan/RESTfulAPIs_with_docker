from dataclasses import dataclass
from datetime import datetime

from settings_manager import SettingsManager

@dataclass
class DataContainer(SettingsManager):
    """ Class to store common data of the project"""
    location: str
    date: datetime
    temperature: float = 0.0

    def __post_init__(self):
        super().__init__()

        self.OK = 1
        self.NOT_OK = 0
        
        self.rc = {
            "OK": 200,
            "Resource_Moved_To_Another_Location": 301,
            "NotFound": 404,
            "ServerError": 500
        }

        self.WEATHER_API = (
            self.config["api"]["weather"]["primary"],
            self.config["api"]["weather"]["secondary"],
            )
        
        self.TOURISM_API = (
            self.config["api"]["tourism"]["primary"],
            self.config["api"]["tourism"]["secondary"],
            )
        
        self.RESTAURANT_API = (
            self.config["api"]["restaurant"]["primary"],
            self.config["api"]["restaurant"]["secondary"],
            )
