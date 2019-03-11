
Scripts:

Setup.py

- Loads the original audio
- Loads the separated components
- Creates the magnitude and phase spectrograms for all the audios involved
- Creates the images of waveforms in the experiment directory


experiment1.py

- varies r, the number of components
- uses NMF EUL, NMF LOG, virtanen007 reconstruction to find the number of components
- computes average SNR for each r for each algo
- computes DR for each r for each algo
- provides plots of DR and SNR over different algos 