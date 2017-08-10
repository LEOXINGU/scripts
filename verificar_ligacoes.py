"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-08-09
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
# Revisor de ligacoes
##13. Revisor de ligacoes=name
##LF2) Revisao=group
##Moldura_1=vector
##Moldura_2=vector
##Shapefile_de_Ganchos=output vector

path_name = Shapefile_de_Ganchos

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing


# Abrir moldura A
moldA = processing.getObject(Moldura_1)

# Abrir moldura B
moldB = processing.getObject(Moldura_2)

# Pegar nome dos bancos e setar uri para cada banco
nomeA = (moldA.source()).split("'")[1]
nomeB = (moldB.source()).split("'")[1]

# Verificacao
if moldA.name()=='aux_moldura_a' and moldB.name()=='aux_moldura_a' and nomeA != nomeB:
    from PyQt4.QtCore import *
    # Criar campos
    fields = QgsFields()
    fields.append(QgsField('classeID', QVariant.String))
    fields.append(QgsField('problema', QVariant.String))
    fields.append(QgsField('descricao', QVariant.String))
    SRC = moldA.crs()
    # Criar shapefile de ganchos
    encoding = u'system'
    formato = 'ESRI Shapefile'
    writer = QgsVectorFileWriter(path_name, encoding, fields, QGis.WKBPoint, SRC, formato)
    feature = QgsFeature(fields)

    # Camadas a serem verificadas
    linhas = ['asb_descontinuidade_geometrica_l',
    'eco_descontinuidade_geometrica_l',
    'eco_equip_agropec_l',
    'edu_descontinuidade_geometrica_l',
    'edu_pista_competicao_l',
    'enc_est_gerad_energia_eletr_l',
    'enc_hidreletrica_l',
    'enc_trecho_comunic_l',
    'enc_trecho_energia_l',
    'hid_banco_areia_l',
    'hid_barragem_l',
    'hid_comporta_l',
    'hid_corredeira_l',
    'hid_descontinuidade_geometrica_l',
    'hid_foz_maritima_l',
    'hid_ilha_l',
    'hid_limite_massa_dagua_l',
    'hid_natureza_fundo_l',
    'hid_quebramar_molhe_l',
    'hid_queda_dagua_l',
    'hid_recife_l',
    'hid_trecho_drenagem_l',
    'lim_delimitacao_fisica_l',
    'lim_limite_area_especial_l',
    'lim_limite_intra_munic_adm_l',
    'lim_limite_operacional_l',
    'lim_limite_particular_l',
    'lim_limite_politico_adm_l',
    'lim_linha_de_limite_l',
    'lim_outros_limites_oficiais_l',
    'loc_descontinuidade_geometrica_l',
    'rel_alter_fisiog_antropica_l',
    'rel_curva_batimetrica_l',
    'rel_curva_nivel_l',
    'rel_descontinuidade_geometrica_l',
    'rel_elemento_fisiog_natural_l',
    'tra_arruamento_l',
    'tra_atracadouro_l',
    'tra_caminho_aereo_l',
    'tra_ciclovia_l',
    'tra_condutor_hidrico_l',
    'tra_cremalheira_l',
    'tra_descontinuidade_geometrica_l',
    'tra_eclusa_l',
    'tra_fundeadouro_l',
    'tra_funicular_l',
    'tra_galeria_bueiro_l',
    'tra_local_critico_l',
    'tra_obstaculo_navegacao_l',
    'tra_passag_elevada_viaduto_l',
    'tra_pista_ponto_pouso_l',
    'tra_ponte_l',
    'tra_travessia_l',
    'tra_travessia_pedestre_l',
    'tra_trecho_duto_l',
    'tra_trecho_ferroviario_l',
    'tra_trecho_hidroviario_l',
    'tra_trecho_rodoviario_l',
    'tra_trilha_picada_l',
    'tra_tunel_l']

    poligonos = ['adm_area_pub_civil_a',
    'adm_area_pub_militar_a',
    'adm_descontinuidade_geometrica_a',
    'adm_edif_pub_civil_a',
    'adm_edif_pub_militar_a',
    'adm_posto_fiscal_a',
    'adm_posto_pol_rod_a',
    'asb_area_abast_agua_a',
    'asb_area_saneamento_a',
    'asb_cemiterio_a',
    'asb_dep_abast_agua_a',
    'asb_dep_saneamento_a',
    'asb_descontinuidade_geometrica_a',
    'asb_edif_abast_agua_a',
    'asb_edif_saneamento_a',
    'eco_area_comerc_serv_a',
    'eco_area_ext_mineral_a',
    'eco_area_industrial_a',
    'eco_deposito_geral_a',
    'eco_descontinuidade_geometrica_a',
    'eco_edif_agrop_ext_veg_pesca_a',
    'eco_edif_comerc_serv_a',
    'eco_edif_ext_mineral_a',
    'eco_edif_industrial_a',
    'eco_equip_agropec_a',
    'eco_ext_mineral_a',
    'eco_plataforma_a',
    'edu_area_ensino_a',
    'edu_area_lazer_a',
    'edu_area_religiosa_a',
    'edu_area_ruinas_a',
    'edu_arquibancada_a',
    'edu_campo_quadra_a',
    'edu_coreto_tribuna_a',
    'edu_descontinuidade_geometrica_a',
    'edu_edif_const_lazer_a',
    'edu_edif_const_turistica_a',
    'edu_edif_ensino_a',
    'edu_edif_religiosa_a',
    'edu_piscina_a',
    'edu_ruina_a',
    'enc_area_comunicacao_a',
    'enc_area_energia_eletrica_a',
    'eco_area_agrop_ext_veg_pesca_a',
    'enc_descontinuidade_geometrica_a',
    'enc_edif_comunic_a',
    'enc_edif_energia_a',
    'enc_est_gerad_energia_eletr_a',
    'enc_grupo_transformadores_a',
    'enc_hidreletrica_a',
    'enc_termeletrica_a',
    'enc_zona_linhas_energia_com_a',
    'hid_area_umida_a',
    'hid_bacia_hidrografica_a',
    'hid_banco_areia_a',
    'hid_barragem_a',
    'hid_corredeira_a',
    'hid_foz_maritima_a',
    'hid_ilha_a',
    'hid_massa_dagua_a',
    'hid_natureza_fundo_a',
    'hid_quebramar_molhe_a',
    'hid_queda_dagua_a',
    'hid_recife_a',
    'hid_reservatorio_hidrico_a',
    'hid_rocha_em_agua_a',
    'hid_terreno_suj_inundacao_a',
    'hid_trecho_massa_dagua_a',
    'lim_area_de_litigio_a',
    'lim_area_desenv_controle_a',
    'lim_area_especial_a',
    'lim_area_particular_a',
    'lim_area_politico_adm_a',
    'lim_area_uso_comunitario_a',
    'lim_bairro_a',
    'lim_descontinuidade_geometrica_a',
    'lim_distrito_a',
    'lim_municipio_a',
    'lim_outras_unid_protegidas_a',
    'lim_pais_a',
    'lim_regiao_administrativa_a',
    'lim_sub_distrito_a',
    'lim_terra_indigena_a',
    'lim_terra_publica_a',
    'lim_unidade_conserv_nao_snuc_a',
    'lim_unidade_federacao_a',
    'lim_unidade_protecao_integral_a',
    'lim_unidade_uso_sustentavel_a',
    'loc_area_edificada_a',
    'loc_area_habitacional_a',
    'loc_area_urbana_isolada_a',
    'loc_descontinuidade_geometrica_a',
    'loc_edif_habitacional_a',
    'loc_edificacao_a',
    'loc_hab_indigena_a',
    'pto_area_est_med_fenom_a',
    'pto_descontinuidade_geometrica_a',
    'pto_edif_constr_est_med_fen_a',
    'rel_alter_fisiog_antropica_a',
    'rel_descontinuidade_geometrica_a',
    'rel_dolina_a',
    'rel_duna_a',
    'rel_elemento_fisiog_natural_a',
    'rel_rocha_a',
    'rel_terreno_exposto_a',
    'sau_area_saude_a',
    'sau_area_servico_social_a',
    'sau_descontinuidade_geometrica_a',
    'sau_edif_saude_a',
    'sau_edif_servico_social_a',
    'tra_area_duto_a',
    'tra_area_estrut_transporte_a',
    'tra_atracadouro_a',
    'tra_descontinuidade_geometrica_a',
    'tra_eclusa_a',
    'tra_edif_constr_aeroportuaria_a',
    'tra_edif_constr_portuaria_a',
    'tra_edif_metro_ferroviaria_a',
    'tra_edif_rodoviaria_a',
    'tra_faixa_seguranca_a',
    'tra_fundeadouro_a',
    'tra_local_critico_a',
    'tra_obstaculo_navegacao_a',
    'tra_patio_a',
    'tra_pista_ponto_pouso_a',
    'tra_posto_combustivel_a',
    'veg_brejo_pantano_a',
    'veg_caatinga_a',
    'veg_campinarana_a',
    'veg_campo_a',
    'veg_cerrado_cerradao_a',
    'veg_estepe_a',
    'veg_floresta_a',
    'veg_macega_chavascal_a',
    'veg_mangue_a',
    'veg_veg_area_contato_a',
    'veg_veg_cultivada_a',
    'veg_veg_restinga_a',
    'veg_vegetacao_a']

    # Transformar as molduras em geometria linha
    feat = moldA.getFeatures().next()
    pol = feat.geometry()
    coord = pol.asMultiPolygon()
    linA = QgsGeometry.fromMultiPolyline(coord[0])

    feat = moldB.getFeatures().next()
    pol = feat.geometry()
    coord = pol.asMultiPolygon()
    linB = QgsGeometry.fromMultiPolyline(coord[0])

    # Verificar se as molduras se interseptam
    if  linA.intersects(linB):
        # Verificar intersecao
        buffLinA = linA.buffer(0.5,5)
        buffLinB = linB.buffer(0.5,5)
        Inter = buffLinA.intersection(buffLinB)
        # Criar Buffer
        Buffer = Inter.buffer(0.5,5)
        # Criar lista do DB "A" e do DB "B" que interseptam a area de ligacao
        LinA = []
        LinB = []
        PolA = []
        PolB = []
        dict_fields = {}
        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            if layer.type()==0 and layer.name() in linhas:
                # Pegando o nome dos atributos
                if not (layer.name() in dict_fields):
                    dict_fields[layer.name()] = [field.name() for field in layer.pendingFields()]
                for feat in layer.getFeatures():
                    geom = feat.geometry()
                    if geom.intersects(Buffer):
                        coord = geom.asMultiPolyline()
                        if coord:
                            nomeBanco = (layer.source()).split("'")[1]
                            if nomeBanco == nomeA:
                                LinA += [[layer.name(), feat.attributes(), coord]]
                            elif nomeBanco == nomeB:
                                LinB += [[layer.name(), feat.attributes(), coord]]
            if layer.type()==0 and layer.name() in poligonos:
                # Pegando o nome dos atributos
                if not (layer.name() in dict_fields):
                    dict_fields[layer.name()] = [field.name() for field in layer.pendingFields()]
                for feat in layer.getFeatures():
                    geom = feat.geometry()
                    if geom.intersects(Buffer):
                        coord = geom.asMultiPolygon()
                        if coord:
                            nomeBanco = (layer.source()).split("'")[1]
                            if nomeBanco == nomeA:
                                PolA += [[layer.name(), feat.attributes(), coord]]
                            elif nomeBanco == nomeB:
                                PolB += [[layer.name(), feat.attributes(), coord]]

        # Verificar se a geometria de A toca (ou intersepta) outra geometria de B
        for itemA in LinA:
            nomeA = itemA[0]
            geomA = QgsGeometry.fromMultiPolyline(itemA[2])
            buffA = geomA.buffer(1,5)
            attA = itemA[1]
            sentinela = False
            for itemB in LinB:
                nomeB = itemB[0]
                geomB = QgsGeometry.fromMultiPolyline(itemB[2])
                buffB = geomB.buffer(1,5)
                attB = itemB[1]
                if buffA.intersects(buffB):
                    sentinela = True
                    # Verificar classes
                    if not(nomeA == nomeB):
                        # Problema 1
                        att = [nomeA+': ' + str(attA[0]) + ' e ' +nomeB+': ' + str(attB[0]) , 'Ligacao entre classes diferentes', 'Ligacao incompativel entre as classes ' +nomeA+ ' e ' +nomeB]
                        geom = buffA.intersection(buffB)
                        c = geom.centroid()
                        feature.setGeometry(c)
                        feature.setAttributes(att)
                        writer.addFeature(feature)
                    else:
                        # Verificar atributos
                        if not(attA[1:min(len(attA), len(attB))-1] == attB[1:min(len(attA), len(attB))-1]):
                            # Problema 2
                            texto = 'Os atributos '
                            for k in range(1, min(len(attA), len(attB))-1):
                                if attA[k] != attB[k]:
                                    campo = dict_fields[nomeA][k]
                                    texto += '"' +campo +'", '
                            texto = texto[:-2] + ' nao conferem'
                            att = [nomeA+': ' + str(attA[0]) + ' e ' + str(attB[0]) , 'Atributos nao conferem', texto]
                            geom = buffA.intersection(buffB)
                            c = geom.centroid()
                            feature.setGeometry(c)
                            feature.setAttributes(att)
                            writer.addFeature(feature)
            if not sentinela:
                # Problema 3
                att = [nomeA+': ' + str(attA[0]), 'Feicao nao esta ligada']
                geom = buffA.intersection(Buffer)
                c = geom.centroid()
                feature.setGeometry(c)
                feature.setAttributes(att)
                writer.addFeature(feature)

        for itemB in LinB:
            nomeB = itemB[0]
            geomB = QgsGeometry.fromMultiPolyline(itemB[2])
            buffB = geomB.buffer(1,5)
            sentinela = False
            for itemA in LinA:
                nomeA = itemA[0]
                geomA = QgsGeometry.fromMultiPolyline(itemA[2])
                buffA = geomA.buffer(1,5)
                if buffA.intersects(buffB):
                    sentinela = True
            if not sentinela:
                # Problema 3
                att = [nomeB+': ' + str(attB[0]), 'Feicao nao esta ligada']
                geom = buffB.intersection(Buffer)
                c = geom.centroid()
                feature.setGeometry(c)
                feature.setAttributes(att)
                writer.addFeature(feature)
        
        for itemA in PolA:
            nomeA = itemA[0]
            geomA = QgsGeometry.fromMultiPolygon(itemA[2])
            buffA = geomA.buffer(1,5)
            attA = itemA[1]
            sentinela = False
            for itemB in PolB:
                nomeB = itemB[0]
                geomB = QgsGeometry.fromMultiPolygon(itemB[2])
                buffB = geomB.buffer(1,5)
                attB = itemB[1]
                if buffA.intersects(buffB):
                    intersecao = buffA.intersection(buffB)
                    if intersecao.area() > 10:
                        sentinela = True
                        # Verificar classes
                        if not(nomeA == nomeB):
                            # Problema 1
                            att = [nomeA+': ' + str(attA[0]) + ' e ' +nomeB+': ' + str(attB[0]) , 'Ligacao entre classes diferentes', 'Ligacao incompativel entre as classes ' +nomeA+ ' e ' +nomeB]
                            geom = buffA.intersection(buffB)
                            c = geom.centroid()
                            feature.setGeometry(c)
                            feature.setAttributes(att)
                            writer.addFeature(feature)
                        # Verificar atributos
                        elif not(attA[1:min(len(attA), len(attB))-1] == attB[1:min(len(attA), len(attB))-1]):
                            # Problema 2
                            texto = 'Os atributos '
                            for k in range(1, min(len(attA), len(attB))-1):
                                if attA[k] != attB[k]:
                                    campo = dict_fields[nomeA][k]
                                    texto += '"' +campo +'", '
                            texto = texto[:-2] + ' nao conferem'
                            att = [nomeA+': ' + str(attA[0]) + ' e ' + str(attB[0]) , 'Atributos nao conferem', texto]
                            geom = buffA.intersection(buffB)
                            c = geom.centroid()
                            feature.setGeometry(c)
                            feature.setAttributes(att)
                            writer.addFeature(feature)
            if not sentinela:
                # Problema 3
                att = [nomeA+': ' + str(attA[0]), 'Feicao nao esta ligada']
                geom = buffA.intersection(Buffer)
                c = geom.centroid()
                feature.setGeometry(c)
                feature.setAttributes(att)
                writer.addFeature(feature)

        for itemB in PolB:
            nomeB = itemB[0]
            geomB = QgsGeometry.fromMultiPolygon(itemB[2])
            buffB = geomB.buffer(1,5)
            sentinela = False
            for itemA in PolA:
                nomeA = itemA[0]
                geomA = QgsGeometry.fromMultiPolygon(itemA[2])
                buffA = geomA.buffer(1,5)
                if buffA.intersects(buffB):
                    intersecao = buffA.intersection(buffB)
                    if intersecao.area() > 10:
                        sentinela = True
            if not sentinela:
                # Problema 3
                att = [nomeB+': ' + str(attB[0]), 'Feicao nao esta ligada']
                geom = buffB.intersection(Buffer)
                c = geom.centroid()
                feature.setGeometry(c)
                feature.setAttributes(att)
                writer.addFeature(feature)

    del writer


    progress.setInfo('<b>Opera&ccedil;&atilde;o conclu&iacute;da com sucesso!</b><br/><br/>')
    progress.setInfo('<b>3&ordm; CGEO</b><br/>')
    progress.setInfo('<b>Cap Leandro - Eng Cart</b><br/>')
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
    time.sleep(5)
else:
    progress.setInfo('<br/><b><font  color="#ff0000">Escolha duas camadas de moldura de bancos distintos.</b><br/><br/>')
    iface.messageBar().pushMessage(u'Problema', "Verifique as camadas de moldura de entrada.", level=QgsMessageBar.WARNING, duration=10)
    time.sleep(7)