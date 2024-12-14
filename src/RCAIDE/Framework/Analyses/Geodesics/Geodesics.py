# RCAIDE/Framework/Analyses/Geodesics/Geodesics.py
# 
# Created:  Oct. 2024, A. Molloy 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports
from  RCAIDE.Library.Methods.Geodesics.Geodesics import Geodesic_Calculate

# ----------------------------------------------------------------------------------------------------------------------
#  Calculate Distance between two coordinate locations
# ----------------------------------------------------------------------------------------------------------------------  
def Calculate_Distance(coord1, coord2):
    """This passes the coordinates to the distance calculation method and then returns the results in kilometers
    
       Inputs:
       - Coordinates (lat, long)
       
       Outputs:
       - Distance in kilometers between the two coordinates.
       
       Assumptions:
       None

       Source:
       None 
            """    
    distance = Geodesic_Calculate(coord1, coord2).kilometers
    return(distance)