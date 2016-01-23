import curses
import time
from brewtroller import *

class Tun:
    # window size
    height=13
    width=11

    temperature=-3222
    power=-223
    setpoint=-443

    # temperature display position in the window
    tempx=3
    tempy=3

    def __init__(self,bt,myid,title,x,y):
        self.id = myid
        self.win = curses.newwin(self.height, self.width, x, y)
        self.win.border("|","|","-","-","/","\\","\\","/")
        self.win.addstr(0,(self.width-len(title))/2,title)
        self.win.addstr(2,3,"Temp:",curses.A_BOLD)
        self.win.addstr(5,3,"Set:",curses.A_BOLD)
        self.win.addstr(8,3,"Power:",curses.A_BOLD)
        self.bt = bt

    def update(self):
        redraw=0
        # get temperature
        temperature=self.bt.getTemp(self.id)
        if self.temperature != temperature:
            self.temperature = temperature
            redraw = 1

            if temperature > 150: # easy, ugly check if there is no sensor
                self.win.addstr(3,3,"ERROR",curses.A_BLINK)
            else:
                self.win.addstr(3,3,"     ") # erase first
                self.win.addstr(3,3,str(temperature))

        # get setpoint

        setpoint=self.bt.getSetpoint(self.id)
        if self.setpoint != setpoint:
            self.setpoint=setpoint
            redraw = 1

            self.win.addstr(6,3,"     ") # erase first
            self.win.addstr(6,3,str(setpoint))

        # get heatingpower

        power=self.bt.getHeatpwr(self.id)

        if self.power != power:
            redraw=1
            self.power=power
            self.win.addstr(9,3,"     ") # erase first
            self.win.addstr(9,3,str(power)+"%")

        if redraw == 1:
            self.win.refresh()

class Pump:
    state=0 # 0 - recirc, 1 - fill 
    
    def __init__(self,x,y,width,height):
        self.win =  curses.newwin(height, width, y, x)
        #self.win.hline(10,0,"=",width)
        #self.win.border()
        self.width=width
        self.height=height

    def update(self):
        # here is code to check the state of the valves
        # if newstate != oldstate then redraw...

        self.win.erase()
        
        if self.state == 0:
            self.win.hline(10,0,">",2)
            self.win.hline(2,0,"<",2)
            self.win.vline(2,2,"^",8)
        else:
            self.win.hline(10,0,">",self.width)

        self.win.refresh()

def main(stdscr):
#    begin_x = 20; begin_y = 7
#    height = 5; width = 40
#    win = curses.newwin(height, width, begin_y, begin_x)
#    win.addstr(0,0,"apa")
#    win.refresh()
#    time.sleep(10)

    # create a connection to the btnic daemon
    bt = BrewTroller("http://10.168.0.10/cgi-bin/btnic.cgi")

    # we create two windows - one for the HLT and one for the MLT
    hlt = Tun(bt,0, "HLT", 10,10)
    mlt = Tun(bt,1, "MLT", 10,35)
    pump = Pump(21,10,14,13)


    while 1:
        hlt.update()
        mlt.update()
        pump.update()
        time.sleep(1)

curses.wrapper(main)
