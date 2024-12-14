# RCAIDE/Compoments/Propulsors/Converters/Ducted_Fan.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core     import Data
from RCAIDE.Library.Components import Component
from RCAIDE.Library.Methods.Propulsors.Converters.Ducted_Fan.append_ducted_fan_conditions import  append_ducted_fan_conditions
import numpy as np
import scipy as sp
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ----------------------------------------------------------------------------------------------------------------------  
class Ducted_Fan(Component):
    """ This is a ducted fan component
    
    Assumptions:
    None
    
    Source:
    N/A
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
        self.duct_airfoil                      = Data()
        self.hub_airfoil                       = Data() 
      
    
    def append_duct_airfoil(self,airfoil):
        """ Adds an airfoil to the segment 
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """ 

        # Assert database type
        if not isinstance(airfoil,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.duct_airfoil.append(airfoil)

        return
    

    def append_hub_airfoil(self,airfoil):
        """ Adds an airfoil to the segment 
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """ 

        # Assert database type
        if not isinstance(airfoil,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.hub_airfoil.append(airfoil)

        return 

    def append_operating_conditions(ducted_fan,segment,propulsor): 
        energy_conditions       = segment.state.conditions.energy[propulsor.tag]
        append_ducted_fan_conditions(ducted_fan,segment,energy_conditions)
        return        
          
    def vec_to_vel(self):
        """This rotates from the ducted fan's vehicle frame to the ducted fan's velocity frame

        Assumptions:
        There are two ducted fan frames, the ducted fan vehicle frame and the ducted fan velocity frame. When ducted fan
        is axially aligned with the vehicle body:
           - The velocity frame is X out the nose, Z towards the ground, and Y out the right wing
           - The vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """

        rot_mat = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()

        return rot_mat
    

    def body_to_prop_vel(self,commanded_thrust_vector):
        """This rotates from the system's body frame to the ducted fan's velocity frame

        Assumptions:
        There are two ducted fan frames, the vehicle frame describing the location and the ducted fan velocity frame.
        Velocity frame is X out the nose, Z towards the ground, and Y out the right wing
        Vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
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


    def duct_vel_to_body(self,commanded_thrust_vector):
        """This rotates from the ducted fan's velocity frame to the system's body frame

        Assumptions:
        There are two ducted fan frames, the vehicle frame describing the location and the ducted fan velocity frame
        velocity frame is X out the nose, Z towards the ground, and Y out the right wing
        vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """

        body2ductvel,rots = self.body_to_duct_vel(commanded_thrust_vector)

        r = sp.spatial.transform.Rotation.from_matrix(body2ductvel)
        r = r.inv()
        rot_mat = r.as_matrix()

        return rot_mat, rots
    
    def vec_to_duct_body(self,commanded_thrust_vector):
        rot_mat, rots =  self.duct_vel_to_body(commanded_thrust_vector) 
        return rot_mat, rots 