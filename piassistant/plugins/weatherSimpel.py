import requests

class Plugin():
    def __init__(self, memory, **kwargs):
        self.apiKey = kwargs["apiKey"]
        self.memory = memory
        self.dest = kwargs["location"]
        call = "http://api.openweathermap.org/data/2.5/weather?q={loc}&lang=de&appid={id}".format(loc=self.dest,
                                                                                                  id=self.apiKey)
        cache = requests.get(call)
        cache = cache.json()
        self.lon = cache["coord"]["lon"]
        self.lat = cache["coord"]["lat"]

    def process(self, command):
        weatherflag = None
        timeflag = None
        commad = command.lower()
        if "warm" in command or "grad" in command or "temperatur" in command:
            weatherflag = "temp"
        if "wetter" in command:
            weatherflag = "weather"
        if "wind" in command:
            weatherflag = "wind"
        if "regen" in command or "regnen" in command:
            weatherflag = "rain"

        if weatherflag is not None:
            data = {}
            call = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&lang=de&appid={id}&units=metric".format(
                lat=self.lat, lon=self.lon, id=self.apiKey)
            cache = requests.get(call)
            cache = cache.json()

            if "morgen" in command:
                data = cache["daily"][1]
            elif "übermorgen" in command:
                data = cache["daily"][2]
            elif "heute" in command:
                data = cache["daily"][0]
            else:
                data = cache["daily"][0]

            min = str(data["temp"]["min"]).replace(".",",")
            max = str(data["temp"]["max"]).replace(".",",")
            if "rain" in data.keys():
                rain = str(data["rain"]).replace(".",",")
            else:
                rain = 0
            speed = str(data["wind_speed"]).replace(".",",")

            if weatherflag == "temp":
                awnser = "es wird zwischen {min} und {max} grad warm".format(min=min,max=max)
            elif weatherflag == "rain":
                if rain == 0:
                    awnser = " es wird keinen Niederschlag geben"
                else:
                    awnser = "es wird {rain} milimeter Niederschlag geben".format(rain=rain)
            elif weatherflag == "wind":
                awnser = "die durchschnittliche Windgeschwindigkeit beträgt {wind} meter pro sekunde".format(wind=speed)
            else:
                awnser = "es wird zwischen {min} und {max} grad warm, bei {rain} milimeter Niederschlag" \
                         " und einer durchschnittlichen Windgeschwindigkeit von {wind} meter pro sekunde".format(min=min,max=max,rain=rain,wind=speed)
            return awnser
        return None

if __name__ == "__main__":
    plug = Plugin(None,location="Wiesloch",apiKey="Your API key")
    com = input("geben sie etwas ein:")
    ret = plug.process(com)
    print(ret)
