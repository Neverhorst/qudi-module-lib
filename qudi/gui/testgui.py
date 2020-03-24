# -*- coding: utf-8 -*-
"""
This file contains a qudi GUI module template

Qudi is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Qudi is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Qudi. If not, see <http://www.gnu.org/licenses/>.

Copyright (c) the Qudi Developers. See the COPYRIGHT.txt file at the
top-level directory of this distribution and at <https://github.com/Ulm-IQO/qudi/>
"""

from core.connector import Connector
from core.statusvariable import StatusVar
from core.configoption import ConfigOption
from core.module import GuiBase
from qtpy import QtCore, QtWidgets, QtGui


class MyMainWindow(QtWidgets.QMainWindow):
    """Create a Qt main window.
    Can either be customized entirely here or loaded from a .ui file.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button_up = QtWidgets.QPushButton('count up')
        self.button_down = QtWidgets.QPushButton('count down')
        self.spinbox = QtWidgets.QSpinBox()
        self.spinbox.setRange(-2**31, 2**31-1)
        self.spinbox.setValue(0)
        self.spinbox.setReadOnly(True)
        self.label = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button_up)
        layout.addWidget(self.spinbox)
        layout.addWidget(self.button_down)
        layout.addWidget(self.label)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


class TemplateGui(GuiBase):
    """Description of this qudi module goes here.
    """

    my_first_logic_connector = Connector(interface='TemplateLogic')
    my_second_logic_connector = Connector(interface='TemplateLogic')

    _display_str = ConfigOption(name='display_string', default='No string given in config...', missing='warn')

    sigStuffDone = QtCore.Signal()

    _my_status_variable = StatusVar(name='my_status_variable', default=42)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mw = None

    def on_activate(self):
        """Everything that should be done when activating the module must go in here.
        Especially instantiating the QMainWindow (or similar) object should be done here.
        It is also a good place to initialize all GUI elements.
        """
        # The GUI main window is usually named "_mw" in qudi GUI modules
        self._mw = MyMainWindow()

        # Initialize GUI elements
        self._mw.spinbox.setValue(self._my_status_variable)  # Restore shown value from StatusVar
        self._mw.label.setText(self._display_str)  # Use ConfigOption

        # Establish Qt signal-slot connections if needed. Also connect to logic signals and slots,
        # preferably through QtCore.Qt.QueuedConnection
        self.sigStuffDone.connect(self.my_slot_for_stuff)
        self._mw.button_down.clicked.connect(self.count_down)
        self._mw.button_up.clicked.connect(self.count_up)

        self.my_first_logic_connector().sigStuffDone.connect(self.my_slot_for_stuff)
        self.my_second_logic_connector().sigStuffDone.connect(self.my_slot_for_stuff)

        # Show main window
        self.show()
        return

    def on_deactivate(self):
        """Undo everything that has been done in on_activate. In other words clean up after
        yourself and ensure there are no lingering connections, references to outside objects, open
        file handles etc. etc.
        """
        # disconnect all signals connected in on_activate
        self.sigStuffDone.disconnect(self.my_slot_for_stuff)
        self._mw.button_down.clicked.disconnect()
        self._mw.button_up.clicked.disconnect()

        # Close all windows associated with this GUI
        self._mw.close()
        return

    def show(self):
        """This method must be implemented by all GUI modules. It should show the GUI main window
        and bring it to the top.
        """
        self._mw.show()
        self._mw.raise_()
        self._mw.activateWindow()
        return

    @QtCore.Slot()
    def count_down(self):
        """Example callback function for "count down" button pressed.
        """
        self._my_status_variable -= 1
        self._mw.spinbox.setValue(self._my_status_variable)
        return

    @QtCore.Slot()
    def count_up(self):
        """Example callback function for "count up" button pressed.
        """
        self._my_status_variable += 1
        self._mw.spinbox.setValue(self._my_status_variable)

    @QtCore.Slot()
    @QtCore.Slot(object)
    def my_slot_for_stuff(self, val=None):
        """Dummy slot that gets called every time sigStuffDone is emitted and connected.
        """
        print('my_slot_for_stuff has been called!', val)
        return
