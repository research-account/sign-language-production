import re
import os
from os import listdir
from os.path import isfile, join
video_directory = 'reduced_videos'
audio_directory = 'extracted_wav_files'
onlyfiles = [f for f in listdir(video_directory) if isfile(join(video_directory, f))]
onlyfiles.sort(key=lambda f: int(re.sub('\D', '', f)))
print(onlyfiles)
for filename in onlyfiles:
    print(f"extract from {filename}")
    actual_filename = filename.split('.')[0]
    if os.path.exists(f".//{actual_filename}.wav"):
        print("skipping")
        continue
    os.system('ffmpeg.exe -i \"./{}/{}\" -acodec pcm_s16le -ar 16000 \"./{}/{}.wav\"'.format(video_directory, filename,
                                                                                 audio_directory, actual_filename))
