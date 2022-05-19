import pickle
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import shutil
import os
import cv2
from numpy.linalg import norm
from scipy.spatial.distance import cityblock

print("loading all saved variables")
hypotheses_file = open('my_variables/hypotheses.pickle', 'rb')
hypotheses = pickle.load(hypotheses_file)

input_file = open('my_variables/inputs.pickle', 'rb')
input = pickle.load(input_file)

references_file = open('my_variables/references.pickle', 'rb')
references = pickle.load(references_file)

file_paths_file = open('my_variables/file_paths.pickle', 'rb')
file_paths = pickle.load(file_paths_file)

# display_file = open('my_variables/display.pickle', 'rb')
# display = pickle.load(display_file)

scaler = pickle.load(open('my_variables/scaler.pickle', 'rb'))

numpy_references = []
numpy_hypotheses = []

for single_hypothesis in hypotheses:
    numpy_hypotheses.append(np.array(scaler.inverse_transform(single_hypothesis.cpu()), dtype=int))

for single_reference in references:
    numpy_references.append(np.array(scaler.inverse_transform(single_reference.cpu()), dtype=int))
print("completed loading all variables")

print("generating videos...")

shutil.rmtree('videos')
os.makedirs('videos', exist_ok=True)

# video = cv2.VideoWriter('videos/test_video3.avi', cv2.VideoWriter_fourcc(*"MJPG"), 10,
#                         (1600, 800))

count_of_sentence = len(file_paths)

font = ImageFont.truetype("arial.ttf", 25)

frozen_frame = numpy_references[0][-1]

def extract_body_points(skeleton):
    body_pose = skeleton[:50]
    left_hand = skeleton[50:92]
    right_hand = skeleton[92:134]

    def extract_xy(points):
        x = []
        y = []
        for (i, point) in enumerate(points):
            if i % 2 == 0:
                x.append(point)
            else:
                y.append(point)
        return x, y

    left_hand_x, left_hand_y = extract_xy(left_hand)
    right_hand_x, right_hand_y = extract_xy(right_hand)
    body_pose_x, body_pose_y = extract_xy(body_pose)
    return (body_pose_x, body_pose_y), (left_hand_x, left_hand_y), (right_hand_x, right_hand_y)


def get_skeleton_pil_image(skeleton):
    (body_x, body_y), (left_x, left_y), (right_x, right_y) = extract_body_points(skeleton)
    img = Image.new("RGB", (800, 800), (255, 255, 255))
    img1 = ImageDraw.Draw(img)

    hand_lines = [(0, 1), (1, 2), (2, 3), (3, 4),
                  (0, 5), (5, 6), (6, 7), (7, 8),
                  (0, 9), (9, 10), (10, 11), (11, 12),
                  (0, 13), (13, 14), (14, 15), (15, 16),
                  (0, 17), (17, 18), (18, 19), (19, 20)]
    # draw left hand
    for line in hand_lines:
        img1.line([(left_x[line[0]], left_y[line[0]]), (left_x[line[1]], left_y[line[1]])], fill="red", width=3)
        img1.line([(right_x[line[0]], right_y[line[0]]), (right_x[line[1]], right_y[line[1]])], fill="blue", width=3)

    body_lines = [(0, 1),
                  (0, 15), (15, 17), (0, 16), (16, 18),
                  (1, 2), (2, 3), (3, 4),
                  (1, 5), (5, 6), (6, 7)]
    for line in body_lines:
        if body_x[line[0]] == 0 or body_y[line[0]] == 0 or body_x[line[1]] == 0 or body_y[line[1]] == 0:
            continue
        img1.line([(body_x[line[0]], body_y[line[0]]), (body_x[line[1]], body_y[line[1]])], fill="green", width=3)

    return img

cosine_similarity_50 = []
cosine_similarity_100 = []
cosine_similarity_150 = []
cosine_similarity_200 = []
cosine_similarity_250 = []
cosine_similarity_300 = []
cosine_similarity_350 = []

for index in range(count_of_sentence):
    file_name = file_paths[index]
    reference_skeletons_of_single_sentence = numpy_references[index]
    hypothesis_skeletons_of_single_sentence = numpy_hypotheses[index]
    single_sentence = input[index]

    print("generative video for " + file_name)

    count_of_skeletons = len(hypothesis_skeletons_of_single_sentence)

    print("count of skeletons in hypothesis: ", len(hypothesis_skeletons_of_single_sentence))
    print("count of skeletons in reference: ", len(reference_skeletons_of_single_sentence))
    for skeleton_index in range(
            min(len(hypothesis_skeletons_of_single_sentence), len(reference_skeletons_of_single_sentence))):

        if (frozen_frame == reference_skeletons_of_single_sentence[skeleton_index]).all():
            continue

        skeleton_A = hypothesis_skeletons_of_single_sentence[skeleton_index]
        skeleton_B = reference_skeletons_of_single_sentence[skeleton_index]

        # cosine = np.sqrt(np.sum(np.square(skeleton_A-skeleton_B)))
        # cosine = cityblock(skeleton_A, skeleton_B)
        cosine = np.dot(skeleton_A, skeleton_B) / (norm(skeleton_A) * norm(skeleton_B))

        if skeleton_index // 50 == 0:
            cosine_similarity_50.append(cosine)
        elif skeleton_index // 100 == 0:
            cosine_similarity_100.append(cosine)
        elif skeleton_index // 150 == 0:
            cosine_similarity_150.append(cosine)
        elif skeleton_index // 200 == 0:
            cosine_similarity_200.append(cosine)
        elif skeleton_index // 250 == 0:
            cosine_similarity_250.append(cosine)
        elif skeleton_index // 300 == 0:
            cosine_similarity_300.append(cosine)
        else:
            cosine_similarity_350.append(cosine)
        image_of_hypothesis = get_skeleton_pil_image(hypothesis_skeletons_of_single_sentence[skeleton_index])

        # draw_text_hypothesis = ImageDraw.Draw(image_of_hypothesis)
        # draw_text_hypothesis.text((50, 100), "Hypothesis", (255, 0, 0), font=font)

        # image_of_reference = get_skeleton_pil_image(reference_skeletons_of_single_sentence[skeleton_index])

        # draw_text_reference = ImageDraw.Draw(image_of_reference)
        # draw_text_reference.text((50, 100), "Reference", (255, 255, 0), font=font)

        # images = [image_of_hypothesis, image_of_reference]

        # new_im = Image.new('RGB', (1600, 800))
        # x_offset = 0
        # for im in images:
        #     new_im.paste(im, (x_offset, 0))
        #     x_offset += im.size[0]

        # draw_text_joined = ImageDraw.Draw(new_im)

        # sentence = " ".join(single_sentence).lower()
        # sentence = sentence.replace("<pad>", "")
        # sentence = sentence.replace("</s>", "")
        # draw_text_joined.text((100, 600), sentence, (255, 0, 0), font=font)

        # open_cv_image = np.array(new_im)
        # open_cv_image = open_cv_image[:, :, ::-1].copy()
        # video.write(cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR))
# video.release()

if not len(cosine_similarity_50) == 0:
    print(np.mean(cosine_similarity_50))
if not len(cosine_similarity_100) == 0:
    print(np.mean(cosine_similarity_100))
if not len(cosine_similarity_150) == 0:
    print(np.mean(cosine_similarity_150))
if not len(cosine_similarity_200) == 0:
    print(np.mean(cosine_similarity_200))
if not len(cosine_similarity_250) == 0:
    print(np.mean(cosine_similarity_250))
if not len(cosine_similarity_300) == 0:
    print(np.mean(cosine_similarity_300))
if not len(cosine_similarity_350) == 0:
    print(np.mean(cosine_similarity_350))

print(len(cosine_similarity_50))
print(len(cosine_similarity_100))
print(len(cosine_similarity_150))
print(len(cosine_similarity_200))
print(len(cosine_similarity_250))
print(len(cosine_similarity_300))
print(len(cosine_similarity_350))
