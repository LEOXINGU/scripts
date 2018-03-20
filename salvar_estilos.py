"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-03-20
        copyright            : (C) 2018 by Leandro Franca - Cartographic Engineer
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

# Salvar Estilos
##1. Salvar Estilos=name
##LF10) Cartografia=group
##Pasta_para_guardar_estilos=folder

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing

for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.type() in [0, 1]:
        nome = layer.name()
        layer.saveNamedStyle(Pasta_para_guardar_estilos+'/'+ nome + '.qml')
        progress.setInfo('<br/>Estilo da camada %s salvo.' %nome)


progress.setInfo('<br/><br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(5)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)