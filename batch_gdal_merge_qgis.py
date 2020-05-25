# cartosaur, 2020
#
# python 3.7
# QGIS 3.10.5
#
# This script loops through folders to collect red, green, and blue band input for the merging of neutral colour images with gdal:merge.
# Results are added to the QGIS map canvas.

# import packages
import os
import processing
from osgeo import gdal
from qgis.utils import iface

# assign input- and output directory
dir_in = r'path\to\your\input'
dir_out = r'path\to\your\output'

# loop through folders and subfolders
for path, name, fname in os.walk(dir_in):
    # skip first folder (input directory)
    if path in dir_in:
        continue
        
    # create input list
    rgb_files = list()
    # assign name to output raster
    output_raster = path[-35:] + '_rgb.tif'
    # declare path to output raster
    path_to_raster = os.path.join(dir_out, output_raster)
    
    # loop through files in subfolder
    for file in fname:
        # collect files that end in B2, B3 or B4
        if file.endswith('B2.TIF') or file.endswith('B3.TIF') or file.endswith('B4.TIF'):
            # add files to list
            rgb_files.append(os.path.join(path,file))  
            
    # reverse the list, so the order is B4, B3, and B2
    rgb_files = sorted(rgb_files, reverse = True)
    
    # declare and assign parameters for the GDAL merge utility
    parameters = { 'INPUT' : rgb_files, 'PCT' : False, 'SEPARATE' : True, 'DATA_TYPE' : 5, 'NODATA_INPUT' : None,
                   'NODATA_OUTPUT' : None, 'OPTIONS' : '', 'EXTRA' : '', 'OUTPUT' : path_to_raster  }        
    # spawn a process to run the GDAL merge utitity
    processing.run('gdal:merge', parameters)
    
    # add output rasters to the map canvas
    iface.addRasterLayer(path_to_raster, output_raster)
