import os

dictionary = {
    "blender": "C:/Program Files/Blender Foundation/Blender 2.91/blender.exe"
}

class Plugin:
    def __init__(self, *args, **kwargs):
        pass
    def process(self, command):
        splitCommand = command.split(" ")
        keywords = ["öffne"]
        testKeyword = False
        for keyword in keywords:
            if keyword in command:
                testKeyword = True
        programm = "nichts"
        if testKeyword is True:
            for word in splitCommand:
                if word != "öffne":
                    print(word)
                    if os.system(word) == 1:
                        if word in dictionary:
                            os.startfile(dictionary[word])
                        else:
                            print("error") #os.system(word)
        # return("Ich öffne".format(programm))

"""
c = Plugin()
c.process("öffne blender")
"""

if __name__ == "__main__":
    c = Plugin()
    for i in ["fünf","drei","dreiundzwanzig","fünfundsechzig"]:
        num = c.process("dummy",i+" timer")
        print(num)