import subprocess
import random
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def encrypt(string, length):
    return ' '.join(string[i:i+length] for i in range(0,len(string),length))

def encrypt2(string, idx, bcolor):
    return (''.join(string[0:idx]) + bcolor
            + string[idx] + bcolors.ENDC + ''.join(string[idx+1:]))

def getstring(arr, times):
    indices = [random.randrange(len(arr)) for _ in range (times)]
    string = ''.join(arr[i] for i in indices)
    return string

def runshell(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def main():
    #REGEX = "(a|bb)*?(a|aa|bb)*"
    #REGEX = "(aa|b)*(a|bb)*(a|aa|bb)*"
    #INPUT = r"'aaaaabb'*100000 + 'z'"
    #REGEX = "(aa|bb|aabba|abbbba)*(a|bb)*"
    REGEX = "(aa|bb|a|b)*(a|bb)*"
    INPUT = r"'aabb' + 'aaaabbbb'*2 + 'z'"
    #INPUT = r"'aaaaabbbbdddaaz'"
    #INPUT = ''.join("a"*i+"bb" for i in [5,6,7]) + "z"
    #REGEX = "(a|aa|bb)*"
    #INPUT = getstring(['a', 'bb'], 10) + "z"
    print(REGEX)
    print(INPUT)
    print(eval(INPUT))

    cmd = '''"import re
print('testre start')
p = re.compile('{}', re.DEBUG, runlen=[2, 2])
p.fullmatch({})
print(p.memostat)"'''.format(REGEX, INPUT)
    #print(cmd)

    subprocess.run("$MYPYTHON -u -c " + cmd + " > out", shell=True)
    subprocess.run("sed -i '0,/^testre start$/d' out", shell=True)
    cp = runshell("grep '_create' out | head -n 2 | tail -n 1 | awk '{printf \"%s\", $4}'")
    addr = cp.stdout
    cp = runshell(f"egrep 'RLEVector_(set|get): vec {addr}' out")
    logs = cp.stdout

    vec = ['0']*(len(eval(INPUT))+1)
    for line in logs.splitlines():
        m = re.search(r"set.*idx (\d+)", line)
        if m:
            idx = int(m.group(1))
            vec[idx] = '1'
            #print("S", idx)
            print(encrypt2(''.join(vec), idx, bcolors.FAIL))
        m = re.search(r"get.*idx (\d+), return 1", line)
        if m:
            idx = int(m.group(1))
            #print("G", idx)
            print(encrypt2(''.join(vec), idx, bcolors.OKBLUE))

    # memo stat
    cp = runshell("grep 'runlen' out")
    print(cp.stdout)


if __name__ == "__main__":
    main()
