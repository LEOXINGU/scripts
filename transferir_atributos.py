"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-05-09
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
# Transferir atributos entre camadas pela posicao
##Transferir Atributos=name
##LF04) Vetor=group
##Camada_de_Origem=vector
##Campo_de_Origem=field Camada_de_Origem
##Camada_de_Destino=vector
##Campo_de_Destino=field Camada_de_Destino
##Tamanho_do_Buffer=number 150.0
##Percentual_dentro_do_Buffer=number 90.0

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing

# Abrir camadas
origem = processing.getObject(Camada_de_Origem)
destino = processing.getObject(Campo_de_Destino)
tol = Tamanho_do_Buffer
percentual = Percentual_dentro_do_Buffer/100.0
att_column = destino.pendingFields().fieldNameIndex(Campo_de_Destino)
DP = destino.dataProvider()

# Transformacao de Unidades
if origem.crs().geographicFlag():
    tol/= float(111000)

if origem.geometryType() != QGis.Line or destino.geometryType() != QGis.Line:
    progress.setInfo('<b>As camadas devem ser do tipo "Linha"!</b><br/>')
    iface.messageBar().pushMessage(u'Situacao', "As camadas devem ser do tipo Linha!", level=QgsMessageBar.CRITICAL, duration=5)
else:
    # Criar lista de Buffers e atributo
    BUFFERS = []
    for feat in origem.getFeatures():
        geom = feat.geometry()
        if geom and feat[Campo_de_Origem] != None:
            geomBuffer = geom.buffer(tol, 5)
            coord = geomBuffer.asPolygon()
            if coord:
                BUFFERS += [[coord, feat[Campo_de_Origem]]]

    for feat in destino.getFeatures():
                        geom = feat.geometry()
                        if geom:
                            comp = geom.length()
                            for item in BUFFERS:
                                geomBuffer = QgsGeometry.fromPolygon(item[0])
                                if geom.intersects(geomBuffer):
                                    intersecao = geom.intersection(geomBuffer)
                                    comp_inter = intersecao.length()
                                    if (comp_inter/comp) >= percentual:
                                        newColumnValueMap = {att_column : item[1]}
                                        newAttributesValuesMap = {feat.id() : newColumnValueMap}
                                        DP.changeAttributeValues(newAttributesValuesMap)

    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(3)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)