from phrase_extraction import phrase_extraction
from phrase_extraction import alignstowords
import codecs
import time
import sys
from collections import defaultdict
from collections import Counter
from operator import div
import pickle
if __name__=='__main__':
    # todo: put path for data and go from there
    en_filepath = '.en'
    de_filepath = '.de'
    align_filepath = '.aligned'