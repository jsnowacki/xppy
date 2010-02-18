from distutils.core import setup
from xppy import __version__ 

setup(name='xppy',
      version=__version__,
      description='Tool to parse and run XPPAut files from Python, with \
      additional utilities.',
      author='Jakub Nowacki',
      author_email='j.s.nowacki@googlemail.com',
      license='LGPL',
      url='http://seis.bris.ac.uk/~enxjn/',
      platforms='All-platforms',
      packages=['xppy','xppy.parser','xppy.utils'],
      )
