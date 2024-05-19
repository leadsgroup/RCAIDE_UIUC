## @ingroup  Library-Methods-Stability
# RCAIDE/Library/Methods/Stability/VLM_Stability.py
# 
# 
# Created:  Apr 2024, M. Clarke
# Updated:  Mat 2024, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE 
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method   import VLM   
from RCAIDE.Library.Methods.Stability.Common          import compute_dynamic_flight_modes

# package imports
import numpy                                                     as np 
from scipy.interpolate                                           import RegularGridInterpolator
from scipy import interpolate

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Stability  
def evaluate_surrogate(state,settings,geometry):
    """Evaluates surrogates forces and moments using built surrogates 
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        stability       : VLM analysis          [unitless]
        state      : flight conditions     [unitless]
        settings   : VLM analysis settings [unitless]
        geometry   : vehicle configuration [unitless] 
        
    Returns: 
        None  
    """          
    
    # unpack
    stability   = state.analyses.stability
    conditions  = state.conditions  
    surrogates  = stability.surrogates 

    AoA         = np.atleast_2d(conditions.aerodynamics.angles.alpha)  
    Beta        = np.atleast_2d(conditions.aerodynamics.angles.beta)    
    Mach        = np.atleast_2d(conditions.freestream.mach_number)
    
    # only compute derivative if control surface exists
    if stability.aileron_flag: 
        delta_a     = np.atleast_2d(conditions.control_surfaces.aileron.deflection)
        pts_delta_a    = np.hstack((delta_a,Mach))
        Clift_delta_a  = np.atleast_2d(surrogates.Clift_delta_a(pts_delta_a)).T
        Cdrag_delta_a  = np.atleast_2d(surrogates.Cdrag_delta_a(pts_delta_a)).T  
        CX_delta_a     = np.atleast_2d(surrogates.CX_delta_a(pts_delta_a)).T 
        CY_delta_a     = np.atleast_2d(surrogates.CY_delta_a(pts_delta_a)).T     
        CZ_delta_a     = np.atleast_2d(surrogates.CZ_delta_a(pts_delta_a)).T     
        CL_delta_a     = np.atleast_2d(surrogates.CL_delta_a(pts_delta_a)).T     
        CM_delta_a     = np.atleast_2d(surrogates.CM_delta_a(pts_delta_a)).T     
        CN_delta_a     = np.atleast_2d(surrogates.CN_delta_a(pts_delta_a)).T  
        
    if stability.elevator_flag: 
        delta_e     = np.atleast_2d(conditions.control_surfaces.elevator.deflection)
        pts_delta_e          = np.hstack((delta_e,Mach))   
        Clift_delta_e  = np.atleast_2d(surrogates.Clift_delta_e(pts_delta_e)).T  
        Cdrag_delta_e  = np.atleast_2d(surrogates.Cdrag_delta_e(pts_delta_e)).T 
        CX_delta_e     = np.atleast_2d(surrogates.CX_delta_e(pts_delta_e)).T
        CY_delta_e     = np.atleast_2d(surrogates.CY_delta_e(pts_delta_e)).T     
        CZ_delta_e     = np.atleast_2d(surrogates.CZ_delta_e(pts_delta_e)).T     
        CL_delta_e     = np.atleast_2d(surrogates.CL_delta_e(pts_delta_e)).T     
        CM_delta_e     = np.atleast_2d(surrogates.CM_delta_e(pts_delta_e)).T     
        CN_delta_e     = np.atleast_2d(surrogates.CN_delta_e(pts_delta_e)).T  
        
    if stability.rudder_flag:
        delta_r     = np.atleast_2d(conditions.control_surfaces.rudder.deflection)
        pts_delta_r          = np.hstack((delta_r,Mach))
        Clift_delta_r  = np.atleast_2d(surrogates.Clift_delta_r(pts_delta_r)).T 
        Cdrag_delta_r  = np.atleast_2d(surrogates.Cdrag_delta_r(pts_delta_r)).T 
        CX_delta_r     = np.atleast_2d(surrogates.CX_delta_r(pts_delta_r)).T
        CY_delta_r     = np.atleast_2d(surrogates.CY_delta_r(pts_delta_r)).T     
        CZ_delta_r     = np.atleast_2d(surrogates.CZ_delta_r(pts_delta_r)).T     
        CL_delta_r     = np.atleast_2d(surrogates.CL_delta_r(pts_delta_r)).T     
        CM_delta_r     = np.atleast_2d(surrogates.CM_delta_r(pts_delta_r)).T     
        CN_delta_r     = np.atleast_2d(surrogates.CN_delta_r(pts_delta_r)).T  
        
    if stability.flap_flag:  
        delta_f     = np.atleast_2d(conditions.control_surfaces.flap.deflection)   
        pts_delta_f          = np.hstack((delta_f,Mach))   
        Clift_delta_f  = np.atleast_2d(surrogates.Clift_delta_f(pts_delta_f)).T  
        Cdrag_delta_f  = np.atleast_2d(surrogates.Cdrag_delta_f(pts_delta_f)).T 
        CX_delta_f     = np.atleast_2d(surrogates.CX_delta_f(pts_delta_f)).T  
        CY_delta_f     = np.atleast_2d(surrogates.CY_delta_f(pts_delta_f)).T     
        CZ_delta_f     = np.atleast_2d(surrogates.CZ_delta_f(pts_delta_f)).T     
        CL_delta_f     = np.atleast_2d(surrogates.CL_delta_f(pts_delta_f)).T     
        CM_delta_f     = np.atleast_2d(surrogates.CM_delta_f(pts_delta_f)).T     
        CN_delta_f     = np.atleast_2d(surrogates.CN_delta_f(pts_delta_f)).T                
        
    if stability.slat_flag:
        delta_s     = np.atleast_2d(conditions.control_surfaces.slat.deflection)    
        pts_delta_s    = np.hstack((delta_s,Mach))        
        Clift_delta_s  = np.atleast_2d(surrogates.Clift_delta_s(pts_delta_s)).T
        Cdrag_delta_s  = np.atleast_2d(surrogates.Cdrag_delta_s(pts_delta_s)).T 
        CX_delta_s     = np.atleast_2d(surrogates.CX_delta_s(pts_delta_s)).T    
        CY_delta_s     = np.atleast_2d(surrogates.CY_delta_s(pts_delta_s)).T     
        CZ_delta_s     = np.atleast_2d(surrogates.CZ_delta_s(pts_delta_s)).T     
        CL_delta_s     = np.atleast_2d(surrogates.CL_delta_s(pts_delta_s)).T     
        CM_delta_s     = np.atleast_2d(surrogates.CM_delta_s(pts_delta_s)).T     
        CN_delta_s     = np.atleast_2d(surrogates.CN_delta_s(pts_delta_s)).T   

    u           = np.atleast_2d(conditions.freestream.u)
    v           = np.atleast_2d(conditions.freestream.v)
    w           = np.atleast_2d(conditions.freestream.w)
    p           = np.atleast_2d(conditions.static_stability.roll_rate)        
    q           = np.atleast_2d(conditions.static_stability.pitch_rate)
    r           = np.atleast_2d(conditions.static_stability.yaw_rate)  

    # Query surrogates  
    pts_alpha            = np.hstack((AoA,Mach))
    pts_beta             = np.hstack((Beta,Mach))  
    pts_u                = np.hstack((u,Mach))
    pts_v                = np.hstack((v,Mach))
    pts_w                = np.hstack((w,Mach))
    pts_p                = np.hstack((p,Mach))
    pts_q                = np.hstack((q,Mach))
    pts_r                = np.hstack((r,Mach))
    
    oswald_efficiency = np.atleast_2d(surrogates.oswald_efficiency(pts_alpha)).T  
    Clift_alpha    = np.atleast_2d(surrogates.Clift_alpha(pts_alpha)).T
    Clift_beta     = np.atleast_2d(surrogates.Clift_beta(pts_beta)).T
    Clift_u        = np.atleast_2d(surrogates.Clift_u(pts_u)).T
    Clift_v        = np.atleast_2d(surrogates.Clift_v(pts_v)).T
    Clift_w        = np.atleast_2d(surrogates.Clift_w(pts_w)).T
    Clift_p        = np.atleast_2d(surrogates.Clift_p(pts_p)).T
    Clift_q        = np.atleast_2d(surrogates.Clift_q(pts_q)).T
    Clift_r        = np.atleast_2d(surrogates.Clift_r(pts_r)).T
    Cdrag_alpha    = np.atleast_2d(surrogates.Cdrag_alpha(pts_alpha)).T
    Cdrag_beta     = np.atleast_2d(surrogates.Cdrag_beta(pts_beta)).T 

    Cdrag_u        = np.atleast_2d(surrogates.Cdrag_u(pts_u)).T
    Cdrag_v        = np.atleast_2d(surrogates.Cdrag_v(pts_v)).T
    Cdrag_w        = np.atleast_2d(surrogates.Cdrag_w(pts_w)).T
    Cdrag_p        = np.atleast_2d(surrogates.Cdrag_p(pts_p)).T
    Cdrag_q        = np.atleast_2d(surrogates.Cdrag_q(pts_q)).T
    Cdrag_r        = np.atleast_2d(surrogates.Cdrag_r(pts_r)).T
    CX_alpha       = np.atleast_2d(surrogates.CX_alpha(pts_alpha)).T
    CX_beta        = np.atleast_2d(surrogates.CX_beta(pts_beta)).T 
    
    CX_u           = np.atleast_2d(surrogates.CX_u(pts_u)).T
    CX_v           = np.atleast_2d(surrogates.CX_v(pts_v)).T
    CX_w           = np.atleast_2d(surrogates.CX_w(pts_w)).T
    CX_p           = np.atleast_2d(surrogates.CX_p(pts_p)).T
    CX_q           = np.atleast_2d(surrogates.CX_q(pts_q)).T
    CX_r           = np.atleast_2d(surrogates.CX_r(pts_r)).T
    CY_alpha       = np.atleast_2d(surrogates.CY_alpha(pts_alpha)).T
    CY_beta        = np.atleast_2d(surrogates.CY_beta(pts_beta)).T

    CY_u           = np.atleast_2d(surrogates.CY_u(pts_u)).T
    CY_v           = np.atleast_2d(surrogates.CY_v(pts_v)).T
    CY_w           = np.atleast_2d(surrogates.CY_w(pts_w)).T
    CY_p           = np.atleast_2d(surrogates.CY_p(pts_p)).T
    CY_q           = np.atleast_2d(surrogates.CY_q(pts_q)).T
    CY_r           = np.atleast_2d(surrogates.CY_r(pts_r)).T
    CZ_alpha       = np.atleast_2d(surrogates.CZ_alpha(pts_alpha)).T
    CZ_beta        = np.atleast_2d(surrogates.CZ_beta(pts_beta)).T 
    
    CZ_u           = np.atleast_2d(surrogates.CZ_u(pts_u)).T
    CZ_v           = np.atleast_2d(surrogates.CZ_v(pts_v)).T
    CZ_w           = np.atleast_2d(surrogates.CZ_w(pts_w)).T
    CZ_p           = np.atleast_2d(surrogates.CZ_p(pts_p)).T
    CZ_q           = np.atleast_2d(surrogates.CZ_q(pts_q)).T
    CZ_r           = np.atleast_2d(surrogates.CZ_r(pts_r)).T
    CL_alpha       = np.atleast_2d(surrogates.CL_alpha(pts_alpha)).T
    CL_beta        = np.atleast_2d(surrogates.CL_beta(pts_beta)).T   
    
    CL_u           = np.atleast_2d(surrogates.CL_u(pts_u)).T
    CL_v           = np.atleast_2d(surrogates.CL_v(pts_v)).T
    CL_w           = np.atleast_2d(surrogates.CL_w(pts_w)).T
    CL_p           = np.atleast_2d(surrogates.CL_p(pts_p)).T
    CL_q           = np.atleast_2d(surrogates.CL_q(pts_q)).T
    CL_r           = np.atleast_2d(surrogates.CL_r(pts_r)).T
    CM_alpha       = np.atleast_2d(surrogates.CM_alpha(pts_alpha)).T
    CM_beta        = np.atleast_2d(surrogates.CM_beta(pts_beta)).T 
    
    CM_u           = np.atleast_2d(surrogates.CM_u(pts_u)).T
    CM_v           = np.atleast_2d(surrogates.CM_v(pts_v)).T
    CM_w           = np.atleast_2d(surrogates.CM_w(pts_w)).T
    CM_p           = np.atleast_2d(surrogates.CM_p(pts_p)).T
    CM_q           = np.atleast_2d(surrogates.CM_q(pts_q)).T
    CM_r           = np.atleast_2d(surrogates.CM_r(pts_r)).T
    CN_alpha       = np.atleast_2d(surrogates.CN_alpha(pts_alpha)).T
    CN_beta        = np.atleast_2d(surrogates.CN_beta(pts_beta)).T 
    
    CN_u           = np.atleast_2d(surrogates.CN_u(pts_u)).T
    CN_v           = np.atleast_2d(surrogates.CN_v(pts_v)).T
    CN_w           = np.atleast_2d(surrogates.CN_w(pts_w)).T
    CN_p           = np.atleast_2d(surrogates.CN_p(pts_p)).T
    CN_q           = np.atleast_2d(surrogates.CN_q(pts_q)).T
    CN_r           = np.atleast_2d(surrogates.CN_r(pts_r)).T

    # Stability Results  
    conditions.S_ref                                                  = stability.S_ref              
    conditions.c_ref                                                  = stability.c_ref              
    conditions.b_ref                                                  = stability.b_ref
    conditions.X_ref                                                  = stability.X_ref
    conditions.Y_ref                                                  = stability.Y_ref
    conditions.Z_ref                                                  = stability.Z_ref
    conditions.aerodynamics.oswald_efficiency                         = oswald_efficiency 
    
    conditions.static_stability.coefficients.lift                     = Clift_alpha + Clift_beta + Clift_u + Clift_v + Clift_w + Clift_p + Clift_q + Clift_r 
    conditions.static_stability.coefficients.drag                     = Cdrag_alpha + Cdrag_beta + Cdrag_u + Cdrag_v + Cdrag_w + Cdrag_p + Cdrag_q + Cdrag_r 
    conditions.static_stability.coefficients.X                        = CX_alpha + CX_beta + CX_u + CX_v + CX_w + CX_p + CX_q + CX_r
    conditions.static_stability.coefficients.Y                        = CY_alpha + CY_beta + CY_u + CY_v + CY_w + CY_p + CY_q + CY_r
    conditions.static_stability.coefficients.Z                        = CZ_alpha + CZ_beta + CZ_u + CZ_v + CZ_w + CZ_p + CZ_q + CZ_r
    conditions.static_stability.coefficients.L                        = CL_alpha + CL_beta + CL_u + CL_v + CL_w + CL_p + CL_q + CL_r
    conditions.static_stability.coefficients.M                        = CM_alpha + CM_beta + CM_u + CM_v + CM_w + CM_p + CM_q + CM_r
    conditions.static_stability.coefficients.N                        = CN_alpha + CN_beta + CN_u + CN_v + CN_w + CN_p + CN_q + CN_r
    
    if stability.aileron_flag: 
        conditions.static_stability.coefficients.lift += Clift_delta_a
        conditions.static_stability.coefficients.drag += Cdrag_delta_a
        conditions.static_stability.coefficients.X    += CX_delta_a 
        conditions.static_stability.coefficients.Y    += CY_delta_a
        conditions.static_stability.coefficients.Z    += CZ_delta_a
        conditions.static_stability.coefficients.L    += CL_delta_a
        conditions.static_stability.coefficients.M    += CM_delta_a
        conditions.static_stability.coefficients.N    += CN_delta_a
        

        conditions.control_surfaces.aileron.static_stability.coefficients.lift       = Clift_delta_a         
        conditions.control_surfaces.aileron.static_stability.coefficients.drag       = Cdrag_delta_a            
        conditions.control_surfaces.aileron.static_stability.coefficients.X          = CX_delta_a             
        conditions.control_surfaces.aileron.static_stability.coefficients.Y          = CY_delta_a            
        conditions.control_surfaces.aileron.static_stability.coefficients.Z          = CZ_delta_a          
        conditions.control_surfaces.aileron.static_stability.coefficients.L          = CL_delta_a          
        conditions.control_surfaces.aileron.static_stability.coefficients.M          = CM_delta_a          
        conditions.control_surfaces.aileron.static_stability.coefficients.N          = CN_delta_a             
        
    if stability.elevator_flag: 
        conditions.static_stability.coefficients.lift += Clift_delta_e
        conditions.static_stability.coefficients.drag += Cdrag_delta_e
        conditions.static_stability.coefficients.X    += CX_delta_e 
        conditions.static_stability.coefficients.Y    += CY_delta_e
        conditions.static_stability.coefficients.Z    += CZ_delta_e
        conditions.static_stability.coefficients.L    += CL_delta_e
        conditions.static_stability.coefficients.M    += CM_delta_e
        conditions.static_stability.coefficients.N    += CN_delta_e
        
        conditions.control_surfaces.elevator.static_stability.coefficients.lift       = Clift_delta_e         
        conditions.control_surfaces.elevator.static_stability.coefficients.drag       = Cdrag_delta_e            
        conditions.control_surfaces.elevator.static_stability.coefficients.X          = CX_delta_e             
        conditions.control_surfaces.elevator.static_stability.coefficients.Y          = CY_delta_e            
        conditions.control_surfaces.elevator.static_stability.coefficients.Z          = CZ_delta_e          
        conditions.control_surfaces.elevator.static_stability.coefficients.L          = CL_delta_e          
        conditions.control_surfaces.elevator.static_stability.coefficients.M          = CM_delta_e          
        conditions.control_surfaces.elevator.static_stability.coefficients.N          = CN_delta_e            
        
    if stability.rudder_flag:  
        conditions.static_stability.coefficients.lift += Clift_delta_r
        conditions.static_stability.coefficients.drag += Cdrag_delta_r
        conditions.static_stability.coefficients.X    += CX_delta_r 
        conditions.static_stability.coefficients.Y    += CY_delta_r
        conditions.static_stability.coefficients.Z    += CZ_delta_r
        conditions.static_stability.coefficients.L    += CL_delta_r
        conditions.static_stability.coefficients.M    += CM_delta_r
        conditions.static_stability.coefficients.N    += CN_delta_r

        conditions.control_surfaces.rudder.static_stability.coefficients.lift       = Clift_delta_r         
        conditions.control_surfaces.rudder.static_stability.coefficients.drag       = Cdrag_delta_r            
        conditions.control_surfaces.rudder.static_stability.coefficients.X          = CX_delta_r             
        conditions.control_surfaces.rudder.static_stability.coefficients.Y          = CY_delta_r            
        conditions.control_surfaces.rudder.static_stability.coefficients.Z          = CZ_delta_r          
        conditions.control_surfaces.rudder.static_stability.coefficients.L          = CL_delta_r          
        conditions.control_surfaces.rudder.static_stability.coefficients.M          = CM_delta_r          
        conditions.control_surfaces.rudder.static_stability.coefficients.N          = CN_delta_r         
        
    if stability.flap_flag:
        conditions.static_stability.coefficients.lift += Clift_delta_f
        conditions.static_stability.coefficients.drag += Cdrag_delta_f
        conditions.static_stability.coefficients.X    += CX_delta_f 
        conditions.static_stability.coefficients.Y    += CY_delta_f
        conditions.static_stability.coefficients.Z    += CZ_delta_f
        conditions.static_stability.coefficients.L    += CL_delta_f
        conditions.static_stability.coefficients.M    += CM_delta_f
        conditions.static_stability.coefficients.N    += CN_delta_f
        

        conditions.control_surfaces.flap.static_stability.coefficients.lift       = Clift_delta_f         
        conditions.control_surfaces.flap.static_stability.coefficients.drag       = Cdrag_delta_f            
        conditions.control_surfaces.flap.static_stability.coefficients.X          = CX_delta_f             
        conditions.control_surfaces.flap.static_stability.coefficients.Y          = CY_delta_f            
        conditions.control_surfaces.flap.static_stability.coefficients.Z          = CZ_delta_f          
        conditions.control_surfaces.flap.static_stability.coefficients.L          = CL_delta_f          
        conditions.control_surfaces.flap.static_stability.coefficients.M          = CM_delta_f          
        conditions.control_surfaces.flap.static_stability.coefficients.N          = CN_delta_f           
        

    if stability.slat_flag: 
        conditions.static_stability.coefficients.lift += Clift_delta_s
        conditions.static_stability.coefficients.drag += Cdrag_delta_s
        conditions.static_stability.coefficients.X    += CX_delta_s 
        conditions.static_stability.coefficients.Y    += CY_delta_s
        conditions.static_stability.coefficients.Z    += CZ_delta_s
        conditions.static_stability.coefficients.L    += CL_delta_s
        conditions.static_stability.coefficients.M    += CM_delta_s
        conditions.static_stability.coefficients.N    += CN_delta_s

        conditions.control_surfaces.slat.static_stability.coefficients.lift       = Clift_delta_s         
        conditions.control_surfaces.slat.static_stability.coefficients.drag       = Cdrag_delta_s            
        conditions.control_surfaces.slat.static_stability.coefficients.X          = CX_delta_s             
        conditions.control_surfaces.slat.static_stability.coefficients.Y          = CY_delta_s            
        conditions.control_surfaces.slat.static_stability.coefficients.Z          = CZ_delta_s          
        conditions.control_surfaces.slat.static_stability.coefficients.L          = CL_delta_s          
        conditions.control_surfaces.slat.static_stability.coefficients.M          = CM_delta_s          
        conditions.control_surfaces.slat.static_stability.coefficients.N          = CN_delta_s                     
     
    
    conditions.static_stability.derivatives.Clift_alpha               = surrogates.dClift_dalpha(Mach)
    conditions.static_stability.derivatives.CY_alpha                  = surrogates.dCY_dalpha(Mach)
    conditions.static_stability.derivatives.CL_alpha                  = surrogates.dCL_dalpha(Mach)
    conditions.static_stability.derivatives.CM_alpha                  = surrogates.dCM_dalpha(Mach)
    conditions.static_stability.derivatives.CN_alpha                  = surrogates.dCN_dalpha(Mach)
    conditions.static_stability.derivatives.Clift_beta                = surrogates.dClift_dbeta(Mach)
    conditions.static_stability.derivatives.CY_beta                   = surrogates.dCY_dbeta(Mach)
    conditions.static_stability.derivatives.CL_beta                   = surrogates.dCL_dbeta(Mach)
    conditions.static_stability.derivatives.CM_beta                   = surrogates.dCM_dbeta(Mach)
    conditions.static_stability.derivatives.CN_beta                   = surrogates.dCN_dbeta(Mach)
    conditions.static_stability.derivatives.Clift_p                   = surrogates.dClift_dp(Mach)
    conditions.static_stability.derivatives.Clift_q                   = surrogates.dClift_dq(Mach)
    conditions.static_stability.derivatives.Clift_r                   = surrogates.dClift_dr(Mach)
    
    conditions.static_stability.derivatives.CX_u                      = surrogates.dCX_du(Mach)
    conditions.static_stability.derivatives.CX_v                      = surrogates.dCX_dv(Mach)
    conditions.static_stability.derivatives.CX_w                      = surrogates.dCX_dw(Mach)
    conditions.static_stability.derivatives.CY_u                      = surrogates.dCY_du(Mach)
    conditions.static_stability.derivatives.CY_v                      = surrogates.dCY_dv(Mach)
    conditions.static_stability.derivatives.CY_w                      = surrogates.dCY_dw(Mach)
    conditions.static_stability.derivatives.CZ_u                      = surrogates.dCZ_du(Mach)
    conditions.static_stability.derivatives.CZ_v                      = surrogates.dCZ_dv(Mach)
    conditions.static_stability.derivatives.CZ_w                      = surrogates.dCZ_dw(Mach)
    conditions.static_stability.derivatives.CL_u                      = surrogates.dCL_du(Mach)
    conditions.static_stability.derivatives.CL_v                      = surrogates.dCL_dv(Mach)
    conditions.static_stability.derivatives.CL_w                      = surrogates.dCL_dw(Mach)
    conditions.static_stability.derivatives.CM_u                      = surrogates.dCM_du(Mach)
    conditions.static_stability.derivatives.CM_v                      = surrogates.dCM_dv(Mach)
    conditions.static_stability.derivatives.CM_w                      = surrogates.dCM_dw(Mach)
    conditions.static_stability.derivatives.CN_u                      = surrogates.dCN_du(Mach)
    conditions.static_stability.derivatives.CN_v                      = surrogates.dCN_dv(Mach)
    conditions.static_stability.derivatives.CN_w                      = surrogates.dCN_dw(Mach)
    
    conditions.static_stability.derivatives.CX_p                      = surrogates.dCX_dp(Mach)
    conditions.static_stability.derivatives.CX_q                      = surrogates.dCX_dq(Mach)
    conditions.static_stability.derivatives.CX_r                      = surrogates.dCX_dr(Mach)
    conditions.static_stability.derivatives.CY_p                      = surrogates.dCY_dp(Mach)
    conditions.static_stability.derivatives.CY_q                      = surrogates.dCY_dq(Mach)
    conditions.static_stability.derivatives.CY_r                      = surrogates.dCY_dr(Mach)
    conditions.static_stability.derivatives.CZ_p                      = surrogates.dCZ_dp(Mach)
    conditions.static_stability.derivatives.CZ_q                      = surrogates.dCZ_dq(Mach)
    conditions.static_stability.derivatives.CZ_r                      = surrogates.dCZ_dr(Mach)
    conditions.static_stability.derivatives.CL_p                      = surrogates.dCL_dp(Mach)
    conditions.static_stability.derivatives.CL_q                      = surrogates.dCL_dq(Mach)
    conditions.static_stability.derivatives.CL_r                      = surrogates.dCL_dr(Mach)
    conditions.static_stability.derivatives.CM_p                      = surrogates.dCM_dp(Mach)
    conditions.static_stability.derivatives.CM_q                      = surrogates.dCM_dq(Mach)
    conditions.static_stability.derivatives.CM_r                      = surrogates.dCM_dr(Mach)
    conditions.static_stability.derivatives.CN_p                      = surrogates.dCN_dp(Mach)
    conditions.static_stability.derivatives.CN_q                      = surrogates.dCN_dq(Mach)
    conditions.static_stability.derivatives.CN_r                      = surrogates.dCN_dr(Mach)
    #conditions.static_stability.neutral_point                         = # Need to Update
    #conditions.static_stability.spiral_criteria                       = # Need to Update 
    
    conditions.aerodynamics.coefficients.lift               = conditions.static_stability.coefficients.lift # overwrite lift in aerodynamic results 
    conditions.aerodynamics.lift_breakdown.total            = conditions.static_stability.coefficients.lift # overwrite lift in aerodynamic results 
    conditions.aerodynamics.drag_breakdown.induced.inviscid = conditions.static_stability.coefficients.drag 

    # -----------------------------------------------------------------------------------------------------------------------                     
    # Dynamic Stability & System Identification
    # -----------------------------------------------------------------------------------------------------------------------      
    # Dynamic Stability
    if np.count_nonzero(geometry.mass_properties.moments_of_inertia.tensor) > 0:  
        compute_dynamic_flight_modes(conditions,geometry)   
        
    return     
 
def evaluate_no_surrogate(state,settings,geometry):
    """Evaluates forces and moments directly using VLM.
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        stability       : VLM analysis          [unitless]
        state      : flight conditions     [unitless]
        settings   : VLM analysis settings [unitless]
        geometry   : vehicle configuration [unitless] 
        
    Returns: 
        None  
    """          

    # unpack
    stability  = state.analyses.stability
    conditions = state.conditions 
    settings   = stability.settings
    geometry   = stability.geometry     
    
    # if in transonic regime, use surrogate
    Clift,Cdrag,CX,CY,CZ,CL_mom,CM,CN, S_ref,b_ref,c_ref,X_ref,Y_ref ,Z_ref = evaluate_VLM(conditions,settings,geometry) 

    # compute deriviatives and pack   
    conditions.static_stability.coefficients.lift    = np.atleast_2d(Clift).T
    conditions.static_stability.coefficients.drag    = np.atleast_2d(Cdrag).T 
    conditions.static_stability.coefficients.X      = np.atleast_2d(CX).T  
    conditions.static_stability.coefficients.Y      = np.atleast_2d(CY).T
    conditions.static_stability.coefficients.Z      = np.atleast_2d(CZ).T  
    conditions.static_stability.coefficients.L      = np.atleast_2d(CL_mom).T
    conditions.static_stability.coefficients.M      = np.atleast_2d(CM).T
    conditions.static_stability.coefficients.N      = np.atleast_2d(CN).T 
    return  

def sample_training(stability):
    """Call methods to run VLM for sample point evaluation. 
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        stability       : VLM analysis          [unitless] 
        
    Returns: 
        None    
    """

    geometry       = stability.geometry
    settings       = stability.settings
    training       = stability.training
    Mach           = stability.training.Mach
    AoA            = stability.training.angle_of_attack                  
    Beta           = stability.training.sideslip_angle
    
    # loop through wings to determine what control surfaces are present 
    for wing in stability.geometry.wings: 
        for control_surface in wing.control_surfaces:  
            if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Aileron: 
                delta_a        = stability.training.aileron_deflection
                len_d_a        = len(delta_a)
                stability.aileron_flag   = True 
            if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Elevator: 
                delta_e        = stability.training.elevator_deflection
                len_d_e        = len(delta_e)   
                stability.elevator_flag = True 
            if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Rudder:  
                delta_r        = stability.training.rudder_deflection
                stability.rudder_flag    = True
                len_d_r        = len(delta_r)  
            if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Slat: 
                delta_s        = stability.training.slat_deflection
                len_d_s        = len(delta_s)   
                stability.slat_flag = True 
            if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Flap:  
                delta_f        = stability.training.rudder_deflection
                stability.flap_flag    = True
                len_d_f        = len(delta_f)  
             
    u              = stability.training.u
    v              = stability.training.v
    w              = stability.training.w
    pitch_rate     = stability.training.pitch_rate
    roll_rate      = stability.training.roll_rate
    yaw_rate       = stability.training.yaw_rate

    len_Mach       = len(Mach)        
    len_AoA        = len(AoA)  
    len_Beta       = len(Beta)
    len_u          = len(u)
    len_v          = len(v)
    len_w          = len(w)
    len_pitch_rate = len(pitch_rate)
    len_roll_rate  = len(roll_rate) 
    len_yaw_rate   = len(yaw_rate) 
    
    # --------------------------------------------------------------------------------------------------------------
    # Alpha
    # --------------------------------------------------------------------------------------------------------------
    
    # Setup new array shapes for vectorization 
    # stakcing 9x9 matrices into one horizontal line(81)  
    AoAs       = np.atleast_2d(np.tile(AoA,len_Mach).T.flatten()).T 
    Machs      = np.atleast_2d(np.repeat(Mach,len_AoA)).T        
    
    # reset conditions  
    conditions                                      = RCAIDE.Framework.Mission.Common.Results()
    conditions.freestream.mach_number               = Machs
    conditions.aerodynamics.angles.alpha            = np.ones_like(Machs)*AoAs 
    
    Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res, S_ref,b_ref,c_ref,X_ref,Y_ref ,Z_ref = evaluate_VLM(conditions,settings,geometry)
    
    Clift_alpha   = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
    Cdrag_alpha   = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T 
    CX_alpha      = np.reshape(CX_res,(len_Mach,len_AoA)).T 
    CY_alpha      = np.reshape(CY_res,(len_Mach,len_AoA)).T 
    CZ_alpha      = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
    CL_alpha      = np.reshape(CL_res,(len_Mach,len_AoA)).T 
    CM_alpha      = np.reshape(CM_res,(len_Mach,len_AoA)).T 
    CN_alpha      = np.reshape(CN_res,(len_Mach,len_AoA)).T 
    
    
    # Angle of Attack at 0 Degrees 
    Clift_alpha_0   =  np.tile(Clift_alpha[4][None,:],(2,1))
    Cdrag_alpha_0   =  np.tile(Cdrag_alpha[4][None,:],(2,1))
    CX_alpha_0      =  np.tile(CX_alpha[4][None,:],(2, 1)) 
    CY_alpha_0      =  np.tile(CY_alpha[4][None,:],(2, 1)) 
    CZ_alpha_0      =  np.tile(CZ_alpha[4][None,:],(2, 1)) 
    CL_alpha_0      =  np.tile(CL_alpha[4][None,:],(2, 1)) 
    CM_alpha_0      =  np.tile(CM_alpha[4][None,:],(2, 1)) 
    CN_alpha_0      =  np.tile(CN_alpha[4][None,:],(2, 1))
    
    
    stability.S_ref = S_ref
    stability.b_ref = b_ref
    stability.c_ref = c_ref
    stability.X_ref = X_ref
    stability.Y_ref = Y_ref
    stability.Z_ref = Z_ref
    stability.aspect_ratio = (b_ref ** 2) / S_ref 
    oswald_efficiency =  (Clift_res**2)/(np.pi* stability.aspect_ratio *Cdrag_res) 
    oswald_efficiency = np.reshape(oswald_efficiency,(len_Mach,len_AoA)).T 
    # --------------------------------------------------------------------------------------------------------------
    # Beta 
    # --------------------------------------------------------------------------------------------------------------
    Betas         = np.atleast_2d(np.tile(Beta,len_Mach).T.flatten()).T 
    Machs         = np.atleast_2d(np.repeat(Mach,len_Beta)).T        

    conditions                                      = RCAIDE.Framework.Mission.Common.Results()
    conditions.expand_rows(rows= len(Machs))
    conditions.freestream.mach_number               = Machs 
    conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12
    conditions.aerodynamics.angles.beta             = np.ones_like(Machs)*Betas   
    
    Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)
    
    Clift_beta = np.reshape(Clift_res,(len_Mach,len_Beta)).T - Clift_alpha_0
    Cdrag_beta = np.reshape(Cdrag_res,(len_Mach,len_Beta)).T - Cdrag_alpha_0                                
    CX_beta    = np.reshape(CX_res,(len_Mach,len_Beta)).T    - CX_alpha_0   
    CY_beta    = np.reshape(CY_res,(len_Mach,len_Beta)).T    - CY_alpha_0   
    CZ_beta    = np.reshape(CZ_res,(len_Mach,len_Beta)).T    - CZ_alpha_0   
    CL_beta    = np.reshape(CL_res,(len_Mach,len_Beta)).T    - CL_alpha_0   
    CM_beta    = np.reshape(CM_res,(len_Mach,len_Beta)).T    - CM_alpha_0   
    CN_beta    = np.reshape(CN_res,(len_Mach,len_Beta)).T    - CN_alpha_0 
 
    # -------------------------------------------------------      
    # Velocity u 
    # -------------------------------------------------------
    u_s     = np.atleast_2d(np.tile(u, len_Mach).T.flatten()).T 
    Machs   = np.atleast_2d(np.repeat(Mach,len_u)).T                   
    conditions                                      = RCAIDE.Framework.Mission.Common.Results() 
    conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12
    conditions.freestream.mach_number               = Machs + Machs*u_s 
    
    Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)
    
    Clift_u     = np.reshape(Clift_res,(len_Mach,len_u)).T - Clift_alpha_0
    Cdrag_u     = np.reshape(Cdrag_res,(len_Mach,len_u)).T - Cdrag_alpha_0
    CX_u        = np.reshape(CX_res,(len_Mach,len_u)).T    - CX_alpha_0   
    CY_u        = np.reshape(CY_res,(len_Mach,len_u)).T    - CY_alpha_0   
    CZ_u        = np.reshape(CZ_res,(len_Mach,len_u)).T    - CZ_alpha_0   
    CL_u        = np.reshape(CL_res,(len_Mach,len_u)).T    - CL_alpha_0   
    CM_u        = np.reshape(CM_res,(len_Mach,len_u)).T    - CM_alpha_0   
    CN_u        = np.reshape(CN_res,(len_Mach,len_u)).T    - CN_alpha_0   
    
    # -------------------------------------------------------               
    # Velocity v 
    # -------------------------------------------------------
    v_s     = np.atleast_2d(np.tile(v, len_Mach).T.flatten()).T 
    Machs         = np.atleast_2d(np.repeat(Mach,len_v)).T    

    conditions                                      = RCAIDE.Framework.Mission.Common.Results()  
    conditions.freestream.mach_number               = Machs
    conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12
    conditions.aerodynamics.angles.beta             = np.arcsin(v_s)       
    
    Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)
    
    Clift_v     = np.reshape(Clift_res,(len_Mach,len_v)).T - Clift_alpha_0
    Cdrag_v     = np.reshape(Cdrag_res,(len_Mach,len_v)).T - Cdrag_alpha_0
    CX_v        = np.reshape(CX_res,(len_Mach,len_v)).T    - CX_alpha_0   
    CY_v        = np.reshape(CY_res,(len_Mach,len_v)).T    - CY_alpha_0   
    CZ_v        = np.reshape(CZ_res,(len_Mach,len_v)).T    - CZ_alpha_0   
    CL_v        = np.reshape(CL_res,(len_Mach,len_v)).T    - CL_alpha_0   
    CM_v        = np.reshape(CM_res,(len_Mach,len_v)).T    - CM_alpha_0   
    CN_v        = np.reshape(CN_res,(len_Mach,len_v)).T    - CN_alpha_0   
    
    # -------------------------------------------------------               
    # Velocity w 
    # -------------------------------------------------------
    w_s     = np.atleast_2d(np.tile(w, len_Mach).T.flatten()).T 
    Machs   = np.atleast_2d(np.repeat(Mach,len_w)).T
     
    conditions                                      = RCAIDE.Framework.Mission.Common.Results()  
    conditions.freestream.mach_number               = Machs 
    conditions.aerodynamics.angles.alpha            = np.arcsin(w_s)
    
    Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)
    
    Clift_w     = np.reshape(Clift_res,(len_Mach,len_w)).T - Clift_alpha_0
    Cdrag_w     = np.reshape(Cdrag_res,(len_Mach,len_w)).T - Cdrag_alpha_0
    CX_w        = np.reshape(CX_res,(len_Mach,len_w)).T    - CX_alpha_0   
    CY_w        = np.reshape(CY_res,(len_Mach,len_w)).T    - CY_alpha_0   
    CZ_w        = np.reshape(CZ_res,(len_Mach,len_w)).T    - CZ_alpha_0   
    CL_w        = np.reshape(CL_res,(len_Mach,len_w)).T    - CL_alpha_0   
    CM_w        = np.reshape(CM_res,(len_Mach,len_w)).T    - CM_alpha_0   
    CN_w        = np.reshape(CN_res,(len_Mach,len_w)).T    - CN_alpha_0           
                    
    # -------------------------------------------------------               
    # Pitch Rate 
    # -------------------------------------------------------
    q_s     = np.atleast_2d(np.tile(pitch_rate, len_Mach).T.flatten()).T 
    Machs   = np.atleast_2d(np.repeat(Mach,len_pitch_rate)).T

    conditions                                      = RCAIDE.Framework.Mission.Common.Results() 
    conditions.freestream.mach_number               = Machs 
    conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12
    conditions.static_stability.pitch_rate          = np.ones_like(Machs)*q_s     
    conditions.freestream.velocity                  = Machs * 343 # speed of sound   
    
    Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)
    
    Clift_pitch_rate     = np.reshape(Clift_res,(len_Mach,len_pitch_rate)).T - Clift_alpha_0
    Cdrag_pitch_rate     = np.reshape(Cdrag_res,(len_Mach,len_pitch_rate)).T - Cdrag_alpha_0
    CX_pitch_rate        = np.reshape(CX_res,(len_Mach,len_pitch_rate)).T    - CX_alpha_0   
    CY_pitch_rate        = np.reshape(CY_res,(len_Mach,len_pitch_rate)).T    - CY_alpha_0   
    CZ_pitch_rate        = np.reshape(CZ_res,(len_Mach,len_pitch_rate)).T    - CZ_alpha_0   
    CL_pitch_rate        = np.reshape(CL_res,(len_Mach,len_pitch_rate)).T    - CL_alpha_0   
    CM_pitch_rate        = np.reshape(CM_res,(len_Mach,len_pitch_rate)).T    - CM_alpha_0   
    CN_pitch_rate        = np.reshape(CN_res,(len_Mach,len_pitch_rate)).T    - CN_alpha_0   

    # -------------------------------------------------------               
    # Roll  Rate 
    # -------------------------------------------------------    
    p_s     = np.atleast_2d(np.tile(roll_rate, len_Mach).T.flatten()).T 
    Machs         = np.atleast_2d(np.repeat(Mach,len_roll_rate)).T

    conditions                                      = RCAIDE.Framework.Mission.Common.Results() 
    conditions.freestream.mach_number               = Machs  
    conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12 
    conditions.static_stability.roll_rate           = np.ones_like(Machs)*p_s 
    conditions.freestream.velocity                  = Machs * 343 # speed of sound           
        
    Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)  
        
    Clift_roll_rate     = np.reshape(Clift_res,(len_Mach,len_roll_rate)).T - Clift_alpha_0
    Cdrag_roll_rate     = np.reshape(Cdrag_res,(len_Mach,len_roll_rate)).T - Cdrag_alpha_0
    CX_roll_rate        = np.reshape(CX_res,(len_Mach,len_roll_rate)).T    - CX_alpha_0   
    CY_roll_rate        = np.reshape(CY_res,(len_Mach,len_roll_rate)).T    - CY_alpha_0   
    CZ_roll_rate        = np.reshape(CZ_res,(len_Mach,len_roll_rate)).T    - CZ_alpha_0   
    CL_roll_rate        = np.reshape(CL_res,(len_Mach,len_roll_rate)).T    - CL_alpha_0   
    CM_roll_rate        = np.reshape(CM_res,(len_Mach,len_roll_rate)).T    - CM_alpha_0   
    CN_roll_rate        = np.reshape(CN_res,(len_Mach,len_roll_rate)).T    - CN_alpha_0       

    # -------------------------------------------------------               
    # Yaw Rate 
    # -------------------------------------------------------        
    r_s     = np.atleast_2d(np.tile(yaw_rate, len_Mach).T.flatten()).T 
    Machs         = np.atleast_2d(np.repeat(Mach,len_yaw_rate)).T

    conditions                                      = RCAIDE.Framework.Mission.Common.Results() 
    conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12
    conditions.freestream.mach_number               = Machs 
    conditions.static_stability.yaw_rate            = np.ones_like(Machs)*r_s
    conditions.freestream.velocity                  = Machs * 343 # speed of sound  
    
    Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)
    
    Clift_yaw_rate     = np.reshape(Clift_res,(len_Mach,len_yaw_rate)).T - Clift_alpha_0
    Cdrag_yaw_rate     = np.reshape(Cdrag_res,(len_Mach,len_yaw_rate)).T - Cdrag_alpha_0
    CX_yaw_rate        = np.reshape(CX_res,(len_Mach,len_yaw_rate)).T    - CX_alpha_0   
    CY_yaw_rate        = np.reshape(CY_res,(len_Mach,len_yaw_rate)).T    - CY_alpha_0   
    CZ_yaw_rate        = np.reshape(CZ_res,(len_Mach,len_yaw_rate)).T    - CZ_alpha_0   
    CL_yaw_rate        = np.reshape(CL_res,(len_Mach,len_yaw_rate)).T    - CL_alpha_0   
    CM_yaw_rate        = np.reshape(CM_res,(len_Mach,len_yaw_rate)).T    - CM_alpha_0   
    CN_yaw_rate        = np.reshape(CN_res,(len_Mach,len_yaw_rate)).T    - CN_alpha_0   
        
    # STABILITY COEFFICIENTS 
    training.oswald_efficiency  = oswald_efficiency
    training.Clift_alpha    = Clift_alpha   
    training.Clift_beta     = Clift_beta
                
    training.Clift_u        = Clift_u       
    training.Clift_v        = Clift_v       
    training.Clift_w        = Clift_w       
    training.Clift_p        = Clift_roll_rate       
    training.Clift_q        = Clift_pitch_rate       
    training.Clift_r        = Clift_yaw_rate       
    training.Cdrag_alpha    = Cdrag_alpha   
    training.Cdrag_beta     = Cdrag_beta 
    training.Cdrag_u        = Cdrag_u       
    training.Cdrag_v        = Cdrag_v       
    training.Cdrag_w        = Cdrag_w       
    training.Cdrag_p        = Cdrag_roll_rate        
    training.Cdrag_q        = Cdrag_pitch_rate       
    training.Cdrag_r        = Cdrag_yaw_rate         
    training.CX_alpha       = CX_alpha      
    training.CX_beta        = CX_beta 
                   
    training.CX_u           = CX_u          
    training.CX_v           = CX_v          
    training.CX_w           = CX_w          
    training.CX_p           = CX_roll_rate           
    training.CX_q           = CX_pitch_rate          
    training.CX_r           = CX_yaw_rate            
    training.CY_alpha       = CY_alpha      
    training.CY_beta        = CY_beta
     
                    
    training.CY_u           = CY_u          
    training.CY_v           = CY_v          
    training.CY_w           = CY_w          
    training.CY_p           = CY_roll_rate            
    training.CY_q           = CY_pitch_rate           
    training.CY_r           = CY_yaw_rate             
    training.CZ_alpha       = CZ_alpha      
    training.CZ_beta        = CZ_beta
      
    training.CZ_u           = CZ_u          
    training.CZ_v           = CZ_v          
    training.CZ_w           = CZ_w          
    training.CZ_p           = CZ_roll_rate           
    training.CZ_q           = CZ_pitch_rate          
    training.CZ_r           = CZ_yaw_rate            
    training.CL_alpha       = CL_alpha      
    training.CL_beta        = CL_beta
                
    training.CL_u           = CL_u          
    training.CL_v           = CL_v          
    training.CL_w           = CL_w          
    training.CL_p           = CL_roll_rate           
    training.CL_q           = CL_pitch_rate          
    training.CL_r           = CL_yaw_rate            
    training.CM_alpha       = CM_alpha      
    training.CM_beta        = CM_beta 
                
    training.CM_u           = CM_u          
    training.CM_v           = CM_v          
    training.CM_w           = CM_w          
    training.CM_p           = CM_roll_rate             
    training.CM_q           = CM_pitch_rate            
    training.CM_r           = CM_yaw_rate              
    training.CN_alpha       = CN_alpha      
    training.CN_beta        = CN_beta 
                
    training.CN_u           = CN_u          
    training.CN_v           = CN_v          
    training.CN_w           = CN_w          
    training.CN_p           = CN_roll_rate            
    training.CN_q           = CN_pitch_rate           
    training.CN_r           = CN_yaw_rate
      
            
    # STABILITY DERIVATIVES 
    training.dClift_dalpha = (Clift_alpha[0,:] - Clift_alpha[1,:]) / (AoA[0] - AoA[1])
    training.dClift_dbeta = (Clift_beta[0,:] - Clift_beta[1,:]) / (Beta[0] - Beta[1]) 
    training.dClift_du = (Clift_u[0,:] - Clift_u[1,:]) / (u[0] - u[1])            
    training.dClift_dv = (Clift_v[0,:] - Clift_v[1,:]) / (v[0] - v[1])          
    training.dClift_dw = (Clift_w[0,:] - Clift_w[1,:]) / (w[0] - w[1])         
    training.dClift_dp = (Clift_roll_rate[0,:] - Clift_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])            
    training.dClift_dq = (Clift_pitch_rate[0,:] - Clift_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])        
    training.dClift_dr = (Clift_yaw_rate[0,:] - Clift_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                
    training.dCdrag_dalpha = (Cdrag_alpha[0,:] - Cdrag_alpha[1,:]) / (AoA[0] - AoA[1])    
    training.dCdrag_dbeta = (Cdrag_beta[0,:] - Cdrag_beta[1,:]) / (Beta[0] - Beta[1])
                
    training.dCdrag_du = (Cdrag_u[0,:] - Cdrag_u[1,:]) / (u[0] - u[1])                     
    training.dCdrag_dv = (Cdrag_v[0,:] - Cdrag_v[1,:]) / (v[0] - v[1])                   
    training.dCdrag_dw = (Cdrag_w[0,:] - Cdrag_w[1,:]) / (w[0] - w[1])                  
    training.dCdrag_dp = (Cdrag_roll_rate[0,:] - Cdrag_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])             
    training.dCdrag_dq = (Cdrag_pitch_rate[0,:] - Cdrag_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])         
    training.dCdrag_dr = (Cdrag_yaw_rate[0,:] - Cdrag_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                 
    training.dCX_dalpha = (CX_alpha[0,:] - CX_alpha[1,:]) / (AoA[0] - AoA[1])            
    training.dCX_dbeta = (CX_beta[0,:] - CX_beta[1,:]) / (Beta[0] - Beta[1]) 
                
    training.dCX_du = (CX_u[0,:] - CX_u[1,:]) / (u[0] - u[1])                                 
    training.dCX_dv = (CX_v[0,:] - CX_v[1,:]) / (v[0] - v[1])                               
    training.dCX_dw = (CX_w[0,:] - CX_w[1,:]) / (w[0] - w[1])                              
    training.dCX_dp = (CX_roll_rate[0,:] - CX_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                
    training.dCX_dq = (CX_pitch_rate[0,:] - CX_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])            
    training.dCX_dr = (CX_yaw_rate[0,:] - CX_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                    
    training.dCY_dalpha = (CY_alpha[0,:] - CY_alpha[1,:]) / (AoA[0] - AoA[1])         
    training.dCY_dbeta = (CY_beta[0,:] - CY_beta[1,:]) / (Beta[0] - Beta[1]) 
            
                
    training.dCY_du = (CY_u[0,:] - CY_u[1,:]) / (u[0] - u[1])                                             
    training.dCY_dv = (CY_v[0,:] - CY_v[1,:]) / (v[0] - v[1])                                           
    training.dCY_dw = (CY_w[0,:] - CY_w[1,:]) / (w[0] - w[1])                                          
    training.dCY_dp = (CY_roll_rate[0,:] - CY_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                 
    training.dCY_dq = (CY_pitch_rate[0,:] - CY_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])             
    training.dCY_dr = (CY_yaw_rate[0,:] - CY_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                     
    training.dCZ_dalpha = (CZ_alpha[0,:] - CZ_alpha[1,:]) / (AoA[0] - AoA[1])             
    training.dCZ_dbeta = (CZ_beta[0,:] - CZ_beta[1,:]) / (Beta[0] - Beta[1])
    
                      
    training.dCZ_du = (CZ_u[0,:] - CZ_u[1,:]) / (u[0] - u[1])                                              
    training.dCZ_dv = (CZ_v[0,:] - CZ_v[1,:]) / (v[0] - v[1])                                              
    training.dCZ_dw = (CZ_w[0,:] - CZ_w[1,:]) / (w[0] - w[1])                                              
    training.dCZ_dp = (CZ_roll_rate[0,:] - CZ_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                
    training.dCZ_dq = (CZ_pitch_rate[0,:] - CZ_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])            
    training.dCZ_dr = (CZ_yaw_rate[0,:] - CZ_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                    
    training.dCL_dalpha = (CL_alpha[0,:] - CL_alpha[1,:]) / (AoA[0] - AoA[1])         
    training.dCL_dbeta = (CL_beta[0,:] - CL_beta[1,:]) / (Beta[0] - Beta[1])                
                
                
    training.dCL_du = (CL_u[0,:] - CL_u[1,:]) / (u[0] - u[1])                                              
    training.dCL_dv = (CL_v[0,:] - CL_v[1,:]) / (v[0] - v[1])                                              
    training.dCL_dw = (CL_w[0,:] - CL_w[1,:]) / (w[0] - w[1])                                              
    training.dCL_dp = (CL_roll_rate[0,:] - CL_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                
    training.dCL_dq = (CL_pitch_rate[0,:] - CL_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])            
    training.dCL_dr = (CL_yaw_rate[0,:] - CL_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                    
    training.dCM_dalpha = (CM_alpha[0,:] - CM_alpha[1,:]) / (AoA[0] - AoA[1])          
    training.dCM_dbeta = (CM_beta[0,:] - CM_beta[1,:]) / (Beta[0] - Beta[1])  
                
    training.dCM_du = (CM_u[0,:] - CM_u[1,:]) / (u[0] - u[1])                                               
    training.dCM_dv = (CM_v[0,:] - CM_v[1,:]) / (v[0] - v[1])                                               
    training.dCM_dw = (CM_w[0,:] - CM_w[1,:]) / (w[0] - w[1])                                               
    training.dCM_dp = (CM_roll_rate[0,:] - CM_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                 
    training.dCM_dq = (CM_pitch_rate[0,:] - CM_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])             
    training.dCM_dr = (CM_yaw_rate[0,:] - CM_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                     
    training.dCN_dalpha = (CN_alpha[0,:] - CN_alpha[1,:]) / (AoA[0] - AoA[1])          
    training.dCN_dbeta = (CN_beta[0,:] - CN_beta[1,:]) / (Beta[0] - Beta[1]) 
                     
    training.dCN_du = (CN_u[0,:] - CN_u[1,:]) / (u[0] - u[1])                                               
    training.dCN_dv = (CN_v[0,:] - CN_v[1,:]) / (v[0] - v[1])                                               
    training.dCN_dw = (CN_w[0,:] - CN_w[1,:]) / (w[0] - w[1])                                               
    training.dCN_dp = (CN_roll_rate[0,:] - CN_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                 
    training.dCN_dq = (CN_pitch_rate[0,:] - CN_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])             
    training.dCN_dr = (CN_yaw_rate[0,:] - CN_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])


    '''  for control surfaces, subtract inflence WITHOUT control surface deflected from coefficients WITH control surfaces'''
    

    # --------------------------------------------------------------------------------------------------------------
    # Aileron 
    # --------------------------------------------------------------------------------------------------------------   
    if stability.aileron_flag:  
        for wing in stability.geometry.wings: 
            for control_surface in wing.control_surfaces:  
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Aileron:
                    
                    Clift_d_a      = np.zeros((len_d_a,len_Mach)) 
                    Cdrag_d_a      = np.zeros((len_d_a,len_Mach)) 
                    CX_d_a         = np.zeros((len_d_a,len_Mach)) 
                    CY_d_a         = np.zeros((len_d_a,len_Mach)) 
                    CZ_d_a         = np.zeros((len_d_a,len_Mach)) 
                    CL_d_a         = np.zeros((len_d_a,len_Mach)) 
                    CM_d_a         = np.zeros((len_d_a,len_Mach)) 
                    CN_d_a         = np.zeros((len_d_a,len_Mach))
                
                    for a_i in range(len_d_a):   
                        Delta_a_s                                       = np.atleast_2d(np.tile(delta_a[a_i],len_Mach).T.flatten()).T 
                        Machs                                           = np.atleast_2d(np.repeat(Mach,1)).T         
                        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
                        conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12
                        conditions.freestream.mach_number               = Machs 
                        conditions.control_surfaces.aileron.deflection  = np.ones_like(Machs)*Delta_a_s
                        control_surface.deflection                      = delta_a[a_i]
                        
                        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)   
                        Clift_d_a[a_i,:] = Clift_res[:,0]  - Clift_alpha_0[0,:]
                        Cdrag_d_a[a_i,:] = Cdrag_res[:,0]  - Cdrag_alpha_0[0,:]                                
                        CX_d_a[a_i,:]    = CX_res[:,0]   - CX_alpha_0[0,:]   
                        CY_d_a[a_i,:]    = CY_res[:,0]   - CY_alpha_0[0,:]  
                        CZ_d_a[a_i,:]    = CZ_res[:,0]   - CZ_alpha_0[0,:]  
                        CL_d_a[a_i,:]    = CL_res[:,0]   - CL_alpha_0[0,:]  
                        CM_d_a[a_i,:]    = CM_res[:,0]   - CM_alpha_0[0,:]  
                        CN_d_a[a_i,:]    = CN_res[:,0]   - CN_alpha_0[0,:]      

     
        training.Clift_delta_a  = Clift_d_a
        training.Cdrag_delta_a  = Cdrag_d_a 
        training.CX_delta_a     = CX_d_a 
        training.CY_delta_a     = CY_d_a 
        training.CZ_delta_a     = CZ_d_a 
        training.CL_delta_a     = CL_d_a 
        training.CM_delta_a     = CM_d_a 
        training.CN_delta_a     = CN_d_a
        
        training.dClift_ddelta_a = (Clift_d_a[0,:] - Clift_d_a[1,:]) / (delta_a[0] - delta_a[1])
        training.dCdrag_ddelta_a = (Cdrag_d_a[0,:] - Cdrag_d_a[1,:]) / (delta_a[0] - delta_a[1]) 
        training.dCX_ddelta_a = (CX_d_a[0,:] - CX_d_a[1,:]) / (delta_a[0] - delta_a[1]) 
        training.dCY_ddelta_a = (CY_d_a[0,:] - CY_d_a[1,:]) / (delta_a[0] - delta_a[1]) 
        training.dCZ_ddelta_a = (CZ_d_a[0,:] - CZ_d_a[1,:]) / (delta_a[0] - delta_a[1]) 
        training.dCL_ddelta_a = (CL_d_a[0,:] - CL_d_a[1,:]) / (delta_a[0] - delta_a[1]) 
        training.dCM_ddelta_a = (CM_d_a[0,:] - CM_d_a[1,:]) / (delta_a[0] - delta_a[1]) 
        training.dCN_ddelta_a = (CN_d_a[0,:] - CN_d_a[1,:]) / (delta_a[0] - delta_a[1])
    
    # --------------------------------------------------------------------------------------------------------------
    # Elevator 
    # -------------------------------------------------------------------------------------------------------------- 
    if stability.elevator_flag: 
        for wing in stability.geometry.wings: 
            for control_surface in wing.control_surfaces:  
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Elevator: 
                
                    Clift_d_e      = np.zeros((len_d_e,len_Mach)) 
                    Cdrag_d_e      = np.zeros((len_d_e,len_Mach)) 
                    CX_d_e         = np.zeros((len_d_e,len_Mach)) 
                    CY_d_e         = np.zeros((len_d_e,len_Mach)) 
                    CZ_d_e         = np.zeros((len_d_e,len_Mach)) 
                    CL_d_e         = np.zeros((len_d_e,len_Mach)) 
                    CM_d_e         = np.zeros((len_d_e,len_Mach)) 
                    CN_d_e         = np.zeros((len_d_e,len_Mach))
                
                    for e_i in range(len_d_e):   
                        Delta_e_s                                       = np.atleast_2d(np.tile(delta_e[e_i],len_Mach).T.flatten()).T 
                        Machs                                           = np.atleast_2d(np.repeat(Mach,1)).T         
                        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
                        conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12
                        conditions.freestream.mach_number               = Machs 
                        conditions.control_surfaces.elevator.deflection = np.ones_like(Machs)*Delta_e_s
                        control_surface.deflection                      = delta_e[e_i]
                        
                        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)   
                        Clift_d_e[e_i,:] = Clift_res[:,0]  - Clift_alpha_0[0,:]
                        Cdrag_d_e[e_i,:] = Cdrag_res[:,0]  - Cdrag_alpha_0[0,:]                                
                        CX_d_e[e_i,:]    = CX_res[:,0]   - CX_alpha_0[0,:]   
                        CY_d_e[e_i,:]    = CY_res[:,0]   - CY_alpha_0[0,:]  
                        CZ_d_e[e_i,:]    = CZ_res[:,0]   - CZ_alpha_0[0,:]  
                        CL_d_e[e_i,:]    = CL_res[:,0]   - CL_alpha_0[0,:]  
                        CM_d_e[e_i,:]    = CM_res[:,0]   - CM_alpha_0[0,:]  
                        CN_d_e[e_i,:]    = CN_res[:,0]   - CN_alpha_0[0,:]                   

                    
        training.Clift_delta_e  = Clift_d_e
        training.Cdrag_delta_e  = Cdrag_d_e  
        training.CX_delta_e  = CX_d_e   
        training.CY_delta_e  = CY_d_e   
        training.CZ_delta_e  = CZ_d_e  
        training.CL_delta_e  = CL_d_e  
        training.CM_delta_e  = CM_d_e  
        training.CN_delta_e  = CN_d_e
        
        training.dClift_ddelta_e = (Clift_d_e[0,:] - Clift_d_e[1,:]) / (delta_e[0] - delta_e[1])
        training.dCdrag_ddelta_e = (Cdrag_d_e[0,:] - Cdrag_d_e[1,:]) / (delta_e[0] - delta_e[1])  
        training.dCX_ddelta_e = (CX_d_e[0,:] - CX_d_e[1,:]) / (delta_e[0] - delta_e[1])  
        training.dCY_ddelta_e = (CY_d_e[0,:] - CY_d_e[1,:]) / (delta_e[0] - delta_e[1]) 
        training.dCZ_ddelta_e = (CZ_d_e[0,:] - CZ_d_e[1,:]) / (delta_e[0] - delta_e[1]) 
        training.dCL_ddelta_e = (CL_d_e[0,:] - CL_d_e[1,:]) / (delta_e[0] - delta_e[1])  
        training.dCM_ddelta_e = (CM_d_e[0,:] - CM_d_e[1,:]) / (delta_e[0] - delta_e[1])  
        training.dCN_ddelta_e = (CN_d_e[0,:] - CN_d_e[1,:]) / (delta_e[0] - delta_e[1])
        
    # --------------------------------------------------------------------------------------------------------------
    # Rudder 
    # -------------------------------------------------------------------------------------------------------------- 
    if stability.rudder_flag:
        for wing in stability.geometry.wings: 
            for control_surface in wing.control_surfaces:  
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Rudder: 
                    Clift_d_r      = np.zeros((len_d_r,len_Mach)) 
                    Cdrag_d_r      = np.zeros((len_d_r,len_Mach)) 
                    CX_d_r         = np.zeros((len_d_r,len_Mach)) 
                    CY_d_r         = np.zeros((len_d_r,len_Mach)) 
                    CZ_d_r         = np.zeros((len_d_r,len_Mach)) 
                    CL_d_r         = np.zeros((len_d_r,len_Mach)) 
                    CM_d_r         = np.zeros((len_d_r,len_Mach)) 
                    CN_d_r         = np.zeros((len_d_r,len_Mach))
                
                    for r_i in range(len_d_r):   
                        Delta_r_s                                       = np.atleast_2d(np.tile(delta_r[r_i],len_Mach).T.flatten()).T 
                        Machs                                           = np.atleast_2d(np.repeat(Mach,1)).T         
                        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
                        conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12
                        conditions.freestream.mach_number               = Machs 
                        conditions.control_surfaces.rudder.deflection  = np.ones_like(Machs)*Delta_r_s
                        control_surface.deflection                      = delta_r[r_i]
                        
                        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)   
                        Clift_d_r[r_i,:] = Clift_res[:,0]  - Clift_alpha_0[0,:]
                        Cdrag_d_r[r_i,:] = Cdrag_res[:,0]  - Cdrag_alpha_0[0,:]                                
                        CX_d_r[r_i,:]    = CX_res[:,0]   - CX_alpha_0[0,:]   
                        CY_d_r[r_i,:]    = CY_res[:,0]   - CY_alpha_0[0,:]  
                        CZ_d_r[r_i,:]    = CZ_res[:,0]   - CZ_alpha_0[0,:]  
                        CL_d_r[r_i,:]    = CL_res[:,0]   - CL_alpha_0[0,:]  
                        CM_d_r[r_i,:]    = CM_res[:,0]   - CM_alpha_0[0,:]  
                        CN_d_r[r_i,:]    = CN_res[:,0]   - CN_alpha_0[0,:]
                         
 
        training.Clift_delta_r  = Clift_d_r
        training.Cdrag_delta_r  = Cdrag_d_r     
        training.CX_delta_r  = CX_d_r   
        training.CY_delta_r  = CY_d_r 
        training.CZ_delta_r  = CZ_d_r 
        training.CL_delta_r  = CL_d_r  
        training.CM_delta_r  = CM_d_r                   
        training.CN_delta_r  = CN_d_r    
        training.dClift_ddelta_r = (Clift_d_r[0,:] - Clift_d_r[1,:]) / (delta_r[0] - delta_r[1])
        training.dCdrag_ddelta_r = (Cdrag_d_r[0,:] - Cdrag_d_r[1,:]) / (delta_r[0] - delta_r[1])  
        training.dCX_ddelta_r = (CX_d_r[0,:] - CX_d_r[1,:]) / (delta_r[0] - delta_r[1])   
        training.dCY_ddelta_r = (CY_d_r[0,:] - CY_d_r[1,:]) / (delta_r[0] - delta_r[1]) 
        training.dCZ_ddelta_r = (CZ_d_r[0,:] - CZ_d_r[1,:]) / (delta_r[0] - delta_r[1])  
        training.dCL_ddelta_r = (CL_d_r[0,:] - CL_d_r[1,:]) / (delta_r[0] - delta_r[1])  
        training.dCM_ddelta_r = (CM_d_r[0,:] - CM_d_r[1,:]) / (delta_r[0] - delta_r[1]) 
        training.dCN_ddelta_r = (CN_d_r[0,:] - CN_d_r[1,:]) / (delta_r[0] - delta_r[1])  
                        
    # --------------------------------------------------------------------------------------------------------------
    # Flap
    # -------------------------------------------------------------------------------------------------------------- 
    if stability.flap_flag:
        for wing in stability.geometry.wings: 
            for control_surface in wing.control_surfaces:  
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Flap:
                    Clift_d_f      = np.zeros((len_d_f,len_Mach)) 
                    Cdrag_d_f      = np.zeros((len_d_f,len_Mach)) 
                    CX_d_f         = np.zeros((len_d_f,len_Mach)) 
                    CY_d_f         = np.zeros((len_d_f,len_Mach)) 
                    CZ_d_f         = np.zeros((len_d_f,len_Mach)) 
                    CL_d_f         = np.zeros((len_d_f,len_Mach)) 
                    CM_d_f         = np.zeros((len_d_f,len_Mach)) 
                    CN_d_f         = np.zeros((len_d_f,len_Mach))
                
                    for f_i in range(len_d_f):   
                        Delta_f_s                                       = np.atleast_2d(np.tile(delta_f[f_i],len_Mach).T.flatten()).T 
                        Machs                                           = np.atleast_2d(np.repeat(Mach,1)).T         
                        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
                        conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12
                        conditions.freestream.mach_number               = Machs 
                        conditions.control_surfaces.flap.deflection     = np.ones_like(Machs)*Delta_f_s
                        control_surface.deflection                      = delta_f[f_i]
                        
                        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)   
                        Clift_d_f[f_i,:] = Clift_res[:,0]  - Clift_alpha_0[0,:]
                        Cdrag_d_f[f_i,:] = Cdrag_res[:,0]  - Cdrag_alpha_0[0,:]                                
                        CX_d_f[f_i,:]    = CX_res[:,0]   - CX_alpha_0[0,:]   
                        CY_d_f[f_i,:]    = CY_res[:,0]   - CY_alpha_0[0,:]  
                        CZ_d_f[f_i,:]    = CZ_res[:,0]   - CZ_alpha_0[0,:]  
                        CL_d_f[f_i,:]    = CL_res[:,0]   - CL_alpha_0[0,:]  
                        CM_d_f[f_i,:]    = CM_res[:,0]   - CM_alpha_0[0,:]  
                        CN_d_f[f_i,:]    = CN_res[:,0]   - CN_alpha_0[0,:]         
    
        training.Clift_delta_f  = Clift_d_f    
        training.Cdrag_delta_f  = Cdrag_d_f    
        training.CX_delta_f     = CX_d_f  
        training.CY_delta_f     = CY_d_f  
        training.CZ_delta_f     = CZ_d_f  
        training.CL_delta_f     = CL_d_f  
        training.CM_delta_f     = CM_d_f                   
        training.CN_delta_f     = CN_d_f 
        training.dClift_ddelta_f = (Clift_d_f[0,:] - Clift_d_f[1,:]) / (delta_f[0] - delta_f[1])
        training.dCdrag_ddelta_f = (Cdrag_d_f[0,:] - Cdrag_d_f[1,:]) / (delta_f[0] - delta_f[1])  
        training.dCX_ddelta_f    = (CX_d_f[0,:] - CX_d_f[1,:]) / (delta_f[0] - delta_f[1])  
        training.dCY_ddelta_f    = (CY_d_f[0,:] - CY_d_f[1,:]) / (delta_f[0] - delta_f[1]) 
        training.dCZ_ddelta_f    = (CZ_d_f[0,:] - CZ_d_f[1,:]) / (delta_f[0] - delta_f[1])   
        training.dCL_ddelta_f    = (CL_d_f[0,:] - CL_d_f[1,:]) / (delta_f[0] - delta_f[1])  
        training.dCM_ddelta_f    = (CM_d_f[0,:] - CM_d_f[1,:]) / (delta_f[0] - delta_f[1])  
        training.dCN_ddelta_f    = (CN_d_f[0,:] - CN_d_f[1,:]) / (delta_f[0] - delta_f[1])   
                    
    # --------------------------------------------------------------------------------------------------------------
    # Slat
    # -------------------------------------------------------------------------------------------------------------- 
    if stability.slat_flag:
        for wing in stability.geometry.wings: 
            for control_surface in wing.control_surfaces:  
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Slat:
                    
                    Clift_d_s      = np.zeros((len_d_s,len_Mach)) 
                    Cdrag_d_s      = np.zeros((len_d_s,len_Mach)) 
                    CX_d_s         = np.zeros((len_d_s,len_Mach)) 
                    CY_d_s         = np.zeros((len_d_s,len_Mach)) 
                    CZ_d_s         = np.zeros((len_d_s,len_Mach)) 
                    CL_d_s         = np.zeros((len_d_s,len_Mach)) 
                    CM_d_s         = np.zeros((len_d_s,len_Mach)) 
                    CN_d_s         = np.zeros((len_d_s,len_Mach))
                
                    for s_i in range(len_d_s):   
                        Delta_s_s                                       = np.atleast_2d(np.tile(delta_f[f_i],len_Mach).T.flatten()).T 
                        Machs                                           = np.atleast_2d(np.repeat(Mach,1)).T         
                        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
                        conditions.aerodynamics.angles.alpha            = np.ones_like(Machs) *1E-12
                        conditions.freestream.mach_number               = Machs 
                        conditions.control_surfaces.flat.deflection     = np.ones_like(Machs)*Delta_s_s
                        control_surface.deflection                      = delta_s[s_i]
                        
                        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res ,_,_,_,_,_,_= evaluate_VLM(conditions,settings,geometry)   
                        Clift_d_f[s_i,:] = Clift_res[:,0]  - Clift_alpha_0[0,:]
                        Cdrag_d_f[s_i,:] = Cdrag_res[:,0]  - Cdrag_alpha_0[0,:]                                
                        CX_d_s[s_i,:]    = CX_res[:,0]   - CX_alpha_0[0,:]   
                        CY_d_s[s_i,:]    = CY_res[:,0]   - CY_alpha_0[0,:]  
                        CZ_d_s[s_i,:]    = CZ_res[:,0]   - CZ_alpha_0[0,:]  
                        CL_d_s[s_i,:]    = CL_res[:,0]   - CL_alpha_0[0,:]  
                        CM_d_s[s_i,:]    = CM_res[:,0]   - CM_alpha_0[0,:]  
                        CN_d_s[s_i,:]    = CN_res[:,0]   - CN_alpha_0[0,:]  

        training.Clift_delta_s  = Clift_d_s
        training.Cdrag_delta_s  = Cdrag_d_s
        training.CX_delta_s  = CX_d_s
        training.CY_delta_s  = CY_d_s 
        training.CZ_delta_s  = CZ_d_s 
        training.CL_delta_s  = CL_d_s 
        training.CM_delta_s  = CM_d_s
        training.CN_delta_s  = CN_d_s  
        training.dClift_ddelta_s = (Clift_d_s[0,:] - Clift_d_s[1,:]) / (delta_s[0] - delta_s[1])
        training.dCdrag_ddelta_s = (Cdrag_d_s[0,:] - Cdrag_d_s[1,:]) / (delta_s[0] - delta_s[1])
        training.dCX_ddelta_s = (CX_d_s[0,:] - CX_d_s[1,:]) / (delta_s[0] - delta_s[1])
        training.dCY_ddelta_s = (CY_d_s[0,:] - CY_d_s[1,:]) / (delta_s[0] - delta_s[1])
        training.dCZ_ddelta_s = (CZ_d_s[0,:] - CZ_d_s[1,:]) / (delta_s[0] - delta_s[1]) 
        training.dCL_ddelta_s = (CL_d_s[0,:] - CL_d_s[1,:]) / (delta_s[0] - delta_s[1]) 
        training.dCM_ddelta_s = (CM_d_s[0,:] - CM_d_s[1,:]) / (delta_s[0] - delta_s[1])  
        training.dCN_ddelta_s = (CN_d_s[0,:] - CN_d_s[1,:]) / (delta_s[0] - delta_s[1])  
    training.NP            = 0  
    
    return
        
def build_surrogate(stability):
    """Build a surrogate using sample evaluation results.
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        stability       : VLM analysis          [unitless] 
        
    Returns: 
        None  
    """        
    # unpack data
    surrogates     = stability.surrogates
    training       = stability.training  
    AoA_data       = stability.training.angle_of_attack 
    mach_data      = stability.training.Mach                 
    Beta_data      = stability.training.sideslip_angle  
    u_data         = stability.training.u
    v_data         = stability.training.v
    w_data         = stability.training.w
    p_data         = stability.training.roll_rate
    q_data         = stability.training.pitch_rate
    r_data         = stability.training.yaw_rate
    aileron_data   = stability.training.aileron_deflection           
    elevator_data  = stability.training.elevator_deflection          
    rudder_data    = stability.training.rudder_deflection            
    flap_data      = stability.training.flap_deflection              
    slat_data      = stability.training.slat_deflection   
    
    # Pack the outputs 
    surrogates.oswald_efficiency = RegularGridInterpolator((AoA_data ,mach_data),training.oswald_efficiency  ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Clift_alpha       = RegularGridInterpolator((AoA_data ,mach_data),training.Clift_alpha        ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Clift_beta        = RegularGridInterpolator((Beta_data,mach_data),training.Clift_beta         ,method = 'linear',   bounds_error=False, fill_value=None) 
    surrogates.Clift_u           = RegularGridInterpolator((u_data,mach_data),training.Clift_u               ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Clift_v           = RegularGridInterpolator((v_data,mach_data),training.Clift_v               ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Clift_w           = RegularGridInterpolator((w_data,mach_data),training.Clift_w               ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Clift_p           = RegularGridInterpolator((p_data,mach_data),training.Clift_p               ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Clift_q           = RegularGridInterpolator((q_data,mach_data),training.Clift_q               ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Clift_r           = RegularGridInterpolator((r_data,mach_data),training.Clift_r               ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Cdrag_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_alpha         ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Cdrag_beta        = RegularGridInterpolator((Beta_data,mach_data),training.Cdrag_beta         ,method = 'linear',   bounds_error=False, fill_value=None)
     
              
    surrogates.Cdrag_u        = RegularGridInterpolator((u_data,mach_data),training.Cdrag_u        ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Cdrag_v        = RegularGridInterpolator((v_data,mach_data),training.Cdrag_v        ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Cdrag_w        = RegularGridInterpolator((w_data,mach_data),training.Cdrag_w        ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Cdrag_p        = RegularGridInterpolator((p_data,mach_data),training.Cdrag_p        ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Cdrag_q        = RegularGridInterpolator((q_data,mach_data),training.Cdrag_q        ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.Cdrag_r        = RegularGridInterpolator((r_data,mach_data),training.Cdrag_r        ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CX_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CX_alpha     ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CX_beta        = RegularGridInterpolator((Beta_data,mach_data),training.CX_beta     ,method = 'linear',   bounds_error=False, fill_value=None) 
     
                    
    surrogates.CX_u           = RegularGridInterpolator((u_data,mach_data),training.CX_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CX_v           = RegularGridInterpolator((v_data,mach_data),training.CX_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CX_w           = RegularGridInterpolator((w_data,mach_data),training.CX_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CX_p           = RegularGridInterpolator((p_data,mach_data),training.CX_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CX_q           = RegularGridInterpolator((q_data,mach_data),training.CX_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CX_r           = RegularGridInterpolator((r_data,mach_data),training.CX_r           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CY_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CY_alpha     ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CY_beta        = RegularGridInterpolator((Beta_data,mach_data),training.CY_beta     ,method = 'linear',   bounds_error=False, fill_value=None)
     
              
    surrogates.CY_u           = RegularGridInterpolator((u_data,mach_data),training.CY_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CY_v           = RegularGridInterpolator((v_data,mach_data),training.CY_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CY_w           = RegularGridInterpolator((w_data,mach_data),training.CY_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CY_p           = RegularGridInterpolator((p_data,mach_data),training.CY_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CY_q           = RegularGridInterpolator((q_data,mach_data),training.CY_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CY_r           = RegularGridInterpolator((r_data,mach_data),training.CY_r           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CZ_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CZ_alpha     ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CZ_beta        = RegularGridInterpolator((Beta_data,mach_data),training.CZ_beta     ,method = 'linear',   bounds_error=False, fill_value=None)
     
                
    surrogates.CZ_u           = RegularGridInterpolator((u_data,mach_data),training.CZ_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CZ_v           = RegularGridInterpolator((v_data,mach_data),training.CZ_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CZ_w           = RegularGridInterpolator((w_data,mach_data),training.CZ_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CZ_p           = RegularGridInterpolator((p_data,mach_data),training.CZ_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CZ_q           = RegularGridInterpolator((q_data,mach_data),training.CZ_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CZ_r           = RegularGridInterpolator((r_data,mach_data),training.CZ_r           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CL_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CL_alpha     ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CL_beta        = RegularGridInterpolator((Beta_data,mach_data),training.CL_beta     ,method = 'linear',   bounds_error=False, fill_value=None)
     
               
    surrogates.CL_u           = RegularGridInterpolator((u_data,mach_data),training.CL_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CL_v           = RegularGridInterpolator((v_data,mach_data),training.CL_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CL_w           = RegularGridInterpolator((w_data,mach_data),training.CL_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CL_p           = RegularGridInterpolator((p_data,mach_data),training.CL_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CL_q           = RegularGridInterpolator((q_data,mach_data),training.CL_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CL_r           = RegularGridInterpolator((r_data,mach_data),training.CL_r           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CM_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CM_alpha     ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CM_beta        = RegularGridInterpolator((Beta_data,mach_data),training.CM_beta     ,method = 'linear',   bounds_error=False, fill_value=None)
    
    surrogates.CM_u           = RegularGridInterpolator((u_data,mach_data),training.CM_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CM_v           = RegularGridInterpolator((v_data,mach_data),training.CM_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CM_w           = RegularGridInterpolator((w_data,mach_data),training.CM_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CM_p           = RegularGridInterpolator((p_data,mach_data),training.CM_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CM_q           = RegularGridInterpolator((q_data,mach_data),training.CM_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CM_r           = RegularGridInterpolator((r_data,mach_data),training.CM_r           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CN_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CN_alpha     ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CN_beta        = RegularGridInterpolator((Beta_data,mach_data),training.CN_beta     ,method = 'linear',   bounds_error=False, fill_value=None)
             
    surrogates.CN_u           = RegularGridInterpolator((u_data,mach_data),training.CN_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CN_v           = RegularGridInterpolator((v_data,mach_data),training.CN_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CN_w           = RegularGridInterpolator((w_data,mach_data),training.CN_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CN_p           = RegularGridInterpolator((p_data,mach_data),training.CN_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CN_q           = RegularGridInterpolator((q_data,mach_data),training.CN_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.CN_r           = RegularGridInterpolator((r_data,mach_data),training.CN_r           ,method = 'linear',   bounds_error=False, fill_value=None)
    
    surrogates.dClift_dalpha    = interpolate.interp1d(mach_data,training.dClift_dalpha    ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dClift_dbeta     = interpolate.interp1d(mach_data,training.dClift_dbeta     ,kind = 'linear',   bounds_error=False, fill_value=None) 
    surrogates.dClift_du        = interpolate.interp1d(mach_data,training.dClift_du        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dClift_dv        = interpolate.interp1d(mach_data,training.dClift_dv        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dClift_dw        = interpolate.interp1d(mach_data,training.dClift_dw        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dClift_dp        = interpolate.interp1d(mach_data,training.dClift_dp        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dClift_dq        = interpolate.interp1d(mach_data,training.dClift_dq        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dClift_dr        = interpolate.interp1d(mach_data,training.dClift_dr        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCdrag_dalpha    = interpolate.interp1d(mach_data,training.dCdrag_dalpha    ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCdrag_dbeta     = interpolate.interp1d(mach_data,training.dCdrag_dbeta     ,kind = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.dCdrag_du        = interpolate.interp1d(mach_data,training.dCdrag_du        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCdrag_dv        = interpolate.interp1d(mach_data,training.dCdrag_dv        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCdrag_dw        = interpolate.interp1d(mach_data,training.dCdrag_dw        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCdrag_dp        = interpolate.interp1d(mach_data,training.dCdrag_dp        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCdrag_dq        = interpolate.interp1d(mach_data,training.dCdrag_dq        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCdrag_dr        = interpolate.interp1d(mach_data,training.dCdrag_dr        ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCX_dalpha       = interpolate.interp1d(mach_data,training.dCX_dalpha       ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCX_dbeta        = interpolate.interp1d(mach_data,training.dCX_dbeta        ,kind = 'linear',   bounds_error=False, fill_value=None)  
    surrogates.dCX_du           = interpolate.interp1d(mach_data,training.dCX_du           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCX_dv           = interpolate.interp1d(mach_data,training.dCX_dv           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCX_dw           = interpolate.interp1d(mach_data,training.dCX_dw           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCX_dp           = interpolate.interp1d(mach_data,training.dCX_dp           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCX_dq           = interpolate.interp1d(mach_data,training.dCX_dq           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCX_dr           = interpolate.interp1d(mach_data,training.dCX_dr           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCY_dalpha       = interpolate.interp1d(mach_data,training.dCY_dalpha       ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCY_dbeta        = interpolate.interp1d(mach_data,training.dCY_dbeta        ,kind = 'linear',   bounds_error=False, fill_value=None)  
    surrogates.dCY_du           = interpolate.interp1d(mach_data,training.dCY_du           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCY_dv           = interpolate.interp1d(mach_data,training.dCY_dv           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCY_dw           = interpolate.interp1d(mach_data,training.dCY_dw           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCY_dp           = interpolate.interp1d(mach_data,training.dCY_dp           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCY_dq           = interpolate.interp1d(mach_data,training.dCY_dq           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCY_dr           = interpolate.interp1d(mach_data,training.dCY_dr           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCZ_dalpha       = interpolate.interp1d(mach_data,training.dCZ_dalpha       ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCZ_dbeta        = interpolate.interp1d(mach_data,training.dCZ_dbeta        ,kind = 'linear',   bounds_error=False, fill_value=None)  
    surrogates.dCZ_du           = interpolate.interp1d(mach_data,training.dCZ_du           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCZ_dv           = interpolate.interp1d(mach_data,training.dCZ_dv           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCZ_dw           = interpolate.interp1d(mach_data,training.dCZ_dw           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCZ_dp           = interpolate.interp1d(mach_data,training.dCZ_dp           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCZ_dq           = interpolate.interp1d(mach_data,training.dCZ_dq           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCZ_dr           = interpolate.interp1d(mach_data,training.dCZ_dr           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCL_dalpha       = interpolate.interp1d(mach_data,training.dCL_dalpha       ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCL_dbeta        = interpolate.interp1d(mach_data,training.dCL_dbeta        ,kind = 'linear',   bounds_error=False, fill_value=None)  
    surrogates.dCL_du           = interpolate.interp1d(mach_data,training.dCL_du           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCL_dv           = interpolate.interp1d(mach_data,training.dCL_dv           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCL_dw           = interpolate.interp1d(mach_data,training.dCL_dw           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCL_dp           = interpolate.interp1d(mach_data,training.dCL_dp           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCL_dq           = interpolate.interp1d(mach_data,training.dCL_dq           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCL_dr           = interpolate.interp1d(mach_data,training.dCL_dr           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCM_dalpha       = interpolate.interp1d(mach_data,training.dCM_dalpha       ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCM_dbeta        = interpolate.interp1d(mach_data,training.dCM_dbeta        ,kind = 'linear',   bounds_error=False, fill_value=None)  
    surrogates.dCM_du           = interpolate.interp1d(mach_data,training.dCM_du           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCM_dv           = interpolate.interp1d(mach_data,training.dCM_dv           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCM_dw           = interpolate.interp1d(mach_data,training.dCM_dw           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCM_dp           = interpolate.interp1d(mach_data,training.dCM_dp           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCM_dq           = interpolate.interp1d(mach_data,training.dCM_dq           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCM_dr           = interpolate.interp1d(mach_data,training.dCM_dr           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCN_dalpha       = interpolate.interp1d(mach_data,training.dCN_dalpha       ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCN_dbeta        = interpolate.interp1d(mach_data,training.dCN_dbeta        ,kind = 'linear',   bounds_error=False, fill_value=None)  
    surrogates.dCN_du           = interpolate.interp1d(mach_data,training.dCN_du           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCN_dv           = interpolate.interp1d(mach_data,training.dCN_dv           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCN_dw           = interpolate.interp1d(mach_data,training.dCN_dw           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCN_dp           = interpolate.interp1d(mach_data,training.dCN_dp           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCN_dq           = interpolate.interp1d(mach_data,training.dCN_dq           ,kind = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.dCN_dr           = interpolate.interp1d(mach_data,training.dCN_dr           ,kind = 'linear',   bounds_error=False, fill_value=None)
   

    if stability.aileron_flag: 
        surrogates.Clift_delta_a    = RegularGridInterpolator((aileron_data,mach_data),training.Clift_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.Cdrag_delta_a    = RegularGridInterpolator((aileron_data,mach_data),training.Cdrag_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CX_delta_a       = RegularGridInterpolator((aileron_data,mach_data),training.CX_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CY_delta_a       = RegularGridInterpolator((aileron_data,mach_data),training.CY_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CZ_delta_a       = RegularGridInterpolator((aileron_data,mach_data),training.CZ_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CL_delta_a       = RegularGridInterpolator((aileron_data,mach_data),training.CL_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CM_delta_a       = RegularGridInterpolator((aileron_data,mach_data),training.CM_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CN_delta_a       = RegularGridInterpolator((aileron_data,mach_data),training.CN_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dClift_ddelta_a  = interpolate.interp1d(mach_data,training.dClift_ddelta_a     , kind = 'linear',   bounds_error=False, fill_value=None)
        surrogates.dCdrag_ddelta_a  = interpolate.interp1d(mach_data,training.dCdrag_ddelta_a     , kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCX_ddelta_a     = interpolate.interp1d(mach_data,training.dCX_ddelta_a        , kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCY_ddelta_a     = interpolate.interp1d(mach_data,training.dCY_ddelta_a        , kind = 'linear',   bounds_error=False, fill_value=None)  
        surrogates.dCZ_ddelta_a     = interpolate.interp1d(mach_data,training.dCZ_ddelta_a        , kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCL_ddelta_a     = interpolate.interp1d(mach_data,training.dCL_ddelta_a        , kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCM_ddelta_a     = interpolate.interp1d(mach_data,training.dCM_ddelta_a        , kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCN_ddelta_a     = interpolate.interp1d(mach_data,training.dCN_ddelta_a        , kind = 'linear',   bounds_error=False, fill_value=None)             
    
    if stability.elevator_flag: 
        surrogates.Clift_delta_e    = RegularGridInterpolator((elevator_data,mach_data),training.Clift_delta_e  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.Cdrag_delta_e    = RegularGridInterpolator((elevator_data,mach_data),training.Cdrag_delta_e  ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CX_delta_e       = RegularGridInterpolator((elevator_data,mach_data),training.CX_delta_e  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CY_delta_e       = RegularGridInterpolator((elevator_data,mach_data),training.CY_delta_e  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CZ_delta_e       = RegularGridInterpolator((elevator_data,mach_data),training.CZ_delta_e  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CL_delta_e       = RegularGridInterpolator((elevator_data,mach_data),training.CL_delta_e  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CM_delta_e       = RegularGridInterpolator((elevator_data,mach_data),training.CM_delta_e  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CN_delta_e       = RegularGridInterpolator((elevator_data,mach_data),training.CN_delta_e  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dClift_ddelta_e  = interpolate.interp1d(mach_data,training.dClift_ddelta_e  ,kind = 'linear',   bounds_error=False, fill_value=None)
        surrogates.dCdrag_ddelta_e  = interpolate.interp1d(mach_data,training.dCdrag_ddelta_e  ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCX_ddelta_e     = interpolate.interp1d(mach_data,training.dCX_ddelta_e     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCY_ddelta_e     = interpolate.interp1d(mach_data,training.dCY_ddelta_e     ,kind = 'linear',   bounds_error=False, fill_value=None)  
        surrogates.dCZ_ddelta_e     = interpolate.interp1d(mach_data,training.dCZ_ddelta_e     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCL_ddelta_e     = interpolate.interp1d(mach_data,training.dCL_ddelta_e     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCM_ddelta_e     = interpolate.interp1d(mach_data,training.dCM_ddelta_e     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCN_ddelta_e     = interpolate.interp1d(mach_data,training.dCN_ddelta_e     ,kind = 'linear',   bounds_error=False, fill_value=None)   
    
    
    if stability.rudder_flag: 
        surrogates.Clift_delta_r    = RegularGridInterpolator((rudder_data,mach_data),training.Clift_delta_r  ,method = 'linear',   bounds_error=False, fill_value=None)  
        surrogates.Cdrag_delta_r    = RegularGridInterpolator((rudder_data,mach_data),training.Cdrag_delta_r  ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CX_delta_r       = RegularGridInterpolator((rudder_data,mach_data),training.CX_delta_r  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CY_delta_r       = RegularGridInterpolator((rudder_data,mach_data),training.CY_delta_r  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CZ_delta_r       = RegularGridInterpolator((rudder_data,mach_data),training.CZ_delta_r  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CL_delta_r       = RegularGridInterpolator((rudder_data,mach_data),training.CL_delta_r  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CM_delta_r       = RegularGridInterpolator((rudder_data,mach_data),training.CM_delta_r  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CN_delta_r       = RegularGridInterpolator((rudder_data,mach_data),training.CN_delta_r  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dClift_ddelta_r  = interpolate.interp1d(mach_data,training.dClift_ddelta_r    ,kind = 'linear',   bounds_error=False, fill_value=None)
        surrogates.dCdrag_ddelta_r  = interpolate.interp1d(mach_data,training.dCdrag_ddelta_r    ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCX_ddelta_r     = interpolate.interp1d(mach_data,training.dCX_ddelta_r       ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCY_ddelta_r     = interpolate.interp1d(mach_data,training.dCY_ddelta_r       ,kind = 'linear',   bounds_error=False, fill_value=None)  
        surrogates.dCZ_ddelta_r     = interpolate.interp1d(mach_data,training.dCZ_ddelta_r       ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCL_ddelta_r     = interpolate.interp1d(mach_data,training.dCL_ddelta_r       ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCM_ddelta_r     = interpolate.interp1d(mach_data,training.dCM_ddelta_r       ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCN_ddelta_r     = interpolate.interp1d(mach_data,training.dCN_ddelta_r       ,kind = 'linear',   bounds_error=False, fill_value=None)   
    
    if stability.flap_flag:
        surrogates.Clift_delta_f    = RegularGridInterpolator((flap_data,mach_data),training.Clift_delta_f  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.Cdrag_delta_f    = RegularGridInterpolator((flap_data,mach_data),training.Cdrag_delta_f  ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CX_delta_f       = RegularGridInterpolator((flap_data,mach_data),training.CX_delta_f  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CY_delta_f       = RegularGridInterpolator((flap_data,mach_data),training.CY_delta_f  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CZ_delta_f       = RegularGridInterpolator((flap_data,mach_data),training.CZ_delta_f  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CL_delta_f       = RegularGridInterpolator((flap_data,mach_data),training.CL_delta_f  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CM_delta_f       = RegularGridInterpolator((flap_data,mach_data),training.CM_delta_f  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CN_delta_f       = RegularGridInterpolator((flap_data,mach_data),training.CN_delta_f  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dClift_ddelta_f  = interpolate.interp1d(mach_data,training.dClift_ddelta_f  ,kind = 'linear',   bounds_error=False, fill_value=None)
        surrogates.dCdrag_ddelta_f  = interpolate.interp1d(mach_data,training.dCdrag_ddelta_f  ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCX_ddelta_f     = interpolate.interp1d(mach_data,training.dCX_ddelta_f     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCY_ddelta_f     = interpolate.interp1d(mach_data,training.dCY_ddelta_f     ,kind = 'linear',   bounds_error=False, fill_value=None)  
        surrogates.dCZ_ddelta_f     = interpolate.interp1d(mach_data,training.dCZ_ddelta_f     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCL_ddelta_f     = interpolate.interp1d(mach_data,training.dCL_ddelta_f     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCM_ddelta_f     = interpolate.interp1d(mach_data,training.dCM_ddelta_f     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCN_ddelta_f     = interpolate.interp1d(mach_data,training.dCN_ddelta_f     ,kind = 'linear',   bounds_error=False, fill_value=None)   
    
    if stability.slat_flag: 
        surrogates.Clift_delta_s    = RegularGridInterpolator((slat_data,mach_data),training.Clift_delta_s  ,method = 'linear',   bounds_error=False, fill_value=None)         
        surrogates.Cdrag_delta_s    = RegularGridInterpolator((slat_data,mach_data),training.Cdrag_delta_s  ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CX_delta_s       = RegularGridInterpolator((slat_data,mach_data),training.CX_delta_s  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CY_delta_s       = RegularGridInterpolator((slat_data,mach_data),training.CY_delta_s  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CZ_delta_s       = RegularGridInterpolator((slat_data,mach_data),training.CZ_delta_s  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CL_delta_s       = RegularGridInterpolator((slat_data,mach_data),training.CL_delta_s  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CM_delta_s       = RegularGridInterpolator((slat_data,mach_data),training.CM_delta_s  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CN_delta_s       = RegularGridInterpolator((slat_data,mach_data),training.CN_delta_s  ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dClift_ddelta_s  = interpolate.interp1d(training.dClift_ddelta_s  ,kind = 'linear',   bounds_error=False, fill_value=None)  
        surrogates.dCdrag_ddelta_s  = interpolate.interp1d(training.dCdrag_ddelta_s  ,kind = 'linear',   bounds_error=False, fill_value=None)   
        surrogates.dCX_ddelta_s     = interpolate.interp1d(training.dCX_ddelta_s     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCY_ddelta_s     = interpolate.interp1d(training.dCY_ddelta_s     ,kind = 'linear',   bounds_error=False, fill_value=None)  
        surrogates.dCZ_ddelta_s     = interpolate.interp1d(training.dCZ_ddelta_s     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCL_ddelta_s     = interpolate.interp1d(training.dCL_ddelta_s     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCM_ddelta_s     = interpolate.interp1d(training.dCM_ddelta_s     ,kind = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.dCN_ddelta_s     = interpolate.interp1d(training.dCN_ddelta_s     ,kind = 'linear',   bounds_error=False, fill_value=None)   

    return

# ----------------------------------------------------------------------
#  Evaluate VLM
# ----------------------------------------------------------------------
def evaluate_VLM(conditions,settings,geometry):
    """Calculate stability coefficients inluding specific wing coefficients using the VLM
        
    Assumptions:
        None
        
    Source:
        None

    Args: 
        conditions : flight conditions     [unitless]
        settings   : VLM analysis settings [unitless]
        geometry   : vehicle configuration [unitless] 
        
    Returns: 
        None  
    """    
    results = VLM(conditions,settings,geometry)
    Clift   = results.CL       
    Cdrag   = results.CDi      
    CX      = results.CX       
    CY      = results.CY       
    CZ      = results.CZ       
    CL      = results.CL_mom   
    CM      = results.CM       
    CN      = results.CN 
    S_ref = results.S_ref    
    b_ref = results.b_ref    
    c_ref = results.c_ref    
    X_ref = results.X_ref    
    Y_ref = results.Y_ref    
    Z_ref = results.Z_ref    

    return Clift,Cdrag,CX,CY,CZ,CL,CM,CN, S_ref,b_ref,c_ref,X_ref,Y_ref ,Z_ref  

