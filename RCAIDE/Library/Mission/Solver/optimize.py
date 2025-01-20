# RCAIDE/Library/Mission/Solver/optimize.py
# 
# Created:  Dec 2016, E. Botero
# Modified: Jun 2017, E. Botero
#           Mar 2020, M. Clarke
#           Apr 2020, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import scipy.optimize as opt
import numpy as np  

# ----------------------------------------------------------------------
#  Converge Root
# ----------------------------------------------------------------------

def converge_opt(segment):
    """
    Interfaces mission segment with optimization algorithms

    Parameters
    ----------
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    This function provides an interface between mission segments and optimization 
    algorithms to minimize an objective function while satisfying constraints.

    **Required Segment Components**

    segment:
        - state:
            unknowns : Data
                Variables to optimize
        - algorithm : str
            Optimization algorithm ('SLSQP' or 'SNOPT')
        - objective : str
            Name of objective function
        - lift_coefficient_limit : float
            Maximum allowable lift coefficient
        - altitude_end : float
            Target final altitude [m]

    **Calculation Process**
    1. Pack optimization variables
    2. Set up objective and constraint functions
    3. Define variable bounds
    4. Call selected optimizer:
       - SLSQP: Sequential Least Squares Programming
       - SNOPT: Sparse Nonlinear OPTimizer

    **Major Assumptions**
    * Problem is well-posed for optimization
    * Objective and constraints are continuous
    * Solution exists within bounds
    * Gradients are well-behaved

    Returns
    -------
    None
        Updates segment state directly with optimal solution

    See Also
    --------
    get_objective
    get_econstraints
    get_ieconstraints
    make_bnds
    """
    
    # pack up the array
    unknowns = segment.state.unknowns.pack_array()
    
    # Have the optimizer call the wrapper
    obj       = lambda unknowns:get_objective(unknowns,segment)   
    econ      = lambda unknowns:get_econstraints(unknowns,segment) 
    iecon     = lambda unknowns:get_ieconstraints(unknowns,segment)
    
    # Setup the bnds of the problem
    bnds = make_bnds(unknowns, segment)
    
    # Solve the problem, based on chosen algorithm
    if segment.algorithm == 'SLSQP':
        unknowns = opt.fmin_slsqp(obj,unknowns,f_eqcons=econ,f_ieqcons=iecon,bounds=bnds,iter=2000)
        
    elif segment.algorithm == 'SNOPT':
        
        # SNOPT imports
        import pyOpt
        import pyOpt.pySNOPT    
        
        # Have the optimizer call the wrapper
        obj_pyopt = lambda unknowns:get_problem_pyopt(unknowns,segment) 
    
        opt_prob = pyOpt.Optimization('RCAIDE',obj_pyopt)
        opt_prob.addObj(segment.objective)
    
        for ii in range(0,len(unknowns)):
            lbd = (bnds[ii][0])
            ubd = (bnds[ii][1])
            vartype = 'c'
            opt_prob.addVar(str(ii),vartype,lower=lbd,upper=ubd,value=unknowns[ii])  
    
        # Setup constraints
        segment_points = segment.state.numerics.number_of_control_points
        for ii in range(0,2*segment_points):
            opt_prob.addCon(str(ii), type='e', equal=0.)
        for ii in range(0,5*segment_points-1):
            opt_prob.addCon(str(ii+segment_points*2), type='i', lower=0.,upper=np.inf)
    
        print(opt_prob)
    
        snopt = pyOpt.pySNOPT.SNOPT()    
        outputs = snopt(opt_prob) 
    
        print(outputs)
        print(opt_prob.solution(0))

    return
    
# ----------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------
    
def get_objective(unknowns, segment):
    """
    Evaluates objective function for current optimization variables

    Parameters
    ----------
    unknowns : array_like
        Current optimization variables
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    Runs segment iteration process if unknowns have changed since last evaluation.

    Returns
    -------
    float
        Objective function value
    """
    
    if isinstance(unknowns,np.ndarray):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    if not np.all(segment.state.inputs_last == segment.state.unknowns):       
        segment.process.iterate(segment)
        
    objective = segment.state.objective_value
    
    return objective

def get_econstraints(unknowns, segment):
    """
    Evaluates equality constraints for current optimization variables

    Parameters
    ----------
    unknowns : array_like
        Current optimization variables
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    Runs segment iteration process if unknowns have changed since last evaluation.

    Returns
    -------
    ndarray
        Equality constraint values
    """
    
    if isinstance(unknowns,np.ndarray):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    if not np.all(segment.state.inputs_last == segment.state.unknowns):       
        segment.process.iterate(segment)

    constraints = segment.state.constraint_values
    
    return constraints

def make_bnds(unknowns, segment):
    """
    Creates bounds for optimization variables

    Parameters
    ----------
    unknowns : array_like
        Optimization variables
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    Sets physical bounds on:
    * Throttle: [0, 1]
    * Body angle: [0, π/2]
    * Flight path angle: [0, π/2]
    * Velocities: [0, 2000] m/s

    Returns
    -------
    list
        Tuples of (lower_bound, upper_bound) for each variable
    """

    ones    = segment.state.ones_row(1)
    ones_m1 = segment.state.ones_row_m1(1).resize(segment.state._size)
    ones_m2 = segment.state.ones_row_m2(1).resize(segment.state._size)
    
    throttle_bnds = ones*(0.,1.)
    body_angle    = ones*(0., np.pi/2.)
    gamma         = ones*(0., np.pi/2.)
    
    if segment.air_speed_end is None:
        vels      = ones_m1*(0.,2000.)
    elif segment.air_speed_end is not None:    
        vels      = ones_m2*(0.,2000.)
    
    bnds = np.vstack([throttle_bnds,gamma,body_angle,vels])
    
    bnds = list(map(tuple, bnds))
    
    return bnds

def get_ieconstraints(unknowns, segment):
    """
    Evaluates inequality constraints for current optimization variables

    Parameters
    ----------
    unknowns : array_like
        Current optimization variables
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    Enforces physical constraints on:
    * Time progression (forward only)
    * Lift coefficient (0 < CL < limit)
    * Altitude (positive)
    * Acceleration (positive)

    Returns
    -------
    ndarray
        Inequality constraint values
    """

    if isinstance(unknowns,np.ndarray):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    if not np.all(segment.state.inputs_last == segment.state.unknowns):
        segment.process.iterate(segment)
    
    # Time goes forward, not backward
    t_final = segment.state.conditions.frames.inertial.time[-1,0]
    time_con = (segment.state.conditions.frames.inertial.time[1:,0] - segment.state.conditions.frames.inertial.time[0:-1,0])/t_final
    
    # Less than a specified CL limit
    lift_coefficient_limit = segment.lift_coefficient_limit
    CL_con = (lift_coefficient_limit  - segment.state.conditions.aerodynamics.coefficients.lift.total[:,0])/lift_coefficient_limit
    
    CL_con2   = segment.state.conditions.aerodynamics.coefficients.lift.total[:,0]
    
    # Altitudes are greater than 0
    alt_con = segment.state.conditions.freestream.altitude[:,0]/segment.altitude_end
    
    # Acceleration constraint, go faster not slower
    acc_con   = segment.state.conditions.frames.inertial.acceleration_vector[:,0]
    
    constraints = np.concatenate((time_con,CL_con,CL_con2,alt_con,acc_con))
    
    return constraints

def get_problem_pyopt(unknowns, segment):
    """
    Formats optimization problem for pyOpt interface

    Parameters
    ----------
    unknowns : array_like
        Current optimization variables
    segment : Segment
        The mission segment being analyzed

    Notes
    -----
    Combines objective and all constraints into format required by pyOpt.

    Returns
    -------
    tuple
        (objective_value, constraint_list, fail_status)
    """

    if isinstance(unknowns,np.ndarray):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    if not np.all(segment.state.inputs_last == segment.state.unknowns):
        segment.process.iterate(segment)
        
    obj      = segment.state.objective_value
    
    # Time goes forward, not backward
    t_final  = segment.state.conditions.frames.inertial.time[-1,0]
    time_con = (segment.state.conditions.frames.inertial.time[1:,0] - segment.state.conditions.frames.inertial.time[0:-1,0])/t_final
    
    # Less than a specified CL limit
    lift_coefficient_limit = segment.lift_coefficient_limit 
    CL_con   = (lift_coefficient_limit  - segment.state.conditions.aerodynamics.coefficients.lift.total[:,0])/lift_coefficient_limit
    
    CL_con2   = segment.state.conditions.aerodynamics.coefficients.lift.total[:,0]
    
    # Altitudes are greater than 0
    alt_con = segment.state.conditions.freestream.altitude[:,0]/segment.altitude_end
    
    # Acceleration constraint, go faster not slower
    acc_con   = segment.state.conditions.frames.inertial.acceleration_vector[:,0]
    
    # Put the equality and inequality constraints together
    constraints = np.concatenate((segment.state.constraint_values,time_con,CL_con,alt_con,acc_con,CL_con2))
    
    
    obj   = segment.state.objective_value
    const = constraints.tolist()
    fail  = np.array(np.isnan(obj) or np.isnan(np.array(const).any())).astype(int)    
    
    return obj,const,fail