from phrase_extraction import phrase_extraction
from phrase_extraction import alignstowords
import codecs
import time
from collections import defaultdict , Counter
from operator import div
import pickle



if __name__=='__main__':
    # todo: put path for data and go from there
    en_filepath = '../../Assignment1/data/file.en'
    de_filepath = '../../Assignment1/data/file.de'
    align_filepath = '../../Assignment1/data/file.aligned'

    # max phrase length
    max_phrase_len = 7

    # file objects
    f_en = codecs.open(en_filepath, 'rb', encoding='utf-8')
    f_de = codecs.open(de_filepath, 'rb', encoding='utf-8')
    f_align = open(align_filepath, 'rb')


    for i, line_en in enumerate(f_en):
            if (i+1) % 10 == 0:
                print ('line no: ', i+1)
            line_de = f_de.readline()
            line_align = f_align.readline()
            phrases_str, phrases, data_alignments, de_alignment_dict, en_alignment_dict, phrases_begin, phrases_end = phrase_extraction(line_en, line_de, line_align, max_phrase_len)