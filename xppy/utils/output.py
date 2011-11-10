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
import os
import numpy as np #@UnresolvedImport
from xppy.parser import parse

class Output:
    '''
    Class stores and manages data from XPPAut output data file.
    '''
    def __init__(self, ode_file='', file_name='output.dat'):
        '''
        Constructor
        '''
        self.__raw_data = None # Content of data file
        self.__desc     = None # Data descriptor, read from the ode_file
        
        if os.path.exists(file_name):
            self.__raw_data = np.loadtxt(file_name)
        
        if os.path.exists(ode_file):
            self.__desc = parse.readOdeVars(ode_file)
        
    
    def loadRawData(self, file_name='output.dat'):
        '''
        Raw data loader
        '''
        if os.path.exists(file_name):
            self.__raw_data = np.loadtxt(file_name)
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

    def readOdeVars(self, ode_file):
        '''
        Set class variable descriptor (to read columns as variable names)
        '''
        self.__desc = parse.readOdeVars(ode_file)
        return True
    
    def setDesc(self, desc):
        '''
        Variable descriptor setter
        '''
        self.__desc = desc
    
    def getDesc(self):
        '''
        Variable descriptor getter
        '''
        return self.__desc
     
    def __getitem__(self, name):
        # TODO Maybe do it more efficiently 
        # Sequence value
        if type(name) is tuple:
            if type(name[1]) is str:
                j = self.__desc[name[1]] 
            elif type(name[1]) is list:
                j = []
                for n in name[1]:
                    if type(n) is int:
                        j.append(n)
                    elif type(n) is str:
                        j.append(self.__desc[n])                      
            else:
                j = name[1]
            i = name[0]
            return self.__raw_data[i,j]
        # Single value         
        elif type(name) is str:
            j = self.__desc[name]
            return self.__raw_data[:,j]
        elif type(name) is int:
            return self.__raw_data[:,name]
        elif type(name) is list:
                j = []
                for n in name:
                    if type(n) is int:
                        j.append(n)
                    elif type(n) is str:
                        j.append(self.__desc[n])
                return self.__raw_data[:,j]
        
        else:
            raise IndexError('Index does not exist!')
        
    def __str__(self):
        ret = 'Columns:'
        for i in range(self.__raw_data.shape[1]):
            ret += ' %i:%s'%(i,self.__desc[i]) 
        ret += '\nData:\n'+str(self.__raw_data)
        
        return ret
