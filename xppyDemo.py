# coding: utf-8
import xppy
xppy.set_cmd('/PATH_TO_XPPAUT/')
subHopf=xppy.run('SOME_ODE_FILE.ode')
subHopf.getDesc()
sHData=subHopf.getRawData()
sHData.shape
from xppy.utils import plot
plot.plotLC(subHopf.getRawData())
plot.pl.show()
