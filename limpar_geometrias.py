"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-10-17
        copyright            : (C) 2017 by Leandro Franca - Cartographic Engineer
        email                : geoleandro.franca@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation.                              *
 *                                                                         *
 ***************************************************************************/
"""
# Limpar geometrias
##LF02) Revisao=group
##07. Limpar Geometrias=name

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

# Varrer camadas
tam = 0
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    tam +=1
    
for i, layer in enumerate(QgsMapLayerRegistry.instance().mapLayers().values()):
    if layer.type()==0:
        if layer.geometryType() == QGis.Line or layer.geometryType() == QGis.Polygon:
            ok = processing.runalg('script:6consertageometriasnobd', layer, 0.01, 0.01, 0, 20)
    progress.setPercentage(int((i+1/float(tam))*100))

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(8)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)