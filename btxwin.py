#!/usr/bin/python


from PyQt4.QtCore import *		# Qt core
from PyQt4.QtGui import *		# Qt GUI interface
from PyQt4.uic import *			# ui files realizer
from PyQt4 import QtGui, uic
from brewtroller import *
from mash import *
from functools import *
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# for example / remove later
from numpy import arange, sin, pi
# for example / end


import sys				# system support

class TehFigure:

    def __init__(self, layoutwidget):
        self.figure = Figure(figsize=(5,4), dpi=100) # magic numbers
        self.axes1=self.figure.add_subplot(111) # more magic
        self.axes2=self.figure.add_subplot(111) # more magic
        self.canvas = FigureCanvas(self.figure)
        self.lines1, = self.axes1.plot([],[], '-')
        self.lines2, = self.axes2.plot([],[], '-')
        self.axes1.set_ylim(0, 100)        
        self.axes2.set_ylim(0, 100)        
        self.compute_initial_figure()
        self.canvas.updateGeometry()

        layoutwidget.addWidget(self.canvas)
        

    def compute_initial_figure(self):
        pass

    def update_plot(self, xdata, ydata):
        # we need to split this somehow.

        #Update data (with the new _and_ the old points)
        self.lines1.set_xdata(xdata["HLT"])
        self.lines1.set_ydata(ydata["HLT"])
        self.lines2.set_xdata(xdata["MLT"])
        self.lines2.set_ydata(ydata["MLT"])
        #Need both of these in order to rescale
        self.axes1.relim()
        self.axes1.autoscale_view()
        self.axes2.relim()
        self.axes2.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def annotate(self, x, y, text):
        self.axes1.annotate(text, xy=(x,y),xytext=(x,50),arrowprops=dict(facecolor='black', arrowstyle="->"))


UI_FILE = 'lodda.ui'		# qt ui descriptor

class XTun(Tun):
     
     setpointsaved = True
     manualsetpoint = 0 

     def setSetpointManually(self, value):
          self.setpointsaved = False
          self.setPointWidget.display(value)
          self.setPointWidget.setStyleSheet("QLCDNumber{color:blue;}")
          self.manualsetpoint = value

     def __init__(self, w, bt, myid, setpoint, temperature, setbutton, dial):
          Tun.__init__(self,bt, myid)
          self.setPointWidget = setpoint
          self.dialWidget = dial
          self.temperatureWidget = temperature

          w.connect(dial,SIGNAL("valueChanged(int)"), partial(XTun.setSetpointManually,self))
          
     def update(self):
          if self.setpointsaved:
               Tun.update(self)
               if self.newsetpoint != self.setpoint:
                    self.setPointWidget.display(self.newsetpoint)
                    self.setPointWidget.setStyleSheet("QLCDNumber{color:green;}")
                    self.setpoint = self.newsetpoint
                    self.manualsetpoint = self.setpoint
#                    print(self.setpoint)

               if (self.newtemperature < 200) and (self.newtemperature > -20): # disconnected onewire results in weird numbers.
                    if self.newtemperature != self.temperature:
                         self.temperatureWidget.setDecMode()
                         self.temperatureWidget.display(self.newtemperature)
                         self.temperatureWidget.setStyleSheet("QLCDNumber{color:red;}")
                         self.temperature = self.newtemperature
                    
               else:
                    self.temperatureWidget.setHexMode()
                    self.temperatureWidget.display(int("dead",16))
                    
class XProgramStatus:

     oldstep=255
     xdata = {}
     ydata = {}
     xdata["HLT"] = []
     ydata["HLT"] = []
     xdata["MLT"] = []
     ydata["MLT"] = []
     

     def __init__(self, w, bt,stepWidgets,nextwidget,stopalarmwidget,plot):
          self.BrewStep = BrewStep(bt)
          self.stepWidgets = stepWidgets
          nextwidget.clicked.connect(self.nextstep)
          stopalarmwidget.clicked.connect(self.stopalarm)
          self.plot = plot
          self.bt = bt

     def stopalarm(self):
          # code to change the alarm indicator back to inactive
          self.bt.stopAlarm()

     def nextstep(self):
          self.bt.advStep()

     def update(self):
          # if the brewstep is 255 the system is idle
          brewstep = self.BrewStep.getStep()



          # need to update the progress bars and display which step is active
          fullstatus = self.bt.getFullStatus()
#               print ("step" + str(brewstep))
          print (fullstatus)

               # put text on the active step
          if self.oldstep != brewstep:
              self.plot.annotate(fullstatus["timestamp"], float(fullstatus["MLT"]["temp"])/100, self.BrewStep.stepnames[brewstep])

              for key in self.stepWidgets:
                  if key == brewstep:
                      self.stepWidgets[key].setTextVisible(True) 
                  else:
                      self.stepWidgets[key].setTextVisible(False)
                      
                  self.oldstep = brewstep
                      
               # update temperature plots

          self.xdata["HLT"].append(fullstatus["timestamp"])
          self.ydata["HLT"].append(float(fullstatus["HLT"]["temp"])/100)
          
          self.xdata["MLT"].append(fullstatus["timestamp"])
          self.ydata["MLT"].append(float(fullstatus["MLT"]["temp"])/100)
#          print self.ydata
          
          self.plot.update_plot(self.xdata, self.ydata)


               # then figure out what the progress is.
               # for steps that are timer controlled, we can use the timer
               # for filling steps, we can use the volume (not implemented, I don't have autofill)
               # for steps that are temperature controlled, it is more difficult ("what is 100% temperature compared to what")
               # being celcius-centric we define the range for 100 % as zero to desired target temperature

                    
               # techdebt: we must be able to configure if we use the HLT or MLT for preheat - this assumes that it is a HLT

          if brewstep==2: # preheat strike water
               # get the temperature for the HLT
               # get the program step temperature
               # calculate and set percentage in progress bar

               progress = (float(fullstatus["HLT"]["temp"]))/float(fullstatus["HLT"]["setpoint"])
               #print (progress)
               self.stepWidgets[brewstep].setValue(int(100*progress))

          if brewstep==3: # dough in
               progress = (float(fullstatus["MLT"]["temp"]))/float(fullstatus["MLT"]["setpoint"])
               #print (progress)
               self.stepWidgets[brewstep].setValue(int(100*progress))

          if brewstep==6: # acid rest
               if fullstatus["mashtimer"]["status"] == 1: #mashing
                    progdata = bt.getProgram(1) # this needs fixing!
                    progress = (float(fullstatus["mashtimer"]["value"])/float(progdata[brewstep]["time"])/60000)
                    self.stepWidgets[brewstep].setValue(int(100*progress))                    

          if brewstep==8 or brewstep==9: # the saccarification steps
              self.stopalarm() # turn off the alarms as soon as possible - it is annoying. I don't really do anything here anyway
              


          # logic to move one step forward automatically for some parts.
          # I personally do not care about:
          # delay, refill, and will skip ahead over those

          if brewstep==1 or brewstep==4 or brewstep==14:
              self.stopalarm()
              self.nextstep()
              print "skipped step "+str(brewstep)
                    
          
class MainWin(QtGui.QMainWindow):
     def __init__(self,bt):
         QtGui.QMainWindow.__init__(self)
         self.bt = bt

         # Set up the user interface from Designer.
         self.ui = uic.loadUi(UI_FILE)
         self.ui.show()

         sc = TehFigure(self.ui.plotlayout)

         self.HLT = XTun(self.ui, bt, 0, self.ui.HLTSet, self.ui.HLTTemp, self.ui.toggleHLT, self.ui.HLTdial)
         self.MLT = XTun(self.ui, bt, 1, self.ui.MLTSet, self.ui.MLTTemp, self.ui.toggleMLT, self.ui.MLTdial)


         stepwidgets = {
              2: self.ui.progresspreheat,
              5: self.ui.progressdoughin,
              6: self.ui.progressacidrest,
              7: self.ui.progressproteinrest,
              8: self.ui.progressacc1,
              9: self.ui.progressacc2,
              10: self.ui.progressmashout
              }
         self.programstatus = XProgramStatus(self.ui, bt, stepwidgets,self.ui.nextProgStep,self.ui.stopAlarm,sc)



         # init callbacks


     

     # callback function

     def updateui(self):
          self.MLT.update()
          self.HLT.update()
          self.programstatus.update()


### main

# create a connection to the btnic daemon
bt = BrewTroller("http://10.168.0.129/cgi-bin/btnic.cgi")
app = QtGui.QApplication(sys.argv)
window = MainWin(bt)

# set a timer that update the status every ten seconds
timer = QTimer()
timer.timeout.connect(window.updateui)
timer.start(10000)


sys.exit(app.exec_())

