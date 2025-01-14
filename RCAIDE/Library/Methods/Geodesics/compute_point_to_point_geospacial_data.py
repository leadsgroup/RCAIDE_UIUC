# RCAIDE/Library/Methods/Geodesics/compute_point_to_point_geospacial_data.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
import RCAIDE
from RCAIDE.Framework.Core import Units 
from scipy.interpolate import griddata
import numpy as np

# ----------------------------------------------------------------------
#  Compute Point to Point Geospacial Data
# --------------------------------------------------------------------- 
def compute_point_to_point_geospacial_data(settings):
    """
    Computes absolute locations between microphones/observers on a defined topography and calculates 
    geospacial relationships between origin and destination points.

    Parameters
    ----------
    settings : Data
        Configuration object containing:
            - topography_file : str
                Path to file containing latitude, longitude, and elevation data
            - aircraft_origin_coordinates : array_like
                [latitude, longitude] of starting point in degrees
            - aircraft_destination_coordinates : array_like
                [latitude, longitude] of ending point in degrees

    Returns
    -------
    None

    Notes
    -----
    This function transforms geographic coordinates into a local cartesian system 
    while preserving elevation data from the topography. It handles coordinate 
    transformations and elevation interpolation. It uses geograpic coordinates 
    and elevation data from the topography file obtained from https://topex.ucsd.edu/cgi-bin/get_data.cgi. 

    Data is returned in the following format:   
        - aircraft_origin_location : [x, y, z]
        - aircraft_destination_location : [x, y, z]

    **Major Assumptions**
        * Topography file follows ASCII XYZ-format
        * Coordinates are in decimal degrees
        * Elevation data is in meters
        * Linear interpolation of elevation data

    See Also
    --------
    RCAIDE.Library.Methods.Geodesics.Geodesics.Calculate_Distance : Function used for distance calculations
    """
    # convert cooordinates to array 
    origin_coordinates   = np.asarray(settings.aircraft_origin_coordinates)
    destination_coordinates = np.asarray(settings.aircraft_destination_coordinates)
    
    # extract data from file 
    data  = np.loadtxt(settings.topography_file)
    Long  = data[:,0]
    Lat   = data[:,1]
    Elev  = data[:,2] 

    x_min_coord = np.min(Lat)
    y_min_coord = np.min(Long)
    dep_lat     = origin_coordinates[0]
    dep_long    = origin_coordinates[1]
    des_lat     = destination_coordinates[0]
    des_long    = destination_coordinates[1]
    if dep_long < 0: 
        dep_long = 360 + dep_long
    if des_long< 0:
        des_long =360 +  des_long 
    
    bottom_left_map_coords   = np.array([x_min_coord,y_min_coord])  
    x0_coord                 = np.array([dep_lat,y_min_coord])
    y0_coord                 = np.array([x_min_coord,dep_long])
    x1_coord                 = np.array([des_lat,y_min_coord])
    y1_coord                 = np.array([x_min_coord,des_long])  
    
    x0 = RCAIDE.Framework.Analyses.Geodesics.Geodesics.Calculate_Distance(x0_coord,bottom_left_map_coords) * Units.kilometers
    y0 = RCAIDE.Framework.Analyses.Geodesics.Geodesics.Calculate_Distance(y0_coord,bottom_left_map_coords) * Units.kilometers
    x1 = RCAIDE.Framework.Analyses.Geodesics.Geodesics.Calculate_Distance(x1_coord,bottom_left_map_coords) * Units.kilometers
    y1 = RCAIDE.Framework.Analyses.Geodesics.Geodesics.Calculate_Distance(y1_coord,bottom_left_map_coords) * Units.kilometers
    
    lat_flag             = np.where(origin_coordinates<0)[0]
    origin_coordinates[lat_flag]  = origin_coordinates[lat_flag] + 360 
    long_flag            = np.where(destination_coordinates<0)[0]
    destination_coordinates[long_flag] = destination_coordinates[long_flag] + 360 
    z0                   = griddata((Lat,Long), Elev, (np.array([origin_coordinates[0]]),np.array([origin_coordinates[1]])), method='nearest')[0]
    z1                   = griddata((Lat,Long), Elev, (np.array([destination_coordinates[0]]),np.array([destination_coordinates[1]])), method='nearest')[0] 
    dep_loc              = np.array([x0,y0,z0])
    des_loc              = np.array([x1,y1,z1])
    
    # pack data 
    settings.aircraft_origin_location      = dep_loc
    settings.aircraft_destination_location = des_loc 
        
    return 
