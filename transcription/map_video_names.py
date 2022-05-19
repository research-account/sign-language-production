import os
with open('video_file_map_file.txt',mode="r", encoding="utf-8") as file:
    lines = file.readlines()
    lines = [line.rstrip().split('|||||') for line in lines]

print(lines)

for line in lines:
    video_name = line[0].split('.')[0]
    map_video_name = line[1].split('.')[0]
    os.rename('transcripts/'+video_name+'.wav.txt', 'transcripts/'+map_video_name+'.txt')
