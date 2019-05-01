#!/usr/bin/python
import sys
import random
import time
import threading
import copy
import jobthread as jt
import collections
import Queue
import fns
import copy
import globalvars as gv


def init():
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

        for job in jobs:
            jobQueue.appendleft(job)



def enter_new_jobs(time, jobs, mem):
    global newjob
    global running_job
    global sort
    if not jobs:
        return
    next_job = jobs.pop()
    while(next_job[1] == time):
        gv.cnt += 1
        newjob = True
        ID,AT,Dur = next_job
        mem.append(jt.jobthread(ID, Dur, AT, time))
        if running_job:
            if mem[-1].Duration < running_job.remainingTime:
                sort = True
        mem[-1].start()
        if not jobs:
            return

        next_job = jobs.pop()

    jobs.append(next_job)

def scheduler_service_routine(time, jobs):
    global results
    global running_job
    global newjob
    global sort


    if running_job:
        state = running_job.decTime(time)

    if(running_job and running_job.state == "TERMINATED"):
        results.append(running_job.get_stats())
        running_job.stop()
        running_job.join()
        jobs_left = len(jobs)
        pad = " " * (4 - jobs_left)
        sys.stdout.write("{}{} processes in memory\r".format(jobs_left, pad))
        sys.stdout.flush()
        jobs.remove(running_job)
        running_job = None
        if not jobs:
            return

    if running_job:
        running_job.pause()

    if newjob:
        if sort:
            running_job = fns.sort_time_left(jobs)
            sort = False
            newjob = False

    if running_job:
        running_job.go(time)
    else:
        running_job = fns.sort_time_left(jobs)
        running_job.go(time)



if __name__ == "__main__":
    jobQueue = collections.deque()
    sort = True

    results = []

    jobs_in_mem = []

    newjob = False
    running_job = None

try:
    print("Starting STCF simulation: (CTRL-C to exit)")
    init()
    while(1):
        enter_new_jobs(gv.CurrT, jobQueue, jobs_in_mem)
        scheduler_service_routine(gv.CurrT, jobs_in_mem)
        if(not jobs_in_mem and not jobQueue):
            break
        gv.CurrT += 1

    print("\n")
    fns.print_results(results)
except Exception, e:
    print(e)
    if jobs_in_mem:
        for job in jobs_in_mem:
            job.stop()
            job.join()
            print("thread id: {} killed".format(job.name))
    sys.exit(1)
except KeyboardInterrupt:
    if jobs_in_mem:
        for job in jobs_in_mem:
            job.stop()
            job.join()
            print("thread id: {} killed".format(job.name))

    sys.exit(1)
except:
    if jobs_in_mem:
        for job in jobs_in_mem:
            job.stop()
            job.join()
            print("thread id: {} killed".format(job.name))

    sys.exit(1)
