## @ingroup Library-Methods-Stability-Dynamic_Stability 
# RCAIDE/Library/Methods/Stability/Dynamic_Stability/compute_dynamic_flight_modes.py
# 
# 
# Created:  Apr 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                            import Units
from RCAIDE.Library.Methods.Stability.Common          import estimate_wing_CL_alpha
from RCAIDE.Library.Components.Wings.Control_Surfaces import Aileron , Elevator  

# python imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  compute_dynamic_flight_modes
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Library-Methods-Stability-Dynamic_Stability
def compute_dynamic_flight_modes(conditions,aircraft): 
    """This function follows the stability axis EOM derivation in Blakelock
    to return the aircraft's dynamic modes and state space 
    
    Assumptions:
       Linerarized Equations are used following the reference below

    Source:
      Automatic Control of Aircraft and Missiles by J. Blakelock Pg 23 and 117 

    Inputs:
       conditions.aerodynamics  
       conditions.static_stability  
       conditions.stability.dynamic 

    Outputs: 
       conditions.dynamic_stability.LatModes
       conditions.dynamic_stability.LongModes 

    Properties Used:
       N/A
     """
 
    # unpack unit conversions  
    g      = conditions.freestream.gravity 
    mach   = conditions.freestream.mach_number 
    rho    = conditions.freestream.density
    u0     = conditions.freestream.velocity
    qDyn0  = conditions.freestream.dynamic_pressure 
      
    # Unpack aircraft Properties
    theta0 = conditions.aerodynamics.angles.alpha
    AoA    = conditions.aerodynamics.angles.alpha
    CLtot  = conditions.aerodynamics.coefficients.lift 
    CDtot  = conditions.aerodynamics.coefficients.drag 
    e      = conditions.aerodynamics.oswald_efficiency
    SS     = conditions.static_stability
    SSD    = SS.derivatives 
    DS     = conditions.dynamic_stability
             
    num_cases  = len(AoA)
     
    b_ref  = conditions.b_ref
    c_ref  = conditions.c_ref
    S_ref  = conditions.S_ref 
    AR     = (b_ref**2)/S_ref
    moments_of_inertia = aircraft.mass_properties.moments_of_inertia.tensor
    Ixx    = moments_of_inertia[0][0]
    Iyy    = moments_of_inertia[1][1]
    Izz    = moments_of_inertia[2][2]    
    if aircraft.mass_properties.mass == 0:
        m  = aircraft.mass_properties.max_takeoff
    elif aircraft.mass_properties.max_takeoff == 0:
        m = aircraft.mass_properties.mass
    else:
        raise AttributeError("Specify Vehicle Mass") 
    
    if np.all(conditions.static_stability.spiral_criteria) == 0: 
        conditions.static_stability.spiral_criteria = SSD.CL_beta*SSD.CN_r / (SSD.CL_r*SSD.CN_beta)
    
      
    ## Build longitudinal EOM A Matrix (stability axis)
    ALon = np.zeros((num_cases,4,4))
    BLon = np.zeros((num_cases,4,1)) 
    CLon = np.zeros((num_cases,4,4))
    for i in range(num_cases): 
        CLon[i,:,:] = np.eye(4)       
    DLon = np.zeros((num_cases,4,1))
    
    Cw         = m * g / (qDyn0 * S_ref) 
    Cxu        = SSD.CX_u
    Xu         = rho * u0 * S_ref * Cw * np.sin(theta0) + 0.5 * rho * u0 * S_ref * Cxu
    Cxalpha    = (CLtot - 2 * CLtot / (np.pi * AR * e ) * SSD.CL_alpha)
    Xw         = 0.5 * rho * u0 * S_ref * Cxalpha
    Xq         = 0  
               
    Czu        = SSD.CZ_u
    Zu         = -rho * u0 * S_ref * Cw * np.cos(theta0) + 0.5 * rho * u0 * S_ref * Czu
    Czalpha    = -CDtot - SSD.CL_alpha
    Zw         = 0.5 * rho * u0 * S_ref * Czalpha
    Czq        = -SSD.CL_q 
    Zq         = 0.25 * rho * u0 * c_ref * S_ref * Czq
    Cmu        = SSD.CM_q   
    Mu         = 0.5 * rho * u0 * c_ref * S_ref * Cmu
    Mw         = 0.5 * rho * u0 * c_ref * S_ref * SSD.CM_alpha
    Mq         = 0.25 * rho * u0 * c_ref * c_ref * S_ref * SSD.CM_q 
    
    # Derivative of pitching rate with respect to d(alpha)/d(t)
    if aircraft.wings['horizontal_stabilizer'] and aircraft.wings['main_wing']:
        l_t             = aircraft.wings['horizontal_stabilizer'].origin[0][0] + aircraft.wings['horizontal_stabilizer'].aerodynamic_center[0] - aircraft.wings['main_wing'].origin[0][0] - aircraft.wings['main_wing'].aerodynamic_center[0] 
        mac             = aircraft.wings['main_wing'].chords.mean_aerodynamic
        CL_alpha_mw     = estimate_wing_CL_alpha(aircraft.wings['main_wing'],mach) 
        ep_alpha        = 2 * CL_alpha_mw/ np.pi / (b_ref ** 2. / S_ref )   # J.H. Blakelock, "AAutomatic Control of Aircraft and Missiles"  Wiley & Sons, Inc. New York, 1991, (pg 34)
        SSD.Cm_alpha_dot = 2. * SSD.CM_alpha * ep_alpha * l_t / mac #  J.H. Blakelock, "Automatic Control of Aircraft and Missiles   Wiley & Sons, Inc. New York, 1991, (pg 23)
        SSD.Cz_alpha_dot = 2. * SSD.CM_alpha * ep_alpha
    else:    
        SSD.Cm_alpha_dot = 0 
        SSD.Cz_alpha_dot = 0
        
    ZwDot      = 0.25 * rho * c_ref * S_ref * SSD.Cz_alpha_dot    
    MwDot      = 0.25 * rho * c_ref * S_ref * SSD.Cm_alpha_dot 
    
    # Elevator effectiveness 
    for wing in aircraft.wings:
        if wing.control_surfaces :
            for ctrl_surf in wing.control_surfaces: 
                if (type(ctrl_surf) ==  Elevator):
                    ele = conditions.control_surfaces.elevator.static_stability.coefficients 
                    Xe  = 0 # Neglect
                    Ze  = 0.5 * rho * u0 * u0 * S_ref * ele.lift
                    Me  = 0.5 * rho * u0 * u0 * S_ref * c_ref * ele.M
                    
                    BLon[:,0,0] = Xe / m
                    BLon[:,1,0] = (Ze / (m - ZwDot)).T[0]
                    BLon[:,2,0] = (Me / Iyy + MwDot / Iyy * Ze / (m - ZwDot)).T[0]
                    BLon[:,3,0] = 0
                    
    
    ALon[:,0,0] = (Xu / m).T[0]
    ALon[:,0,1] = (Xw / m).T[0]
    ALon[:,0,2] =  Xq / m 
    ALon[:,0,3] = (-g * np.cos(theta0)).T[0]
    ALon[:,1,0] = (Zu / (m - ZwDot)).T[0]
    ALon[:,1,1] = (Zw / (m - ZwDot)).T[0]
    ALon[:,1,2] = ((Zq + (m * u0)) / (m - ZwDot) ).T[0]
    ALon[:,1,3] = (-m * g * np.sin(theta0) / (m - ZwDot)).T[0]
    ALon[:,2,0] = ((Mu + MwDot * Zu / (m - ZwDot)) / Iyy).T[0] 
    ALon[:,2,1] = ((Mw + MwDot * Zw / (m - ZwDot)) / Iyy).T[0] 
    ALon[:,2,2] = ((Mq + MwDot * (Zq + m * u0) / (m - ZwDot)) / Iyy ).T[0] 
    ALon[:,2,3] = (-MwDot * m * g * np.sin(theta0) / (Iyy * (m - ZwDot))).T[0] 
    ALon[:,3,0] = 0
    ALon[:,3,1] = 0
    ALon[:,3,2] = 1
    ALon[:,3,3] = 0
     
    # Look at eigenvalues and eigenvectors
    LonModes                  = np.zeros((num_cases,4), dtype = complex)
    phugoidFreqHz             = np.zeros((num_cases,1))
    phugoidDamping            = np.zeros((num_cases,1))
    phugoidTimeDoubleHalf     = np.zeros((num_cases,1))
    shortPeriodFreqHz         = np.zeros((num_cases,1))
    shortPeriodDamping        = np.zeros((num_cases,1))
    shortPeriodTimeDoubleHalf = np.zeros((num_cases,1))
    
    for i in range(num_cases):
        D  , V = np.linalg.eig(ALon[i,:,:]) # State order: u, w, q, theta
        LonModes[i,:] = D
        
        # Find phugoid
        phugoidInd               = np.argmax(V[0,:]) # u is the primary state involved
        phugoidFreqHz[i]         = abs(LonModes[i,phugoidInd]) / 2 / np.pi
        phugoidDamping[i]        = -np.cos(np.angle(LonModes[i,phugoidInd]))
        phugoidTimeDoubleHalf[i] = np.log(2) / abs(2 * np.pi * phugoidFreqHz[i] * phugoidDamping[i])
        
        # Find short period
        shortPeriodInd               = np.argmax(V[1,:]) # w is the primary state involved
        shortPeriodFreqHz[i]         = abs(LonModes[i, shortPeriodInd]) / 2 / np.pi
        shortPeriodDamping[i]        = -np.cos(np.angle(LonModes[i, shortPeriodInd ]))
        shortPeriodTimeDoubleHalf[i] = np.log(2) / abs(2 * np.pi * shortPeriodFreqHz[i] * shortPeriodDamping[i]) 
    
    ## Build lateral EOM A Matrix (stability axis)
    ALat = np.zeros((num_cases,4,4))
    BLat = np.zeros((num_cases,4,1))
    CLat = np.zeros((num_cases,4,4))
    for i in range(num_cases): 
        CLat[i,:,:] = np.eye(4) 
    DLat = np.zeros((num_cases,4,1))
    
    # Need to compute Ixx, Izz, and Ixz as a function of alpha
    Ixp  = np.zeros((num_cases,1))
    Izp  = np.zeros((num_cases,1))
    Ixzp = np.zeros((num_cases,1))
    
    for i in range(num_cases): 
        R       = np.array( [[np.cos(AoA[i][0]*Units.degrees) ,  - np.sin(AoA[i][0]*Units.degrees) ], [ np.sin( AoA[i][0]*Units.degrees) , np.cos(AoA[i][0]*Units.degrees)]])
        modI    = np.array([[moments_of_inertia[0][0],moments_of_inertia[0][2]],[moments_of_inertia[2][0],moments_of_inertia[2][2]]] ) 
        INew    = R * modI  * np.transpose(R)
        IxxStab =  INew[0,0]
        IxzStab = -INew[0,1]
        IzzStab =  INew[1,1]
        Ixp[i]  = (IxxStab * IzzStab - IxzStab**2) / IzzStab
        Izp[i]  = (IxxStab * IzzStab - IxzStab**2) / IxxStab
        Ixzp[i] = IxzStab / (IxxStab * IzzStab - IxzStab**2) 
        
    Yv = 0.5 * rho * u0 * S_ref * SSD.CY_beta
    Yp = 0.25 * rho * u0 * b_ref * S_ref * SSD.CY_p
    Yr = 0.25 * rho * u0 * b_ref * S_ref * SSD.CY_r
    Lv = 0.5 * rho * u0 * b_ref * S_ref * SSD.CL_beta
    Lp = 0.25 * rho * u0 * b_ref**2 * S_ref * SSD.CL_p
    Lr = 0.25 * rho * u0 * b_ref**2 * S_ref * SSD.CL_r
    Nv = 0.5 * rho * u0 * b_ref * S_ref * SSD.CN_beta
    Np = 0.25 * rho * u0 * b_ref**2 * S_ref * SSD.CN_p
    Nr = 0.25 * rho * u0 * b_ref**2 * S_ref * SSD.CN_r
    
    # Aileron effectiveness 
    for wing in aircraft.wings:
        if wing.control_surfaces :
            for ctrl_surf in wing.control_surfaces:
                if (type(ctrl_surf) ==  Aileron): 
                    ail = conditions.control_surfaces.aileron.static_stability.coefficients                  
                    Ya = 0.5 * rho * u0 * u0 * S_ref * ail.Y 
                    La = 0.5 * rho * u0 * u0 * S_ref * b_ref * ail.L 
                    Na = 0.5 * rho * u0 * u0 * S_ref * b_ref * ail.N 
                    
                    BLat[:,0,0] = (Ya / m).T[0]
                    BLat[:,1,0] = (La / Ixp + Ixzp * Na).T[0]
                    BLat[:,2,0] = (Ixzp * La + Na / Izp).T[0]
                    BLat[:,3,0] = 0
 
    ALat[:,0,0] = (Yv / m).T[0] 
    ALat[:,0,1] = (Yp / m).T[0] 
    ALat[:,0,2] = (Yr/m - u0).T[0] 
    ALat[:,0,3] = (g * np.cos(theta0)).T[0] 
    ALat[:,1,0] = (Lv / Ixp + Ixzp * Nv).T[0] 
    ALat[:,1,1] = (Lp / Ixp + Ixzp * Np).T[0] 
    ALat[:,1,2] = (Lr / Ixp + Ixzp * Nr).T[0] 
    ALat[:,1,3] = 0
    ALat[:,2,0] = (Ixzp * Lv + Nv / Izp).T[0] 
    ALat[:,2,1] = (Ixzp * Lp + Np / Izp).T[0] 
    ALat[:,2,2] = (Ixzp * Lr + Nr / Izp).T[0] 
    ALat[:,2,3] = 0
    ALat[:,3,0] = 0
    ALat[:,3,1] = 1
    ALat[:,3,2] = (np.tan(theta0)).T[0] 
    ALat[:,3,3] = 0
                                
    LatModes                    = np.zeros((num_cases,4),dtype=complex)
    dutchRollFreqHz             = np.zeros((num_cases,1))
    dutchRollDamping            = np.zeros((num_cases,1))
    dutchRollTimeDoubleHalf     = np.zeros((num_cases,1))
    rollSubsistenceFreqHz       = np.zeros((num_cases,1))
    rollSubsistenceTimeConstant = np.zeros((num_cases,1))
    rollSubsistenceDamping      = np.zeros((num_cases,1))
    spiralFreqHz                = np.zeros((num_cases,1))
    spiralTimeDoubleHalf        = np.zeros((num_cases,1))
    spiralDamping               = np.zeros((num_cases,1))
    dutchRoll_mode_real         = np.zeros((num_cases,1))
    
    for i in range(num_cases):        
        D  , V = np.linalg.eig(ALat[i,:,:]) # State order: u, w, q, theta
        LatModes[i,:] = D  
        
        # Find dutch roll (complex pair)
        done = 0
        for j in range(3):
            for k in range(j+1,4):
                if LatModes[i,j].real ==  LatModes[i,k].real:
                    dutchRollFreqHz[i] = abs(LatModes[i,j]) / 2 / np.pi
                    dutchRollDamping[i] = -np.cos(np.angle(LatModes[i,j]))
                    dutchRollTimeDoubleHalf[i] = np.log(2) / abs(2 * np.pi * dutchRollFreqHz[i] * dutchRollDamping[i])
                    dutchRoll_mode_real[i] = LatModes[i,j].real /  2 / np.pi
                    done = 1
                    break  
            if done:
                break  
        
        # Find roll mode
        diff_vec = np.arange(0,4)
        tmpInd   = np.setdiff1d(diff_vec , [j,k])
        rollInd  = np.argmax(abs(LatModes[i,tmpInd])) # higher frequency than spiral
        rollInd  = tmpInd[rollInd]
        rollSubsistenceFreqHz[i]       = abs(LatModes[i,rollInd]) / 2 / np.pi
        rollSubsistenceDamping[i]      = - np.sign(LatModes[i,rollInd].real)
        rollSubsistenceTimeConstant[i] = 1 / (2 * np.pi * rollSubsistenceFreqHz[i] * rollSubsistenceDamping[i])
        
        # Find spiral mode
        spiralInd               = np.setdiff1d(diff_vec,[j,k,rollInd])
        spiralFreqHz[i]         = abs(LatModes[i,spiralInd]) / 2 / np.pi
        spiralDamping[i]        = - np.sign(LatModes[i,spiralInd].real)
        spiralTimeDoubleHalf[i] = np.log(2) / abs(2 * np.pi * spiralFreqHz[i] * spiralDamping[i])
         
    ## Build longitudinal and lateral state space system. Requires additional toolbox 
    #from control.matlab import ss  # control toolbox needed in python. Run "pip (or pip3) install control"    
    #LonSys    = {}
    #LatSys    = {}    
    #for i in range(num_cases):         
        #LonSys[cases[i].tag] = ss(ALon[i],BLon[i],CLon[i],DLon[i])
        #LatSys[cases[i].tag] = ss(ALat[i],BLat[i],CLat[i],DLat[i]) 
    
    
    # Inertial coupling susceptibility
    # See Etkin & Reid pg. 118 
    DS.pMax = min(min(np.sqrt(-Mw * u0 / (Izz - Ixx))), min(np.sqrt(-Nv * u0 / (Iyy - Ixx)))) 
    
    # -----------------------------------------------------------------------------------------------------------------------  
    # Store Results
    # ------------------------------------------------------------------------------------------------------------------------  
    DS.LongModes.LongModes                    = LonModes
    #DS.LongModes.LongSys                      = LonSys    
    DS.LongModes.phugoidFreqHz                = phugoidFreqHz
    DS.LongModes.phugoidDamp                  = phugoidDamping
    DS.LongModes.phugoidTimeDoubleHalf        = phugoidTimeDoubleHalf
    DS.LongModes.shortPeriodFreqHz            = shortPeriodFreqHz
    DS.LongModes.shortPeriodDamp              = shortPeriodDamping
    DS.LongModes.shortPeriodTimeDoubleHalf    = shortPeriodTimeDoubleHalf
                                                                    
    DS.LatModes.LatModes                      = LatModes  
    #DS.LatModes.Latsys                        = LatSys   
    DS.LatModes.dutchRollFreqHz               = dutchRollFreqHz
    DS.LatModes.dutchRollDamping              = dutchRollDamping
    DS.LatModes.dutchRollTimeDoubleHalf       = dutchRollTimeDoubleHalf
    DS.LatModes.dutchRoll_mode_real           = dutchRoll_mode_real 
    DS.LatModes.rollSubsistenceFreqHz         = rollSubsistenceFreqHz
    DS.LatModes.rollSubsistenceTimeConstant   = rollSubsistenceTimeConstant
    DS.LatModes.rollSubsistenceDamping        = rollSubsistenceDamping
    DS.LatModes.spiralFreqHz                  = spiralFreqHz
    DS.LatModes.spiralTimeDoubleHalf          = spiralTimeDoubleHalf 
    DS.LatModes.spiralDamping                 = spiralDamping
    
    return 
