# GeoScraper

Small utility python classes that can be used to query ArcGIS MapServer
services for EsriJSON results and save them into a local File
Geodatabase.

You need [ArcPy] on your machine and update start.py with a valid Query
URL and a where string and you are good to go.

This is not the fastest utility around, as it needs to download and
convert a lot of data, but it works.

[ArcPy]: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//000v000000v7000000
