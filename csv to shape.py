ruta = 'E:\ps1_3.csv' # set the filepath for the input CSV

lon_field = 'Latitude' # set the name for the field containing the longitude
lat_field = 'Longitude' # set the name for the field containing the latitude

crs = 4326 # set the crs as needed

salida = 'E:\ps1_4.shp' # set the filepath for the output shapefile

spatRef = QgsCoordinateReferenceSystem(crs, QgsCoordinateReferenceSystem.EpsgCrsId)

inp_tab = QgsVectorLayer(ruta, 'Input_Table', 'ogr')
fields = inp_tab.fields()

outLayer = QgsVectorFileWriter(salida, 
                               None, 
                               fields, 
                               QgsWkbTypes.Point, 
                               spatRef,
                               "ESRI Shapefile")

pt = QgsPointXY()
outFeature = QgsFeature()

for feat in inp_tab.getFeatures():
    attrs = feat.attributes()
    pt.setX(float(feat[lon_field]))
    pt.setY(float(feat[lat_field]))
    outFeature.setAttributes(attrs)
    outFeature.setGeometry(QgsGeometry.fromPointXY(pt))
    outLayer.addFeature(outFeature)

del outLayer