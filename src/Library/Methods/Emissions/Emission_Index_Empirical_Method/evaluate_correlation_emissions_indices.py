# RCAIDE/Library/Methods/Emissions/evaluate_correlation_emissions_indices.py
#  
# Created:  Jul 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import  RCAIDE
from RCAIDE.Framework.Core import Data 
 
# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  evaluate_correlation_emissions_indices
# ---------------------------------------------------------------------------------------------------------------------- 
def evaluate_correlation_emissions_indices(segment,settings,vehicle):
    """ Computes the CO2 equivalent emissions from aircraft propulsors with combustor compoments
    using emissions indices correlated to various fuels
    
    Assumtion:
    None
    
    Source
    None
    
    Args:
    emissions_analysis 
    segment
    
    Returns:
    None  
    """    
    # unpack
    state      = segment.state
    I          = state.numerics.time.integrate
    NOx_total  = 0 * state.ones_row(1)  
    CO2_total  = 0 * state.ones_row(1) 
    SO2_total  = 0 * state.ones_row(1) 
    H2O_total  = 0 * state.ones_row(1) 
    Soot_total = 0 * state.ones_row(1) 

    for network in vehicle.networks:  
        for fuel_line in network.fuel_lines:
            if fuel_line.active: 
                for fuel_tank in fuel_line.fuel_tanks:
                    mdot = 0. * state.ones_row(1)   
                    for propulsor in network.propulsors:
                        for source in (propulsor.active_fuel_tanks):
                            if fuel_tank.tag == source:  
                                propulsor_results =  state.conditions.energy[propulsor.tag]
                                fuel =  fuel_tank.fuel
                                if (type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turbofan) or \
                                    type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turboprop or \
                                    type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turboshaft or \
                                    type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turbojet:    
                         
                                    EI_NOx  = fuel.emission_indices.NOx
                                    EI_CO2  = fuel.emission_indices.CO2 
                                    EI_H2O  = fuel.emission_indices.H2O
                                    EI_SO2  = fuel.emission_indices.SO2
                                    EI_Soot = fuel.emission_indices.Soot  
                                    
                                    mdot = propulsor_results.fuel_flow_rate
                                     
                                    # Integrate them over the entire segment
                                    NOx_total  += np.dot(I,mdot*EI_NOx)
                                    CO2_total  += np.dot(I,mdot*EI_CO2)
                                    SO2_total  += np.dot(I,mdot*EI_SO2)
                                    H2O_total  += np.dot(I,mdot*EI_H2O) 
                                    Soot_total += np.dot(I,mdot*EI_Soot)
                                     
         
    flight_range    =  state.conditions.frames.inertial.aircraft_range 
    Contrails_total =  (flight_range -   flight_range[0]) /1000 * fuel.global_warming_potential_100.Contrails

    emissions                 = Data()
    emissions.total           = Data()
    emissions.index           = Data() 
    emissions.total.NOx       = NOx_total   * fuel.global_warming_potential_100.NOx 
    emissions.total.CO2       = CO2_total   * fuel.global_warming_potential_100.CO2
    emissions.total.H2O       = H2O_total   * fuel.global_warming_potential_100.H2O  
    emissions.total.SO2       = SO2_total   * fuel.global_warming_potential_100.SO2  
    emissions.total.Soot      = Soot_total  * fuel.global_warming_potential_100.Soot 
    emissions.total.Contrails = Contrails_total   
    emissions.index.NOx       = EI_NOx   * state.ones_row(1)
    emissions.index.CO2       = EI_CO2   * state.ones_row(1)
    emissions.index.H2O       = EI_H2O   * state.ones_row(1)
    emissions.index.SO2       = EI_SO2   * state.ones_row(1)
    emissions.index.Soot      = EI_Soot  * state.ones_row(1)
    
    state.conditions.emissions =  emissions
    return   

