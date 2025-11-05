import pyttsx3
import speech_recognition as sr
import json
import os
import os
import webbrowser
from evilgpt import evil, code 

Assistant = pyttsx3.init()
voices = Assistant.getProperty('voices')
Assistant.setProperty('voice', voices[0].id)
Assistant.setProperty('rate', 170)

def speak(audio):
    print("  ")
    Assistant.say(audio)
    print(f": {audio}")
    print("  ")
    Assistant.runAndWait()

def load_data():
    data = {}
    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            data = json.load(file)
    return data

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

speak("Hello, Sunny sir. Your personal AI Assistant is ready.")

def takecommand(data, timeout=8):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening for your voice...")

        # Adjust the energy threshold to focus on near voices and potentially filter out background music
        r.energy_threshold = 5000  # Adjust this value as needed (higher threshold for higher intensity sounds)

        try:
            audio = r.listen(source, timeout=timeout)
            print("Recognizing...")
            
            # Analyze audio duration to differentiate intentional speech from background noise
            speech_duration = len(audio.frame_data) / audio.sample_rate

            if speech_duration >= 1.0:  # Adjust this threshold as needed
                query = r.recognize_google(audio, language='en-in')
                print(f"You said: {query}")
                return query.lower(), data
            else:
                print("No valid speech detected.")
                return "none", data

        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            return "none", data
        except sr.UnknownValueError:
            print("No speech detected.")
            return "none", data
        except sr.RequestError as e:
            print(f"Sorry, there was an error with the service: {e}")
            return "none", data




def process_command(query, data):
    words = query.split()  # Split the user's query into individual words
    found = False

    # Check each word against the keys in the JSON data
    for word in words:
        if word in data:
            speak(data[word])
            found = True
            break  # Break the loop if a match is found

    if not found:
        if "save" in query:
            speak("What data would you like to save?")
            data_to_save = takecommand(data)[0]  # Modified to take user input from speech
            data["saved_data"] = data_to_save
            save_data(data)
            speak("Data saved successfully!")

        elif "retrieve" in query:
            if "saved_data" in data:
                speak("Here is the saved data: " + data["saved_data"])
            else:
                speak("No saved data found.")

        # Check for command-answer pairs in data.json
        else:
            with open("data.json", "r") as file:
                commands = json.load(file)
                if query in commands:
                    speak(commands[query])


        
        
def TaskExe():
    data = load_data() 
    
    
 
    while True:
        query, data = takecommand(data)

        process_command(query, data)
        
        if "exit" in query:
            speak("Goodbye!")
            break
                 
            
        elif 'youtube'in query:
           for key, value in data.items():
            if key in query:
                # Extract the search query after the command keyword
                search_query = query.replace(key, value)
                search_query = search_query.strip()  # Remove extra spaces
                web = 'https://www.youtube.com/results?search_query=' + search_query
                webbrowser.open(web)
                speak(f"Searching for {search_query} on YouTube.")
                found = True
                break
          
        elif 'google' in query:
            for key, value in data.items():
                if key in query:
                    speak("Sure, searching on Google.")
                    query = query.replace(key, value)
                    query = query.strip()
                    search_url = f"https://www.google.com/search?q={query}"
                    webbrowser.open(search_url)
                    speak("Search on Google done!")
                    break 
                
        elif 'create code' in query:
            query = query.replace("create code", " ")
            response = evil(query)
            formatted_code = code(response)
            print(formatted_code)


        

        if query == 'none':
            continue

        if "sleep" in query:
            speak("Going to sleep. Wake me up by saying 'wake'.")
            while True:
                query = takecommand()
                if "wake" in query:
                    speak("I'm awake now. How can I assist you?")
                    break

 

if __name__ == "__main__":
    TaskExe()
