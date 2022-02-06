"""创建一个回调函数，当所有的回调都运行了以后，就调用success"""
class CountDownLatch:
    def __init__(self, success):
        self.chainNum = 0
        self.success = success
        self.callbackCount = 0
        self.numCalled = 0
    def createCallback(self):
        self.callbackCount += 1
        def callback():
            self.numCalled += 1
            if(self.numCalled == self.callbackCount):
                self.success()
        return callback