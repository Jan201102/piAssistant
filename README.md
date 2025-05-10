# piAsisstant
## Installation and Usage
### Requiered Python packages
For windows use the [requirements_windows.txt](requirements_windows.txt) with pip install.
### Other requiered packages
- neopixel: see Adafruits installation guide for neopixel in Python. To be able to run neopixel without root priviliges add:
```
dtparam=spi=on
enable_uart=1
```
to `/boot/config.txt` and connect neopixel to `GPIO10`.
### Requiered models
- vosk model of your choice: https://alphacephei.com/vosk/models
- pocketsphinx model of your choice: https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/ **OR**
- openwakeword models: https://github.com/fwartner/home-assistant-wakewords-collection/tree/main

### Optional Python packages
- general
  - mosquitto
- hue
  - hue-py
- weatherSimple
  - openmeteo_requests
  - requests-cache
  - retry-requests
- timer
  - pyame

### notes on running on pi5
python packages:
 - pyalsaaudio
 - numpy<2 for openwakeword with tflite models
 - tensorflow needed because of some issues wirh support in tflite for tf ops

 ### seting up systemd service
fill in the missing information in th $$ fields in `piassistant-template.service`. Then paste the contents into a file called `/etc/systemd/system/piassistant.service`. After that reaload systemctl with `sudo systemctl daemon-reload`.Then enable the service with 'sudo systemctl enable piassistant` and start it with `sudo systemctl start piassistant`. 

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
              "KWS_engine":"<engine>" # insert "picovoice" or "pocketsphinx" or "openwakeword"
              "signals":"on/off", # set to "on" if you have neopixels atached, default is "off"
              <other args>
              },
}
```
If you want to use Pocketsphinx for key word search replace `<other args>` with:
```json
      "sensitivity": "value 0-100",
      "name": "word by wich the assistant will be activated",
      "pocketsphinxModel":"the path to the pocketsphinxmodel directory"
```
If you want to use picovoice  replace `<other args>` with:
```json
    "picovoice_acccessn_key":"your access key" replace `<other args>` with:
```
If you want to use the openwakeword implementation replace `<other args>` with:

```json
  "openwakewordmodels":["list_of_paths_to_modelfiles"]
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
"weather":{"location":"name of the location you want to have weather information on"}
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

# TODO
## latency improvements
it currently take about 3s from end of speaking to hearing the first answer when using an llm
latency on windows laptop with tts systemengine
1. 1.5s: let vosk stop the listentig faster, takes about 1.5s (half the delay)-> try realtimestt to look for imrpovements, seems to be only as fast, -> manually add VAD to vosk
2. 0.5s: takes about 0.5s from stoping the listening to the first call to say_stream(writing wav: 0.1s, mastermodel 0.15s, getting the first token from ollama: 0.3s)
3. 1s: takes about 1s to synthesise the first audio chunk
