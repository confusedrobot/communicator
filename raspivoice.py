# Algorithm A:

# Pi would continuously record audio, no analysis.
# If the wearable computer is switched into typing mode, Sphinx is launched to analyze the few most recent seconds of recording.
# The algo suggests a phrase, if possible.
# If the user does not use the phrase and types something else instead, the audio recording and 
# the new phrase are saved to be later added to the dictionary.

# Maybe: recommended segment length (some people experienced problems with Google Speech API when sending more than 30 sec at a time)
# segment_length = 30


import os
import time
import glob
import pyaudio
import speech_recognition as sr
from time import gmtime, strftime
from sphinxbase import sphinxbase
from pocketsphinx import pocketsphinx

def RecognizeSpeech(myaudio):
    start_time = time.time()
    # recognize speech using Sphinx
    try:
        audiotext = r.recognize_sphinx(myaudio)
        print("Sphinx thinks you said:" + audiotext)
        end_time = time.time()
        print("run time:", end_time - start_time)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio.")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


def GetLatestOne():
    files = glob.glob('audio/*.wav')
    latestfile = max(files , key = os.path.getctime)
    return latestfile

def GetLatestThree():
    path = 'audio/*.wav'
    files = sorted(os.listdir(path), key=os.path.getctime)
    oldest = files[0]
    newest = files[-1]
    return newest


i = 0

while True:

    audiofilename = strftime("%Y%m%d_%H%M%S", gmtime()) + ".wav"

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise ...")
        r.adjust_for_ambient_noise(source)
        print("Listening ...")
        audio = r.listen(source)

    # write captured audio segment to a WAV file
    with open("audio/" + audiofilename, "wb") as f:
        print("Saving audio to ", "audio/" + audiofilename)
        f.write(audio.get_wav_data())

    if i == 2:
        break
    else:
        i = i + 1


currentaudio = GetLatestOne()

print("Most recent file: ", currentaudio)

print("Analyzing audio in the file ... ")


fromfile = sr.AudioFile(currentaudio)
with fromfile as source:
    audio_2 = r.record(source)

RecognizeSpeech(audio_2)









