# Directory: experiment1   

The objective of this experiment is to determine if and under what conditions (settings of hyperparameters) the proposed algorithm employing sparseness and temporal continuity criteria outperforms vahilla NMF. In each run (of the file experiment1.py), one audio file is processed and three algorithms are used to perform source separation- NMF with Frobenius norm as the loss function, NMF with KL divergence as the loss function and NMF with sparseness and temporal continuity criteria tacked on. The number of components used is varied from the original number of separated sources (known beforehand) to a specified number of components and the SNR for each given "number of components" is recorded. The following descriptions offer details of how (:-P hyper)parameters of the experiment can be varied. The plots resulting from one run can be used to make a comparison of the performance (SNR) of the algorithms for the given audio. 

## Contents  

### experiment1.py

Runs one trial of the experiment described above.  

__Usage__  
Run as   
```
python experiment1.py audio_folder audio_name destination_folder r alpha beta --numiter *numiter_val* --frame_size *framesize_time* --overlap *overlap_fraction*
```   
audio_folder: path to folder containing the source (named as orig*n*.wav) and reference components (named as separated*n*\_*m*.wav). The script supports only .wav files.     
audio_name: name of the audio. If the source file is orig4.wav, then this parameter is orig4.     
destination_folder: path to folder where time domain plots of the audios (source and separated) and the resulting plots (.png) are stored.    
r: maximum number of components to be used for separation each of which is assigned to a source. Must be greater than the number of separated*n*\_*m*.wav files present in audio_folder    
alpha: weight of the temporal continuity loss function    
beta: weight of the sparseness loss function     

*Optional parameters*:
--numiter: number of iterations of each algorithm to run (defautls to 1000)    
--frame_size: frame size in s (defaults to 40e-3)    
--overlap: fraction of overlap between successive frames (defautls to 0.5)        


__Output__
Produces the following outputs at destination_folder:  
- time domain plots of original mixture and separated component signals
- plot of the variation of SNR with different number of components for the three different algorithms
- a readme.txt file containing the details of the trial (essentially the commandline arguements)

### setup.py

A module that handles commandline parsing, audio loading and creation of the readme.txt. Imported as    
```
import setup
```     

### run_expt1.sh   

A script that executes multiple trials with different settings of parameters to determine under what conditions the given algorithm produces the best results for the given audio file. Commands for a few of the trials run are present in the script. To run the script, navigate to where the file is saved (using the terminal) and give it execute permission    
```
chmod +x run_expt1.sh
```
 Then execute the script using the following command in the terminal

```
./run_expt1.sh
```

