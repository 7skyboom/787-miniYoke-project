import pygame
import time
from enum import Enum

class FCC :
    fccState = Enum('MANUAL','AP_ENGAGED')
    def __init__(self, fcu, aviBus):
        self.state = 'MANUAL'
        self.nx = 0
        self.nz = 0
        self.p = 0

        self.ready = False
        self.fcu = fcu
        self.aviBus = aviBus

        self.flaps = 0 # 0, 1, 2, 3
        self.gear = False #False = up, True = down

    def setFlightCommands(self, nx, nz, p):
        self.nx = nx
        self.nz = nz
        self.p = p
        self.ready = True

    def setState(self, state):
        self.state = state
    
    def setReady(self, ready):
        self.ready = ready
    
    def sendButtonsState(self, flapsUp, flapsDown, apDisconnect, gearDown, previousFlapsUp, previousFlapsDown, previousApDisconnect, previousGearDown):
        if flapsUp and not previousFlapsUp :
            print('Flaps up button pushed')
            self.flaps += 1
            self.flaps = 0 if self.flaps > 3 else self.flaps
            self.aviBus.sendMsg('YOKE flaps={}'.format(self.flaps))
        if flapsDown and not previousFlapsDown :
            print('Flaps down button pushed')
            self.flaps -= 1
            self.flaps = 0 if self.flaps < 0 else self.flaps
            self.aviBus.sendMsg('YOKE flaps={}'.format(self.flaps))
        if apDisconnect and not previousApDisconnect :
            print('AP disconnect button pushed')
            if self.state == 'AP_ENGAGED':
                print('fcc state switch from AP_ENGAGED to MANUAL')
                self.aviBus.sendMsg('FCUAP1 off') # Send acknowledge message to the fcu
                self.state = 'MANUAL'
                self.fcu.setApState('OFF')

        if gearDown and not previousGearDown :
            print('Gear down button pushed')
            self.gear = True if not self.gear else False
            self.aviBus.sendMsg('YOKE gear={}'.format(self.gear))

class MiniYoke :
    def __init__(self, fcc, fmgs, flightModel, filterOn, alpha):
        self.nx = 0
        self.nz = 0
        self.p = 0
        
        self.fcc = fcc
        self.fmgs = fmgs
        self.flightModel = flightModel

        self.throttleAxisValue = 0 # throttle axis value from joystick to compute nx
        self.pitchAxisValue = 0 # pitch axis value from joystick to compute nz
        self.rollAxisValue = 0 # roll axis value from joystick to compute p
        
        self.joystick = None # joystick object from pygame
        self.threadRunning = True
        self.moved = False

        self.throttleAxis = 3
        self.pitchAxis = 1
        self.rollAxis = 0

        self.nzMin = -2
        self.nzMax = 4

        self.pMin = -0.35
        self.pMax = 0.35

        self.flapsUpButton = 11
        self.flapsDownButton = 10
        self.apDisconnectButton = 3
        self.gearDownButton = 9

        self.flapsUpPushed = False
        self.flapsDownPushed = False
        self.apDisconnectPushed = False
        self.gearDownPushed = False

        self.previousFlapsUpPushed = False
        self.previousFlapsDownPushed = False
        self.previousApDisconnectPushed = False
        self.previousGearDownPushed = False

        self.pitchAxisMax = 1
        self.pitchAxisMin = -1
        self.rollAxisMax = 1
        self.rollAxisMin = -1

        self.filterOn = filterOn
        self.filteredPitchAxisValue = 0
        self.filteredRollAxisValue = 0
        self.alpha = alpha  # Coefficient for low pass filter


    def begin(self):
        pygame.init()
        pygame.joystick.init()
        
        joystickCount = pygame.joystick.get_count()
        if joystickCount == 0:
            print("No joystick found. Please plug one.")
            pygame.quit()
            time.sleep(2)
            return False
        else:
            print(f"{joystickCount} joystick found.")

        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        print(f"Nom du joystick : {joystick.get_name()}")
        print(f"Nombre d'axes : {joystick.get_numaxes()}")
        print(f"Nombre de boutons : {joystick.get_numbuttons()}")

        self.joystick = joystick

        return True
    
    def listener(self):
        while self.threadRunning :
            pygame.event.pump()
            self.throttleAxisValue = self.joystick.get_axis(self.throttleAxis)
            self.pitchAxisValue = self.joystick.get_axis(self.pitchAxis)
            self.rollAxisValue = self.joystick.get_axis(self.rollAxis)

            self.flapsUpPushed = self.joystick.get_button(self.flapsUpButton)
            self.flapsDownPushed = self.joystick.get_button(self.flapsDownButton)
            self.apDisconnectPushed = self.joystick.get_button(self.apDisconnectButton)
            self.gearDownPushed = self.joystick.get_button(self.gearDownButton)

            self.fcc.sendButtonsState(self.flapsUpPushed, self.flapsDownPushed, self.apDisconnectPushed, self.gearDownPushed, self.previousFlapsUpPushed, self.previousFlapsDownPushed, self.previousApDisconnectPushed, self.previousGearDownPushed)

            self.previousFlapsUpPushed = self.flapsUpPushed
            self.previousFlapsDownPushed = self.flapsDownPushed
            self.previousApDisconnectPushed = self.apDisconnectPushed
            self.previousGearDownPushed = self.gearDownPushed
            
            self.moved = True if self.pitchAxisValue != 0 and self.rollAxisValue != 0 else False

            self.getFlightCommands(self.pitchAxisValue, self.rollAxisValue)
            self.fcc.setFlightCommands(self.nx, self.nz, self.p)
            #print("pitch Axis:")
            #print(self.pitchAxisValue)
            #print("roll Axis")
            #print(self.rollAxisValue)
            time.sleep(0.1)

    def getFlightCommands(self, pitchAxisValue, rollAxisValue):
        self.nx = self.nxLaw()
        self.nz = self.nzLaw(pitchAxisValue)
        self.p = self.pLaw(rollAxisValue)
        
    
    def nxLaw(self):
        return 0

    def nzLaw(self, pitchAxisValue):
        if self.filterOn:
            self.filteredPitchAxisValue = self.alpha * pitchAxisValue + (1 - self.alpha) * self.filteredPitchAxisValue
            nz = self.nzMin + (self.nzMax - self.nzMin) * (self.filteredPitchAxisValue - self.pitchAxisMin) / (self.pitchAxisMax - self.pitchAxisMin)
        else:
            nz = self.nzMin + (self.nzMax - self.nzMin) * (pitchAxisValue - self.pitchAxisMin) / (self.pitchAxisMax - self.pitchAxisMin)


        if self.flightModel.fpa < self.fmgs.fpaMin or self.flightModel.fpa > self.fmgs.fpaMax:
            nz = 1

        #return -2
        return max(self.fmgs.nzMin, min(self.fmgs.nzMax, nz))

    def pLaw(self, rollAxisValue):
        if self.filterOn:
            self.filteredRollAxisValue = self.alpha * rollAxisValue + (1 - self.alpha) * self.filteredRollAxisValue
            p = self.pMin + (self.pMax - self.pMin) * (self.filteredRollAxisValue - self.rollAxisMin) / (self.rollAxisMax - self.rollAxisMin)
        else:
            p = self.pMin + (self.pMax - self.pMin) * (rollAxisValue - self.rollAxisMin) / (self.rollAxisMax - self.rollAxisMin)

        
        if self.flightModel.phi < self.fmgs.phiMin and self.rollAxisValue < 0:
            p = 0
        if self.flightModel.phi > self.fmgs.phiMax and self.rollAxisValue > 0:
            p = 0
    
        return max(self.fmgs.pMin, min(self.fmgs.pMax, p))
    
    def end(self):
        self.threadRunning = False
        pygame.quit()
        pygame.joystick.quit()

class ApLAT :
    def __init__(self):
        self.p = 0
        self.ready = False
        self.regex = '^AP_LAT p=(\S+)'
    
    def parser(self, *msg):
        self.p = msg[1]
        self.ready = True # apLat data is ready to be sent

        print('Received message from AP_LAT :')
        print('p =', self.p)
        
    def setReady(self, ready):
        self.ready = ready
    
class ApLONG :
    def __init__(self):
        self.nx = 0
        self.nz = 0
        self.ready = False
        self.regex = '^AP_LONG nx=(\S+) nz=(\S+)'
    
    def parser(self, *msg):
        self.nx = msg[1]
        self.nz = msg[2]
        print('Received message from AP_LONG :')
        print('nx =', self.nx)
        print('nz =', self.nz)

        self.ready = True # apLong data is ready to be sent
    
    def setReady(self, ready):
        self.ready = ready

class FMGS : 
    def __init__(self, prod=True):
        self.nxMax = 0
        self.nxMin = 0
        self.nzMax = 0
        self.nzMin = 0
        self.pMax = 0
        self.pMin = 0
        self.fpaMax = 0 # Flight Path Angle = Gamma here
        self.fpaMin = 0
        self.phiMax = 0
        self.fpaMax = 0
        self.regex = '^Performances NxMax=(\S+) NxMin=(\S+) NzMax=(\S+) NzMin=(\S+) PMax=(\S+) PMin=(\S+) AlphaMax=(\S+) AlphaMin=(\S+) PhiMaxManuel=(\S+) PhiMaxAutomatique=(\S+) GammaMax=(\S+) GammaMin=(\S+)'
        
        self.prod = prod
        if self.prod:
            self.nxMax = 0.5
            self.nxMin = -1
            self.nzMax = 2.5
            self.nzMin = -1.5
            self.pMax = 0.7
            self.pMin = -0.7
            self.phiMax = 1.152 # 1.152 rad = 66°
            self.phiMin = -self.phiMax
            self.fpaMax = 0.175 # 0.175 rad = 10°
            self.fpaMin = - 0.5 # - 0.262 rad = - 15°
            
            
    def parser(self, *msg):
        self.nxMax = msg[1]
        self.nxMin = msg[2]
        self.nzMax = msg[3]
        self.nzMin = msg[4]
        self.pMax = msg[5]
        self.pMin = msg[6]
        self.phiMax = msg[9]
        self.fpaMax = msg[10]
        self.fpaMin = msg[11]

        print('Received message from FMGS :')
        print('nxMax =', self.nxMax)
        print('nxMin =', self.nxMin)
        print('nzMax =', self.nzMax)
        print('nzMin =', self.nzMin)
        print('pMax =', self.pMax)
        print('pMin =', self.pMin)
        print('phiMax =', self.phiMax)
        print('fpaMax =', self.fpaMax)
        print('fpaMin =', self.fpaMin)
        
class FCU :
    AP_STATE = Enum('ON','OFF')
    def __init__(self):
        self.ApState = 'OFF'
        self.regex = '^FCUAP1 push'

    def parser(self, *msg):
        print('Ap button pushed on FCU')
        self.ApState = 'ON' if self.ApState == 'OFF' else 'OFF'

        print('AP state =', self.ApState)
    
    def setApState(self, state):
        self.ApState = state

class FlightModel :
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.Vp = 0
        self.fpa = 0
        self.psi = 0
        self.phi = 0
        self.regex = '^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)'

    def parser(self, *msg):
        self.x = float(msg[1])
        self.y = float(msg[2])
        self.z = float(msg[3])
        self.Vp = float(msg[4])
        self.fpa = float(msg[5])
        self.psi = float(msg[6])
        self.phi = float(msg[7])

        #print('Received message from FM :')
        #print('x =', self.x)
        #print('y =', self.y)
        #print('z =', self.z)
        #print('Vp =', self.Vp)
        print('fpa =', self.fpa)
        #print('psi =', self.psi)
        print('phi =', self.phi)