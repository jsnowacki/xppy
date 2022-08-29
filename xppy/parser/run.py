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
import shutil
from xppy.parser import parse
from xppy.utils.output import Output

tmp_name = '__tmp__'
tmp_ode  = tmp_name+'.ode'
tmp_set  = tmp_name+'.set'
c_g = 'xppaut'

def set_cmd(xpp_path):
    global c_g
    c_g = os.path.join(xpp_path, c_g)
    print("XPP Path set: %s" % (c_g,))
    return c_g

def run(ode_file=tmp_ode, set_file=tmp_set, verbose=False):
    ''' 
    Function runs xppaut with the given ode_file and, optionally, set_file and
    returns the output of the simulation.
    If verbose=True (default False) xppaut output messages are displayed. 
    '''
    if not os.path.exists(ode_file):
        raise IOError('No such file or directory: '+ode_file)

    c = str(c_g) + ' '+ode_file+' -silent'
    if os.path.exists(set_file):
        c = c+' -setfile '+set_file
    # By default XPP stdio is not displayed
    if not verbose:
        if os.name in ['posix','mac']:
            c = c+' > /dev/null'
        elif os.name == 'nt':
            c = c+' > NUL'
    os.system(c)
    return Output(ode_file)

def runLast(last_out=None, ode_file=tmp_ode, set_file=tmp_set, verbose=False):
    ''' 
    Function runs xppaut with the given ode_file and, optionally, set_file using 
    the last_out as the initial conditions (if not provided runs a clean simulation)
    and returns the output of the simulation.
    If verbose=True (default False) xppaut output messages are displayed. 
    '''
    if last_out == None:
        last_out = run(ode_file, set_file, verbose)
    
    # Set the last point of the previous simulation as the initial conditions
    pars = parse.readOdePars(ode_file, False, True, False)
    for p in pars:
        p[2] = last_out[-1,p[1]]
    
    if os.path.exists(set_file):
        parse.changeSet(pars, set_file)
    else:
        parse.changeOde(pars, ode_file)
    
    return run(ode_file, set_file, verbose)

def createTmp(ode_file=None, set_file=None):
    '''
    Function creates temporary copies of ode and set files.
    '''
    if ode_file != None:
        shutil.copy(ode_file, tmp_ode)
    if set_file != None:
        shutil.copy(set_file, tmp_set)
    if ode_file == None and set_file == None:
        print('Warning! No files where created, both ode and set arguments are None.')

def deleteTmp(del_ode=True, del_set=True):
    '''
    Function deletes temporary copies of ode and set files.
    '''
    if del_ode and os.path.exists(tmp_ode):
        os.remove(tmp_ode)
    if del_set and os.path.exists(tmp_set):
        os.remove(tmp_set)

def cleanUp():
    '''
    Function performs a clean up (deletes temporary and output files).
    '''
    deleteTmp()
    if os.path.exists('output.dat'):
        os.remove('output.dat')
