import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

sentence_lengths_cumulative_file = open('sentence_lengths_cumulative.pickle', 'rb')
sentence_lengths_cumulative = pickle.load(sentence_lengths_cumulative_file)
print("sentence count: ", len(sentence_lengths_cumulative))

final_list_of_skeletons_file = open('all_single_skeletons_of_all_videos.pickle', 'rb')

final_list_of_skeletons = pickle.load(final_list_of_skeletons_file)

count_of_skeletons = len(final_list_of_skeletons)
print("checking skeleton names")
for one_skeleton in final_list_of_skeletons:
    if not len(one_skeleton) == 151:
        print("Invalid found")
print("finished checking skeleton name")

final_list_of_skeletons = np.array(final_list_of_skeletons, dtype=float)

print(final_list_of_skeletons.shape)

scaler = StandardScaler()
scaler.fit(final_list_of_skeletons)

scaler_file = open('scaler.pickle','wb')
pickle.dump(scaler, scaler_file)

final_list_of_skeletons = scaler.transform(final_list_of_skeletons)

data_skeletons = open('data.skels', 'w')

sentence_lengths_cumulative = np.insert(sentence_lengths_cumulative, 0, 0, axis=0)
total_sentence_length_of_video = sentence_lengths_cumulative[-1]
print("distributing skeletons")
for i in range(1, len(sentence_lengths_cumulative)):
    print(i)
    start_of_skeletons = int((sentence_lengths_cumulative[i-1]/total_sentence_length_of_video)*count_of_skeletons)
    end_of_skeletons = int((sentence_lengths_cumulative[i]/total_sentence_length_of_video)*count_of_skeletons)
    skeletons_of_one_sentence = final_list_of_skeletons[start_of_skeletons:end_of_skeletons]
    skeleton_numbers_of_one_sentence = []
    for single_skeleton in skeletons_of_one_sentence:
        for single_coordinate in single_skeleton:
            skeleton_numbers_of_one_sentence.append("{:.5f}".format(single_coordinate))

    print(" ".join(skeleton_numbers_of_one_sentence), file=data_skeletons)

print(final_list_of_skeletons.shape)

data_skeletons.close()

