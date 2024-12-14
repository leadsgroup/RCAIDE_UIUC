# RCAIDE/Library/Methods/Aerodynamics/Athena_Vortex_Lattice/build_VLM_surrogates.py
#
# Created: Oct 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports 
from scipy.interpolate                                           import RegularGridInterpolator 

# ----------------------------------------------------------------------------------------------------------------------
#  build_AVL_surrogates
# ---------------------------------------------------------------------------------------------------------------------- 
def build_AVL_surrogates(aerodynamics):
    """Build a surrogate using sample evaluation results.
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        aerodynamics       : VLM analysis          [unitless] 
        
    Returns: 
        None  
    """
    surrogates  = aerodynamics.surrogates
    training    = aerodynamics.training  
    AoA_data    = training.angle_of_attack
    mach_data   = training.Mach
    

    CL_data       = training.coefficients[0,:,:]
    CDi_data      = training.coefficients[1,:,:]
    e_data        = training.coefficients[2,:,:]  
    CM_data       = training.coefficients[3,:,:]
    Cm_alpha_data = training.coefficients[4,:,:]
    Cn_beta_data  = training.coefficients[5,:,:]
    NP_data       = training.coefficients[6,:,:] 
   
    surrogates.lift_coefficient            = RegularGridInterpolator((AoA_data, mach_data), CL_data      ,method = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.drag_coefficient            = RegularGridInterpolator((AoA_data, mach_data), CDi_data     ,method = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.span_efficiency_factor      = RegularGridInterpolator((AoA_data, mach_data), e_data       ,method = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.moment_coefficient          = RegularGridInterpolator((AoA_data, mach_data), CM_data      ,method = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.Cm_alpha_moment_coefficient = RegularGridInterpolator((AoA_data, mach_data), Cm_alpha_data,method = 'linear',   bounds_error=False, fill_value=None)    
    surrogates.Cn_beta_moment_coefficient  = RegularGridInterpolator((AoA_data, mach_data), Cn_beta_data ,method = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.neutral_point               = RegularGridInterpolator((AoA_data, mach_data), NP_data      ,method = 'linear',   bounds_error=False, fill_value=None)     
        
    return 