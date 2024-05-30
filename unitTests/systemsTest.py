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
        self.phiMinManuel = 0
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
        self.phiMinManuelData = []
        self.phiMaxAutomatiqueData = []
        self.fpaMaxData = []
        self.fpaMinData = []

    def getRegex(self):
        regexToSend = self.regex.format(self.nxMax, self.nxMin, self.nzMax, self.nzMin, self.pMax, self.pMin, self.alphaMax, self.alphaMin, self.phiMaxManuel, self.phiMaxAutomatique, self.fpaMax, self.fpaMin)
        return regexToSend

    def setData(self, nxMax, nxMin, nzMax, nzMin, pMax, pMin, alphaMax, alphaMin, phiMaxManuel, phiMaxAutomatique, fpaMax, fpaMin):
        self.nxMax = float(nxMax)
        self.nxMin = float(nxMin)
        self.nzMax = float(nzMax)
        self.nzMin = float(nzMin)
        self.pMax = float(pMax)
        self.pMin = float(pMin)
        self.alphaMax = float(alphaMax)
        self.alphaMin = float(alphaMin)
        self.phiMaxManuel = float(phiMaxManuel)
        self.phiMinManuel = - self.phiMaxManuel
        self.phiMaxAutomatique = float(phiMaxAutomatique)
        self.fpaMax = float(fpaMax)
        self.fpaMin = float(fpaMin)
    
    def resetRecord(self):
        self.nxMaxData = []
        self.nxMinData = []
        self.nzMaxData = []
        self.nzMinData = []
        self.pMaxData = []
        self.pMinData = []
        self.alphaMaxData = []
        self.alphaMinData = []
        self.phiMaxManuelData = []
        self.phiMinManuelData = []
        self.phiMaxAutomatiqueData = []
        self.fpaMaxData = []
        self.fpaMinData = []
    
class ApLATTest():
    def __init__(self):
        self.p = 0
        self.regex = 'AP_LAT p={}'

        self.pData = []
    
    def getRegex(self):
        regexToSend = self.regex.format(self.p)
        
        return regexToSend
    
    def setData(self, p):
        self.p = p

    def resetRecord(self):
        self.pData = []

class ApLONGTest():
    def __init__(self):
        self.nx = 0
        self.nz = 0

        self.nxData = []
        self.nzData = []

        self.regex = 'AP_LONG nx={} nz={}'

    def getRegex(self):
        regexToSend = self.regex.format(self.nx, self.nz)
        
        return regexToSend
    
    def setData(self, nx, nz):
        self.nx = nx
        self.nz = nz
    
    def resetRecord(self):
        self.nxData = []
        self.nzData = []

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
    
    def resetRecord(self):
        self.xData = []
        self.yData = []
        self.zData = []
        self.VpData = []
        self.fpaData = []
        self.psiData = []
        self.phiData = []

class FcuTest():
    def __init__(self):
        self.apState = 'off'
        self.regex = 'FCUAP1 push'

        self.apStateData = []
    
    def getRegex(self):
        return self.regex
    
    def setApState(self, apState):
        self.apState = apState
    
    def resetRecord(self):
        self.apStateData = []
    
class FccTest():
    def __init__(self, fcu):
        self.nx = 0
        self.nz = 0
        self.p = 0
        self.flaps = 0
        self.gear = False
        self.fcu = fcu

        self.nxData = []
        self.nzData = []
        self.pData = []

        self.nxRegex = '^APNxControl nx=(\S+)'
        self.nzRegex = '^APNzControl nz=(\S+)'
        self.pRegex = '^APLatControl rollRate=(\S+)'
        self.flapsRegex = '^VoletState=(\S+)'
        self.gearRegex = '^LandingGearState=(\S+)'
        self.apAckRegex = '^FCUAP1 (.*)'
    
    def nxParser(self, *msg):
        self.nx = float(msg[1])
    
    def nzParser(self, *msg):
        self.nz = float(msg[1])
    
    def pParser(self, *msg):
        self.p = float(msg[1])
    
    def flapsParser(self, *msg):
        self.flaps = float(msg[1])
    
    def gearParser(self, *msg):
        if msg[1] == 'True':
            self.gear = True
        else:
            self.gear = False
    
    def apAckParser(self, *msg):
        print("AP Ack: ", msg[1])
        self.fcu.apState = msg[1]
    
    def resetRecord(self):
        self.nxData = []
        self.nzData = []
        self.pData = []

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
        fmgs.phiMinManuelData.append(fmgs.phiMinManuel)
        fmgs.phiMaxAutomatiqueData.append(fmgs.phiMaxAutomatique)
        fmgs.fpaMaxData.append(fmgs.fpaMax)
        fmgs.fpaMinData.append(fmgs.fpaMin)
        
    def sampleApLat(self, apLat):
        apLat.pData.append(apLat.p)
        pass
    
    def sampleApLong(self, apLong):
        apLong.nxData.append(apLong.nx)
        pass

    def sampleStateVector(self, stateVector):
        stateVector.xData.append(stateVector.x)
        stateVector.yData.append(stateVector.y)
        stateVector.zData.append(stateVector.z)
        stateVector.VpData.append(stateVector.Vp)
        stateVector.fpaData.append(stateVector.fpa)
        stateVector.psiData.append(stateVector.psi)
        stateVector.phiData.append(stateVector.phi)
        

    def sampleFcu(self, fcu):
        fcu.apStateData.append(fcu.apState)
    
    def samplefcc(self, fcc):
        fcc.nxData.append(fcc.nx)
        fcc.nzData.append(fcc.nz)
        fcc.pData.append(fcc.p)
    
    def stop(self):
        self.doSample = False
    
    def reset(self):
        self.fmgs.resetRecord()
        self.apLat.resetRecord()
        self.apLong.resetRecord()
        self.stateVector.resetRecord()
        self.fcu.resetRecord()
        self.fcc.resetRecord()
    
    def end(self):
        self.threadRunning = False
    
    def plotNzLimitation(self):
        nz = self.fcc.nzData
        nzMax = self.fmgs.nzMaxData
        nzMin = self.fmgs.nzMinData

        plt.figure(figsize=(10, 6))

        plt.plot(nz, label='Nz')
        plt.plot(nzMax, label='NzMax')
        plt.plot(nzMin, label='NzMin')
        plt.title('FCC Nz vs FMGS NzMax & NzMin')
        plt.xlabel('time (ms)')
        plt.ylabel('Nz')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def plotFpaLimitation(self):
        fpa = self.stateVector.fpaData
        fpaMax = self.fmgs.fpaMaxData
        fpaMin = self.fmgs.fpaMinData

        plt.figure(figsize=(10, 6))

        plt.plot(fpa, label='fpa (rad)')
        plt.plot(fpaMax, label='fpa max (rad)')
        plt.plot(fpaMin, label='fpa min (rad)')
        plt.title('StateVector FPA vs FMGS FpaMax & FpaMin')
        plt.xlabel('time (ms)')
        plt.ylabel('FPA')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def plotPLimitationTest(self):
        p = self.fcc.pData
        pMax = self.fmgs.pMaxData
        pMin = self.fmgs.pMinData

        plt.figure(figsize=(10, 6))

        plt.plot(p, label='p (rad/s)')
        plt.plot(pMax, label='p Max (rad/s)')
        plt.plot(pMin, label='p Min (rad/s)')
        plt.title('FCC P vs FMGS PMax & PMin')
        plt.xlabel('time (ms)')
        plt.ylabel('P')
        plt.legend()

        plt.tight_layout()
        plt.show()
    
    def plotPhiLimitationTest(self):
        phiMax = self.fmgs.phiMaxManuelData
        phiMin = self.fmgs.phiMinManuelData
        phi = self.stateVector.phiData

        plt.figure(figsize=(10, 6))

        plt.plot(phi, label='Phi (rad)')
        plt.plot(phiMax, label='PhiMax (rad)')
        plt.plot(phiMin, label='PhiMin (rad)')
        plt.title('FCC Phi Limitation')
        plt.xlabel('time (ms)')
        plt.ylabel('Phi')
        plt.legend()

        plt.tight_layout()
        plt.show()
    
    def plotApTest(self):
        nx = self.fcc.nxData
        nz = self.fcc.nzData
        p = self.fcc.pData

        nxAp = self.apLong.nxData
        nzAp = self.apLong.nzData
        pAp = self.apLat.pData

        plt.figure(figsize=(10, 6))

        plt.plot(nx, label='Nx')
        plt.plot(nz, label='Nz')
        plt.plot(p, label='P')
        plt.plot(nxAp, label='Nx AP')
        plt.plot(nzAp, label='Nz AP')
        plt.plot(pAp, label='P AP')

        plt.title('FCC vs AP')
        plt.xlabel('time (ms)')
        plt.ylabel('Value')
        plt.legend()

        plt.tight_layout()
        plt.show()