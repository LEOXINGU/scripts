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
##CT para BD=name
##LF8) EDGV=group
##Cobertura_Terrestre=vector


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

# Abrir camada de CT
CT_layer = processing.getObject(Cobertura_Terrestre)

# Colocar geometrias da CT em um dicionario
if CT_layer.geometryType() == QGis.Polygon:
    DIC = {}
    classes = []
    for feat in CT_layer.getFeatures():
        att = feat.attributes()
        classe = att[1]
        if not classe in classes:
            DIC[classe] = {}
            classes += [classe]

    for feat in CT_layer.getFeatures():
        geom = feat.geometry()
        if geom:
            coord = geom.asPolygon()
            if coord == []:
                coord = geom.asMultiPolygon()
            else:
                coord = [coord]
        att = feat.attributes()
        classe = att[1]
        ID = att[2]
        DIC[classe][ID] = coord

Banco_de_Dados = att[0]

# Varrer camadas e subtituir geometrias das camadas da CT
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.type()==0:
        try:
            lyr_source = (layer.source()).split("'")[1]
            layer_name = layer.name()
            if lyr_source == Banco_de_Dados and layer_name in CT:
                DP = layer.dataProvider()
                for feature in layer.getFeatures():
                    ID = feature.id()
                    coord = DIC[layer_name][ID]
                    newGeom = QgsGeometry.fromMultiPolygon(coord)
                    newGeomMap = {ID : newGeom}
                    DP.changeGeometryValues(newGeomMap)
                    
        except:
            pass

progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(5)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)