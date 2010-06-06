'''
This file is part of XPPy.

XPPy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

XPPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with XPPy.  If not, see <http://www.gnu.org/licenses/>.
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
