## @ingroup Analyses-Aerodynamics
# RCAIDE/Framework/Analyses/Aerodynamics/Vortex_Lattice.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                                     import Data 
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method import VLM 
from RCAIDE.Library.Methods.Utilities                          import Cubic_Spline_Blender  

# package imports
import numpy as np 
from scipy.interpolate import RectBivariateSpline, RegularGridInterpolator

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Aerodynamics 
def evaluate_surrogate(state,settings,geometry):
    """Evaluates lift and drag using available surrogates.

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    state.conditions.
      freestream.dynamics_pressure       [-]
      angle_of_attack                    [radians]

    Outputs:
    conditions.aerodynamics.lift_breakdown.
      inviscid_wings[wings.*.tag]             [-] CL (wing specific)
      inviscid_wings_lift.total               [-] CL
      compressible_wing                       [-] CL (wing specific)
    conditions.aerodynamics.coefficients.lift  [-] CL
    conditions.aerodynamics.drag_breakdown.induced.
      total                                   [-] CDi 
      inviscid                                [-] CDi 
      wings_sectional_drag                    [-] CDiy (wing specific)
      inviscid_wings                          [-] CDi (wing specific)
      
    Properties Used:
    aero.surrogates.
      lift_coefficient                        [-] CL
      wing_lift_coefficient[wings.*.tag]      [-] CL (wing specific)
    """          
    
    # unpack
    aero        = state.analyses.aerodynamics
    conditions  = state.conditions
    settings    = aero.settings
    geometry    = aero.geometry
    surrogates  = aero.surrogates
    hsub_min    = aero.hsub_min
    hsub_max    = aero.hsub_max
    hsup_min    = aero.hsup_min
    hsup_max    = aero.hsup_max 

    AoA         = conditions.aerodynamics.angles.alpha.T[0]
    Mach        = conditions.freestream.mach_number.T[0]
    
    
    # Unapck the surrogates
    CL_surrogate_sub          = surrogates.lift_coefficient_sub  
    CL_surrogate_sup          = surrogates.lift_coefficient_sup  
    CL_surrogate_trans        = surrogates.lift_coefficient_trans
    CDi_surrogate_sub         = surrogates.drag_coefficient_sub  
    CDi_surrogate_sup         = surrogates.drag_coefficient_sup  
    CDi_surrogate_trans       = surrogates.drag_coefficient_trans
    wing_CL_surrogates_sub    = surrogates.wing_lift_coefficient_sub  
    wing_CL_surrogates_sup    = surrogates.wing_lift_coefficient_sup  
    wing_CL_surrogates_trans  = surrogates.wing_lift_coefficient_trans
    wing_CDi_surrogates_sub   = surrogates.wing_drag_coefficient_sub  
    wing_CDi_surrogates_sup   = surrogates.wing_drag_coefficient_sup  
    wing_CDi_surrogates_trans = surrogates.wing_drag_coefficient_trans
    
    # Create Result Data Structures         
    data_len                                                           = len(AoA)
    inviscid_lift                                                      = np.zeros([data_len,1]) 
    inviscid_drag                                                      = np.zeros([data_len,1])  
    conditions.aerodynamics.drag_breakdown.induced                     = Data()
    conditions.aerodynamics.drag_breakdown.induced.inviscid_wings      = Data()
    conditions.aerodynamics.lift_breakdown                             = Data()
    conditions.aerodynamics.lift_breakdown.inviscid_wings              = Data()
    conditions.aerodynamics.lift_breakdown.compressible_wings          = Data()
    conditions.aerodynamics.drag_breakdown.compressible                = Data() 
    
    # 3 Cases for surrogates, subsonic only, supersonic only, and both
    if CL_surrogate_sup == None:
        inviscid_lift = CL_surrogate_sub(AoA,Mach,grid=False)
        inviscid_drag = CDi_surrogate_sub(AoA,Mach,grid=False)
    elif CL_surrogate_sub == None:
        inviscid_lift = CL_surrogate_sup(AoA,Mach,grid=False)
        inviscid_drag = CDi_surrogate_sup(AoA,Mach,grid=False)     
    else:
        # Spline for Subsonic-to-Transonic-to-Supersonic Regimes
        sub_trans_spline = Cubic_Spline_Blender(hsub_min,hsub_max)
        h_sub            = lambda M:sub_trans_spline.compute(M)          
        sup_trans_spline = Cubic_Spline_Blender(hsup_min,hsup_max) 
        h_sup            = lambda M:sup_trans_spline.compute(M)          
    
        inviscid_lift = h_sub(Mach)*CL_surrogate_sub(AoA,Mach,grid=False)    +\
                          (h_sup(Mach) - h_sub(Mach))*CL_surrogate_trans((AoA,Mach))+ \
                          (1- h_sup(Mach))*CL_surrogate_sup(AoA,Mach,grid=False)

        inviscid_drag = h_sub(Mach)*CDi_surrogate_sub(AoA,Mach,grid=False)   +\
                          (h_sup(Mach) - h_sub(Mach))*CDi_surrogate_trans((AoA,Mach))+ \
                          (1- h_sup(Mach))*CDi_surrogate_sup(AoA,Mach,grid=False)

    # Pack
    conditions.aerodynamics.coefficients.lift                = np.atleast_2d(inviscid_lift).T
    conditions.aerodynamics.lift_breakdown.total            = np.atleast_2d(inviscid_lift).T
    conditions.aerodynamics.drag_breakdown.induced.inviscid = np.atleast_2d(inviscid_drag).T
    
    for wing in geometry.wings.keys(): 
        
        if CL_surrogate_sup == None:
            inviscid_wing_lifts = wing_CL_surrogates_sub[wing](AoA,Mach,grid=False)
            inviscid_wing_drags = wing_CDi_surrogates_sub[wing](AoA,Mach,grid=False)            
            
        elif CL_surrogate_sub == None:
            inviscid_wing_lifts = wing_CL_surrogates_sup[wing](AoA,Mach,grid=False)
            inviscid_wing_drags = wing_CDi_surrogates_sup[wing](AoA,Mach,grid=False)                
        
        else:
            inviscid_wing_lifts = h_sub(Mach)*wing_CL_surrogates_sub[wing](AoA,Mach,grid=False)    + \
                                    (h_sup(Mach) - h_sub(Mach))*wing_CL_surrogates_trans[wing]((AoA,Mach))+ \
                                    (1- h_sup(Mach))*wing_CL_surrogates_sup[wing](AoA,Mach,grid=False)
            
            inviscid_wing_drags = h_sub(Mach)*wing_CDi_surrogates_sub[wing](AoA,Mach,grid=False)  + \
                                    (h_sup(Mach) - h_sub(Mach))*wing_CDi_surrogates_trans[wing]((AoA,Mach))+ \
                                    (1- h_sup(Mach))*wing_CDi_surrogates_sup[wing](AoA,Mach,grid=False)
         
        # Pack 
        conditions.aerodynamics.lift_breakdown.inviscid_wings[wing]         = np.atleast_2d(inviscid_wing_lifts).T
        conditions.aerodynamics.lift_breakdown.compressible_wings[wing]     = np.atleast_2d(inviscid_wing_lifts).T
        conditions.aerodynamics.drag_breakdown.induced.inviscid_wings[wing] = np.atleast_2d(inviscid_wing_drags).T
     
    return     

def evaluate_no_surrogate(state,settings,geometry):
    """Evaluates lift and drag directly using VLM
    
    Assumptions:
    no changes to initial geometry or settings
    
    Source:
    N/A
    
    Inputs:
    state.conditions.
      angle_of_attack                         [radians]
      
    Outputs:
    conditions.aerodynamics.lift_breakdown.
      inviscid_wings_lift[wings.*.tag]        [-] CL (wing specific)
      inviscid_wings_lift.total               [-] CL
      inviscid_wings_sectional                [-] Cly  
      compressible_wing                       [-] CL (wing specific)
    conditions.aerodynamics.drag_breakdown.induced.
      total                                   [-] CDi 
      inviscid                                [-] CDi 
      wings_sectional_drag                    [-] CDiy (wing specific)
      induced.inviscid_wings                  [-] CDi  (wing specific)        

    conditions.aerodynamics.
      pressure_coefficient                    [-] CP
     
    Properties Used:
    aero.surrogates.
      lift_coefficient                        [-] CL
      wing_lift_coefficient[wings.*.tag]      [-] CL (wing specific)
    """          
    
    # unpack        
    aero       = state.analyses.aerodynamics
    conditions = state.conditions
    settings   = aero.settings
    geometry   = aero.geometry     
    
    # Evaluate the VLM
    # if in transonic regime, use surrogate
    inviscid_lift, inviscid_drag, inviscid_side, wing_lifts, wing_drags, wing_lift_distribution, \
    wing_drag_distribution, induced_angle_distribution, pressure_coefficient, CYMTOT,CRMTOT,CM = \
        calculate_VLM(conditions,settings,geometry)
    
    # Lift 
    conditions.aerodynamics.coefficients.lift                        = inviscid_lift  
    conditions.aerodynamics.lift_breakdown.total                    = inviscid_lift        
    conditions.aerodynamics.lift_breakdown.compressible_wings       = wing_lifts
    conditions.aerodynamics.lift_breakdown.inviscid_wings           = wing_lifts
    conditions.aerodynamics.lift_breakdown.inviscid_wings_sectional = wing_lift_distribution
    
    # Drag        
    conditions.aerodynamics.drag_breakdown.induced                 = Data()
    conditions.aerodynamics.drag_breakdown.induced.total           = inviscid_drag     
    conditions.aerodynamics.drag_breakdown.induced.inviscid        = inviscid_drag     
    conditions.aerodynamics.drag_breakdown.induced.inviscid_wings  = wing_drags
    conditions.aerodynamics.drag_breakdown.induced.wings_sectional = wing_drag_distribution 
    conditions.aerodynamics.drag_breakdown.induced.angle           = induced_angle_distribution
    
    #Side
    conditions.aerodynamics.side_force_coefficient                 = inviscid_side
    
    # Pressure and moment coefficients
    conditions.aerodynamics.pressure_coefficient = pressure_coefficient
    conditions.aerodynamics.moment_coefficient   = CM
    
    # Stability
    conditions.static_stability.yawing_moment_coefficient = CYMTOT
    conditions.static_stability.rolling_moment_coefficient = CRMTOT
    
    return  


def sample_training(aero):
    """Call methods to run vortex lattice for sample point evaluation.

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    see properties used

    Outputs:
    aero.training.
      lift_coefficient            [-] 
      wing_lift_coefficient       [-] (wing specific)
      drag_coefficient            [-]          

      wing_drag_coefficient       [-] (wing specific)

    Properties Used:
    aero.geometry.wings.*.tag
    aero.settings                 (passed to calculate vortex lattice)
    aero.training.angle_of_attack [radians]
    """
    # unpack
    geometry      = aero.geometry
    settings      = aero.settings
    training      = aero.training
    AoA           = training.angle_of_attack 
    Mach          = training.Mach
    lenAoA        = len(AoA)
    sub_len       = int(sum(Mach<1.))
    sup_len       = len(Mach)-sub_len
    
    # Assign placeholders        
    CL_sub    = np.zeros((lenAoA,sub_len))
    CL_sup    = np.zeros((lenAoA,sup_len))
    CDi_sub   = np.zeros((lenAoA,sub_len))
    CDi_sup   = np.zeros((lenAoA,sup_len))
    CL_w_sub  = Data()
    CL_w_sup  = Data()
    CDi_w_sub = Data()
    CDi_w_sup = Data() 
        
    # Setup new array shapes for vectorization
    lenM   = len(Mach)
    AoAs   = np.atleast_2d(np.tile(AoA,lenM).T.flatten()).T
    Machs  = np.atleast_2d(np.tile(Mach,lenAoA).flatten()).T
    zeros  = np.zeros_like(Machs)
    
    # Setup Konditions    
    cons                              = RCAIDE.Framework.Mission.Common.Results()
    cons.aerodynamics.angles.alpha    = AoAs
    cons.freestream.mach_number       = Machs
    cons.freestream.velocity          = zeros
    
    total_lift, total_drag, total_side, wing_lifts, wing_drags, _, _, _, _, _, _, _ = calculate_VLM(cons,settings,geometry)     

    # Split subsonic from supersonic
    if np.sum(Machs<1.)==0:
        sub_sup_split = 0
    else:
        sub_sup_split = np.where(Machs < 1.0)[0][-1] + 1 
    len_sub_mach  = np.sum(Mach<1.)
    len_sup_mach  = lenM - len_sub_mach
    
    # Divide up the data to get ready to store
    CL_sub  = total_lift[0:sub_sup_split,0]
    CL_sup  = total_lift[sub_sup_split:,0]
    CDi_sub = total_drag[0:sub_sup_split,0]
    CDi_sup = total_drag[sub_sup_split:,0]
    
    # A little reshape to get into the right order
    CL_sub  = np.reshape(CL_sub,(len_sub_mach,lenAoA)).T
    CL_sup  = np.reshape(CL_sup,(len_sup_mach,lenAoA)).T
    CDi_sub = np.reshape(CDi_sub,(len_sub_mach,lenAoA)).T
    CDi_sup = np.reshape(CDi_sup,(len_sup_mach,lenAoA)).T
    
    # Now do the same for each wing
    for wing in geometry.wings.keys():
        
        # Slice out the sub and supersonic
        CL_wing_sub  = wing_lifts[wing][0:sub_sup_split,0]
        CL_wing_sup  = wing_lifts[wing][sub_sup_split:,0]
        CDi_wing_sub = wing_drags[wing][0:sub_sup_split,0]  
        CDi_wing_sup = wing_drags[wing][sub_sup_split:,0]  
        
        # Rearrange and pack
        CL_w_sub[wing]  = np.reshape(CL_wing_sub,(len_sub_mach,lenAoA)).T
        CL_w_sup[wing]  = np.reshape(CL_wing_sup,(len_sup_mach,lenAoA)).T
        CDi_w_sub[wing] = np.reshape(CDi_wing_sub,(len_sub_mach,lenAoA)).T   
        CDi_w_sup[wing] = np.reshape(CDi_wing_sup,(len_sup_mach,lenAoA)).T   
    
    # surrogate not run on sectional coefficients and pressure coefficients
    # Store training data 
    training.lift_coefficient_sub         = CL_sub
    training.lift_coefficient_sup         = CL_sup
    training.wing_lift_coefficient_sub    = CL_w_sub        
    training.wing_lift_coefficient_sup    = CL_w_sup
    training.drag_coefficient_sub         = CDi_sub
    training.drag_coefficient_sup         = CDi_sup
    training.wing_drag_coefficient_sub    = CDi_w_sub        
    training.wing_drag_coefficient_sup    = CDi_w_sup
    
    return
    
def build_surrogate(aero):
    """Build a surrogate using sample evaluation results.

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    see properties used

    Outputs:
    aero.surrogates.
      lift_coefficient            
      wing_lift_coefficient       
      drag_coefficient            
      wing_drag_coefficient

    Properties Used:
    aero.training.
      lift_coefficient            [-] 
      wing_lift_coefficient       [-] (wing specific)
      drag_coefficient            [-] 
      wing_drag_coefficient       [-] (wing specific)
    """           

    # unpack data
    surrogates     = aero.surrogates
    training       = aero.training
    geometry       = aero.geometry
    Mach           = training.Mach
    AoA_data       = training.angle_of_attack[:,0]
    if np.sum(Mach<1.)==0:
        sub_sup_split = 0
    else:
        sub_sup_split = np.where(Mach < 1.0)[0][-1] + 1 
    mach_data_sub  = training.Mach[0:sub_sup_split,0]
    mach_data_sup  = training.Mach[sub_sup_split:,0]
    CL_data_sub    = training.lift_coefficient_sub   
    CL_data_sup    = training.lift_coefficient_sup
    CDi_data_sub   = training.drag_coefficient_sub         
    CDi_data_sup   = training.drag_coefficient_sup 
    CL_w_data_sub  = training.wing_lift_coefficient_sub
    CL_w_data_sup  = training.wing_lift_coefficient_sup     
    CDi_w_data_sub = training.wing_drag_coefficient_sub         
    CDi_w_data_sup = training.wing_drag_coefficient_sup
    
    # Instantiate surrogates as none for now
    CL_surrogate_sub        = None
    CL_surrogate_sup        = None
    CL_surrogate_trans      = None
    CL_w_surrogates_sub     = None
    CL_w_surrogates_sup     = None
    CL_w_surrogates_trans   = None
    CDi_surrogate_sub       = None
    CDi_surrogate_sup       = None
    CDi_surrogate_trans     = None
    CDi_w_surrogates_sub    = None
    CDi_w_surrogates_sup    = None
    CDi_w_surrogates_trans  = None
    

    # Check for 3 different cases, pure subsonic, pure supersonic, both
    SUB = np.shape(CL_data_sub)[1]>0
    SUP = np.shape(CL_data_sup)[1]>0

    # Do the subsonic surrogates:
    if SUB:
        CL_surrogate_sub  = RectBivariateSpline(AoA_data, mach_data_sub, CL_data_sub)
        CDi_surrogate_sub = RectBivariateSpline(AoA_data, mach_data_sub, CDi_data_sub)  
    
    # Do the supersonic surrogates:
    if SUP:
        CL_surrogate_sup  = RectBivariateSpline(AoA_data, mach_data_sup, CL_data_sup) 
        CDi_surrogate_sup = RectBivariateSpline(AoA_data, mach_data_sup, CDi_data_sup)    
            
    # Do the transonic regime surrogates:
    if SUB and SUP:	                             
        CL_data_trans        = np.zeros((len(AoA_data),3))	      
        CDi_data_trans       = np.zeros((len(AoA_data),3))	 	      
        CL_w_data_trans      = Data()	                     
        CDi_w_data_trans     = Data()    
        CL_data_trans[:,0]   = CL_data_sub[:,-1]    	     
        CL_data_trans[:,1]   = CL_data_sup[:,0] 
        CL_data_trans[:,2]   = CL_data_sup[:,1] 
        CDi_data_trans[:,0]  = CDi_data_sub[:,-1]	     
        CDi_data_trans[:,1]  = CDi_data_sup[:,0] 

        mach_data_trans_CL   = np.array([mach_data_sub[-1],mach_data_sup[0],mach_data_sup[1]]) 
        mach_data_trans_CDi  = np.array([mach_data_sub[-1],mach_data_sup[0],mach_data_sup[1]]) 

        CL_surrogate_trans  = RegularGridInterpolator((AoA_data, mach_data_trans_CL), CL_data_trans, \
                                                                 method = 'linear', bounds_error=False, fill_value=None)  
        CDi_surrogate_trans = RegularGridInterpolator((AoA_data, mach_data_trans_CDi), CDi_data_trans, \
                                                                 method = 'linear', bounds_error=False, fill_value=None)  

    CL_w_surrogates_sub            = Data() 
    CL_w_surrogates_sup            = Data() 
    CL_w_surrogates_trans          = Data() 
    CDi_w_surrogates_sub           = Data()             
    CDi_w_surrogates_sup           = Data() 
    CDi_w_surrogates_trans         = Data()
    
    for wing in geometry.wings.keys():           
        
        # Do the subsonic surrogates:
        if SUB:
            CL_w_surrogates_sub[wing]    = RectBivariateSpline(AoA_data, mach_data_sub, CL_w_data_sub[wing]) 
            CDi_w_surrogates_sub[wing]   = RectBivariateSpline(AoA_data, mach_data_sub, CDi_w_data_sub[wing])  
        # Do the supersonic surrogates:
        if SUP:
            CL_w_surrogates_sup[wing]    = RectBivariateSpline(AoA_data, mach_data_sup, CL_w_data_sup[wing]) 
            CDi_w_surrogates_sup[wing]   = RectBivariateSpline(AoA_data, mach_data_sup, CDi_w_data_sup[wing])
        # Do the transonic regime surrogates:
        if SUB and SUP:	  
            CLw                    = np.zeros_like(CL_data_trans)
            CDiw                   = np.zeros_like(CDi_data_trans)            
            CLw[:,0]               = CL_w_data_sub[wing][:,-1]   	 
            CLw[:,1]               = CL_w_data_sup[wing][:,0]  	
            CLw[:,2]               = CL_w_data_sup[wing][:,1]  	
            CDiw[:,0]              = CDi_w_data_sub[wing][:,-1]    
            CDiw[:,1]              = CDi_w_data_sup[wing][:,0]   
            CDiw[:,2]              = CDi_w_data_sup[wing][:,1]   
            CL_w_data_trans[wing]  = CLw
            CDi_w_data_trans[wing] = CDiw  
            
            CL_w_surrogates_trans[wing]  = RegularGridInterpolator((AoA_data, mach_data_trans_CL),\
                                                                   CL_w_data_trans[wing],method = 'linear', \
                                                                   bounds_error=False, fill_value=None)     
            CDi_w_surrogates_trans[wing] = RegularGridInterpolator((AoA_data, mach_data_trans_CL), \
                                                                   CDi_w_data_trans[wing],method = 'linear', \
                                                                   bounds_error=False, fill_value=None)           

    # Pack the outputs
    surrogates.lift_coefficient_sub        = CL_surrogate_sub  
    surrogates.lift_coefficient_sup        = CL_surrogate_sup  
    surrogates.lift_coefficient_trans      = CL_surrogate_trans
    surrogates.wing_lift_coefficient_sub   = CL_w_surrogates_sub  
    surrogates.wing_lift_coefficient_sup   = CL_w_surrogates_sup  
    surrogates.wing_lift_coefficient_trans = CL_w_surrogates_trans
    surrogates.drag_coefficient_sub        = CDi_surrogate_sub  
    surrogates.drag_coefficient_sup        = CDi_surrogate_sup  
    surrogates.drag_coefficient_trans      = CDi_surrogate_trans
    surrogates.wing_drag_coefficient_sub   = CDi_w_surrogates_sub  
    surrogates.wing_drag_coefficient_sup   = CDi_w_surrogates_sup  
    surrogates.wing_drag_coefficient_trans = CDi_w_surrogates_trans
    
    return

# ----------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------
def calculate_VLM(conditions,settings,geometry):
    """Calculate the total vehicle lift coefficient and specific wing coefficients (with specific wing reference areas)
    using a vortex lattice method.

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    conditions                      (passed to vortex lattice method)
    settings                        (passed to vortex lattice method)
    geometry.reference_area         [m^2]
    geometry.wings.*.reference_area (each wing is also passed to the vortex lattice method)

    Outputs:
    total_lift_coeff                [array]
    total_induced_drag_coeff        [array]
    wing_lifts                      [Data]
    wing_drags                      [Data]
    Properties Used:
    
    """            
    # iterate over wings
    total_lift_coeff   = 0.0
    wing_lifts         = Data()
    wing_drags         = Data()
    wing_induced_angle = Data()
        
    results = VLM(conditions,settings,geometry)
    total_lift_coeff          = results.CL
    total_induced_drag_coeff  = results.CDi
    total_side_coef           = results.CY 
    CL_wing                   = results.CL_wing  
    CDi_wing                  = results.CDi_wing 
    cl_y                      = results.cl_y     
    cdi_y                     = results.cdi_y    
    alpha_i                   = results.alpha_i  
    CPi                       = results.CP  
    CN                        = results.CN
    CL_mom                    = results.CL_mom
    CM                        = results.CM
    
    # Dimensionalize the lift and drag for each wing
    areas = geometry.vortex_distribution.wing_areas
    dim_wing_lifts = CL_wing  * areas
    dim_wing_drags = CDi_wing * areas
    
    i = 0
    # Assign the lift and drag and non-dimensionalize
    for wing in geometry.wings.values():
        ref = wing.areas.reference
        if wing.symmetric:
            wing_lifts[wing.tag]         = np.atleast_2d(np.sum(dim_wing_lifts[:,i:(i+2)],axis=1)).T/ref
            wing_drags[wing.tag]         = np.atleast_2d(np.sum(dim_wing_drags[:,i:(i+2)],axis=1)).T/ref
            wing_induced_angle[wing.tag] = np.concatenate((alpha_i[i],alpha_i[i+1]),axis=1)
            i+=1
        else:
            wing_lifts[wing.tag]         = np.atleast_2d(dim_wing_lifts[:,i]).T/ref
            wing_drags[wing.tag]         = np.atleast_2d(dim_wing_drags[:,i]).T/ref
            wing_induced_angle[wing.tag] = alpha_i[i]
        i+=1

    return total_lift_coeff, total_induced_drag_coeff, total_side_coef, wing_lifts, wing_drags, cl_y, cdi_y, wing_induced_angle, CPi,CN,CL_mom, CM
