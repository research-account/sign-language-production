from os import listdir
import os
from extract_single_person_coordinates import extract_single_person_coordinates
folder_of_all_jsons_of_all_videos = 'raw_skeletons'
final_folder_of_all_jsons_of_all_videos = 'final_keypoints_of_all_videos'
all_json_folders = [f for f in listdir(folder_of_all_jsons_of_all_videos)]

print(all_json_folders)

for json_folder in all_json_folders:
    if os.path.exists('final_keypoints_of_all_videos/'+json_folder+'.pickle'):
        print(f"skipping: {json_folder}")
        continue
    extract_single_person_coordinates(json_folder='raw_skeletons/'+json_folder, final_keypoints_of_json_folder='final_keypoints_of_all_videos/'+json_folder+'.pickle')