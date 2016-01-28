URL1="http://127.0.0.1//cgi-bin//btnic.cgi?q1"
URL2="http://127.0.0.1//cgi-bin//btnic.cgi?q2"

import urllib2
import re
import time
import csv
import matplotlib.pyplot as plt

plt.ion()
class DynamicUpdate():
    #Suppose we know the x range
    min_x = 0
    max_x = 10

    def on_launch(self):
        #Set up plot
        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot([],[], '-o')
        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_autoscalex_on(True)
#        self.ax.set_ylim(0, 100)
        #Other stuff
        self.ax.grid()

    def on_running(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    #Example
    def __call__(self):
        import numpy as np
        import time
        self.on_launch()

        with open("templogg.csv","a") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",")
            xdata = []
            ydata = []

            while True:
                response = urllib2.urlopen(URL1)
                html = response.read()
#print html
                stamp1 = [int(s) for s in re.findall(r'\b\d+\b', html)]

                response = urllib2.urlopen(URL2)
                html = response.read()
#print html
                stamp2 = [int(s) for s in re.findall(r'\b\d+\b', html)]

#                tfnupp.append(stamp)
#                print tfnupp
#        plt.scatter(*zip(*tfnupp))
#        plt.ion()
#        plt.show()
    #print stamp
                csvwriter.writerow(stamp1,stamp2)
                xdata.append(stamp2[0])
                ydata.append(stamp2[1])
                self.on_running(xdata, ydata) 
                csvfile.flush()
                time.sleep(10)

            return xdata, ydata

d = DynamicUpdate()
d()

print "Logging..."



tfnupp = []

