#!/usr/bin/python
import sys
import threading
import jobthread as jt
import collections
import fns
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
            gv.cnt += 1
            job = job.split()
            job =  [ int(x) for x in job ]
            tmp.append(job)

        jobs = tmp

        for job in jobs:
            jobQueue.appendleft(job)


def enter_new_jobs(time, jobs):
    global newjob
    global running_job
    global running_queue
    global newjob_queue

    if not jobs:
        return
    next_job = jobs.pop()

    while(next_job[1] == time):
        newjob = True
        ID,AT,Dur = next_job
        newjob_queue.appendleft(jt.jobthread(ID, Dur, AT, time))
        newjob_queue[0].start()
        if not jobs:
            return
        next_job = jobs.pop()

    jobs.append(next_job)


def scheduler_service_routine(time):
    global results
    global running_job
    global running_queue
    global newjob_queue
    global newjob
    global slice_cnt

    if not running_job:
        if newjob_queue:
            running_job = newjob_queue.pop()
        elif running_queue:
            running_job = running_queue.pop()
        else:
            return

    state = running_job.decTime(time)

    if(state == "TERMINATED"):
        slice_cnt = 0
        results.append(running_job.get_stats())
        running_job.stop()
        running_job.join()
        jobs_left = len(running_queue)
        pad = " " * (4 - jobs_left)
        sys.stdout.write("{}{} processes in memory\r".format(jobs_left, pad))
        sys.stdout.flush()
        if newjob_queue:
            next_job = newjob_queue.pop()
        elif running_queue:
            next_job = running_queue.pop()
        elif not running_job.is_alive():
            return
        else:
            next_job = running_job

        running_job = next_job
        running_job.go(time)
    elif(slice_cnt % gv.time_slice == 0 and slice_cnt > 0):
        if newjob_queue:
            next_job = newjob_queue.pop()
        elif running_queue:
            next_job = running_queue.pop()
        elif not running_job.is_alive():
            return
        else:
            next_job = running_job

        if(state == "TERMINATED"):
            slice_cnt = 0
            results.append(running_job.get_stats())
            running_job.stop()
            running_job.join()
            sys.stdout.write("{} processes in memory\r".format(len(running_queue)))
            sys.stdout.flush()
        else:
            running_job.pause()
            running_queue.appendleft(running_job)

        running_job = next_job
        running_job.go(time)


if __name__ == "__main__":
    jobQueue = collections.deque()
    running_queue = collections.deque()
    newjob_queue = collections.deque()
    avgTAT = 0
    slice_cnt = 0
    results = []

    TIM = threading.Event()
    newjob = False
    running_job = None

try:
    print("Starting Round Robin simulation: (CTRL-C to exit)")
    init()
    while(1):
        enter_new_jobs(gv.CurrT, jobQueue)
        scheduler_service_routine(gv.CurrT)
        gv.CurrT += 1
        slice_cnt += 1
        if(not running_queue and not jobQueue and not running_job.is_alive()):
            break

    print("\n")
    fns.print_results(results)
except Exception, e:
    print e
    if running_job:
        running_job.stop()
        running_job.join()

    for job in running_queue:
        job.stop()
        job.join()
        print("thread id: {} killed".format(job.name))
except KeyboardInterrupt:
    if running_job:
        running_job.stop()
        running_job.join()

    for job in running_queue:
        job.stop()
        job.join()
        print("thread id: {} killed".format(job.name))

    sys.exit(1)
