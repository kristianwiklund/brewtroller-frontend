import requests

# commands: https://github.com/BrewTroller/BrewTroller-Official/blob/master/Com_BTnic.h#L557

class BrewTroller:
    def __init__(self, adress):
        self.adress=adress

    # use a http request to send a command
    # parse the return value
    def sendCommand(self,command):
        r = requests.get(self.adress+"?"+command)
        # parse the request into an array of responses
        return str(r.text).translate(None,"[]\"").split(",")
    
    # get the temperature of a tun
    def getTemp(self,tunid):
        response=self.sendCommand("q"+str(tunid))
        return round(float(response[2])/100,2)

    # get the setpoint of a tun
    def getSetpoint(self,tunid):
        response=self.sendCommand("t"+str(tunid))
        return round(float(response[2]),2) # this does not seem to be multiplied with 100

    # get the heating power of a tun
    def getHeatpwr(self,tunid):
        response=self.sendCommand("s"+str(tunid))
        return round(float(response[2]),0) # this does not seem to be multiplied with 100

    def getProgramStep(self):
        response = self.sendCommand("n")
        if int(response[2])<255:
            return int(response[2])
        else:
            return int(response[4])

    def getFullStatus(self):
        u = self.sendCommand("a")
        r = {}
        r["alarmstatus"] = u[2]
        # 3,4,5 is valve status
        r["HLT"] = {"setpoint": u[6], "temp": u[7], "power": u[8], "targetvol": u[9], "vol": u[10]}
        # 11 is flow rate
        r["MLT"] = {"setpoint": u[12], "temp": u[13], "power": u[14], "targetvol": u[15], "vol": u[16]}
        # 17 is flow rate
        r["BK"] = {"setpoint": u[18], "temp": u[19], "power": u[20], "targetvol": u[21], "vol": u[22]}
        # 23 is flow rate

        # timers in milliseconds
        r["mashtimer"] = {"value": u[24], "status": u[25]}
        r["boiltimer"] = {"value": u[26], "status": u[27]}

        # 28 boil control state
        # 29 and onwards is the program steps
        
        return r

    def getProgram(self, progid):
        u = self.sendCommand("@"+str(progid))
        r = {}
        
        r["id"] = progid
        r["name"] = u[2]
        r["volume"] = u[3]
        r["grainweight"] = u[4]
        r["ratio"] = u[5]

        # 6 mash steps. using the same index as for the brewsteps

        # dough in
        r[5]["setpoint"] = u[6]
        r[5]["time"] = u[7]

        # acid rest
        r[6]["setpoint"] = u[8]
        r[6]["time"] = u[9]

        # protein rest
        r[7]["setpoint"] = u[10]
        r[7]["time"] = u[11]

        # sacc 1
        r[8]["setpoint"] = u[12]
        r[8]["time"] = u[13]

        # sacc 2
        r[9]["setpoint"] = u[14]
        r[9]["time"] = u[15]

        # mash out
        r[10]["setpoint"] = u[16]
        r[10]["time"] = u[17]

        return r
