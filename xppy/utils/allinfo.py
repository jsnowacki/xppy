'''
This file is part of XPPy.

Copyright (c) 2009-2011, Jakub Nowacki
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the XPPy Developers nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
####
# Reading XPPAut AllInfo file
####
import os
import numpy as np #@UnresolvedImport

class AllInfo:
    '''
    Class stores and manages data from XPPAut allinfo data file.
    '''
    def __init__(self, file_name=None):
        '''
        Constructor
        '''
        self.__raw_data = None
        self.__branches = []
        self.noVar = 0
        # If file name is given try to load the file  
        if file_name != None and os.path.exists(file_name):
            self.__raw_data = np.loadtxt(file_name)
            # Calculate the number of variables
            self.noVar = int((self.__raw_data.shape[1]-5)/4)
    
    def loadRawData(self, file_name):
        '''
        Raw data loader
        '''
        if os.path.exists(file_name):
            self.__raw_data = np.loadtxt(file_name)
            # Calculate the number of variables
            self.noVar = int((self.__raw_data.shape[1]-5)/4)
            return True
        else:
            return False
   
    def setRawData(self, raw_data):
        '''
        Raw data setter
        '''
        if isinstance(raw_data,np.ndarray):
            set.__raw_data = raw_data
            # Calculate the number of variables
            self.noVar = int((self.__raw_data.shape[1]-5)/4)
            return True
        else:
            return False

    def getRawData(self):
        '''
        Raw data getter
        '''
        return self.__raw_data

    def findBranches(self):
        '''
        Finds all branches in the raw data
        '''
        if self.__raw_data == None:
            return False
        
        # Scan file for branches
        bl = []
        for b in self.__raw_data[:,1]:
            try:
                i = bl.index(b)
            except ValueError:
                i = -1 # no match
            if i == -1:
                bl.append(b)
        self.__branches = sorted(bl)
        return True

    def findParts(self, branchArr):
        '''
        Finds parts in the given branch array 
        (branch extracted by e.g. getBranch) 
        '''
        parts = []; last = 0
        for i in range(0,branchArr.shape[0]):
            if branchArr[i,0] != last:
                parts.append(i)
                last = branchArr[i,0]
        return parts

    def getBranches(self):
        '''
        Branches getter
        '''
        if len(self.__branches) == 0:
            self.findBranches()

        return self.__branches

    def getBranch(self, nr, getParts=False):
        '''
        Function returns data of branch number nr
        additionally it cen return list with indexes of parts
        of the branch (stability wise)
        '''
        if len(self.__branches) == 0:
            self.findBranches()
        
        try:
            self.__branches.index(nr)
        except ValueError:
            return None # no match

        i = np.nonzero(self.__raw_data[:,1] == nr)
        retArr = self.__raw_data[i[0],:]
        # If we want additional parts array
        if getParts:
            parts = self.findParts(retArr)
            return (retArr, parts)
        # Else, just return the branch array
        return retArr          
 
    def getFlippedBranch(self, nr, getParts=False):
        '''
        Function returns flipped data of branch number nr;
        additionally it cen return list with indexes of parts
        of the branch (stability wise)
        '''
        (b,p) = self.getBranch(nr,True)
        if b == None:
            return None
            
        # Find starting point
        i = np.ix_(b[:,2]==b[0,2],b[:,3]==b[0,3])[0].ravel()
        # If the branch can't be flipped, return
        try:
            i = i[1]
        except IndexError:
            if getParts:
                return (b,p)
            else:
                return b
        # Change the stability of the first point to the proper one
        b[0,0] = b[1,0]
        # Stack two arrays togather in better order
        retArr = np.vstack((np.flipud(b[0:i,:]),b[i+1:,:]))
        # If we want additional parts array
        if getParts:
            parts = self.findParts(retArr)
            return (retArr, parts)
        # Else, just return the branch array
        return retArr          
