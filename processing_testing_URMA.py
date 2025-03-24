from header_processing import *
from functions_processing import *


#%% Global vars

PATH_TO_DOWNLOAD_TO = r"C:\Users\alex.schein\Test code and files\Test files\Herbie_downloads"

MODEL='URMA'

#bounds of rectangular subregion of interest, in degrees
MIN_LAT = 37 
MAX_LAT = 41 
MIN_LON = 360-109
MAX_LON = 360-104

# Shift amount for index-based grid selection
# Due to how this selection works, need to go south and east a little bit with the SW corner of the grid
EPSILON_LAT = -0.3
EPSILON_LON = 0.25

# Number of pixels to add to MIN_LAT and MIN_LON to get a square image subsample of the data. 
# Currently choosing the same value but can change if rectangular region is more representative and still easy to work with
# Remember 1 pixel = 3x3 km
IMG_SIZE_LAT = 180
IMG_SIZE_LON = 180

#Should only be run once, never in a loop
IDX_MIN_LON, IDX_MIN_LAT = FindIndicesOfSpecificPoint(MIN_LAT+EPSILON_LAT, MIN_LON+EPSILON_LON, model='urma')


#%% 
# testing on one URMA file
H = Herbie("2014-08-02 00:00", model=MODEL, save_dir=PATH_TO_DOWNLOAD_TO, verbose=False)
H.download()
urma = H.xarray()

#%%
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
            
#%%
# spatial subsetting
# NOT using the Herbie pick_points() method b/c it shouldn't preserve spatial structure - though it is likely superior for single-point data

# easiest: using .where, but this results in NaNs
subregion_where = urma_t2m.where((urma_t2m.latitude>MIN_LAT)
                                 &(urma_t2m.latitude<MAX_LAT)
                                 &(urma_t2m.longitude>MIN_LON)
                                 &(urma_t2m.longitude<MAX_LON), 
                                 drop=True)

# less easy: appealing to x/y dimensions and doing index selection to get a square region
# "square" is relative - due to the projection, this is actually a distorted rectangle with curved sides and wider bottom than top when projected onto the urma map

subregion_idx = urma_t2m.isel(y=slice(IDX_MIN_LAT, IDX_MIN_LAT+IMG_SIZE_LAT),
                              x=slice(IDX_MIN_LON, IDX_MIN_LON+IMG_SIZE_LON))

#%% 

projection = ccrs.LambertConformal(
    central_longitude = -87.5,
    central_latitude = 38.5,
    standard_parallels = (38.5,38.5),
    cutoff = 0)

fig = plt.figure()
plt.suptitle(f"Regional selection, {MODEL} grid", y=0.88, fontsize=13)
ax1 = fig.add_subplot(1,2,1, projection=projection)
ax2 = fig.add_subplot(1,2,2, projection=projection)

ax1.set_extent([-114, -98, 32, 45])
ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=2)
ax1.add_feature(cfeature.STATES.with_scale('50m'))
ax1.contourf(subregion_where.longitude.data, subregion_where.latitude.data, subregion_where.data, transform=ccrs.PlateCarree(), cmap=cm.coolwarm)
ax1.set_title("xarray.where selection")

ax2.set_extent([-114, -98, 32, 45])
ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=2)
ax2.add_feature(cfeature.STATES.with_scale('50m'))
ax2.contourf(subregion_idx.longitude.data, subregion_idx.latitude.data, subregion_idx.data, transform=ccrs.PlateCarree(), cmap=cm.coolwarm)
ax2.set_title("index-based selection")

plt.savefig(r'C:\Users\alex.schein\Test code and files\selections.png', dpi=300, bbox_inches='tight')