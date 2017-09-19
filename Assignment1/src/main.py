# Your task is to build a translation model. You have to implement and compute the following for
# both data sets (clean and web):
# 1. Phrase extraction algorithm
# f ||| e ||| freq(f) freq(e) freq(f, e)

# 2. Phrase translation probabilities
# 3. Lexical translation probabilities (KMO approach)
# 4. The resulting files of (1-3) can be combined into one single file of the form:


# file.aligned: g-e


import numpy as np

# 1. Phrase extraction algorithm

def phrase_extraction(e, f, a):
    for i in len(e):
        phrases = np.array([])
        enlish_sentence = e[i].split()
        foreign_sentence = f[i].split()
        alignment = a[i].split()

        for word in english_sentence:
            if word
            valid = True
            this_phrase = np.array([])
            while valid:
                for word in english_sentence:




with open('../data/file.en') as textfile:
    english_reader = textfile.readlines()
    with open('../data/file.de') as textfile:
        german_reader = textfile.readlines()
        with open('../data/file.aligned') as textfile:
            aligned_reader = textfile.readlines()

            phrase_extraction(english_reader, german_reader, aligned_reader)

