#!/usr/bin/python
import sys
import random
import time

random.seed(time.time())

arriveTime = 0

jobs = []

jobQueue = []

for _ in range(0,100):
    duration = random.randint(1,1000)
    next_job = 0
    while(next_job in jobs):
        next_job = random.randint(0, 1000)

    job_info = (next_job, arriveTime, duration)
    jobs.append(next_job)
    jobQueue.append(job_info)

    if(random.randint(1,4) != 1):
        arriveTime = arriveTime + random.randint(1, 100)


try:
	if len(sys.argv) in range(2,3):
		f = open(sys.argv[1], "w+")
	else:
		f = open("jobs.dat", "w+")
except IOError:
	print("Error Creating File")
	sys.exit(1)

for job in jobQueue:
    f.write("{0}    {1}    {2}\n".format(job[0],job[1],job[2]))

f.close()
