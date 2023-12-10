import logging
import os
import pandas as pd
import shutil
from os import path


class Memory:
    def __init__(self):
        self.memory_folder = path.dirname(__file__)

    def memorize(self, plugin, **data):
        if plugin+".csv" in os.listdir(self.memory_folder):
            dataframe = pd.read_csv(path.join(self.memory_folder, plugin+".csv"))
        else:
            dataframe = pd.DataFrame()
        logging.debug(dataframe)
        for key in data.keys():
            if key not in dataframe.columns:
                dataframe[key] = None
        logging.debug(dataframe)
        dataframe = dataframe.append(data, ignore_index=True)

        dataframe.to_csv(path.join(self.memory_folder, plugin+".csv"),index=False)

    def memorize_audio(self, wavfile, text):
        shutil.move(wavfile,path.join(self.memory_folder,"wavFiles/"))
        with open(path.join(self.memory_folder,"transcriptions.csv"), "a") as out:
            out.write(wavfile+";"+text+"\n")