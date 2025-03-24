from header_processing import *
from functions_processing import *

import time

#%% Generate NDFD coords
# !!!!!!!!!!!! SHOULD NOT HAVE TO BE RUN AGAIN, IF NDFD_coords.nc IS ON DISK !!!!!!!!

# ds = xr.open_dataset(r'C:\Users\alex.schein\Test code and files\Test files\NDFD_example.grib2', engine='cfgrib')

# NDFD_lats = ds.latitude.data
# NDFD_lons = ds.longitude.data

# with Dataset(r'C:\Users\alex.schein\Test code and files\Test files\NDFD_coords.nc', 'w') as f:
#     f.createDimension('x', np.shape(NDFD_lons)[1])
#     f.createDimension('y', np.shape(NDFD_lons)[0])
    
#     lonvar = f.createVariable('lons_NDFD', 'float32', ('y','x'))
#     lonvar[:] = NDFD_lons
    
#     latvar = f.createVariable('lats_NDFD', 'float32', ('y','x'))
#     latvar[:] = NDFD_lats

#%% Global vars

PATH_TO_DOWNLOAD_TO = r"C:\Users\alex.schein\Test code and files\Test files\Herbie_downloads"

#bounds of rectangular subregion of interest, in degrees
# MIN_LAT = 37 
# MIN_LON = 360-109

# MAX_LAT = 41
# MAX_LON = 360-104

#%% 

# testing on one HRRR file
H_HRRR = Herbie("2014-08-02 00:00", model="hrrr", product='sfc', save_dir=PATH_TO_DOWNLOAD_TO, verbose=True)
HRRR_t2m = H_HRRR.xarray(r":TMP:surface") #does NOT download to local directory!


ds_coords = xr.open_dataset(r"C:\Users\alex.schein\Test code and files\Test files\NDFD_coords.nc")
ds_coords = ds_coords.rename({"lons_NDFD":"lon", "lats_NDFD":"lat"}) #to be safe


#%% 
# SLOW TO BUILD - DON'T REDO

start_cpu1 = time.process_time()
start_wall1 = time.time()
regridder_bilinear = xesmf.Regridder(HRRR_t2m, ds_coords, 'bilinear')
end_cpu1 = time.process_time() - start_cpu1
end_wall1 = time.time() - start_wall1
print(f"Bilinear regridder done. Build time = {end_cpu1} s cpu, {end_wall1} s wall")


start_cpu2 = time.process_time()
start_wall2 = time.time()
regridder_patch = xesmf.Regridder(HRRR_t2m, ds_coords, 'patch')
end_cpu2 = time.process_time() - start_cpu2
end_wall2 = time.time() - start_wall2
print(f"Patch regridder done. Build time = {end_cpu2} s cpu, {end_wall2} s wall")


regridder_bilinear.to_netcdf(r"C:\Users\alex.schein\Test code and files\Test files\regridder_bilinear_HRRRtoNDFD.nc")
regridder_patch.to_netcdf(r"C:\Users\alex.schein\Test code and files\Test files\regridder_patch_HRRRtoNDFD.nc")


#%%


#Fast but doesn't give rectuangular data array........

HRRR_t2m_regridded_bilinear = regridder_bilinear(HRRR_t2m)
HRRR_t2m_regridded_patch = regridder_patch(HRRR_t2m)

#%% 

# testing on one URMA file
H = Herbie("2014-08-02 00:00", model='urma', save_dir=PATH_TO_DOWNLOAD_TO, verbose=False)
H.download()
urma = H.xarray()

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

##### URMA and NDFD grids align but URMA extends further north - also need to deal with the slightly different grid of 2024 data - investigate...


#%%

# projection = ccrs.LambertConformal(
#     central_longitude = -87.5,
#     central_latitude = 38.5,
#     standard_parallels = (38.5,38.5),
#     cutoff = 0)

# fig = plt.figure()#figsize=(12,9))
# ax1 = fig.add_subplot(1,1,1, projection=projection)
# ax2 = fig.add_subplot(1,2,2, projection=projection)

# ax1.set_extent([-114, -98, 32, 45])
# ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=2)
# ax1.add_feature(cfeature.STATES.with_scale('50m'))
# ax1.contourf(HRRR_t2m.longitude.data, HRRR_t2m.latitude.data, HRRR_t2m.t.data, transform=ccrs.PlateCarree(), cmap=cm.coolwarm)
# ax1.set_title("xarray.where selection")

# ax2.set_extent([-114, -98, 32, 45])
# ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=2)
# ax2.add_feature(cfeature.STATES.with_scale('50m'))
# ax2.contourf(subregion_idx.longitude.data, subregion_idx.latitude.data, subregion_idx.t.data, transform=ccrs.PlateCarree(), cmap=cm.coolwarm)
# ax2.set_title("index-based selection")

# plt.savefig(r'C:\Users\alex.schein\Test code and files\selections.png', dpi=300, bbox_inches='tight')