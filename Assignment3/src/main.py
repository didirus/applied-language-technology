import time
from read_data import *
from calculate_costs import overall_trans_cost


if __name__ == '__main__':

    start = time.time()

    data_path = '../data/ALT/'

    print('Read  phrases and probabs from phrase table')
    phrase_table = open(data_path + 'phrase-table', 'r')
    phrases = read_pt(pt_file=phrase_table)

    print('Read Language model and probabilities')
    language_model = open(data_path+'file.en.lm', 'r')
    lm,minlm_p = read_lm(lm_file=language_model)

    print('Read reorderings')
    reordering_file = open(data_path+'dm_fe_0.75', 'r')
    reordering = read_ro(ro_file=reordering_file)

    # test_results_trace = open(data_path+'testresults.trans.txt.trace', 'r')

    # overall_trans_cost(phrases,lm,minlm_p,reordering)

    print('time:', time.time() - start)
