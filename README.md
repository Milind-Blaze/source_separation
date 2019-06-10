# Source separation    
   
## Objective:    
This repository contains implementations of various source separation algorithms in Python. Presently, all algorithms are based on non-negative matrix factorization and its variants. More implementations using other techniques will follow.  While the presentation of the NMF algrithms and its variants is work done as a part of the course EE4902, this also contributed quite significantly to a [course project](https://www.youtube.com/watch?v=vc-WlAqv17c) completed as a part of the course EE5120 at IIT Madras. 
     

## Usage on Linux:         

All code is written in Python (and functional in version 3.6.8) and uses the libraries listed in ```environment.yml```. This assumes that you have miniconda installed. If you do not, get it [here](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html).     

Create a conda environment in which all the code can be run using the following command in the terminal:       
```
conda env create -f environment.yml
```     

This will create an environment named source_separation (name can be changed by changing the value of "name" in the ```environment.yml``` file). Activate the environment using 
```
conda activate source_separation
```     

and run the desired script as described.
            
## Directories:           
     
__Monoaural_source_separation_using_Non-negative_matrix_factorization__: Code for source separation based on the technique described in the paper [Monaural Sound Source Separation by NonnegativeMatrix Factorization With Temporal Continuity and Sparseness Criteria](http://www.cs.tut.fi/sgn/arg/music/tuomasv/virtanen_taslp2007.pdf).        
__sourcesep__: Modules for all implemented source separation algorithms       
__tools__: Modules for helper functions      
