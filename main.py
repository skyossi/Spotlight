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
HOTKEY_SHOW = "Shift+Space"
SHORTCUT_HIDE = "ESC"

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
       super().__init__()

       self.setupUI()
       self.oldPos = None

    def setupUI(self):
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint |
                            # Hide application from taskbar
                            QtCore.Qt.Tool)

        height = 54
        self.setStyleSheet("background-color: rgb(66, 66, 66)")

        grid = QtWidgets.QGridLayout(self)
        grid.setHorizontalSpacing(15)

        self.image = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("Images/magnifier.png")
        self.image.setPixmap(pixmap.scaledToHeight(height / 2, QtCore.Qt.SmoothTransformation))
        grid.addWidget(self.image, 0, 0)

        self.text = QtWidgets.QLineEdit(self)
        font = self.text.font()
        font.setPixelSize(height / 2)
        self.text.setFont(font)
        self.text.setStyleSheet("QLineEdit { color: rgb(200, 200, 200); \
                                             background-color: rgb(66, 66, 66); \
        	                                 border: none; \
                                	         outline: none;}")
        self.text.textChanged.connect(self.textChanged)
        grid.addWidget(self.text, 0, 1)

        self.resize(900, height)
        self.center()

    def center(self):
        frame = self.frameGeometry()
        frame.moveCenter(QtWidgets.QApplication.desktop().screenGeometry().center())
        self.setGeometry(frame)
        
    def textChanged(self):
        print("textChanged: " + self.text.text())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


class MainApplication(QtCore.QObject):
    def __init__(self):
        super().__init__()

        # Create a Qt application
        self.app = QtWidgets.QApplication(sys.argv)
        self.mainWindow = MainWindow()

        self.dialog = None

        self.setupSystemTray()
        self.setupHotKey()
        self.setupShortcut()
        # self.mainWindow.installEventFilter(self)

    def setupSystemTray(self):
        menu = QtWidgets.QMenu()
        openAction = menu.addAction("Open")
        openAction.triggered.connect(self.show)

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
        self.show_shortcut.activated.connect(self.show)

    def setupShortcut(self):
        self.hide_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(SHORTCUT_HIDE), self.mainWindow)
        self.hide_shortcut.activated.connect(self.hide)

    def eventFilter(self, object, event):
        if object == self.mainWindow and \
           event.type() == QtCore.QEvent.WindowDeactivate:
            self.hide()

        return False

    def run(self):
        # Enter Qt application main loop
        self.app.exec_()
        sys.exit()

    def show(self):
        self.mainWindow.show()
        # self.mainWindow.raise_()
        self.mainWindow.activateWindow()        

    def hide(self):
        self.mainWindow.hide()

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
    app.show()
    app.run()

if __name__ == "__main__":
    # Ctrl+C behaves as expected with PyQt
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    logger.init()
    logger.print_python_version()

    main()
