# Your task is to build a translation model. You have to implement and compute the following for
# both data sets (clean and web):
# 1. Phrase extraction algorithm
# 2. Phrase translation probabilities
# 3. Lexical translation probabilities (KMO approach)
# 4. The resulting files of (1-3) can be combined into one single file of the form:
import timeit,pickle
import part1
import part2
# import part3
# import part4


def do_part_1():
    f_en = open('../data/file.en', 'r')
    f_de = open('../data/file.de', 'r')
    f_align = open('../data/file.aligned', 'r')

    en = f_en.readlines()
    de = f_de.readlines()
    align = f_align.readlines()

    de_p, en_p, de_freq, en_freq, c_freq = part1.phrase_extraction(de, en, align)

    f_en.close()
    f_de.close()
    f_align.close()

    pickle.dump(de_p, open('../pickled_files/de_p.pickle', "wb"))
    pickle.dump(en_p, open('../pickled_files/en_p.pickle', "wb"))
    pickle.dump(de_freq, open('../pickled_files/de_freq.pickle', "wb"))
    pickle.dump(en_freq, open('../pickled_files/en_freq.pickle', "wb"))
    pickle.dump(c_freq, open('../pickled_files/c_freq.pickle', "wb"))

    return de_p, en_p, de_freq, en_freq, c_freq


def get_part_1():
    de_p = pickle.load(open('../pickled_files/de_p.pickle', "rb"))
    en_p = pickle.load(open('../pickled_files/en_p.pickle', "rb"))
    de_freq = pickle.load(open('../pickled_files/de_freq.pickle', "rb"))
    en_freq = pickle.load(open('../pickled_files/en_freq.pickle', "rb"))
    c_freq = pickle.load(open('../pickled_files/c_freq.pickle', "rb"))

    return de_p, en_p, de_freq, en_freq, c_freq


def make_output(*args):

    if args[0] == 'part1':
        f = open('../output/' + args[0] + '.txt', 'w')

        f_p = args[1]
        e_p = args[2]
        f_freq = args[3]
        e_freq = args[4]
        c_freq = args[5]
        for i in range(len(f_p)):
            for item in [f_p[i], '|||', e_p[i], '|||', f_freq[i], e_freq[i], c_freq[i]]:
                f.write(item)

    if args[0] == 'part2':
        f = open('../output/' + args[0] + '.txt', 'w')

        f_p = args[1]
        e_p = args[2]
        p_fe = args[3]
        p_ef = args[4]
        for i in range(len(f_p)):
            for item in [f_p[i], '|||', e_p[i], '|||', p_fe[i], p_ef[i]]:
                f.write(item)

    if args[0] == 'part3':
        f = open('../output/' + args[0] + '.txt', 'w')

        f_p = args[1]
        e_p = args[2]
        p_fe = args[3]
        p_ef = args[4]
        l_fe = args[5]
        l_ef = args[6]
        for i in range(len(f_p)):
            for item in [f_p[i], '|||', e_p[i], '|||', p_fe[i], p_ef[i], l_fe[i], l_ef[i]]:
                f.write(item)

    if args[0] == 'combine':
        f = open('../output/' + args[0] + '.txt', 'w')

        f_p = args[1]
        e_p = args[2]
        p_fe = args[3]
        p_ef = args[4]
        l_fe = args[5]
        l_ef = args[6]
        f_freq = args[7]
        e_freq = args[8]
        c_freq = args[9]
        for i in range(len(f_p)):
            for item in [f_p[i], '|||', e_p[i], '|||', p_fe[i], p_ef[i], l_fe[i], l_ef[i], '|||', f_freq[i], e_freq[i], c_freq[i]]:
                f.write(item)

    f.close()


# TODO make output file for part 1

# de_p, en_p, de_freq, en_freq, c_freq = do_part_1()
d_p, e_p, d_freq, e_freq, c_freq = get_part_1()
make_output('part1', d_p, e_p, d_freq, e_freq, c_freq)

p_de, p_ed = part2.phrase_probabilities(d_freq, e_freq, c_freq)
make_output('part2', d_p, e_p, p_de, p_ed)

l_de, l_ed = part3.lexical_probabilities()
make_output('part3', d_p, e_p, p_de, p_ed, l_de, l_ed)

make_output('combine', d_p, e_p, p_de, p_ed, l_de, l_ed, d_freq, e_freq, c_freq)