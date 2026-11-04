# load required libraries
import cubo
import ee
import xarray as xr

# initialize GEE
ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')

lat=51.3397
lon=12.3731
edge_size=250 # in meters
resolution=10 # in meters
start_date="2021-04-01",
end_date="2021-04-15",

# # get sentinel data
# sen = cubo.create(
#     # set query location
#     lat=lat,
#     lon=lon,
# 
#     # set data to query
#     collection=[
#         "sentinel-2-l2a",
#         "sentinel-1-rtc"
#         ],
#     bands={
#         "sentinel-2-l2a": ["B02", "B03", "B04", "B08", "SCL"],
#         "sentinel-1-rtc": ["vv","vh"]
#         },
# 
#     # set temporal window
#     start_date = start_date,
#     end_date = end_date,
# 
#     # set cube dimensions
#     edge_size = edge_size,
#     units = "m",
#     resolution = resolution,
# 
#     # set output specs
#     datatree = True,
#     dataset = True,
#     xy_coords = "center",
# )

 
# # grab DEM data (static)
# dem = cubo.create(
#     # set query location
#     lat=lat,
#     lon=lon,
# 
#     # set data to query
#     collection=[
#         "cop-dem-glo-30"
#         ],
#     bands={
#         "cop-dem-glo-30": ["data"]
#         },
# 
#     # set temporal window
#     start_date="2021-04-21",
#     end_date="2021-04-21",
# 
#     # set cube dimensions
#     edge_size=edge_size,
#     units="m",
#     resolution=resolution,
# 
#     # set output specs
#     datatree=True,
#     dataset=True,
#     xy_coords="center",
# )
#sen['cop-dem-glo-30'] = dem['cop-dem-glo-30']
 
# # get GEE based data (climate and soil)
# gee = cubo.create(
#     # set query location
#     lat=lat,
#     lon=lon,
# 
#     # set data to query GEE specs
#     collection="ECMWF/ERA5_LAND",
#     bands="temperature_2m",
#     
#     # set temporal window
#     start_date=start_date,
#     end_date=end_date,
# 
#     # set cube dimensions
#     edge_size=edge_size,
#     units="m",
#     resolution=resolution,
# 
#     # set output specs
#     datatree=True,
#     dataset=True,
#     xy_coords="center",
#     gee = True # USE GEE instead of STAC <-- important
# )
