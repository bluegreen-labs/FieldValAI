#!/usr/bin/env python

# load required libraries
import os, argparse, re
import cubo
import numpy as np
import ee
import xee
import xarray as xr
import datetime as dt

def bulk_density(lat, lon, edge_size, resolution, start_date, end_date):

    # Bulk Density Query
    ds = cubo.create(
        lat=lat,
        lon=lon,
        collection=["OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02"],
        bands=["b0", "b10", "b30"],
        start_date=start_date,
        end_date=end_date,
        edge_size=edge_size,
        units="m",
        resolution=resolution,
        #datatree=True,
        dataset=True,
        gee=True,
    )

    # rename variables for clarity
    ds = ds.rename_vars({
        "b0":"bulk_density_b0",
        "b10":"bulk_density_b10",
        "b30":"bulk_density_b30"
    })

    # list all coordinate values
    coords = list(ds.coords)
    coords.remove("time")
    coords.remove("x")
    coords.remove("y")

    # manipulate coordinates (for datatree??)
    ds = ds.reset_coords(names=coords, drop = True)

    # reassign unprojected coordinates
    ds = ds.assign_coords(
        coords={
            "x": list(range(0, ds.sizes['x'])),
            "y": sorted(list(range(0, ds.sizes['y'])), reverse = True)
            }
        )
    
    # manipulate atributes

    # drop everything
    ds = ds.drop_attrs()

    return ds

def carbon(lat, lon, edge_size, resolution, start_date, end_date):

    # Organic Carbon Query
    ds = cubo.create(
        lat=lat,
        lon=lon,
        collection=["OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02"],
        bands=["b0", "b10", "b30"],
        start_date=start_date,
        end_date=end_date,
        edge_size=edge_size,
        units="m",
        resolution=resolution,
        #datatree=True,
        dataset=True,
        gee=True,
    )

    # rename variables for clarity
    ds = ds.rename_vars({
        "b0":"carbon_b0",
        "b10":"carbon_b10",
        "b30":"carbon_b30"
    })

    # list all coordinate values
    coords = list(ds.coords)
    coords.remove("time")
    coords.remove("x")
    coords.remove("y")

    # manipulate coordinates (for datatree??)
    ds = ds.reset_coords(names=coords, drop = True)

    # reassign unprojected coordinates
    ds = ds.assign_coords(
        coords={
            "x": list(range(0, ds.sizes['x'])),
            "y": sorted(list(range(0, ds.sizes['y'])), reverse = True)
            }
        )
    
    # drop everything
    ds = ds.drop_attrs()

    return ds

def field_capacity(lat, lon, edge_size, resolution, start_date, end_date):

    # Water Content (Field Capacity) Query
    ds = cubo.create(
        lat=lat,
        lon=lon,
        collection=["OpenLandMap/SOL/SOL_WATERCONTENT-33KPA_USDA-4B1C_M/v01"],
        bands=["b0", "b10", "b30"],
        start_date=start_date,
        end_date=end_date,
        edge_size=edge_size,
        units="m",
        resolution=resolution,
        #datatree=True,
        dataset=True,
        gee=True,
    )

    # rename variables for clarity
    ds = ds.rename_vars({
        "b0":"field_capacity_b0",
        "b0":"field_capacity_b10",
        "b30":"field_capacity_b30"
    })

    # list all coordinate values
    coords = list(ds.coords)
    coords.remove("time")
    coords.remove("x")
    coords.remove("y")

    # manipulate coordinates (for datatree??)
    ds = ds.reset_coords(names=coords, drop = True)

    # reassign unprojected coordinates
    ds = ds.assign_coords(
        coords={
            "x": list(range(0, ds.sizes['x'])),
            "y": sorted(list(range(0, ds.sizes['y'])), reverse = True)
            }
        )
    # manipulate atributes

    # drop everything
    ds = ds.drop_attrs()

    return ds

def era5(lat, lon, edge_size, resolution, start_date, end_date):

    # climatology
    ds = cubo.create(
        # set query location
        lat = lat,
        lon = lon,

        # set data to query GEE specs
        collection = [
            "ECMWF/ERA5_LAND/DAILY_AGGR"
            ],
        bands = [
            "temperature_2m",
            "total_precipitation_sum",
            "surface_pressure",
            "dewpoint_temperature_2m"
            ],
        
        # set temporal window
        start_date = start_date,
        end_date = end_date,
    
        # set cube dimensions
        edge_size = edge_size,
        units = "m",
        resolution = resolution,
    
        # set output specs
        #datatree = True,
        dataset = True,

        # etc
        gee = True
    )

 # list all coordinate values
    coords = list(ds.coords)
    coords.remove("time")
    coords.remove("x")
    coords.remove("y")

    # manipulate coordinates (for datatree??)
    ds = ds.reset_coords(names=coords, drop = True)

    # reassign unprojected coordinates
    ds = ds.assign_coords(
        coords={
            "x": list(range(0, ds.sizes['x'])),
            "y": sorted(list(range(0, ds.sizes['y'])), reverse = True)
            }
        )
    
    # manipulate atributes

    # drop everything
    ds = ds.drop_attrs()

    return ds


def sentinel2(lat, lon, edge_size, resolution, start_date, end_date):

    ds = cubo.create(
        # set query location
        lat = lat,
        lon = lon,

        # set data to query GEE specs
        collection = [
            "COPERNICUS/S2_SR_HARMONIZED",
            "GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED",
            ],
        bands = {
            "COPERNICUS/S2_SR_HARMONIZED":["B2","B3","B4","B8"],
            "GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED":["cs_cdf"]
            },
        
        # set temporal window
        start_date = start_date,
        end_date = end_date,
    
        # set cube dimensions
        edge_size = edge_size,
        units = "m",
        resolution = resolution,
    
        # set output specs
        #datatree = True,
        dataset = True,

        # etc
        gee = True
    )

    #----- aggregate to daily time steps ----

    # screen for cloud cover
    ds = ds.where(ds.cs_cdf > 0.6, np.nan)

    # drop the cloud screening layer
    ds = ds.drop_vars("cs_cdf")

    # convert dates to isoformat dates (Y-m-d)
    # without time (assumes that dates are in UTC/GMT)
    # across datasets and services
    ds["time"] = ds["time"].dt.strftime("%Y-%m-%d")

    # get daily median (if multiple tiles are there)
    # skip na values to retain a maximum of good pixels
    ds = ds.groupby("time").median(skipna = True)

    #----- strip identifying information ----

    # list all coordinate values
    # only retain time and coordinates
    # (which are corrected below)
    coords = list(ds.coords)
    coords.remove("time")
    coords.remove("x")
    coords.remove("y")

    # manipulate coordinates (for datatree??)
    ds = ds.reset_coords(names=coords, drop = True)

    # drop everything
    ds = ds.drop_attrs()

    # reassign unprojected coordinates
    ds = ds.assign_coords(
        coords={
            "x": list(range(0, ds.sizes['x'])),
            "y": sorted(list(range(0, ds.sizes['y'])), reverse = True)
            }
        )

    # drop fully empty layers (due to cloud filtering)
    ds = ds.dropna(dim = "time", how = "all")

    return ds

def sentinel1(lat, lon, edge_size, resolution, start_date, end_date):

    ds = cubo.create(
        # set query location
        lat = lat,
        lon = lon,

        # collection and bands
        collection = ["sentinel-1-rtc"],

        bands = ["vv", "vh"],
        
        # set temporal window
        start_date = start_date,
        end_date = end_date,
    
        # set cube dimensions
        edge_size = edge_size,
        units = "m",
        resolution = resolution,
    
        # filter for descending images only
        # ascending components can have missing data
        query = {"sat:orbit_state": {"eq": "descending"}},

        # set output specs
        #datatree = True,
        dataset = True
    )

    #----- aggregate to daily time steps ----

    # convert dates to isoformat dates (Y-m-d)
    # without time (assumes that dates are in UTC/GMT)
    # across datasets and services
    ds["time"] = ds["time"].dt.strftime("%Y-%m-%d")

    # get daily median (if multiple tiles are there)
    # skip na values to retain a maximum of good pixels
    ds = ds.groupby("time").mean(skipna = True)

    #----- strip identifying information ----

    # list all coordinate values
    # only retain time and coordinates
    # (which are corrected below)
    coords = list(ds.coords)
    coords.remove("time")
    coords.remove("x")
    coords.remove("y")

    # manipulate coordinates (for datatree??)
    ds = ds.reset_coords(names=coords, drop = True)

    # drop everything
    ds = ds.drop_attrs()

    # reassign unprojected coordinates
    ds = ds.assign_coords(
        coords={
            "x": list(range(0, ds.sizes['x'])),
            "y": sorted(list(range(0, ds.sizes['y'])), reverse = True)
            }
        )
    return ds


def dem(lat, lon, edge_size, resolution, start_date, end_date):

    ds = cubo.create(
        # set query location
        lat = lat,
        lon = lon,

        # set data to query GEE specs
        collection = [
            "cop-dem-glo-30"
            ],
        bands = {
            "cop-dem-glo-30":["data"]
            },
        
        # set temporal window
        start_date = "2021-04-22",
        end_date = "2021-04-22",
    
        # set cube dimensions
        edge_size = edge_size,
        units = "m",
        resolution = resolution,
    
        # set output specs
        #datatree = True,
        dataset = True
    )

    #----- strip identifying information ----

    # list all coordinate values
    # only retain time and coordinates
    # (which are corrected below)
    coords = list(ds.coords)
    coords.remove("time")
    coords.remove("x")
    coords.remove("y")

    # manipulate coordinates (for datatree??)
    ds = ds.reset_coords(names=coords, drop = True)

    # drop everything
    ds = ds.drop_attrs()

    # reassign unprojected coordinates
    ds = ds.assign_coords(
        coords={
            "x": list(range(0, ds.sizes['x'])),
            "y": sorted(list(range(0, ds.sizes['y'])), reverse = True)
            }
        )
    
    return ds

def data_cube(lat, lon, edge_size, resolution, start_date, end_date):

    # download all DataSets
    dem_ds = dem(lat, lon, edge_size, resolution, start_date, end_date)
    s2_ds = sentinel2(lat, lon, edge_size, resolution, start_date, end_date)
    s1_ds = sentinel1(lat, lon, edge_size, resolution, start_date, end_date)
    era5_ds = era5(lat, lon, edge_size, resolution, start_date, end_date)
    bd_ds = bulk_density(lat, lon, edge_size, resolution, start_date, end_date)
    c_ds = carbon(lat, lon, edge_size, resolution, start_date, end_date)
    fc_ds = field_capacity(lat, lon, edge_size, resolution, start_date, end_date)

    # data list to process
    cubes = {
        "s1": s1_ds,
        "s2": s2_ds,
        "era5": era5_ds,
        "dem": dem_ds,
        "bd": bd_ds,
        "c": c_ds,
        "fc": fc_ds
        }

    # create empty data tree
    root = xr.Dataset(
        coords={
            "y": cubes["dem"].y.values,
            "x": cubes["dem"].x.values,
        }
    )
    nodes = {"/": root}

    # fill nodes with the datasets
    for key, value in cubes.items():
        nodes[key] = value

    return xr.DataTree.from_dict(nodes)

def getArgs():

    # setup parser
    parser = argparse.ArgumentParser(

    description = '''Parse data cubes for geographic locations''',
    epilog = '''post bug reports to the github repository''')

    parser.add_argument('-lat',
                        '--latitude',
                        help = 'Location latitude',
                        required = True,
                        type = float
                        )

    parser.add_argument('-lon',
                        '--longitude',
                        help = 'Location longitude',
                        required = True,
                        type = float
                        )
                        
    parser.add_argument('-es',
                        '--edge_size',
                        help = 'edge size in meters',
                        default = 640,
                        required = True,
                        type=int
                        )

    parser.add_argument('-res',
                        '--resolution',
                        help = 'output resolution in meter',
                        default = 10,
                        required = True,
                        type = int
                        )

    parser.add_argument('-sd',
                        '--start_date',
                        help = 'Start date of the period desired',
                        required = True
                        )
    
    parser.add_argument('-ed',
                        '--end_date',
                        help = 'End date of the period desired',
                        required = True
                        )

    parser.add_argument('-p',
                        '--project',
                        help = 'GEE project ID',
                        required = True
                        )

    parser.add_argument('-o',
                        '--output_file',
                        help = 'file path where to save the data as a netCDF file',
                        required = True
                        )
                                        
    parser.add_argument('-v',
                        '--verbose',
                        help = '''verbose debugging''',
                        default = False
                    )

    # put arguments in dictionary with
    # keys being the argument names given above
    return parser.parse_args()


if __name__ == "__main__":

    # parse arguments
    args = getArgs()

    # initialize GEE session
    # requires a valid authentication token
    # to be present on the system
    ee.Initialize(
        project = args.project,
        opt_url = 'https://earthengine-highvolume.googleapis.com' # required for data export
    )

    # download data using the gee_subset routine
    # print to console if verbose
    try:
        tree = data_cube(
            args.latitude,
            args.longitude,
            args.edge_size,
            args.resolution,
            args.start_date,
            args.end_date
            )
    except Exception as e:
        print("Error:", e)
    else: 
        tree.to_netcdf(args.output_file)