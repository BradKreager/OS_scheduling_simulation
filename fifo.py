#!/usr/bin/python
import sys
import random
import time
import copy
import fns
import globalvars as gv


results = []

try:
    if len(sys.argv) in range(2,3):
        f = open(sys.argv[1], "r")
    else:
        f = open("jobs.dat", "r")
except IOError:
    print("file not found")
    sys.exit(1)
else:
    jobs = f.read().splitlines()
    f.close()
    for job in jobs:
        gv.cnt = gv.cnt + 1
        ID,AT,Dur = job.split()
        ID = int(ID)
        AT = int(AT)
        Dur = int(Dur)
        startTime = gv.CurrT
        completionTime = gv.CurrT + Dur
        gv.CurrT = completionTime
        TAT = completionTime - AT
        responseTime = startTime - AT
        stats = {
            "ID": ID,
            "ST": startTime,
            "FT": completionTime,
            "TT": TAT,
            "RT": responseTime
        }
        results.append(stats)

	fns.print_results( results )
