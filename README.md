# piAsisstant
## Installation and Usage
### Requiered Python packages
- vosk
- pandas
- pyaudio
- pocketsphinx or pvcorupine and pyrecorder
- tensorflow or tensorflow lite
### Other requiered packages
- neopixel: see Adafruits installation guide for neopixel in Python
### Requiered models
- vosk model of your choice: https://alphacephei.com/vosk/models
- pocketsphinx model of your choice: https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/
### Optional Python packages
- general
  - mosquitto
- hue
  - hue-py
- weatherSimple
  - none
- timer
  - pyame
  

## Configuration
The piAssistant is configuered via the config.json file.
### General structure
```json
  {"assistant":{"configuration of the core functionalities"
               },
  "plugins": {"<plugin name>":{"configuration"} "every plugin
              that is listed in here will be used, all other will be ignored"
              },
  "apps": {"<app name": {"app specific configurations"}}
  }
```
### Configuration of the core functionalities
```json
{"assistant":{"voskModel": ["the path to the vosk model"],   
              "KWS_engine":"<engine>" # insert "picovoice" or "pocketsphinx"
              "name": "word by wich the assistant will be activated",
              "signals":"on/off", # set to "on" if you have neopixels atached, default is "off"
              "micId":<int> # index number of the mic used for audio input
              <other args>
              },
}
```
If you want to use Pocketsphinx for key word search replace `<other args>` with:
```json
      "sensitivity": "value 0-100",
      "pocketsphinxModel":"the path to the pocketsphinxmodel directory"
```
If you want to use picovoice  replace `<other args>` with:
```json
    "picovoice_acccessn_key":"your access key"
```
### Apps
All apps are controlled with one single tensorflow model. The tensorflow model processes the user
input and then calls the corresponding apps. All necessary information
and configuration are provided via config.json.
#### App configuration
- hue
```json
"hue":{"ip":"ip of your hue bridge"}
```
- weatherSimple
```json
"weatherSimple":{"apiKey":"apiKey for openweathermap.org",
                 "location":"name of the location you want to have weather information on"}
```
- timer
```json
"timer":{}
```
### Plugins
If the main tensorflow model can't determine, which app the user wants to use,
the user input is passed to all plugins. Each plugin then processes the input for itself.
#### Plugin configuration
currently there are no plugins available
### Run
After setting everything  up to your wishes just run the example.py file
