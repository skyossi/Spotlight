import sys
import logging
import PyQt5.QtCore
import platform

"""
Logger levels (descending order of importance)

CRITICAL
ERROR
WARNING
INFO
DEBUG
NOTSET
"""

def init():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(module)s - %(message)s',
                                  datefmt="%Y-%m-%d %H:%M:%S")

    fileHandler = logging.FileHandler('trace.log', 'w')
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

def printPythonVersion():
    log = logging.getLogger()

    log.debug("===================================")
    log.debug("Python version: " + platform.python_version())
    log.debug("Python architecture 64 bit: " + str(sys.maxsize > 2**32))
    # Qt version (which PyQt was compiled against)
    log.debug("Qt version: " + PyQt5.QtCore.QT_VERSION_STR)
    log.debug("Qt runtime version: " + PyQt5.QtCore.qVersion())
    log.debug("PyQt version: " + PyQt5.QtCore.PYQT_VERSION_STR)
    log.debug("===================================")
