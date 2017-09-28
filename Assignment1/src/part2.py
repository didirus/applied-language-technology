import numpy as np

def phrase_probabilities(freq_e=None,freq_f=None, c_freq=None):

    """

    :param freq_e: Frequency of English phrase
    :param freq_f: Frequency of deu phrase
    :param c_freq: Count when e-d allign
    :return: Probability P(e|d) and P(d|e)
    """


    p_ef = np.zeros(len(freq_e),dtype=float)
    p_fe = np.zeros(len(freq_f),dtype=float)

    for i in range(len(e)):
        N_r = c_freq[i]
        D_r1 = freq_f[i]
        D_r2 = freq_e[i]
        p_ef[i]= (N_r/D_r1)
        p_fe[i] = (N_r/D_r2)

    return p_ef, p_fe
# test
e = np.array(['resumption', 'red','blue'])
d = np.array(['rs','r','b'])
f_e = np.array([1,2,3],dtype=float)
f_d = np.array([3,2,1],dtype=float)
c_fe = np.array([1,2,1],dtype=float)
phrase_probabilities(e=e,d=d,f_e=f_e,f_d=f_d,c_fe=c_fe)

