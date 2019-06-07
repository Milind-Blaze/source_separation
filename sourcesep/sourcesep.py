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

  
def lstfind(V,r,numiter,toprint = None):
    np.random.seed(3)
    eps = np.finfo(np.float32).eps/10
    V = V + eps
    n= V.shape[0]
    m= V.shape[1]
    # initial scaling copied from scikit 
    # implementation
    q= (V.mean())/r
    W= q*np.random.random((n,r)) 
    H= q*np.random.random((r,m))
    cost=[lstcost(V,np.dot(W,H))]

    if toprint == None:
        toprint = numiter + 1

    for i in range(1,numiter+1):
        W = W*(np.dot(V,H.T))/(np.dot(W,np.dot(H,H.T)))
    # TODO: remove the hnew?
        hnew= H*(np.dot(W.T,V))/(np.dot(W.T,np.dot(W,H)))
    # W is updated before H is and the new value is used    
        H= hnew.copy()
        cost.append(lstcost(V,np.dot(W,H)))
        if i%toprint==0:
            print("cost after " +str(i) + " iterations: " + str(cost[-1]) )
    return (W,H,cost)
  
def divfind(V,r,numiter,toprint = None):
    np.random.seed(3)
    n= V.shape[0]
    m= V.shape[1]
    q= (V.mean())/r
    q=1
    eps = np.finfo(np.float32).eps/10
    V = V + eps
    W= q*np.random.random((n,r))
    H= q*np.random.random((r,m))
    cost=[divcost(V,np.dot(W,H))]

    if toprint == None:
        toprint = numiter + 1

    for i in range(1,numiter+1):
        W = W*(np.dot(V/np.dot(W,H),H.T))/(np.sum(H,axis=1,keepdims=True)).T
        H = H*(np.dot(W.T,V/np.dot(W,H)))/(np.sum(W,axis=0,keepdims=True)).T
        #wnew= W*(np.dot(V,H.T))/(np.dot(W,np.dot(H,H.T)))
        #H= hnew.copy()
        #W= wnew.copy()
        cost.append(divcost(V,np.dot(W,H)))
        if i%toprint==0:
            print("cost after " +str(i) + " iterations: " + str(cost[-1]) )
    return (W,H,cost)

def SNR(A, B):
    """
     A is the original magnitude spectrogram 
     B is the reconstructed magnitude spectrogram
    # unlikely that they will ever be vectors 
    """
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
    if sigmaj.ndim == 1:
        sigmaj = sigmaj[:, np.newaxis]
    ct = np.sum(np.sum((gtj - gt_prevj)**2, axis = 1)/(sigmaj**2))
    cs = np.sum(np.sum(np.abs(G), axis = 1)/sigmaj)
    cost = cr + alpha*ct + beta*cs
    return cost


def virtanen007_find(X, r, alpha, beta, numiter, toprint= None):
    """
    Obtains the factorization for the matrix X by minimising the KL divergence alongwith the use of sparseness and temporal continuity criteria.
    
    Parameters:
    
    X (2d numpy array): the magnitude spectrogram of the audio. Of shape m x n.
    r (int): the number of components to be obtained. 
    alpha (float): coefficient of the temporal continuity term
    beta (float): coefficient of the sparseness term
    numiter (int): number of iterations of the algorithm to be run
    toprint (int): number of iterations after which the cost is to be printed. Defaults to None. If None, cost is never printed.
                    
    Returns:
    B (2d numpy array): Matrix of shape m x r whose column vectors form the components for the separated sources.
    G (2d numpy array): Matrix of shape r x n whose ith row forms the time encoding for the ith component of B.
    cost (list): a list of lenght numiter with the cost function calculated at every iteration
    """
    np.random.seed(3)
    eps = np.finfo(np.float32).eps/10
    # print("small value being added to prevent nan: ",eps)
    # print("minimum value of input magnitude spectrogram: ", np.min(X[np.nonzero(X)]))
    m = np.shape(X)[0]
    n = np.shape(X)[1]
    # initializing as gaussian noise 
    B = np.abs(np.random.randn(m,r))
    G = np.abs(np.random.randn(r,n))

    X = X + eps
    cost=[virtanen007_loss(X, B, G, alpha, beta)]
    one = np.ones((m,n))
    if toprint == None:
        toprint = numiter + 1
        
    for i in range(1,numiter+1):
        B = B*(np.dot(X/np.dot(B,G),G.T))/(np.dot(one, G.T))
        
        
        sigmaj = np.sqrt(np.mean(G**2, axis = 1, keepdims = True))
        
        
        crplus = np.dot(B.T, one)
        
        crminus =  np.dot(B.T, X/np.dot(B,G))
        
        ctplus = 4*G/(sigmaj**2)
        
        T = np.shape(G)[1]
        

        g0 = G[:,0]
        g0 = g0[:, np.newaxis]
        gn = G[:,-1]
        gn = gn[:, np.newaxis]
        gtminus = np.append(g0, G[:,:-1], axis = 1)
        gtplus = np.append(G[:,1:], gn, axis = 1)
        term1 = (2)*((gtminus + gtplus)/(sigmaj**2))
        diff_square = np.sum((G[:,1:] - G[:,:-1])**2, axis =1, keepdims = True)
        term2 = G*(2/(T*sigmaj**4))*diff_square
        ctminus = term1 + term2
        
        
        csplus = np.repeat(1/sigmaj, np.shape(G)[1], axis = 1)
        
        colsum = np.sum(G, axis = 1, keepdims= True)
        csminus = G*colsum/((sigmaj**3)*T)
        
        derplus = crplus + alpha*ctplus + beta*csplus
        derminus = crminus + alpha*ctminus + beta*csminus
            
        G = G*(derminus/derplus)
        
        cost.append(virtanen007_loss(X, B, G , alpha, beta))
        
        if i%toprint==0:
            print("cost after " +str(i) + " iterations: " + str(cost[-1]) )
            
    return (B,G,cost)


def reconmag_r_components(B,G):
    """
    Parameters:
    B : matrix (m x r) whose column vectors act as the basis vectors for the separated sources
    G : matrix (r x n) whose ij_th element corresponds to the gain of the ith component in the jth time frame
    
    
    Return:
    components : list of the magnitude spectrograms of the separated components   
    
    """
    m = np.shape(B)[0]
    n = np.shape(G)[1]
    r = np.shape(B)[1]
    if np.shape(G)[0] != r:
        print("B and G can not be multiplied")
        return
    components = []
    for i in np.arange(0,r):
        componenti = np.outer(B[:,i], G[i,:])
        components.append(componenti)
    
    return components


def virtanen007_cluster_all(sources, components):
    """
    assign each component reconstructed to a source component by finding that source from sources which has 
    the highest SNR with the given component
    
    Parameters: 
        sources : list of magnitude spectra of each source used to create the mixture
        components : list of the magnitude spectra of the components obtained from separation
    
    Returns:
        allocation : list whose kth element is list with zeroth element as source_k and remaining elements as the 
                    components allcoated to it
    
    """
    
    num_sources = len(sources)
    num_components = len(components)
    
    allocation = [[source] for source in sources]
        
    for i in range(num_components):
        component = components[i]
        snrs = [0]*num_sources
        
        for j in range(num_sources):
            source = sources[j]
            snrs[j] = SNR(source, component)
        assgn = np.argmax(snrs)
        allocation[assgn].append(component)
        
    return allocation



def distortion_measure(orig, recon):
    eps = np.finfo(np.float32).eps/10
    orig = orig + eps
    recon = recon + eps
    mid = (orig/recon)**2 
    midlog = np.log(1/mid)
    return np.sum((mid - 1 + midlog))


def virtanen007_cluster_max(sources, components):
    """
    assigns one component which produced max SNR to 
    """
    return
