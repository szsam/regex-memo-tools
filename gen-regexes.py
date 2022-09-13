from nltk.parse.generate import generate
from nltk import CFG
import pyparsing as pp
import numpy as np


grammar = CFG.fromstring("""
        #S -> '(' U ')' '*' '(' U ')' '*'
        S -> S S
        S -> '(' T ')'
        S -> '(' T ')' '*' | '(' T ')' '+' | '(' T ')' '?'
        #S -> '(' T ')' '*?' | '(' T ')' '+?' | '(' T ')' '??'
        #S -> '(' T ')' '{3,5}'
        #S -> '(' T ')' '{3,5}?'
        T -> T '|' T
        T -> U
        U -> U U
        U -> 'a'
        """)

# ----------------------------------------------
def do_U(toks):
    #print("U:", len(toks[0]))
    return len(toks[0])

def do_T(toks):
    k = np.lcm.reduce(toks).item()
    #print("T:", toks, k)
    return k

def do_S(toks):
    #print("S:", toks)
    return toks

lp = pp.Char('(').suppress()
rp = pp.Char(')').suppress()
U = pp.Word(pp.alphas).set_parse_action(do_U)
T = U + pp.ZeroOrMore(pp.Char('|').suppress() + U)
T.set_parse_action(do_T)
S = pp.OneOrMore(
        (lp + T.suppress() + rp) ^
        (lp + T + rp + pp.Literal('*').suppress()) ^
        (lp + T + rp + pp.Literal('+').suppress()) ^
        (lp + T + rp + pp.Literal('?').suppress()) ^
        (lp + T + rp + pp.Literal('*?').suppress()) ^
        (lp + T + rp + pp.Literal('+?').suppress()) ^
        (lp + T + rp + pp.Literal('??').suppress()) ^
        (lp + T + rp + pp.Literal('{3,5}').suppress()) ^
        (lp + T + rp + pp.Literal('{3,5}?').suppress()) )
S.set_parse_action(do_S)
#----------------------------------------------------


#print(grammar)

sentences = []
for sentence in generate(grammar, depth=5):
    sentences.append(''.join(sentence))

for s in set(sentences):
    runlen = S.parse_string(s).as_list()
    if runlen:
        print(s, runlen)

#import collections
#print([item for item, count in collections.Counter(sentences).items() if count > 1])
#
#print(len(sentences), len(set(sentences)))

