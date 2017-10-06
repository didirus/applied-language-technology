from phrase_extraction import phrase_extraction
from phrase_extraction import alignstowords
import codecs
import time
from collections import defaultdict, Counter
from operator import div
import pickle



def create_orientation_histograms(orientations):

    


f_phrase = open('phrase_result.txt', 'rb')
f_word = open('word_result.txt', 'rb')


create_orientation_histograms(['swap', 'discontinuity', 'monotone'])


f_phrase.close()
f_word.close()