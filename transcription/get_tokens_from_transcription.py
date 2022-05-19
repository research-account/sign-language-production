import string
import re
from nltk.corpus import stopwords
from os import listdir
from os.path import isfile, join
import numpy as np
import pickle

text_directory = 'transcripts'
text_files = [f for f in listdir(text_directory) if isfile(join(text_directory, f))]
text_files.sort(key=lambda f: int(re.sub('\D', '', f)))

whole_text = ''
for text_file in text_files:
    file = open(text_directory + '\\' + text_file, mode='r')
    all_of_it = file.read()
    whole_text += all_of_it + ' '
    file.close()

# print("whole text: ")
# print(whole_text)
# print("_"*50)

length_of_text = len(whole_text)
whole_text_with_EOF = ''
for i in range(len(whole_text)):
    # print(whole_text[i], end='')
    if i + 2 < length_of_text and whole_text[i] == '.' and re.search("[A-Z1-9]", whole_text[i + 2]) is not None:
        whole_text_with_EOF += ' ENDOFSENTENCE'
    else:
        whole_text_with_EOF += whole_text[i]

whole_text_with_EOF = whole_text_with_EOF.replace('?', ' ENDOFSENTENCE')
#
# for (i, sentence) in enumerate(whole_text_with_EOF.split('ENDOFSENTENCE')):
#     print(i,sentence)

whole_text_without_punctuation = whole_text_with_EOF.translate(str.maketrans('', '', string.punctuation)).upper()

# for (i, sentence) in enumerate(whole_text_without_punctuation.split('ENDOFSENTENCE')):
#     print(i,sentence)

sentences = whole_text_without_punctuation.strip().split('ENDOFSENTENCE')
print('individual sentences')
# print(sentences)
print("COUNT OF SENTENCES: ", len(sentences))
tokens_of_sentences = []
stop_words = set(stopwords.words('english'))
sentence_lengths = []

token_counts_of_all_sentences = []

unique_tokens = []
for i, sentence in enumerate(sentences):
    # print(i, 'len: ', len(sentence), sentence)
    sentence_lengths.append(len(sentence))
    tokens_of_one_sentence = sentence.strip().split(' ')
    filtered_tokens = []
    for unfiltered_one_token in tokens_of_one_sentence:
        if unfiltered_one_token.lower() not in stop_words:
            filtered_tokens.append(unfiltered_one_token)
            if unfiltered_one_token not in unique_tokens:
                unique_tokens.append(unfiltered_one_token)

    tokens_of_sentences.append(filtered_tokens)
    token_counts_of_all_sentences.append(len(filtered_tokens))

# for i, filtered_tokens_of_one_sentence in enumerate(tokens_of_sentences):
#     print(i, filtered_tokens_of_one_sentence)

print("sum of characters: ", np.sum(sentence_lengths))
print(sentence_lengths)
sentence_lengths_cumulative = np.zeros((len(sentence_lengths)), dtype=int)
for i in range(len(sentence_lengths)):
    for j in range(i, len(sentence_lengths)):
        sentence_lengths_cumulative[j] += sentence_lengths[i]

print("sentence length cumulative: ", sentence_lengths_cumulative)

# print("breakpoints: ", np.array(sentence_lengths_cumulative*1200*len(text_files)/np.sum(sentence_lengths), dtype=int))

# frame_counts_for_each_video = np.array((np.array(sentence_lengths, dtype=int)*1200*len(text_files)) / np.sum(sentence_lengths), dtype=int)

# print("frame counts for each video: ", frame_counts_for_each_video)
# print("max frame: ", np.max(frame_counts_for_each_video))
# print("average frame per sentence: ", np.average(frame_counts_for_each_video))
print("max token in sentence: ", np.max(token_counts_of_all_sentences))
print("average token count per sentence: ", np.average(token_counts_of_all_sentences))

print("len(tokens_of_sentences): ", len(tokens_of_sentences))

gloss_file = open('data.gloss', mode='w')
for i, filtered_tokens_of_one_sentence in enumerate(tokens_of_sentences):
    print(" ".join(filtered_tokens_of_one_sentence).replace("\n", " "), file=gloss_file)

gloss_file.close()

sentence_lengths_cumulative_file = open('sentence_lengths_cumulative.pickle', 'wb')

# source, destination
pickle.dump(sentence_lengths_cumulative, sentence_lengths_cumulative_file)
print('len(sentence_lengths_cumulative): ' + str(len(sentence_lengths_cumulative)))

src_vocab_file = open('src_vocab.txt', 'w')
print('<unk>', file=src_vocab_file)
print('<pad>', file=src_vocab_file)
print('<s>', file=src_vocab_file)
print('</s>', file=src_vocab_file)
print("\n".join(unique_tokens), file=src_vocab_file)
