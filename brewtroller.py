import requests

class BrewTroller:
    def __init__(self, adress):
        self.adress=adress

    # use a http request to send a command
    # parse the return value
    def sendCommand(command):
        r = requests.get(adress,params={command})

    
    # get the temperature of a tun
    def getTemp(tunid):
        response=self.sendCommand("q"+str(tunid))
        return response[0]
