import pickle, os


def checkif_float(N):
    '''
    check if the value if float
    :param N:
    :return:T/F
    '''
    try:
        float(N)
        return True
    except ValueError:
        return False


def read_pt(data_path, pt_file=None):
    """
    Function to read phrase table
    :param pt_file: file object for phrase table
    :return: Dictionary of phrases. key: (f,e) and value:list of probability
    """
    if os.path.exists(data_path + "phrases"):
        print('read from pickle phrase table')
        phrases = pickle.load(open(data_path + 'phrases', 'rb'))
    else:
        phrases = {}
        i = 0
        for line in pt_file:
            if (i+1) % 50000 == 0:
                print('line no.(PT) ', i)
                #break
            i += 1

            line = line.split(' ||| ')
            f = line[0]
            e = line[1]
            probab = [float(p) for p in line[2].split()]
            phrases[(f, e)] = probab
        pickle.dump(phrases, open(data_path + 'phrases','wb'))
    return phrases


def read_lm(data_path, lm_file=None):
    """
    Function to read Language modelprobs
    :param lm_file: file object for lang. Model
    :return: Dictionary with key: 'ngram text' and value (ngram prob, backoff)
    """
    if os.path.exists(data_path + "lm_min_p"):
        print('read from pickle lm,lm_p_min')
        lm, min_p = pickle.load(open(data_path + 'lm_min_p', 'rb'))
    else:
        gram = 0
        lm = {}
        min_p = 0.0

        i = 0
        for line in lm_file:
            if (i+1) % 50000 == 0:
                print ('line no.(lm): ', i)
            i += 1

            if line[0] == '\\':  # Because python does not recognise 1 slash
                if line[-7:-1] == 'grams:':
                    print (line)
                    gram = line[1]
                continue
            line = line.split()

            if gram != 0 and len(line) > 0:
                prob = float(line[0])
                if prob < min_p:
                    min_p = prob

                if checkif_float(line[-1]):
                    backoff_prob = float(line[-1])
                    words = line[1:-1]
                else:
                    backoff_prob = 0
                    words = line[1:]

                ph = ' '.join(words)
                lm[ph] = (prob, backoff_prob)
        pickle.dump([lm, min_p], open(data_path + 'lm_min_p', 'wb'))

    return lm, min_p


def read_ro(data_path, ro_file=None):
    """
    Function(same as read_pt()) to read phrase table
    :param ro_file: file object for reorderings
    :return: Dictionary of phrases. key: (f,e) and value:list of probability
    """
    if os.path.exists(data_path + 'reordering'):
        print('read from pickle reordering')
        reordering = pickle.load(open(data_path + 'reordering', 'rb'))
    else:
        i = 0
        reordering = {}
        for line in ro_file:
            if (i+1) % 50000 == 0:
                print ('line no.(ro)',i)
                #break
            i += 1
            line = line.split(' ||| ')
            f = line[0]
            e = line[1]
            probs = [float(p) for p in line[2].split()]
            reordering[(f, e)] = probs
        pickle.dump(reordering, open(data_path + 'reordering', 'wb'))
    return reordering
