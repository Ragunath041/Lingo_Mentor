import openai
import pyttsx3
import speech_recognition as sr
import json
def rec():
    init_rec = sr.Recognizer()
    print("Let's speak!!")
    with sr.Microphone() as source:
        init_rec.adjust_for_ambient_noise(source)  
        audio_data = init_rec.listen(source)  
        print("Recognizing your text.............")
        try:
            text = init_rec.recognize_google(audio_data)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return None
        except sr.RequestError as e:
            print("Sorry, my speech recognition service is not available. Error:", e)
            return None


def maleVoice(text):
    print("Assistant : "+text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 25)  
    engine.say(text)
    engine.runAndWait()

openai.api_key = "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"
messages = [{"role": "system", "content": "Conversation with English Professor"}]

while True:
    user_input = rec() 
    if user_input:
        messages.append({"role": "user", "content": user_input})
        if user_input.lower() in ["thank you", "thankyou", "stop"]:
            with open("conversation_history.json", "w") as file:
                json.dump(messages, file, indent=4)
            print("Conversation ended. Conversation history saved to conversation_history.json")
            break
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages) 
        reply = response["choices"][0]["message"]["content"]
        maleVoice(reply)  
        messages.append({"role": "assistant", "content": reply})
