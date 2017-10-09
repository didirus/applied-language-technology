import matplotlib.pyplot as plt
import pickle


def create_orientation_histograms(counts_dict, phrase_length):
    i = 0
    for direction in counts_dict.keys():
        for orientation, countsname in counts_dict[direction].items():
            print(direction, orientation)
            counts = get_counts(countsname)
            orientation_count_hash = {}
            for line in counts:
                if len(line[0]) == phrase_length or len(line[1]) == phrase_length:
                    if counts[line] not in orientation_count_hash:
                        orientation_count_hash[counts[line]] = 0
                    orientation_count_hash[counts[line]] += 1

            plt.figure(i)
            plt.bar(orientation_count_hash.keys(), orientation_count_hash.values(), 1.0, color='g')
            plt.title(direction + ' ' + orientation)
            plt.show()
            i += 1


def get_counts(name):
    counts = pickle.load(open('../small-pickled/' + name + '.pickle', 'rb'))
    return counts


counts_dict = {}

counts_dict['left-right'] = {
                             'swap': 'count_phrase_LR_s',
                             'discontinuity-left': 'count_phrase_LR_dl',
                             'discontinuity-right': 'count_phrase_LR_dr',
                             'monotone': 'count_phrase_LR_m'
                            }

counts_dict['right-left'] = {
                             'swap': 'count_phrase_RL_s',
                             'discontinuity-left': 'count_phrase_RL_dl',
                             'discontinuity-right': 'count_phrase_RL_dr',
                             'monotone': 'count_phrase_RL_m'
                            }

create_orientation_histograms(counts_dict, 7)

