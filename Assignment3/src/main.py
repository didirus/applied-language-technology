from collections import defaultdict
import pickle


def read_pt(pt_file=None):
    """
    Function to read phrase table
    :param pt_file: file object for phrase table
    :return: Dictonary of phrases. key: (f,e) and value:list of probability
    """
    phrases = {}
    i=0
    for line in pt_file:
        if i==100:
            print('line no. ',i)
        i+=1

        line = line.split(' ||| ')
        f = line[0]
        e = line[1]
        probab = [float(p) for p in line[2].split()]
        phrases[(f, e)] = probab
    return phrases


if __name__ == '__main__':

    data_path = '../data/ALT/'
    # f_en = open(data_path +'file.test.en', 'r')
    # f_de = open(data_path+'file.test.de', 'r')

    # Read  phrases and probabs from phrase table
    phrase_table = open(data_path+'phrase-table', 'r')
    phrases = read_pt(pt_file=phrase_table)


    # test_results = open(data_path+'testresults.trans.txt.trace', 'r')
    # language_model = open(data_path+'file.en.lm', 'r')
    # reordering = open(data_path+'dm.fe.0.75', 'r')
