"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-03-07
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
# Juntar Camadas de CT em uma Camada
##BD para CT=name
##LF8) EDGV=group
##Banco_de_Dados=string
##Cobertura_Terrestre=output vector


from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing

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

# Pegar o SRC do BD
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.type()==0:
        try:
            lyr_source = (layer.source()).split("'")[1]
            if lyr_source == Banco_de_Dados:
                SRC = layer.crs()
        except:
            pass

# Cirando camada de sobreposicao
fields = QgsFields()
fields.append(QgsField('BD', QVariant.String))
fields.append(QgsField('classe', QVariant.String))
fields.append(QgsField('id', QVariant.Int))
encoding = 'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(Cobertura_Terrestre, encoding, fields, QGis.WKBMultiPolygon, SRC, formato)


# Varrer camadas e pegar as geometrias das classes que compoe a cobertura terrestre
feat =QgsFeature()
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.type()==0:
        try:
            lyr_source = (layer.source()).split("'")[1]
            layer_name = layer.name()
            if lyr_source == Banco_de_Dados and layer_name in CT:
                for feature in layer.getFeatures():
                    ID = feature.id()
                    geom = feature.geometry()
                    att = [Banco_de_Dados, layer_name, ID]
                    feat.setGeometry(geom)
                    feat.setAttributes(att)
                    ok = writer.addFeature(feat)
        except:
            pass
            
del writer

progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(5)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)