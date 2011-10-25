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
from xppy.utils import allinfo
import matplotlib.pyplot as pl #@UnresolvedImport
from matplotlib.collections import LineCollection #@UnresolvedImport

class Surf:
    '''
    Class that stores the surface data
    '''
    def __init__(self, x=[], y=[], z=[], type=None):
        '''
        Constructor
        '''
        self.type = type
        if len(x) == len(y) == len(z) != 0:
            self.x = np.array([x])
            self.y = np.array([y])
            self.z = np.array([z])
        else:
            self.x = []
            self.y = []
            self.z = []
    
    def setData(self, x, y, z):
        '''
        Data setter
        '''
        if not len(x) == len(y) == len(z):
            return

        self.x = x
        self.y = y
        self.z = z
    
    def getData(self):
        '''
        Data getter
        '''
        return (self.x, self.y, self.z)

    def appendData(self, x, y, z):
        '''
        Append data to the matrix 
        '''
        if not len(x) == len(y) == len(z):
            return

        if len(self.x) == 0:
            self.x = np.array([x])
            self.y = np.array([y])
            self.z = np.array([z])
        else:
            self.x = np.append(self.x, np.array([x]), axis=0)
            self.y = np.append(self.y, np.array([y]), axis=0)
            self.z = np.append(self.z, np.array([z]), axis=0)

def plotDiag(file_name, axes = None, tr_file='', tr_cols=[],
             xlabel='', ylabel='', img_dir='', img_ext='png'):

    #print 'Plotting',file_name
    if not axes:
        f = pl.figure()
        ax = f.add_subplot(111)
    else:
        ax = axes
    # read the data file for second (right) fpo continuation
    ai = allinfo.AllInfo(file_name)
    bl = ai.getBranches()
    #print 'branches: ',bl
    # color setup
    c = ['','-k','-r','-b','-m']
    # plot all branches
    for n in bl:
        (b,p) = ai.getBranch(n, True)
        # plot all parts
        for i in range(0,len(p)):
            if i == len(p)-1:
                ax.plot(b[p[i]:,2],b[p[i]:,5],c[int(b[p[i],0])])
                # if the branch is periodic orbit, plot low value as well
                if int(b[p[i],0]) in [3,4]:
                    ax.plot(b[p[i]:,2],b[p[i]:,5+ai.noVar],
                            c[int(b[p[i],0])])
            else:
                ax.plot(b[p[i]:p[i+1],2],b[p[i]:p[i+1],5],c[int(b[p[i],0])])
                # if the branch is periodic orbit, plot low value as well
                #if b[p[i],1] < 0:
                if int(b[p[i],0]) in [3,4]:
                    ax.plot(b[p[i]:p[i+1],2],b[p[i]:p[i+1],5+ai.noVar],
                            c[int(b[p[i],0])])
    del ai
    # Adding trajectory to the picture
    if len(tr_file) > 0 and len(tr_cols) == 2:
        tr = np.loadtxt(tr_file)
        ax.plot(tr[:,tr_cols[0]], tr[:,tr_cols[1]], 'g-')
    # Some additional info
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    # if axes were passed don't save as we do not know the fig
    if not axes:
        ax.set_title(file_name)
        # Save figure
        fn = file_name.split('/')[-1]
        fn = fn.split('.')[0]+'.'+img_ext
        fn = img_dir+fn
        f.savefig(fn,dpi=200)

def plotLC(data, cols=[0,1], axes=None, colormap=None):
    '''
    Function plots data from selected two columns in form of Line Collection
    using selected colormap. If no axes is given, function create new axes.
    '''
    if len(cols) != 2:
        raise ValueError('List should contain to columns!')

    sec = zip(data[:-1,cols],data[1:,cols])
    cm = pl.cm.get_cmap(colormap)
    c = cm(np.linspace(0,1,data.shape[0]))
    lc = LineCollection(sec, color=c)
    if axes == None:
        axes = pl.subplot(111)
    axes.add_collection(lc)
    axes.axis([data[:,cols[0]].min(),
               data[:,cols[0]].max(),
               data[:,cols[1]].min(),
               data[:,cols[1]].max()])

