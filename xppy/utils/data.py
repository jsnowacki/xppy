'''
Created on Feb 11, 2010

@author: enxjn
'''
import numpy as np #@UnresolvedImport

#####
# Data processing/analysing functions
#####
def getOrbit(data, start=None, eps=1e-4, col=1):
    '''
    Function extracts single orbit from given data and returns it.
    The orbit is ectracted from 'start' with accuracy of the end 
    point less than eps. The compared data is taken from 
    the column col.
    '''
    # If no starting point is specified, start from the minimal value
    if start == None:
        start = data[:,col].argmin()

    stop = start+1
    avr = data[:,col].min() + \
          (np.abs(data[:,col].max()) + np.abs(data[:,col].min()))/2
    crossAvr = False 
    for i in range(start+1,data.shape[0]):
        # Orbit have to cross maximu avarege value firs
        if not crossAvr:
            if data[i,col] >= avr:
                crossAvr = True
            else:
                continue
        # After crossing the avarge value, we're looking for the end
        if np.abs(data[start,col]-data[i,col]) <= eps:
            stop = i+1
            break
    return data[start:stop,:]

def arcLength(data):
    '''
    Calculate the arclenght of the provided data.
    '''
    alen = 0
    for i in range(0,data.shape[0]-1):
        alen += np.linalg.norm(data[i+1,:]-data[i,:])
    return alen

def resample1d(data, ns):
    '''
    Function resamples the given data (1d line [x,y] data) using even 
    arc lenght (linear interpolation). New (resampled) data is returned.  
    '''
    # Calculating arc lenght of the bit and the whole data
    tot_alen = arcLength(data)
    bit_alen = tot_alen/(ns-1)
    # Chopping the line unto even ns segments
    new_data = np.ones((ns,2))*np.NaN
    new_data[0,:] = data[0,:]
    cur_alen = arcLength(data[[0,1],:])
    old_alen = 0
    j = 0
    for i in range(1,ns-1):
        while j <= data.shape[0]-2:
            if cur_alen > (i)*bit_alen:
                # Slope of a line
                a = ((i)*bit_alen-old_alen)/(cur_alen-old_alen)
                new_data[i,:] = data[j,:] + a*(data[j+1,:]-data[j,:])
                break
            else:
                j += 1
                old_alen = cur_alen
                cur_alen += np.linalg.norm(data[j,:]-data[j+1,:])
    new_data[-1,:] = data[-1,:] # First and last points sould be the same
    return new_data

def findSpikes(data, cols=[0,1], threshold=1.7, sampleThr=3):
    '''
    Function finds spiks in the given two data columns data. 
    Threshold is a slope of the tangent line. SampleThr is 
    minimal number of samples where slope is greater then threshold.
    '''
    if len(cols) != 2:
        raise ValueError('List should contain to columns!')
    
    st = 0 # Number of samples above threshold
    # List contain begining, top and end of the spike i
    spb = []; spm = []; spe = []
    # Last slope
    sl_last = 0
    # Spike flag (0 - nothing, 1 - passed begining, 
    # 2 - passed midpoint, 3 - on the way down (on steep slope))
    spf = 0
    for i in range(1,data.shape[0]):
        # Difference of the given components
        dx,dy = data[i,cols] - data[i-1,cols]
        # Slope of tangent line
        sl = dy/dx

        # Looking for midpoint
        if spf == 1:
            # If slopes have different sign we have midpoint/top
            if np.sign(sl_last) != np.sign(sl):
                spm.append(i-1)
                spf = 2
            sl_last = sl
            continue
        
        # Looking for the steep slope down
        if spf == 2:
            if np.abs(sl) > threshold and np.sign(sl) == -1:
                spf = 3
            continue

        # Looking for the bottom of the spike
        if spf == 3:
            if (not np.abs(sl) > threshold) or np.sign(sl_last) != np.sign(sl):
                spe.append(i-1)
                spf = 0
                st = 0
            sl_last = sl
            continue

        # A candidate for a spike
        if np.abs(sl) > threshold:
            st += 1
            # If we passed sample threshold, we have begining of a spike
            if st >= sampleThr and sl > 0:
                spb.append(i-1)
                spf = 1
        else:
            st = 0
        sl_last = sl

    return (spb,spm,spe)

def findADP(data, cols=[0,1], threshold=1.7, sampleThr=3):
    '''
    Function finds ADP in data in given columns. Threshold and sample threshold,
    are parameters for findSpikes.
    '''
    (spb, spm, spe) = findSpikes(data, cols, threshold, sampleThr)
    adp = []
    # For each spike end
    for i in range(len(spe)):
        # Calculating slope for the end of the spike
        # Difference of the given components
        dx,dy = data[spe[i],cols] - data[spe[i]-1,cols]
        # Slope of tangent line
        sl_last = dy/dx
        # If we have more spikes, look for ADP till the begining 
        # of the next spike, else look till the end of the data
        if i+1 < len(spe):
            j_end = spb[i+1]
        else:
            j_end = data.shape[0]
        for j in range(spe[i]+1,j_end):
            # Difference of the given components
            dx,dy = data[j,cols] - data[j-1,cols]
            # Slope of tangent line
            sl = dy/dx
            # We've found the potential ADP's end
            if np.abs(sl) > np.abs(sl_last) and sl < 0:
                if j-spe[i] > 2:
                    adp.append(j)
                break
            sl_last = sl
    return adp

def ISI(data, cols=[0,1], threshold=1.7, sampleThr=3):
    '''
    Function calculates ISI from given data and return in the form of an array
    of ISI for the given pair. The ISI is calculated for the peak of the spikes.
    '''
    
    (spb, spm, spe) = findSpikes(data, cols, threshold, sampleThr)
    
    # ISI can be calculated for at least 2 spikes
    if len(spm) < 2:
        return None
    
    return np.diff(data[spm,cols[0]])

def getDVDT(data, cols=[0,1]):
    '''
    Function calculated dV/dt over given data.
    '''

    return np.diff(data[:,cols[1]])/np.diff(data[:,cols[0]])

def getThreshold(data, cols=[0,1]):
    ''' 
    Function returns a threshold time and value for the first spike in the spike train.
    Threshold is defined as dV/dt crossing of 10 mV/ms.
    '''
    dv = getDVDT(data, cols)
    
    i = (dv >= 10).nonzero()[0][0]
    
    return data[i,:]

def getTau(data, cols=[0,1]):
    '''
    Function gets time constant from hyperpolarizing current injection data.
    Time constant is defined as a crossing of 63% of the maximal amplitude
    of the trajectory. Note that t0 is the beginning of the current injection,
    function does not detect the beginning of current injection by itself.
    '''
    d = np.abs(data[:,cols].copy())
    v_63  = 0.63*(d[:,cols[1]].max() - d[:,cols[1]].min()) + d[0,cols[1]]    

    # Index of the 63% crossing 
    i_63 = (d[:,cols[1]] >= v_63).nonzero()[0][0]
    return d[i_63,cols[1]] - d[0,cols[1]]