from ivy.std_api import *

def on_cx_proc(agent, connected):
    print("Agent {} is {}connected".format(agent, "" if connected else "dis"))

def on_die_proc(agent):
    print("Agent {} has died".format(agent))

class AviBusTest :
    def __init__(self, appName, prod):
        self.prod = prod
        self.appName = appName
        #self.adress = "224.255.255.255:2010" if self.prod else "127.0.0.1:8000"
        self.adress = "192.168.0.255:2010" if self.prod else "127.0.0.1:8000"

        IvyInit(self.appName, "hello, world !", 0, on_cx_proc, on_die_proc)
        IvyStart(self.adress)

    def sendMsg(self, msg):
        IvySendMsg(msg)
    
    def bindMsg(self, callback, regex):
        IvyBindMsg(callback, regex)
    
    def stop(self):
        IvyStop()