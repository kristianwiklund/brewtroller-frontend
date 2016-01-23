import curses
import time
from brewtroller import *
from mash import *

class CursesTun(Tun):
    # window size
    height=13
    width=11

    # temperature display position in the window
    tempx=3
    tempy=3

    def __init__(self,bt,myid,title,x,y):
        Tun.__init__(self,bt,myid,title)
        self.win = curses.newwin(self.height, self.width, x, y)
        self.win.border("|","|","-","-","/","\\","\\","/")
        self.win.addstr(0,(self.width-len(title))/2,title)
        self.win.addstr(2,3,"Temp:",curses.A_BOLD)
        self.win.addstr(5,3,"Set:",curses.A_BOLD)
        self.win.addstr(8,3,"Power:",curses.A_BOLD)

    def update(self):

        redraw=0

        Tun.update(self)

        if self.temperature != self.newtemperature:
            self.temperature = self.newtemperature
            redraw = 1

            if self.temperature > 150: # easy, ugly check if there is no sensor
                self.win.addstr(3,3,"ERROR",curses.A_BLINK)
            else:
                self.win.addstr(3,3,"     ") # erase first
                self.win.addstr(3,3,str(self.temperature))

        # get setpoint

        if self.setpoint != self.newsetpoint:
            self.setpoint=self.newsetpoint
            redraw = 1

            self.win.addstr(6,3,"     ") # erase first
            self.win.addstr(6,3,str(self.setpoint))

        # get heatingpower


        if self.power != self.newpower:
            redraw=1
            self.power=self.newpower
            self.win.addstr(9,3,"     ") # erase first
            self.win.addstr(9,3,str(self.newpower)+"%")

        if redraw == 1:
            self.win.refresh()

class CursesHLTRecirc(HLTRecirc):
    def __init__(self,bt,x,y,width,height):
        HLTRecirc.__init__(self,bt)
        self.win =  curses.newwin(height, width, y, x)
        #self.win.hline(10,0,"=",width)
        #self.win.border()
        self.width=width
        self.height=height

    def update(self):
        HLTRecirc.update(self)

        if self.state != self.newstate:
            self.state = self.newstate
            self.win.erase()
            
            if self.state == 0:
                self.win.hline(10,0,">",2)
                self.win.hline(2,0,"<",2)
                self.win.vline(2,2,"^",8)
            else:
                self.win.hline(10,0,">",self.width)

            self.win.refresh()

class CursesBrewStep(BrewStep):
    
    def __init__ (self, bt, x,y,width,height):
        BrewStep.__init__(self,bt)
        self.win =  curses.newwin(height, width, y, x)
        #self.win.hline(10,0,"=",width)
        #self.win.border()
        self.width=width
        self.height=height

    def update(self):
        BrewStep.update(self)

        if self.step != self.newstep:
            self.step = self.newstep
            self.win.erase()
            self.win.addstr(0,0,self.stepnames[self.step])
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
    hlt = CursesTun(bt,0, "HLT", 10,10)
    mlt = CursesTun(bt,1, "MLT", 10,35)
    pump = CursesHLTRecirc(bt,21,10,14,13)
    step = CursesBrewStep(bt,21,25,15,1)

    while 1:
        hlt.update()
        mlt.update()
        pump.update()
        step.update()
        time.sleep(1)


curses.wrapper(main)
