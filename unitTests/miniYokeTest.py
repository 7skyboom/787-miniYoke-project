import time,threading
from systemsTest import FmgsTest, ApLATTest, ApLONGTest, StateVectorTest, FcuTest, FccTest, DataSampler
from busTest import AviBusTest

aviBus = AviBusTest(appName="MiniYokeTest", prod=True)

fmgs = FmgsTest()
apLat = ApLATTest()
apLong = ApLONGTest()
stateVector = StateVectorTest()
fcuTest = FcuTest()
fccTest = FccTest()
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

    time.sleep(10)

def nzAlphaMaxtest():
    print("Begin nzMax and alphaMax test")
    dataSampler.run()
    for msg in stateVector.initRegexs(30, 120, 12.69):
        aviBus.sendMsg(msg)
    
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

    print("please pull the yoke for 10 secs")
    time.sleep(3)
    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=1, 
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
    time.sleep(3)

    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=1.75, 
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
    time.sleep(4)
    
    dataSampler.stop()
    dataSampler.plotFirstTestData()
    dataSampler.reset()
    
def nzAlphaMintest():
    pass

def nxAlphaMaxtest():
    pass

def main():
    pass

if __name__ == '__main__':
    testInit()
    nzAlphaMaxtest()
    try :
        while run:
            main()
    except KeyboardInterrupt:
        run = False
        aviBus.stop()
    #plot results