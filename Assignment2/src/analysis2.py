import matplotlib.pyplot as plt
import pickle
import numpy as np
from nltk import compat


def plot_phrase_len_reorder():
    # reordering events frequency wrt German-side phrase len
    mp = pickle.load(open('../pickled/phrase_len_reor_m.pickle','rb'))
    sp = pickle.load(open('../pickled/phrase_len_reor_s.pickle','rb'))
    dp = pickle.load(open('../pickled/phrase_len_reor_d.pickle','rb'))

    m = mp.values()
    s = sp.values()
    d = dp.values()

    x = np.arange(len(mp.values()))

    ax = plt.subplot(111)
    width = 0.4
    ax.set_xticks(x + width)
    ax.set_xticklabels(['1', '2', '3', '4', '5','6','7'])
    plt.xlabel('Phrase length')
    plt.ylabel('Counts')
    mon = plt.bar(x + width * 0.5, m, width, color='#5f9ed1', edgecolor='None')
    dis = plt.bar(x + width * 0.5, d, width, color='#f26c64', edgecolor='None')
    swap = plt.bar(x + width * 0.5, s, width, color='#32a251', edgecolor='None')
    ax.legend((mon[0], dis[0], swap[0]), ('Monotone', 'Discontinuous', 'Swap'), frameon=False)
    # plt.show()
    plt.savefig('../fig/phrase_len_reor', bbox_inches='tight')
    plt.close()

    return True


def plot_phrase_len_discont():
    # frequency of discontinuous-to-the-left and -to-the-right wrt distance
    dl = pickle.load(open('../pickled/phrase_discont_dist_LR_l.pickle','rb'))
    dr = pickle.load(open('../pickled/phrase_discont_dist_LR_r.pickle','rb'))

    x = np.arange(len(np.bincount(dl)))

    ax = plt.subplot(111)
    width = 0.4
    plt.xlabel('Distance')
    plt.ylabel('Counts')
    mon = plt.bar(x, np.bincount(dl), width, color='#5f9ed1', edgecolor='None')
    # plt.show()
    plt.ylim((0,2500000))
    plt.savefig('../fig/phrase_dist_freq_l', bbox_inches='tight')
    plt.close()

    x = np.arange(len(np.bincount(dr)))

    ax = plt.subplot(111)
    width = 0.4
    plt.xlabel('Distance')
    plt.ylabel('Counts')
    mon = plt.bar(x, np.bincount(dr), width, color='#5f9ed1', edgecolor='None')
    plt.ylim((0,2500000))
    plt.savefig('../fig/phrase_dist_freq_r', bbox_inches='tight')
    plt.close()

    return True


def plot_phrase_discontinuous_distance():
    # phrase discontinuous distance
    phrase_discont_dist_LR_l = pickle.load(open('../pickled/phrase_discont_dist_LR_l.pickle','rb'))
    phrase_discont_dist_LR_r = pickle.load(open('../pickled/phrase_discont_dist_LR_r.pickle','rb'))
    phrase_discont_dist_RL_l = pickle.load(open('../pickled/phrase_discont_dist_RL_l.pickle','rb'))
    phrase_discont_dist_RL_r = pickle.load(open('../pickled/phrase_discont_dist_RL_r.pickle','rb'))

    means = [np.mean(phrase_discont_dist_LR_l), np.mean(phrase_discont_dist_LR_r),
            np.mean(phrase_discont_dist_RL_l), np.mean(phrase_discont_dist_RL_r)]

    stds = [np.std(phrase_discont_dist_LR_l), np.std(phrase_discont_dist_LR_r),
            np.std(phrase_discont_dist_RL_l), np.std(phrase_discont_dist_RL_r)]

    print 'Means: ', means
    print 'Stds: ', stds

    labels = ['Left2Right\nLeft', 'Left2Right\nRight', 'Right2Left\nLeft', 'Right2Left\nRight']

    plt.errorbar(np.array(range(len(means))) + .9, means, stds, marker='o', linestyle='None', \
                 ecolor='#5f9ed1', mfc='#5f9ed1', mec='None', label='Young')
    # plt.axhline(y=0, color='grey', linestyle='--', alpha=0.5)
    plt.xticks(np.array(range(len(means))) + .9, [compat.text_type(s.replace(' ', '\n')) for s in labels])
    plt.yticks(range(1,21), [str(i) for i in range(1,21)])
    plt.xlabel('Phrase discontinuous events')
    plt.ylabel('Distance')

    plt.ylim((1,20))

    plt.savefig('../fig/phrase_discont_dist', dpi=100, bbox_inches='tight')
    plt.close()

    return True


def plot_word_discontinuous_distance():
    # word discontinuous distance
    phrase_discont_dist_LR_l = pickle.load(open('../pickled/word_discont_dist_LR_l.pickle','rb'))
    phrase_discont_dist_LR_r = pickle.load(open('../pickled/word_discont_dist_LR_r.pickle','rb'))
    phrase_discont_dist_RL_l = pickle.load(open('../pickled/word_discont_dist_RL_l.pickle','rb'))
    phrase_discont_dist_RL_r = pickle.load(open('../pickled/word_discont_dist_RL_r.pickle','rb'))

    means = [np.mean(phrase_discont_dist_LR_l), np.mean(phrase_discont_dist_LR_r),
            np.mean(phrase_discont_dist_RL_l), np.mean(phrase_discont_dist_RL_r)]

    stds = [np.std(phrase_discont_dist_LR_l), np.std(phrase_discont_dist_LR_r),
            np.std(phrase_discont_dist_RL_l), np.std(phrase_discont_dist_RL_r)]

    print 'Means: ', means
    print 'Stds: ', stds

    labels = ['Left2Right\nLeft', 'Left2Right\nRight', 'Right2Left\nLeft', 'Right2Left\nRight']

    plt.errorbar(np.array(range(len(means))) + .9, means, stds, marker='o', linestyle='None', \
                 ecolor='#5f9ed1', mfc='#5f9ed1', mec='None', label='Young')
    plt.xticks(np.array(range(len(means))) + .9, [compat.text_type(s.replace(' ', '\n')) for s in labels])
    plt.yticks(range(1,21), [str(i) for i in range(1,21)])
    plt.xlabel('Word discontinuous events')
    plt.ylabel('Distance')

    plt.ylim((1,20))

    plt.savefig('../fig/word_discont_dist', dpi=100, bbox_inches='tight')
    plt.close()

    return True


if __name__ == '__main__':
    # phrase discontinuous distance
    plot_phrase_discontinuous_distance()

    # word discontinuous distance
    plot_word_discontinuous_distance()

    # reordering events frequency wrt German-side phrase len
    plot_phrase_len_reorder()

    # frequency of discontinuous-to-the-left and -to-the-right wrt distance
    plot_phrase_len_discont()