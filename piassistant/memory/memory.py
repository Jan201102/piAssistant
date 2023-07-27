import logging
import os
import pandas as pd
import shutil


class Memory:
    def __int__(self):
        pass

    def memorize(self, plugin, **data):
        if plugin+".csv" in os.listdir("./memory"):
            dataframe = pd.read_csv("./memory/"+plugin+".csv")
        else:
            dataframe = pd.DataFrame()
        logging.debug(dataframe)
        for key in data.keys():
            if key not in dataframe.columns:
                dataframe[key] = None
        logging.debug(dataframe)
        dataframe = dataframe.append(data, ignore_index=True)

        dataframe.to_csv("./memory/"+plugin+".csv",index=False)

    def memorize_audio(self, wavfile, text):
        shutil.move(wavfile, "./memory/wavFiles/")
        with open("./memory/transcriptions.csv", "a") as out:
            out.write(wavfile+";"+text+"\n")
