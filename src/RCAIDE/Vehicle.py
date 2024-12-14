# Vehicle.py
# 
# Created:  Apr 2024, M. Clarke
# Modified:  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from RCAIDE                    import Framework
from RCAIDE.Framework.Core     import Data, DataOrdered
from RCAIDE.Library            import Components, Attributes 
import numpy as np 
from RCAIDE.Library.Methods.Weights.Correlation_Buildups.Common.compute_operating_empty_weight import  compute_operating_empty_weight

# ----------------------------------------------------------------------------------------------------------------------
#  Vehicle
# ----------------------------------------------------------------------------------------------------------------------  
class Vehicle(Data):
    """RCAIDE Vehicle container class with database + input / output functionality
    """    

    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """    
        self.tag                                                           = 'vehicle'
        self.networks                                                      = Framework.Networks.Network.Container()
        self.fuselages                                                     = Components.Fuselages.Fuselage.Container()
        self.wings                                                         = Components.Wings.Wing.Container()
        self.nacelles                                                      = Components.Nacelles.Nacelle.Container()
        self.systems                                                       = Components.Systems.System.Container()
        self.avionics                                                      = Components.Systems.Avionics.Container()
        self.booms                                                         = Components.Booms.Boom.Container()
        self.mass_properties                                               = Vehicle_Mass_Container()
        self.payload                                                       = Components.Payloads.Payload.Container()
        self.costs                                                         = Data()     
        self.landing_gears                                                 = Components.Landing_Gear.Landing_Gear.Container()  
        self.reference_area                                                = 0.0
        self.passengers                                                    = 0.0
        self.maximum_cross_sectional_area                                  = 0.0
        
        self.flight_envelope                                               = Data()
        self.flight_envelope.design_dynamic_pressure                       = None 
        self.flight_envelope.design_mach_number                            = None  
        self.flight_envelope.design_cruise_altitude                        = None
        self.flight_envelope.design_range                                  = None 
        self.flight_envelope.ultimate_load                                 = 5.7 
        self.flight_envelope.limit_load                                    = 3.8   
        self.flight_envelope.alpha_maximum                                 = 0.0
        self.flight_envelope.alt_vc                                        = 0.0
        self.flight_envelope.alt_gust                                      = 0.0
        self.flight_envelope.max_ceiling                                   = 0.0
        self.flight_envelope.maximum_dynamic_pressure                      = 0.0
        self.flight_envelope.maximum_mach_operational                      = 0.0

        self.flight_envelope.maneuver                                      = Data()
        self.flight_envelope.maneuver.load_alleviation_factor              = 0.0
        
        self.flight_envelope.maneuver.equivalent_speed                     = Data()
        self.flight_envelope.maneuver.equivalent_speed.velocity_max_gust   = 0
        self.flight_envelope.maneuver.equivalent_speed.velocity_max_cruise = 0
        self.flight_envelope.maneuver.equivalent_speed.velocity_max_dive   = 0
        
        self.flight_envelope.maneuver.load_factor                          = Data()
        self.flight_envelope.maneuver.load_factor.velocity_max_gust        = 0
        self.flight_envelope.maneuver.load_factor.velocity_max_cruise      = 0
        self.flight_envelope.maneuver.load_factor.velocity_max_dive        = 0

        self.flight_envelope.gust                                          = Data()
        self.flight_envelope.gust.load_alleviation_factor                  = 0.0
        self.flight_envelope.gust.equivalent_speed                         = Data()
        self.flight_envelope.gust.equivalent_speed.velocity_max_gust       = 0
        self.flight_envelope.gust.equivalent_speed.velocity_max_cruise     = 0
        self.flight_envelope.gust.equivalent_speed.velocity_max_dive       = 0
        
        self.flight_envelope.gust.load_factor                              = Data()
        self.flight_envelope.gust.load_factor.velocity_max_gust            = 0
        self.flight_envelope.gust.load_factor.velocity_max_cruise          = 0
        self.flight_envelope.gust.load_factor.velocity_max_dive            = 0 
        
        self.performance                              = DataOrdered()
         
    _energy_network_root_map = None 

    def __init__(self,*args,**kwarg):
        """ Sets up the component hierarchy for a vehicle
    
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
        # will set defaults
        super(Vehicle,self).__init__(*args,**kwarg)  

        self._component_root_map = {
            Components.Fuselages.Fuselage              : self['fuselages']        ,
            Components.Wings.Wing                      : self['wings']            ,
            Components.Systems.System                  : self['systems']          ,
            Components.Systems.Avionics                : self['avionics']         ,
            Components.Payloads.Payload                : self['payload']          , 
            Components.Nacelles.Nacelle                : self['nacelles']         , 
            Components.Booms.Boom                      : self['booms']            ,
            Components.Landing_Gear.Landing_Gear       : self['landing_gears']     ,
            Vehicle_Mass_Properties                    : self['mass_properties']  ,
        }
         
        self._energy_network_root_map= {
            Framework.Networks.Network                 : self['networks']         ,
            }    
        
        self.append_component(Vehicle_Mass_Properties())
         
        return
    

    def find_component_root(self,component):
        """ find pointer to component data root.
        
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

        # find component root by type, allow subclasses
        for component_type, component_root in self._component_root_map.items():
            if isinstance(component,component_type):
                break
        else:
            raise Exception("Unable to place component type %s" % component.typestring())

        return component_root


    def append_component(self,component):
        """ Adds a component to vehicle
        
            Assumptions:
                None
    
            Source:
                None
        """  

        # assert database type
        if not isinstance(component,Data):
            raise Exception('input component must be of type Data()')

        # find the place to store data
        component_root = self.find_component_root(component)
        
        # See if the component exists, if it does modify the name
        keys = component_root.keys()
        if str.lower(component.tag) in keys:
            string_of_keys = "".join(component_root.keys())
            n_comps = string_of_keys.count(component.tag)
            component.tag = component.tag + str(n_comps+1)

        # store data
        component_root.append(component)

        return

    def find_energy_network_root(self,energy_network):
        """ Find pointer to energy network data root.
        
            Assumptions:
                None
    
            Source:
                None
        """  
        # find energy network root by type, allow subclasses
        for energy_network_type, energy_network_root in self._energy_network_root_map.items():
            if isinstance(energy_network,energy_network_type):
                break
        else:
            raise Exception("Unable to place energy_network type %s" % energy_network.typestring())

        return energy_network_root

    def sum_mass(self):
        """ Regresses through the vehicle and sums the masses
        
            Assumptions:
                None
    
            Source:
                None
        """  

        total = 0.0
        
        for key in self.keys():
            item = self[key]
            if isinstance(item,Components.Component.Container):
                total += item.sum_mass()

        return total
    
    
    def center_of_gravity(self):
        """ will recursively search the data tree and sum
            any Comp.Mass_Properties.mass, and return the total sum
        
            Assumptions:
                None
    
            Source:
                None
        """   
        total = np.array([[0.0,0.0,0.0]])

        for key in self.keys():
            item = self[key]
            if isinstance(item,Components.Component.Container):
                total += item.total_moment()
                
        mass = self.sum_mass()
        if mass ==0:
            mass = 1.
                
        CG = total/mass
        
        self.mass_properties.center_of_gravity = CG
                
        return CG
    
    def moment_of_inertia(self):
        """  
        """
        M = np.zeros((3, 3))
        center_of_gravity =  self.mass_properties.center_of_gravity 
        for key in self.keys():
            item = self[key] 
            M += item.moment_of_inertia(center_of_gravity) 
                
        return M
     
    def operating_empty_weight(self):
        """ Compute operating empty weight  
        
            Assumptions:
                None
    
            Source:
                None
        """  
        outputs = compute_operating_empty_weight(self)  
                
        return outputs     
    
    def append_energy_network(self,energy_network):
        """ Adds an energy network to vehicle 
        
            Assumptions:
                None
    
            Source:
                None
        """  

        # assert database type
        if not isinstance(energy_network,Data):
            raise Exception('input energy network must be of type Data()')

        # find the place to store data
        energy_network_root = self.find_energy_network_root(energy_network)
        
        # See if the energy network exists, if it does modify the name
        keys = energy_network_root.keys()
        if str.lower(energy_network.tag) in keys:
            string_of_keys = "".join(energy_network_root.keys())
            n_comps = string_of_keys.count(energy_network.tag)
            energy_network.tag = energy_network.tag + str(n_comps+1)

        # store data
        energy_network_root.append(energy_network)

        return    

    def find_energy_network_root(self,energy_network):
        """ Find pointer to energy network data root.
        
            Assumptions:
                None
    
            Source:
                None
        """  
        # find energy network root by type, allow subclasses
        for energy_network_type, energy_network_root in self._energy_network_root_map.items():
            if isinstance(energy_network,energy_network_type):
                break
        else:
            raise Exception("Unable to place energy_network type %s" % energy_network.typestring())

        return energy_network_root
 
class Vehicle_Mass_Properties(Components.Mass_Properties): 
    """ The vehicle's mass properties.
        
            Assumptions:
                None
    
            Source:
                None
    """

    def __defaults__(self):
        """This sets the default values.
        
            Assumptions:
                None
    
            Source:
                None
            """         

        self.tag                         = 'mass_properties'
        self.operating_empty             = 0.0
        self.max_takeoff                 = 0.0
        self.takeoff                     = 0.0
        self.max_landing                 = 0.0
        self.landing                     = 0.0
        self.max_cargo                   = 0.0
        self.cargo                       = 0.0
        self.max_payload                 = 0.0
        self.payload                     = 0.0
        self.passenger                   = 0.0
        self.crew                        = 0.0
        self.max_fuel                    = 0.0
        self.fuel                        = 0.0
        self.max_zero_fuel               = 0.0
        self.center_of_gravity           = [[0.0,0.0,0.0]]
        self.zero_fuel_center_of_gravity = np.array([[0.0,0.0,0.0]])    
        
class Vehicle_Mass_Container(Components.Component.Container,Vehicle_Mass_Properties):
        
    def append(self,value,key=None):
        """ Appends the vehicle mass, but only let's one ever exist. Keeps the newest one
        
            Assumptions:
                None
    
            Source:
                None
        """      
        self.clear()
        for key in value.keys():
            self[key] = value[key]

    def get_children(self):
        """ Returns the components that can go inside
        
            Assumptions:
                None
    
            Source:
                None
        """       
        
        return [Vehicle_Mass_Properties]
