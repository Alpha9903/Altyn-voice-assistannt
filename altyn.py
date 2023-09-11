import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import openai
from aihead import apikey

engine = pyttsx3.init("sapi5")


voices = engine.getProperty('voices')       
engine.setProperty('voice', voices[0].id) 

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetings():
    hour = int(datetime.datetime.now().strftime("%H"))
    if hour< 0 and hour <12:
        speak("Good Evening Sir!")

    elif hour<=12 and hour<18:
        speak("Good Afternoon Sir!")

    elif hour<=18 and hour<20:
        speak("Good evening Sir!")

    else:
        speak ("Hello sir, how may I help you?")


def speech_recognition():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)

    # Recognize Speech
    try:
        print("Recogninsing....")
        problem = r.recognize_google(audio, language="en-in")
        print("you said" , problem)

    except Exception as e:
        print(e)

        speak("pardon, can you please say that again...") 

    return problem


greetings()

chatstr = ''
def chat(problem):
    global chatstr
    openai.api_key = apikey
    chatstr += f" Ketan : {problem} \n program: "
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = chatstr,
        max_tokens = 200,
        temperature = 0.5,
        n = 1,
        stop = None)
    print((response['choices'][0]['text']))
    speak(response['choices'][0]['text'])
    chatstr += f"{response['choices'][0]['text']}\n"
    return response['choices'][0]['text']


def ai(prompt):
    openai.api_key = apikey

    completion = openai.Completion.create(
        model = "text-davinci-003",
        prompt = prompt,
        max_tokens = 200,
        temperature = 0.5,
        n = 1,
        stop = None)

    response = completion.choices[0].text
    print(response)
    speak(response)


while True:
    problem = speech_recognition().lower()

    if "wikipedia" in problem:
        speak("Searching Wikipedia for your query......")
        problem = problem.replace('wikipedia', "")
        results = wikipedia.summary(problem , sentences = 2 )
        speak("according to wikipedia")
        speak(results)

    elif "the time" in problem:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"the time is {strTime} sir")

    elif "spotify" in problem:
        speak("opening spotify..")
        webbrowser.open_new("www.spotify.com")

    elif "google" in problem:
        speak("searching google....")
        webbrowser.open_new("www.google.com")

    elif "youtube" in problem:
        speak("opening youtube")
        webbrowser.open_new("www.youtube.com")

    elif "quit" in problem:
        speak("thank you sir...")
        break	

    elif "shin-chan" in problem:
        ai(prompt = problem)

    else:
        chat(problem)


