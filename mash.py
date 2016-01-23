import curses
import time
from brewtroller import *

# keep track of a liquid tun
class Tun:
    temperature=-3222
    power=-223
    setpoint=-443

    def __init__(self,bt,myid,title):
        self.id = myid
        self.bt = bt

    def update(self):
        self.newtemperature=self.bt.getTemp(self.id)
        self.newsetpoint=self.bt.getSetpoint(self.id)
        self.newpower=self.bt.getHeatpwr(self.id)

# keep track of the HLT recirculation
# bt assumptions:
# bt configured to four outputs, only one is used for heating.
# continous recirculation of the HLT
# mash pump turned on manually (or by linux) when the MLT is filled

# pin assignments:
 #define VALVE1_PIN 20 //OUT3 - HLT recirc
 #define VALVE2_PIN 19 //OUT4 - Fill MLT
 #define VALVE3_PIN 18 //OUT5 - MLT recirc
 #define VALVE4_PIN 21 // OUT2 - Fill Boil
 #define HLTHEAT_PIN 22 //OUT1


class HLTRecirc:
    state=-1234 # 0 - valve 0, 1 - valve 1 
    newstate=0

    def update(self):
        # here is code to check the state of the valves
        # change "newstate"
        self.newstate=self.state

    def __init__(self,bt):
        self.bt = bt
        HLTRecirc.update(self)
        
class BrewStep:
    step=-234 
    newstep=0

    stepnames = {
        0: "FILL",
        1: "DELAY",
        2: "PRE-HEAT",
        3: "ADD GRAIN",
        4: "REFILL",
        5: "DOUGH IN",
        6: "ACID REST",
        7: "PROTEIN REST",
        8: "SACC 1",
        9: "SACC 2",
        10: "MASH OUT",
        11: "MASH OUT HOLD",
        12: "SPARGE",
        13: "BOIL",
        14: "CHILL",
        255: "IDLE"
        };

    def update(self):
        self.newstep=self.bt.getProgramStep()

    def __init__(self,bt):
        self.bt = bt
        BrewStep.update(self)
