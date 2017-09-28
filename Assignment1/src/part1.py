import numpy as np


def update_frequencies(e_p, f_p, e_freq, f_freq, c_freq, e_phrase, f_phrase):
    # TODO if computational problems, setup for new entry frequencie, no lookup necessary
    e_indices = np.where(e_p == e_phrase)
    f_indices = np.where(f_p == f_phrase)

    e_freq[e_indices] += 1
    f_freq[f_indices] += 1

    c_index = np.intersect1d(e_indices, f_indices)
    c_freq[c_index] += 1

    return e_freq, f_freq, c_freq


def new_entry(e_p, f_p, e_freq, f_freq, c_freq, p_a, e_phrase, f_phrase):
    e_p = np.append(e_p, e_phrase)
    f_p = np.append(f_p, f_phrase)
    e_freq = np.append(e_freq, 0)
    f_freq = np.append(f_freq, 0)
    c_freq = np.append(c_freq, 0)
    p_a = np.append(p_a, 0)
    return e_p, f_p, e_freq, f_freq, c_freq, p_a


def valid_phrase_pair(matrix, v_pivot, h_pivot, v_width, h_width):
    shape_matrix = list(matrix.shape)
    top_matrix = matrix[0:v_pivot, h_pivot:h_pivot+h_width]
    bottom_matrix = matrix[v_pivot+v_width:shape_matrix[0]+1, h_pivot:h_pivot+h_width]

    left_matrix = matrix[v_pivot:v_pivot+v_width, 0:h_pivot]
    right_matrix = matrix[v_pivot:v_pivot+v_width, h_pivot+h_width:shape_matrix[1]]
    inside_mat_flag=False
    inside_matrix = matrix[v_pivot:v_pivot+v_width,h_pivot:h_pivot+h_width]
    for i in range(len(inside_matrix)):
        if np.sum(inside_matrix[i]) == 0:
            inside_mat_flag=True

    for i in range(inside_matrix.shape[1]):
        if np.sum(inside_matrix[:, i])==0:
            inside_mat_flag=True

    if np.sum(top_matrix)+np.sum(bottom_matrix)+np.sum(right_matrix)+np.sum(left_matrix) > 0 :
        return False
    elif inside_mat_flag:
        return False
    else:
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

    # We initialise numpy arrays
    e_p = np.array([], dtype=str)  # The english phrases
    f_p = np.array([], dtype=str)  # The translated phrases
    e_freq = np.array([], dtype=float)  # The frequency of the english phrases
    f_freq = np.array([], dtype=float)  # The frequency of the translated phrases
    c_freq = np.array([], dtype=float)  # The frequency of the english and translated phrases together
    p_a = np.array([], dtype=int)  # The alignments of the phrase pairs

    # For every sentence for e, f, and a...
    for i in range(len(e)):

        # Split the lines
        e_s, f_s, alignment = process_sentence(e, f, a, i)
        print('Row: ', i, ': ', len(e_s))
        # Create the alignment matrix
        matrix = create_matrix(alignment, e_s, f_s)
        # print(matrix)
        # Set the scan widths initially to 1
        v_width, h_width = 1, 1
        # A phrase has a limit amount of words
        grow_limit = 5
        # Start with a vertical pivot which is just going from top to down in the matrix
        for v_pivot in range(len(e_s)):
            # The horizontal pivot is the location where the first alignment is found
            hit = np.where(matrix[v_pivot, :] == 1)[0]
            if len(hit) < 1:
                continue
            h_pivot = hit[0]
            # Set the flag for 'growing' to True
            grow = True
            # While we are looking for phrases, we are growing our search space bounded by the limit
            while grow:
                # Get list of indices of sentence which is the potential phrase (both languages)
                temp_e_p = list(range(v_pivot, v_pivot+v_width))
                temp_f_p = list(range(h_pivot, h_pivot+h_width))
                # Get total string of phrase (both languages)
                e_phrase = ' '.join(e_s[temp_e_p])
                f_phrase = ' '.join(f_s[temp_f_p])
                # If a valid phrase pair is found: update arrays
                if valid_phrase_pair(matrix, v_pivot, h_pivot, v_width, h_width):
                    if e_phrase not in e_p:
                        # English phrase not found yet, so add new entry
                        e_p, f_p, e_freq, f_freq, c_freq, p_a = new_entry(e_p, f_p, e_freq, f_freq, c_freq, p_a, e_phrase, f_phrase)
                    else:
                        # English phrase found, now check for foreign phrase
                        exists = False
                        for ind in np.where(e_p == e_phrase)[0]:
                            if f_p[ind] == f_phrase:
                                # Entry already exists
                                exists = True
                                break
                        if not exists:
                            # Foreign phrase not found yet, so add new entry
                            e_p, f_p, e_freq, f_freq, c_freq, p_a = new_entry(e_p, f_p, e_freq, f_freq, c_freq, p_a, e_phrase, f_phrase)

                    # Update frequencies
                    e_freq, f_freq, c_freq = update_frequencies(e_p, f_p, e_freq, f_freq, c_freq, e_phrase, f_phrase)

                    if h_width >= grow_limit or v_width >= grow_limit:
                        h_width = 1
                        v_width = 1
                        grow = False
                    else:
                        # If not yet pair found and search space was already max: stop growing
                        if (v_width > grow_limit and h_width > grow_limit) or \
                                (h_pivot+h_width >= len(f_s) or v_pivot + v_width >= len(e_s)):
                            h_width = 1
                            v_width = 1
                            grow = False
                        else:
                            h_width += 1
                            v_width += 1

                elif (v_width == grow_limit and h_width == grow_limit) or \
                        (h_pivot+h_width >= len(f_s) and v_pivot + v_width >= len(e_s)) or \
                        (v_width == grow_limit and h_pivot + h_width >= len(f_s)) or \
                        (h_width == grow_limit and v_pivot + v_width >= len(e_s)):

                        h_width = 1
                        v_width = 1
                        grow = False
                # If not yet pair found: grow search space
                else:
                    if h_width == grow_limit or h_pivot+h_width >= len(f_s):
                        h_width = 1
                        v_width += 1
                    else:
                        h_width += 1




