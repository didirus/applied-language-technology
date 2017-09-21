import numpy as np

# 1. Phrase extraction algorithm


def phrase_extraction(e, f, a):

    # english_phrases = np.array(['resumption', ])
    # foreign_phrases = np.array([reskjslf])
    # english_freq = np.array([2342])
    # foreign_freq = np.array([23421])
    # combi_freq = np.array([251])

    for i in range(len(e)):
        enlish_sentence = e[i].split()
        foreign_sentence = f[i].split()
        alignment = a[i].split()
        alignment = [x.split('-') for x in alignment]

        matrix = np.zeros((len(enlish_sentence), len(foreign_sentence)), dtype=int)

        for alig in alignment:
            matrix[int(alig[0]),int(alig[1])] = 1
        print('oi')
        # horizontal = []
        # vertical = []
        #
        # for h in range(len(enlish_sentence)):
        #     for v in range(len(foreign_sentence)):
        #         if matrix[h,v] ==