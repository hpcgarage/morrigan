#!/usr/bin/env python3

# Automating steps from here: https://www.spec.org/cpu2017/Docs/runcpu-avoidance.html

import sys
import os
import re
from os.path import exists

config="patrick"

try:
    spechome = os.environ['SPEC']
except:
    print("Unable to find SPEC location in evironment")
    sys.exit(1)

if (spechome == ""):
    print("Couldn't find spec location")
    sys.exit(1)

if (not exists("benchmarks.txt")):
    print("Missing benchmarks.txt")
    sys.exit(1)

benchmark = []
with open("benchmarks.txt", "r") as benchfile:
    lines = benchfile.readlines()
    for line in lines:
        bench = "".join(line.split())
        if bench == "" or bench[0] == "#":
            continue
        benchmark.append(bench)

if (len(benchmark) == 0):
    print("No benchmarks specified.")
    sys.exit(1)

print("Configs will be generated for {}".format(benchmark))

# Execute fake run to set up directories

step1 = {}
for bench in benchmark:
    out = os.popen("runcpu --fake --loose --size test --tune base --config {} {}".format(config, bench)).read()
    regex = "Success:.*" + re.escape(bench)
    if (re.search(regex, out)):
        step1[bench] = "success"
    else:
        step1[bench] = "failure"

print("Step 1:")
print(step1)

rundir = os.getcwd()


step2 = {}
step3 = {}

for bench in benchmark:
    bindir = spechome+"/benchspec/CPU/{}/run/run_base_test_mrgn-m64.0000".format(bench)
    try:
        os.chdir(bindir)
    except:
        print("Unable to change to benchmark directory")
        step2[bench] = "failure"
        continue
    step2[bench] = "success"


    # run specinvoke
    out = os.popen("specinvoke -n").read()

    for line in out.splitlines():
        x = re.findall("^#", line)
        if x:
            continue
        x = re.findall("^specinvoke", line)
        if x:
            continue
        print(line)


print(step2)


