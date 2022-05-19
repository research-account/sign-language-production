import zipfile
import shutil
import os
from os import listdir
from os.path import isfile, join
import re

# shutil.rmtree('extracted_folders', ignore_errors=True)
# os.makedirs('extracted_folders', exist_ok=True)

zip_directory = 'zip_files'
zip_files = [f for f in listdir(zip_directory) if isfile(join(zip_directory, f))]
zip_files.sort(key=lambda f: int(re.sub('\D', '', f)))

for zip_file in zip_files:
    video_name = zip_file.split('.')[0]
    print(video_name)
    shutil.copyfile('removed_background_audios/'+video_name+'.wav', 'final_audios_selected/'+video_name+'.wav')
    # shutil.rmtree('extracted_folders/'+video_name, ignore_errors=True)
    # os.makedirs('extracted_folders/'+video_name, exist_ok=True)
    #
    # with zipfile.ZipFile('zip_files/'+zip_file, 'r') as zip_ref:
    #     zip_ref.extractall('extracted_folders/'+video_name)

