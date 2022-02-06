class RunEntry():
    def __init__(self, startFrame, frameParam, func, isInterval):
        self.startFrame = startFrame
        self.frameParam = frameParam
        self.isInterval = isInterval
        self.func = func

    def needToRun(self, frameNow):
        e = frameNow - self.startFrame
        if self.isInterval:  # 按间隔运行
            if(e % self.frameParam == 0):
                return True
        elif e >= self.frameParam:  # 只运行一次
            return True
        return False

    def run(self, frameNow):
        if(self.needToRun(frameNow)):
            self.func()
            return True
        return False


class FrameRunner():
    """ """

    def __init__(self):
        self.currentFrame = 0
        self.entries = []

    def update(self):
        """update"""
        for i in range(0, len(self.entries)):
            e = self.entries[i]
            if e is not None and e.run(self.currentFrame):
                if(not e.isInterval):
                    self.entries[i] = None
        self.currentFrame += 1

    def setTimeout(self, func, frameCount):
        entry = RunEntry(self.currentFrame, frameCount, func, False)
        return self.append(entry)

    def clearTimeout(self, instanceId):
        self.entries[instanceId] = None

    def setInterval(self, func, frameCount):
        entry = RunEntry(self.currentFrame, frameCount, func, True)
        return self.append(entry)

    def clearInterval(self, instanceId):
        self.entries[instanceId] = None

    def append(self, entry):
        for i in range(0, len(self.entries)):
            e = self.entries[i]
            if(e is None):
                self.entries[i] = entry
                return i
        self.entries.append(entry)
        return len(self.entries)-1
