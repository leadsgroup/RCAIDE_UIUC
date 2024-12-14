# RCAIDE/Methods/Aerodynamics/Airfoil_Panel_Method/chordwise_distribution
# 
# 
# Created:  May 2024, Niranjan Nanjappa

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports    
from RCAIDE.Framework.Core import Data 

# package imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# chordwise_distribution
# ---------------------------------------------------------------------------------------------------------------------- 
def chordwise_distribution(x,y,cp,al,npanel,cf,vt):
    """Compute chordwise distribution of lift and drag for
        an airfoil          

    Assumptions:
    None

    Source:
    Anderson, J. D. "Fundamentals of aerodynamics 6th ed". MCGRAW-HILL EDUCATION (2017)                                                                  
                                                                   
    Inputs:                                                     
    x       -  Vector of x coordinates of the surface nodes      
    y       -  Vector of y coordinates of the surface nodes       
    cp      -  Vector of coefficients of pressure at the nodes  
    al      -  Angle of attack in radians                             
    npanel  -  Number of panels on the airfoil
    cf      -  skin friction coeff over the surface of airfoil
    vt      -  tangential velocity at all nodes   
                                                                 
    Outputs:                                           
    fD      -  chordwise distribution of drag
    fL      -  chordwise distribution of lift    
     
   Properties Used:
    N/A

    """
    al       = al.T
    dx       = x[1:]-x[:-1]
    dy       = y[1:]-y[:-1]
    LE_ind   = int(npanel/2)
    dx_l     = -np.flip(dx[0:LE_ind], axis=0)
    dx_u     = dx[LE_ind:]
    dy_l     = -np.flip(dy[0:LE_ind], axis=0)
    dy_u     = dy[LE_ind:]
    
    cp_l     = np.flip(cp[0:LE_ind], axis=0)
    cp_u     = cp[LE_ind:]
    
    cf       = cf*(vt/np.abs(vt))
    cf_l     = -np.flip(cf[0:LE_ind], axis=0)
    cf_u     = cf[LE_ind:]
    
    dcn      = cp_l*dx_l - cp_u*dx_u + cf_u*dy_u - cf_l*dy_l
    dca      = cp_u*dy_u - cp_l*dy_l + cf_u*dx_u + cf_l*dx_l
    
    dcl      = dcn*np.cos(al) - dca*np.sin(al)
    dcd      = dcn*np.sin(al) + dca*np.cos(al)
    
    cl       = np.sum(dcl, axis=0)
    cd       = np.sum(dcd, axis=0)
    
    fL       = dcl/cl
    fD       = dcd/cd
    
    return fL,fD
    