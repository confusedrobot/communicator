import os
import time
import glob
import pyaudio
import speech_recognition as sr
from time import gmtime, strftime
from sphinxbase import sphinxbase
from pocketsphinx import pocketsphinx

# use natural language toolkit
import nltk
from nltk.stem.lancaster import LancasterStemmer


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

def RecognizeSpeechGoogle(myaudio):
    # recognize speech using Google Speech
    try: 
        text = r.recognize_google(myaudio) 
        print("Google thinks you said: " + text) 

    except sr.UnknownValueError: 
        print("Google Speech Recognition could not understand audio") 
      
    except sr.RequestError as e: 
        print("Could not request results from Google Speech Recognition service; {0}".format(e)) 




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


r = sr.Recognizer()

currentaudio = GetLatestOne()

print("Most recent file: ", currentaudio)
print("Analyzing audio in the file ... ")


fromfile = sr.AudioFile(currentaudio)
with fromfile as source:
    audio_2 = r.record(source)

#RecognizeSpeech(audio_2)
RecognizeSpeechGoogle(audio_2)

# do some NLP
# word stemmer
stemmer = LancasterStemmer()

# 3 classes of training data
training_data = []
training_data.append({"class":"hello", "sentence":"how are you?"})
training_data.append({"class":"hello", "sentence":"how is your day?"})
training_data.append({"class":"hello", "sentence":"how are you doing today?"})
training_data.append({"class":"hello", "sentence":"how is it going today?"})

training_data.append({"class":"goodbye", "sentence":"have a nice day"})
training_data.append({"class":"goodbye", "sentence":"see you later"})
training_data.append({"class":"goodbye", "sentence":"have a nice day"})
training_data.append({"class":"goodbye", "sentence":"talk to you soon"})

training_data.append({"class":"food", "sentence":"what do you want for dinner?"})
training_data.append({"class":"food", "sentence":"do you like pizza?"})
training_data.append({"class":"food", "sentence":"having a sandwich today?"})
training_data.append({"class":"food", "sentence":"what's for lunch?"})
print ("%s sentences of training data" % len(training_data))

# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
print ("Class words: %s" % class_words)


# calculate a score for a given class
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with same weight
            score += 1
            
            if show_details:
                print ("   match: %s" % stemmer.stem(word.lower() ))
    return score



# we can now calculate a score for a new sentence
sentence = "where do you want to go for lunch?"

# now we can find the class with the highest score
for c in class_words.keys():
    print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))



