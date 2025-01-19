# RCAIDE/Library/Mission/Common/Update/noise.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
# noise
# ---------------------------------------------------------------------------------------------------------------------- 
def noise(segment):
    """
    Updates noise calculations for current segment

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function evaluates the noise model if one is defined for the
    segment. It handles all types of noise calculations including:
    - Propulsion noise
    - Aerodynamic noise
    - Total vehicle noise

    **Required Segment Components**

    segment:
        analyses:
            noise : Model, optional
                Noise analysis model

    **Major Assumptions**
    * Valid noise model if defined
    * Compatible segment conditions
    * Well-defined operating state
    * Appropriate atmospheric conditions

    Returns
    -------
    None
        Updates segment conditions directly through noise model:
        - conditions.noise:
            - total_SPL : array
                Total sound pressure level [dB]
            - component_noise : dict
                Individual noise source levels


    """   
    noise_model = segment.analyses.noise
    
    if noise_model:
        noise_model.evaluate_noise(segment)    