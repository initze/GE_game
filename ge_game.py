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

mode = 'coast'
parser = argparse.ArgumentParser(usage="")
parser.add_argument('-m', '--mode', dest='mode', nargs='?', type=str, help="Mode")
parser.add_argument('-shp', '--shapefile', dest='shp', nargs='*', type=str, help="custom Shapefile mode")
parser.add_argument('-vh', '--viewheight', dest='vh', type=int, default=100000, help="Viewing height in meters in Google Earth. Default is 100,000 (100km)")
args = parser.parse_args()

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        hbox = QtGui.QHBoxLayout(self)

        # TODO: Change Styling
        topleft = QtGui.QFrame(self)
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)

        topright = QtGui.QFrame(self)
        topright.setFrameShape(QtGui.QFrame.StyledPanel)

        bottom = QtGui.QFrame(self)
        bottom.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
        self.show()

    def onChanged(self, text):

        self.lbl.setText(text)
        self.lbl.adjustSize()


class GameGui(QtGui.QMainWindow):

    def __init__(self, game_object):
        super(GameGui, self).__init__()

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.initUI()
        self.game = game_object


    # Initiate GUI
    def initUI(self):

        btn_next = QtGui.QPushButton("Next", self)
        btn_next.move(30, 20)
        btn_next.setAutoDefault(True)

        btn_quit = QtGui.QPushButton("Quit", self)
        btn_quit.move(150, 20)

        btn_settings = QtGui.QPushButton("Edit view height", self)
        btn_settings.move(30, 60)

        btn_start = QtGui.QPushButton("Start Menu", self)
        btn_start.move(150, 60)

        btn_next.clicked.connect(self.buttonClick)
        btn_quit.clicked.connect(self.quitClick)
        btn_settings.clicked.connect(self.settingsDialog)
        btn_start.clicked.connect(self.mainMenu)

        self.statusBar()

        self.setGeometry(300, 300, 280, 120)
        self.setWindowTitle('Google Earth Game')
        self.show()

    ######################
    # Button Actions
    def buttonClick(self):
        sender = self.sender()
        self.statusBar().showMessage('Next Object')
        self.game.next()

    def quitClick(self):
        self.close()
    ##################

    def mainMenu(self):
        self.mm = Example()

    def settingsDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
            'Enter new View height in meters:')
        if ok:
            try:
                self.game.vh = float(text)
                self.game.reload()
            except:
                # TODO: pop-up error message
                None

    def newwindow(self):
        self.wid = QtGui.QWidget()
        self.wid.resize(250, 150)
        self.wid.setWindowTitle('NewWindow')
        print "widget opened"
        self.wid.show()



class GE_Game():

    def __init__(self, vh=100000, outfile=r'outfile.kml', input_vector=None):
        self.counter = 0
        self.vh = vh
        self.outfile = outfile
        self.active = True

        if input_vector:
            self.input_vector = input_vector
            self.make_point_series_from_vector()
        else:
            self.make_random_point_series()
        self.next()


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

    def make_point_series_from_vector(self):
        with fiona.open(self.input_vector) as ds:
            self.nfeatures = ds.session.get_length() # get number of features
            self.index = np.arange(0, self.nfeatures, dtype=np.uint16) # make indices
            np.random.shuffle(self.index)
            self.lon, self.lat = np.array([ds[int(i)]['geometry']['coordinates'][:2] for i in self.index]).T

    def make_random_point_series(self, npoints=5):
        print "Creating Points"
        lon_list = []
        lat_list = []
        counter_local = 0
        p = 'vectors/world.shp'
        ds = ogr.Open(p)
        lyr = ds.GetLayerByIndex(0)
        feat = lyr.GetFeature(0)
        geom = feat.geometry()
        while counter_local < npoints:
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


    def reload(self):
        self.make_kml(self.lon[self.counter], self.lat[self.counter])
        os.system(self.outfile)

    def next(self):
        self.make_kml(self.lon[self.counter], self.lat[self.counter])
        os.system(self.outfile)
        self.counter += 1
        if self.counter == self.nfeatures-1:
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



def main():

    # set game modes from input args
    print args.shp
    if args.shp:
        game = GE_Game(input_vector=args.shp[0], vh=args.vh)
    else:
        game = GE_Game(vh=args.vh)

    # Start Gui and run program
    app = QtGui.QApplication(sys.argv)
    ex = GameGui(game)
    sys.exit(app.exec_())

    #ex = StartMenu(game)
    #sys.exit(app.exec_())

if __name__ == "__main__":
    main()