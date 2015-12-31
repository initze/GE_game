from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from osgeo import ogr
import numpy as np
import os
import sys
from PyQt4 import QtGui, QtCore
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
# TODO: make main Menu Ui separate

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui=Ui_MainWindow()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.ui.setupUi(self)
        self.settingsMenu = Settings()
        self.gameMenu = GameMenu()


        # mainMenu Actions
        self.ui.pushButton.clicked.connect(self.start_game)
        self.ui.pushButton_2.clicked.connect(self.quit_game)
        self.ui.toolButton.clicked.connect(self.showDialog)

        # settingsMenu Actions
        self.settingsMenu.ui.pushButton.clicked.connect(self.update_vh)
        self.settingsMenu.ui.pushButton.clicked.connect(self.show_game)
        self.settingsMenu.ui.pushButton_2.clicked.connect(self.back_to_main)

        # gameMenu Actions
        self.gameMenu.ui.pushButton_Previous.clicked.connect(self.previous_feature)
        self.gameMenu.ui.pushButton_Next.clicked.connect(self.next_feature)
        self.gameMenu.ui.pushButton_Quit.clicked.connect(self.back_to_main)
        self.gameMenu.ui.pushButton_Settings.clicked.connect(self.show_settings)
        self.gameMenu.ui.pushButton_Reload.clicked.connect(self.restart_game)
        self.gameMenu.ui.pushButton_Solution.clicked.connect(self.show_solution)
        self.show()

    def autoset_game_mode(self):
        # check out selected mode and call SubClass accordingly
        if self.ui.radioButton.isChecked():
            self.game = GE_Game_random(npoints=self.ui.spinBox.value())
        elif (self.ui.radioButton_2.isChecked()) and (self.fname):
            self.game = GE_Game_Vector(self.fname)

    def back_to_main(self):
        self.game = None
        self.settingsMenu.hide()
        self.settingsMenu.ui.pushButton_2.setEnabled(False)
        self.gameMenu.hide()
        self.gameMenu.ui.pushButton_Next.setEnabled(True)
        self.gameMenu.ui.pushButton_Reload.setEnabled(False)
        self.show()

    def showDialog(self):
        """
        File selection pop-up dialog
        :return:
        """
        filters = "Vector Files(*.shp *.kml)"
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                os.getcwd(), filters)
        self.ui.radioButton_2.setChecked(True)
        self.ui.radioButton.setChecked(False)
        self.ui.lineEdit_filePath.setText(self.fname)

    def check_gameMenu_setup(self):
        """
        Check current status and setup active and inactive features of settingsMenu
        :return:
        """
        if self.game.counter == 0:
            #previous and reload disabled
            self.gameMenu.ui.pushButton_Previous.setEnabled(False)
            self.gameMenu.ui.pushButton_Reload.setEnabled(False)
        if self.game.counter == self.game.nfeatures-1:
            #next disabled reload enabled
            self.gameMenu.ui.pushButton_Previous.setEnabled(True)
            self.gameMenu.ui.pushButton_Next.setEnabled(False)
            self.gameMenu.ui.pushButton_Reload.setEnabled(True)
        else:
            #reload disabled others enabled
            self.gameMenu.ui.pushButton_Previous.setEnabled(True)
            self.gameMenu.ui.pushButton_Next.setEnabled(True)
            self.gameMenu.ui.pushButton_Reload.setEnabled(False)

    def show_settings(self):
        """
        Show settingsMenu and hide other widgets
        :return:
        """
        self.set_settings_table()
        self.settingsMenu.show()
        self.gameMenu.hide()

    def set_settings_table(self):
        """
        Setup table within settingsMenu for solution field selection
        :return:
        """
        self.settingsMenu.ui.tableWidget.setHorizontalHeaderLabels(['Field', 'Example'])
        self.settingsMenu.ui.tableWidget.setRowCount(self.game.nfields)
        self.settingsMenu.ui.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        for fname, fval, i in zip(self.game.fieldname, self.game.fieldvalue, range(self.game.nfields)):
            self.settingsMenu.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(fname))
            self.settingsMenu.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(str(fval)))
        self.settingsMenu.ui.tableWidget.setEnabled(True)
        self.settingsMenu.ui.tableWidget.selectRow(self.selected_table_row)
        #self.settingsMenu.row_select = int(self.settingsMenu.ui.tableWidget.currentRow())

    def update_vh(self):
        """
        Update manually selected view-height
        :return:
        """
        self.game.vh = float(self.settingsMenu.ui.lineEdit.text())

    def show_game(self):

        #self.game.get_solutions(idx)
        self.check_gameMenu_setup()
        self.settingsMenu.hide()
        self.gameMenu.show()
        self.current_feature()

    def start_game(self):
        """
        Set-up game and create point-series
        :return:
        """
        # check out selected mode and call SubClass accordingly
        self.selected_table_row = 0
        self.autoset_game_mode()
        self.hide()
        self.game.make_point_series()
        self.game.get_fields() # check
        self.settingsMenu.ui.lineEdit.setText(str(self.game.vh))
        self.show_settings()

    # TODO: Fix Bug - finished after 2 features after reload
    def restart_game(self):
        self.game.make_point_series()
        self.game.counter=0
        self.update_feature_counter()
        self.current_feature()
        self.gameMenu.ui.pushButton_Next.setEnabled(True)
        self.gameMenu.ui.pushButton_Reload.setEnabled(False)

    def file_loader(self):
        self.game.input_vector = str(QtGui.QFileDialog.getOpenFileName()) # Filename line
        self.ui.radioButton_2.setChecked(True)
        self.ui.radioButton.setChecked(False)

    def current_feature(self):
        """
        load current feature
        :return:
        """
        self.game.call_current()
        self.update_feature_counter()
        self.check_gameMenu_setup()

    def next_feature(self):
        """
        load next feature
        :return:
        """
        self.game.call_next()
        self.update_feature_counter()
        self.check_gameMenu_setup()
        self.clear_solution_field()

    def previous_feature(self):
        """
        load previous feature
        :return:
        """
        self.game.call_previous()
        self.update_feature_counter()
        self.check_gameMenu_setup()
        self.clear_solution_field()

    def quit_game(self):
        self.close()

    def update_feature_counter(self):
        self.gameMenu.ui.label.setText('Feature: {0} / {1}'.format(self.game.counter+1, self.game.nfeatures))

    def show_solution(self):
        """
        print solution to specified lineEdit widget
        :return:
        """
        self.selected_table_row = int(self.settingsMenu.ui.tableWidget.currentRow())
        self.game.get_solution(self.selected_table_row, int(self.game.index[self.game.counter]))
        self.gameMenu.ui.lineEdit_Solution.setText(self.game.solution)

    def clear_solution_field(self):
        """
        Clear solution lineEdit widget
        :return:
        """
        self.gameMenu.ui.lineEdit_Solution.setText('')

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

    def call_current(self):
        self.make_kml(self.lon[self.counter], self.lat[self.counter])
        os.system(self.outfile)

    def call_next(self):
        self.counter += 1
        self.make_kml(self.lon[self.counter], self.lat[self.counter])
        os.system(self.outfile)
        if self.counter == self.nfeatures-1:
            self.active = False

    def call_previous(self):
        if self.counter == 0:
            return
        self.counter -= 1
        self.make_kml(self.lon[self.counter], self.lat[self.counter])
        os.system(self.outfile)

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

    def get_fields(self):
        self.nfields = None
        self.fieldname = None
        self.fieldvalue = None
        pass

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
        self.solution = ''
        self.nfields = 0
        self.nfeatures = 0

    def make_point_series(self):
        ds = ogr.Open(self.input_vector)
        lyr = ds.GetLayerByIndex(0)
        self.nfeatures = lyr.GetFeatureCount()
        self.index = np.arange(0, self.nfeatures, dtype=np.uint16) # make indices
        np.random.shuffle(self.index)
        pts = []
        for i in self.index:
            i = int(i)
            lyr = ds.GetLayerByIndex(0)
            feat = lyr.GetFeature(i)
            pts.append(feat.geometry().GetPoint())
        self.lon, self.lat, _ = np.array(pts).T
        ds = None

    def get_fields(self):
        ds = ogr.Open(self.input_vector)
        lyr = ds.GetLayerByIndex(0)
        feat = lyr.GetFeature(0)
        self.nfields = feat.GetFieldCount()
        self.fieldname, self.fieldvalue = np.array([(feat.GetFieldDefnRef(i).GetName(), feat.GetField(i))
                                                    for i in range(self.nfields)]).T
        ds = None

    def get_solution(self, field_id, index_id):
        ds = ogr.Open(self.input_vector)
        lyr = ds.GetLayerByIndex(0)
        feat = lyr.GetFeature(index_id)
        self.solution = feat.GetField(field_id)

def main():
    # Start Gui and run program
    app = QtGui.QApplication (sys.argv)
    m = MainWindow()
    sys.exit (app.exec_ () )

if __name__ == "__main__":
    main()