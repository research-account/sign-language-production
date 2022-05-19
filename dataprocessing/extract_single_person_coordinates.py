import json
import re
from os import listdir
from os.path import isfile, join
import sys
import pickle
from tqdm import tqdm

last_seen_attributes = None

def extract_single_person_coordinates(json_folder, final_keypoints_of_json_folder):
    concerned_properties_of_person = ["pose_keypoints_2d", "hand_left_keypoints_2d",
                                       "hand_right_keypoints_2d", "face_keypoints_2d"]

    print("processing json folder: "+final_keypoints_of_json_folder)


    final_keypoints_of_all_json = []
    all_json_files = [f for f in listdir(json_folder) if isfile(join(json_folder, f))]
    all_json_files.sort(key=lambda f: int(re.sub('\D', '', f)))
    frame_without_person = 0



    for file_name in tqdm(all_json_files):
        f = open(json_folder + '/' + file_name)
        data = json.load(f)
        people = data['people']
        if len(people) == 0:
            # print("\nperson not found in " + file_name)
            frame_without_person = frame_without_person + 1
            final_keypoints_of_all_json.append(last_seen_attributes)
            continue
        max_sum_of_confidence = 0
        person_with_max_confidence = None

        for single_person in people:
            sum_of_confidence = 0
            for concerned_key in concerned_properties_of_person:
                array_of_one_attribute = single_person[concerned_key]
                for x in range(2, len(array_of_one_attribute), 3):
                    sum_of_confidence = sum_of_confidence + array_of_one_attribute[x]
            if sum_of_confidence > max_sum_of_confidence:
                max_sum_of_confidence = sum_of_confidence
                person_with_max_confidence = single_person

        attributes_of_one_person_from_json = {}
        for concerned_key in concerned_properties_of_person:
            list_of_values_of_property_without_confidence = []
            list_with_confidences = person_with_max_confidence[concerned_key]
            for i in range(len(list_with_confidences)):
                if not i % 3 == 2:
                    list_of_values_of_property_without_confidence.append(list_with_confidences[i])
            attributes_of_one_person_from_json[concerned_key] = list_of_values_of_property_without_confidence

        attributes_of_one_person_from_json["face_keypoints_2d"] = attributes_of_one_person_from_json["face_keypoints_2d"][:43]

        final_keypoints_of_all_json.append(attributes_of_one_person_from_json)
        last_seen_attributes = attributes_of_one_person_from_json

        f.close()

    file_of_final_keypoints_of_all_json = open(final_keypoints_of_json_folder, 'wb')
    pickle.dump(final_keypoints_of_all_json,file_of_final_keypoints_of_all_json)
    print("skeleton not found on " + str(frame_without_person) + ' frames')
