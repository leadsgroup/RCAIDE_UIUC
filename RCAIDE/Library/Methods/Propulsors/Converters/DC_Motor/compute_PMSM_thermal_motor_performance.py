# RCAIDE/Library/Methods/Propulsors/Converters/DC_Motor/compute_PMSM_thermal_motor_performance.py
# 
# Created:  Jan 2025, M. Clarke, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  compute_PMSM_motor_thermal_performance
# ----------------------------------------------------------------------------------------------------------------------    
def compute_PMSM_motor_thermal_performance(motor):
    
    A              = np.pi * ((motor.D_out**2 - motor.D_in**2) / 4)                    # [m**2]         cross-sectional area of the reluctance path perpendicular to length 𝑙    
    R_cond_path    = motor.l_cond_path/(motor.k*A)                                     # [K/W]          Conductive Path Thermal Resistance (Eq.68)

    if motor.Conduction_laminar_flow == True:   
        Nu     = 0.453*(motor.Re**0.5)*(motor.Pr**(1/3))                               # Laminar Nusselt number (Eq.71)
    else:
        Nu   = 0.0308*(motor.Re**(4/5))*(motor.Pr**(1/3))                              # Turbulent Nusselt number (Eq.71) 
    h    = motor.L_flow*Nu*motor.k_f                                                   # [W/m**2*K]     convection coefficient of the flow at a liquid to solid interfaced
    R_conv_path    = 1/(h*A)                                                           # [K/W]          Fluid Flow Thermal Resistance (Eq.69)

    if motor.Re < 3000:
        Nu_cooling_flow     = 1.051*np.log(motor.h_fin/motor.w_channel) + 2.89         # Nusselt number for cooling flow in rectangular ducts and Re_d < 3000 (Eq.72)
        h_cooling_flow      = motor.L_flow*Nu_cooling_flow*motor.k_f                   # [W/m**2*K]     convection coefficient of the flow at a liquid to solid interfaced
        R_conv_path_cooling_flow    = 1/(h_cooling_flow*A)                             # [K/W]          Fluid Flow Thermal Resistance (Eq.69)
    else:
        if motor.Convection_laminar_flow == True:
            f = 64/motor.Re
        else:
            f = (0.79*np.log(motor.Re) - 1.64)**(-2)                                   # Turbulent Moody friction factor (Eq.73)
        Nu_cooling_flow   = ((f/8)*(motor.Re - 1000)*motor.Pr)/(1 + 12.7*((f/8)**0.5)*(motor.Pr**(2/3) - 1)) # Nusselt number for cooling flow in rectangular ducts and Re_d >= 3000 (Eq.72)
        h_cooling_flow    = motor.L_flow*Nu_cooling_flow*motor.k_f                     # [W/m**2*K]     convection coefficient of the flow at a liquid to solid interfaced
        R_conv_path_cooling_flow    = 1/(h_cooling_flow*A)                             # [K/W]          Fluid Flow Thermal Resistance (Eq.69)

    Delta_P_flow               = ((f*motor.rho*motor.v**2)/(2*motor.D_h))*motor.L_channel # Flow pressure drop (Eq.74)
    Loss_cooling               = Delta_P_flow*motor.V_dot                              # Power needed to pump the fluid through the duct (Eq.75)

    if motor.Ta < 41: 
        Nu_airgap  = 2                                                                 # Nusselt number for the airgap convection and Ta < 41 (Eq.76)
    elif motor.Ta> 41 and motor.Ta < 100:
        Nu_airgap = 0.202*(motor.Ta**(0.63))*(motor.Pr**0.27)                          # Nusselt number for the airgap convection and 41 < Ta < 100 (Eq.76)
    else:
        Nu_airgap = 0.386*(motor.Ta**0.5)*(motor.Pr**0.27)                             # Nusselt number for the airgap convection and 100 < Ta (Eq.76)
    h_airgap    = motor.L_flow*Nu_airgap*motor.k_f                                     # [W/m**2*K]     convection coefficient of the flow at a liquid to solid interfaced
    R_airgap    = 1/(h_airgap*A)                                                       # [K/W]          Fluid Flow Thermal Resistance (Eq.69)

    if motor.G == 0.01:
        if motor.Re_airgap < 1e5:
            Nu_G          = 7.46*motor.Re_airgap**(0.32)                               # Nusselt number for laminar flow and G = 0.01 (Eq.77)
        else:
            Nu_G        = 0.044*motor.Re_airgap**(0.75)                                # Nusselt number for turbulent flow and G = 0.01 (Eq.78)  
    elif motor.G> 0.02 and motor.G < 0.06:
        if motor.Re_airgap < 1e5:
            Nu_G     = 0.5*(1 + 5.47*(10**-4)*np.exp(112*motor.G))*(motor.Re_airgap**0.5) # Nusselt number for laminar flow and G = 0.02 - 0.06 (Eq.77)
        else:    
            Nu_G  = 0.5*(12.57*np.exp(-33.18*motor.G))*(motor.Re_airgap**(0.6 + 25*motor.G**(12/7))) # Nusselt number for turbulent flow and G = 0.02 - 0.06 (Eq.78)    
    elif motor.G > 0.06:
        if motor.Re_airgap < 1e5:
            Nu_G = 0.35*(motor.Re_airgap**0.5)                                         # Nusselt number for laminar flow and G > 0.06 (Eq.77)
        else:    
            Nu_G = 0.0151*(motor.Re_airgap**0.6)                                       # Nusselt number for turbulent flow and G > 0.06 (Eq.78)
    h_endspace    = motor.L_flow*Nu_G*motor.k_f                                        # [W/m**2*K]     convection coefficient of the flow at a liquid to solid interfaced
    R_endspace    = 1/(h_endspace*A)                                                   # [K/W]          Fluid Flow Thermal Resistance (Eq.69)



    Q_cond_path              = motor.Delta_T/R_cond_path                               # heat through a conductive thermal path (Eq.67)
    Q_conv_path              = motor.Delta_T/R_conv_path                               # heat through a thermal path (Eq.67)
    Q_conv_path_cooling_flow = motor.Delta_T/R_conv_path_cooling_flow                  # heat through a thermal path (Eq.67)
    Q_conv_airgap            = motor.Delta_T/R_airgap                                  # heat through a thermal path (Eq.67)
    Q_conv_endspace          = motor.Delta_T/R_endspace                                # heat through a thermal path (Eq.67)

    return Q_cond_path, Q_conv_path, Q_conv_path_cooling_flow, Q_conv_airgap, Q_conv_endspace, Delta_P_flow, Loss_cooling