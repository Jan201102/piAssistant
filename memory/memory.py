import mysql.connector
import os


# Table memory:
# CREATE TABLE memory(ID INTEGER AUTO_INCREMENT,
#                    audio MEDIUMBLOB null,
#                    transcription varchar(256) null,
#                    Primary key(ID));

class Memory:
    def __init__(self):
        try:
            self.DBconnection = mysql.connector.connect(user='piAssistant',
                                                        password='12345',
                                                        database='Memory')
        except:
            self.DBconnection = None

    def __del__(self):
        self.DBconnection.close()

    def memorize(self, audio_file=None, transcription=None):
        if self.DBconnection is not None:
            query = "INSERT INTO memory(audio,transcription) Values(%s,%s)"
            cursor = self.DBconnection.cursor()
            blob = None

            if audio_file is not None:
                with open(audio_file, 'rb') as f:
                    blob = f.read()
                os.remove(audio_file)

            if audio_file is not None or transcription is not None:
                data = (blob, transcription)
                cursor.execute(query, data)
                self.DBconnection.commit()

            cursor.close()
