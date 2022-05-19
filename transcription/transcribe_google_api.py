from google.cloud import speech_v1 as speech
import os
from os import listdir
from os.path import isfile, join
import io
import re
from os.path import exists
import urllib.parse

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

client = speech.SpeechClient()


def speech_to_text(config, audio, file_name):
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result()
    print_sentences(response, file_name)


def print_sentences(response, file_name):
    sentence = ""
    file = open('transcripts/' + file_name + '.wav.txt', 'w')
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print("-" * 80)
        sentence += transcript+" "
        print(f"{transcript}")
        print(f"Confidence: {confidence:.0%}")
    sentence = sentence.replace("\n", ".")
    print(sentence, file=file)
    file.close()


config = dict(language_code="en-US", audio_channel_count=2)
config.update(dict(enable_automatic_punctuation=True))

video_directory = 'D:\\thesis\\reduced_videos'
video_files = [f for f in listdir(video_directory) if isfile(join(video_directory, f))]
video_files.sort(key=lambda f: int(re.sub('\D', '', f)))

for video_file in video_files:
    video_name = video_file.split('.')[0]
    print(video_name)
    if exists('transcripts/' + video_name + '.wav.txt'):
        print("skipping transcription of " + video_name)
        continue
    speech_to_text(config, dict(uri="gs://signthesis/wav_data/"+video_name+".wav.wav"),
                   video_name)