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
# Verificacao da Cob Ter (juntar todas as classes que compoe a Cob Ter)
##Cob Ter=name
##LF7) Outros=group
##Moldura=vector
##Todas_os_poligonos_de_Cob_Ter=output vector

path_name = Todas_os_poligonos_de_Cob_Ter

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
from processing.tools.vector import VectorWriter
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
#            'veg_veg_area_contato_a',
            'veg_veg_restinga_a',
#            'veg_vegetacao_a',
            'veg_veg_cultivada_a']

# Moldura
moldura = processing.getObject(Moldura)

# Criar camada de todas as geometrias
fields = QgsFields()
fields.append(QgsField('id', QVariant.Int))
fields.append(QgsField('classe', QVariant.String))
encoding = 'utf-8'
writer = VectorWriter(path_name, encoding, fields, QGis.WKBPolygon, moldura.crs())

cont = 1
feat =QgsFeature(fields)
# Varrer camadas e pegar as geometrias das classes que compoe a cobertura terrestre
# Carregar cada feicao na camada temporaria
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.name() in CT:
        for feature in layer.getFeatures():
            geom = feature.geometry()
            coord = geom.asPolygon()
            if coord == []:
                COORD =geom.asMultiPolygon()
                for coord in COORD:
                    new_geom = QgsGeometry.fromPolygon(coord)
                    feat.setGeometry(new_geom)
                    feat.setAttributes([cont, layer.name()])
                    writer.addFeature(feat)
                    cont +=1
            else:
                new_geom = QgsGeometry.fromPolygon(coord)
                feat.setGeometry(new_geom)
                feat.setAttributes([cont, layer.name()])
                writer.addFeature(feat)
                cont +=1

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>3 CGEO</b><br/>')
progress.setInfo('<b>Cap Leandro - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
time.sleep(3)