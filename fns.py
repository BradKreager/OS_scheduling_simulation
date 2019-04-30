import threading
import globalvars as gv

def print_results(d):

    avgTAT = 0
    avgRT = 0
    print("ID : Start Time\t\tFinish Time\t\tTotal Time\t\tResponse Time\n")

    maxIDlen = len( str( max([ x["ID"] for x in d ]) ) )

    for data in d:
        pad = ' ' * (maxIDlen - len(str(data["ID"])))
        padST = ' ' * (len("Start Time") - len(str(data["ST"])))

        padFT = ' ' * (len("Finish Time") - len(str(data["FT"])))

        padTT = ' ' * (len("Total Time") - len(str(data["TT"])))

        print("{0}{5}: {1}{6}\t\t{2}{7}\t\t{3}{8}\t\t{4}".format(str(data["ID"]), str(data["ST"]), str(data["FT"]), str(data["TT"]), str(data["RT"]), pad, padST, padFT, padTT))

    for data in d:
        avgTAT += int(data["TT"])
        avgRT += int(data["RT"])

    avgTAT = avgTAT / gv.cnt
    avgRT = avgRT / gv.cnt
    print("\nProcess Count: {}".format(gv.cnt))
    print("\nAverage Turn-Around-Time: {}".format(str(avgTAT)))
    print("\nAverage Response-Time: {}".format(str(avgRT)))


def timer_int(time, job):
    job.time_event()
    job.updateTime(time)
    while not job.in_sync():
        continue
    return time

def sjf(arr):
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
            tmp.sort(key = lambda x: x[2])
            arr[base:curr] = tmp
        base = curr

def sort_time_left(arr):
    minTime = min([x.remainingTime for x in arr])
    for job in arr:
        if(job.remainingTime == minTime):
            return job
    return None
