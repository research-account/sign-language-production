from pydub import AudioSegment
from os import listdir
from os.path import isfile, join

startMin = 3
startSec = 0

# Time to miliseconds
startTime = startMin*60*1000+startSec*1000

# Opening file and extracting segment
audio_directory = 'extracted_wav_files'
untrimmed_audio_files = [f for f in listdir(audio_directory) if isfile(join(audio_directory, f))]

for untrimmed_audio_file in untrimmed_audio_files:
    print("trimming: "+untrimmed_audio_file)
    file_name = untrimmed_audio_file.split('.')[0]
    if not len(untrimmed_audio_file.split('.')) == 2:
        print("fatal error. exit")
        exit(1)
    song = AudioSegment.from_wav(audio_directory+"/"+untrimmed_audio_file)
    extract = song[startTime:]
    extract.export("trimmed_audios/"+untrimmed_audio_file+'.wav', format="wav")