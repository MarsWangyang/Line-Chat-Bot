# -*- coding: utf-8 -*-

import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow
import random
import json
import pickle
nltk.download('punkt')

stemmer = LancasterStemmer()

path = './intents.json'
with open(path, 'r') as f:
    data = json.load(f)

#try:
with open('data.pickle', 'rb') as file:
    words, labels, training, output = pickle.load(file)

# except:
#
#     words = []
#     labels = []
#     docs_x = []
#     docs_y = []
#
#     for intent in data['intents']:
#         for pattern in intent['patterns']:
#             wrds = nltk.word_tokenize(pattern)  # 斷詞
#             words.extend(wrds)
#             docs_x.append(wrds)
#             docs_y.append(intent['tag'])
#
#         if intent['tag'] not in labels:
#             labels.append(intent['tag'])
#
#     words = [stemmer.stem(w.lower()) for w in words if w != '?']
#     words = sorted(list(set(words)))
#     labels = sorted(labels)
#
#     training = []
#     output = []
#
#     out_empty = [0 for _ in range(len(labels))]
#
#     for x, doc in enumerate(docs_x):
#         bag = []
#         letters = [stemmer.stem(w) for w in doc]
#
#         for l in words:
#             if l in letters:
#                 bag.append(1)
#             else:
#                 bag.append(0)
#
#         output_row = out_empty[:]
#         output_row[labels.index(docs_y[x])] = 1
#
#         training.append(bag)
#         output.append(output_row)
#     training = np.array(training)  # (46,)
#     output = np.array(output)  # (26, 6)
#     print(output.shape)
#
#     with open('data.pickle', 'wb') as file:
#         pickle.dump((words, labels, training, output), file)

#from tensorflow.python.framework import ops

#ops.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)

#try:
model.load('model.tflearn')
#except:
#model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
#model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return np.array(bag)


def chat(msg):
    results = model.predict([bag_of_words(msg, words)])[0]
    results_index = np.argmax(results)
    tag = labels[results_index]
    print(results)

    if results[results_index] > 0.7:
        for tg in data['intents']:
            if tg['tag'] == tag:
                responses = tg['responses']
        return random.choice(responses)

    else:
        return "I didn't get that, please try again."
