'''
Created on Feb 11, 2010

@author: enxjn
'''
import os
import shutil
from xppy.parser import parse
from xppy.utils.output import Output

tmp_name = '__tmp__'
tmp_ode  = tmp_name+'.ode'
tmp_set  = tmp_name+'.set'

def run(ode_file=tmp_ode, set_file=tmp_set, verbose=False):
    ''' 
    Function runs xppaut with the given ode_file and, optionally, set_file and
    returns the output of the simulation.
    If verbose=True (default False) xppaut output messages are displayed. 
    '''
    if not os.path.exists(ode_file):
        raise IOError('No such file or directory: '+ode_file)

    c = 'xppaut '+ode_file+' -silent'
    if os.path.exists(set_file):
        c = c+' -setfile '+set_file
    # Moves the xppaut output messages to trash (posix systems only)
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
        print 'Warning! No files where created, both ode and set arguments are None.'

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