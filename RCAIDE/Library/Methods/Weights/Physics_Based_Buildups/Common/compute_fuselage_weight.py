# RCAIDE/Library/Methods/Weights/Buildups/Common/compute_fuselage_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
# RCAIDE imports   
from RCAIDE.Library.Attributes.Materials import Bidirectional_Carbon_Fiber, Carbon_Fiber_Honeycomb, Paint, Unidirectional_Carbon_Fiber, Acrylic, Steel

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Compute boom weight
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_fuselage_weight(fuse,maxSpan, MTOW, 
             maximum_g_load = 3.8,
             landing_impact_factor = 3.5,
             safety_factor = 1.5):
    """ Calculates the structural mass of a fuselage for an eVTOL vehicle,
        assuming a structural keel taking bending an torsional loads.
        
        Assumptions:  
        If vehicle model does not have material properties assigned, appropriate
        assumptions are made based on RCAIDE's Solids Attributes library.
        
        Sources:
        Project Vahana Conceptual Trade Study

        Inputs:

            config                      RCAIDE Vehicle Configuration
            max_g_load                  Max Accelerative Load During Flight [Unitless]
            landing_impact_factor       Maximum Load Multiplier on Landing  [Unitless]

        Outputs:

            weight:                 Estimated Fuselage Mass             [kg]
        
        Properties Used:
        Material Properties of Imported RCAIDE Solids
    """

    #-------------------------------------------------------------------------------
    # Unpack Inputs
    #------------------------------------------------------------------------------- 
    fLength = fuse.lengths.total
    fWidth  = fuse.width
    fHeight = fuse.heights.maximum
    G_max   = maximum_g_load
    LIF     = landing_impact_factor
    SF      = safety_factor

    #-------------------------------------------------------------------------------
    # Unpack Material Properties
    #-------------------------------------------------------------------------------

    try:
        rbmMat = fuse.keel_materials.root_bending_moment_carrier
    except AttributeError:
        rbmMat = Unidirectional_Carbon_Fiber()
    rbmDen = rbmMat.density
    rbmUTS = rbmMat.ultimate_tensile_strength

    try:
        shearMat = fuse.keel_materials.shear_carrier
    except AttributeError:
        shearMat = Bidirectional_Carbon_Fiber()
    shearDen = shearMat.density
    shearUSS = shearMat.ultimate_shear_strength

    try:
        bearingMat = fuse.keel_materials.bearing_carrier
    except AttributeError:
        bearingMat = Bidirectional_Carbon_Fiber()
    bearingDen = bearingMat.density
    bearingUBS = bearingMat.ultimate_bearing_strength

    try:
        boltMat = fuse.materials.bolt_materials.landing_pad_bolt
    except AttributeError:
        boltMat = Steel()
    boltUSS = boltMat.ultimate_shear_strength


    # Calculate Skin & Canopy Weight Per Unit Area (arealWeight) based on material

    try:
        skinArealWeight = np.sum([(mat.minimum_gage_thickness * mat.density) for mat in fuse.skin_materials])
    except AttributeError:
        skinArealWeight = 1.2995 # Stack of bidirectional CFRP, Honeycomb Core, Paint

    try:
        canopyArealWeight = np.sum([(mat.minimum_gage_thickness * mat.density) for mat in fuse.canopy_materials])
    except AttributeError:
        canopyArealWeight = 3.7465 # Acrylic

    # Calculate fuselage area (using assumption of ellipsoid), and weight:

    S_wet = 4 * np.pi * (((fLength * fWidth/4)**1.6
        + (fLength * fHeight/4)**1.6
        + (fWidth * fHeight/4)**1.6)/3)**(1/1.6)
    skinMass = S_wet * skinArealWeight

    # Calculate the mass of a structural bulkhead

    bulkheadMass = 3 * np.pi * fHeight * fWidth/4 * skinArealWeight

    # Calculate the mass of a canopy

    canopyMass = S_wet/8 * canopyArealWeight

    # Calculate keel mass needed to carry lifting moment

    L_max       = G_max * MTOW * 9.8 * SF  # Max Lifting Load
    M_lift      = L_max * fLength/2.       # Max Moment Due to Lift
    beamWidth   = fWidth/3.                # Allowable Keel Width
    beamHeight  = fHeight/10.              # Allowable Keel Height

    beamArea    = M_lift * beamHeight/(4*rbmUTS*(beamHeight/2)**2)
    massKeel    = beamArea * fLength * rbmDen

    # Calculate keel mass needed to carry wing bending moment shear

    M_bend      = L_max/2 * maxSpan/2                           # Max Bending Moment
    beamArea    = beamHeight * beamWidth                        # Enclosed Beam Area
    beamThk     = 0.5 * M_bend/(shearUSS * beamArea)            # Beam Thickness
    massKeel   += 2*(beamHeight + beamWidth)*beamThk*shearDen

    # Calculate keel mass needed to carry landing impact load assuming

    F_landing   = SF * MTOW * 9.8 * LIF * 0.6403        # Side Landing Force
    boltArea    = F_landing/boltUSS                     # Required Bolt Area
    boltDiam    = 2 * np.sqrt(boltArea/np.pi)           # Bolt Diameter
    lamThk      = F_landing/(boltDiam*bearingUBS)       # Laminate Thickness
    lamVol      = (np.pi*(20*lamThk)**2)*(lamThk/3)     # Laminate Pad volume
    massKeel   += 4*lamVol*bearingDen                   # Mass of 4 Pads

    # Calculate total mass as the sum of skin mass, bulkhead mass, canopy pass,
    # and keel mass. Called weight by RCAIDE convention

    weight = skinMass + bulkheadMass + canopyMass + massKeel

    return weight