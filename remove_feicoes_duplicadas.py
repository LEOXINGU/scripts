"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-10-10
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
# Verificar Auto-Intersecao
##LF2) Revisao=group
##06. Remover Feicoes Duplicadas=name

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

# Camada para nao verificar
nao_verif = ['rel_curva_nivel_l',
                    'hid_trecho_drenagem_l']

# Varrer camadas
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.type()==0:
        cont = 0
        lista = []
        apagar = []
        for feat in layer.getFeatures():
            geom = feat.geometry()
            coord = geom.exportToGeoJSON()
            att = feat.attributes()
            if [coord, att[1:]] in lista:
                apagar += [feat.id()]
                cont += 1
            else:
                lista += [[coord, att[1:]]]
        # Apagar feicoes
        if apagar:
            DP = layer.dataProvider()
            print apagar
            DP.deleteFeatures(apagar)
            progress.setInfo('<b>Classe: %s </b><br/>' %layer.name())
            progress.setInfo('- %d feicoes duplicadas removidas.<br/>' %cont)

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(8)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)