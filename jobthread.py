import threading
import sys
import time
import globalvars as gv

class jobthread(threading.Thread):
    """        """
    def __init__(self, id, dur, arrvT, time):
        """                """
        threading.Thread.__init__(self)
        self.name = id
        self.time = time
        self.intTIM = threading.Event()
        self._done = threading.Event()
        self.AT = arrvT
        self.ST = 0
        self.TT = 0
        self.Duration = dur
        self.remainingTime = dur
        self.state = "NEW"
        self.paused = True
        self.RT = 0

    def run(self):
        while not self._done.is_set():
            if not self.paused:
                if self.remainingTime == 0:
                    self.state = "TERMINATED"
                    self.paused = True

    def pause(self):
        self.state = "WAITING"
        self.paused = True

    def go(self, time):
        if self.state == "NEW":
            self.ST = time

        self.state = "RUNNING"
        self.paused = False

    def updateTime(self, time):
        self.time = time

    def decTime(self, time):
        self.remainingTime -= 1
        if self.remainingTime <= 0:
            self.time = time
            self.remainingTime = 0
            self.state = "TERMINATED"
            self.paused = True

        return self.state

    def stop(self):
        self._done.set()

    def time_event(self):
        self.intTIM.set()

    def in_sync(self):
        if self.intTIM.is_set():
            return False
        else:
            return True

    def get_time_left(self):
        return self.remainingTime

    def get_stats(self):
        startTime = self.ST
        stats = {
            "ID": self.name,
            "ST": self.ST,
            "FT": self.time,
            "TT": self.time - self.AT,
            "RT": (self.ST - self.AT)
        }
        return stats

