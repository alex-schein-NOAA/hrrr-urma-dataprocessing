from header_processing import *

#%% Global vars

PATH_TO_DOWNLOAD_TO = r"C:\Users\alex.schein\Test code and files\Test files\Herbie_downloads"

#bounds of rectangular subregion of interest, in degrees
MIN_LAT = 37 
MAX_LAT = 41 
MIN_LON = 360-109
MAX_LON = 360-102

INIT_TIME_LIST = ["00"] #members will populate filename in the "t[INIT_TIME]z." portion
FORECAST_TIME_LIST = ["00"] #members will populate filename in the "


#%%

### THIS IS WHERE THE MAIN LOOP WILL GO


#%% 

# testing on one HRRR file
H_HRRR = Herbie("2014-08-01 00:00", model="hrrr", save_dir=PATH_TO_DOWNLOAD_TO, verbose=True)
