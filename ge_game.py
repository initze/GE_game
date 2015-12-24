from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
from osgeo import ogr
import argparse
import numpy as np
import fiona
import os
import sys
from PyQt4 import QtGui, Qt, QtCore
from mainMenu import Ui_MainWindow
from gameMenu import Ui_GameMenu
from settingsMenu import Ui_SettingsMenu


class Settings(QtGui.QWidget):
    def __init__(self):
        super(Settings, self).__init__()
        self.ui = Ui_SettingsMenu()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)


class GameMenu(QtGui.QWidget):
    def __init__(self):
        super(GameMenu, self).__init__()
        self.ui = Ui_GameMenu()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

# TODO: restart needs to be fixed
# TODO: auto reload for settings
# TODO: make main Menu Ui separate

class MainWindow(QtGui.QMainWindow):
    #def __init__(self, game):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui=Ui_MainWindow()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.ui.setupUi(self)
        self.settingsMenu = Settings()
        self.gameMenu = GameMenu()

        # mainMenu Actions
        self.ui.pushButton.clicked.connect(self.start_game2)
        self.ui.pushButton_2.clicked.connect(self.quit_game)
        self.ui.toolButton.clicked.connect(self.showDialog)

        # settingsMenu Actions
        self.settingsMenu.ui.pushButton.clicked.connect(self.update_vh)
        self.settingsMenu.ui.pushButton.clicked.connect(self.show_game)
        self.settingsMenu.ui.pushButton_2.clicked.connect(self.back_to_main)

        # gameMenu Actions
        self.gameMenu.ui.pushButton_Next.clicked.connect(self.next_feature)
        self.gameMenu.ui.pushButton_Quit.clicked.connect(self.back_to_main)
        self.gameMenu.ui.pushButton_Settings.clicked.connect(self.show_settings)
        self.show()

    def back_to_main(self):
        self.settingsMenu.hide()
        self.settingsMenu.ui.pushButton_2.setEnabled(False)
        self.gameMenu.hide()
        self.show()

    def showDialog(self):
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                os.getcwd())
        self.ui.radioButton_2.setChecked(True)
        self.ui.radioButton.setChecked(False)
        #TODO: show filename
        self.ui.lineEdit_filePath.setText(self.fname)

    def show_settings_onstart(self):
        if self.ui.radioButton.isChecked():
            self.mode = 1
            self.game.vh = 100000
        elif self.ui.radioButton_2.isChecked():
            self.mode=2
            self.game.vh = 7000
        self.settingsMenu.show()
        self.hide()
        self.game.next()

    def show_settings(self):
        self.settingsMenu.show()
        self.gameMenu.hide()

    def update_vh(self):
        self.game.vh = float(self.settingsMenu.ui.lineEdit.text())
        #self.game.reload() # needs some improvement

    def show_game(self):
        self.settingsMenu.hide()
        self.gameMenu.show()

    def start_game(self):
        self.game = GE_Game()
        self.settingsMenu.hide()
        self.settingsMenu.ui.pushButton_2.setEnabled(False)
        self.hide()
        self.gameMenu.show()
        self.game.make_random_point_series(npoints=self.ui.spinBox.value())
        self.game.next()
        self.update_feature_counter()

    def start_game2(self):
        # check out selected mode and call SubClass accordingly
        if self.ui.radioButton.isChecked():
            self.game = GE_Game_random(npoints=self.ui.spinBox.value())
        elif (self.ui.radioButton_2.isChecked()) and (self.fname):
            self.game = GE_Game_Vector(self.fname)
        else:
            return
        self.settingsMenu.ui.lineEdit.setText(str(self.game.vh))
        self.settingsMenu.show()
        self.hide()
        self.game.make_point_series()

    def file_loader(self):
        self.game.input_vector = str(QtGui.QFileDialog.getOpenFileName()) # Filename line
        print self.game.input_vector
        print os.path.exists(self.game.input_vector)
        self.ui.radioButton_2.setChecked(True)
        self.ui.radioButton.setChecked(False)

    def next_feature(self):
        self.game.next()
        self.update_feature_counter()
        if not self.game.active:
            self.gameMenu.ui.pushButton_Next.setEnabled(False)
            self.gameMenu.ui.pushButton_Reload.setEnabled(True)

    def quit_game(self):
        self.close()

    def update_feature_counter(self):
        self.gameMenu.ui.label.setText('Feature: {0} / {1}'.format(self.game.counter, self.game.nfeatures))

class GE_Game():

    def __init__(self, outfile=r'outfile.kml'):
        self.counter = 0
        self.outfile = outfile
        self.active = True

    def make_kml(self, lon, lat):
        """
        :return: write kml file from defined properties
        """
        doc = KML.kml(
        etree.Comment(' required when using gx-prefixed elements '),
        GX.FlyTo(
        GX.flyToMode('bounce'),
        GX.duration('0.5')
        ),
        KML.Placemark(
        KML.name('gx:altitudeMode Example'),
        KML.Camera(
          KML.altitude(self.vh),
          KML.longitude(str(lon)),
          KML.latitude(str(lat))
        ),
        ),
        )
        string = etree.tostring(etree.ElementTree(doc),pretty_print=True)
        #writeToFile
        f = open(self.outfile, 'w')
        f.writelines(string)
        f.close()

    # TODO: needs to be fixed
    def reload(self):
        self.make_kml(self.lon[self.counter], self.lat[self.counter])
        os.system(self.outfile)
    # TODO: needs to be fixed
    def next(self):
        self.make_kml(self.lon[self.counter], self.lat[self.counter])
        os.system(self.outfile)
        self.counter += 1
        if self.counter == self.nfeatures:
            self.active = False

    @staticmethod
    def make_random_point():
        lon = (np.random.random(1)*360-180)[0]
        lat = (np.random.random(1)*180-90)[0]
        return lon, lat

    @staticmethod
    def geom_sr_from_point(lat, lon, epsg):
        wkt_bbox = 'POLYGON(({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))'.format(lon-0.1, lat-0.1, lon+0.1, lat+0.1)
        geom_bbox = ogr.CreateGeometryFromWkt(wkt_bbox)
        sr_bbox = ogr.osr.SpatialReference()
        sr_bbox.ImportFromEPSG(int(epsg))
        geom_bbox.AssignSpatialReference(sr_bbox)
        return geom_bbox, sr_bbox

class GE_Game_random(GE_Game):
    def __init__(self, npoints, vh=100000, outfile=r'outfile.kml'):
        self.counter = 0
        self.vh = 100000
        self.outfile = outfile
        self.active = True
        self.npoints = npoints

    def make_point_series(self):
        print "Creating Points"
        lon_list = []
        lat_list = []
        counter_local = 0
        p = 'vectors/world.shp'
        ds = ogr.Open(p)
        lyr = ds.GetLayerByIndex(0)
        feat = lyr.GetFeature(0)
        geom = feat.geometry()
        while counter_local < self.npoints:
            lon, lat = self.make_random_point()
            g, l = self.geom_sr_from_point(lat, lon, 4326)
            if ogr.Geometry.Intersects(g, geom):
                lon_list.append(lon)
                lat_list.append(lat)
                counter_local += 1
                print counter_local
        ds = None
        self.nfeatures = len(lon_list)
        self.lon = np.array(lon_list)
        self.lat = np.array(lat_list)

class GE_Game_Vector(GE_Game):

    def __init__(self, input_vector, vh=5000, outfile=r'outfile.kml'):
        self.counter = 0
        self.vh = vh
        self.outfile = outfile
        self.active = True
        self.input_vector = os.path.abspath(input_vector)

    def make_point_series(self):
        with fiona.open(self.input_vector) as ds:
            self.nfeatures = ds.session.get_length() # get number of features
            self.index = np.arange(0, self.nfeatures, dtype=np.uint16) # make indices
            np.random.shuffle(self.index)
            self.lon, self.lat = np.array([ds[int(i)]['geometry']['coordinates'][:2] for i in self.index]).T

def main():
    # Start Gui and run program
    app = QtGui.QApplication (sys.argv)
    m = MainWindow()
    sys.exit (app.exec_ () )

if __name__ == "__main__":
    main()