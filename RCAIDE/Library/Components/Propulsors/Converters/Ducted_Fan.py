# RCAIDE/Compoments/Propulsors/Converters/Ducted_Fan.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core              import Data
from RCAIDE.Library.Components          import Component 
from RCAIDE.Library.Methods.Propulsors.Converters.Ducted_Fan.append_ducted_fan_conditions import  append_ducted_fan_conditions
import numpy as np
import scipy as sp
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ----------------------------------------------------------------------------------------------------------------------  
class Ducted_Fan(Component):
    """
    A ducted fan propulsion system model that simulates the performance of a shrouded fan.

    Attributes
    ----------
    tag : str
        Identifier for the ducted fan. Default is 'ducted_fan'.
        
    number_of_radial_stations : int
        Number of radial calculation points for blade analysis. Default is 20.
        
    number_of_rotor_blades : int
        Number of blades in the rotor. Default is 12.
        
    tip_radius : float
        Outer radius of the rotor [m]. Default is 1.0.
        
    hub_radius : float
        Inner radius of the rotor at hub [m]. Default is 0.1.
        
    blade_clearance : float
        Clearance between blade tip and duct [m]. Default is 0.01.
        
    length : float
        Length of the ducted fan assembly [m]. Default is 1.0.
        
    fidelity : str
        Level of fidelity for calculations. Default is 'polytropic'.
        
    nacelle : Component
        Nacelle component. Default is None.
        
    fan : Component
        Fan component. Default is Fan().
        
    ram : Component
        Ram air intake component. Default is Ram().
        
    inlet_nozzle : Component
        Inlet nozzle component. Default is Compression_Nozzle().
        
    orientation_euler_angles : list
        Vector of angles defining default orientation [rad]. Default is [0.,0.,0.].
        
    rotor : Data
        Rotor configuration data

        - percent_x_location : float
            Rotor position as fraction of length. Default is 0.4.
            
    stator : Data
        Stator configuration data

        - percent_x_location : float
            Stator position as fraction of length. Default is 0.7.
            
    cruise : Data
        Design cruise conditions

        - design_thrust : float
            Design point thrust. Default is None.

        - design_altitude : float
            Design altitude [m]. Default is None.
            
        - design_angular_velocity : float
            Design rotational speed [rad/s]. Default is None.

        - design_freestream_velocity : float
            Design forward velocity [m/s]. Default is None.

        - design_reference_velocity : float
            Design reference velocity [m/s]. Default is None.

        - design_freestream_mach : float
            Design Mach number. Default is None.

        - design_reference_mach : float
            Design reference Mach number. Default is None.
            
    duct_airfoil : Data
        Duct aerodynamic surface data. Default is empty Data().
        
    hub_airfoil : Data
        Hub aerodynamic surface data. Default is empty Data().

    Notes
    -----
    The Ducted_Fan class models a shrouded fan propulsion system, including:
    * Rotor-stator interaction effects
    * Duct aerodynamic influences
    * Hub effects
    * Multiple coordinate frame transformations
    
    The model supports various fidelity levels and can handle both design and 
    off-design conditions.

    **Definitions**

    'Euler Angles'
        Set of three angles used to describe orientation in 3D space
        
    'Reference Velocity'
        Characteristic velocity used for non-dimensionalization
        
    'Polytropic'
        Thermodynamic process with constant polytropic efficiency

    See Also
    --------
    RCAIDE.Library.Components.Propulsors.Converters.Fan
    RCAIDE.Library.Components.Propulsors.Converters.Ram
    RCAIDE.Library.Components.Propulsors.Converters.Compression_Nozzle
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
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
        
        self.tag                               = 'ducted_fan'  
        self.number_of_radial_stations         = 20
        self.number_of_rotor_blades            = 12  
        self.tip_radius                        = 1.0
        self.hub_radius                        = 0.1
        self.blade_clearance                   = 0.01
        self.length                            = 1
        self.fidelity                          = 'polytropic'
        self.nacelle                           = None  
        self.fan                               = RCAIDE.Library.Components.Propulsors.Converters.Fan()   
        self.ram                               = RCAIDE.Library.Components.Propulsors.Converters.Ram()  
        self.inlet_nozzle                      = RCAIDE.Library.Components.Propulsors.Converters.Compression_Nozzle()  
        
        self.orientation_euler_angles          = [0.,0.,0.]  # vector of angles defining default orientation of rotor
        self.rotor                             = Data()
        self.stator                            = Data()
        self.rotor.percent_x_location          = 0.4
        self.stator.percent_x_location         = 0.7
        self.cruise                            = Data()
        self.cruise.design_thrust              = None
        self.cruise.design_altitude            = None
        self.cruise.design_angular_velocity    = None
        self.cruise.design_freestream_velocity = None
        self.cruise.design_reference_velocity  = None 
        self.cruise.design_freestream_mach     = None
        self.cruise.design_reference_mach      = None 
        self.duct_airfoil                      = None
        self.hub_airfoil                       = None
      
    
    def append_duct_airfoil(self, airfoil):
        """
        Adds an airfoil to the ducted fan's duct section.

        Parameters
        ----------
        airfoil : Data
            Airfoil data container with aerodynamic properties for the duct section.
            Must be of type Data().

        Returns
        -------
        None

        Notes
        -----
        This method appends airfoil data to the duct_airfoil attribute of the ducted fan.
        The airfoil data is used to model the aerodynamic characteristics of the duct
        section, which influences the overall performance of the ducted fan system.

        Raises
        ------
        Exception
            If input airfoil is not of type Data()
        """

        # Assert database type
        if not isinstance(airfoil,RCAIDE.Library.Components.Airfoils.Airfoil):
            raise Exception('input component must be of type Airfoil') 

        # Store data
        self.duct_airfoil =  airfoil

        return
    

    def append_hub_airfoil(self, airfoil):
        """
        Adds an airfoil to the ducted fan's hub section.

        Parameters
        ----------
        airfoil : Data
            Airfoil data container with aerodynamic properties for the hub section.
            Must be of type Data().

        Returns
        -------
        None

        Notes
        -----
        This method appends airfoil data to the hub_airfoil attribute of the ducted fan.
        The airfoil data is used to model the aerodynamic characteristics of the hub
        section, which affects the flow field and performance of the ducted fan system.

        Raises
        ------
        Exception
            If input airfoil is not of type Data()
        """

        # Assert database type
        if not isinstance(airfoil,RCAIDE.Library.Components.Airfoils.Airfoil):
            raise Exception('input component must be of type Airfoil') 

        # Store data
        self.hub_airfoil =  airfoil

        return 

    def append_operating_conditions(ducted_fan,segment,propulsor): 
        energy_conditions       = segment.state.conditions.energy[propulsor.tag]
        append_ducted_fan_conditions(ducted_fan,segment,energy_conditions)
        return        
          
    def vec_to_vel(self):
        """
        Rotates from the ducted fan's vehicle frame to the ducted fan's velocity frame.

        Parameters
        ----------
        None

        Returns
        -------
        rot_mat : ndarray
            3x3 rotation matrix transforming from vehicle frame to velocity frame.

        Notes
        -----
        This method creates a rotation matrix for transforming coordinates between
        two reference frames of the ducted fan. When the ducted fan is axially
        aligned with the vehicle body:

        Velocity frame:
        * X-axis points out the nose
        * Z-axis points towards the ground
        * Y-axis points out the right wing

        Vehicle frame:
        * X-axis points towards the tail
        * Z-axis points towards the ceiling
        * Y-axis points out the right wing

        **Theory**
        The transformation is accomplished using a rotation of π radians about the Y-axis,
        represented as a rotation vector [0, π, 0].

        **Major Assumptions**
        * The ducted fan's default orientation is aligned with the vehicle body
        * Right-handed coordinate system is used
        """

        rot_mat = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()

        return rot_mat
    

    def body_to_prop_vel(self, commanded_thrust_vector):
        """
        Rotates from the system's body frame to the ducted fan's velocity frame.

        Parameters
        ----------
        commanded_thrust_vector : ndarray
            Vector of commanded thrust angles [rad] for each time step.

        Returns
        -------
        rot_mat : ndarray
            3x3 rotation matrix transforming from body frame to ducted fan velocity frame.
        rots : ndarray
            Array of rotation vectors including commanded thrust angles.

        Notes
        -----
        This method performs a sequence of rotations to transform coordinates from
        the vehicle body frame to the ducted fan's velocity frame. The transformation
        sequence is:
        1. Body to vehicle frame (π rotation about Y-axis)
        2. Vehicle to ducted fan vehicle frame (includes thrust vector rotation)
        3. Ducted fan vehicle to ducted fan velocity frame

        Reference frames:
        Velocity frame:
        * X-axis points out the nose
        * Z-axis points towards the ground
        * Y-axis points out the right wing

        Vehicle frame:
        * X-axis points towards the tail
        * Z-axis points towards the ceiling
        * Y-axis points out the right wing

        **Theory**
        The complete transformation is computed as:
        rot_mat = (body_2_vehicle @ vehicle_2_duct_vec) @ duct_vec_2_duct_vel

        **Major Assumptions**
        * The ducted fan's default orientation is defined by orientation_euler_angles
        * Right-handed coordinate system is used
        * Thrust vector rotation is applied about the Y-axis
        * Matrix multiplication order preserves proper transformation sequence
        """

        # Go from velocity to vehicle frame
        body_2_vehicle = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()

        # Go from vehicle frame to ducted fan vehicle frame: rot 1 including the extra body rotation
        cpts       = len(np.atleast_1d(commanded_thrust_vector))
        rots       = np.array(self.orientation_euler_angles) * 1.
        rots       = np.repeat(rots[None,:], cpts, axis=0) 
        rots[:,1] += commanded_thrust_vector[:,0] 
        
        vehicle_2_duct_vec = sp.spatial.transform.Rotation.from_rotvec(rots).as_matrix()

        # GO from the ducted fan vehicle frame to the ducted fan velocity frame: rot 2
        duct_vec_2_duct_vel = self.vec_to_vel()

        # Do all the matrix multiplies
        rot1    = np.matmul(body_2_vehicle,vehicle_2_duct_vec)
        rot_mat = np.matmul(rot1,duct_vec_2_duct_vel)
 
        return rot_mat , rots


    def duct_vel_to_body(self, commanded_thrust_vector):
        """
        Rotates from the ducted fan's velocity frame to the system's body frame.

        Parameters
        ----------
        commanded_thrust_vector : ndarray
            Vector of commanded thrust angles [rad] for each time step.

        Returns
        -------
        rot_mat : ndarray
            3x3 rotation matrix transforming from ducted fan velocity frame to body frame.
        rots : ndarray
            Array of rotation vectors including commanded thrust angles.

        Notes
        -----
        This method performs the inverse transformation sequence of body_to_prop_vel.
        The transformation sequence is:
        1. Ducted fan velocity to ducted fan vehicle frame
        2. Ducted fan vehicle to vehicle frame (includes thrust vector rotation)
        3. Vehicle to body frame (π rotation about Y-axis)

        Reference frames:
        Velocity frame:
        * X-axis points out the nose
        * Z-axis points towards the ground
        * Y-axis points out the right wing

        Vehicle frame:
        * X-axis points towards the tail
        * Z-axis points towards the ceiling
        * Y-axis points out the right wing

        **Theory**
        The transformation is computed by inverting the rotation matrix from 
        body_to_prop_vel using:
        rot_mat = (body_2_duct_vel)^(-1)

        **Major Assumptions**
        * The ducted fan's default orientation is defined by orientation_euler_angles
        * Right-handed coordinate system is used
        * Thrust vector rotation is applied about the Y-axis
        """

        body2ductvel,rots = self.body_to_duct_vel(commanded_thrust_vector)

        r = sp.spatial.transform.Rotation.from_matrix(body2ductvel)
        r = r.inv()
        rot_mat = r.as_matrix()

        return rot_mat, rots
    
    def vec_to_duct_body(self,commanded_thrust_vector):
        rot_mat, rots =  self.duct_vel_to_body(commanded_thrust_vector) 
        return rot_mat, rots 