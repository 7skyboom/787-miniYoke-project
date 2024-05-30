import time
from systemsTest import FmgsTest, ApLATTest, ApLONGTest, StateVectorTest, FcuTest, FccTest, DataSampler
from busTest import AviBusTest

aviBus = AviBusTest(appName="MiniYokeTest", adress="192.168.0.255:2010")

fmgs = FmgsTest()
apLat = ApLATTest()
apLong = ApLONGTest()
stateVector = StateVectorTest()
fcuTest = FcuTest()
fccTest = FccTest(fcuTest)
dataSampler = DataSampler(fmgs, apLat, apLong, stateVector, fcuTest, fccTest)

def testInit():
    global run
    run = True

    print("Welcome to the miniYoke test program")
    # Bind msg here
    aviBus.bindMsg(stateVector.parser, stateVector.parserRegex)
    aviBus.bindMsg(fccTest.nxParser, fccTest.nxRegex)
    aviBus.bindMsg(fccTest.nzParser, fccTest.nzRegex)
    aviBus.bindMsg(fccTest.pParser, fccTest.pRegex)
    aviBus.bindMsg(fccTest.flapsParser, fccTest.flapsRegex)
    aviBus.bindMsg(fccTest.gearParser, fccTest.gearRegex)
    aviBus.bindMsg(fccTest.apAckParser, fccTest.apAckRegex)

    time.sleep(5)

def nzLimitationTest():
    print("Begin nzMax and alphaMax test")
    for msg in stateVector.initRegexs(30, 120, 12.69):
        aviBus.sendMsg(msg)

    dataSampler.run()
    
    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=2.5, 
                 nzMin=-1.5, 
                 pMax=0.7, 
                 pMin=-0.7, 
                 alphaMax=0.5, 
                 alphaMin=-0.5, 
                 phiMaxManuel=1.152, 
                 phiMaxAutomatique=1.52, 
                 fpaMax=0.175, 
                 fpaMin=-0.2)
    msg = fmgs.getRegex()
    aviBus.sendMsg(msg)

    print("please pull the yoke for 10 secs")
    
    time.sleep(10)

    print("please push the yoke for 10 secs")

    time.sleep(10)
    
    dataSampler.stop()
    dataSampler.plotNzLimitation()
    dataSampler.plotFpaLimitation()
    dataSampler.reset()

def pLimitationTest():
    print("Begin p limitation test")
    time.sleep(2)
    for msg in stateVector.initRegexs(30, 120, 12.69):
        aviBus.sendMsg(msg)
    
    dataSampler.run()

    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=2.5, 
                 nzMin=-1.5, 
                 pMax=0.7, 
                 pMin=-0.7, 
                 alphaMax=0.5, 
                 alphaMin=-0.5, 
                 phiMaxManuel=1.152, 
                 phiMaxAutomatique=1.52, 
                 fpaMax=0.175, 
                 fpaMin=-0.5)
    msg = fmgs.getRegex()
    aviBus.sendMsg(msg)

    print("please roll the yoke left for 10 secs")
    time.sleep(3)

    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=2.5, 
                 nzMin=-1.5, 
                 pMax=1.1, 
                 pMin=-1.1, 
                 alphaMax=0.5, 
                 alphaMin=-0.5, 
                 phiMaxManuel=1.152, 
                 phiMaxAutomatique=1.52, 
                 fpaMax=0.175, 
                 fpaMin=-0.5)
    msg = fmgs.getRegex()
    aviBus.sendMsg(msg)

    time.sleep(3)

    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=2.5, 
                 nzMin=-1.5, 
                 pMax=0.3, 
                 pMin=-0.3, 
                 alphaMax=0.5, 
                 alphaMin=-0.5, 
                 phiMaxManuel=1.152, 
                 phiMaxAutomatique=1.52, 
                 fpaMax=0.175, 
                 fpaMin=-0.5)
    
    msg = fmgs.getRegex()
    aviBus.sendMsg(msg)
    time.sleep(4)

    print("please roll the yoke right for 10 secs")

    time.sleep(3)

    fmgs.setData(nxMax=0.5,
                    nxMin=-1,
                    nzMax=2.5,
                    nzMin=-1.5,
                    pMax=1.1,
                    pMin=-1.1,
                    alphaMax=0.5,
                    alphaMin=-0.5,
                    phiMaxManuel=1.152,
                    phiMaxAutomatique=1.52,
                    fpaMax=0.175,
                    fpaMin=-0.5)
    
    msg = fmgs.getRegex()
    aviBus.sendMsg(msg)
    time.sleep(7)

    dataSampler.stop()
    dataSampler.plotPLimitationTest()
    dataSampler.plotPhiLimitationTest()

    dataSampler.reset()

def apTest():
    print("Begin autopilot test")
    time.sleep(2)
    for msg in stateVector.initRegexs(30, 120, 12.69):
        aviBus.sendMsg(msg)

    print("activating autopilot...")
    msg = fcuTest.getRegex()
    aviBus.sendMsg(msg)
    time.sleep(1)

    dataSampler.run()

    apLat.setData(p= 0.3)
    msgLat = apLat.getRegex()
    apLong.setData(nx=0.3, nz=1.6)
    msgLong = apLong.getRegex()
    aviBus.sendMsg(msgLat)
    aviBus.sendMsg(msgLong)

    time.sleep(2)

    apLat.setData(p= -0.4)
    msgLat = apLat.getRegex()
    aviBus.sendMsg(msgLat)

    time.sleep(1)

    apLong.setData(nx=0, nz=2.5)
    msgLong = apLong.getRegex()
    aviBus.sendMsg(msgLong)

    time.sleep(3)

    dataSampler.stop()
    dataSampler.plotApTest()
    
    

def buttonsTest():
    print("Begin buttons test")
    time.sleep(2)
    for msg in stateVector.initRegexs(30, 120, 12.69):
        aviBus.sendMsg(msg)
    
    print("Sending ap push")
    msg = fcuTest.getRegex()
    aviBus.sendMsg(msg)

    print("wait acknoledge response...")
    while fcuTest.apState != 'on':
        print(".")
        time.sleep(1)
    print("acknoledge response received")

    print("please disengage the autopilot")
    while fcuTest.apState != 'off':
        print(".")
        time.sleep(1)
    print("autopilot disengaged")

    print("reengaging autopilot")
    msg = fcuTest.getRegex()
    aviBus.sendMsg(msg)

    print("wait acknoledge response...")
    while fcuTest.apState != 'on':
        print(".")
        time.sleep(1)
    print("acknoledge response received")

    print("please disconnect the autopilot by mooving the yoke")
    while fcuTest.apState != 'off':
        print(".")
        time.sleep(1)
    print("autopilot disconnected")

    print("Testing flaps buttons...")
    print("please extend flaps to 3")
    while fccTest.flaps != 3:
        print(".")
        time.sleep(1)
    print("flaps extended to 3")
    
    print("please retract flaps to 0")
    while fccTest.flaps != 0:
        print(".")
        time.sleep(1)
    print("flaps retracted to 0")

    print("Testing gear button...")
    print("please retract gear")
    while fccTest.gear != True:
        print(".")
        time.sleep(1)

    print("gear retracted")

    print("please extend gear")
    while fccTest.gear != False:
        print(".")
        print(fccTest.gear)
        print("fccTest.gearParser != False", fccTest.gearParser != False)
        time.sleep(1)
    
    print("gear extended")

    print("Button test completed")
    

if __name__ == '__main__':
    testInit()
    try :
        #nzLimitationTest()
        #pLimitationTest()
        #buttonsTest()
        apTest()
    except KeyboardInterrupt:
        aviBus.stop()
    