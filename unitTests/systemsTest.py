import time,threading
import matplotlib.pyplot as plt

class FmgsTest():
    def __init__(self):
        self.nxMax = 0
        self.nxMin = 0
        self.nzMax = 0
        self.nzMin = 0
        self.pMax = 0
        self.pMin = 0
        self.alphaMax = 0
        self.alphaMin = 0
        self.phiMaxManuel = 0
        self.phiMaxAutomatique = 0
        self.fpaMax = 0
        self.fpaMin = 0
        self.regex = 'Performances NxMax={} NxMin={} NzMax={} NzMin={} PMax={} PMin={} AlphaMax={} AlphaMin={} PhiMaxManuel={} PhiMaxAutomatique={} GammaMax={} GammaMin={}'

        self.nxMaxData = []
        self.nxMinData = []
        self.nzMaxData = []
        self.nzMinData = []
        self.pMaxData = []
        self.pMinData = []
        self.alphaMaxData = []
        self.alphaMinData = []
        self.phiMaxManuelData = []
        self.phiMaxAutomatiqueData = []
        self.fpaMaxData = []
        self.fpaMinData = []

    def getRegex(self):
        regexToSend = self.regex.format(self.nxMax, self.nxMin, self.nzMax, self.nzMin, self.pMax, self.pMin, self.alphaMax, self.alphaMin, self.phiMaxManuel, self.phiMaxAutomatique, self.fpaMax, self.fpaMin)
        return regexToSend

    def setData(self, nxMax, nxMin, nzMax, nzMin, pMax, pMin, alphaMax, alphaMin, phiMaxManuel, phiMaxAutomatique, fpaMax, fpaMin):
        self.nxMax = nxMax
        self.nxMin = nxMin
        self.nzMax = nzMax
        self.nzMin = nzMin
        self.pMax = pMax
        self.pMin = pMin
        self.alphaMax = alphaMax
        self.alphaMin = alphaMin
        self.phiMaxManuel = phiMaxManuel
        self.phiMaxAutomatique = phiMaxAutomatique
        self.fpaMax = fpaMax
        self.fpaMin = fpaMin
    
class ApLATTest():
    def __init__(self):
        self.p = 0
        self.regex = 'AP_LAT p={}'

        self.pData = []
    
    def getRegex(self):
        regexToSend = self.sendRegex.format(self.p)
        
        return regexToSend
    
    def setData(self, p):
        self.p = p

class ApLONGTest():
    def __init__(self):
        self.nx = 0
        self.nz = 0

        self.nxData = []
        self.nzData = []

        self.regexNx = 'AP_LONGI Nx={}'
        self.regexNz = 'AP_LONGI Nz={}'
    
    def getRegexNx(self):
        regexToSend = self.sendRegex.format(self.nx)
        
        return regexToSend
    
    def getRegexNz(self):
        regexToSend = self.sendRegex.format(self.nz)
        
        return regexToSend
    
    def setData(self, nx, nz):
        self.nx = nx
        self.nz = nz

class StateVectorTest():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.Vp = 0
        self.fpa = 0
        self.psi = 0
        self.phi = 0
        self.parserRegex = '^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)'

        self.xData = []
        self.yData = []
        self.zData = []
        self.VpData = []
        self.fpaData = []
        self.psiData = []
        self.phiData = []

        self.regex = 'InitStateVector x={} y={} z={} Vp={} fpa={} psi={} phi={}'
        self.windregex = 'VWind={} dirWind={}'
        self.MagneticDeclination = 'MagneticDeclination={}'
    
    def initRegexs(self, VWind, dirWind, MagneticDeclination):
        regexToSend = self.regex.format(0, 0, 10668, 100, 0, 0, 0) # Level flight at FL350
        windRegexToSend = self.windregex.format(VWind, dirWind)
        MagneticDeclinationRegexToSend = self.MagneticDeclination.format(MagneticDeclination)
        
        return regexToSend, windRegexToSend, MagneticDeclinationRegexToSend
    
    def parser(self, *msg):
        self.x = float(msg[1])
        self.y = float(msg[2])
        self.z = float(msg[3])
        self.Vp = float(msg[4])
        self.fpa = float(msg[5])
        self.psi = float(msg[6])
        self.phi = float(msg[7])

class FcuTest():
    def __init__(self):
        self.apState = 'OFF'
        self.regex = 'FCUAP1 push'

        self.apStateData = []
    
    def getRegex(self):
        return self.regex
    
    def setApState(self, apState):
        self.apState = apState
    
class FccTest():
    def __init__(self):
        self.nx = 0
        self.nz = 0
        self.p = 0

        self.nxData = []
        self.nzData = []
        self.pData = []

        self.nxRegex = 'APNxControl nx=(\S+)'
        self.nzRegex = 'APNzControl nz=(\S+)'
        self.pRegex = 'APLatControl rollRate=(\S+)'
    
    def nxParser(self, *msg):
        self.nx = float(msg[1])
    
    def nzParser(self, *msg):
        self.nz = float(msg[1])
    
    def pParser(self, *msg):
        self.p = float(msg[1])

class DataSampler():
    def __init__(self, fmgs, apLat, apLong, stateVector, fcu, fcc):
        self.fmgs = fmgs
        self.apLat = apLat
        self.apLong = apLong
        self.stateVector = stateVector
        self.fcu = fcu
        self.fcc = fcc

        self.sampleThread = None
        self.doSample = False
        self.threadRunning = True

        self.sampleThread = threading.Thread(target=self.fetch)
        self.sampleThread.start()
    
    def run(self):
        self.doSample = True

    def fetch(self):
        while self.threadRunning:
            if self.doSample:
                print(".")
                self.sampleFmgs(self.fmgs)
                self.sampleApLat(self.apLat)
                self.sampleApLong(self.apLong)
                self.sampleStateVector(self.stateVector)
                self.sampleFcu(self.fcu)
                self.samplefcc(self.fcc)

            time.sleep(0.1)

    def sampleFmgs(self, fmgs):
        fmgs.nxMaxData.append(fmgs.nxMax)
        fmgs.nxMinData.append(fmgs.nxMin)
        fmgs.nzMaxData.append(fmgs.nzMax)
        fmgs.nzMinData.append(fmgs.nzMin)
        fmgs.pMaxData.append(fmgs.pMax)
        fmgs.pMinData.append(fmgs.pMin)
        fmgs.alphaMaxData.append(fmgs.alphaMax)
        fmgs.alphaMinData.append(fmgs.alphaMin)
        fmgs.phiMaxManuelData.append(fmgs.phiMaxManuel)
        fmgs.phiMaxAutomatiqueData.append(fmgs.phiMaxAutomatique)
        fmgs.fpaMaxData.append(fmgs.fpaMax)
        fmgs.fpaMinData.append(fmgs.fpaMin)
        
    def sampleApLat(self, apLat):
        pass
    
    def sampleApLong(self, apLong):
        pass

    def sampleStateVector(self, stateVector):
        pass

    def sampleFcu(self, fcu):
        pass
    
    def samplefcc(self, fcc):
        fcc.nxData.append(fcc.nx)
        fcc.nzData.append(fcc.nz)
        fcc.pData.append(fcc.p)

    
    def stop(self):
        self.doSample = False
        #self.sampleThread.join()
    
    def reset(self):
        pass
    
    def end(self):
        self.threadRunning = False
    
    def plotFirstTestData(self):
        nx = self.fcc.nxData
        nz = self.fcc.nzData
        p = self.fcc.pData
        nzMax = self.fmgs.nzMaxData
        nzMin = self.fmgs.nzMinData

        plt.figure(figsize=(10, 6))

        plt.plot(nz, label='FCC Nz')
        plt.plot(nzMax, label='FMGS NzMax')
        plt.plot(nzMin, label='FMGS NzMin')
        plt.title('FCC Nz vs FMGS NzMax')
        plt.xlabel('Sample')
        plt.ylabel('Nz')
        plt.legend()

        plt.tight_layout()
        plt.show()

        
