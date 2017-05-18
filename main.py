#! /usr/bin/python

import sys
import signal
import logging
import Infrastructure.Logging.logger as logger

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import pygs

import searchbar

log = logging.getLogger()

# Ctrl maps to Command on Mac OS X
HOTKEY_SHOW = "Alt+Space"


class MainApplication(QtCore.QObject):
    def __init__(self):
        super().__init__()

        # Create a Qt application
        self.app = QtWidgets.QApplication(sys.argv)
        self.searchBar = searchbar.SearchBar()

        self.dialog = None

        self.loadStylesheet()
        self.setupSystemTray()
        self.setupHotKey()
        # self.searchBar.installEventFilter(self)

    def loadStylesheet(self):
        ssFile = "Stylesheets/dark.stylesheet"
        with open(ssFile, "r") as f:
            self.searchBar.setStyleSheet(f.read())

    def setupSystemTray(self):
        menu = QtWidgets.QMenu()
        openAction = menu.addAction("Open")
        openAction.triggered.connect(self.showSearchBar)

        settingAction = menu.addAction("Settings")
        settingAction.triggered.connect(self.settings)

        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)

        icon = QtGui.QIcon("Images/spotlight.ico")
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip("Spotlight")
        #self.tray.showMessage("fuga", "moge")

    def setupHotKey(self):
        self.show_shortcut = pygs.QxtGlobalShortcut()
        self.show_shortcut.setShortcut(QtGui.QKeySequence(HOTKEY_SHOW))
        self.show_shortcut.activated.connect(self.toggleSearchBar)

    def eventFilter(self, object, event):
        if object == self.searchBar and \
           event.type() == QtCore.QEvent.WindowDeactivate:
            self.hide()

        return False

    def run(self):
        # Enter Qt application main loop
        self.app.exec_()
        sys.exit()

    def showSearchBar(self):
        self.searchBar.show()
        # self.searchBar.raise_()
        self.searchBar.activateWindow()

    def hideSearchBar(self):
        self.searchBar.hide()

    def toggleSearchBar(self):
        if self.searchBar.isVisible():
            self.hideSearchBar()
        else:
            self.showSearchBar()

    def settings(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setAttribute(QtCore.Qt.WA_QuitOnClose, False)
        self.dialog.setWindowTitle("Setting Dialog")
        self.dialog.show()

    def exit(self):
        sys.exit(0)


def main(args=None):
    # The main routine.
    if args is None:
        args = sys.argv[1:]

    app = MainApplication()
    app.showSearchBar()
    app.run()

if __name__ == "__main__":
    # Ctrl+C behaves as expected with PyQt
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    logger.init()
    logger.print_python_version()

    main()
