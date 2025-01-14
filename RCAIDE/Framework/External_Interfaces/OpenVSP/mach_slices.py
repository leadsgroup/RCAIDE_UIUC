# RCAIDE/Framework/External_Interfaces/OpenVSP/mach_slices.py
# Created:  May 2021, E. Botero 
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports 
from . import export_vsp_vehicle

try:
    import vsp as vsp
except ImportError:
    try:
        import openvsp as vsp
    except ImportError:
        # This allows RCAIDE to build without OpenVSP
        pass
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Mach Slices
# ---------------------------------------------------------------------------------------------------------------------- 
def mach_slices(vehicle, mach, angle_of_attack=[0.], number_slices=99):
    """
    Calculates volume equivalent area for sonic boom analysis using OpenVSP

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle
        Vehicle to analyze
    mach : array_like
        Mach numbers to evaluate
    angle_of_attack : array_like, optional
        Angles of attack in radians
        Default: [0.]
    number_slices : int, optional
        Number of slices to use in calculation
        Default: 99

    Returns
    -------
    X_locs_all : list of ndarray
        X-axis locations [m] for each Mach number where areas are computed
    slice_areas_all : list of ndarray
        Cross-sectional areas [m^2] at each X location for each Mach number

    Notes
    -----
    This function computes equivalent areas for sonic boom analysis by:
    1. Writing vehicle to OpenVSP
    2. Calculating Mach angle and adjusting for angle of attack
    3. Slicing geometry along Mach planes
    4. Computing areas normal to freestream

    **Major Assumptions**
    * Vehicle geometry is suitable for sonic boom analysis
    * Mach angles and areas are computed in the X-Z plane
    * Areas are projected normal to the freestream direction

    **Extra modules required**
    * OpenVSP (vsp or openvsp module)
    """       
    

    # Write the vehicle
    export_vsp_vehicle(vehicle,vehicle.tag,write_file=False)
    
    X_locs_all       = []
    slice_areas_all = []
    
    for ii in range(len(mach)):
        
        m   = mach[ii] 
        
        if len(angle_of_attack)>1:
            aoa = angle_of_attack[ii]
        else:
            aoa = angle_of_attack[0]
        
    
        # Calculate the mach angle and adjust for AoA
        mach_angle = np.arcsin(1/m)
        roty = (np.pi/2-mach_angle) + aoa
        
        # Take the components of the X and Z axis to get the slicing plane
        x_component = np.cos(roty)
        z_component = np.sin(roty)
        
        # Now slice it 
        vsp.ComputePlaneSlice( 0, number_slices, vsp.vec3d(x_component[0], 0.0, z_component[0]), True)
        
        # Pull out the areas from the slices
        pslice_results = vsp.FindLatestResultsID("Slice")
        slice_areas    = vsp.GetDoubleResults( pslice_results, "Slice_Area" ) * np.cos(roty)
        vec3d          = vsp.GetVec3dResults(pslice_results, "Slice_Area_Center")
        
        X = []
        Z = []
        
        for v in vec3d:
            X.append(v.x())
            Z.append(v.z())
        
        X = np.array(X)
        Z = np.array(Z)
            
        X_locs = X + Z*np.tan(mach_angle)
        
        if slice_areas[-1]==0.:
            slice_areas = slice_areas[0:-1]
            X_locs      = X_locs[:-1]
            
        # Turn them into arrays
        X_locs      = np.array(X_locs)
        slice_areas = np.array(slice_areas)
        
        # A vectorized Output
        X_locs_all.append(X_locs)
        slice_areas_all.append(slice_areas)

    return X_locs_all, slice_areas_all