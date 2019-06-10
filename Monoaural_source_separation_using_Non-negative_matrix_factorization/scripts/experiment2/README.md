# Directory: experiment2    

This experiment studies the variation of the SNR of the proposed algorithm with variation in the values of alpha and beta. The objective is to determine what the best combination of the values alpha and beta is to obtain the highest SNR for any given number of components. In each trial of the experiment, the proposed algorithm with the temporal continuity and sparseness criteria is run for a given number of components and the variation of SNR obtained with the variation of each of alpha and beta values while the other is kept at zero. This experiment is repeated for different "number of component" values and an attempt is made to determine what the optimal setting of alpha and beta values is.

## Contents  

### experiment2.py

Runs one trial of the experiment described above.  

__Usage__  
Run as   
```
python experiment2.py audio_folder audio_name destination_folder r alpha beta --numiter *numiter_val* --frame_size *framesize_time* --overlap *overlap_fraction*
```   
audio_folder: path to folder containing the source (named as orig*n*.wav) and reference components (named as separated*n*\_*m*.wav). The script supports only .wav files.     
audio_name: name of the audio. If the source file is orig4.wav, then this parameter is orig4.     
destination_folder: path to folder where time domain plots of the audios (source and separated) and the resulting plots (.png) are stored.    
r: number of components to be used for separation each of which is assigned to a constituent source. Must be greater than the number of separated*n*\_*m*.wav files present in audio_folder    
alpha: lower bound of the weights associated with the temporal continuity and  sparseness criteria loss functions. The weights are varied logarithmically in the interval [alpha, beta]. The number of points can be adjusted by adjusting the num_alphas variable in experiment2.py.             
beta: upper bound of the weights associated with the temporal continuity and sparseness criteria loss functions. The weights are varied logarithmically in the interval [alpha, beta]. The number of points can be adjusted by adjusting the num_alphas variable in experiment2.py.                 

__Note__: The alpha and beta above refer to the commandline arguements alpha and beta passed to the script and not to the weights of the temporal continuity and sparseness loss functions themselves. However, the alpha and beta might refer to the weights as well, for instance in the plots produced by the script. However, the distinction is fairly easy to make depending on the context and the user is encouraged to do the same.

*Optional parameters*:
--numiter: number of iterations of each algorithm to run (defautls to 1000)    
--frame_size: frame size in s (defaults to 40e-3)    
--overlap: fraction of overlap between successive frames (defautls to 0.5)        


__Output__
Produces the following outputs at destination_folder:  
- time domain plots of original mixture and separated component signals
- plot of the variation of SNR with variation in the weight of the temporal continuity loss function alpha (see note above)     
- plot of the variation of SNR with variation in the weight of the sparseness loss function beta (see note above)     
- a readme.txt file containing the details of the trial (essentially the commandline arguements)

### setup.py

A module that handles commandline parsing, audio loading and creation of the readme.txt. Imported as    
```
import setup
```     

### run_expt2.sh   

A script that executes multiple trials with different settings of parameters to determine under what conditions the given algorithm produces the best results for the given audio file and for the same variation of the weights alpha and beta. Commands for a few of the trials run are present in the script. To run the script, navigate to where the file is saved (using the terminal) and give it execute permission    
```
chmod +x run_expt2.sh
```
 Then execute the script using the following command in the terminal

```
./run_expt2.sh
```

