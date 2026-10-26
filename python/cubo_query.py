# load required libraries
import cubo
import xarray as xr

# basic cubo query with required data calls
# soil data might fail as the temporal window
# does not necessarily overlap with the data acqusition
# a separate time agnostic query + merge might be required 
dt = cubo.create(
    # set query location
    lat=51.3397,
    lon=12.3731,
    
    # set data to query
    collection=[
        "sentinel-2-l2a",
        "sentinel-1-rtc",
        "cop-dem-glo-30"
        ],
    bands={
        "sentinel-2-l2a": ["B02", "B03", "B04", "B08", "SCL"],
        "sentinel-1-rtc": ["vv", "vh"],
        "cop-dem-glo-30": ["data"],
        "ECMWF/ERA5_LAND":["temperature_2m","surface_pressure","total_precipitation_sum","dewpoint_temperature_2m"],
        "ISRIC/SoilGrids250m/v2_0":["val_0_5cm_mean","val_5_15cm_mean","val_15_30cm_mean"],
        "OpenLandMap/SOL/SOL_WATERCONTENT-33KPA_USDA-4B1C_M/v01":["b0","b10", "b30"]
        },
    stac={
        "https://planetarycomputer.microsoft.com/api/stac/v1": "sentinel-2-l2a", # STAC collections
        "https://planetarycomputer.microsoft.com/api/stac/v1": "sentinel-1-rtc",
        "ee": "ECMWF/ERA5_LAND", # GEE collections ERA5
        "ee": "ISRIC/SoilGrids250m/v2_0" #GEE soilgrids (funky time dimensions)
        "ee": "OpenLandMap/SOL/SOL_WATERCONTENT-33KPA_USDA-4B1C_M/v01" #OpenLand (funky time dimensions)
    },
    
    # set temporal window
    start_date="2022-06-01",
    end_date="2022-06-15",
    
    # set cube dimensions
    edge_size=1500,
    units="m",
    resolution=10,
    
    # set output specs
    datatree=True,
    dataset=True,
    xy_coords="center",
)

# quick overview of the demo call
dt["sentinel-1-rtc"]["vv"]
