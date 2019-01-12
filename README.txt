[UNMAINTAINED] The library is no logner maintained by me as I don't work in the area anymore. Please see the forks for newer, maintened versions.

XPPy is a Python interface for Bard Ermentrout's XPP. XPPy was inspired by a 
similar XPP-Matlab interface by Rob Clewley. 

The main feature is ability to parse and change XPP's ode and set files, and 
run a simulation using XPP. The package contains some data wrapping classes 
that aid working with data files produced by XPP (timetraces, allinfo and 
bifurcation files files). In addition, it contains additional plotting tools 
for matplotlib. 

#################
# LICENCE       #
#################
XPPy is free software: you can redistribute it and/or modify it under the terms 
of the GNU Lesser General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any 
later version. 

XPPy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE. See the GNU Lesser General Public License for more details. 

You should have received a copy of the GNU Lesser General Public License along 
with XPPy in COPYING.txt file. If not, see http://www.gnu.org/licenses/.

#################
# DOCUMENTATION #
#################
Since XPPy is a collection of tools I created on a course of my work, it was 
primary used by one person, therefore it is not extremely well documented.
Nevertheless, there is a Doxygen-generated documentation for the package in
the folder doc. You can choose between HTML and LaTeX documentation.
To obtain PDF from LaTeX documentation you need to have PDFLaTeX installed.
To make PDF file just go to the LaTeX documentation folder and type 'make', e.g.:

$ cd doc/latex
$ make

Moreover, every object contains docstring, which more or less explains 
its purpose.

#################
# INSTALLATION  #
#################
Before you install XPPy you should install NumPy, which is extensively used 
by XPPy. Also if you want to use plotting tools (xppy.utils.plot) you should 
have matplotlib. Note that XPPy installation script does not check for those 
packages and will install anyway, the error messages will appear when you will 
try to import XPPy.

XPPy has a Python distutils setup script. To install XPPy just unpack the 
source package and change the directory, e.g.

$ unzip xppy-x.y.z.zip 
$ cd xppy-x.y.z

(where x.y.z is a current version number, e.g. 1.2.3), and type the below 
command to install the package

$ python setup.py install

This command will install XPPy in as standard site-packages folder of the 
Python version used. If you have more then one Python on your machine, it is 
advisable to check which version is currently used or call a certain version of 
Python by writing, e.g. python2.6 instead of just python. 

If you have some problems or want to know more about the installation proces, 
please check distutils documentation first. 

Before you start using XPPy make sure that path to XPP is present in your PATH 
variable. Easy way to check that is to type xppaut in the terminal window 
anywhere outside the XPP directory, that should open XPP window. If you have 
some problems with XPP itself, please refer to XPP documentation.

#####################
# HOW TO CITE XPPY? #
#####################
If you want to refer to XPPy in a publication, you can use 

"Nowacki J. XPPy. 2011. Available at: http://seis.bris.ac.uk/~enxjn/xppy/."

or BibTeX:

@misc{xppy, 
      author = {Nowacki, Jakub}, 
      title = {{XPPy}}, 
      url = {http://seis.bris.ac.uk/~enxjn/xppy/}, 
      year = {2011} 
}
