# RCAIDE/Methods/Aerodynamics/Airfoil_Panel_Method/cf_filter.py
# 
# 
# Created:  Jun 2024, Niranjan Nanjappa 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    

# RCAIDE imports  
from RCAIDE.Framework.Core import Data

# package imports  
import numpy as np 
from scipy.signal import lfilter 

# ----------------------------------------------------------------------------------------------------------------------
# cf_filter.py
# ---------------------------------------------------------------------------------------------------------------------- 
def cf_filter(ncpts,ncases,npanel,CF):
    n = npanel
    
    #filter strength
    m = 30
    
    b = [1.0/m]*m
    a = 1
    CF_new = CF
    
    # number of points to be excluded from the filter
    n_f = n/10
    n_r = n/20
    
    for i in range(ncpts):
        for j in range(ncases):
                CF_new[int(n_r):int((n/2)-(n_f)),j,i] = lfilter(b, a, CF[int(n_r):int((n/2)-(n_f)),j,i])
                CF_new[int((n/2)+(n_f)):int(n-(n_r)),j,i] = lfilter(b, a, CF[int((n/2)+(n_f)):int(n-(n_r)),j,i])
    
    return CF_new
                
                # # case 1
                # if CF[k,j,i]>10*CF[k-1,j,i] and CF[k,j,i]>10*CF[k+1,j,i]:
                #     CF[k,j,i] = (CF[k+1,j,i] + CF[k-1,j,i])/2
                
                # # case 2
                # if CF[k,j,i]<0.1*CF[k-1,j,i] and CF[k,j,i]<0.1*CF[k+1,j,i]:
                #     CF[k,j,i] = (CF[k+1,j,i] + CF[k-1,j,i])/2
                    
                # # # case 3
                # # if CF[k,j,i]>10*CF[k-1,j,i] or CF[k,j,i]<0.1*CF[k-1,j,i]:
                # #     CF[k,j,i] = 
            
            # for k in range(int((npanel/2)+(npanel/20)),int(npanel-(npanel/20))):
            #     # # case 1
            #     # if CF[k,j,i]>10*CF[k-1,j,i] and CF[k,j,i]>10*CF[k+1,j,i]:
            #     #     CF[k,j,i] = (CF[k+1,j,i] + CF[k-1,j,i])/2
                
            #     # # case 2
            #     # if CF[k,j,i]<0.1*CF[k-1,j,i] and CF[k,j,i]<0.1*CF[k+1,j,i]:
            #     #     CF[k,j,i] = (CF[k+1,j,i] + CF[k-1,j,i])/2