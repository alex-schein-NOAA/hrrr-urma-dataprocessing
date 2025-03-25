from header_processing import *


def FindIndicesOfSpecificPoint(LAT=37, LON=251, model='hrrr'): #default coords = SW corner of CO
    #lat and lon are ordered to where north and east are positive, respectively
    #adapted from https://github.com/blaylockbk/pyBKB_v3/blob/master/demo/Nearest_lat-lon_Grid.ipynb     

    # designed to work in both HRRR and URMA grids
    if type(model) is xr.core.dataarray.DataArray: #OVERLOADING: pass URMA dataset (e.g. t2m) in for "model" for this
        ds = model
    elif model=='hrrr':
        H = Herbie("2014-08-02 00:00", model="hrrr", product='sfc', verbose=False)
        ds = H.xarray(r":TMP:surface")
    elif model=='urma':
        H = Herbie("2024-01-01 00:00", model="urma", verbose=False)
        urma = H.download()
        ds = SelectURMAt2m(urma)
    else:
        print("This method only works for HRRR and URMA data. Enter ' model='hrrr' ' or ' model='urma' ' or pass in an URMA DataArray")
        
    abslat = np.abs(ds.latitude.data - LAT)
    abslon = np.abs(ds.longitude.data - LON)
    
    center = np.maximum(abslat, abslon)

    y_c, x_c = np.where(center==np.min(center))
    
    #returns the raw integers of the indices, NOT the xarray or int64
    #ORDER GIVES LON THEN LAT 
    return int(x_c[0]), int(y_c[0])


def SelectURMAt2m(urma):
    #input: list of hypercubes from URMA download via Herbie
    #horrible but needed to account for different dataset structures in different URMA sets
    flag = True
    HYPERCUBE_LOC=0
    while flag:
        try:
            urma_t2m = urma[HYPERCUBE_LOC]['t2m']
            flag=False #should only run if previous line is a success
            print(f"t2m found in hypercube {HYPERCUBE_LOC}")
        except:
            HYPERCUBE_LOC+=1
            if HYPERCUBE_LOC>10:
                flag=False
                print("Something went wrong when trying to locate t2m")
    
    return urma_t2m


def GenerateNDFDCoords():
    
    print("Generating NDFD coordinate NetCDF")
    
    ds = xr.open_dataset(r'C:\Users\alex.schein\Test code and files\Test files\NDFD_example.grib2', engine='cfgrib')

    NDFD_lats = ds.latitude.data
    NDFD_lons = ds.longitude.data

    with Dataset(r'C:\Users\alex.schein\Test code and files\Test files\NDFD_coords.nc', 'w') as f:
        f.createDimension('x', np.shape(NDFD_lons)[1])
        f.createDimension('y', np.shape(NDFD_lons)[0])
        
        lonvar = f.createVariable('lons_NDFD', 'float32', ('y','x'))
        lonvar[:] = NDFD_lons
        
        latvar = f.createVariable('lats_NDFD', 'float32', ('y','x'))
        latvar[:] = NDFD_lats
        
    return

####################################
# TO DO: make master function that calls the 4 below and returns the indices to trim HRRR, URMA so we get a shared domain for regridding

def IsNorthOfSouthernmostRow(HRRR_t2m, URMA_t2m):
    #input: HRRR, URMA t2m DataArrays
    #output: vector of bools w/ len = # rows in URMA, same ordering, w/ True if row is COMPLETELY north of southernmost row of lats in HRRR
    
    dataset1 = URMA_t2m.latitude.data
    dataset2 = HRRR_t2m.latitude.data
    
    max_lat_ds2 = np.max(dataset2[0])
    output = np.zeros(np.shape(dataset1)[0])
    for i in range(np.shape(dataset1)[0]):
        #is min lat in a row of URMA below the max lat of the southernmost row of HRRR?
        min_lat_ds1 = np.min(dataset1[i])
        if min_lat_ds1 >= max_lat_ds2:
            output[i] = True
        else:
            output[i] = False
            
    return output


def IsEastOfWesternmostColumn(HRRR_t2m, URMA_t2m):
    #input: HRRR, URMA t2m DataArrays
    #output: vector of bools w/ len = # columns in HRR, same ordering, w/ True if column is COMPLETELY east of westernmost column of lats in HRRR
    
    dataset2 = URMA_t2m.longitude.data
    dataset1 = HRRR_t2m.longitude.data
    
    max_lon_ds2 = np.max(dataset2[:,0])
    output = np.zeros(np.shape(dataset1)[1])
    for i in range(np.shape(dataset1)[1]):
        #is min lon in a column of HRRR east of the max lon of the westernmost column of URMA?
        min_lon_ds1 = np.max(dataset1[:,i])
        if min_lon_ds1 >= max_lon_ds2:
            output[i] = True
        else:
            output[i] = False
    
    return output