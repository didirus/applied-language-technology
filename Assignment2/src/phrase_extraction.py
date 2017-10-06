
#From assignment 1

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
    :param positions: positions of the german and english sentence
    :param de_line: german line
    :param en_line: english line
    :return: tuple in text
    '''
    return (' '.join(map(de_line.__getitem__, positions[0])), ' '.join(map(en_line.__getitem__, positions[1])))


def update_word_count(de_line, en_line):
    '''
    updates word counts. Used to compute lexical probabilities.
    '''

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

    global joint_freq
    global de_freq
    global en_freq

    t = (de_phrase_str, en_phrase_str)
    joint_freq[t] += 1
    de_freq[de_phrase_str] += 1
    en_freq[en_phrase_str] += 1

    return

"""
PART-3
"""
def translation_probs(t):

    p_f_e = joint_freq[t] / float(en_freq[en_phrase_str])
    p_e_f = joint_freq[t] / float(de_freq[de_phrase_str])

    return (p_f_e, p_e_f)

def dump_data(t):
    '''
    dump into files for submission
    '''
    global f_ext_out
    global f_phrase_out
    global f_lex_out
    global f_comb_out

    global lex_e
    global lex_f
    global phrase_probs
    global joint_freq
    global de_freq
    global en_freq

    common_de_text = ''
    common_de_text += t[0]
    common_de_text += ' ||| '
    common_de_text += t[1]
    common_de_text += ' ||| '

    frequency = str(de_freq[t[0]])
    frequency += ' '
    frequency += str(en_freq[t[1]])
    frequency += ' '
    frequency += str(joint_freq[t])

    translation_prob = str(phrase_probs[t][0])
    translation_prob += ' '
    translation_prob += str(phrase_probs[t][1])

    lex_prob = translation_prob
    lex_prob += ' '
    lex_prob += str(lex_f[t])
    lex_prob += ' '
    lex_prob += str(lex_e[t])

    f_ext_out.write(common_de_text + frequency + '\n')
    f_phrase_out.write(common_de_text + translation_prob + '\n')
    f_lex_out.write(common_de_text + lex_prob + '\n')
    f_comb_out.write(common_de_text + lex_prob + ' ||| ' + frequency + '\n')

    return
"""
PART-3
"""
def lexical_prob(phrase_aligns, f_start, e_start, f_word_freq, f_phrase, e_phrase, direct):
    '''
    calculate the lexical probability of a phrase
    :param phrase_aligns: {source positions : list of foreign aligned positions}
    :param f_start: starting position of the foreign phrase in the original sentence
    :param e_start: starting position of the source phrase in the original sentence
    :param f_word_freq: foreign word count
    :param f_phrase: foreign phrase
    :param e_phrase: source phrase
    :return: lex probability
    '''

    global joint_word_freq

    prob = 1
    for e_pos, f_aligns in phrase_aligns.iteritems():
        if f_aligns:
            if direct:
                prob *= sum(map(lambda x: joint_word_freq[(f_phrase[x - f_start], e_phrase[e_pos - e_start])] \
                                          / float(f_word_freq[f_phrase[x - f_start]]), f_aligns)) / float(len(f_aligns))
            else:
                prob *= sum(map(lambda x: joint_word_freq[(f_phrase[e_pos - f_start], e_phrase[x - e_start])] \
                                          / float(f_word_freq[e_phrase[x - e_start]]), f_aligns)) / float(len(f_aligns))
        else:
            if direct:
                prob *= joint_word_freq[(nil, e_phrase[e_pos - e_start])] / float(f_word_freq[nil])
            else:
                prob *= joint_word_freq[(f_phrase[e_pos - f_start], nil)] / float(f_word_freq[nil])

    return prob

def phrase_extraction(line_en, line_de, line_align, max_phrase_len):
    '''
    Extracts phrases from a bitext sentence.
    '''

    start = time.time()

    data_alignments = defaultdict(list)

    # resulting phrases
    phrases = []
    phrases_str = set()

    phrases_begin = defaultdict(list)
    phrases_end = defaultdict(list)

    # print 'Extracting phrases for sentence: %s\n' %line_en

    # read english line
    en_sent = line_en.strip().split()  # whitespace tokenization

    # read deutsch line
    de_sent = line_de.strip().split()  # whitespace tokenization

    en_alignment_dict = defaultdict(list)
    de_alignment_dict = defaultdict(list)

    for de_a, en_a in map(lambda x: x.split('-'), line_align.strip().split()):
        de_alignment_dict[int(de_a)].append(int(en_a))
        en_alignment_dict[int(en_a)].append(int(de_a))

    # update_word_count(de_sent, en_sent, en_alignment_dict)

    # generate all possible deutsch phrases
    de_candidate_phrases = [range(i, i + j + 1) for i, _ in enumerate(de_sent) \
                            for j in range(min([len(de_sent), max_phrase_len, len(de_sent) - i]))]

    # generate all possible english phrases
    en_candidate_phrases = [range(i, i + j + 1) for i, _ in enumerate(en_sent) \
                            for j in range(min([len(en_sent), max_phrase_len, len(en_sent) - i]))]

    for en_cand in en_candidate_phrases:
        for de_cand in de_candidate_phrases:
            if check1(de_cand, en_cand, en_alignment_dict) and check2(de_cand, en_cand, de_alignment_dict):

                translation = alignstowords((de_cand, en_cand), de_sent, en_sent)
                if translation not in phrases_str:
                    phrases_str.add(translation)
                    phrases.append((de_cand, en_cand))

                de_phrase_alignments = {pos: de_alignment_dict[pos] for pos in de_cand}
                en_phrase_alignments = {pos: en_alignment_dict[pos] for pos in en_cand}
                data_alignments[(translation[0], translation[1])].append(
                    (de_phrase_alignments, en_phrase_alignments))

                phrases_begin[min(en_cand)].append((de_cand, en_cand))
                phrases_end[max(en_cand)].append((de_cand, en_cand))



    return phrases_str, phrases, data_alignments, de_alignment_dict, en_alignment_dict, phrases_begin, phrases_end