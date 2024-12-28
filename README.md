<p align="center">
  <img src="https://github.com/leadsgroup/RCAIDE_Website/blob/main/assets/img/RCAIDE_Logo_No_Background.png" width=25% height=25%> 
</p> 

# 
<div align="center">

[![CI](https://github.com/leadsgroup/RCAIDE_LEADS/actions/workflows/CI.yml/badge.svg)](https://github.com/leadsgroup/RCAIDE_LEADS/actions/workflows/CI.yml)  
[![Documentation](https://github.com/leadsgroup/RCAIDE_LEADS/actions/workflows/sphinx_docs.yml/badge.svg)](https://github.com/leadsgroup/RCAIDE_LEADS/actions/workflows/sphinx_docs.yml)
[![codecov](https://codecov.io/gh/leadsgroup/RCAIDE_LEADS/graph/badge.svg?token=WZOFW5EKWJ)](https://codecov.io/gh/leadsgroup/RCAIDE_LEADS)


</div>

[RCAIDE: Research Community Aircraft Interdisciplinary Design Environment]([link](https://www.rcaide.leadsresearchgroup.com/))
=======

The Research Community Aircraft Interdisciplinary Design Environment, or RCAIDE  (pronounced “arcade”) is a powerful open-source Python platform that revolutionizes aircraft design and analysis. From commercial airliners to UAVs and next-generation hybrid-electric aircraft, RCAIDE provides comprehensive multi-disciplinary analysis tools backed by validated engineering methods. Our streamlined workflow and modular architecture help aerospace engineers and researchers accelerate development cycles and explore innovative designs with confidence. RCAIDE-LEADS is a form from RCAIDE, developed and maintained by the [Lab for Electric Aircraft Design and Sustainability](https://www.leadsresearchgroup.com/)
 
## Transinitign from SUAVE Legacy 
RCAIDE was built to allow users to transition their work to smoothly from SUAVE to RCAIDE. RCAIDE's code is architected in such a way that a native SUAVE user can understand it, but breaks free of some of the antiquated nomenclature. 
 
## Code Architecture 
The code is arranged into repositories that house native data structures, functions, components, and subroutines for discipline analyses and support number-crunching operations. This allows developers or avid users seeking to modify the source code to navigate intuitively. Solely written in Python, an RCAIDE installation
appears in one repository that is itself organized into two secondary-level repositories: 
* **RCAIDE** sub-directory, where their source code resides
* **Regressions** sub-directory, where unit tests for verification and validation are performed.

```mermaid
%%{init: {'flowchart': {'curve': 'linear', 'nodeSpacing': 50, 'rankSpacing': 50}}}%%
flowchart LR
    RCAIDE_LEADS[RCAIDE_LEADS]
    RCADIE[RCADIE]
    Regressions[Regressions]
    
    RCAIDE_LEADS ---> RCADIE
    RCAIDE_LEADS ---> Regressions

    style RCAIDE_LEADS fill:#0d6dc5,color:#fff
    style RCADIE fill:#09d0d9,color:#fff
    style Regressions fill:#09d0d9,color:#fff
```
The RCAIDE subdirectory is arranged into frameworks and methods modules. Its predecessor, SUAVE, was written primarily as a superseding framework. Think of framework modules as the glue or roadmap that connects all the functions housed in the Library folder. The framework folder mainly comprises core data structures, classes instances of the various methods within the code, the mission and energy networks and the optimization framework. The Library module comprises five tertiary submodules: Attributes, Components,  Methods, Mission and Plots.

```mermaid
%%{init: {'flowchart': {'curve': 'linear', 'nodeSpacing': 50, 'rankSpacing': 50}}}%%
flowchart TB
    RCADIE[RCADIE] --> Framework
    RCADIE --> Libraries
    
    %% Framework components
    Framework --> Mission
    Framework --> Analyses
    Framework --> Optimization
    Framework --> Data
    
    %% Library components
    Libraries --> Aerodynamics
    Libraries --> Noise
    Libraries --> Costs
    Libraries --> Stability
    Libraries --> Energy
    Libraries --> FlightPerf[Flight Performance]
    Libraries --> Weights
    
    %% Styling
    style RCADIE fill:#09d0d9,color:#fff
    style Framework fill:#0fcf99,color:#fff
    style Libraries fill:#0fcf99,color:#fff
    
    %% Framework children styling - Burgundy
    style Mission fill:#800020,color:#fff
    style Analyses fill:#800020,color:#fff
    style Optimization fill:#800020,color:#fff
    style Data fill:#800020,color:#fff
    
    %% Libraries children styling - Purple
    style Aerodynamics fill:#5D3FD3,color:#fff
    style Noise fill:#5D3FD3,color:#fff
    style Costs fill:#5D3FD3,color:#fff
    style Stability fill:#5D3FD3,color:#fff
    style Energy fill:#5D3FD3,color:#fff
    style FlightPerf fill:#5D3FD3,color:#fff
    style Weights fill:#5D3FD3,color:#fff
```
## Capabilities of RCAIDE
RCAIDE currently possesses the ability to perform the following analyses, each at varying levels of fidelity. Here, we define fidelity as a level of accuracy to the actual physical value. As the level of fidelity increases, so does accuracy. However, this comes with the penalty of computational time and memory.  Having multi-fidelity capability allows RCAIDE to perform energy network analysis, complete flight  vehicle mission analysis, multi-fidelity optimization, design space exploration, artificial intelligence, and model-based systems engineering. Here are some notable use cases of RCAIDE:

* Mission Analysis   
* Optimization 
    * Gradient-based optimization
    * Non-gradient-based optimization
    * Multi-fidelity optimization
* Performance Analysis
    * Payload range 
    * Aerodynamic analysis
    * V-N diagrams
    * Propeller analysis 
    * Takeoff Field Length Estimation
* Weights Analysis
    * Operating empty weight, zero-fuel weight estimation
    * Component weight estimation 
    * Center of gravity estimation
    * Moment of inertia estimation 


## Installing RCAIDE 
RCAIDE is available on GNU/Linux, MacOS and Windows. We strongly recommend installing RCAIDE within a Python virtual environment to avoid altering any distribution of Python files. Please review the documentation for instructions on creating a virtual environment for RCAIDE.

* [See Installation Instructions](https://www.docs.rcaide.leadsresearchgroup.com/install.html)
* Using pip (coming soon) 
* Using conda (coming soon) 

## Tutorials
[See Tutorials here](https://docs.rcaide.leadsresearchgroup.com/tutorials.html)

## Citing RCAIDE
(coming soon) 

## Contributing to RCAIDE
**Contributing Institutions** 
* Aerospace Research Community, LLC
* [University of Illinois Lab for Electric Aircraft Design and Sustainability](https://www.leadsresearchgroup.com/)
* [Stanford University Aerospace Design Lab](http://adl.stanford.edu)
  
**Contributing Developers**  
* Matthew Clarke 
* Emilio Botero 
* Jordan Smart 
* Racheal Erhard
* [University of Illinois Lab for Electric Aircraft Design and Sustainability](https://www.leadsresearchgroup.com/)) 
* [Stanford University Aerospace Design Lab](http://adl.stanford.edu)

**Getting Involved**   

If you'd like to help us develop RCAIDE by adding new methods, writing documentation, or fixing embarrassing bugs, please look at these [guidelines](https://www.docs.rcaide.leadsresearchgroup.com/contributing.html) first.

Submit improvements or new features with a [pull request](https://github.com/leadsgroup/RCAIDE_LEADS/pulls)

## Get in touch

Share feedback, report issues, and request features via or [Github Issues](https://github.com/leadsgroup/RCAIDE_LEADS/issues)

Engage with peers and maintainers in [Discussions](https://github.com/leadsgroup/RCAIDE_LEADS/discussions)


