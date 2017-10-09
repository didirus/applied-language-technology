from phrase_extraction import phrase_extraction
from phrase_extraction import alignstowords
import codecs
import time
from collections import defaultdict, Counter
from operator import div
import pickle


def probabs(count_LR_m, count_LR_s, count_LR_dl, count_LR_dr,
                  count_RL_m, count_RL_s, count_RL_dl, count_RL_dr,
                  total_LR, total_RL, phrase_str):
    p1 = check_div(div)(count_LR_m[phrase_str], float(total_LR[phrase_str]))
    p2 = check_div(div)(count_LR_s[phrase_str], float(total_LR[phrase_str]))
    p3 = check_div(div)(count_LR_dl[phrase_str], float(total_LR[phrase_str]))
    p4 = check_div(div)(count_LR_dr[phrase_str], float(total_LR[phrase_str]))
    p5 = check_div(div)(count_RL_m[phrase_str], float(total_RL[phrase_str]))
    p6 = check_div(div)(count_RL_s[phrase_str], float(total_RL[phrase_str]))
    p7 = check_div(div)(count_RL_dl[phrase_str], float(total_RL[phrase_str]))
    p8 = check_div(div)(count_RL_dr[phrase_str], float(total_RL[phrase_str]))

    return p1, p2, p3, p4, p5, p6, p7, p8


def check_div(f):
    def helper(a, b):
        if b == 0:
            return 0.0
        else:
            return f(a, b)

    return helper


def dump_file(f_out, p1, p2, p3, p4, p5, p6, p7, p8, phrase):
    sep = '|||'
    probs_str = map(str, [p1, p2, p3, p4, p5, p6, p7, p8])
    f_out.write(' '.join([phrase[0], sep, phrase[1], sep] + probs_str + ['\n']))

    return True


def move_down_diagonal(phrases_end,
                       pos_de,
                       pos_en,
                       phrase_discont_dist_RL_l,
                       phrase_discont_dist_RL_r,
                       word_discont_dist_RL_r,
                       word_discont_dist_RL_l):
    # Get possible previous phrase (going below the diagonal)
    previous = [t for t in phrases_end[pos_en[0] - 1] if pos_de[0] not in t[0]]

    # Get and count all the RL monotone orientations (phrase- AND word- based)
    rl_phrase_monotone = [(p_de, p_en) for p_de, p_en in previous if p_de[-1] == pos_de[0] - 1]
    N_RL_phrase_monotone = len(rl_phrase_monotone)
    N_RL_word_monotone = int(pos_en[0] - 1 in de_align_dict.__getitem__(pos_de[0] - 1))

    # Get and count all the RL swaps (phrase- AND word- based)
    rl_phrase_swap = [(p_de, p_en) for p_de, p_en in previous if p_de[0] == pos_de[-1] + 1]
    N_RL_phrase_swap = len(rl_phrase_swap)
    N_RL_word_swap = int(pos_en[0] - 1 in de_align_dict.__getitem__(pos_de[-1] + 1))

    # Get and count all the RL discontinuous (phrase- AND word- based)
    rl_phrase_discontinuous = [t for t in previous if
                               (t not in rl_phrase_monotone and t not in rl_phrase_swap)]
    N_RL_phrase_discontinuous_l = len(
        [(p_de, p_en) for p_de, p_en in rl_phrase_discontinuous if pos_de[-1] < p_de[0]])
    N_RL_phrase_discontinuous_r = len(rl_phrase_discontinuous) - N_RL_phrase_discontinuous_l

    # Get all the discontinuous (left/right) distortions (used for empirical analysis in Q2)

    # >PHRASE-BASED
    # >>Returns the phrase pairs RL L
    phrase_discont_dist_RL_l.extend(
        [p_de[0] - pos_de[-1] - 1 for p_de, p_en in rl_phrase_discontinuous if pos_de[-1] < p_de[0]])
    # >>Returns the phrase pairs RL R
    phrase_discont_dist_RL_r.extend(
        [pos_de[0] - p_de[-1] - 1 for p_de, p_en in rl_phrase_discontinuous if pos_de[0] > p_de[-1]])
    # >>Check if it is a monotone or swap, if not it is a swap
    de_al = en_align_dict.__getitem__(pos_en[0] - 1)
    monotone = pos_de[0] - 1 in de_al
    swap = pos_de[-1] + 1 in de_al
    if monotone or swap:
        N_RL_word_discontinuous_r = 0
        N_RL_word_discontinuous_l = 0
    else:
        N_RL_word_discontinuous_r = int(any([x < pos_de[0] - 1 for x in de_al]))
        N_RL_word_discontinuous_l = int(any([x > pos_de[-1] + 1 for x in de_al]))

    # >WORD-BASED
    if not monotone and not swap and any([x < pos_de[0] - 1 for x in de_al]):
        word_discont_dist_RL_r.append(min([pos_de[0] - x - 1 for x in de_al if pos_de[0] - 1 > x]))
    if not monotone and not swap and any([x > pos_de[-1] + 1 for x in de_al]):
        word_discont_dist_RL_l.append(min([x - pos_de[-1] - 1 for x in de_al if x > pos_de[-1] + 1]))

    return  N_RL_phrase_monotone, \
            N_RL_word_monotone, \
            N_RL_phrase_swap, \
            N_RL_word_swap, \
            N_RL_phrase_discontinuous_l, \
            N_RL_phrase_discontinuous_r, \
            phrase_discont_dist_RL_l, \
            phrase_discont_dist_RL_r, \
            N_RL_word_discontinuous_r, \
            N_RL_word_discontinuous_l, \
            word_discont_dist_RL_r, \
            word_discont_dist_RL_l

def move_up_diagonal(phrases_begin,
                     pos_de,
                     pos_en,
                     phrase_discont_dist_LR_l,
                     phrase_discont_dist_LR_r,
                     word_discont_dist_LR_r,
                     word_discont_dist_LR_l):

    # Get possible next phrase (going up the diagonal)
    nexts = [t for t in phrases_begin[pos_en[-1] + 1] if pos_de[-1] not in t[0]]  # for l-r

    # Get and count all the LR monotone orientations (phrase- AND word- based)
    lr_phrase_monotone = [(p_de, p_en) for p_de, p_en in nexts if p_de[0] == pos_de[-1] + 1]
    N_LR_phrase_monotone = len(lr_phrase_monotone)
    N_LR_word_monotone = int(pos_en[-1] + 1 in de_align_dict.__getitem__(pos_de[-1] + 1))

    # Get and count all the LR swaps (phrase- AND word- based)
    lr_phrase_swap = [(p_de, p_en) for p_de, p_en in nexts if p_de[-1] == pos_de[0] - 1]
    N_LR_phrase_swap = len(lr_phrase_swap)
    N_LR_word_swap = int(pos_en[-1] + 1 in de_align_dict.__getitem__(pos_de[0] - 1))

    # Get and count all the LR discontinuous (phrase-based)
    lr_phrase_discontinuous = [t for t in nexts if (t not in lr_phrase_monotone and t not in lr_phrase_swap)]
    N_LR_phrase_discontinuous_l = len(
        [(p_de, p_en) for p_de, p_en in lr_phrase_discontinuous if pos_de[0] > p_de[-1]])
    N_LR_phrase_discontinuous_r = len(lr_phrase_discontinuous) - N_LR_phrase_discontinuous_l

    # Get all the discontinuous (left/right) distortions (used for empirical analysis in Q2)

    # >PHRASE-BASED

    # >>Returns the phrase pairs LR L
    phrase_discont_dist_LR_l.extend(
        [pos_de[0] - p_de[-1] - 1 for p_de, p_en in lr_phrase_discontinuous if pos_de[0] > p_de[-1]])
    # >>Returns the phrase pairs LR R
    phrase_discont_dist_LR_r.extend(
        [p_de[0] - pos_de[-1] - 1 for p_de, p_en in lr_phrase_discontinuous if pos_de[-1] < p_de[0]])
    # >>Check if it is a monotone or swap, if not it is a swap
    de_al = en_align_dict.__getitem__(pos_en[-1] + 1)
    monotone = pos_de[-1] + 1 in de_al
    swap = pos_de[0] - 1 in de_al
    if monotone or swap:
        N_LR_word_discontinuous_r = 0
        N_LR_word_discontinuous_l = 0
    else:
        N_LR_word_discontinuous_r = int(any([x > pos_de[-1] + 1 for x in de_al]))
        N_LR_word_discontinuous_l = int(any([x < pos_de[0] - 1 for x in de_al]))

    # >WORD-BASED
    if not monotone and not swap and any([x > pos_de[-1] + 1 for x in de_al]):
        word_discont_dist_LR_r.append(min([x - pos_de[-1] - 1 for x in de_al if x > pos_de[-1] + 1]))
    if not monotone and not swap and any([x < pos_de[0] - 1 for x in de_al]):
        word_discont_dist_LR_l.append(min([pos_de[0] - x - 1 for x in de_al if pos_de[0] - 1 > x]))


    return N_LR_phrase_monotone, \
           N_LR_word_monotone, \
           N_LR_phrase_swap, \
           N_LR_word_swap, \
           N_LR_phrase_discontinuous_l, \
           N_LR_phrase_discontinuous_r, \
           phrase_discont_dist_LR_l, \
           phrase_discont_dist_LR_r, \
           N_LR_word_discontinuous_r,\
           N_LR_word_discontinuous_l, \
           word_discont_dist_LR_r, \
           word_discont_dist_LR_l


if __name__ == '__main__':
    start = time.time()
    print('reading the files')
    en_filepath = '../../Assignment1/data/file.en'
    de_filepath = '../../Assignment1/data/file.de'
    align_filepath = '../../Assignment1/data/file.aligned'

    # Max phrase length
    max_phrase_len = 7

    # File objects
    f_en = codecs.open(en_filepath, 'rb', encoding='utf-8')
    f_de = codecs.open(de_filepath, 'rb', encoding='utf-8')
    f_align = open(align_filepath, 'rb')

    # Counters
    # L=Left, R=Right, N=number of ...
    print('initialising the variables')
    count_phrase_LR_m = Counter()
    count_phrase_LR_s = Counter()
    count_phrase_LR_dr = Counter()
    count_phrase_LR_dl = Counter()

    total_phrase_LR = Counter()

    count_word_LR_m = Counter()
    count_word_LR_s = Counter()
    count_word_LR_dr = Counter()
    count_word_LR_dl = Counter()

    total_word_LR = Counter()

    count_phrase_RL_m = Counter()
    count_phrase_RL_s = Counter()
    count_phrase_RL_dr = Counter()
    count_phrase_RL_dl = Counter()

    total_phrase_RL = Counter()

    count_word_RL_m = Counter()
    count_word_RL_s = Counter()
    count_word_RL_dr = Counter()
    count_word_RL_dl = Counter()

    total_word_RL = Counter()

    # Extras for empirical analysis (Q2)
    phrase_discont_dist_LR_l = []
    phrase_discont_dist_LR_r = []
    phrase_discont_dist_RL_l = []
    phrase_discont_dist_RL_r = []

    word_discont_dist_LR_l = []
    word_discont_dist_LR_r = []
    word_discont_dist_RL_l = []
    word_discont_dist_RL_r = []

    phrase_len_reor_m = defaultdict(int)
    phrase_len_reor_s = defaultdict(int)
    phrase_len_reor_d = defaultdict(int)

    # Creating the files to dump the results
    f_phrase = codecs.open('../phrase_results.txt', 'wb', encoding='utf-8')
    f_word = codecs.open('../word_results.txt', 'wb', encoding='utf-8')

    print('getting the phrases and counts')
    for i, line_en in enumerate(f_en):
        if (i + 1) % 100 == 0:
            print('line no: ', i + 1)
            print('time:', time.time() - start)
            break

        # Read the input data
        line_de = f_de.readline()
        line_align = f_align.readline()

        # Extract the phrases like we did for Assignment 1, but now with additional information
        phrases_str, phrases, data_aligns, de_align_dict, en_align_dict, phrases_begin, phrases_end =\
            phrase_extraction(line_en, line_de, line_align, max_phrase_len)

        # For every phrase pair...
        for pos_de, pos_en in phrases:

            N_LR_phrase_monotone, \
            N_LR_word_monotone, \
            N_LR_phrase_swap, \
            N_LR_word_swap, \
            N_LR_phrase_discontinuous_l, \
            N_LR_phrase_discontinuous_r, \
            phrase_discont_dist_LR_l, \
            phrase_discont_dist_LR_r, \
            N_LR_word_discontinuous_r, \
            N_LR_word_discontinuous_l, \
            word_discont_dist_LR_r, \
            word_discont_dist_LR_l = move_up_diagonal(phrases_begin,
                                                      pos_de,
                                                      pos_en,
                                                      phrase_discont_dist_LR_l,
                                                      phrase_discont_dist_LR_r,
                                                      word_discont_dist_LR_r,
                                                      word_discont_dist_LR_l)

            N_RL_phrase_monotone, \
            N_RL_word_monotone, \
            N_RL_phrase_swap, \
            N_RL_word_swap, \
            N_RL_phrase_discontinuous_l, \
            N_RL_phrase_discontinuous_r, \
            phrase_discont_dist_RL_l, \
            phrase_discont_dist_RL_r, \
            N_RL_word_discontinuous_r, \
            N_RL_word_discontinuous_l, \
            word_discont_dist_RL_r, \
            word_discont_dist_RL_l = move_down_diagonal(phrases_end,
                                                      pos_de,
                                                      pos_en,
                                                      phrase_discont_dist_RL_l,
                                                      phrase_discont_dist_RL_r,
                                                      word_discont_dist_RL_r,
                                                      word_discont_dist_RL_l)

            # Getting the actual words from the alignments
            phrase_str = alignstowords((pos_de, pos_en), line_de.strip().split(), line_en.strip().split())

            # Updating all the counts

            # LR m/s/dr/dl phrase
            count_phrase_LR_m[phrase_str] += N_LR_phrase_monotone
            count_phrase_LR_s[phrase_str] += N_LR_phrase_swap
            count_phrase_LR_dr[phrase_str] += N_LR_phrase_discontinuous_r
            count_phrase_LR_dl[phrase_str] += N_LR_phrase_discontinuous_l

            # Total count of LR phrases (all orientations)
            total_phrase_LR[
                phrase_str] += N_LR_phrase_monotone + N_LR_phrase_swap + N_LR_phrase_discontinuous_r + \
                               N_LR_phrase_discontinuous_l

            # LR m/s/dr/dl words
            count_word_LR_m[phrase_str] += N_LR_word_monotone
            count_word_LR_s[phrase_str] += N_LR_word_swap
            count_word_LR_dr[phrase_str] += N_LR_word_discontinuous_r
            count_word_LR_dl[phrase_str] += N_LR_word_discontinuous_l

            # Total count of LR words (all orientations)
            total_word_LR[
                phrase_str] += N_LR_word_monotone + N_LR_word_swap + N_LR_word_discontinuous_r + \
                               N_LR_word_discontinuous_l

            # RL m/s/dr/dl phrases
            count_phrase_RL_m[phrase_str] += N_RL_phrase_monotone
            count_phrase_RL_s[phrase_str] += N_RL_phrase_swap
            count_phrase_RL_dr[phrase_str] += N_RL_phrase_discontinuous_r
            count_phrase_RL_dl[phrase_str] += N_RL_phrase_discontinuous_l

            # Total count of RL phrases (all orientations)
            total_phrase_RL[
                phrase_str] += N_RL_phrase_monotone + N_RL_phrase_swap + N_RL_phrase_discontinuous_r + \
                               N_RL_phrase_discontinuous_l

            # RL m/s/dr/dl words
            count_word_RL_m[phrase_str] += N_RL_word_monotone
            count_word_RL_s[phrase_str] += N_RL_word_swap
            count_word_RL_dr[phrase_str] += N_RL_word_discontinuous_r
            count_word_RL_dl[phrase_str] += N_RL_word_discontinuous_l

            # Total count of RL words (all orientations)
            total_word_RL[
                phrase_str] += N_RL_word_monotone + N_RL_word_swap + N_RL_word_discontinuous_r + \
                               N_RL_word_discontinuous_l

            # For Empirical Analysis; how many of every orientation is there (length and count)
            german_len = len(pos_de)
            phrase_len_reor_m[german_len] += N_LR_phrase_monotone + N_RL_phrase_monotone
            phrase_len_reor_s[german_len] += N_LR_phrase_swap + N_RL_phrase_swap
            phrase_len_reor_d[german_len] += N_LR_phrase_discontinuous_r + N_LR_phrase_discontinuous_l + \
                                             N_RL_phrase_discontinuous_r + N_RL_phrase_discontinuous_l

    print('getting the probabilities')
    for ph in count_phrase_LR_m.keys():
        # Getting the probabilities by dividing the counts by the total
        # Phrases
        p1, p2, p3, p4, p5, p6, p7, p8 = probabs(count_phrase_LR_m, count_phrase_LR_s,count_phrase_LR_dl,
                                               count_phrase_LR_dr, count_phrase_RL_m,count_phrase_RL_s,count_phrase_RL_dl,
                                               count_phrase_RL_dr, total_phrase_LR, total_phrase_RL, ph)

        # Saving the output to a file
        # Phrases
        dump_file(f_phrase, p1, p2, p3, p4, p5, p6, p7, p8, ph)

        # Words
        p1, p2, p3, p4, p5, p6, p7, p8 = probabs(count_word_LR_m, count_word_LR_s, count_word_LR_dl,
                                                      count_word_LR_dr, count_word_RL_m, count_word_RL_s,
                                                      count_word_RL_dl,
                                                      count_word_RL_dr, total_word_LR, total_word_RL, ph)
        # Words
        dump_file(f_word, p1, p2, p3, p4, p5, p6, p7, p8, ph)

    f_phrase.close()
    f_word.close()


    # pickle the dictionaries

    # pickle.dump(count_phrase_LR_m,open('../pickled/count_phrase_LR_m.pickle','wb'))
    # pickle.dump(count_phrase_LR_s, open('../pickled/count_phrase_LR_s.pickle', 'wb'))
    # pickle.dump(count_phrase_LR_dl, open('../pickled/count_phrase_LR_dl.pickle', 'wb'))
    # pickle.dump(count_phrase_LR_dr, open('../pickled/count_phrase_LR_dr.pickle', 'wb'))
    # pickle.dump(count_phrase_RL_m, open('../pickled/count_phrase_RL_m.pickle', 'wb'))
    # pickle.dump(count_phrase_RL_s, open('../pickled/count_phrase_RL_s.pickle', 'wb'))
    # pickle.dump(count_phrase_RL_dl, open('../pickled/count_phrase_RL_dl.pickle', 'wb'))
    # pickle.dump(count_phrase_RL_dr, open('../pickled/count_phrase_RL_dr.pickle', 'wb'))
    # pickle.dump(total_phrase_LR, open('../pickled/total_phrase_LR.pickle', 'wb'))
    # pickle.dump(total_phrase_RL, open('../pickled/total_phrase_RL.pickle', 'wb'))
    # pickle.dump(count_word_LR_m, open('../pickled/count_word_LR_m.pickle', 'wb'))
    # pickle.dump(count_word_LR_s, open('../pickled/count_word_LR_s.pickle', 'wb'))
    # pickle.dump(count_word_LR_dl, open('../pickled/count_word_LR_dl.pickle', 'wb'))
    # pickle.dump(count_word_LR_dr, open('../pickled/count_word_LR_dr.pickle', 'wb'))
    # pickle.dump(count_word_RL_m, open('../pickled/count_word_RL_m.pickle', 'wb'))
    # pickle.dump(count_word_RL_s, open('../pickled/count_word_RL_s.pickle', 'wb'))
    # pickle.dump(count_word_RL_dl, open('../pickled/count_word_RL_dl.pickle', 'wb'))
    # pickle.dump(count_word_RL_dr, open('../pickled/count_word_RL_dr.pickle', 'wb'))
    # pickle.dump(total_word_LR, open('../pickled/total_word_LR.pickle', 'wb'))
    # pickle.dump(total_word_RL, open('../pickled/total_word_RL.pickle', 'wb'))
    # pickle.dump(phrase_discont_dist_LR_l, open('../pickled/phrase_discont_dist_LR_l.pickle', 'wb'))
    # pickle.dump(phrase_discont_dist_LR_r, open('../pickled/phrase_discont_dist_LR_r.pickle', 'wb'))
    # pickle.dump(phrase_discont_dist_RL_l, open('../pickled/phrase_discont_dist_RL_l.pickle', 'wb'))
    # pickle.dump(phrase_discont_dist_RL_l, open('../pickled/phrase_discont_dist_RL_l.pickle', 'wb'))
    # pickle.dump(phrase_discont_dist_RL_r, open('../pickled/phrase_discont_dist_RL_r.pickle', 'wb'))
    # pickle.dump(word_discont_dist_LR_l, open('../pickled/word_discont_dist_LR_l.pickle', 'wb'))
    # pickle.dump(word_discont_dist_LR_r, open('../pickled/word_discont_dist_LR_r.pickle', 'wb'))
    # pickle.dump(word_discont_dist_RL_l, open('../pickled/word_discont_dist_RL_l.pickle', 'wb'))
    # pickle.dump(word_discont_dist_RL_r, open('../pickled/word_discont_dist_RL_r.pickle', 'wb'))
    # pickle.dump(phrase_len_reor_m, open('../pickled/phrase_len_reor_m.pickle', 'wb'))
    # pickle.dump(phrase_len_reor_s, open('../pickled/phrase_len_reor_s.pickle', 'wb'))
    # pickle.dump(phrase_len_reor_d, open('../pickled/phrase_len_reor_d.pickle', 'wb'))

    print('time:', time.time() - start)


