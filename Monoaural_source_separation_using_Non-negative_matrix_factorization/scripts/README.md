# Directory: scripts

This folder contains the setup for the three experiments performed to verify the superior performance of the proposed algorithm and to look for any potential improvements of the same. It is worth noting that all the experiments were performed only for the four audios provided by the author and experimentation with a greater number of audios will follow soon.   
    
## Contents     

__experiment1__: A study of the variation of the SNR of the separated sources with respect to the reference signals for three different algorithms: NMF with Frobenius norm as the loss function and KL divergence as the loss function, and the proposed algorithm.    
__experiment2__: A study of the variation of the SNR of the separated sources with respect to the reference signals for only the algorithm in the refrenced paper with the variation of the parameters alpha and beta. 
__experiment3__: A study of the variation of the SNR of the proposed algorithm with different windows and window sizes. This is to verify if the use of Hann window as done by the author is in fact the best thing to do for this problem. The windows tested are the Hann, Hamming, Blackman-Harris and Chebyshev windows.  