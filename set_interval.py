# https://stackoverflow.com/a/48709380

import time, threading

class setInterval:
    def __init__(self, interval, skipper, token):
        self.interval = interval
        self.skipper = skipper
        self.token = token
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.skipper(self.token)

    def cancel(self):
        self.stopEvent.set()
