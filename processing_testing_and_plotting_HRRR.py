from header_processing import *
from functions_processing import *


#%% Global vars

PATH_TO_DOWNLOAD_TO = r"C:\Users\alex.schein\Test code and files\Test files\Herbie_downloads"

#bounds of rectangular subregion of interest, in degrees
MIN_LAT = 37 
MAX_LAT = 41 
MIN_LON = 360-109
MAX_LON = 360-104

# Number of pixels to add to MIN_LAT and MIN_LON to get a square image subsample of the data. 
# Currently choosing the same value but can change if rectangular region is more representative and still easy to work with
# Remember 1 pixel = 3x3 km
IMG_SIZE_LAT = 160
IMG_SIZE_LON = 160


INIT_TIME_LIST = ["00"] #members will populate filename in the "t[INIT_TIME]z." portion
FORECAST_TIME_LIST = ["00"] #members will populate filename in the "wrfsfc[FORECAST_TIME]" portion


#%%

### THIS IS WHERE THE MAIN LOOP WILL GO

#%% 

# testing on one HRRR file
H_HRRR = Herbie("2014-08-02 00:00", model="hrrr", product='sfc', save_dir=PATH_TO_DOWNLOAD_TO, verbose=True)

HRRR_t2m = H_HRRR.xarray(r":TMP:surface") #does NOT download to local directory!

#%%
# spatial subsetting
# NOT using the Herbie pick_points() method b/c it shouldn't preserve spatial structure - though it is likely superior for single-point data

# easiest: using .where, but this results in NaNs
subregion_where = HRRR_t2m.where((HRRR_t2m.latitude>MIN_LAT)&(HRRR_t2m.latitude<MAX_LAT)&(HRRR_t2m.longitude>MIN_LON)&(HRRR_t2m.longitude<MAX_LON), drop=True)

# less easy: appealing to x/y dimensions and doing index selection to get a square region
# "square" is relative - due to the projection, this is actually a distorted rectangle with curved sides and wider bottom than top when projected onto the HRRR map

IDX_MIN_LON, IDX_MIN_LAT = FindIndicesOfSouthwestCornerOfCO_HRRR(MIN_LAT-0.5, MIN_LON+0.2)

subregion_idx = HRRR_t2m.isel(y=slice(IDX_MIN_LAT, IDX_MIN_LAT+IMG_SIZE_LAT),
                              x=slice(IDX_MIN_LON, IDX_MIN_LON+IMG_SIZE_LON))


#%%
# plt.figure()
# subregion_where.t.plot(cmap=cm.coolwarm)
# plt.figure()
# subregion_idx.t.plot(cmap=cm.coolwarm)


#%% 

projection = ccrs.LambertConformal(
    central_longitude = -87.5,
    central_latitude = 38.5,
    standard_parallels = (38.5,38.5),
    cutoff = 0)

fig = plt.figure()#figsize=(12,9))
ax1 = fig.add_subplot(1,2,1, projection=projection)
ax2 = fig.add_subplot(1,2,2, projection=projection)

ax1.set_extent([-114, -98, 32, 45])
ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=2)
ax1.add_feature(cfeature.STATES.with_scale('50m'))
ax1.contourf(subregion_where.longitude.data, subregion_where.latitude.data, subregion_where.t.data, transform=ccrs.PlateCarree(), cmap=cm.coolwarm)
ax1.set_title("xarray.where selection")

ax2.set_extent([-114, -98, 32, 45])
ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=2)
ax2.add_feature(cfeature.STATES.with_scale('50m'))
ax2.contourf(subregion_idx.longitude.data, subregion_idx.latitude.data, subregion_idx.t.data, transform=ccrs.PlateCarree(), cmap=cm.coolwarm)
ax2.set_title("index-based selection")

plt.savefig(r'C:\Users\alex.schein\Test code and files\selections.png', dpi=300, bbox_inches='tight')