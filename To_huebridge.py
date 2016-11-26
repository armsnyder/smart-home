import phue


# bridge = phue.Bridge() # include IP address here


class fireplace(object):
    def __init__(self, flicker_function):
        self.flicker = flicker_function
        self.running = False

    def start(self):
        self.running = True
        self.run()
        return

    def stop(self):
        self.running = False
        return

    def run(self):
        if self.running:
            self.flicker()
            self.run()
        return

