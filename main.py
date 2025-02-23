import requests
import os
import json
import time
from tenacity import retry, stop_after_attempt

from common_data import DataContainer
from datetime import datetime
from bat_runner import BatRunner

class Program(DataContainer, BatRunner):
    """ Main instance of the project """
    
    def __init__(self):
        super().__init__(location= " ", date= datetime.now)
        self.settings_path = os.path.abspath("settings.toml")
        self.weather_api_url_primary = self.WEATHER_API[0]
        self.weather_api_url_secondary = self.WEATHER_API[1]
        self.api_rc = self.rc
        self.bat_runner_instance = BatRunner()
        
    def __setup(self) -> bool:
        """
        Run the setup: 
            - check settings file;
            - run bat file to init docker container: check image, build if nedded;
            - get api keys
        """
        __verdict_1 = os.path.exists(self.settings_path)
        print(f"[⚠️][DEBUG][main.py] --> Check settings.toml: {self.settings_path}, Exists? {__verdict_1}")
        #================================================================================
        print(f"[⚠️][DEBUG][main.py] --> Run .bat file ...")
        __verdict_2 = False
        try:
            self.bat_runner_instance.bat_runner(file=self.bat_runner_instance.bat_file)
            __verdict_2 = True
        except Exception as e:
            print(f"[❌][ERROR][main.py] --> Error durring .bat setup: {e}")
        #================================================================================
        print(f"[⚠️][DEBUG][main.py] --> Get API keys ...")
        self.WEATHER_API_KEY_1 = os.getenv("WEATHER_API_KEY_1")
        self.WEATHER_API_KEY_2 = os.getenv("WEATHER_API_KEY_2")
        print(f"[⚠️][DEBUG][main.py] --> WEATHER_API_KEY_1 {self.WEATHER_API_KEY_1}, {type(self.WEATHER_API_KEY_1)}")
        print(f"[⚠️][DEBUG][main.py] --> WEATHER_API_KEY_2 {self.WEATHER_API_KEY_2}, {type(self.WEATHER_API_KEY_2)}")
        __verdict_3 = False
        if self.WEATHER_API_KEY_1 and self.WEATHER_API_KEY_2:
            __verdict_3 = True 
        
        if __verdict_1 and __verdict_2 and __verdict_3:
            return 1
        return 0
 
    @retry(stop=stop_after_attempt(3))
    def __fetch_weather_data(self, location:str, url:str, key:str, api:str) -> dict:
        """ Fetch  data from weather APIs """
        #================================================================================
        apis = ["OpenWeatherMap", "WeatherAPI"]
        #================================================================================
        __request_params = {
        "q": location,
        "units": "metric"
        }
        if api == apis[0]:  
            __request_params["appid"] = key
        elif api == apis[1]:  
            __request_params["key"] = key
        #================================================================================
        __api_response = requests.get(url, params=__request_params)
        if __api_response.status_code == self.api_rc["OK"]:
            data = __api_response.json()
            print(f"[✅][DEBUG][main.py][🌤️] --> Weather Data (from {api}):", data)
            return data
        else:
            print(f"[❌][DEBUG][main.py][🌤️] --> Error {__api_response.status_code}: {__api_response.text} ")
            return None
                       
    def __get_location(self):
        pass
    
    def __manipulate_data(self, weather_data: dict):
        """Extract relevant weather information and save it to a JSON file."""
        
        self.json_inputs_file = os.path.join(os.path.dirname(__file__), "inputs.json")

        if not weather_data or "main" not in weather_data or "wind" not in weather_data or "weather" not in weather_data:
            print("[❌][DEBUG][main.py] --> Missing essential weather data in API response.")
            return

        temperature = weather_data.get("main", {}).get("temp")
        wind_speed = weather_data.get("wind", {}).get("speed")
        feels_like = weather_data.get("main", {}).get("feels_like")
        
        temperature = temperature if isinstance(temperature, (int, float)) else None
        wind_speed = wind_speed if isinstance(wind_speed, (int, float)) else None
        feels_like = feels_like if isinstance(feels_like, (int, float)) else None

        # is_sunny = any("sun" in weather.get("main", "").lower() for weather in weather_data.get("weather", []))

        data_to_save = {
            "temperature": temperature,
            "wind_speed": wind_speed,
            "feels_like": feels_like,
            # "is_sunny": is_sunny
        }

        print(f"[DEBUG][⚠️][main.py] --> Temperature: {temperature}, Wind Speed: {wind_speed}, Feels Like: {feels_like}, ") #Is Sunny: {is_sunny}")

        try:
            with open(self.json_inputs_file, 'w') as file:
                json.dump(data_to_save, file, indent=4)
                print(f"[✅][DEBUG][main.py] --> Data saved in {self.json_inputs_file}")
        except Exception as e:
            print(f"[❌][DEBUG][main.py] --> Error writing to file: {e}")
            
        try:
            with open(self.json_inputs_file, 'r') as file:
                saved_data = json.load(file)
            print(f"[✅][INFO][main.py] --> JSON file content:\n{json.dumps(saved_data, indent=4)}")
        except Exception as e:
            print(f"[❌][DEBUG][main.py] --> Error reading JSON file: {e}")
             
    def main_function(self):
        """ Main function """
        self.__setup_status = self.__setup()
        __can_run = False
        if self.__setup_status == self.OK:
            print(f"[✅][DEBUG][main.py] --> Setup status: {self.__setup_status}")
            __can_run = True
        elif self.__setup_status == self.NOT_OK:
            print(f"[❌][DEBUG][main.py] --> Setup status: {self.__setup_status}")
            exit(1)
            
        if __can_run:
            location = input("Choose your destination: ")
            time.sleep(0.5)
            weather_data_primary = self.__fetch_weather_data(location=location,
                                                             url= self.weather_api_url_primary,
                                                             key= self.WEATHER_API_KEY_1,
                                                             api= "OpenWeatherMap")
            if weather_data_primary:
                self.__manipulate_data(weather_data= weather_data_primary)
            elif not weather_data_primary:
                weather_data_secondary = self.__fetch_weather_data(location=location,
                                                                   url= self.weather_api_url_secondary,
                                                                   key = self.WEATHER_API_KEY_2,
                                                                   api= "WeatherAPI")
                self.__manipulate_data(weather_data= weather_data_secondary)
                
        
if __name__ == "__main__":
    p = Program()
    p.main_function()


