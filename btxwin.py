#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : A spin box replicated into a text label (Qt4)
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	7-Dec-2006
# .copyright  : (c) 2006 Fabrizio Pollastri.
# .license    : GNU General Public License (see below)
#
# This file is part of "AVC, Application View Controller".
#
# AVC is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# AVC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# .-


from PyQt4.QtCore import *		# Qt core
from PyQt4.QtGui import *		# Qt GUI interface
from PyQt4.uic import *			# ui files realizer
from PyQt4 import QtGui, uic

import sys				# system support


UI_FILE = 'lodda.ui'		# qt ui descriptor


class MainWin(QtGui.QMainWindow):
     def __init__(self):
         QtGui.QMainWindow.__init__(self)

         # Set up the user interface from Designer.
         self.ui = uic.loadUi(UI_FILE)
         self.ui.show()

         self.connect(self.ui.HLTdial,SIGNAL("valueChanged(int)"), self.setHLTSetpoint)

     def setHLTSetpoint(self, value):
       self.ui.HLTSet.display(value)

app = QtGui.QApplication(sys.argv)
window = MainWin()

sys.exit(app.exec_())

