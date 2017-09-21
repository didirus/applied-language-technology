import numpy as np

def phrase_probabilities(e=None, d=None, f_e=None,f_d=None, c_fe=None):

    """

    :param e: Phrase in english
    :param d: Phrase in deu
    :param f_e: Frequency of english phrase
    :param f_d: Frequency of deu phrase
    :param c_fe: Count when e-d allign
    :return: Probability P(e|d) and P(d|e)
    """

    p_ed = np.zeros(len(e),dtype=float)
    p_de = np.zeros(len(e),dtype=float)

    for i in range(len(e)):
        N_r = c_fe[i]
        D_r1 = f_d[i]
        D_r2 = f_e[i]
        p_ed[i]= (N_r/D_r1)
        p_de[i] = (N_r/D_r2)

    return p_ed, p_de
# test
e = np.array(['resumption', 'red','blue'])
d = np.array(['rs','r','b'])
f_e = np.array([1,2,3],dtype=float)
f_d = np.array([3,2,1],dtype=float)
c_fe = np.array([1,2,1],dtype=float)
phrase_probabilities(e=e,d=d,f_e=f_e,f_d=f_d,c_fe=c_fe)

