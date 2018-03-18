# -*- coding: utf-8 -*-
"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-05-30
        copyright            : (C) 2017 by Leandro Franca - Cartographic Engineer @ Brazilian Army
        email                : franca.leandro@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation.                              *
 *                                                                         *
 ***************************************************************************/
"""
# Identifica geometrias imprestaveis
##Geometrias Problematicas=name
##LF11) Outros=group
##Arquivo_txt=output file

if Arquivo_txt[-4:] != '.txt':
    Arquivo_txt += '.txt'

# Criar arquivo txt
arquivo = open(Arquivo_txt, 'w')
arquivo.write('RELATORIO DE GEOMETRIAS IMPRESTAVEIS\n')

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time

cont = 0
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    nome = layer.name()
    for feat in layer.getFeatures():
        geom = feat.geometry()
        
        if not geom:
            id = feat.id()
            arquivo.write('Classe: %s, Id: %d \n' %(nome, id))
            cont +=1

if cont>0:
    arquivo.write('Total de %d geometrias imprestaveis\n' %cont)
else:
    arquivo.write('Nao existe geometria imprestavel na lista de camadas')

arquivo.close()