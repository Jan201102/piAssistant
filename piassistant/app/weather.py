import requests
import logging

class App:
    def __init__(self, **kwargs):
        self.apiKey = kwargs["apiKey"]
        self.dest = kwargs["location"]
        call = "http://api.openweathermap.org/data/2.5/weather?q={loc}&lang=de&appid={id}".format(loc=self.dest,
                                                                                                  id=self.apiKey)
        cache = requests.get(call)
        cache = cache.json()
        self.lon = cache["coord"]["lon"]
        self.lat = cache["coord"]["lat"]

    def request(self, range, when = 0, type = ""):
        range = range.strip()
        type = type.strip()
        call = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&lang=de&appid={id}&units=metric".format(
            lat=self.lat, lon=self.lon, id=self.apiKey)
        cache = requests.get(call)
        cache = cache.json()
        logging.debug("retrieved weather information from Server")

        if range == "current":
            data = cache[range]
        else:
            data = cache[range][when]

        if "rain" in data.keys():
            rain = str(data["rain"]).replace(".",",")
        else:
            rain = 0
        wind_speed = str(data["wind_speed"]).replace(".", ",")

        #create an answer that can be spoken
        if type == "temp":
            if range == "daily":
                min = str(data["temp"]["min"]).replace(".", ",")
                max = str(data["temp"]["max"]).replace(".", ",")
                answer = "es wird zwischen {min} und {max} grad warm".format(min=min, max=max)
            else:
                temp = str(data["temp"]).replace(".",",")
                answer = f"es wird {temp} grad warm"
        elif type == "rain":
            if rain == 0:
                answer = " es wird keinen Niederschlag geben"
            else:
                answer = "es wird {rain} milimeter Niederschlag geben".format(rain=rain)
        elif type == "wind":
            answer = "die durchschnittliche Windgeschwindigkeit beträgt {wind} meter pro sekunde".format(wind=wind_speed)
        else:
            if range == "daily":
                min = str(data["temp"]["min"]).replace(".", ",")
                max = str(data["temp"]["max"]).replace(".", ",")
                answer = "es wird zwischen {min} und {max} grad warm, bei {rain} milimeter Niederschlag" \
                     " und einer durchschnittlichen Windgeschwindigkeit von {wind} meter pro sekunde".format(min=min, max=max, rain=rain, wind=wind_speed)
            else:
                temp = str(data["temp"]).replace(".", ",")
                answer = "es wird zwischen {temp} grad warm, bei {rain} milimeter Niederschlag" \
                         " und einer durchschnittlichen Windgeschwindigkeit von {wind} meter pro sekunde".format(
                    temp=temp, rain=rain, wind=wind_speed)

        return answer
