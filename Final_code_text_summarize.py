# You have to add the location of audio file path in "path" at line number 9 and make sure that it path have backslash


import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
r=sr.Recognizer()
path="D:/ytmp3free (mp3cut.net).wav"
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

def makesummary(text):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm') 
    doc = nlp(text) 
    tokens = [token.text for token in doc]
    punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n'

    word_fq = {}
    for word in  doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_fq.keys():
                    word_fq[word.text] = 1
                else:
                    word_fq[word.text]+=1

                    
    max_fq = max(word_fq.values())
    for word in word_fq.keys():
            word_fq[word] = word_fq[word]/max_fq
            
            
    s_tokens = [sent for sent in doc.sents]

    s_score = {}
    for sent in s_tokens:
        for word in sent:
            if word.text.lower() in word_fq.keys():
                if sent not in s_score.keys():
                    s_score[sent]= word_fq[word.text.lower()]
                else:
                    s_score[sent]+= word_fq[word.text.lower()]
                    

    s_length = int(len(s_tokens)*0.2)
    summary = nlargest(s_length,s_score,key =s_score.get)
    f_sum = [word.text for word in summary]
    summary = " ".join(f_sum)
    return summary
    
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 1500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=1500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "

                whole_text += text
    # return the text for all chunks detected
#     print(type(text))
    return whole_text

text = get_large_audio_transcription(path)
final = makesummary(text)
final_len = len(final.split( ))
text_len = len(text.split( ))
print(final)
print("Text Word Count: ",(text_len))
print("Summary Word Count:",(final_len))
