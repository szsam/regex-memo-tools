# regex-memo-tools

## Python regex engine that implements memoization
https://github.com/szsam/cpython/tree/regex-memo-test

Compile the project and set the environment variable 
``` bash
export MYPYTHON=/path/to/python/binary
```

## Basic usage
The function `re.compile()` takes a new argument `runlen` to specify the run lengths used for each instruction to be memoized marked by `MEMO`.

Statistics on memoization, such as max # of runs and final # of runs, can be obtained by calling `memostat` member of the regular expression object returned by `re.compile`.

See the following example:
``` Python
# example.py
import re

# 2 for (aa)*, 4 for (aaaa)*
p = re.compile("(aa)*(aaaa)*", re.DEBUG, runlen=[2, 4])
m = p.fullmatch("a"*20 + "b")
print(p.memostat)
```
Run it with
``` bash
$MYPYTHON example.py 
```
Output is
```
MAX_REPEAT 0 MAXREPEAT
  SUBPATTERN 1 0 0
    LITERAL 97
    LITERAL 97
MAX_REPEAT 0 MAXREPEAT
  SUBPATTERN 2 0 0
    LITERAL 97
...

 0. INFO 4 0b0 0 MAXREPEAT (to 5)
 5: REPEAT 11 0 MAXREPEAT (to 17)
 9.   MARK 0
11.   LITERAL 0x61 ('a')
13.   LITERAL 0x61 ('a')
15.   MARK 1
17: MEMO
18. MAX_UNTIL # inst0
19. REPEAT 15 0 MAXREPEAT (to 35)
23.   MARK 2
25.   LITERAL 0x61 ('a')
...
33.   MARK 3
35: MEMO
36. MAX_UNTIL # inst1
37. SUCCESS
{'runlen': [2, 4], 'max_n_runs': [1, 3], 'final_n_runs': [1, 2]}
# inst0: runlen[0]=2, max_n_runs=1, final_n_runs=1
# inst1: runlen[1]=4, max_n_runs=3, final_n_runs=2
```

# mytest.py
Read regexes and run lengths from a file. For each regex, run `fullmatch` on inputs `"a"`, `"aa"`, ..., `"a"*N`. The amount of work is divided evenly to cpu cores. Each line in the file is a regex followed by a run length list. A sample file:
```
# regexes-two-star.txt
(a)*(a)* [1,1]
(a)*(aa)* [1,2]
(a)*(aaa)* [1,3]
````
Run this test script by `$MYPYTHON mytest.py regexes-two-star.txt`. You can submit the job to bell cluster by `sbatch run.sub mytest.py regexes-two-star.txt`.

# visualize-seq.py
This script visualizes how the visit vector evolves during the matching process by parsing the log of regex engine. Red means the bit is set, and blue means the bit is read.

<img src="https://github.com/szsam/regex-memo-tools/blob/main/visit-vector-visualization.jpg" width="300">

You need to modify line 126 of `cpython/Modules/sre.h` to set log level to `verbose` or higher, e.g. `#define LOG_THRESHOLD  LOG_VERBOSE`. Compile then run `python3 visualize-seq.py`.

# gen-regexes.py
Enumerate all sentences from a context free grammar. This can be used to generate all regexes matching a grammar.

See [here](https://www.nltk.org/api/nltk.parse.generate.html) for details of `nltk` API.
