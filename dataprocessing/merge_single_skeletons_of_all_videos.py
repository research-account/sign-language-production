from os import listdir
import re
import pickle
from tqdm import tqdm
skeletons_of_all_videos = [f for f in listdir('final_keypoints_of_all_videos')]

skeletons_of_all_videos.sort(key=lambda f: int(re.sub('\D', '', f)))

final_list_of_skeletons_file = open('all_single_skeletons_of_all_videos.pickle', 'wb')

final_list_of_skeletons = []

for file_of_filtered_skeleton_of_one_video in skeletons_of_all_videos:
    # print(file_of_filtered_skeleton_of_one_video)
    print(file_of_filtered_skeleton_of_one_video)

    file = open('final_keypoints_of_all_videos/'+file_of_filtered_skeleton_of_one_video, mode='rb')
    final_keypoints_of_all_json = pickle.load(file)
    # print(final_keypoints_of_all_json)

    for final_keypoint in final_keypoints_of_all_json:
        try:
            one_skeleton = []
            one_skeleton += final_keypoint["pose_keypoints_2d"]
            one_skeleton += final_keypoint["hand_left_keypoints_2d"]
            one_skeleton += final_keypoint["hand_right_keypoints_2d"]
            one_skeleton += final_keypoint["face_keypoints_2d"][:151-len(one_skeleton)]
            # print(len(one_skeleton))
            final_list_of_skeletons.append(one_skeleton)
        except:
            print("ERROR")
            print(final_keypoint)
    file.close()

print("count of skeletons: ", len(final_list_of_skeletons))

pickle.dump(final_list_of_skeletons[1800:], final_list_of_skeletons_file)

final_list_of_skeletons_file.close()