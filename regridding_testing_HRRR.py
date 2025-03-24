from header_processing import *
from functions_processing import *


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


#%%


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