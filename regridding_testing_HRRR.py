from header_processing import *
from functions_processing import *

import time

#%% Generate NDFD coords
# !!!!!!!!!!!! SHOULD NOT HAVE TO BE RUN AGAIN, IF NDFD_coords.nc IS ON DISK !!!!!!!!

# GenerateNDFDCoords()

#%% Global vars

PATH_TO_DOWNLOAD_TO = r"C:\Users\alex.schein\Test code and files\Test files\Herbie_downloads"

#%% Dataset DLs

H_HRRR = Herbie("2014-08-02 00:00", model="hrrr", product='sfc', save_dir=PATH_TO_DOWNLOAD_TO, verbose=True)
HRRR_t2m = H_HRRR.xarray(r":TMP:surface") #does NOT download to local directory!

# ds_coords = xr.open_dataset(r"C:\Users\alex.schein\Test code and files\Test files\NDFD_coords.nc")
# ds_coords = ds_coords.rename({"lons_NDFD":"lon", "lats_NDFD":"lat"}) #to be safe

H = Herbie("2014-08-02 00:00", model='urma', save_dir=PATH_TO_DOWNLOAD_TO, verbose=False)
H.download()
URMA_t2m = SelectURMAt2m(H.xarray())


#%% 

# lats_HRRR = HRRR_t2m.t.latitude.data
# lats_NDFD = ds_coords.lat.data
# lats_urma = urma_t2m.latitude.data

# lons_HRRR = HRRR_t2m.t.longitude.data
# lons_NDFD = ds_coords.lon.data
# lons_urma = urma_t2m.longitude.data

##### URMA and NDFD grids align but URMA extends further north - also need to deal with the slightly different grid of 2024 data - investigate...

#%%

#routine to check the following:
    # 1. if a row of lats of dataset1 is completely north of the southernmost row of lats of dataset2
    # 2. if a column of lons of dataset1 is completely east of the westernmost column of lons of dataset2
    # 3. if a row of lats of dataset1 is completely south of the northernmost row of lats of dataset2
    # 4. if a column of lons of dataset1 is completely west of the easternmost column of lats of dataset2
    
# As HRRR is less tall but wider than URMA, should have the following ordering:
    # 1. dataset1 = URMA, dataset2 = HRRR
    # 2. dataset1 = HRRR, dataset2 = URMA
    # 3. dataset1 = URMA, dataset2 = HRRR
    # 4. dataset1 = HRRR, dataset2 = URMA
    
   
def IsSouthOfNorthernmostRow(HRRR_t2m, URMA_t2m):
    #input: HRRR, URMA t2m DataArrays
    #output: vector of bools w/ len = # rows in URMA, same ordering, w/ True if row is COMPLETELY north of southernmost row of lats in HRRR
    
    dataset1 = URMA_t2m.latitude.data
    dataset2 = HRRR_t2m.latitude.data

#%% testing each func

dataset1 = URMA_t2m.latitude.data
dataset2 = HRRR_t2m.latitude.data

#%%

min_lat_ds2 = np.min(dataset2[-1])
output = np.zeros(np.shape(dataset1)[0])
for i in range(np.shape(dataset1)[0]):
    #is max lat in a row of URMA below the min lat of the northernmost row of HRRR?
    max_lat_ds1 = np.max(dataset1[i])
    if min_lat_ds1 >= max_lat_ds2:
        output[i] = True
    else:
        output[i] = False


#%%

test_URMA = URMA_t2m.where((URMA_t2m.latitude >= np.min(HRRR_t2m.latitude.data[0]) ), drop=True)

#%% 
# SLOW TO BUILD - DON'T REDO

# start_cpu1 = time.process_time()
# start_wall1 = time.time()
# regridder_bilinear = xesmf.Regridder(HRRR_t2m, ds_coords, 'bilinear')
# end_cpu1 = time.process_time() - start_cpu1
# end_wall1 = time.time() - start_wall1
# print(f"Bilinear regridder done. Build time = {end_cpu1} s cpu, {end_wall1} s wall")


# start_cpu2 = time.process_time()
# start_wall2 = time.time()
# regridder_patch = xesmf.Regridder(HRRR_t2m, ds_coords, 'patch')
# end_cpu2 = time.process_time() - start_cpu2
# end_wall2 = time.time() - start_wall2
# print(f"Patch regridder done. Build time = {end_cpu2} s cpu, {end_wall2} s wall")


# regridder_bilinear.to_netcdf(r"C:\Users\alex.schein\Test code and files\Test files\regridder_bilinear_HRRRtoNDFD.nc")
# regridder_patch.to_netcdf(r"C:\Users\alex.schein\Test code and files\Test files\regridder_patch_HRRRtoNDFD.nc")


#Fast but doesn't give rectuangular data array........

# HRRR_t2m_regridded_bilinear = regridder_bilinear(HRRR_t2m)
# HRRR_t2m_regridded_patch = regridder_patch(HRRR_t2m)


#%%

projection = ccrs.LambertConformal(
    central_longitude = 265-360,
    central_latitude = 38.5,
    standard_parallels = (38.5,38.5),
    cutoff = 0)

fig = plt.figure()#figsize=(12,9))
ax1 = fig.add_subplot(1,1,1, projection=projection)
# ax2 = fig.add_subplot(1,2,2, projection=projection)

# ax1.set_extent([-114, -98, 32, 45])
ax1.set_extent([236-360, 292-360, 19, 24])
ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=1)
ax1.add_feature(cfeature.STATES.with_scale('50m'))
ax1.scatter(URMA_t2m.longitude.data, URMA_t2m.latitude.data, transform=ccrs.PlateCarree(), s=0.02, c='r', marker='X', label='URMA')
ax1.scatter(HRRR_t2m.longitude.data, HRRR_t2m.latitude.data, transform=ccrs.PlateCarree(), s=0.02, c='k', marker ='X', label='HRRR')
# ax1.scatter(URMA_t2m.longitude.data[186:,:], URMA_t2m.latitude.data[186:,:], transform=ccrs.PlateCarree(), s=0.02, c='r', marker='X', label='URMA')
gl1 = ax1.gridlines(draw_labels=True)
gl1.top_labels=False
gl1.bottom_labels=False
gl1.right_labels=False

# ax1.legend(loc='center left')
ax1.set_title("Misalignment of HRRR and URMA grids, full southern region")

# ax2.set_extent([-114, -98, 32, 45])
# ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=2)
# ax2.add_feature(cfeature.STATES.with_scale('50m'))
# ax2.contourf(subregion_idx.longitude.data, subregion_idx.latitude.data, subregion_idx.t.data, transform=ccrs.PlateCarree(), cmap=cm.coolwarm)
# ax2.set_title("index-based selection")

plt.savefig(r'C:\Users\alex.schein\Test code and files\grid_misalignment_south.png', dpi=300, bbox_inches='tight')