import zipfile
import shutil
import os
from os import listdir
from os.path import isfile, join
import re

zip_directory = 'raw_skeletons_zip'
zip_files = [f for f in listdir(zip_directory) if isfile(join(zip_directory, f))]
zip_files.sort(key=lambda f: int(re.sub('\D', '', f)))

for zip_file in zip_files:
    video_name = zip_file.split('.')[0]
    print(video_name)
    shutil.rmtree('raw_skeletons/'+video_name, ignore_errors=True)
    os.makedirs('raw_skeletons/'+video_name, exist_ok=True)

    with zipfile.ZipFile('raw_skeletons_zip/'+zip_file, 'r') as zip_ref:
        zip_ref.extractall('raw_skeletons/'+video_name)

