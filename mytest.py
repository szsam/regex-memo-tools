import re
#import concurrent.futures
import multiprocessing
import math
import json
import argparse

#REGEX = "(" + "a"*7 + "|" + "a"*9 + ")*"
#RUNLEN = [63, 1]

#REGEX = "(aaa)*(a|aa)(aa)*"
#RUNLEN = [3,6]

def do_test(regex, start, end, runlen):
    #print("args:", regex, start, end, runlen)
    patt = re.compile(regex, runlen=runlen)
    results = []
    for l in range(start, end):
        input_str = "a"*l + "z"
        m = patt.fullmatch(input_str)
        results.append(patt.memostat)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    #regexes = ["(aaa)*?(aaaa)*"]
    #runlens = [[3, 4]]

    regexes, runlens = [], []
    with open(args.filename) as f:
        #regexes = [line.rstrip() for line in f]
        for line in f:
            line = line.split(maxsplit=1)
            regex, runlen = line[0], line[1].rstrip()
            runlen = json.loads(runlen)
            regexes.append(regex)
            runlens.append(runlen)

    #print(regexes, runlens)
    #regexes = regexes[:100]
    #runlens = runlens[:100]

    #with concurrent.futures.ProcessPoolExecutor() as executor:
    num_cores = 64
    N = 10000
    print("N=1:{}".format(N))

    for regex, runlen in zip(regexes, runlens):
        print(regex, runlen)
        with multiprocessing.Pool(num_cores) as pool:
            args = [(regex, math.floor(N*math.sqrt(k/num_cores)),
                     math.floor(N*math.sqrt((k+1)/num_cores)),
                     runlen) for k in range(num_cores)]
            results = pool.starmap(do_test, args)
            results = [item for sublist in results for item in sublist]
            #[print(item) for item in results]
            lst_final_runs  = [item['final_n_runs']  for item in results]
            lst_max_runs    = [item['max_n_runs']    for item in results]

            final_runs_bound = [max(v) for v in zip(*lst_final_runs)]
            max_runs_bound = [max(v) for v in zip(*lst_max_runs)]

            for i,(r,f,m) in enumerate(zip(runlen, final_runs_bound, max_runs_bound)):
                print("[vertex {}] runlen: {}, final_n_runs_bound: {}, max_n_runs_bound: {}".format(
                    i, r, f, m))


if __name__ == "__main__":
    main()
