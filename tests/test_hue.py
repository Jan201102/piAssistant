from unittest import TestCase
from piassistant.plugins import hue
from json import loads


class TestPlugin(TestCase):
    def setUp(self) -> None:
        #self.hue = hue.Plugin(None,ip = "192.168.2.106")
        self.converter = hue.CommandConverter()

    def test_run_model(self):
        testCommands = [["mache die stehlampe aus"," stehlampe : off"],
                        ["mache das licht aus"," all : off"],
                        ["mache das licht an"," all : on"],
                        ["mache das licht aus"," all : off"],
                        ["dimme das licht auf siebzig prozent"," all : 70"],
                        ["schlate die stehlampe aus und die leselampe an", " stehlampe : off , leselampe : on"],
                        ["wie soll das wetter werden"," none"]]
        for command in testCommands:
            with self.subTest(command = command):
                result = self.converter.run_model(command[0])
                self.assertEqual(result, command[1])

    def test_output_to_json(self):
        testInputs=[[" all : off", "{'all':'off'}"],["leselampe : off","{'leselampe':'off'}"],
                    ["leselampe klein : 60 , tischlampe : off","{'leselampe klein':60,'tischlampe':'off'}"]]
        for input in testInputs:
            with self.subTest(input = input):
                result = self.converter.output_to_json(input[0])
                self.assertEqual(str(result).replace(" ",""),input[1].replace(" ",""))
