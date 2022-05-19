from os import listdir
from os.path import isfile, join
from pydub import AudioSegment
from tqdm import tqdm

audio_directory = 'extracted_wav_files'
untrimmed_audio_files = [f for f in listdir(audio_directory) if isfile(join(audio_directory, f))]
# total minute: 5833
total_seconds = 0
for untrimmed_audio_file in tqdm(untrimmed_audio_files):
    file_name = untrimmed_audio_file.split('.')[0]
    song = AudioSegment.from_wav(audio_directory+"/"+untrimmed_audio_file)
    total_seconds += song.duration_seconds

print("total minutes: ", total_seconds/60)