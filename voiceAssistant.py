import speech_recognition as sr  # import the speech recognition module
import playsound  # import a module to play audio files
from gtts import gTTS  # import the gTTS (Google Text-to-Speech) module
import os  # import the os module
import wolframalpha  # import the wolframalpha module to perform calculations
from selenium import webdriver  # import the webdriver module to control Chrome
from selenium.webdriver.common.keys import Keys  # import the keys module to send special keys to the web browser
from selenium.webdriver.common.by import By  # import the by module to specify which element to search for on a webpage
from selenium.webdriver.chrome.options import Options  # import the options module to set Chrome options

num = 1  # initialize the num variable to 1

# define the assistantSpeaking function which takes in a string called 'output'
def assistantSpeaking(output):
    global num  # make the num variable global so it can be modified within this function
    num += 1  # increment the num variable by 1
    print("Human: ", output)  # print the output string to the console

    # create a gTTS object called 'toSpeak' with the given text and language
    toSpeak = gTTS(text=output, lang='en', slow=False)
    file = str(num)+".mp3"  # create a string called 'file' with the value of num concatenated with ".mp3"
    toSpeak.save(file)  # save the gTTS object to the file
    playsound.playsound(file, True)  # play the audio file
    os.remove(file)  # delete the file

# define the getAudio function which doesn't take in any parameters
def getAudio():
    rObject = sr.Recognizer()  # create a recognizer object
    audio = ""  # initialize the audio variable to an empty string
    with sr.Microphone() as source:  # open the default microphone
        print("Speak...")  # print a message to the console
        audio = rObject.listen(source, phrase_time_limit=10)  # listen for audio for up to 10 seconds
    print("Enough. ")  # print a message to the console once the user has stopped speaking

    # try to recognize the audio using Google's speech recognition service
    try:
        text = rObject.recognize_google(audio, language='en-US')  # recognize the audio and store it in the 'text' variable
        print("You: ", text)  # print the recognized text to the console
        return text  # return the recognized text
    except:
        # if the audio couldn't be recognized, call the assistantSpeaking function with an error message
        assistantSpeaking("I'm sorry, I couldn't understand you. Can you try again? ")
        return 'a'  # return 'a' as a placeholder

# define the searchweb function which takes in a string called 'input'
def searchweb(input):
    input = input[input.index('search')+6:]  # get the search query by slicing the input string
    print(input)  # print the search query to the console
    chrome_options = Options()  # create a Chrome options object
    chrome_options.add_experimental_option('detach', True)  # set the detach option to True
    driver = webdriver.Chrome(options=chrome_options)  # create a Chrome webdriver object with the given options
    query = input.split()  # split the search query into a list of words
    # navigate to Google's search page with the search query
    driver.get("https://www.google.com/search?q=" + '+'.join(query))
    return  # end the function

# define the playvideo function which takes in a string called 'input'
def playvideo(input):
    input = input[input.index('play')+4:]  # get the search query by slicing the input string
    print(input)  # print the search query to the console
    chrome_options = Options()  # create a Chrome options object
    chrome_options.add_experimental_option('detach', True)  # set the detach option to True
    driver = webdriver.Chrome(options=chrome_options)  # create a Chrome webdriver object with the given options
    query = input.split()  # split the search query into a list of words
    # navigate to YouTube's search page with the search query
    driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query))
    return  # end the function

# define the processText function which takes in a string called 'input'
def processText(input):
    try:
        if "search" in input:  # if the user wants to search the web
            searchweb(input)  # call the searchweb function
        elif "play" in input:  # if the user wants to play a video
            playvideo(input)  # call the playvideo function
        elif "tell me a joke" in input or "make me laugh" in input:  # if the user wants a joke
            says = "Why did the chicken cross the road? To get to the other side ha ha ha ha ha"  # create a joke string
            assistantSpeaking(says)  # call the assistantSpeaking function with the joke string
            return  # end the function
        
        elif "calculate" in input:  # if the user wants to perform a calculation
            app_id = "TY9X97-TEKHRHX6T7"  # create a string with the Wolfram Alpha API key
            client = wolframalpha.Client(app_id)  # create a Wolfram Alpha client with the API key
            res = client.query(' '.join(input.split()))  # send a query to the Wolfram Alpha API
            answer = next(res.results).text  # get the first result from the API response
            assistantSpeaking("The answer is " + answer)  # call the assistantSpeaking function with the answer
            return  # end the function

        else:  # if the user's input is something else
            assistantSpeaking("I can browse Chrome for you, do you want that? If yes, what would you like to search? ")  # ask the user if they want to search the web
            rply = getAudio()  # get the user's response
            if "yes" in str(rply) or "yea" in str(rply) or "sure" in str(rply):  # if the user wants to search the web
                searchweb(input)  # call the searchweb function
        
    except:  # if an exception occurs
        assistantSpeaking("I don't understand, I can search the web for you, Do you want to continue?")  # ask the user if they want to search the web
        rply = getAudio()  # get the user's response
        if "yes" in str(rply) or "yea" in str(rply) or "sure" in str(rply):  # if the user wants to search the web
            searchweb(input)  # call the searchweb function

if __name__ == "__main__":
    # call the assistantSpeaking function with a greeting message
    assistantSpeaking("Hello! I'm a robot, what is your name, Friend? ")
    name = "Friend"  # initialize the name variable to "Friend"
    name = getAudio()  # get the user's name
    # call the assistantSpeaking function with a greeting message using the user's name
    assistantSpeaking(f"Hey, {name}! ")

    while(1):  # create an infinite loop
        # call the assistantSpeaking function with a prompt for the user
        assistantSpeaking("How can I be of assistance? ")
        text = getAudio().lower()  # get the user's input and convert it to lowercase
        
        if text == 0:  # if the user didn't speak
            assistantSpeaking("I'm sorry, I couldn't understand you. Could you repeat that? ")  # call the assistantSpeaking function with an error message
            continue  # go back to the start of the loop
        
        # call the processText function with the user's input
        processText(text)

# Created by Isaac Tomeho & Ryan Kpamengan
    





