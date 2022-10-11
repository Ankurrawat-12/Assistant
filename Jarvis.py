import csv
import datetime
import pyttsx3
import speech_recognition as sr
import pyjokes
import wikipedia
from randfacts import get_fact
import webbrowser
import google_search_py


engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
gender = 1
rate = 180
lines = 2
speach_power = 500
my_age = voices[gender].age
name = voices[gender].name.split(" ")[1]
engine.setProperty('voice', voices[gender].id)
engine.setProperty('rate', rate)
personal_info = {
    'Name': "Ankur Rawat",
    "Age": 18,
    "Email": "ankurrawat620@gmail.com",
    "Phone": 8287413412
}
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s"
# chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

with open("about_me.csv", 'w') as file:
    writer = csv.writer(file)
    for key, value in personal_info.items():
        writer.writerow([key, value])


def speak(audio):
    """
    AI speak something
    :param audio:
    :return:
    """
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def about_myself():
    # not completed
    with open("about_me.csv", 'r') as file:
        dict_reader = csv.DictReader(file)
        personal_info = dict(list(dict_reader)[0])
    # speak(f"you'r name is {personal_info['Name']}, You are {personal_info['Age']} years old,"
    #       f" you'r email is {personal_info['Email']}, you'r phone number is {personal_info['Phone']}")
    for things in personal_info:
        speak(f"You'r {things} is {personal_info[things]}")
    speak("Do you want to Update You'r Personal Info")
    change = take_command().lower()
    if 'yes' in change:
        speak("What do you Want to do?")
        option = take_command().lower()
        if "name" in option:
            speak("What is you'r name")
            personal_info['Name'] = take_command().lower()
        if "age" in option:
            speak("What is you'r age")
            personal_info['Age'] = take_command().lower()
        if "phone" in option:
            speak("What is you'r Phone number")
            personal_info['Phone'] = int(take_command())
        if "email" in option:
            speak("What is you'r Email Address")
            personal_info['Email'] = take_command().lower() + "@gmail.com"
    else:
        speak("ok")


def wikipedia_search(query):
    """
    search something in wikipedia
    :param query:
    :return: results
    """
    try:
        results = wikipedia.summary(query, sentences=5)
    except Exception as e:
        speak("Please try to search for more specific term")
        return "NONE"
    return results


def change_property():
    """
    this function is used to change the settings of the assistant
    :return:
    """
    speak("What do you want to change")
    option = take_command().lower()
    if "speed" in option:
        speak("Do you want to change the speach Speed")
        change_speed = take_command().lower()
        if "yes" in change_speed:
            speak("What speed do you want")
            new_rate = int(take_command())
            engine.setProperty('rate', new_rate)
            speak(f"changed the speach speed from {rate} to {new_rate}")
        else:
            speak("ok")
    elif "assistant" in option:
        speak("Do you want to change the assistant")
        change_assistant = take_command()
        if "yes" in change_assistant:
            speak("What Assistant do you want")
            assistant = take_command().lower()
            if "david" in assistant:
                voice = 0
            else:
                voice = 1
            engine.setProperty('voice', voices[voice].id)
            name = voices[voice].name.split(" ")[1]
            speak("Hi, My Name is " + name + ".")
            speak("i am your new Assistant")


def tell_fact():
    """
    Tells a Random Fact
    :return:
    """
    fact = get_fact(False)
    speak(f"Time for Some fact , {fact}")


def wish_me():
    """
    Wishes me according to the time
    :return:
    """
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning, Sir")
    elif 12 <= hour < 18:
        speak("Good Afternoon, Sir")
    else:
        speak("Good Evening, Sir")
    speak("I am " + name)


def google_Search(query):
    """
    search the query in the Google and open's it in brave
    :param query:
    :return:
    """
    query.replace("search", "")
    search = google_search_py.search(query)
    speak(search['title'])
    speak(search['description'])
    webbrowser.get(brave_path).open(search['url'])


def tell_joke():
    """
    Tells a Joke
    :return:
    """
    joke = pyjokes.get_joke()
    speak(joke)


def about_me():
    """
    about AI
    :return:
    """
    speak(f"Hello my name is {name}")
    speak(f"I am {my_age} year's old")
    speak("I was developed in India")
    # speak("Ankur Rawat Developed me")


def take_command():
    """
    Takes microphone input from the user
    :return: string
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        # r.pause_threshold = 1
        r.energy_threshold = speach_power
        audio = r.listen(source)
 
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        speak(f"You said , {query}")

    except Exception as e:
        # print(e)
        speak("Say That Again Please")
        return "None"
    return query


if __name__ == "__main__":
    speak("Hello Sir")
    # print("say :- Wikipedia the term you want to search about")
    wish_me()
    while True:
        speak("Please tell me how may i help you")
        query = take_command().lower()
        if "fact" in query:
            tell_fact()
        elif "joke" in query:
            tell_joke()

        # information
        elif "wikipedia" in query:
            search = query.replace("wikipedia", " ")
            result = wikipedia_search(search)
            speak(f"Searching {search} in Wikipedia")
            if result != "NONE":
                speak(f"According to Wikipedia")
                speak(result)
        elif "search" in query:
            google_Search(query)
        # open websites
        # elif "open " in query:
        #     search = query.replace('open ', '')
        #     search.replace(' ', '')
        #     speak(f"Opening {search}")
        #     webbrowser.get(brave_path).open(f"{search}.to")
        elif "open" in query:
            search = query.replace('open ', '')
            speak(f"Opening {search}")
            if "." in query:
                webbrowser.get(brave_path).open(f"{search}")
            else:
                webbrowser.get(brave_path).open(f"{search}.com")

        elif "youtube" in query and "open" not in query:
            search = "https://www.youtube.com/results?search_query=" + query.split(" youtube")[0].replace(" ", "+")
            speak(f"Searching {query.split(' youtube')[0]} at Youtube")
            webbrowser.get(brave_path).open(search)
        elif "anime" in query and "open" not in query:
            search = "https://animixplay.to/v1/" + query.split(" anime")[0].replace(" ", "-")
            speak(f"Opening {query.split(' anime')[0]} at anime")
            webbrowser.get(brave_path).open(search)
        elif "manga" in query and "open" not in query:
            search = "https://mangakakalot.is/search?keyword=" + query.split(" manga")[0].replace(" ", "+")
            speak(f"Opening {query.split(' manga')[0]} manga")
            webbrowser.get(brave_path).open(search)

        # date and time
        elif "today's date" in query:
            date = datetime.datetime.now().date()
            speak(f"Today's Date is {date}")
        elif "current time" in query:
            hour = int(datetime.datetime.now().hour)
            min = int(datetime.datetime.now().minute)
            sec = int(datetime.datetime.now().second)
            speak(f"Current time is {hour} Hour , {min} Minutes and {sec} , {sec + 1}, {sec + 2}  seconds")
        # My self
        # elif "about" in query and ("me" in query or "myself" in query):
        #     about_myself()

        # assistant
        elif "yourself" in query:
            about_me()

        elif "settings" in query and "assistant" in query:
            change_property()
        # close assistant
        elif "quit" in query or "good night" in query:
            speak("Goodbye Sir, Take care")
            break
