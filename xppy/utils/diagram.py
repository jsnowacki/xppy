'''
Created on Feb 11, 2010

@author: enxjn
'''
import numpy as np #@UnresolvedImport

def read_diagram(diag):
    '''
    Function reads provided XPPAut-style diagram and returns more
    plotting-friendly version
    '''
    diag_ret = np.zeros([diag.shape[0],9])*np.NaN
    for i in range(0,diag.shape[0]):
        if diag[i,3] == 1:
            diag_ret[i,[1,5]] = diag[i,[1,2]]
        elif diag[i,3] == 2:
            diag_ret[i,[2,6]] = diag[i,[1,2]]
        elif diag[i,3] == 3:
            diag_ret[i,[3,7]] = diag[i,[1,2]]
        elif diag[i,3] == 4:
            diag_ret[i,[4,8]] = diag[i,[1,2]]
    diag_ret[:,0] = diag[:,0]
    
    return diag_ret
