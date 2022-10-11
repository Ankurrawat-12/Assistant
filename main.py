import speech_recognition as sr
import pywhatkit
import sys
import pyttsx3
import datetime
import wikipedia
import pyjokes

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
voice = 1
rate = 150
name = voices[voice].name.split(" ")[1]
engine.setProperty('voice', voices[voice].id)
engine.setProperty('rate', rate)



def speak(text):
    engine.say(text)
    engine.runAndWait()


def hear_me():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        audio = r.listen(source)
    try:
        print("Recognizing")
        query = r.recognize_google(audio, language='en-in')
        print('you said : ', query)
        engine.say(query)
        engine.runAndWait()
    except Exception:
        engine.say('Say that again')
        print('Say That Again')
        hear_me()
    return query


def change_property():
    speak("What do you want to change")
    option = hear_me().lower()
    if "speed" in option:
        speak("Do you want to change the speach Speed")
        change_speed = hear_me().lower()
        if "yes" in change_speed:
            speak("What speed do you want")
            new_rate = int(hear_me())
            engine.setProperty('rate', new_rate)
            speak("changed the speach speed from" + rate + "to" + new_rate)
        else:
            speak("ok")
    if "assistant" in option:
        speak("Do you want to change the assistant")
        change_assistant = hear_me()
        if "yes" in change_assistant:
            speak("What Assistant do you want")
            assistant = hear_me().lower()
            # new_voice = voice

            if "female" in assistant:
                voice = 1
            else:
                voice = 0
            engine.setProperty('voice', voices[voice].id)
            name = voices[voice].name.split(" ")[1]
            speak("Hi, My Name is " + name + ".")
            speak("i am your new Assistant")


if __name__ == "__main__":
    speak("Hi, My Name is " + name + ".")
    speak("do you want to change the settings")
    change = hear_me().lower()
    if "yes" in change:
        change_property()
    else:
        speak("Good by mister")

