from numpy import array


class SpeechActToVectorConverter:

    speech_acts: dict = {
        "ack": 1,
        "affirm": 2,
        "bye": 3,
        "confirm": 4,
        "deny": 5,
        "hello": 6,
        "inform": 7,
        "negate": 8,
        "null": 9,
        "repeat": 10,
        "reqalts": 11,
        "reqmore": 12,
        "request": 13,
        "restart": 14,
        "thankyou": 15
    }

    def convert_from_speech_act(self, speech_act: str):
        return self.speech_acts[speech_act]

    def convert_to_speech_act(self, integer: int):
        for speech_act, integer_representation in self.speech_acts.items():
            if integer_representation == integer:
                return speech_act
        return ""

    def convert_list(self, speech_acts: list):
        print("Converting speech act list")
        result = list()
        for speech_act in speech_acts:
            result.append(array([self.convert_from_speech_act(speech_act)]))
        print("Done converting speech act list")
        return array(result)
