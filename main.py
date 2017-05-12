#! /usr/bin/python

import sys
import signal
import logging
import Infrastructure.Logging.logger as logger

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import pygs

log = logging.getLogger()

# Ctrl maps to Command on Mac OS X
SHORTCUT_SHOW = "Ctrl+Alt+S"


class MainApplication:
    def __init__(self):
        # Create a Qt application
        self.app = QtWidgets.QApplication(sys.argv)
        self.dialog = None

        menu = QtWidgets.QMenu()
        openAction = menu.addAction("Open")
        openAction.triggered.connect(self.open)

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

        self.shortcut_show = pygs.QxtGlobalShortcut()
        self.shortcut_show.setShortcut(QtGui.QKeySequence(SHORTCUT_SHOW))
        self.shortcut_show.activated.connect(self.settings)

    def run(self):
        # Enter Qt application main loop
        self.app.exec_()
        sys.exit()

    def open(self):
        return

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
    app.run()

if __name__ == "__main__":
    # Ctrl+C behaves as expected with PyQt
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    logger.init()
    logger.print_python_version()

    main()
