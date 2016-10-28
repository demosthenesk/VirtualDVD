#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
from PyQt4 import QtGui, QtCore

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

        #test if VirtualDVD folder exists in home
        home = QtCore.QDir.homePath()
        v = home + "/VirtualDVD/"
        b = QtCore.QDir(v).exists()

        if b == False:
            #mkdir the folder
            d = QtCore.QDir().mkdir(v)
            if d == False:
                #raise error. Could not create folder
                m = "Could not create virtual dvd folder"
                msg = QtGui.QMessageBox.critical(self.parent(), "Error", m)
                raise Exception(m)

        #create the systray menu
        menu = QtGui.QMenu(parent)
        exitAction = menu.addAction(QtGui.QIcon(QtGui.QPixmap("exit.png")), "Exit")
        mountAction = menu.addAction(QtGui.QIcon(QtGui.QPixmap("mount.png")), "Mount Image...")
        umountAction = menu.addAction(QtGui.QIcon(QtGui.QPixmap("umount.png")), "Unmount Image...")

        self.setContextMenu(menu)
        QtCore.QObject.connect(exitAction, QtCore.SIGNAL('triggered()'), self.exit)
        QtCore.QObject.connect(mountAction, QtCore.SIGNAL('triggered()'), self.mount)
        QtCore.QObject.connect(umountAction, QtCore.SIGNAL('triggered()'), self.umount)

    def exit(self):
        '''Quit the application'''
        QtCore.QCoreApplication.exit()

    def mount(self):
        '''fuseiso mounts an image file'''
        #get virtualdvd folder
        home = QtCore.QDir.homePath()
        vpath = home + "/VirtualDVD"

        #show QFileDialog and selects .ISO, .BIN, .MDF, .IMG and .NRG file.
        fname = QtGui.QFileDialog.getOpenFileName(self.parent(), 'Mount file', QtCore.QDir.homePath(), "Image files (*.iso *.bin *.mdf *.img *.nrg)")

        #mount the image file fname
        cmd = 'fuseiso "' + fname + '" "'+ vpath + '"'
        proc = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE).stdout.read()
        print proc

    def umount(self):
        '''unmounts VirtualDVD'''
        #get virtualdvd folder
        home = QtCore.QDir.homePath()
        vpath = home + "/VirtualDVD"

        cmd = 'gksudo umount ' + vpath
        subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE).stdout.read()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("virtualdvd.png"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()