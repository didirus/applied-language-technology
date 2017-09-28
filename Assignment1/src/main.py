# Your task is to build a translation model. You have to implement and compute the following for
# both data sets (clean and web):
# 1. Phrase extraction algorithm
# 2. Phrase translation probabilities
# 3. Lexical translation probabilities (KMO approach)
# 4. The resulting files of (1-3) can be combined into one single file of the form:
import timeit
import part1
import part2
# import part3
# import part4

f_en = open('../data/file.en', 'r')
f_de = open('../data/file.de', 'r')
f_align = open('../data/file.aligned', 'r')

en = f_en.readlines()
de = f_de.readlines()
align = f_align.readlines()

start = timeit.default_timer()
de_p, en_p, de_freq, en_freq, c_freq = part1.phrase_extraction(de, en, align)
# TODO make output file for part 1
stop = timeit.default_timer()
print(stop - start)

part2.phrase_probabilities(de_freq, en_freq, c_freq)
# part3.lexical_probabilities()
# part4.combine()

f_en.close()
f_de.close()
f_align.close()