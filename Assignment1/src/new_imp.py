
import codecs
from collections import Counter
import time
from collections import defaultdict
from time import sleep
import sys


def check1(de_pos, en_pos, en_alignment_dict):
    '''
    check if no English words in the phrase pair are aligned to words outside it
    :return: t/f if it satisfies the condition
    '''

    check = True
    min_one = False

    # alignments related with en positions
    for en in en_pos:
        # de positions related with the english word
        for a in en_alignment_dict[en]:
            min_one = True
            check = check and (True if a in de_pos else False)

    return check and min_one

def check2(de_pos, en_pos, de_alignment_dict):
    '''
    check that no foreign words in the phrase pair are aligned to words outside it
    :return: t/f it satisfies the condition
    '''

    check = True
    min_one = False

    # alignments associated with en positions
    for de in de_pos:
        for a in de_alignment_dict[de]:
            min_one = True
            check = check and (True if a in en_pos else False)

    return check and min_one

def alignstowords(positions, de_line, en_line):
    '''
    converter function numbers to words
    '''

    return (' '.join(map(de_line.__getitem__, positions[0])), ' '.join(map(en_line.__getitem__, positions[1])))

def update_word_count(de_line, en_line):
    '''
    updates word counts. Used to compute lexical probabilities.
    '''
    # global arguments can use it anywhere after this
    global de_word_freq
    global en_word_freq
    global joint_word_freq
    global en_alignment_dict

    # aligned deutsch words
    de_aligned_total = set()

    for e_w_idx, en_word in enumerate(en_line):
        en_word_freq[en_word] += 1

        for d_w_idx in en_alignment_dict[e_w_idx]:
            de_word_freq[de_line[d_w_idx]] += 1
            joint_word_freq[(de_line[d_w_idx], en_word)] += 1

        if not en_alignment_dict[e_w_idx]:
            # aligned to NiL
            joint_word_freq[(nil, en_word)] += 1
            de_word_freq[nil] += 1

        de_aligned_total = de_aligned_total.union(en_alignment_dict[e_w_idx])

    for d_w_idx in set(range(len(de_line))).difference(de_aligned_total):
        en_word_freq[nil] += 1
        joint_word_freq[(de_line[d_w_idx], nil)] += 1

    return




def update_phrase_counts(de_phrase_str, en_phrase_str):
    '''
    updates word and phrase counts
    '''
    # global arguments can use it anywhere after this
    global joint_freq
    global de_freq
    global en_freq

    t = (de_phrase_str, en_phrase_str)
    joint_freq[t] += 1
    de_freq[de_phrase_str] += 1
    en_freq[en_phrase_str] += 1

    return

# TODO prob function
def translation_probs(t):
    p_f_e = joint_freq[t] / float(en_freq[en_phrase_str])
    p_e_f = joint_freq[t] / float(de_freq[de_phrase_str])

    return (p_f_e, p_e_f)



# TODO Lex prob function



if __name__ == '__main__':

    start = time.time()

    # debug file paths
    en_filepath = '../data/file.en'
    de_candilepath = '../data/file.de'
    align_filepath = '../data/file.aligned'

    # max phrase length
    max_phrase_len = 5

    # file objects codecs open cos. having problem in py2.7
    f_en = codecs.open(en_filepath, 'rb', encoding='utf-8')
    f_de = codecs.open(de_candilepath, 'rb', encoding='utf-8')
    f_align = open(align_filepath, 'rb')

    phrases = []
    phrases_str = set()
    data_alignments = dict()


    # w counters
    de_word_freq = Counter()
    en_word_freq = Counter()
    joint_word_freq = Counter()

    # ph counters
    joint_freq = Counter()
    de_freq = Counter()
    en_freq = Counter()



    # NiL word
    nil = '#NiL#'

    data_alignments = defaultdict(list)
    count__ = 0
    print 'Extract phrase pairs'
    for line in f_en:
        # print (line)
        # read english line
        en_line = line.strip().split() # whitespace tokenization

        # read germ line
        de_line = f_de.readline().strip().split()

        en_alignment_dict = defaultdict(list)
        de_alignment_dict = defaultdict(list)

        for de_a,en_a in map(lambda x:x.split('-'),f_align.readline().strip().split()):
            de_alignment_dict[int(de_a)].append(int(en_a))
            en_alignment_dict[int(en_a)].append(int(de_a))

        update_word_count(de_line, en_line)

        # all possible germ phrases
        de_cand_phrases = [range(i,i+j+1) for i,_ in enumerate(de_line) \
                                for j in range(min([len(de_line), max_phrase_len, len(de_line)-i]))]
        # print (de_cand_phrases)
        # all possible en phrases
        en_cand_phrases = [range(i,i+j+1) for i,_ in enumerate(en_line) \
                                for j in range(min([len(en_line), max_phrase_len, len(en_line)-i]))]
        # print (en_cand_phrases)
        # sleep(5)

        for en_cand in en_cand_phrases:
            for de_cand in de_cand_phrases:
                if check1(de_cand, en_cand, en_alignment_dict) and check2(de_cand, en_cand, de_alignment_dict):

                    translation = alignstowords((de_cand, en_cand), de_line, en_line)

                    if translation not in phrases_str:
                        phrases_str.add(translation)
                        phrases.append((de_cand,en_cand))

                    de_phrase_alignments = {pos: de_alignment_dict[pos] for pos in de_cand}
                    en_phrase_alignments = {pos: en_alignment_dict[pos] for pos in en_cand}
                    # print (de_phrase_alignments)
                    # print (en_phrase_alignments)
                    # sleep(5)
                    data_alignments[(translation[0], translation[1])].append((de_phrase_alignments, en_phrase_alignments))
                    update_phrase_counts(translation[0], translation[1])
                    # print (data_alignments)
                    # sleep(5)

        count__+=1

        if (count__%100) == 0:
            # print (phrases)
            # sleep(10)
            # print (phrases_str)
            # sleep(10)
            # print (data_alignments)
            # sleep(10)
            # break

            print (count__)


    print('time:', time.time()-start)
    # sleep(5)
    # print (len(phrases))
    # sleep(5)
    # print (phrases_str)

    # # lexical probabilities
    word_probs = dict()
    # # probab results
    lex_e = defaultdict(int)
    lex_f = defaultdict(int)

    phrase_probs = dict()
    for i, (de_phrase_str, en_phrase_str) in enumerate(phrases_str):
        t = (de_phrase_str, en_phrase_str)
        phrase_probs[t] = translation_probs(t)



    # print (phrase_probs)
    # print (lex_e)
    # sleep(10)
    # print (lex_f)

