#! /usr/bin/python

import sys
import signal
import logging
import Infrastructure.Logging.logger as logger

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import pygs

import Infrastructure.Dispatcher.dispatcher as dispatcher

log = logging.getLogger()


class MainApplication(QtCore.QObject):
    def __init__(self):
        super().__init__()

        self.settings = QtCore.QSettings('settings.conf', QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

        # Create a Qt application
        self.app = QtWidgets.QApplication(sys.argv)
        self.dispatcher = dispatcher.SLDispatcher()

        self.dialog = None

        self.loadStylesheet()
        self.setupSystemTray()
        self.setupHotKey()

    def loadStylesheet(self):
        ssFile = self.settings.value("theme", "Stylesheets/dark.stylesheet")
        with open(ssFile, "r") as f:
            self.app.setStyleSheet(f.read())

    def setupSystemTray(self):
        menu = QtWidgets.QMenu()
        openAction = menu.addAction("Open")
        openAction.triggered.connect(self.showSearchBar)

        settingAction = menu.addAction("Settings")
        settingAction.triggered.connect(self.showSettings)

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
        hotkey = self.settings.value("Hotkey", "Alt+Space")
        self.show_shortcut.setShortcut(QtGui.QKeySequence(hotkey))
        self.show_shortcut.activated.connect(self.toggleSearchBar)

    def run(self):
        # Enter Qt application main loop
        self.app.exec_()
        sys.exit()

    def showSearchBar(self):
        self.dispatcher.searchBar.show()
        # self.dispatcher.searchBar.raise_()
        self.dispatcher.searchBar.activateWindow()

    def hideSearchBar(self):
        self.dispatcher.searchBar.hide()

    def toggleSearchBar(self):
        if self.dispatcher.searchBar.isVisible():
            self.hideSearchBar()
        else:
            self.showSearchBar()

    def showSettings(self):
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
