import string
import re
from nltk.corpus import stopwords
from os import listdir
from os.path import isfile, join
import numpy as np
import pickle
from tqdm import tqdm
stop_words = set(stopwords.words('english'))

keypoint_directory = 'final_keypoints_of_all_videos'
keypoint_files = [f for f in listdir(keypoint_directory) if isfile(join(keypoint_directory, f))]
keypoint_files.sort(key=lambda f: int(re.sub('\D', '', f)))

text_directory = 'text_transcriptions'

whole_text = ''
print("reading all files")
for keypoint_file in tqdm(keypoint_files):
    file = open(text_directory+'\\'+keypoint_file.split('.')[0]+'.txt', mode='r')
    all_of_it = file.read()
    all_of_it = all_of_it.strip()
    whole_text += all_of_it+'.'
    file.close()

whole_text = ' '.join(whole_text.split())

whole_text = whole_text.lower()

whole_text = whole_text.replace('?', ' ENDOFSENTENCE ')
whole_text = whole_text.replace('.', ' ENDOFSENTENCE ')
whole_text = whole_text.translate(str.maketrans('', '', string.punctuation)).upper()

for stopword in stop_words:
    whole_text = whole_text.replace(" "+stopword+" ", ' ')

sentences = whole_text.strip().split('ENDOFSENTENCE')

stripped_sentences = []
for sentence in tqdm(sentences):
    clean_sentence = ' '.join(sentence.split())
    if not len(clean_sentence) < 5:
        stripped_sentences.append(clean_sentence)

sentences = stripped_sentences

print("COUNT OF SENTENCES: ", len(sentences))

all_sentences_file = open('all_sentences.txt', 'w')
for sentence in sentences:
    print(sentence, file=all_sentences_file)
all_sentences_file.close()

tokens_of_sentences = []

sentence_lengths = []

token_counts_of_all_sentences = []

unique_tokens = []
print("tokenize sentences")
for i, sentence in tqdm(enumerate(sentences)):
    sentence_lengths.append(len(sentence))
    tokens_of_one_sentence = sentence.strip().split(' ')
    filtered_tokens = []
    for unfiltered_one_token in tokens_of_one_sentence:
        filtered_tokens.append(unfiltered_one_token)
        if unfiltered_one_token not in unique_tokens:
            unique_tokens.append(unfiltered_one_token)

    tokens_of_sentences.append(filtered_tokens)
    token_counts_of_all_sentences.append(len(filtered_tokens))

print("sum of characters: ", np.sum(sentence_lengths))
# print(sentence_lengths)


sentence_lengths_cumulative = np.zeros((len(sentence_lengths)), dtype=int)
for i in tqdm(range(len(sentence_lengths))):
    for j in range(i,len(sentence_lengths)):
        sentence_lengths_cumulative[j] += sentence_lengths[i]
print("sentence length cumulative: ", sentence_lengths_cumulative)
sentence_lengths_cumulative_file = open('sentence_lengths_cumulative.pickle', 'wb')
pickle.dump(sentence_lengths_cumulative, sentence_lengths_cumulative_file)
print('len(sentence_lengths_cumulative): '+str(len(sentence_lengths_cumulative)))

print("max token in sentence: ", np.max(token_counts_of_all_sentences))
print("average token count per sentence: ", np.average(token_counts_of_all_sentences))
print("len(tokens_of_sentences): ", len(tokens_of_sentences))

gloss_file = open('data.gloss', mode='w')

print("writing data.gloss")
for i, filtered_tokens_of_one_sentence in tqdm(enumerate(tokens_of_sentences)):
    if len(filtered_tokens_of_one_sentence) == 0:
        print("FATAL error")
        exit(0)
    print(" ".join(filtered_tokens_of_one_sentence), file=gloss_file)

gloss_file.close()

src_vocab_file = open('src_vocab.txt', 'w')
print('<unk>',file=src_vocab_file)
print('<pad>', file=src_vocab_file)
print('<s>', file = src_vocab_file)
print('</s>', file = src_vocab_file)
print("\n".join(unique_tokens), file=src_vocab_file)