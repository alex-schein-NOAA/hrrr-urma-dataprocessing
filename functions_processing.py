# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 15:49:36 2025

@author: alex.schein
"""

from header_processing import *


def FindIndicesOfSouthwestCornerOfCO_HRRR(MIN_LAT, MIN_LON):
    #Finds the indices of the SW corner of CO
    #Expensive and should only be run once!
    #Designed to be self-contained apart from coords of SW corner
    #lat and lon are ordered to where north and east are positive, respectively
    #thus to find the SW corner of CO that we want to build from, start from the min of both
    
    
    #adapted from https://github.com/blaylockbk/pyBKB_v3/blob/master/demo/Nearest_lat-lon_Grid.ipynb 
    
    
    #random HRRR dataset - coords same between all so specific doesn't matter
    H = Herbie("2014-08-02 00:00", model="hrrr", product='sfc', verbose=False)
    HRRR_t2m = H.xarray(r":TMP:surface")
    
    abslat = np.abs(HRRR_t2m.latitude.data - MIN_LAT)
    abslon = np.abs(HRRR_t2m.longitude.data - MIN_LON)

    center = np.maximum(abslat, abslon)

    y_sw, x_sw = np.where(center==np.min(center))
    
    #returns the raw integers of the indices, NOT the xarray or int64
    #ORDER GIVES LON THEN LAT 
    return int(x_sw[0]), int(y_sw[0])


def FindIndicesOfSpecificPoint(MIN_LAT=37, MIN_LON=251, model='hrrr'):
    
    # designed to work in both HRRR and URMA grids
    if model=='hrrr':
        H = Herbie("2014-08-02 00:00", model="hrrr", product='sfc', verbose=False)
        ds = H.xarray(r":TMP:surface")
    elif model=='urma':
        H = Herbie("2024-01-01 00:00", model="urma", verbose=False)
        H.download()
        ds = H.xarray()[3]
        ds = ds['t2m']
    else:
        print("This method only works for HRRR and URMA data. Enter ' model='hrrr' or ' model='urma' ' ")
        
    abslat = np.abs(ds.latitude.data - MIN_LAT)
    abslon = np.abs(ds.longitude.data - MIN_LON)
    
    center = np.maximum(abslat, abslon)

    y_sw, x_sw = np.where(center==np.min(center))
    
    #returns the raw integers of the indices, NOT the xarray or int64
    #ORDER GIVES LON THEN LAT 
    return int(x_sw[0]), int(y_sw[0])