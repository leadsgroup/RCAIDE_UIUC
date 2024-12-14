# RCAIDE/Library/Missions/Common/compute_point_to_point_geospacial_data.py
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
    """This computes the absolute microphone/observer locations on a defined topography
            
    Assumptions: 
        topography_file is a text file obtained from https://topex.ucsd.edu/cgi-bin/get_data.cgi
    
    Source:
        N/A  

    Inputs:   
        topography_file                        - file of lattide, longitude and elevation points     
        origin_coordinates                     - coordinates of origin location                                              [degrees]
        destination_coordinates                - coordinates of destimation location                                            [degrees]  
        
    Outputs:                                   
        latitude_longitude_micrphone_locations - latitude-longitude and elevation coordinates of all microphones in domain      [deg,deg,m]  
        flight_range                           - gound distance between origin and destination location                      [meters]              
        true_course                            - true course angle measured clockwise from true north                     [radians]                      
        origin_location                        - cartesial coordinates of origin location relative to computational domain   [meters]                   
        destination_xyz_location               - cartesial coordinates of destination location relative to computational domain [meters]    
    
    Properties Used:
        N/A       
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
