# experiment 3 catalogs the variation of virtanen007 algorithm with snr with number of components over the windows hann, hamming and blackman harris
# r is the maximum number of components


# python experiment3.py ../audios/orig4/ orig4 ../experiments/experiment3/temp/ 8 10 0.1 --numiter 10
python experiment3.py ../audios/orig4/ orig4 ../experiments/experiment3/alpha_10_beta_0.1_numcomp_40_40ms/ 40 10 0.1 --numiter 1000	
python experiment3.py ../audios/orig4/ orig4 ../experiments/experiment3/alpha_10_beta_0.1_numcomp_40_60ms/ 40 10 0.1 --numiter 1000 --frame_size 60e-3
python experiment3.py ../audios/orig4/ orig4 ../experiments/experiment3/alpha_10_beta_0.1_numcomp_40_80ms/ 40 10 0.1 --numiter 1000	--frame_size 80e-3