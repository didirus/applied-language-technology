import math
import numpy as np

# todo: calculate cost from language model recursive?
def lm_cost(phrase_lm, lm, min_lm_prob):
    lmcost = 0
    e = phrase_lm
    words = e.split()
    # For all words w_n in phrase
    for cur_pos in range(0, len(words)):
        # History: w1,...w_{n-1}
        history_pos = range(0, cur_pos)
        history = [words[pos] for pos in history_pos]

        w_n = words[cur_pos]

        # Do not take into account unigram of first word,
        #  if first word is <s>
        if cur_pos == 0 and w_n == "<s>":
            continue

        # Language model of a phrase is sum of p(w_n| w1,...,w_{n-1}) for every w_n
        cost_word = word_cost(w_n, history, lm, min_lm_prob)
        lmcost += cost_word
    lmcost *= 1
    return lmcost


def word_cost(w_n,history, lm, minimum_cost, backoff=False):

    wn_cost = 0
    n_gram = ' '.join(history + [w_n])
    if n_gram in lm:
        wn_cost = lm[n_gram][0]
        if backoff:
            wn_cost += lm[n_gram][1]
    else:
        # n-gram not available
        if len(history) > 0:
            #backoff to shorter history w_2...w_{n-1}
            new_history = history[1:]
            # Recursive call of word_cost,
            # and add backoff probability
            wn_cost = word_cost(w_n,new_history, lm, minimum_cost, backoff=True)
        else:
            # Assign wn_cost=0 if unigram is not available
            wn_cost = minimum_cost
    return wn_cost


def reor_model_cost(phrase, trace, reorder_file, f_line):

    print ('reordering model cost')
    # index of the phrase in the trace sentence
    phrase_index = ''.join([str(phrase[0]), ':', str(phrase[1])])

    phrase_pos = trace.index(phrase_index)
    prev_ph_align = trace[phrase_pos - 1].split(':')[0]
    if (phrase_pos != len(trace) - 1):
        next_ph_align = trace[phrase_pos + 1].split(':')[0]
    else:
        next_ph_align = 'end-end'
    next_ph_align_begin, next_ph_align_end = next_ph_align.split('-')
    prev_ph_align_start, prev_ph_align_end = prev_ph_align.split('-')

    reor_cost = 0
    e = phrase[1].rstrip()
    f_align_start = int(phrase[0].split('-')[0])
    f_align_end = int(phrase[0].split('-')[1])

    # list of words from the f_line
    f = f_line[f_align_start:f_align_end + 1]
    f = ' '.join(f).rstrip()
    try:
        probs = reorder_file[(f, e)]
        rl_m, rl_s, rl_d, lr_m, lr_s, lr_d = probs
        RL_cost = 0
        LR_cost = 0

        # if phrase is first in line
        if phrase_pos == 0:
            RL_cost = rl_m
        else:
            if (int(prev_ph_align_end) == f_align_start - 1):
                RL_cost = rl_m
            elif (int(prev_ph_align_start) == f_align_end + 1):
                RL_cost = rl_s
            else:
                RL_cost = rl_d

        # if phrase is last in line
        if phrase_pos == len(trace) - 1:
            LR_cost = lr_m
        else:
            if int(next_ph_align_begin) == f_align_end + 1:
                LR_cost = lr_m
            elif int(next_ph_align_end) == f_align_start - 1:
                LR_cost = lr_s
            else:
                LR_cost = lr_d

        # probabs of both direction multiplied
        phrase_cost = LR_cost * RL_cost

        # log probabs
        phrase_cost = math.log10(phrase_cost)
        phrase_cost *= 1
    except KeyError:
        # untranslated phrase
        phrase_cost = -1
    reor_cost += phrase_cost
    return reor_cost


def transl_model_cost(phrase, p_table, f_line):
    print ('translation model cost')
    # phrases in the trace assign 4 translation model weights
    e = phrase[1].rstrip()

    f_al_start = int(phrase[0].split('-')[0])
    f_al_stop = int(phrase[0].split('-')[1])

    # Get list of words from the f_line
    f = f_line[f_al_start:f_al_stop + 1]
    f = ' '.join(f).rstrip()

    try:
        p_fe, lex_fe, p_ef, lex_ef, word_pen = p_table[(f, e)]
        # For now assumed to be the sum of all the probs (weighted by 1)
        phrase_cost = 1 * math.log10(p_fe) + 1 * math.log10(lex_fe) + 1 * math.log10(p_ef) + 1 * math.log10(
            lex_ef) + 1 * word_pen
        phrase_cost = phrase_cost * 1  # -1
    except KeyError:
        if f != e:
            print ('key not found: ', (f, e))

        phrase_cost = -1
    return phrase_cost


def lin_dist_cost(phrase, next_phrase):
    this_end = int(phrase[0].split('-')[1])
    next_start = int(next_phrase[0].split('-')[0])
    cost = -1 * abs(next_start - this_end - 1)
    return cost


def overall_trans_cost(l_r, l_t, l_l, l_d, l_p, p_table=None, lm=None, min_lm_prob=None, reorder_file=None):

    data_path = '../data/ALT/'

    print ('overall cost function')

    traces = open(data_path+'testresults.trans.txt.trace', 'r')
    f_file = open(data_path+'file.test.de', 'r')
    output_file = open(data_path+'cost_output.txt', 'w')

    sentence_cost_list = []

    for f_line, trace in zip(f_file, traces):
        trace = trace.split(' ||| ')
        f_line = f_line.split()
        phrases = [tuple(p.split(':', 1)) for p in trace]
        cost_per_phrase = []
        for i in range(0, len(phrases)):

            phrase = phrases[i]

            # translation cost
            phrase_translation_model_cost = transl_model_cost(phrase, p_table, f_line)

            # orientation distortion cost
            phrase_reordering_model_cost = reor_model_cost(phrase, trace, reorder_file, f_line)

            # language model cost
            # language model-> start and end symbols need to be added to the phrase
            phrase_lm = phrase[1]
            if i == 0:
                phrase_lm = "<s> " + phrase[1]
            if i == len(phrases):
                phrase_lm = phrase[1] + " </s>"
            phrase_language_model_cost = lm_cost(phrase_lm, lm, min_lm_prob)

            # linear distortion cost
            phrase_linear_distortion_cost = lin_dist_cost(phrase, phrases[i+1])

            # phrase penalty
            phrase_penalty = -1

            # combine all costs into one "phrase cost"
            # phrase_cost = np.sum(l_r * phrase_reordering_model_cost,
            #                      l_t * phrase_translation_model_cost,
            #                      l_l * phrase_language_model_cost,
            #                      l_d * phrase_linear_distortion_cost,
            #                      l_p * phrase_penalty)
            phrase_cost = l_r * phrase_reordering_model_cost+l_t * phrase_translation_model_cost+l_l * phrase_language_model_cost+l_d * phrase_linear_distortion_cost+l_p * phrase_penalty

            cost_per_phrase.append(phrase_cost)

            # dump in file
            output_file.write(trace[i].rstrip() + " lm:" + str(phrase_language_model_cost) +
                              " tm:" + str(phrase_translation_model_cost) + " rm:" + str(phrase_reordering_model_cost)
                              + ' lin_dist:' + str(phrase_linear_distortion_cost) + " total_phrase:" + str(phrase_cost)
                              + " ||| ")

        # sum all the phrase costs for entire sentence
        sentence_cost = sum(cost_per_phrase)
        output_file.write("Line cost: "+ str(sentence_cost) + '\n')

    # close files
    traces.close()
    f_file.close()
    output_file.close()

    return

