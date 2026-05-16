import speech_recognition as sr

from speakerpy.lib_speak import Speaker
from datetime import datetime

import data

class VoiceAssistant:
    def __init__(self):
        self.speaker = Speaker(model_id="ru_v3", language="ru", speaker="baya", device="cpu")
        self.r = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.command = ''
        self.dictionary = data.phrases
        self.funcs = data.funcs
        self.keyword = data.keyword
        self.time = int(datetime.now().time().hour)
        self.commands = {
            data.shutdown: self.shutdown,
        }
        for key, value in self.dictionary.items():
            if key in self.funcs:
                self.commands[value] = self.funcs[key]

    def speak(self, text, speed=1.0, sample_rate = 48000):
        self.speaker.speak(text=text, sample_rate=sample_rate, speed=speed)

    def listen_for_activate(self):
        print('\n=== ЖДУ ===')
        
        with sr.Microphone() as source:
            while True:
                audio = self.r.listen(source)
                try:
                    command = self.r.recognize_google(audio, language="ru-RU")
                
                    if command is None:
                        continue

                    if "алиса" in command.lower():
                        self.listen_for_commands()
                        break
                    elif 'выключаю' in command.lower():
                        self.shutdown()

                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print(f"Ошибка запроса; {e}")   

    def listen_for_commands(self):
        print('\n=== СЛУШАЮ ===')
        self.speak(data.gs2[1])
        with sr.Microphone() as source:
            while True:
                self.r.pause_threshold = 1.5
                audio = self.r.listen(source)
                try:
                    command = self.r.recognize_google(audio, language="ru-RU")
                    
                    if "вернись" in command.lower() or "назад" in command.lower():
                        print("Возвращаюсь в режим ожидания")
                        self.speak(data.gs2[4])
                        return
                    
                    command = command.lower().strip()
                    for phrase, func in self.commands.items():
                        if phrase in command:
                            try:
                                self.speak(func(command))
                            except TypeError:
                                self.speak(func())    
                            return
                        
                    else:    
                        self.speak(data.AI(command))

                except sr.UnknownValueError:
                    print("Не удалось распознать команду.")
                    return 
                except sr.RequestError as e:
                    print(f"Ошибка запроса; {e}")
                    return   

    def shutdown(self):
        print("Выключаюсь полностью")
        self.speak(data.gs2[5])
        exit(0)

    def run(self):
        print("ЗАПУСТИЛСЯ")
        if self.time >= 4 and self.time <= 11:
            self.speak(data.Random_phrase(data.greetings_morning))
        elif self.time >= 12 and self.time <= 16:
            self.speak(data.Random_phrase(data.greetings_afternoon))
        elif self.time >= 17 and self.time < 22:
            self.speak(data.Random_phrase(data.greetings_evening))
        else:
            self.speak(data.Random_phrase(data.greetings_night))

        while True:
            self.listen_for_activate()

assistant = VoiceAssistant()
assistant.run()