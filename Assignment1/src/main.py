# Your task is to build a translation model. You have to implement and compute the following for
# both data sets (clean and web):
# 1. Phrase extraction algorithm
# f ||| e ||| freq(f) freq(e) freq(f, e)

# 2. Phrase translation probabilities
# 3. Lexical translation probabilities (KMO approach)
# 4. The resulting files of (1-3) can be combined into one single file of the form:


# file.aligned: g-e

# 0-0 1-1 1-2 2-3
# wiederaufnahme der sitzungsperiode
# resumption of the session


import numpy as np

# 1. Phrase extraction algorithm


def phrase_extraction(e, f, a):

    # english_phrases = np.array([])
    # foreign_phrases = np.array([])
    # english_freq = np.array([])
    # foreign_freq = np.array([])
    # combi_freq = np.array([])

    for i in range(len(e)):
        enlish_sentence = e[i].split()
        foreign_sentence = f[i].split()
        alignment = a[i].split()
        alignment = [x.split('-') for x in alignment]

        matrix = np.zeros((len(enlish_sentence), len(foreign_sentence)), dtype=int)

        for alig in alignment:
            matrix[int(alig[0]),int(alig[1])] = 1

        horizontal = []
        vertical = []

        for h in range(len(enlish_sentence)):
            for v in range(len(foreign_sentence)):
                if matrix[h,v] ==

with open('../data/file.en') as textfile:
    english_reader = textfile.readlines()
    with open('../data/file.de') as textfile:
        german_reader = textfile.readlines()
        with open('../data/file.aligned') as textfile:
            aligned_reader = textfile.readlines()

            phrase_extraction(german_reader, english_reader, aligned_reader)

