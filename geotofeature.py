import arcpy

class FeatureExport:
  # This is a script that I use to convert geojson to
  # features in a file gdb
  # Step 1. Use the REST page of an ArcGIS Map Service to
  # 	get the esri json results of the data you want.
  # Step 2. I used my EsriJSON to GeoJSON app to convert
  #	the results to geojson. http://esritogeo.herokuapp.com/
  # Step 3. In ArcMap, use the python window to create a
  #	python dictionary of your geojson.
  # Step4. Use the following script to convert that geojson
  #	into featureclasses and then merge them.

  def exportToFeature(self, workspace, geojson, outputName):
    arcpy.env.workspace = workspace
    # I'm going to save my features to a list for merge later
    items = []
    count = 0
    for g in geojson["features"]:
      # Refer to AsShape docs
        # http://help.arcgis.com/en/arcgisdesktop/10.0/help/000v/000v00000153000000.htm
        # AsShape only creates a geometry object, so it's up to you
        # 	to use the AddField/Calculate field tools if you want to get the
        # 	attribute data across.
        geom = arcpy.AsShape(g["geometry"])

        feature = outputName + "_" + str(count)
        count = count + 1
        # refer to the Copy Features docs
        # http://help.arcgis.com/en/arcgisdesktop/10.0/help/0017/001700000035000000.htm
        arcpy.CopyFeatures_management(geom, feature)

        # iterate fields and add them to feature, but do it only once
        for f in g["properties"]:
          isnot_default = f.find('Shape') < 0
          value = None
          print 'Currently adding field: ', f
          # refer to the AddField docs
          # http://help.arcgis.com/en/arcgisdesktop/10.0/help/0017/001700000047000000.htm
          curr_val = g["properties"][f]
          if isinstance(curr_val, int) and isnot_default:
            print 'adding a SHORT field', f
            if f.find('OBJECTID') < 0:
              arcpy.AddField_management(feature, f, "SHORT", field_alias=f)
              value = g["properties"][f] or 0
          elif isinstance(curr_val, float) and isnot_default:
            print 'adding a DOUBLE field', f
            arcpy.AddField_management(feature, f, "DOUBLE", field_scale=8, field_alias=f)
            value = g["properties"][f] or 0
          elif isinstance(curr_val, long) and isnot_default:
            # This was giving me trouble.
            # If I use a long, unable to calculate field.
            # Usually occurs with date fields, but don't register as date
            # objects in Python
            print 'adding a DOUBLE field from a python long', f
            if f.find('OBJECTID') < 0:
              arcpy.AddField_management(feature, f, "DOUBLE", field_scale=8, field_alias=f)
              #arcpy.AddField_management(feature, f, "LONG", field_precision=len(str(f))+1, field_alias=f)
              value = g["properties"][f]
          elif isnot_default:
            print 'adding a TEXT field', f
            arcpy.AddField_management(feature, f, "TEXT", field_length=50, field_alias=f)
            if g["properties"][f] != None:
              value = '"' + g["properties"][f] + '"'

          # refer to the CalculateField docs
          # http://help.arcgis.com/en/arcgisdesktop/10.0/help/0017/00170000004m000000.htm
          try:
            if isnot_default and value != None:
              print 'Calculating field: {%s} with value: {%s}' % (f, value)
              arcpy.CalculateField_management(feature, f, value, "PYTHON")
          except Exception, e:
            print 'Error calculating field:', f
            print e
        # save my features to a list
        items.append(feature)
        del geom

    target = outputName
    # refer to Merge docs
    # http://help.arcgis.com/en/arcgisdesktop/10.0/help/0017/001700000055000000.htm
    arcpy.Merge_management(items, target)
    # then loop my list and
    # delete my individual features
    # http://help.arcgis.com/en/arcgisdesktop/10.0/help/0017/001700000052000000.htm
    # This only deleted them from my map project, not the file gdb

    for i in items:
        arcpy.Delete_management(i, "")
    del items

    # If someone knows of a more efficient way to do this, I'd love to hear about it.
    # This script isn't exactly a speed demon.
