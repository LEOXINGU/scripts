"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-06-12
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
# Verificar sobreposicao de todas as linhas da lista de camadas
##Remover Camadas=name
##LF8) Outros=group

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time

LISTA = ['hid_confluencia_p',
                'hid_descontinuidade_geometrica_p',
                'hid_natureza_fundo_p',
                'hid_ponto_drenagem_p',
                'hid_ponto_inicio_drenagem_p',
                'hid_ponto_inicio_drenagem_p',
                'hid_limite_massa_dagua_l',
                'hid_natureza_fundo_l',
                'hid_bacia_hidrografica_a',
                'hid_natureza_fundo_a',
                'hid_reservatorio_hidrico_a',
                'rel_descontinuidade_geometrica_p',
                'rel_ponto_cotado_batimetrico_p',
                'rel_curva_batimetrica_l',
                'rel_descontinuidade_geometrica_l',
                'rel_descontinuidade_geometrica_a',
                'veg_descontinuidade_geometrica_p',
                'veg_descontinuidade_geometrica_l',
                'veg_vegetacao_a',
                'veg_veg_area_contato_a',
                'tra_cremalheira_p',
                'tra_descontinuidade_geometrica_p',
                'tra_entroncamento_p',
                'tra_local_critico_p',
                'tra_ponto_duto_p',
                'tra_ponto_ferroviario_p',
                'tra_ponto_hidroviario_p',
                'tra_ponto_rodoviario_p',
                'tra_ciclovia_l',
                'tra_cremalheira_l',
                'tra_descontinuidade_geometrica_l',
                'tra_local_critico_l',
                'tra_area_duto_a',
                'tra_descontinuidade_geometrica_a',
                'tra_faixa_seguranca_a',
                'tra_local_critico_a',
                'enc_descontinuidade_geometrica_p',
                'enc_ponto_trecho_energia_p',
                'enc_torre_comunic_p',
                'enc_torre_energia_p',
                'enc_trecho_comunic_l',
                'enc_trecho_energia_l',
                'enc_descontinuidade_geometrica_a',
                'enc_zona_linhas_energia_com_a',
                'asb_descontinuidade_geometrica_p',
                'asb_descontinuidade_geometrica_l',
                'asb_descontinuidade_geometrica_a',
                'edu_descontinuidade_geometrica_p',
                'edu_descontinuidade_geometrica_l',
                'edu_descontinuidade_geometrica_a',
                'aux_descontinuidade_geometrica_p',
                'aux_descontinuidade_geometrica_l',
                'aux_descontinuidade_geometrica_a',
                'eco_equip_agropec_p',
                'eco_descontinuidade_geometrica_p',
                'eco_descontinuidade_geometrica_l',
                'eco_equip_agropec_l',
                'eco_descontinuidade_geometrica_a',
                'eco_equip_agropec_a',
                'loc_localidade_p',
                'loc_descontinuidade_geometrica_p',
                'loc_aglomerado_rural_p',
                'loc_descontinuidade_geometrica_l',
                'loc_descontinuidade_geometrica_a',
                'pto_pto_geod_topo_controle_p',
                'pto_pto_controle_p',
                'pto_descontinuidade_geometrica_p',
                'pto_descontinuidade_geometrica_a',
                'lim_area_desenv_controle_p',
                'lim_area_especial_p',
                'lim_descontinuidade_geometrica_p',
                'lim_terra_publica_p',
                'lim_unidade_conserv_nao_snuc_p',
                'lim_limite_area_especial_l',
                'lim_limite_intra_munic_adm_l',
                'lim_limite_operacional_l',
                'lim_limite_particular_l',
                'lim_limite_politico_adm_l',
                'lim_linha_de_limite_l',
                'lim_outros_limites_oficiais_l',
                'lim_area_desenv_controle_a',
                'lim_area_especial_a',
                'lim_area_particular_a',
                'lim_area_politico_adm_a',
                'lim_descontinuidade_geometrica_a',
                'lim_municipio_a',
                'lim_pais_a',
                'lim_terra_publica_a',
                'lim_unidade_federacao_a',
                'adm_descontinuidade_geometrica_p',
                'adm_descontinuidade_geometrica_a',
                'sau_descontinuidade_geometrica_p',
                'sau_descontinuidade_geometrica_a']

# Remover layers
for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.name() in LISTA:
        QgsMapLayerRegistry.instance().removeMapLayer( layer.id() )

# Remover grupos vazios
toc = iface.legendInterface()
relacao = toc.groupLayerRelationship()
groups = toc.groups()
indices = []
for grupo in relacao:
    index = groups.index(grupo[0])
    groups[index] = 'z'
    indices += [index]

cont = len(relacao)
for grupo in relacao[::-1]:
    cont -=1
    if len(grupo[1]) ==0:
        print grupo, cont, indices[cont]
        toc.removeGroup(indices[cont])

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>3 CGEO</b><br/>')
progress.setInfo('<b>Cap Leandro - Eng Cart</b><br/>')
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
time.sleep(3)