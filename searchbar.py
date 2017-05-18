#! /usr/bin/python

import sys
import signal
import logging
import Infrastructure.Logging.logger as logger

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

log = logging.getLogger()

SHORTCUT_HIDE = "ESC"


class SLQLineEdit(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(SLQLineEdit, self).__init__(*args, **kwargs)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.customContextMenu)

    def customContextMenu(self):
        menu = QtWidgets.QMenu()
        self.addCustomMenuItems(menu)
        menu.exec_(QtGui.QCursor.pos())

    def addCustomMenuItems(self, menu):
        menu.addAction("Cut", self.cut, QtGui.QKeySequence.Cut)
        menu.addAction("Copy", self.copy, QtGui.QKeySequence.Copy)
        menu.addAction("Paste", self.paste, QtGui.QKeySequence.Paste)
        menu.addSeparator()
        menu.addAction("Select All", self.selectAll, QtGui.QKeySequence.SelectAll)


class SearchBar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setupUI()
        self.setupShortcut()
        self.oldPos = None

    def setupUI(self):
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint |
                            # Hide application from taskbar
                            QtCore.Qt.Tool)

        width = 1200
        height = 27

        # Main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setSpacing(12)
        self.mainLayout.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        # Error bar layout
        self.errorBarLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.errorBarLayout)

        # Search bar layout
        self.searchBarLayout = QtWidgets.QHBoxLayout()
        self.searchBarLayout.setSpacing(16)
        self.mainLayout.addLayout(self.searchBarLayout)

        # Content layout
        self.contentLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.contentLayout)

        self.image = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("Images/magnifier.png")
        self.image.setPixmap(pixmap.scaledToHeight(height, QtCore.Qt.SmoothTransformation))
        self.searchBarLayout.addWidget(self.image)

        self.text = SLQLineEdit()
        self.text.setMinimumWidth(width)
        font = self.text.font()
        font.setPixelSize(height)
        self.text.setFont(font)
        self.text.textChanged.connect(self.textChanged)
        self.searchBarLayout.addWidget(self.text)

        self.center()

    def setupShortcut(self):
        self.hide_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(SHORTCUT_HIDE), self)
        self.hide_shortcut.activated.connect(self.hide)

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
