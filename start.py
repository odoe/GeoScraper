# This is just a sample of how to use these scripts
from queryresults import QueryServer
from esritogeo import EsriToGeo
from geotofeature import FeatureExport

url = 'http://sampleserver3.arcgisonline.com/ArcGIS/rest/services/Earthquakes/Since_1970/MapServer/0/query'
where = 'Num_Deaths=50'

query = QueryServer()

#json result
result = query.request(where, url)

converter = EsriToGeo()
geojson = converter.convert_to_geo(result)

featureExport = FeatureExport()
# Make sure you have a File GeoDatabase set like below.
# Needed to save results.
workspace = r'C:\WorkSpace\target.gdb'

featureExport.exportToFeature(workspace, geojson, 'points')

print 'Task complete'
