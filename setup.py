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
from distutils.core import setup
from xppy import __version__ 

setup(name='xppy',
      version=__version__,
      description='XPP interface for Python, with additional utilities.',
      author='Jakub Nowacki',
      author_email='j.s.nowacki@gmail.com',
      license='LGPL',
      url='http://seis.bris.ac.uk/~enxjn/xppy',
      platforms='All-platforms',
      packages=['xppy','xppy.parser','xppy.utils']
      )
