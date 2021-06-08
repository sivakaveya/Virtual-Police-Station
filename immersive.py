#pip install SpeechRecognition
#pip install gTTS
#pip install google-trans-new
#pip install pygame

import speech_recognition as sr
from gtts import gTTS
from google_trans_new import google_translator
from pygame import mixer
from time import sleep
import pyttsx3 as tts

translator = google_translator()
mixer.init()
engine=tts.init()


def translation(s, lang):
    s = translator.translate(s, lang)
    return s


def speak(text, lang):
    text = translation(text, lang)
    print(text)
    engine.say(text)
    engine.runAndWait()
    '''speech = gTTS(text,lang=lang)
    speech.save("C:\\Users\\sivaa\\PycharmProjects\\Virtual_Police_Station\\voice.mp3")
    mixer.music.load("C:\\Users\\sivaa\\PycharmProjects\\Virtual_Police_Station\\voice.mp3")
    mixer.music.play(1)
    sleep(1)'''


def speech_recognition():
    r = sr.Recognizer()
    #print("Speak a sentence: ")
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, 2, 8)
            text = r.recognize_google(audio)
            return text
        except:
            print("Not Audible!")


if __name__ == '__main__':
    '''t = speech_recognition()
    print("Choose a Language: 1.Hindi 2.English 3.Tamil 4.Malayalam 5.Gujarati")
    c=int(input())
    if c==1:
        speak(t, 'hi')
    elif c==2:
        speak(t,'en-in')
    elif c==3:
        speak(t, 'ta')
    elif c==4:
        speak(t, 'ml')
    elif c==5:
        speak(t, 'gu')
    else:
        print("invalid Choice")
    print(t)'''
    t=translation("How are you",'gu')
    print(t)
    #speak("tame kem cho",'hi')
    '''voices=engine.getProperty('voices')
    engine.say("Hello Ritika")
    engine.runAndWait()
    for voice in voices:
        print(voice)'''
    speak("Hello World",'en')
    speak("Ritika",'en')


#pata nahi  i cant hear  now its working