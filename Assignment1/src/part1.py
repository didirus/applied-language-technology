import numpy as np


def update_frequencies(e_p, f_p, e_freq, f_freq, c_freq, e_phrase, f_phrase):

    return e_freq, f_freq, c_freq


def new_entry(e_p, f_p, e_freq, f_freq, c_freq, p_a, e_phrase, f_phrase):
    e_p = np.append(e_p, e_phrase)
    f_p = np.append(f_p, f_phrase)
    e_freq = np.append(e_freq, 0)
    f_freq = np.append(f_freq, 0)
    c_freq = np.append(c_freq, 0)
    p_a = np.append(p_a, 0)
    return e_p, f_p, e_freq, f_freq, c_freq, p_a


def valid_phrase_pair():

    return True


def create_matrix(alignment, e_s, f_s):
    matrix = np.zeros((len(e_s), len(f_s)), dtype=int)

    for alig in alignment:
        matrix[int(alig[0]), int(alig[1])] = 1

    return matrix


def process_sentence(e, f, a, i):
    e_s = e[i].split()
    f_s = f[i].split()
    alignment = a[i].split()
    alignment = [x.split('-') for x in alignment]
    return np.asarray(e_s), np.asarray(f_s), np.asarray(alignment)


def phrase_extraction(e, f, a):

    e_p = np.array([], dtype=str)
    f_p = np.array([], dtype=str)
    e_freq = np.array([], dtype=float)
    f_freq = np.array([], dtype=float)
    c_freq = np.array([], dtype=float)
    p_a = np.array([], dtype=int)

    for i in range(len(e)):
        e_s, f_s, alignment = process_sentence(e, f, a, i)
        matrix = create_matrix(alignment, e_s, f_s)
        v_width, h_width = 1, 1
        grow_limit = 5

        for v_pivot in range(len(e_s)):

            h_pivot = np.where(matrix[v_pivot, :] == 1)[0][0]

            grow = True
            while grow:

                # get list of indices of sentence which is the phrase
                temp_e_p = list(range(v_pivot, v_pivot+v_width))
                temp_f_p = list(range(h_pivot, h_pivot+h_width))
                # get total string of phrase
                e_phrase = ' '.join(e_s[temp_e_p])
                f_phrase = ' '.join(f_s[temp_f_p])

                # if a valid phrase pair is found: update arrays
                if valid_phrase_pair():
                    if e_phrase not in e_p:
                        # english phrase not found yet, so add new entry
                        e_p, f_p, e_freq, f_freq, c_freq, p_a = new_entry(e_p, f_p, e_freq, f_freq, c_freq, p_a, e_phrase, f_phrase)
                    else:
                        # english phrase found, now check for foreign phrase
                        exists = False
                        for ind in np.where(e_p == e_phrase)[0]:
                            if f_p[ind] == f_phrase:
                                # entry already exists
                                exists = True
                                break
                        if not exists:
                            # foreign phrase not found yet, so add new entry
                            e_p, f_p, e_freq, f_freq, c_freq = new_entry(e_p, f_p, e_freq, f_freq, c_freq, p_a, e_phrase, f_phrase)

                    # update frequencies
                    e_freq, f_freq, c_freq = update_frequencies(e_p, f_p, e_freq, f_freq, c_freq, e_phrase, f_phrase)

                    h_width = min(h_width, v_width) + 1
                    v_width = min(h_width, v_width) + 1

                # if not yet pair found and search space was already max: stop growing
                elif v_width == grow_limit and h_width == grow_limit:
                    grow = False

                # if not yet pair found: grow search space
                else:
                    if h_width == grow_limit or h_pivot+h_width > len(e_s)-1:
                        h_width = 1
                        v_width += 1
                    else:
                        h_width += 1




