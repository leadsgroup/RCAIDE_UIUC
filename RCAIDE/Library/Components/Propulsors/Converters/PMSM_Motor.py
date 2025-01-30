# RCAIDE/Library/Components/Propulsors/Converters/DC_Motor.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
from RCAIDE.Library.Methods.Propulsors.Converters.DC_Motor.append_motor_conditions import  append_motor_conditions

# ----------------------------------------------------------------------------------------------------------------------
#  PMSM_Motor  
# ----------------------------------------------------------------------------------------------------------------------           
class PMSM_Motor(Component):
    """
    A permanent magnet synchronous motor (PMSM) component model for electric propulsion systems.

    Attributes
    ----------
    tag : str
        Identifier for the motor. Default is 'motor'.
        
    resistance : float
        Internal electrical resistance of the motor [Ω]. Default is 0.0.
        
    no_load_current : float
        Current drawn by the motor with no mechanical load [A]. Default is 0.0.
        
    speed_constant : float
        Motor speed constant (Kv). Default is 0.0.
        
    rotor_radius : float
        Radius of the motor's rotor [m]. Default is 0.0.
        
    rotor_Cp : float
        Specific heat capacity of the rotor [J/kg/K]. Default is 0.0.
        
    efficiency : float
        Overall motor efficiency. Default is 1.0.
        
    gear_ratio : float
        Ratio of output shaft speed to motor speed. Default is 1.0.
        
    gearbox_efficiency : float
        Efficiency of the gearbox. Default is 1.0.
        
    expected_current : float
        Expected operating current [A]. Default is 0.0.
        
    power_split_ratio : float
        Ratio of power distribution when motor drives multiple loads. Default is 0.0.
        
    design_torque : float
        Design point torque output [N·m]. Default is 0.0.
        
    interpolated_func : callable
        Function for interpolating motor performance. Default is None.

    Notes
    -----
    The DC_Motor class models a direct current electric motor's performance
    characteristics. It accounts for electrical, mechanical, and thermal effects
    including:
    * Internal resistance losses
    * No-load current losses
    * Gearbox losses
    * Speed-torque relationships
    * Power distribution for multiple loads

    **Definitions**

    'Kv'
        Motor velocity constant, relating voltage to unloaded motor speed

    'No-load Current'
        Current drawn by motor to overcome internal friction when unloaded
        
    'Power Split Ratio'
        Fraction of total power delivered to primary load in multi-load applications

    See Also
    --------
    RCAIDE.Library.Methods.Propulsors.Converters.DC_Motor
    """      
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """           
        self.tag                = 'PMSM_motor' 
        # Input data from Datasheet
        self.Kv                        = 6.56                        # [rpm/V]        speed constant
        self.V                         = 610                         # [V]            nominal voltage
        self.D_in                      = 0.16                        # [m]            stator inner diameter
        self.I_tot                     = 375                         # [A]            total current that passes through the stator in both axial directions   
        self.D_out                     = 0.348                       # [m]            stator outer diameter

        # Input data from Literature
        self.k_w                       = 0.95                        # [-]            winding factor

        # Input data from Assumptions
        self.R                         = 0.002                       # [Ω]            resistance
        self.L                         = 11.40                       # [m]            (It should be around 0.14 m) motor stack length 
        self.N                         = 80                          # [-]            number of turns  
        self.l                         = 0.4                         # [m]            length of the path  
        self.mu_0                      = 1.256637061e-6              # [N/A**2]       permeability of free space
        self.mu_r                      = 1005                        # [N/A**2]       relative permeability of the magnetic material 
        self.k                         = 200                         # [W/m*K]        thermal conductivity of the magnetic material
        self.Delta_T                   = 10                          # [K]            temperature difference between the inner and outer surfaces of the stator
        self.L_flow                    = 0.01                        # [m]            characteristic length of the flow
        self.k_f                       = 0.026                       # [W/m*K]        thermal conductivity of the fluid
        self.l_cond_path               = 0.4                         # [m]            length of the conductive path  
        self.Re                        = 100000                      # [-]            Reynolds number of the coolingflow
        self.Re_airgap                 = 100000                      # [-]            Reynolds number of the flow in the airgap
        self.Pr                        = 0.708                       # [-]            Prandtl number of the flow
        self.h_fin                     = 0.005                       # [m]            height of the duct
        self.w_channel                 = 0.005                       # [m]            width of the duct
        self.D_h                       = 0.005                       # [m]            hydraulic diameter of the duct
        self.L_channel                 = 0.005                       # [m]            length of the channel
        self.V_dot                     = 0.005                       # [m**3/s]       volume flow rate of the fluid
        self.rho                       = 1000                        # [kg/m**3]      density of the fluid
        self.v                         = 0.005                       # [m/s]          velocity of the fluid
        self.Ta                        = 20                          # [-]            Taylor number 
        self.G                         = 0.01                        # [-]            ratio of the axial gap to the radius of the rotor
        self.Conduction_laminar_flow   = True                        # [-]            True if the flow is laminar, False if the flow is turbulent
        self.Convection_laminar_flow   = True                        # [-]            True if the flow is laminar, False if the flow is turbulent
        
    def append_operating_conditions(self,segment,propulsor):
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_motor_conditions(self,segment,propulsor_conditions)
        return
    