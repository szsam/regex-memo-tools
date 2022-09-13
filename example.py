import re

p = re.compile("(aa)*(aaaa)*", re.DEBUG, runlen=[2, 4])
m = p.fullmatch("a"*20 + "b")
print(p.memostat)
