"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-05-24
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
# Verificacao de cobertura terrestre (SOBREPOSICAO)
##06. Cob Ter Sobreposicao=name
##LF2) Revisao=group
##Camada_de_Sobreposicao=output vector

saida = Camada_de_Sobreposicao
tol = 0.1

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

CT = [  'hid_massa_dagua_a',
            'hid_trecho_massa_dagua_a',
            'hid_barragem_a',
            'loc_area_edificada_a',
            'rel_terreno_exposto_a',
            'rel_alter_fisiog_antropica_a',
            'rel_rocha_a',
            'tra_pista_ponto_pouso_a',
            'veg_campo_a',
            'veg_floresta_a',
            'veg_estepe_a',
            'veg_brejo_pantano_a',
            'veg_caatinga_a',
            'veg_campinarana_a',
            'veg_cerrado_cerradao_a',
            'veg_macega_chavascal_a',
            'veg_mangue_a',
            'veg_veg_area_contato_a',
            'veg_veg_restinga_a',
            'veg_vegetacao_a',
            'veg_veg_cultivada_a']

# Pegando o EPSG do projeto
canvas = iface.mapCanvas()
epsg = int((canvas.mapRenderer().destinationCrs().authid()).split(':')[1])


# Varrer camadas e pegar as geometrias das classes que compoe a cobertura terrestre
# Carregar cada feicao na camada temporaria
lista = []
cont = 1
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.name() in CT:
        for feature in layer.getFeatures():
            geom = feature.geometry()
            if geom:
                coord = geom.asPolygon()
                if coord == []:
                    COORD = geom.asMultiPolygon()
                    for coord in COORD:
                        if coord != []:
                            lista += [(coord, layer.name())]
                            cont +=1
                else:
                    if coord != []:
                        lista += [(coord, layer.name())]
                        cont +=1

# Cirando camada de sobreposicao
fields = QgsFields()
fields.append(QgsField('id', QVariant.Int))
fields.append(QgsField('camada1', QVariant.String))
fields.append(QgsField('camada2', QVariant.String))
CRS = QgsCoordinateReferenceSystem()
CRS.createFromSrid(epsg)
encoding = 'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(saida, encoding, fields, QGis.WKBPolygon, CRS, formato)

# Verificar Sobreposicao
fet =QgsFeature()
tam = len(lista)
cont = 0
for i in range(tam-1):
    for j in range(i+1, tam):
        A = QgsGeometry.fromPolygon(lista[i][0])
        B = QgsGeometry.fromPolygon(lista[j][0])
        if A.overlaps(B) or A.equals(B):
            C = A.intersection(B)
            if C.asPolygon() != []:
                cont +=1
                att = [cont, lista[i][1], lista[j][1]]
                if C.area() > tol:
                    fet.setGeometry(C)
                    fet.setAttributes(att)
                    writer.addFeature(fet)
            elif C.asMultiPolygon() != []:
                for pol in C.asMultiPolygon():
                    cont +=1
                    att = [cont, lista[i][1], lista[j][1]]
                    geom = QgsGeometry.fromPolygon(pol)
                    if geom.area()>tol:
                        fet.setGeometry(geom)
                        fet.setAttributes(att)
                        writer.addFeature(fet)
    progress.setPercentage(int(((i+1)/float(tam))*100))
        
del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>3 CGEO</b><br/>')
progress.setInfo('<b>Cap Leandro - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 
time.sleep(3)