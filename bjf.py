#!/usr/bin/python
import sys
import random
import time
import copy
import fns
import globalvars as gv

def bjf(arr):
    base = 0
    curr = 0
    while(curr < len(arr)):
        tmp = []
        curr = curr + 1
        if curr == len(arr):
            break
        tmp.append(arr[base])
        while(arr[base][1] == arr[curr][1] and curr < len(arr)):
            tmp.append(arr[curr])
            curr = curr + 1
        if len(tmp) > 1:
            tmp.sort(key = lambda x: x[2], reverse = True)
            arr[base:curr] = tmp
        base = curr


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
    tmp = []
    for job in jobs:
        job = job.split()
        job =  [ int(x) for x in job ]
        tmp.append(job)

    jobs = tmp

    bjf(jobs)

    for job in jobs:
        gv.cnt = gv.cnt + 1
        ID,AT,Dur = job
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
