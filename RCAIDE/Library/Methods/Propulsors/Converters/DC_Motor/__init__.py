# RCAIDE/Library/Methods/Propulsors/Converters/DC_Motor/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .append_motor_conditions           import append_motor_conditions  
from .compute_motor_performance         import compute_RPM_and_torque_from_power_coefficent_and_voltage
from .compute_motor_performance         import compute_current_from_RPM_and_voltage 
from .design_motor                      import design_motor
