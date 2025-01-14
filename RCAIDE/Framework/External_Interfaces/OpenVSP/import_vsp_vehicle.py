# RCAIDE/Framework/External_Interfaces/OpenVSP/import_vsp_vehicle.py

# Created:  Jun 2018, T. St Francis
# Modified: Aug 2018, T. St Francis
#           Jan 2020, T. MacDonald
#           Jul 2020, E. Botero
#           Sep 2021, R. Erhard
#           Dec 2021, E. Botero

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports 
import RCAIDE
from  RCAIDE.Framework.Core import Units, Data, Container 
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_rotor           import read_vsp_rotor
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_fuselage         import read_vsp_fuselage
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_wing             import read_vsp_wing
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_nacelle          import read_vsp_nacelle
from RCAIDE.Framework.External_Interfaces.OpenVSP.get_vsp_measurements import get_vsp_measurements


from copy import deepcopy

try:
    import vsp as vsp
except ImportError:
    try:
        import openvsp as vsp
    except ImportError:
        # This allows RCAIDE to build without OpenVSP
        pass
    
# ---------------------------------------------------------------------------------------------------------------------- 
#  vsp read
# ---------------------------------------------------------------------------------------------------------------------- 
def import_vsp_vehicle(tag, network_type=None, propulsor_type=None, units_type='SI', use_scaling=True, calculate_wetted_area=True):
    """
    Reads an OpenVSP vehicle geometry and converts it to RCAIDE vehicle format

    Parameters
    ----------
    tag : str
        Name of .vsp3 file to import
    network_type : RCAIDE.Framework.Networks.Network
        Type of energy network to use
    propulsor_type : RCAIDE.Library.Components.Propulsors.Propulsor
        Type of propulsion system to use
    units_type : {'SI', 'imperial', 'inches'}, optional
        Units system to use
        Default: 'SI'
    use_scaling : bool, optional
        Whether to use OpenVSP scaling
        Default: True
    calculate_wetted_area : bool, optional
        Whether to compute wetted areas
        Default: True

    Returns
    -------
    vehicle : RCAIDE.Vehicle
        Vehicle object containing imported geometry with components:
        
        Wings.Wing.*
            - origin [m]
            - spans.projected [m]
            - chords.root/tip [m]
            - aspect_ratio [-]
            - sweeps.quarter_chord [rad]
            - twists.root/tip [rad]
            - thickness_to_chord [-]
            - dihedral [rad]
            - areas.reference/wetted [m^2]
            - Segments with airfoil data
            
        Fuselages.Fuselage.*
            - origin [m]
            - width [m]
            - lengths.total/nose/tail [m] 
            - heights.maximum/at_quarter_length [m]
            - effective_diameter [m]
            - fineness.nose/tail [-]
            - areas.wetted [m^2]
            - segments with shape data
            
        Propellers.Propeller.*
            - location [rad]
            - rotation [rad]
            - tip_radius [m]
            - hub_radius [m]

    Notes
    -----
    This function imports OpenVSP geometry into RCAIDE format, handling wings,
    fuselages, propellers and other components.

    **Major Assumptions**
    * OpenVSP vehicle uses conventional shapes for fuselages, wings, rotors
    * Fuselage is designed realistically without superficial elements
    * Fuselage origin at nose
    * Single geometry per fuselage (no additional components)
    * Written for OpenVSP 3.21.1

    **Extra modules required**
    * OpenVSP (vsp or openvsp module)

    Raises
    ------
    Exception
        If network_type or propulsor_type not specified
    """

    if isinstance(network_type,RCAIDE.Framework.Networks.Network) != True:
        raise Exception('Vehicle energy network type must be defined. \n Choose from list in RCAIDE.Framework.Networks') 

    if isinstance(propulsor_type,RCAIDE.Library.Components.Propulsors.Propulsor ) != True:
        raise Exception('Vehicle propulsor type must be defined. \n Choose from list in RCAIDE.Library.Compoments.Propulsors')     

    vsp.ClearVSPModel() 
    vsp.ReadVSPFile(tag)	

    vsp_fuselages     = []
    vsp_wings         = []	
    vsp_rotors         = [] 
    vsp_nacelles      = [] 
    vsp_nacelle_type  = []
    
    vsp_geoms         = vsp.FindGeoms()
    geom_names        = []

    vehicle           = RCAIDE.Vehicle()
    vehicle.tag       = tag 

    if units_type == 'SI':
        units_type = 'SI' 
    elif units_type == 'inches':
        units_type = 'inches'	
    else:
        units_type = 'imperial'	

    # The two for-loops below are in anticipation of an OpenVSP API update with a call for GETGEOMTYPE.
    # This print function allows user to enter VSP GeomID manually as first argument in import_vsp_vehicle functions.

    print("VSP geometry IDs: ")	

    # Label each geom type by storing its VSP geom ID. 

    for geom in vsp_geoms: 
        geom_name = vsp.GetGeomName(geom)
        geom_names.append(geom_name)
        print(str(geom_name) + ': ' + geom)
        
    
    # ------------------------------------------------------------------        
    # Use OpenVSP to calculate wetted area
    # ------------------------------------------------------------------
    if calculate_wetted_area:
        measurements = get_vsp_measurements()
        if units_type == 'SI':
            units_factor = Units.meter * 1.
        elif units_type == 'imperial':
            units_factor = Units.foot * 1.
        elif units_type == 'inches':
            units_factor = Units.inch * 1.	         
        
    # ------------------------------------------------------------------
    # AUTOMATIC VSP ENTRY & PROCESSING
    # ------------------------------------------------------------------		

    for geom in vsp_geoms:
        geom_name = vsp.GetGeomName(geom)
        geom_type = vsp.GetGeomTypeName(str(geom))

        if geom_type == 'Fuselage':
            vsp_fuselages.append(geom)
        if geom_type == 'Wing':
            vsp_wings.append(geom)
        if geom_type == 'Propeller':
            vsp_rotors.append(geom) 
        if (geom_type == 'Stack') or (geom_type == 'BodyOfRevolution'):
            vsp_nacelle_type.append(geom_type)
            vsp_nacelles.append(geom) 
        
    # ------------------------------------------------------------------			
    # Read Fuselages 
    # ------------------------------------------------------------------			    
    for fuselage_id in vsp_fuselages:
        sym_planar = vsp.GetParmVal(fuselage_id, 'Sym_Planar_Flag', 'Sym') # Check for symmetry
        sym_origin = vsp.GetParmVal(fuselage_id, 'Sym_Ancestor_Origin_Flag', 'Sym') 
        if sym_planar == 2. and sym_origin == 1.:  
            num_fus  = 2 
            sym_flag = [1,-1]
        else: 
            num_fus  = 1 
            sym_flag = [1] 
        for fux_idx in range(num_fus):	# loop through fuselages on aircraft 
            fuselage = read_vsp_fuselage(fuselage_id,fux_idx,sym_flag[fux_idx],units_type,use_scaling)
            
            if calculate_wetted_area:
                fuselage.areas.wetted = measurements[vsp.GetGeomName(fuselage_id)] * (units_factor**2)
            
            vehicle.append_component(fuselage)
        
    # ------------------------------------------------------------------			    
    # Read Wings 
    # ------------------------------------------------------------------			
    for wing_id in vsp_wings:
        wing = read_vsp_wing(wing_id, units_type,use_scaling)
        if calculate_wetted_area:
            wing.areas.wetted = measurements[vsp.GetGeomName(wing_id)] * (units_factor**2)  
        vehicle.append_component(wing)		 
        
    # ------------------------------------------------------------------			    
    # Read Enegy Network 
    # ------------------------------------------------------------------
    network =  deepcopy(network_type)  
    i       = 0
    # Condition when equal number of rotors and nacelles are defined 
    if len(vsp_rotors) == len(vsp_nacelles):
        for idx , (rotor_id,nacelle_id) in enumerate(zip(vsp_rotors, vsp_nacelles)):
            # define new propulsor 
            propulsor = deepcopy(propulsor_type) 
            propulsor.tag =  'propulsor_' +  str(i+1)
            
            # Rotor 
            rotor           = read_vsp_rotor(rotor_id,units_type)
            rotor.tag       = vsp.GetGeomName(rotor_id) 
            propulsor.rotor = rotor
            
            # Nacelle 
            nacelle = read_vsp_nacelle(nacelle_id,vsp_nacelle_type[idx], units_type)
            if calculate_wetted_area:
                nacelle.areas.wetted = measurements[vsp.GetGeomName(nacelle_id)] * (units_factor**2)           
            propulsor.nacelle = nacelle          
             
            # Append to Network 
            network.propulsors.append(propulsor)
            
            
            # If symmetry is defined
            if vsp.GetParmVal(rotor_id, 'Sym_Planar_Flag', 'Sym')== 2.0:
                # update index 
                i += 1
                
                # define new propulsor 
                propulsor =  deepcopy(propulsor_type) 
                propulsor.tag =  'propulsor_' +  str(i+1)
                
                
                # Rotor 
                rotor_sym = deepcopy(rotor)
                rotor_sym.origin[0][1] = - rotor_sym.origin[0][1] 
                propulsor.rotor = rotor_sym
                
        
                # Nacelle 
                nacelle_sym = deepcopy(nacelle)
                nacelle_sym.origin[0][1] = - nacelle_sym.origin[0][1]  
                nacelle_sym.areas.wetted = nacelle.areas.wetted
                propulsor.nacelle = nacelle          
                 
                # Append to Network             
                network.propulsors.append(propulsor)
                
    # Condition when only nacelles are defined 
    elif (len(vsp_rotors) ==  0) and (len(vsp_nacelles) > 0):

        for idx ,  nacelle_id in enumerate(vsp_nacelles):
            # define new propulsor 
            propulsor = deepcopy(propulsor_type) 
            propulsor.tag =  'propulsor_' +  str(i+1)
             
            # Nacelle 
            nacelle = read_vsp_nacelle(nacelle_id,vsp_nacelle_type[idx], units_type)
            if calculate_wetted_area:
                nacelle.areas.wetted = measurements[vsp.GetGeomName(nacelle_id)] * (units_factor**2)           
            propulsor.nacelle = nacelle          
             
            # Append to Network 
            network.propulsors.append(propulsor)
            
            
            # If symmetry is defined
            if vsp.GetParmVal(nacelle_id, 'Sym_Planar_Flag', 'Sym')== 2.0:
                # update index 
                i += 1
                
                # define new propulsor 
                propulsor =  deepcopy(propulsor_type) 
                propulsor.tag =  'propulsor_' +  str(i+1)
                 
        
                # Nacelle 
                nacelle_sym = deepcopy(nacelle)
                nacelle_sym.origin[0][1] = - nacelle_sym.origin[0][1]  
                nacelle_sym.areas.wetted = nacelle.areas.wetted
                propulsor.nacelle = nacelle          
                 
                # Append to Network             
                network.propulsors.append(propulsor)
                
        

    # Condition when only rotors are defined 
    elif (len(vsp_rotors) >  0) and (len(vsp_nacelles) == 0):
        for idx , rotor_id in enumerate( vsp_rotors):
            # define new propulsor 
            propulsor = deepcopy(propulsor_type) 
            propulsor.tag =  'propulsor_' +  str(i+1)
            
            # Rotor 
            rotor           = read_vsp_rotor(rotor_id,units_type)
            rotor.tag       = vsp.GetGeomName(rotor_id) 
            propulsor.rotor = rotor
            
            # Append to Network 
            network.propulsors.append(propulsor)
            
            
            # If symmetry is defined
            if vsp.GetParmVal(rotor_id, 'Sym_Planar_Flag', 'Sym')== 2.0:
                # update index 
                i += 1
                
                # define new propulsor 
                propulsor =  deepcopy(propulsor_type) 
                propulsor.tag =  'propulsor_' +  str(i+1)
                
                
                # Rotor 
                rotor_sym = deepcopy(rotor)
                rotor_sym.origin[0][1] = - rotor_sym.origin[0][1] 
                propulsor.rotor = rotor_sym  
                propulsor.nacelle = nacelle          
                 
                # Append to Network             
                network.propulsors.append(propulsor) 
            
    else:
        print ('Unequal numbers of rotors and nacelles defined. Skipping propulsor definition.') 
                
    vehicle.networks.append(network)

    return vehicle