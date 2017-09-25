"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-06-07
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
# Verificar Ortografia
##03. Verificar Ortografia=name
##LF2) Revisao=group
##Arquivo_CSV=output file

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time

# Verificando nome do arquivo
if Arquivo_CSV[-4:] != '.csv':
    Arquivo_CSV += '.csv'

# Criar arquivo CSV
arquivo = open(Arquivo_CSV, 'w')
ArquivoX = Arquivo_CSV[:-3]+'indice'
Xfile = open(ArquivoX, 'w')
ArquivoBKP = Arquivo_CSV[:-3]+'bkp'
BKPfile = open(ArquivoBKP, 'w')

lista = ['adm_area_pub_civil_a',
            'adm_area_pub_militar_a',
            'adm_edif_pub_civil_a',
            'adm_edif_pub_civil_p',
            'adm_edif_pub_militar_a',
            'adm_edif_pub_militar_p',
            'adm_posto_fiscal_a',
            'adm_posto_fiscal_p',
            'adm_posto_pol_rod_a',
            'adm_posto_pol_rod_p',
            'asb_area_abast_agua_a',
            'asb_area_saneamento_a',
            'asb_cemiterio_a',
            'asb_cemiterio_p',
            'asb_dep_abast_agua_a',
            'asb_dep_abast_agua_p',
            'asb_dep_saneamento_a',
            'asb_dep_saneamento_p',
            'asb_edif_abast_agua_a',
            'asb_edif_abast_agua_p',
            'asb_edif_saneamento_a',
            'asb_edif_saneamento_p',
            'eco_area_agrop_ext_veg_pesca_a',
            'eco_area_comerc_serv_a',
            'eco_area_ext_mineral_a',
            'eco_area_industrial_a',
            'eco_deposito_geral_a',
            'eco_deposito_geral_p',
            'eco_edif_agrop_ext_veg_pesca_a',
            'eco_edif_agrop_ext_veg_pesca_p',
            'eco_edif_comerc_serv_a',
            'eco_edif_comerc_serv_p',
            'eco_edif_ext_mineral_a',
            'eco_edif_ext_mineral_p',
            'eco_edif_industrial_a',
            'eco_edif_industrial_p',
            'eco_ext_mineral_a',
            'eco_ext_mineral_p',
            'eco_plataforma_a',
            'eco_plataforma_p',
            'edu_area_ensino_a',
            'edu_area_lazer_a',
            'edu_area_religiosa_a',
            'edu_area_ruinas_a',
            'edu_arquibancada_a',
            'edu_arquibancada_p',
            'edu_campo_quadra_a',
            'edu_campo_quadra_p',
            'edu_coreto_tribuna_a',
            'edu_coreto_tribuna_p',
            'edu_edif_const_lazer_a',
            'edu_edif_const_lazer_p',
            'edu_edif_const_turistica_a',
            'edu_edif_const_turistica_p',
            'edu_edif_ensino_a',
            'edu_edif_ensino_p',
            'edu_edif_religiosa_a',
            'edu_edif_religiosa_p',
            'edu_piscina_a',
            'edu_pista_competicao_l',
            'edu_ruina_a',
            'edu_ruina_p',
            'enc_antena_comunic_p',
            'enc_area_comunicacao_a',
            'enc_area_energia_eletrica_a',
            'enc_edif_comunic_a',
            'enc_edif_comunic_p',
            'enc_edif_energia_a',
            'enc_edif_energia_p',
            'enc_est_gerad_energia_eletr_a',
            'enc_est_gerad_energia_eletr_l',
            'enc_est_gerad_energia_eletr_p',
            'enc_grupo_transformadores_a',
            'enc_grupo_transformadores_p',
            'enc_hidreletrica_a',
            'enc_hidreletrica_l',
            'enc_hidreletrica_p',
            'enc_termeletrica_a',
            'enc_termeletrica_p',
            'hid_area_umida_a',
            'hid_banco_areia_a',
            'hid_banco_areia_l',
            'hid_barragem_a',
            'hid_barragem_l',
            'hid_barragem_p',
            'hid_comporta_l',
            'hid_comporta_p',
            'hid_corredeira_a',
            'hid_corredeira_l',
            'hid_corredeira_p',
            'hid_descontinuidade_geometrica_l',
            'hid_fonte_dagua_p',
            'hid_foz_maritima_a',
            'hid_foz_maritima_l',
            'hid_foz_maritima_p',
            'hid_ilha_a',
            'hid_ilha_l',
            'hid_ilha_p',
            'hid_massa_dagua_a',
            'hid_quebramar_molhe_a',
            'hid_quebramar_molhe_l',
            'hid_queda_dagua_a',
            'hid_queda_dagua_l',
            'hid_queda_dagua_p',
            'hid_recife_a',
            'hid_recife_l',
            'hid_recife_p',
            'hid_rocha_em_agua_a',
            'hid_rocha_em_agua_p',
            'hid_sumidouro_vertedouro_p',
            'hid_terreno_suj_inundacao_a',
            'hid_trecho_drenagem_l',
            'hid_trecho_massa_dagua_a',
            'lim_area_de_litigio_a',
            'lim_area_uso_comunitario_a',
            'lim_area_uso_comunitario_p',
            'lim_bairro_a',
            'lim_delimitacao_fisica_l',
            'lim_distrito_a',
            'lim_marco_de_limite_p',
            'lim_outras_unid_protegidas_a',
            'lim_outras_unid_protegidas_p',
            'lim_regiao_administrativa_a',
            'lim_sub_distrito_a',
            'lim_terra_indigena_a',
            'lim_terra_indigena_p',
            'lim_unidade_conserv_nao_snuc_a',
            'lim_unidade_protecao_integral_a',
            'lim_unidade_protecao_integral_p',
            'lim_unidade_uso_sustentavel_a',
            'lim_unidade_uso_sustentavel_p',
            'loc_aglom_rural_de_ext_urbana_p',
            'loc_aglomerado_rural_isolado_p',
            'loc_area_edificada_a',
            'loc_area_habitacional_a',
            'loc_area_urbana_isolada_a',
            'loc_capital_p',
            'loc_cidade_p',
            'loc_edif_habitacional_a',
            'loc_edif_habitacional_p',
            'loc_edificacao_a',
            'loc_edificacao_p',
            'loc_hab_indigena_a',
            'loc_hab_indigena_p',
            'loc_nome_local_p',
            'loc_vila_p',
            'pto_area_est_med_fenom_a',
            'pto_edif_constr_est_med_fen_a',
            'pto_edif_constr_est_med_fen_p',
            'pto_pto_est_med_fenomenos_p',
            'pto_pto_ref_geod_topo_p',
            'rel_alter_fisiog_antropica_a',
            'rel_alter_fisiog_antropica_l',
            'rel_curva_nivel_l',
            'rel_dolina_a',
            'rel_dolina_p',
            'rel_duna_a',
            'rel_duna_p',
            'rel_elemento_fisiog_natural_a',
            'rel_elemento_fisiog_natural_l',
            'rel_elemento_fisiog_natural_p',
            'rel_gruta_caverna_p',
            'rel_pico_p',
            'rel_ponto_cotado_altimetrico_p',
            'rel_rocha_a',
            'rel_rocha_p',
            'rel_terreno_exposto_a',
            'sau_area_saude_a',
            'sau_area_servico_social_a',
            'sau_edif_saude_a',
            'sau_edif_saude_p',
            'sau_edif_servico_social_a',
            'sau_edif_servico_social_p',
            'tra_area_estrut_transporte_a',
            'tra_arruamento_l',
            'tra_atracadouro_a',
            'tra_atracadouro_l',
            'tra_atracadouro_p',
            'tra_caminho_aereo_l',
            'tra_condutor_hidrico_l',
            'tra_eclusa_a',
            'tra_eclusa_l',
            'tra_eclusa_p',
            'tra_edif_constr_aeroportuaria_a',
            'tra_edif_constr_aeroportuaria_p',
            'tra_edif_constr_portuaria_a',
            'tra_edif_constr_portuaria_p',
            'tra_edif_metro_ferroviaria_a',
            'tra_edif_metro_ferroviaria_p',
            'tra_edif_rodoviaria_a',
            'tra_edif_rodoviaria_p',
            'tra_fundeadouro_a',
            'tra_fundeadouro_l',
            'tra_fundeadouro_p',
            'tra_funicular_l',
            'tra_funicular_p',
            'tra_galeria_bueiro_l',
            'tra_galeria_bueiro_p',
            'tra_girador_ferroviario_p',
            'tra_identific_trecho_rod_p',
            'tra_obstaculo_navegacao_a',
            'tra_obstaculo_navegacao_l',
            'tra_obstaculo_navegacao_p',
            'tra_passag_elevada_viaduto_l',
            'tra_passag_elevada_viaduto_p',
            'tra_passagem_nivel_p',
            'tra_patio_a',
            'tra_patio_p',
            'tra_pista_ponto_pouso_a',
            'tra_pista_ponto_pouso_l',
            'tra_pista_ponto_pouso_p',
            'tra_ponte_l',
            'tra_ponte_p',
            'tra_posto_combustivel_a',
            'tra_posto_combustivel_p',
            'tra_sinalizacao_p',
            'tra_travessia_l',
            'tra_travessia_p',
            'tra_travessia_pedestre_l',
            'tra_travessia_pedestre_p',
            'tra_trecho_duto_l',
            'tra_trecho_ferroviario_l',
            'tra_trecho_hidroviario_l',
            'tra_trecho_rodoviario_l',
            'tra_trilha_picada_l',
            'tra_tunel_l',
            'tra_tunel_p',
            'veg_brejo_pantano_a',
            'veg_caatinga_a',
            'veg_campinarana_a',
            'veg_campo_a',
            'veg_cerrado_cerradao_a',
            'veg_estepe_a',
            'veg_floresta_a',
            'veg_macega_chavascal_a',
            'veg_mangue_a',
            'veg_veg_cultivada_a',
            'veg_veg_restinga_a']

for layer in QgsMapLayerRegistry.instance().mapLayers().values():
    if layer.type() == 0 and layer.name() in lista:
        classe = layer.name()
        header = layer.pendingFields()
        # Verificar quais campos sao do tipo texto em cada classe
        campo_texto = []
        for k, campo in enumerate(header):
            if campo.type() == 10 and campo.name() != 'uuid' and campo.name()[:3] != 'id_' and campo.name() != 'id':
                nome = campo.name()
                campo_texto += [(k, nome)]
        # Na camada extrair os textos e ids que nao sao nulos
        if len(campo_texto)>0:
            texto =[]
            ID = []
            for feat in layer.getFeatures():
                att = feat.attributes()
                # Atributos do tipo texto
                att_text = []
                for h in campo_texto:
                    att_text += [att[h[0]]]
                ID +=[feat. id()]
                texto +=[att_text]
            
            # Pegando os textos
            nlin = len(texto)
            ncol = len(texto[0])
            campos = []
            textos = []
            sentinela = False
            for col in range(ncol):
                campos += [campo_texto[col][1]]
                text_id = u''
                text_att = u''
                for lin in range(nlin):
                    atributo = texto[lin][col]
                    if not (atributo == None or atributo =='' or atributo ==' '):
                        atributo= atributo.replace(';', ',')
                        text_id += str(ID[lin])+u';'
                        text_att += atributo+u';'
                        sentinela = True
                textos += [(text_id, text_att)]
            # Salvar no CSV
            if sentinela:
                Xfile.write('Classe:;%s\n' %classe)
                for  ind, camp in enumerate(campos):
                    if textos[ind][0] != '':
                        Xfile.write('Campo:;%s\n' %camp)
                        Xfile.write(u'ID:;%s\n' %textos[ind][0][:-1])
                        Atributo = classe + '\\' + camp
                        arquivo.write((u'%s:;%s\n' %(Atributo, textos[ind][1][:-1])).encode('utf-8'))
                        BKPfile.write((u'Atributo:;%s\n' %textos[ind][1][:-1]).encode('utf-8'))

arquivo.close()
Xfile.close()
BKPfile.close()

progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)