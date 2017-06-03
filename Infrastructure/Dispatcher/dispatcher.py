#! /usr/bin/python

import sys
import signal
import logging
import Infrastructure.Logging.logger as logger

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import searchbar

# Plugins
import Plugins.MiniBrowser.minibrowser as minibrowser

log = logging.getLogger()

class SLDispatcher(QtCore.QObject):
    def __init__(self):
        super().__init__()

        self.searchBar = searchbar.SearchBar()
        self.searchBar.registerForTextChangeEvent(self.textChanged)
        # self.searchBar.installEventFilter(self)

    def eventFilter(self, object, event):
        if object == self.searchBar and \
           event.type() == QtCore.QEvent.WindowDeactivate:
            self.searchBar.hide()

        return False

    def textChanged(self):
        print("dispatch: textChanged: " + self.searchBar.text.text())
