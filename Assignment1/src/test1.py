from collections import defaultdict

DATA_DIR  = '../data/'

#Loaded files
f_en = open('../data/file.en', 'r')
f_de = open('../data/file.de', 'r')
f_align = open('../data/file.aligned', 'r')
print (type(f_en))
# print (len(f_en))

for line_aligned in zip(f_align):
    print type(line_aligned)
    alignments = []
    alignments_temp = str(line_aligned).replace("\n","").split(" ")
    print (alignments_temp)