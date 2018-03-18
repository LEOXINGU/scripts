"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-06-01
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
# Verificacao de medidas minimas
##11. Medidas Minimas=name
##LF02) Revisao=group
##Moldura=vector
##Escala=selection 1:25.000;1:50.000
##Verificar_Trecho_de_Drenagem=boolean False
##Saida=output vector

lista = [0, 1]
escala = lista[Escala]
saida = Saida
moldura = Moldura

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

# Medidas minimas
min_pol = {'adm_area_pub_civil_a': [15625, 20, 62500, 40],
'adm_area_pub_militar_a': [15625, 20, 62500, 40],
'adm_edif_pub_civil_a': [625, 12,5, 2500, 25],
'adm_edif_pub_militar_a': [625, 12,5, 2500, 25],
'adm_posto_pol_rod_a': [625, 12,5, 2500, 25],
'asb_area_abast_agua_a': [15625, 20, 62500, 40],
'asb_area_saneamento_a': [15625, 20, 62500, 40],
'asb_cemiterio_a': [2500, 20, 10000, 40],
'asb_dep_abast_agua_a': [625, 12,5, 2500, 25],
'asb_dep_saneamento_a': [625, 12,5, 2500, 25],
'asb_edif_abast_agua_a': [625, 12,5, 2500, 25],
'asb_edif_saneamento_a': [625, 12,5, 2500, 25],
'eco_area_comerc_serv_a': [15625, 20, 62500, 40],
'eco_area_ext_mineral_a': [15625, 20, 62500, 40],
'eco_area_industrial_a': [15625, 20, 62500, 40],
'eco_deposito_geral_a': [625, 12,5, 2500, 25],
'eco_edif_agrop_ext_veg_pesca_a': [625, 12,5, 2500, 25],
'eco_edif_comerc_serv_a': [625, 12,5, 2500, 25],
'eco_edif_ext_mineral_a': [625, 12,5, 2500, 25],
'eco_edif_industrial_a': [625, 12,5, 2500, 25],
'eco_ext_mineral_a': [15625, 20, 62500, 40],
'edu_area_ensino_a': [15625, 20, 62500, 40],
'edu_area_lazer_a': [15625, 20, 62500, 40],
'edu_area_religiosa_a': [15625, 20, 62500, 40],
'edu_area_ruinas_a': [15625, 20, 62500, 40],
'edu_arquibancada_a': [15625, 20, 62500, 40],
'edu_campo_quadra_a': [625, 12,5, 2500, 25],
'edu_edif_const_lazer_a': [625, 12,5, 2500, 25],
'edu_edif_const_turistica_a': [625, 12,5, 2500, 25],
'edu_edif_ensino_a': [625, 12,5, 2500, 25],
'edu_edif_religiosa_a': [625, 12,5, 2500, 25],
'edu_piscina_a': [625, 12,5, 2500, 25],
'enc_area_comunicacao_a': [15625, 20, 62500, 40],
'enc_area_energia_eletrica_a': [15625, 20, 62500, 40],
'enc_edif_comunic_a': [625, 12,5, 2500, 25],
'enc_edif_energia_a': [625, 12,5, 2500, 25],
'enc_est_gerad_energia_eletr_a': [625, 12,5, 2500, 25],
'enc_grupo_transformadores_a': [625, 12,5, 2500, 25],
'hid_area_umida_a': [15625, 50, 62500, 100],
'hid_banco_areia_a': [2500, 20, 10000, 40],
'hid_barragem_a': [2500, 20, 10000, 40],
'hid_corredeira_a': [1000, 20, 4000, 40],
'hid_foz_maritima_a': [2500, 20, 10000, 40],
'hid_ilha_a': [2500, 20, 10000, 40],
'hid_massa_dagua_a': [2500, 20, 10000, 40],
'hid_quebramar_molhe_a': [1000, 20, 4000, 40],
'hid_rocha_em_agua_a': [2500, 20, 10000, 40],
'hid_terreno_suj_inundacao_a': [15625, 50, 62500, 100],
'hid_trecho_massa_dagua_a': [2500, 20, 10000, 40],
'loc_area_edificada_a': [15625, 20, 62500, 40],
'loc_area_habitacional_a': [15625, 20, 62500, 40],
'loc_area_urbana_isolada_a': [15625, 20, 62500, 40],
'loc_edif_habitacional_a': [625, 12,5, 2500, 25],
'loc_edificacao_a': [625, 12,5, 2500, 25],
'rel_alter_fisiog_antropica_a': [5000, 50, 20000, 100],
'rel_dolina_a': [15625, 20, 62500, 40],
'rel_duna_a': [15625, 20, 62500, 40],
'rel_terreno_exposto_a': [15625, 20, 62500, 40],
'sau_area_saude_a': [15625, 20, 62500, 40],
'sau_area_servico_social_a': [15625, 20, 62500, 40],
'sau_edif_saude_a': [625, 12,5, 2500, 25],
'sau_edif_servico_social_a': [625, 20, 2500, 40],
'tra_atracadouro_a': [15625, 20, 62500, 40],
'tra_edif_constr_aeroportuaria_a': [625, 12,5, 2500, 25],
'tra_edif_constr_portuaria_a': [625, 12,5, 2500, 25],
'tra_edif_metro_ferroviaria_a': [625, 12,5, 2500, 25],
'tra_edif_rodoviaria_a': [625, 12,5, 2500, 25],
'tra_patio_a': [15625, 20, 62500, 40],
'tra_pista_ponto_pouso_a': [2500, 20, 10000, 40],
'tra_posto_combustivel_a': [625, 12,5, 2500, 25],
'veg_brejo_pantano_a': [15625, 50, 62500, 100],
'veg_caatinga_a': [15625, 50, 62500, 100],
'veg_campo_a': [15625, 50, 62500, 100],
'veg_cerrado_cerradao_a': [15625, 50, 62500, 100],
'veg_estepe_a': [15625, 50, 62500, 100],
'veg_floresta_a': [15625, 50, 62500, 100],
'veg_macega_chavascal_a': [15625, 50, 62500, 100],
'veg_mangue_a': [15625, 50, 62500, 100],
'veg_veg_cultivada_a': [15625, 50, 62500, 100],
'veg_veg_restinga_a': [15625, 50, 62500, 100],
'veg_vegetacao_a': [15625, 50, 62500, 100]}

min_lin = {'edu_pista_competicao_l': [125, 250],
'enc_est_gerad_energia_eletr_l': [20, 40],
'enc_hidreletrica_l': [20, 40],
'enc_trecho_comunic_l': [125, 250],
'enc_trecho_energia_l': [125, 250],
'hid_banco_areia_l': [20, 40],
'hid_barragem_l': [20, 40],
'hid_comporta_l': [20, 40],
'hid_corredeira_l': [20, 40],
'hid_foz_maritima_l': [20, 40],
'hid_ilha_l': [20, 40],
'hid_quebramar_molhe_l': [20, 40],
'rel_alter_fisiog_antropica_l': [100, 200],
'rel_elemento_fisiog_natural_l': [250, 500],
'tra_arruamento_l': [50, 100],
'tra_atracadouro_l': [20, 40],
'tra_galeria_bueiro_l': [20, 40],
'tra_passag_elevada_viaduto_l': [20, 40],
'tra_pista_ponto_pouso_l': [125, 250],
'tra_ponte_l': [20, 40],
'tra_travessia_l': [20, 40],
'tra_travessia_pedestre_l': [20, 40],
'tra_trecho_duto_l': [125, 250],
'tra_trecho_ferroviario_l': [125, 250],
'tra_trecho_hidroviario_l': [500, 1000],
'tra_trecho_rodoviario_l': [125, 250],
'tra_trilha_picada_l': [250, 500],
'tra_tunel_l': [125, 250]}

if Verificar_Trecho_de_Drenagem:
    min_lin['hid_trecho_drenagem_l'] = [500, 1000]

# Pegando o EPSG da moldura
frame = processing.getObject(moldura)
crs = frame.crs()
feat = frame.getFeatures().next()
geom = feat.geometry()
coord = geom.asMultiPolygon()
geom = QgsGeometry.fromPolyline(coord[0][0])
Buffer = geom.buffer(1,5)

# Criar arquivo de pontos para armazenar as informacoes
fields = QgsFields()
fields.append(QgsField('id', QVariant.Int))
fields.append(QgsField('problema', QVariant.String))
fields.append(QgsField( 'medida', QVariant.Double, "numeric", 14, 3))
fields.append(QgsField( 'previsto', QVariant.Int))
fields.append(QgsField('classe', QVariant.String))
fields.append(QgsField('classe_id', QVariant.Int))

writer = QgsVectorFileWriter(saida, 'utf-8', fields, QGis.WKBPoint, crs, 'ESRI Shapefile')

# Mensagem de inicio de processamento
if escala ==0:
    progress.setInfo('<b>Processamento para a escala 1:25.000</b><br/>')
else:
    progress.setInfo('<b>Processamento para a escala 1:50.000</b><br/>')

# Verificar medidas minimas
cont = 0
feat = QgsFeature()
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    nome = layer.name()
    # AREA
    if nome in min_pol:
        min_area =  min_pol[nome][2*escala]
        min_larg = min_pol[nome][2*escala+1]
        for feature in layer.getFeatures():
            # Area minima
            geom = feature.geometry()
            area = geom.area()
            if area < min_area:
                if not geom.intersects(Buffer):
                    cont +=1
                    problema = 'Area menor que a area minima'
                    id = feature.id()
                    c = feature.geometry().centroid()
                    feat.setGeometry(c)
                    feat.setAttributes([cont, problema, area, min_area, nome, id])
                    writer.addFeature(feat)
            
            # Largura Minima
            
            # Buffer negativo
            buffNeg = geom.buffer( -0.99*min_larg/2 , 5)
            # Buffer positivo
            if buffNeg.area() > 0:
                buffPos = buffNeg.buffer(2.1*min_larg/2, 5)
                # Diferenca
                Difer = geom.difference(buffPos)
                if Difer:
                    # Pegar centroides do(s) poligono(s) da diferenca
                    lista = Difer.asMultiPolygon()
                    if lista:
                        id = feature.id()
                        for pol in lista:
                            poligono = QgsGeometry.fromPolygon(pol)
                            c = poligono.centroid()
                            cont +=1
                            problema = 'Largura menor que a largura minima'
                            feat.setGeometry(c)
                            feat.setAttributes([cont, problema, None, min_larg, nome, id])
                            writer.addFeature(feat)
                    elif Difer.asPolygon():
                        c = Difer.centroid()
                        cont +=1
                        problema = 'Largura menor que a largura minima'
                        feat.setGeometry(c)
                        feat.setAttributes([cont, problema, None, min_larg, nome, id])
                        writer.addFeature(feat)
            else:
                c = geom.centroid()
                cont +=1
                problema = 'Largura menor que a largura minima'
                feat.setGeometry(c)
                feat.setAttributes([cont, problema, None, min_larg, nome, id])
                writer.addFeature(feat)
    
    # LINHA
    if nome in min_lin:
        min_comp = min_lin[nome][escala]
        for feature in layer.getFeatures():
            # Comprimento minimo
            geom = feature.geometry()
            comp = geom.length()
            if comp < min_comp:
                if not geom.intersects(Buffer):
                    cont +=1
                    problema = 'Comprimento menor que o minimo'
                    id = feature.id()
                    c = feature.geometry().centroid()
                    feat.setGeometry(c)
                    feat.setAttributes([cont, problema, comp, min_comp, nome, id])
                    writer.addFeature(feat)


del writer

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)