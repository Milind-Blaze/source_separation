import numpy as np
import librosa
import librosa.display
from librosa.core import resample


# Frobenius norm with square root
def lstcost(A,B):
    return np.sqrt(np.sum((A-B)**2))
  
# second type of divergence  
def divcost(A,B):
    return np.sum(A*np.log(A/B))-np.sum(A)+np.sum(B)

  
def lstfind(V,r,numiter,toprint):
    np.random.seed(3)
    n= V.shape[0]
    m= V.shape[1]
    # initial scaling copied from scikit 
    # implementation
    q= (V.mean())/r
    W= q*np.random.random((n,r))
    H= q*np.random.random((r,m))
    cost=[lstcost(V,np.dot(W,H))]
    for i in range(1,numiter+1):
        W = W*(np.dot(V,H.T))/(np.dot(W,np.dot(H,H.T)))
    # TODO: remove the hnew?
        hnew= H*(np.dot(W.T,V))/(np.dot(W.T,np.dot(W,H)))
    # W is updated before H is and the new value is used    
        H= hnew.copy()
        
        if i%toprint==0:
            cost.append(lstcost(V,np.dot(W,H)))
            print("cost after " +str(i) + " iterations: " + str(cost[-1]) )
    return (W,H,cost)
  
def divfind(V,r,numiter,toprint):
    np.random.seed(3)
    n= V.shape[0]
    m= V.shape[1]
    q= (V.mean())/r
    q=1
    W= q*np.random.random((n,r))
    H= q*np.random.random((r,m))
    cost=[divcost(V,np.dot(W,H))]
    for i in range(1,numiter+1):
        W = W*(np.dot(V/np.dot(W,H),H.T))/(np.sum(H,axis=1,keepdims=True)).T
        H = H*(np.dot(W.T,V/np.dot(W,H)))/(np.sum(W,axis=0,keepdims=True)).T
        #wnew= W*(np.dot(V,H.T))/(np.dot(W,np.dot(H,H.T)))
        #H= hnew.copy()
        #W= wnew.copy()
        if i%toprint==0:
            cost.append(divcost(V,np.dot(W,H)))
            print("cost after " +str(i) + " iterations: " + str(cost[-1]) )
    return (W,H,cost)

def SNR(A, B):
    # A is the original magnitude spectrogram 
    # B is the reconstructed magnitude spectrogram
    # unlikely that they will ever be vectors 
    if A.ndim == 1:
        A = A[:, np.newaxis]
    if B.ndim == 1:
        B = B[:, np.newaxis]
    numer = np.sum(A**2)
    denom = np.sum((A - B)**2)
    return numer/denom
 
def load_audio(fs_target, path_audio):
    audio, fs = librosa.load(path_audio,sr = fs_target)
    t = np.arange(len(audio))/fs_target
    return audio, fs, t

def virtanen007_loss(X, B, G, alpha, beta):
    """
    Returns the loss function corresponding to KL divergence + alpha*sparseness + beta*temporal_continuity
    """
    epsilon1 = np.min(X[np.nonzero(X)])/1000
    recon = np.dot(B,G)
    epsilon2 = np.min(recon[np.nonzero(recon)])/1000
    cr = divcost(X + epsilon1, recon + epsilon2)
    gtj = G[:,1:]
    gt_prevj = G[:,:-1]
    sigmaj = np.sqrt(np.mean(G**2, axis = 1))
    ct = np.sum(np.sum((gtj - gt_prevj)**2, axis = 1)/(sigmaj**2))
    cs = np.sum(np.sum(np.abs(G), axis = 1)/sigmaj)
    cost = cr + ct + cs
    return cost

