import curses
import time
import brewtroller

class Tun:
    # window size
    height=10
    width=10

    # temperature display position in the window
    tempx=3
    tempy=3

    def __init__(self,myid,x,y):
        self.id = myid
        self.win = curses.newwin(self.height, self.width, x, y)
        self.win.border("|","|","-","-","/","\\","\\","/")

    def update(self):
        # get temperature
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
    hlt = Tun(1, 10,10)
    hlt.update()
    time.sleep(20)
    

curses.wrapper(main)
