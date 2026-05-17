import random
import webbrowser
import requests
import pyttsx3
import speech_recognition as sr


class VoiceAssistant:
    """Voice assistant with word search functionality - FULL VOICE MODE"""
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        
        # 设置英语语音
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if 'english' in voice.name.lower() or 'en' in voice.id.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.in_dialog = False
        self.current_word_data = None
        self.current_word = None
        self.current_random_index = None
        
        # 校准麦克风
        self.say("Calibrating microphone. Please wait...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        self.say("Microphone ready!")

    def say(self, text):
        print(f'Assistant: {text}')
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        try:
            with self.microphone as source:
                print("\n[Listening...]")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("[Processing...]")
            command = self.recognizer.recognize_google(audio, language='en-US')
            print(f'You said: {command}')
            return command.lower()

        except sr.WaitTimeoutError:
            print("No speech detected")
            return ''
        except sr.UnknownValueError:
            self.say("Sorry, I didn't understand that")
            return ''
        except sr.RequestError as e:
            self.say(f"Speech recognition service error: {e}")
            return ''
        except Exception as e:
            print(f"Error: {e}")
            return ''

    def get_word(self, word):
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        try:
            response = requests.get(url)
            if response.status_code != 200:
                self.say(f'Word "{word}" not found')
                return None
            return response.json()
        except requests.RequestException:
            self.say('Network error occurred')
            return None

    def run(self):
        self.say('Your voice assistant is activated and ready to work!')
        self.say('Please say "hello assistant" to begin.')
        
        print("\n" + "="*50)
        print("VOICE COMMANDS:")
        print('  Say "hello assistant" - start assistant')
        print('  Say "goodbye" - exit program')
        print('  Say "find" - search for a word (after start)')
        print('  Say "meaning" - get definition')
        print('  Say "example" - get example sentence')
        print('  Say "link" - open dictionary link')
        print('  Say "save" - save to file')
        print('  Say "stop" - exit word feature')
        print("="*50 + "\n")

        while True:
            command = self.listen()
            
            if not command:
                continue
                
            if 'hello assistant' in command:
                self.say('Hello! Give me a task. Say "find" to search for a word.')
                self.in_dialog = True
                
            elif 'goodbye' in command:
                self.say('Goodbye!')
                break
                
            elif self.in_dialog and 'find' in command:
                self.say('Tell me what word do you want to find. Say only one word')
                word = self.listen()
                
                if not word:
                    continue
                    
                self.say(f'You said: {word}')
                res = self.get_word(word)
                
                if not res:
                    continue
                
                self.current_word_data = res
                self.current_word = word
                self.current_random_index = random.randint(0, len(res[0]['meanings'])-1)
                self.say('What do you want to do? Say: meaning, example, link, save, or stop')
                
            elif self.in_dialog and 'meaning' in command and self.current_word_data:
                try:
                    meaning = self.current_word_data[0]['meanings'][self.current_random_index]['definitions'][0]['definition']
                    self.say(f'Meaning: {meaning}')
                except (KeyError, IndexError):
                    self.say('Could not retrieve meaning')
                    
            elif self.in_dialog and 'example' in command and self.current_word_data:
                try:
                    definition_data = self.current_word_data[0]['meanings'][self.current_random_index]['definitions'][0]
                    if 'example' in definition_data:
                        self.say(f'Example: {definition_data["example"]}')
                    else:
                        self.say('There is no example')
                except (KeyError, IndexError):
                    self.say('Could not retrieve example')
                    
            elif self.in_dialog and 'link' in command and self.current_word_data:
                try:
                    link = self.current_word_data[0]['sourceUrls'][0]
                    webbrowser.open(link)
                    self.say('Opening link in browser')
                except (KeyError, IndexError):
                    self.say('No link available')
                    
            elif self.in_dialog and 'save' in command and self.current_word_data:
                try:
                    meaning = self.current_word_data[0]['meanings'][self.current_random_index]['definitions'][0]['definition']
                    link = self.current_word_data[0]['sourceUrls'][0]
                    with open('last_word.txt', 'w', encoding='utf-8') as file:
                        file.write(f"{self.current_word}\nDefinition: {meaning}\nLink: {link}")
                    self.say('Word information saved to file')
                except Exception:
                    self.say('Error saving file')
                    
            elif self.in_dialog and 'stop' in command:
                self.say('Returning to main menu')
                self.in_dialog = False
                self.current_word_data = None
                
            elif self.in_dialog:
                self.say('Please say: meaning, example, link, save, or stop')


if __name__ == '__main__':
    print("Starting Voice Assistant...")
    print("Make sure your microphone is connected and allowed.\n")
    assistant = VoiceAssistant()
    assistant.run()