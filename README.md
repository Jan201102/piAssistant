# piAsisstant
## Installation and Usage
### Requiered Python packages
- vosk
- pandas
- pyaudio
- pocketsphinx
### Requiered models
- vosk model of your choice: https://alphacephei.com/vosk/models
- pocketsphinx model of your choice: https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/
### Optional Python packages
- general
  - mosquitto
- hue
  - tensorflow
  - hue-py
  - keras
-hueLite
  - tensorflowlite
- weatherSimple
  - none
- clock
  - pyame
  - numpy
  

## Configuration
The piAssistant is configuered via the config.json file.
### General structure
```json
  {"assistant":{"configuration of the core functionalities"
               },
  "plugins": {"<plugin name>":{"configuration"} "every plugin
              that is listed in here will be used, all other will be ignored"
              }
  }
```
### Configuration of the core functionalities
```json
{"assistant":{"voskModel": ["the path to the vosk model"],   
              "sensitivity": "value 0-100",
              "pocketsphinxModel":"the path to the pocketsphinxmodel directory",
              "name": "word by wich the assistant will be activated",
              "mqtthost":"<optional> ip of the mqtt host",
              "light":"<optional> mqtt compatilbe light to light up, if assistant is active"},
}
```
### plugin configuration
- hue & hueLite
```json
"hue":{"ip":"ip of your hue bridge"}
```
```json
"hueLite":{"ip":"ip of your hue bridge"}
```
- weatherSimpel
```json
"weatherSimple":{"apiKey":"apiKey for openweathermap.org",
                 "location":"name of the location you want to have weather information on"}
```
- clock
```json
"clock":{"no configuration needed"}
```
### Run
After setting everything  up to your wishes just run the example.py file
