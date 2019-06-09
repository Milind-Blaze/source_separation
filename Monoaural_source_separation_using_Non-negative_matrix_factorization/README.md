# Directory: Monoaural_source_separation_using_Non-negative_matrix_factorization    

This folder contains a rudimentary implementation of the algorithm presented in [this](https://ieeexplore.ieee.org/abstract/document/4100700) paper and a few experiments performed to reproduce results presented in the paper and wherever possible, extend the results by experimenting with various parameters such as windows, frame size and so forth. Each subfolder contains the entire experimental framework to obtain the results - the basic code to run one trial and a bash script with details of all the experiments run.


## Contents   

```Monoaural_source_separation_Frobenius_norm.ipynb```: A jupyter notebook working with one of the audios made available by the author visualizing the audio, performing source separation with plain NMF and the algorithm proposed.
__scripts__: Folder containing the setup for the three experiments performed to evaluate the (relative) performance of the algorithms of interest for the task of source separation.    

## Useful links   
  
- [Original paper](https://ieeexplore.ieee.org/abstract/document/4100700)
- [Audio files made available](http://www.cs.tut.fi/sgn/arg/music/tuomasv/temp-nmf/)