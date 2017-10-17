"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-07-27
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
# Sobreposicao de Poligonos Nao Cob Ter
##14. Sobrepos de Poligonos=name
##LF2) Revisao=group
##Camada_de_Sobreposicao=output vector

saida = Camada_de_Sobreposicao
tol = 0.1

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time

classes = [  'rel_duna_a',
'edu_area_ruinas_a',
'eco_descontinuidade_geometrica_a',
'tra_edif_constr_portuaria_a',
'rel_elemento_fisiog_natural_a',
'tra_edif_rodoviaria_a',
'tra_obstaculo_navegacao_a',
'loc_hab_indigena_a',
'hid_foz_maritima_a',
'adm_posto_fiscal_a',
'pto_descontinuidade_geometrica_a',
'edu_area_religiosa_a',
'asb_dep_saneamento_a',
'eco_area_ext_mineral_a',
'tra_atracadouro_a',
'lim_bairro_a',
'hid_queda_dagua_a',
'asb_area_saneamento_a',
'lim_regiao_administrativa_a',
'sau_descontinuidade_geometrica_a',
'hid_bacia_hidrografica_a',
'enc_est_gerad_energia_eletr_a',
'edu_area_lazer_a',
'asb_cemiterio_a',
'hid_banco_areia_a',
'tra_area_estrut_transporte_a',
'loc_area_urbana_isolada_a',
'eco_equip_agropec_a',
'loc_descontinuidade_geometrica_a',
'eco_plataforma_a',
'edu_edif_const_lazer_a',
'pto_edif_constr_est_med_fen_a',
'adm_descontinuidade_geometrica_a',
'tra_edif_metro_ferroviaria_a',
'lim_area_especial_a',
'lim_unidade_uso_sustentavel_a',
'lim_unidade_conserv_nao_snuc_a',
'tra_fundeadouro_a',
'lim_area_politico_adm_a',
'hid_ilha_a',
'tra_area_duto_a',
'enc_termeletrica_a',
'edu_descontinuidade_geometrica_a',
'tra_faixa_seguranca_a',
'rel_descontinuidade_geometrica_a',
'sau_edif_saude_a',
'asb_edif_abast_agua_a',
'eco_ext_mineral_a',
'eco_edif_agrop_ext_veg_pesca_a',
'eco_deposito_geral_a',
'edu_edif_const_turistica_a',
'eco_area_comerc_serv_a',
'lim_municipio_a',
'tra_eclusa_a',
'asb_dep_abast_agua_a',
'edu_edif_ensino_a',
'adm_area_pub_civil_a',
'enc_area_comunicacao_a',
'eco_edif_comerc_serv_a',
'lim_area_uso_comunitario_a',
'lim_pais_a',
'aux_objeto_desconhecido_a',
'hid_corredeira_a',
'enc_zona_linhas_energia_com_a',
'lim_unidade_protecao_integral_a',
'asb_area_abast_agua_a',
'enc_hidreletrica_a',
'tra_patio_a',
'lim_terra_publica_a',
'eco_edif_industrial_a',
'edu_arquibancada_a',
'tra_posto_combustivel_a',
'hid_natureza_fundo_a',
'enc_edif_energia_a',
'loc_area_habitacional_a',
'edu_ruina_a',
'lim_sub_distrito_a',
'hid_rocha_em_agua_a',
'adm_posto_pol_rod_a',
'rel_dolina_a',
'asb_edif_saneamento_a',
'lim_distrito_a',
'aux_descontinuidade_geometrica_a',
'enc_descontinuidade_geometrica_a',
'edu_piscina_a',
'hid_area_umida_a',
'lim_terra_indigena_a',
'adm_area_pub_militar_a',
'adm_edif_pub_militar_a',
'hid_terreno_suj_inundacao_a',
'edu_area_ensino_a',
'edu_campo_quadra_a',
'sau_edif_servico_social_a',
'loc_edif_habitacional_a',
'adm_edif_pub_civil_a',
'eco_area_industrial_a',
'eco_edif_ext_mineral_a',
'hid_recife_a',
'pto_area_est_med_fenom_a',
'aux_area_a',
'tra_local_critico_a',
'enc_grupo_transformadores_a',
'edu_coreto_tribuna_a',
'lim_area_desenv_controle_a',
'eco_area_agrop_ext_veg_pesca_a',
'lim_area_de_litigio_a',
'lim_descontinuidade_geometrica_a',
'asb_descontinuidade_geometrica_a',
'enc_edif_comunic_a',
'hid_quebramar_molhe_a',
'loc_edificacao_a',
'sau_area_saude_a',
'lim_outras_unid_protegidas_a',
'edu_edif_religiosa_a',
'tra_edif_constr_aeroportuaria_a',
'hid_reservatorio_hidrico_a',
'lim_unidade_federacao_a',
'tra_descontinuidade_geometrica_a',
'sau_area_servico_social_a',
'lim_area_particular_a',
'enc_area_energia_eletrica_a']

# Pegando o EPSG do projeto
canvas = iface.mapCanvas()
epsg = int((canvas.mapRenderer().destinationCrs().authid()).split(':')[1])


# Varrer camadas e pegar as geometrias das classes que compoe a cobertura terrestre
# Carregar cada feicao na camada temporaria
lista = []
cont = 1
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.name() in classes:
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

progress.setInfo('<b>Opera&ccedil;&atilde;o conclu&iacute;da!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=7)