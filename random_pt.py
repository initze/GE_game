from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
from osgeo import ogr
import argparse
import numpy as np

mode = 'coast'
parser = argparse.ArgumentParser(usage="")
parser.add_argument('-m', '--mode', dest='mode', nargs='?', type=str, help="Mode")
parser.add_argument('-vh', '--viewheight', dest='vh', type=int, default=100000, help="Viewing height in meters in Google Earth. Default is 100,000 (100km)")
args = parser.parse_args()

def geom_sr_from_point(lat, lon, epsg):
    wkt_bbox = 'POLYGON(({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))'.format(lon-0.1, lat-0.1, lon+0.1, lat+0.1)
    geom_bbox = ogr.CreateGeometryFromWkt(wkt_bbox)
    sr_bbox = ogr.osr.SpatialReference()
    sr_bbox.ImportFromEPSG(int(epsg))
    geom_bbox.AssignSpatialReference(sr_bbox)
    return geom_bbox, sr_bbox

def filter_by_location():
    pass

def make_random_point():
    lon = (np.random.random(1)*360-180)[0]
    lat = (np.random.random(1)*180-90)[0]
    return lon, lat



lon, lat = make_random_point()
p = 'vectors/world.shp'


ds = ogr.Open(p)
lyr = ds.GetLayerByIndex(0)
feat = lyr.GetFeature(0)
geom = feat.geometry()

if args.mode == 'coast':
    bnd = geom.Boundary()
    bnd_s = bnd.Simplify(10)
    """
    #reproject to metric system
    #world mercator
    srx_wm = ogr.osr.SpatialReference()
    srx_wm.ImportFromEPSG(3857)
    #latlon
    srx_ll = ogr.osr.SpatialReference()
    srx_ll.ImportFromEPSG(3857)

    bnd_s.TransformTo(srx_wm)
    """
    geom = bnd_s.Buffer(0.01)
    #geom.TransformTo(srx_ll)

g, l = geom_sr_from_point(lat, lon, 4326)

while not ogr.Geometry.Intersects(g, geom):
    lon = (np.random.random(1)*360-180)[0]
    lat = (np.random.random(1)*180-90)[0]
    g, l = geom_sr_from_point(lat, lon, 4326)
ds = None
    
#runKML
doc = KML.kml(
  etree.Comment(' required when using gx-prefixed elements '),
  GX.FlyTo(
    GX.flyToMode('bounce'),
    GX.duration('0.5')
  ),
  KML.Placemark(
    KML.name('gx:altitudeMode Example'),
    KML.Camera(
      KML.altitude(args.vh),
      KML.longitude(str(lon)),
      KML.latitude(str(lat))
    ),
  ),
)
string = etree.tostring(etree.ElementTree(doc),pretty_print=True)

#writeToFile
f = open('outfile.kml', 'w')
f.writelines(string)
f.close()
