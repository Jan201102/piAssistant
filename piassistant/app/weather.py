from geopy.geocoders import Nominatim
import requests_cache
from retry_requests import retry
import openmeteo_requests
import logging

class App:
    def __init__(self, **kwargs):
        self.dest = kwargs["location"]
        self.url = "https://api.open-meteo.com/v1/forecast"

        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        self.openmeteo = openmeteo_requests.Client(session = retry_session)

        geolocator = Nominatim(user_agent="weather")
        location = geolocator.geocode(self.dest)

        self.params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "temperature_2m_mean", "wind_speed_10m_mean"],
            "current": ["temperature_2m", "precipitation", "wind_speed_10m", "weather_code"]
        }

    def request(self, range, when = 0, type = ""):
        range = range.strip()
        #required fields temp min max,current,rain,wind_speed
        response = self.openmeteo.weather_api(self.url, params=self.params)[0]
        answer = ""
        if range == "current":
            logging.debug("requesting current weather")
            current =  response.Current()
            weather_description = self.wmo_code_to_german_description(current.Variables(3).Value())
            temp = round(current.Variables(0).Value())
            rain = round(current.Variables(1).Value())
            wind_speed = round(current.Variables(2).Value())
            if type == "temp":
                answer = "es ist {temp} grad".format(temp=temp)
            elif type == "rain":
                if rain == 0:
                    answer = "es wird keinen Niederschlag geben"
                else:
                    answer = "es wird {rain} milimeter Niederschlag geben".format(rain=rain)
            elif type == "wind":
                answer = "die Windgeschwindigkeit beträgt {wind} meter pro sekunde".format(wind=wind_speed)
            else:
                answer = "es ist {desc} bei einer Temperatur von {temp} grad, {rain} milimeter Niederschlag" \
                            " und einer Windgeschwindigkeit von {wind} meter pro sekunde".format(
                    temp=temp, rain=rain, wind=wind_speed, desc=weather_description)
        else:
            forecast = response.Daily()
            weather_description = self.wmo_code_to_german_description(forecast.Variables(0).Values(when))
            temp_max = round(forecast.Variables(1).Values(when))
            temp_min = round(forecast.Variables(2).Values(when))
            rain = round(forecast.Variables(3).Values(when))
            temp_mean = round(forecast.Variables(4).Values(when))
            wind_speed = round(forecast.Variables(5).Values(when))
            if type == "temp":
                answer = "es wird zwischen {temp_min} und {temp_max} grad warm".format(temp_min=temp_min, temp_max=temp_max)
            elif type == "rain":
                if rain == 0:
                    answer = "es wird keinen Niederschlag geben"
                else:
                    answer = "es wird {rain} milimeter Niederschlag geben".format(rain=rain)
            elif type == "wind":
                answer = "die durchschnittliche Windgeschwindigkeit beträgt {wind} meter pro sekunde".format(wind=wind_speed)
            else:
                answer = "es wird {desc} bei einer Temperatur zwischen {temp_min} und {temp_max} grad, {rain} milimeter Niederschlag" \
                         " und einer durchschnittlichen Windgeschwindigkeit von {wind} meter pro sekunde".format(
                    temp_min=temp_min, temp_max=temp_max, rain=rain, wind=wind_speed,desc=weather_description)

        return answer
    
    def wmo_code_to_german_description(self,code):
        """
        Converts a WMO weather code to its German description.
        Args:
            code (int): The WMO weather code.
        Returns:
            str: The German description of the weather condition.
        """
        wmo_descriptions = {
            0: "Klarer Himmel",
            1: "Meist klar",
            2: "Teilweise bewölkt",
            3: "Bewölkt",
            45: "Nebel",
            48: "Gefrierender Nebel",
            51: "Leichter Nieselregen",
            53: "Mäßiger Nieselregen",
            55: "Starker Nieselregen",
            56: "Leichter gefrierender Nieselregen",
            57: "Starker gefrierender Nieselregen",
            61: "Leichter Regen",
            63: "Mäßiger Regen",
            65: "Starker Regen",
            66: "Leichter gefrierender Regen",
            67: "Starker gefrierender Regen",
            71: "Leichter Schneefall",
            73: "Mäßiger Schneefall",
            75: "Starker Schneefall",
            77: "Schneekörner",
            80: "Leichte Regenschauer",
            81: "Mäßige Regenschauer",
            82: "Starke Regenschauer",
            85: "Leichte Schneeschauer",
            86: "Starke Schneeschauer",
            95: "Gewitter",
            96: "Gewitter mit leichtem Hagel",
            99: "Gewitter mit starkem Hagel"
        }

        return wmo_descriptions.get(code, "Unbekannte Wetterbedingung")
