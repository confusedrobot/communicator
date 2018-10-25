import time
import speech_recognition as sr

import os
from pocketsphinx import pocketsphinx
from sphinxbase import sphinxbase
import pyaudio


start_time = time.time()
print("Step 1: recognizing free-form speech.")

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    end_time = time.time()
    print("run time:", end_time - start_time)
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))


start_time = time.time()
print("Step 2: recognizing pre-defined phrases.")