# Directory: experiment3    

The original paper employs the Hann window before obtaining the STFT and continuing with processing. This experiment determines the validity of the use of this window by testing the performance against different windows such as Hamming, Chebyshev and Blackman-Harris. Each trial of the experiment (i.e run of the file experiment3.py) produces a plot of the variation of the SNR of the proposed algorithm with different number for components for three different windows- Hann, Hamming and Blackman-Harris for a given frame size (which equals window size). The value of alpha is chosen to be 10 and the value of beta is chosen to be 0.1. This choice is a consequence of the results of experiment 2. This experiment is run for different values of frame size varying from 30 to 99 ms in steps of 3ms (see run_expt3_combined.sh). This is to determine how frame size affects the relative performance of the algorithm for the three different windows. This is then extended to determine the effect of main lobe width versus that of side lobe attenuation by experimenting with the Chebyshev window whichc optimzes for the smallest main lobe width given a window size and side lobe attenuation. The attenuation value is set to that of the Hamming window (42 dB) and the frame sizes are varied as described above. Further, 0th and last points of the Chebyshev window are set equal to the 1st and the last but one point to avoid the peaks produced in the window for the specified values. This does compromise the equiripple nature of the window but it is assumed from visual observation that this effect is not too significant (change my mind! :-P ). The SNR produced after the use of the Chebyshev window is compared to that of the other windows to determine the effect of reducing the main lobe width. This experiment is performed only at a frame size of 40ms as this is found to be the window size at which highest SNR is obtained for all windows. Further, unlike in the other experiments where only one audio is used, four audios are made use of in this experiment and the SNR values are averaged over all constituent sources.

## Contents  

### experiment3.py

Runs one trial of the experiment described above.  

__Usage__  
Run as   
```
python experiment3.py audio_folder audio_name destination_folder r alpha beta --numiter *numiter_val* --frame_size *framesize_time* --overlap *overlap_fraction*
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
- plot of the variation of SNR with variation in the number of compoents for Hann, Hamming and Blackman-Harris windows     
- *readme.txt*: a file containing the details of the trial (essentially the commandline arguements)     
- *Experiment3_<alpha>_<beta>_<frame_size>.pickle*: a pickle file containing a dictionary with the SNR values obtained, the windows corresponding to them and the range of the number of components. These details are used for later averaging.

### setup.py

A module that handles commandline parsing, audio loading and creation of the readme.txt. Imported as    
```
import setup
```     

### run_expt3_combined.sh   

A script that executes multiple trials with different settings of parameters to determine under what conditions the given algorithm produces the best results for the given audio file and for the same variation of the number of components. Commands for all of the trials run are present in the script. To run the script, navigate to where the file is saved (using the terminal) and give it execute permission    
```
chmod +x run_expt3_combined.sh
```
 Then execute the script using the following command in the terminal

```
./run_expt3.sh
```     

### chebwin_constant_att.py

Experiment to minimize main lobe width while sticking to the attenuation of the Hamming window. Usage instructions same as those for experiment3.py.

### combined_graph.py     
     
A tool to combine the results of multiple runs of various experiments by averaging the SNRs over multiple sources.      

__Usage__     
Run as      
```
python combined_graph.py --path_expt_folder *experiment_directoy* --path_store *result_directory*
```      

--path_expt_folder: directory where results of different trials are stored. Each trial needs to be saved in a subfolder with name blah_blah_<frame_size>*ms* where blah_blah can be any details related to the run. The frame size is extracted from the folder name and used for processing.   
--path_store: directory where the output of the script is stored.

__Output__    
Obtains averages of SNR for a given frame size for a given window over all values of number of components and all sources and plots the variaton.


### store_averages.py    

Does the same processing as ```combined_graph.py```- obtains the average SNR values and pickles them for later use in the specified folder instead of plotting them out. The purpose of the script is to extend the averaging functionality to multiple audio files all of which have been fed as input to the experimental setup described above by splitting up the averaging and plotting functionalities.

### final_average.py
Run as    
```
python final_average.py
```

Locations of the outputs of ```store_avearages.py``` script and a ```num_components.txt``` are hard coded into the script. ```num_components.txt``` contains details of the number of separated sources present for each separated audio and these details are used to obtain averages of the SNR for different windows over different mixtures.

__Output__    
Produces a plot of the average SNR values over all numbers of components and all sources associated with all processed mixtures in the same folder where the data of average SNRs is stored. Obtained results will be uploaded here soon. 

### run_generator.py    
File to generate ```run_expt3_combined.sh```.    

__Usage__   
 Run as     
```
python run_generator.py
```

__Output__   
run_expt3_combined.sh     

### run_chebwin.sh

A bash script to run multiple trials of the experiment with a chebyshev window. Navigate to where the script is stored and run the following commands in the terminal to give the script execute permission and then run it   
```
chmod +x run_chebwin.sh    
./run_chebwin.sh
```
