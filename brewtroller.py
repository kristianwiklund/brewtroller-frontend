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
