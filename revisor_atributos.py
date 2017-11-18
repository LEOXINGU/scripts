"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-07-18
        copyright            : (C) 2017 by Leandro Franca - Cartographic Engineer
        email                : geoleandro.franca@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation.                             *
 *                                                                         *
 ***************************************************************************/
"""
# Revisor de atributos
##02. Revisor de atributos=name
##LF2) Revisao=group
##Shapefile_de_Ganchos=output vector
##Forcar_Atributos=boolean False

path_name = Shapefile_de_Ganchos
SimNao = Forcar_Atributos

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time

# Criar campos
fields = QgsFields()
fields.append(QgsField('classe', QVariant.String))
fields.append(QgsField('ID', QVariant.Int))
fields.append(QgsField('atributo', QVariant.String))
fields.append(QgsField('problema', QVariant.String))

# Pegando o SRC da camada trecho de drenagem
layerList = QgsMapLayerRegistry.instance().mapLayersByName('hid_trecho_drenagem_l')
if layerList:
 layer = layerList[0]
 SRC = layer.crs()
 
# Criar shapefile de ganchos
encoding = u'utf-8'
formato = 'ESRI Shapefile'
writer = QgsVectorFileWriter(path_name, encoding, fields, QGis.WKBPoint, SRC, formato)
feature = QgsFeature(fields)


dominios = {'antropizada': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'caracteristicafloresta': {3: 'Bosque', 1: 'Floresta', 2: 'Mata', 0: 'Desconhecido'},
 'bitola': {1: 'M\xc3\xa9trica', 3: 'Larga', 6: 'Mista Internacional Larga', 0: 'Desconhecido', 2: 'Internacional', 4: 'Mista M\xc3\xa9trica Internacional', 5: 'Mista M\xc3\xa9trica Larga'},
 'classificacao': {0: 'Desconhecido', 9: 'Internacional', 10: 'Dom\xc3\xa9stico'},
 'canteirodivisorio': {1: 'Sim', 2: 'N\xc3\xa3o'},
 'classificsigiloso': {0: 'Desconhecido', 2: 'Ostensivo', 1: 'Sigiloso'},
 'coincidecomdentrode_hid': {10: 'Represa/a\xc3\xa7ude', 14: 'Eclusa', 2: 'Canal', 9: 'Laguna', 11: 'Vala', 19: 'Barragem', 15: 'Terreno sujeito a inunda\xc3\xa7\xc3\xa3o', 1: 'Rio', 97: 'N\xc3\xa3o aplic\xc3\xa1vel', 12: 'Queda d\xc2\xb4\xc3\xa1gua', 13: 'Corredeira', 16: 'Foz mar\xc3\xadtima'},
 'administracao': {15: 'Privada', 12: 'Federal/Estadual/Municipal', 3: 'Municipal', 11: 'Estadual/Municipal', 5: 'Distrital', 2: 'Estadual', 98: 'Mista', 6: 'Particular', 10: 'Federal/Municipal', 4: 'Estadual/Municipal', 1: 'Federal', 0: 'Desconhecida', 7: 'Concessionada', 97: 'N\xc3\xa3o aplic\xc3\xa1vel', 9: 'Federal/Estadual'},
 'causa': {3: 'Absor\xc3\xa7\xc3\xa3o', 1: 'Canaliza\xc3\xa7\xc3\xa3o', 0: 'Desconhecida', 2: 'Gruta ou Fenda'},
 'coincidecomdentrode_lim': {96: 'N\xc3\xa3o Identificado', 4: 'Linha Seca', 3: 'Cumeada', 6: 'Rodovia', 9: 'Massa D`\xc3\x81gua', 5: 'Costa Vis\xc3\xadvel da Carta', 7: 'Ferrovia', 2: 'Contorno Massa D`\xc3\x81gua', 8: 'Trecho de Drenagem'},
 'causaexposicao': {0: 'Desconhecido', 4: 'Natural', 5: 'Artificial'},
 'atividade': {0: 'Desconhecido', 10: 'Produ\xc3\xa7\xc3\xa3o', 9: 'Prospec\xc3\xa7\xc3\xa3o'},
 'dentrodepoligono': {1: 'Sim', 2: 'N\xc3\xa3o'},
 'compartilhado': {1: 'Sim', 2: 'N\xc3\xa3o'},
 'eletrificada': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'denso': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'cultivopredominante': {26: 'Bracatinga', 96: 'N\xc3\xa3o identificado', 42: 'Videira', 33: 'Cebola', 13: 'Arroz', 4: 'Trigo', 32: 'Juta', 15: 'Cacau', 6: 'Algod\xc3\xa3o herb\xc3\xa1ceo', 18: 'A\xc3\xa7a\xc3\xad', 27: 'Arauc\xc3\xa1ria', 22: 'Algaroba', 30: 'Ma\xc3\xa7\xc3\xa3', 10: 'Batata inglesa', 25: 'Hortali\xc3\xa7as', 12: 'Feij\xc3\xa3o', 23: 'Pinus', 31: 'P\xc3\xaassego', 2: 'Banana', 17: 'Palmeira', 24: 'Pastagem cultivada', 20: 'Eucalipto', 3: 'Laranja', 16: 'Erva-mate', 99: 'Outros', 1: 'Milho', 21: 'Ac\xc3\xa1cia', 28: 'Carnauba', 29: 'Pera', 19: 'Seringueira', 98: 'Misto', 7: 'Cana-de-A\xc3\xa7\xc3\xbacar', 9: 'Soja', 14: 'Caf\xc3\xa9', 8: 'Fumo', 11: 'Mandioca'},
 'construcao': {97: 'N\xc3\xa3o aplic\xc3\xa1vel', 2: 'Aberta', 1: 'Fechada'},
 'eixoprincipal': {1: 'Sim', 2: 'N\xc3\xa3o'},
 'cotacomprovada': {1: 'Sim', 2: 'N\xc3\xa3o'},
 'destenergelet': {0: 'Desconhecido', 3: 'Comercializa\xc3\xa7\xc3\xa3o de Energia COM)', 1: 'Auto-Produ\xc3\xa7\xc3\xa3o de Energia APE)', 4: 'Produ\xc3\xa7\xc3\xa3o Independente de Energia PIE)', 5: 'Servi\xc3\xa7o P\xc3\xbablico SP)', 2: 'Auto-Produ\xc3\xa7\xc3\xa3o com Comercializa\xc3\xa7\xc3\xa3o de Excedente APE-COM)'},
 'destinacaofundeadouro': {0: 'Desconhecido', 99: 'Outros', 12: '\xc3\x81reas de fundeio com limite definido', 11: 'Fundeadouro com designa\xc3\xa7\xc3\xa3o alfanum\xc3\xa9rica', 13: '\xc3\x81reas de fundeio proibido', 10: 'Fundeadouro recomendado sem limite definido'},
 'combrenovavel': {1: 'Sim', 2: 'N\xc3\xa3o'},
 'coletiva': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'destinadoa': {40: 'Palmito', 99: 'Outros', 38: 'Coco', 39: 'Jaborandi', 37: 'Carna\xc3\xbaba', 18: 'A\xc3\xa7a\xc3\xad', 0: 'Desconhecido', 44: 'Pesca', 34: 'Turfa', 36: 'Castanha', 5: 'Madeira', 41: 'Baba\xc3\xa7u', 43: 'Pecu\xc3\xa1ria', 35: 'L\xc3\xa1tex'},
 'depressao': {1: 'Sim', 2: 'N\xc3\xa3o'},
 'emduto': {1: 'Sim', 2: 'N\xc3\xa3o'},
 'emarruamento': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'finalidade_veg': {2: 'Subist\xc3\xaancia', 0: 'Desconhecido', 3: 'Conserva\xc3\xa7\xc3\xa3o ambiental', 99: 'Outros', 1: 'Explora\xc3\xa7\xc3\xa3o econ\xc3\xb4mica'},
 'espessalgas': {1: 'Finas', 2: 'M\xc3\xa9dias', 3: 'Grossas'},
 'ensino': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'frigorifico': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'fixa': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'especie': {0: 'Desconhecido', 2: 'Transmiss\xc3\xa3o', 3: 'Distribui\xc3\xa7\xc3\xa3o'},
 'finalidade_eco': {0: 'Desconhecido', 98: 'Mista', 1: 'Comercial', 2: 'Servi\xc3\xa7o'},
 'funcaoedifmetroferrov': {99: 'Outros', 15: 'Administrativa', 20: 'Oficina de manuten\xc3\xa7\xc3\xa3o', 17: 'Esta\xc3\xa7\xc3\xa3o metrovi\xc3\xa1ria', 18: 'Terminal ferrovi\xc3\xa1rio de cargas', 0: 'Desconhecido', 16: 'Esta\xc3\xa7\xc3\xa3o ferrovi\xc3\xa1ria de passageiros', 19: 'Terminal ferrovi\xc3\xa1rio de passageiros e cargas'},
 'especiepredominante': {96: 'N\xc3\xa3o identificado', 10: 'Cip\xc3\xb3', 11: 'Bambu', 17: 'Palmeira', 27: 'Arauc\xc3\xa1ria', 98: 'Misto', 41: 'Baba\xc3\xa7u', 12: 'Sororoca'},
 'finalidade_asb': {8: 'Armazenamento', 0: 'Desconhecido', 2: 'Tratamento', 3: 'Recalque', 4: 'Distribui\xc3\xa7\xc3\xa3o'},
 'geracao': {0: 'Desconhecido', 1: 'Eletricidade - GER 0', 2: 'CoGera\xc3\xa7\xc3\xa3o'},
 'homologacao': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'formaextracao': {0: 'Desconhecida', 5: 'C\xc3\xa9u aberto', 6: 'Subterr\xc3\xa2neo'},
 'jurisdicao': {9: 'Federal/Estadual', 3: 'Municipal', 11: 'Estadual/Municipal', 12: 'Federal/Estadual/Municipal', 10: 'Federal/Municipal', 1: 'Federal', 0: 'Desconhecida', 2: 'Estadual', 6: 'Particular', 8: 'Propriedade particular'},
 'materializado': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'indice': {1: 'Mestra', 2: 'Normal', 3: 'Auxiliar'},
 'materialpredominante': {24: 'Saibro', 14: 'Lama', 21: 'Concha', 15: 'Argila', 0: 'Desconhecido', 20: 'Coral', 13: 'Areia Fina', 4: 'Rocha', 50: 'Pedra', 18: 'Cascalho', 16: 'Lodo', 19: 'Seixo', 12: 'Areia', 98: 'Misto', 97: 'N\xc3\xa3o Aplic\xc3\xa1vel'},
 'multimodal': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'nascente': {1: 'Sim', 2: 'N\xc3\xa3o'},
 'matconstr': {99: 'Outros', 1: 'Alvenaria', 26: 'Fio Met\xc3\xa1lico', 4: 'Rocha', 23: 'Terra', 0: 'Desconhecido', 3: 'Metal', 97: 'N\xc3\xa3o Aplic\xc3\xa1vel', 7: 'Tela ou Alambrado', 6: 'Arame', 5: 'Madeira', 8: 'Cerca viva', 25: 'Fibra \xc3\xb3tica', 2: 'Concreto'},
 'instituicao': {6: 'Aeron\xc3\xa1utica', 8: 'Corpo de bombeiros', 99: 'Outros', 5: 'Ex\xc3\xa9rcito', 4: 'Marinha', 7: 'Pol\xc3\xadcia militar', 0: 'Desconhecida'},
 'modalidade': {99: 'Outras', 2: 'Radiodifus\xc3\xa3o/som e imagem', 3: 'Telefonia', 0: 'Desconhecido', 5: 'Radiodifus\xc3\xa3o/som', 4: 'Dados', 1: 'Radiocomunica\xc3\xa7\xc3\xa3o'},
 'modaluso': {14: 'Portu\xc3\xa1rio', 9: 'Aeroportu\xc3\xa1rio', 5: 'Ferrovi\xc3\xa1rio', 98: 'Misto', 7: 'Dutos', 8: 'Rodoferrovi\xc3\xa1rio', 4: 'Rodovi\xc3\xa1rio', 6: 'Metrovi\xc3\xa1rio'},
 'mattransp': {29: 'Gasolina', 4: 'Nafta', 8: 'Efluentes', 3: 'Petr\xc3\xb3leo', 0: 'Desconhecido', 5: 'G\xc3\xa1s', 30: '\xc3\x81lcool', 31: 'Querosene', 99: 'Outros', 7: 'Min\xc3\xa9rio', 1: '\xc3\x81gua', 2: '\xc3\x93leo', 6: 'Gr\xc3\xa3os', 9: 'Esgoto'},
 'isolada': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'navegabilidade': {0: 'Desconhecida', 2: 'N\xc3\xa3o naveg\xc3\xa1vel', 1: 'Naveg\xc3\xa1vel'},
 'nivelatencao': {6: 'Secund\xc3\xa1rio', 7: 'Terci\xc3\xa1rio', 5: 'Prim\xc3\xa1rio'},
 'ocorrenciaem': {96: 'N\xc3\xa3o Identificado', 14: 'Macega ou chavascal', 7: 'Estepe', 5: 'Brejo ou P\xc3\xa2ntano', 13: 'Cerrado ou cerrad\xc3\xa3o', 8: 'Pastagem', 19: 'Campinarana', 6: 'Caatinga', 15: 'Floresta'},
 'posicaoreledific': {17: 'Adjacente a edifica\xc3\xa7\xc3\xa3o', 18: 'Sobre edifica\xc3\xa7\xc3\xa3o', 14: 'Isolado'},
 'poderpublico': {0: 'Desconhecido', 2: 'Legislativo', 1: 'Executivo', 3: 'Judici\xc3\xa1rio'},
 'regime': {0: 'Desconhecido', 1: 'Permanente', 6: 'Sazonal', 4: 'Tempor\xc3\xa1rio com leito permanente', 3: 'Tempor\xc3\xa1rio', 2: 'Permanente com grande varia\xc3\xa7\xc3\xa3o', 5: 'Seco'},
 'qualidagua': {0: 'Desconhecida', 4: 'Salobra', 2: 'N\xc3\xa3o pot\xc3\xa1vel', 1: 'Pot\xc3\xa1vel', 3: 'Mineral'},
 'ovgd': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'rede': {15: 'Privada', 2: 'Estadual', 0: 'Desconhecida', 3: 'Municipal', 14: 'Nacional'},
 'referencialgrav': {4: 'Local', 1: 'Postdam 1930', 2: 'IGSN71', 0: 'Desconhecido', 3: 'Absoluto', 97: 'N\xc3\xa3o Aplic\xc3\xa1vel'},
 'referencialaltim': {2: 'Imbituba', 4: 'Local', 5: 'Outra refer\xc3\xaancia', 1: 'Torres', 3: 'Santana'},
 'proximidade': {15: 'Adjacente', 16: 'Coincidente', 0: 'Desconhecida', 14: 'Isolado'},
 'nrlinhas': {1: 'Simples', 0: 'Desconhecido', 3: 'M\xc3\xbaltipla', 2: 'Dupla'},
 'posicaopista': {12: 'Adjacentes', 0: 'Desconhecida', 13: 'Superpostas', 97: 'N\xc3\xa3o Aplic\xc3\xa1vel'},
 'procextracao': {0: 'Desconhecido', 2: 'Manual', 1: 'Mecanizado'},
 'posicaorelativa': {5: 'Submerso', 3: 'Elevado', 2: 'Superf\xc3\xadcie', 0: 'Desconhecida', 4: 'Emerso', 6: 'Subterr\xc3\xa2neo'},
 'relacionado_hdr': {14: 'Eclusa', 12: 'Queda d\xc3\xa1gua', 19: 'Barragem', 22: 'Complexo portu\xc3\xa1rio', 24: 'Atracadouro', 21: 'Conflu\xc3\xaancia', 17: 'Interrup\xc3\xa7\xc3\xa3o com a Moldura', 13: 'Corredeira', 23: 'Entre trechos hidrovi\xc3\xa1rios', 16: 'Foz mar\xc3\xadtima'},
 'relacionado': {10: 'Edifica\xc3\xa7\xc3\xa3o Metro Ferrovi\xc3\xa1ria', 8: 'Entroncamento', 3: 'Ponte', 1: 'T\xc3\xbanel', 2: 'Passagem elevada ou viaduto', 7: 'Mudan\xc3\xa7a de atributo', 19: 'Barragem', 17: 'Interrup\xc3\xa7\xc3\xa3o com a Moldura', 5: 'Edifica\xc3\xa7\xc3\xa3o rodovi\xc3\xa1ria', 11: 'Localidade', 6: 'Galeria ou bueiro', 12: 'Patio', 13: 'Passagem de n\xc3\xadvel', 4: 'Travessia', 9: 'In\xc3\xadcio ou fim de trecho'},
 'relacionado_fer': {10: 'Edifica\xc3\xa7\xc3\xa3o Metro Ferrovi\xc3\xa1ria', 8: 'Entroncamento', 3: 'Ponte', 1: 'T\xc3\xbanel', 2: 'Passagem elevada ou viaduto', 7: 'Mudan\xc3\xa7a de atributo', 19: 'Barragem', 17: 'Interrup\xc3\xa7\xc3\xa3o com a Moldura', 5: 'Edifica\xc3\xa7\xc3\xa3o rodovi\xc3\xa1ria', 11: 'Localidade', 6: 'Galeria ou bueiro', 12: 'Patio', 13: 'Passagem de n\xc3\xadvel', 4: 'Travessia', 9: 'In\xc3\xadcio ou fim de trecho'},
 'setor': {0: 'Desconhecido', 1: 'Energ\xc3\xa9tico', 2: 'Econ\xc3\xb4mico', 4: 'Saneamento b\xc3\xa1sico', 3: 'Abastecimento de \xc3\xa1gua'},
 'situacaoespacial': {12: 'Adjacentes', 13: 'Superpostos', 99: 'Outros'},
 'situacaoemagua': {0: 'Desconhecido', 4: 'Emerso', 7: 'Cobre e Descobre', 5: 'Submerso'},
 'revestimento': {0: 'Desconhecido', 4: 'Cal\xc3\xa7ado', 1: 'Leito natural', 2: 'Revestimento prim\xc3\xa1rio', 3: 'Pavimentado'},
 'sistemageodesico': {5: 'Astro Chu\xc3\xa1', 2: 'SIRGAS', 4: 'C\xc3\xb3rrego Alegre', 3: 'WGS-84', 1: 'SAD-69', 6: 'Outra refer\xc3\xaancia'},
 'sigla': {16: 'PR', 4: 'AM', 1: 'AC', 24: 'SC', 10: 'MA', 27: 'TO', 23: 'RR', 20: 'RN', 7: 'DF', 22: 'RO', 21: 'RS', 17: 'PE', 8: 'ES', 19: 'RJ', 26: 'SE', 3: 'AP', 18: 'PI', 0: 'Desconhecido', 15: 'PB', 13: 'MG', 9: 'GO', 5: 'BA', 25: 'SP', 14: 'PA', 6: 'CE', 11: 'MT', 2: 'AL', 12: 'MS'},
 'salinidade': {1: 'Doce', 0: 'Desconhecida', 2: 'Salgada'},
 'situacaocosta': {11: 'Afastado', 10: 'Cont\xc3\xadguo'},
 'relacionado_hid': {2: 'Barragem', 13: 'Entre trechos de drenagem', 4: 'Queda d\xe2\x80\x99\xc3\xa1gua', 15: 'Conflu\xc3\xaancia', 5: 'Corredeira', 7: 'Sumidouro', 14: 'Ponto in\xc3\xadcio de drenagem', 3: 'Comporta', 19: 'Ramifica\xc3\xa7\xc3\xa3o', 9: 'Lago / Lagoa', 6: 'Foz mar\xc3\xadtima', 17: 'Interrup\xc3\xa7\xc3\xa3o \xc3\xa0 Jusante', 11: 'Laguna', 16: 'Vertedouro', 8: 'Meandro abandonado', 12: 'Represa/ a\xc3\xa7ude', 1: 'Eclusa', 18: 'Interrup\xc3\xa7\xc3\xa3o \xc3\xa0 Montante'},
 'relacionado_dut': {5: 'Ponto de ramifica\xc3\xa7\xc3\xa3o', 4: 'Dep\xc3\xb3sito geral', 3: 'Local cr\xc3\xadtico', 1: 'Ponto inicial', 17: 'Interrup\xc3\xa7\xc3\xa3o com a Moldura', 2: 'Ponto final'},
 'residuo': {0: 'Desconhecido', 1: 'L\xc3\xadquido', 2: 'S\xc3\xb3lido'},
 'relacionado_rod': {10: 'Edifica\xc3\xa7\xc3\xa3o Metro Ferrovi\xc3\xa1ria', 8: 'Entroncamento', 3: 'Ponte', 1: 'T\xc3\xbanel', 2: 'Passagem elevada ou viaduto', 7: 'Mudan\xc3\xa7a de atributo', 19: 'Barragem', 17: 'Interrup\xc3\xa7\xc3\xa3o com a Moldura', 5: 'Edifica\xc3\xa7\xc3\xa3o rodovi\xc3\xa1ria', 11: 'Localidade', 6: 'Galeria ou bueiro', 12: 'Patio', 13: 'Passagem de n\xc3\xadvel', 4: 'Travessia', 9: 'In\xc3\xadcio ou fim de trecho'},
 'tipocampo': {0: 'Desconhecido', 1: 'Sujo', 2: 'Limpo'},
 'tipoalterantrop': {0: 'Desconhecido', 27: 'Aterro', 28: 'Res\xc3\xadduo de bota-fora', 25: '\xc3\x81rea aterrada', 26: 'Corte', 29: 'Res\xc3\xadduo s\xc3\xb3lido em geral', 24: 'Caixa de empr\xc3\xa9stimo'},
 'tipoaglomrurisol': {7: 'Outros Aglomerados Rurais Isolados', 5: 'Aglomerado Rural Isolado - Povoado', 6: 'Aglomerado Rural Isolado - N\xc3\xbacleo'},
 'tipoassociado': {4: 'Vila', 1: 'Cidade'},
 'tipocaminhoaereo': {12: 'Telef\xc3\xa9rico', 99: 'Outros'},
 'situacaojuridica': {1: 'Delimitada', 0: 'Desconhecida', 4: 'Regularizada', 3: 'Homologada ou demarcada', 2: 'Declarada'},
 'tipoareausocomun': {1: 'Quilombo', 2: 'Assentamento rural'},
 'situacaomarco': {5: 'N\xc3\xa3o encontrado', 2: 'Destru\xc3\xaddo', 6: 'N\xc3\xa3o visitado', 3: 'Destru\xc3\xaddo sem chapa', 0: 'Desconhecido', 7: 'N\xc3\xa3o constru\xc3\xaddo', 4: 'Destru\xc3\xaddo com chapa danificada', 1: 'Bom'},
 'tipoatracad': {43: 'Dolfim', 41: 'Molhe de atraca\xc3\xa7\xc3\xa3o', 40: 'Trapiche', 0: 'Desconhecido', 42: 'Pier', 44: 'Desembarcadouro', 39: 'Cais flutuante', 38: 'Cais'},
 'situamare': {8: 'Sempre fora d\xc2\xb4\xc3\xa1gua', 9: 'Sempre submerso', 7: 'Cobre e descobre', 0: 'Desconhecido'},
 'terreno': {1: 'Seco', 2: 'Irrigado', 3: 'Inundado'},
 'tipobrejopantano': {0: 'Desconhecido', 1: 'Brejo', 2: 'P\xc3\xa2ntano'},
 'tipobanco': {2: 'Mar\xc3\xadtimo', 1: 'Fluvial', 3: 'Lacustre', 4: 'Cord\xc3\xa3o Arenoso'},
 'tipoareaumida': {0: 'Desconhecido', 4: 'Arenoso', 3: 'Lamacento'},
 'tipocerr': {0: 'Desconhecido', 2: 'Cerrad\xc3\xa3o', 1: 'Cerrado'},
 'tipocondutor': {0: 'Desconhecido', 4: 'Tubula\xc3\xa7\xc3\xa3o', 2: 'Calha'},
 'tipocomplexolazer': {13: 'Camping', 6: 'Parque aqu\xc3\xa1tico', 7: 'Parque tem\xc3\xa1tico', 14: 'Complexo desportivo', 4: 'Parque de divers\xc3\xb5es', 12: 'Parque de eventos culturais', 9: 'H\xc3\xadpica', 11: 'Campo de golfe', 8: 'Hip\xc3\xb3dromo', 0: 'Desconhecido', 1: 'Complexo recreativo', 3: 'Aut\xc3\xb3dromo', 16: 'Jardim bot\xc3\xa2nico', 5: 'Parque urbano', 15: 'Zool\xc3\xb3gico', 10: 'Estande de tiro', 2: 'Clube'},
 'tipoclassecnae': {35: '91.91-0', 16: '80.13-6', 32: '85.31-6', 21: '80.32-2', 28: '85.13-8', 7: '75.12-4', 8: '75.13-2', 19: '80.20-9', 3: '40.14-2', 13: '75.24-8', 18: '80.15-2', 17: '80.14-4', 10: '75.21-3', 12: '75.23-0', 27: '85.12-0', 34: '90.00-0', 97: 'N\xc3\xa3o Aplic\xc3\xa1vel', 30: '85.16-2', 24: '80.97-7', 11: '75.22-1', 9: '75.14-0', 6: '75.11-6', 15: '75.30-2', 0: 'Desconhecido', 5: '64.20-3', 26: '85.11-1', 14: '75.25-6', 25: '80.99-3', 99: 'Outros', 33: '85.32-4', 4: '41.00-9', 98: 'Misto', 1: '40.11-8', 20: '80.31-4', 2: '40.12-6', 23: '80.96-9', 22: '80.33-0', 31: '85.20-0', 29: '85.14-6'},
 'tipocombustivel': {0: 'Desconhecido', 5: 'G\xc3\xa1s', 99: 'Outros', 3: 'Diesel', 33: 'Carv\xc3\xa3o', 1: 'Nuclear', 98: 'Misto'},
 'tipocomplexoportuario': {31: 'Instala\xc3\xa7\xc3\xa3o portu\xc3\xa1ria', 0: 'Desconhecido', 30: 'Porto organizado'},
 'tipocomplexoaero': {25: 'Heliporto', 24: 'Aeroporto', 23: 'Aer\xc3\xb3dromo'},
 'tipoconteudo': {0: 'Desconhecido', 3: 'Res\xc3\xadduo', 1: 'Insumo', 2: 'Produto'},
 'tipocapital': {2: 'Capital Federal', 3: 'Capital Estadual'},
 'tipodepsaneam': {0: 'Desconhecido', 99: 'Outros', 1: 'Tanque', 5: 'Aterro sanit\xc3\xa1rio', 6: 'Aterro controlado', 4: 'Dep\xc3\xb3sito de lixo'},
 'tipodepgeral': {9: 'Silo', 11: 'Dep\xc3\xb3sito frigor\xc3\xadfico', 99: 'Outros', 32: 'Armaz\xc3\xa9m', 19: 'Reservat\xc3\xb3rio de Combust\xc3\xadvel', 8: 'Galp\xc3\xa3o', 0: 'Desconhecido', 10: 'Composteira'},
 'tipocampoquadra': {1: 'Futebol', 4: 'P\xc3\xb3lo', 99: 'Outros', 7: 'T\xc3\xaanis', 3: 'V\xc3\xb4lei', 6: 'Poliesportiva', 0: 'Desconhecido', 2: 'Basquete', 5: 'Hipismo'},
 'tipodepabast': {0: 'Desconhecido', 3: 'Cisterna', 1: 'Tanque', 99: 'Outros', 2: 'Caixa d`\xc3\xa1gua'},
 'tipodelimfis': {0: 'Desconhecido', 2: 'Muro', 1: 'Cerca'},
 'tipoedifaero': {0: 'Desconhecido', 99: 'Outros', 29: 'Hangar', 27: 'Terminal de cargas', 28: 'Torre de controle', 15: 'Administrativa', 26: 'Terminal de passageiros'},
 'tipoedifagropec': {99: 'Outros', 14: 'Api\xc3\xa1rio', 0: 'Desconhecido', 18: 'Curral', 12: 'Sede operacional de fazenda', 17: 'Pocilga', 13: 'Avi\xc3\xa1rio', 15: 'Viveiro de plantas', 16: 'Viveiro para acquicultura'},
 'tipodivisaocnae': {92: 'Atividades Recreativas Culturais e Desportivas', 21: 'Fabrica\xc3\xa7\xc3\xa3o de Celulose Papel e Produtos de Papel', 45: 'Constru\xc3\xa7\xc3\xa3o', 19: 'Prepara\xc3\xa7\xc3\xa3o de couros e Fabrica\xc3\xa7\xc3\xa3o de Artefatos de Couro Artigos de Viagem e Cal\xc3\xa7ados', 30: 'Fabrica\xc3\xa7\xc3\xa3o de M\xc3\xa1quinas de Escrit\xc3\xb3rio e Equipamentos de Inform\xc3\xa1tica', 32: 'Fabrica\xc3\xa7\xc3\xa3o de Material Eletr\xc3\xb4nicode Aparelhos e Equipamentos de Comunica\xc3\xa7\xc3\xb5es', 36: 'Fabrica\xc3\xa7\xc3\xa3o de M\xc3\xb3veis e Industrias Diversas', 24: 'Fabrica\xc3\xa7\xc3\xa3o de Produtos Qu\xc3\xadmicos', 33: 'Fabrica\xc3\xa7\xc3\xa3o de Equipamentos de Instrumenta\xc3\xa7\xc3\xa3o M\xc3\xa9dico-Hospitalares Instumentos de Precis\xc3\xa3o e \xc3\x93pticos Equipamentos para Automa\xc3\xa7\xc3\xa3o Industrial Cron\xc3\xb4metros e Rel\xc3\xb3gios', 52: 'Com\xc3\xa9rcio Varejista e Repara\xc3\xa7\xc3\xa3o de Objetos Pessoais e Dom\xc3\xa9sticos.', 14: 'Extra\xc3\xa7\xc3\xa3o de Minerais N\xc3\xa3o-Met\xc3\xa1licos', 1: 'Agricultura Pecu\xc3\xa1ria e Servi\xc3\xa7os Relacionados', 26: 'Fabrica\xc3\xa7\xc3\xa3o de Produtos de Minerais N\xc3\xa3o-Met\xc3\xa1licos', 31: 'Fabrica\xc3\xa7\xc3\xa3o de M\xc3\xa1quinas Aparelhos e Materiais El\xc3\xa9tricos', 28: 'Fabrica\xc3\xa7\xc3\xa3o de Produtos de Metal Exclusive M\xc3\xa1quinas e Equipamentos', 22: 'Edi\xc3\xa7\xc3\xa3o Impress\xc3\xa3o e Reprodu\xc3\xa7\xc3\xa3o de Grava\xc3\xa7\xc3\xb5es', 27: 'Metalurgia B\xc3\xa1sica', 55: 'Alojamento e Alimenta\xc3\xa7\xc3\xa3o', 50: 'Com\xc3\xa9rcio e Repara\xc3\xa7\xc3\xa3o de Ve\xc3\xadculos Automotores e Motocicletas e Com\xc3\xa9rcio a Varejo de Combust\xc3\xadveis.', 16: 'Fabrica\xc3\xa7\xc3\xa3o de Produtos do Fumo', 23: 'Fabrica\xc3\xa7\xc3\xa3o de Coque Refino de Petr\xc3\xb3leo Elabora\xc3\xa7\xc3\xa3o de Combust\xc3\xadveis Nucleares e Produ\xc3\xa7\xc3\xa3o de \xc3\x81lcool', 11: 'Extra\xc3\xa7\xc3\xa3o de Petr\xc3\xb3leo e Servi\xc3\xa7os Relacionados', 20: 'Fabrica\xc3\xa7\xc3\xa3o de produtos de Madeira e Celulose', 37: 'Reciclagem', 5: 'Pesca Aquicultura e Servi\xc3\xa7os Relacionados', 35: 'Fabrica\xc3\xa7\xc3\xa3o de Outros Equipamentos de Transporte', 15: 'Fabrica\xc3\xa7\xc3\xa3o Aliment\xc3\xadcia e Bebidas', 51: 'Com\xc3\xa9rcio por Atacado e Representantes Comerciais. E agentes do com\xc3\xa9rcio', 74: 'Servi\xc3\xa7os Prestados Principalmente \xc3\xa0s Empresas organiza\xc3\xa7\xc3\xb5es).', 99: 'Outros', 0: 'Desconhecido', 13: 'Extra\xc3\xa7\xc3\xa3o de Minerais Met\xc3\xa1licos', 17: 'Fabrica\xc3\xa7\xc3\xa3o de Produtos T\xc3\xaaxteis', 25: 'Fabrica\xc3\xa7\xc3\xa3o de Artigos de Borracha e Material Pl\xc3\xa1stico', 34: 'Fabrica\xc3\xa7\xc3\xa3o e Montagem de Ve\xc3\xadculos Automotores Reboques e Carrocerias', 29: 'Fabrica\xc3\xa7\xc3\xa3o de M\xc3\xa1quinas e Equipamentos', 18: 'Confec\xc3\xa7\xc3\xa3o de Artigos do Vestu\xc3\xa1rio e Acess\xc3\xb3rios', 10: 'Extra\xc3\xa7\xc3\xa3o de Carv\xc3\xa3o Mineral', 2: 'Silvicultura Explora\xc3\xa7\xc3\xa3o Florestal e Servi\xc3\xa7os Relacionados'},
 'tipoedifabast': {0: 'Desconhecido', 2: 'Tratamento', 99: 'Outros', 1: 'Capta\xc3\xa7\xc3\xa3o', 3: 'Recalque', 98: 'Misto'},
 'tipoedifcomercserv': {8: 'Restaurante', 99: 'Outros', 6: 'Feira', 5: 'Centro de conven\xc3\xa7\xc3\xb5es', 3: 'Centro comercial', 4: 'Mercado', 0: 'Desconhecido', 7: 'Hotel/motel/pousada'},
 'tipoedifcomunic': {1: 'Centro de opera\xc3\xa7\xc3\xb5es', 0: 'Desconhecido', 4: 'Esta\xc3\xa7\xc3\xa3o repetidora', 2: 'Central comuta\xc3\xa7\xc3\xa3o e transmiss\xc3\xa3o', 3: 'Esta\xc3\xa7\xc3\xa3o radio-base'},
 'tipoedifenergia': {0: 'Desconhecido', 3: 'Seguran\xc3\xa7a', 99: 'Outros', 1: 'Administra\xc3\xa7\xc3\xa3o', 2: 'Oficinas', 4: 'Dep\xc3\xb3sito', 5: 'Chamin\xc3\xa9'},
 'tipoediflazer': {99: 'Outros', 1: 'Est\xc3\xa1dio', 7: 'Centro cultural', 8: 'Plataforma de pesca', 2: 'Gin\xc3\xa1sio', 0: 'Desconhecido', 4: 'Teatro', 5: 'Anfiteatro', 6: 'Cinema', 3: 'Museu'},
 'tipoedifmil': {14: 'Campo de tiro', 99: 'Outros', 19: 'Posto', 15: 'Base a\xc3\xa9rea', 12: 'Aquartelamento', 0: 'Desconhecido', 18: 'Delegacia servi\xc3\xa7o militar', 16: 'Distrito naval', 13: 'Campo de instru\xc3\xa7\xc3\xa3o', 17: 'Hotel de tr\xc3\xa2nsito'},
 'tipoedifport': {34: 'Dique de estaleiro', 99: 'Outros', 32: 'Armaz\xc3\xa9m', 0: 'Desconhecido', 37: 'Terminal privativo', 15: 'Administrativa', 36: 'Carreira', 27: 'Terminal de cargas', 35: 'Rampa', 33: 'Estaleiro', 26: 'Terminal de passageiros'},
 'tipoedifrelig': {4: 'Mosteiro', 5: 'Convento', 1: 'Igreja', 6: 'Mesquita', 2: 'Templo', 0: 'Desconhecido', 3: 'Centro', 99: 'Outros', 7: 'Sinagoga'},
 'tipoedifrod': {13: 'Posto de ped\xc3\xa1gio', 99: 'Outros', 10: 'Parada interestadual', 9: 'Terminal urbano', 14: 'Posto de fiscaliza\xc3\xa7\xc3\xa3o', 15: 'Administrativa', 8: 'Terminal interestadual', 0: 'Desconhecido', 12: 'Posto de pesagem'},
 'tipoedifsaneam': {5: 'Tratamento de esgoto', 99: 'Outros', 0: 'Desconhecido', 3: 'Recalque', 6: 'Usina de reciclagem', 7: 'Incinerador'},
 'tipoedifturist': {10: 'Est\xc3\xa1tua', 13: 'Pante\xc3\xa3o', 99: 'Outros', 11: 'Mirante', 0: 'Desconhecido', 9: 'Cruzeiro', 12: 'Monumento'},
 'tipoelemnat': {13: 'Fal\xc3\xa9sia', 8: 'Escarpa', 9: 'Pen\xc3\xadnsula', 5: 'Maci\xc3\xa7o', 0: 'Desconhecido', 3: 'Montanha', 11: 'Cabo', 14: 'Talude', 99: 'Outros', 10: 'Ponta', 4: 'Chapada', 7: 'Plan\xc3\xadcie', 12: 'Praia', 6: 'Planalto', 2: 'Morro', 1: 'Serra'},
 'tipofontedagua': {0: 'Desconhecido', 2: 'Po\xc3\xa7o Artesiano', 3: 'Olho d`\xc3\xa1gua', 1: 'Po\xc3\xa7o'},
 'tipogrupocnae': {4: '80.9 - Educa\xc3\xa7\xc3\xa3o Profissional e Outras Atividades de Ensino', 99: 'Outros', 3: '80.3 - Ensino Superior', 10: '85-3 - Servi\xc3\xa7o Social', 98: 'Misto', 8: '85.1 Atividades de Aten\xc3\xa7\xc3\xa3o \xc3\xa0 Sa\xc3\xbade', 1: '80.1 - Educa\xc3\xa7\xc3\xa3o Infantil e Ensino Fundamental', 0: 'Desconhecido', 9: '85.2 Servi\xc3\xa7os Veterin\xc3\xa1rios', 6: '75-2 - Servi\xc3\xa7os Coletivos Prestados pela Administra\xc3\xa7\xc3\xa3o P\xc3\xbablica', 5: '75-1 - Administra\xc3\xa7\xc3\xa3o do Estado e da Pol\xc3\xadtica Econ\xc3\xb4mica e Social', 19: '80.2 - Ensino M\xc3\xa9dio', 7: '75-3 - Seguridade Social'},
 'tipolavoura': {0: 'Desconhecido', 2: 'Semi-perene', 3: 'Anual', 1: 'Perene'},
 'tipoequipagropec': {0: 'Desconhecido', 99: 'Outros', 1: 'Piv\xc3\xb4 central'},
 'tipoestgerad': {0: 'Desconhecido', 99: 'Outros', 5: 'E\xc3\xb3lica', 7: 'Mar\xc3\xa9-motriz', 6: 'Solar'},
 'tipoilha': {1: 'Fluvial', 2: 'Mar\xc3\xadtima', 98: 'Mista', 3: 'Lacustre'},
 'tipoestmed': {1: 'Esta\xc3\xa7\xc3\xa3o Climatol\xc3\xb3gica Principal - CP', 11: 'Esta\xc3\xa7\xc3\xa3o Maregr\xc3\xa1fica - MA', 2: 'Esta\xc3\xa7\xc3\xa3o Climatol\xc3\xb3gica Auxiliar - CA', 9: 'Esta\xc3\xa7\xc3\xa3o de Radiossonda - RS', 4: 'Esta\xc3\xa7\xc3\xa3o Pluviom\xc3\xa9trica - PL', 0: 'Desconhecido', 8: 'Esta\xc3\xa7\xc3\xa3o de Radar Meteorol\xc3\xb3gico - RD', 5: 'Esta\xc3\xa7\xc3\xa3o E\xc3\xb3lica - EO', 7: 'Esta\xc3\xa7\xc3\xa3o Solarim\xc3\xa9trica - SL', 6: 'Esta\xc3\xa7\xc3\xa3o Evaporim\xc3\xa9trica - EV', 10: 'Esta\xc3\xa7\xc3\xa3o Fluviom\xc3\xa9trica - FL', 3: 'Esta\xc3\xa7\xc3\xa3o Agroclimatol\xc3\xb3gica - AC', 12: 'Esta\xc3\xa7\xc3\xa3o de Mar\xc3\xa9s Terrestres - Crosta'},
 'tipoentroncamento': {5: 'Entroncamento ferrovi\xc3\xa1rio', 1: 'Cruzamento rodovi\xc3\xa1rio', 99: 'Outros', 4: 'R\xc3\xb3tula', 3: 'Trevo rodovi\xc3\xa1rio', 2: 'C\xc3\xadrculo rodovi\xc3\xa1rio'},
 'tipolimmassa': {2: 'Margem de massa d`\xc3\xa1gua', 5: 'Limite interno entre massas e/ou trechos', 1: 'Costa vis\xc3\xadvel da carta', 4: 'Margem direita de trechos de massa d`\xc3\xa1gua', 7: 'Limite interno com foz mar\xc3\xadtima', 6: 'Limite com elemento artificial', 3: 'Margem esquerda de trechos de massa d`\xc3\xa1gua'},
 'tipoestrut': {4: 'Porto seco', 5: 'Terminal rodovi\xc3\xa1rio', 3: 'Fiscaliza\xc3\xa7\xc3\xa3o', 1: 'Esta\xc3\xa7\xc3\xa3o', 2: 'Com\xc3\xa9rcio e servi\xc3\xa7os', 0: 'Desconhecido', 7: 'Terminal multimodal', 6: 'Terminal urbano'},
 'tipolimintramun': {5: 'Bairro', 2: 'Sub-distrital', 1: 'Distrital', 4: 'Regi\xc3\xa3o administrativa', 3: 'Per\xc3\xadmetro urbano legal'},
 'tipogrutacaverna': {20: 'Caverna', 19: 'Gruta'},
 'tipolimareaesp': {31: 'Esta\xc3\xa7\xc3\xa3o Ecol\xc3\xb3gica - ESEC', 5: 'Amaz\xc3\xb4nia legal', 17: 'Reserva florestal', 23: 'Floresta Extrativista', 2: 'Terra ind\xc3\xadgena', 8: '\xc3\x81rea de preserva\xc3\xa7\xc3\xa3o permanente', 18: 'Reserva ecol\xc3\xb3gica', 29: 'Reserva de Fauna - REFAU', 22: 'Floresta de rendimento sustent\xc3\xa1vel', 4: 'Assentamento rural', 28: 'Reserva Extrativista - RESEX', 14: 'S\xc3\xadtios RAMSAR', 16: 'Reserva da biosfera', 21: 'Estrada parque', 3: 'Quilombo', 32: 'Parque - PAR', 11: 'Distrito florestal', 7: 'Pol\xc3\xadgono das secas', 10: 'Mosaico', 24: '\xc3\x81rea de prote\xc3\xa7\xc3\xa3o ambiental - APA', 30: 'Reserva Particular do Patrim\xc3\xb4nio Natural - RPPN', 15: 'S\xc3\xadtios do patrim\xc3\xb4nio', 36: 'Area Militar', 12: 'Corredor ecol\xc3\xb3gico', 99: 'Outros', 34: 'Reserva Biol\xc3\xb3gica - REBIO', 33: 'Monumento Natural - MONA', 1: 'Terra p\xc3\xbablica', 6: 'Faixa de fronteira', 35: 'Ref\xc3\xbagio de Vida Silvestre - RVS', 13: 'Floresta p\xc3\xbablica', 9: 'Reserva legal', 20: 'Horto florestal', 19: 'Esta\xc3\xa7\xc3\xa3o biol\xc3\xb3gica', 27: 'Reserva de Desenvolvimento Sustent\xc3\xa1vel - RDS', 26: 'Floresta - FLO', 25: '\xc3\x81rea de Relevante Interesse Ecol\xc3\xb3gico - ARIE'},
 'tipoextmin': {5: 'Garimpo', 99: 'Outros', 4: 'Mina', 6: 'Salina', 8: 'Ponto de Prospec\xc3\xa7\xc3\xa3o', 0: 'Desconhecido', 7: 'Pedreira', 1: 'Po\xc3\xa7o'},
 'tipolocalcrit': {7: 'Outras interfer\xc3\xaancias', 2: 'Risco geot\xc3\xa9cnico', 4: 'Interfer\xc3\xaancia com hidrografia', 5: 'Interfer\xc3\xaancia com \xc3\xa1reas especiais', 6: 'Interfer\xc3\xaancia com vias', 0: 'Desconhecido', 3: 'Interfer\xc3\xaancia com localidades', 1: 'Subesta\xc3\xa7\xc3\xa3o de v\xc3\xa1lvulas e/ou bombas'},
 'tipooperativo': {0: 'Desconhecido', 1: 'Elevadora', 2: 'Abaixadora'},
 'tipomarcolim': {1: 'Internacional', 99: 'Outros', 2: 'Estadual', 3: 'Municipal'},
 'tipooutlimofic': {99: 'Outros', 3: 'Zona econ\xc3\xb4mica exclusiva', 5: 'Faixa de fronteira', 1: 'Mar territorial', 0: 'Desconhecido', 2: 'Zona cont\xc3\xadgua', 6: 'Plataforma continental jur\xc3\xaddica', 4: 'Lateral mar\xc3\xadtima'},
 'tipolimoper': {6: 'Linha m\xc3\xa9dia de enchente-ORD', 5: 'Linha preamar m\xc3\xa9dia - 1831', 1: 'Setor censit\xc3\xa1rio', 0: 'Desconhecido', 4: 'Costa vis\xc3\xadvel da cartainterpretada)', 2: 'Linha de base normal', 3: 'Linha de base reta'},
 'tipoobst': {4: 'Natural', 5: 'Artificial'},
 'tipopassagviad': {6: 'Viaduto', 5: 'Passagem elevada'},
 'tipooutunidprot': {5: 'Corredor ecol\xc3\xb3gico', 4: 'Distrito florestal', 8: 'S\xc3\xadtios do patrim\xc3\xb4nio', 2: 'Reserva legal', 9: 'Reserva da biosfera', 6: 'Floresta p\xc3\xbablica', 3: 'Mosaico', 1: '\xc3\x81rea de preserva\xc3\xa7\xc3\xa3o permanente', 7: 'S\xc3\xadtios RAMSAR'},
 'tipomacchav': {0: 'Desconhecido', 1: 'Macega', 2: 'Chavascal'},
 'tipomaqtermica': {0: 'Desconhecido', 2: 'Turbina \xc3\xa0 vapor TBVP)', 4: 'Motor de Combust\xc3\xa3o Interna NCIA)', 1: 'Turbina \xc3\xa0 g\xc3\xa1s TBGS)', 3: 'Ciclo combinado CLCB)'},
 'tipomassadagua': {10: 'Represa/A\xc3\xa7ude', 5: 'Enseada', 3: 'Oceano', 7: 'Lago/Lagoa', 4: 'Ba\xc3\xada', 6: 'Meandro Abandonado', 0: 'Desconhecida'},
 'tipopista': {1: 'Atletismo', 2: 'Ciclismo', 98: 'Misto', 99: 'Outros', 3: 'Motociclismo', 9: 'Pista de pouso', 0: 'Desconhecido', 4: 'Automobilismo', 5: 'Corrida de cavalos', 11: 'Heliporto', 10: 'Pista de t\xc3\xa1xi'},
 'tipoplataforma': {0: 'Desconhecido', 3: 'Petr\xc3\xb3leo', 98: 'Misto', 5: 'G\xc3\xa1s'},
 'tipolimpol': {1: 'Internacional', 2: 'Estadual', 3: 'Municipal'},
 'tiporesiduo': {14: 'Lixo s\xc3\xa9ptico', 15: 'Chorume', 99: 'Outros', 9: 'Esgoto', 12: 'Lixo domiciliar e comercial', 98: 'Misto', 13: 'Lixo t\xc3\xb3xico', 0: 'Desconhecido', 16: 'Vinhoto'},
 'tipoptoenergia': {3: 'Subesta\xc3\xa7\xc3\xa3o de distribui\xc3\xa7\xc3\xa3o', 4: 'Ponto de ramifica\xc3\xa7\xc3\xa3o', 1: 'Esta\xc3\xa7\xc3\xa3o geradora de energia', 2: 'Subesta\xc3\xa7\xc3\xa3o de transmiss\xc3\xa3o', 0: 'Desconhecido'},
 'tipoptorefgeodtopo': {1: 'V\xc3\xa9rtice de Triangula\xc3\xa7\xc3\xa3o - VT', 6: 'Ponto barom\xc3\xa9trico - B', 99: 'Outros', 8: 'Ponto de Sat\xc3\xa9lite - SAT', 0: 'Desconhecido', 7: 'Ponto Trigonom\xc3\xa9trico - RV', 2: 'Refer\xc3\xaancia de N\xc3\xadvel - RN', 5: 'Ponto Astron\xc3\xb4mico - PA', 4: 'Esta\xc3\xa7\xc3\xa3o de Poligonal - EP', 3: 'Esta\xc3\xa7\xc3\xa3o Gravim\xc3\xa9trica - EG'},
 'tipoquebramolhe': {0: 'Desconhecido', 2: 'Molhe', 1: 'Quebramar'},
 'tipoponte': {0: 'Desconhecido', 1: 'M\xc3\xb3vel', 3: 'Fixa', 2: 'P\xc3\xaansil'},
 'tiporef': {2: 'Planim\xc3\xa9trico', 1: 'Altim\xc3\xa9trico', 4: 'Gravim\xc3\xa9trico', 3: 'Planialtim\xc3\xa9trico'},
 'tipoptocontrole': {9: 'Ponto de Controle', 12: 'Ponto Perspectivo', 13: 'Ponto Fotogram\xc3\xa9trico', 99: 'Outros'},
 'tipoqueda': {0: 'Desconhecido', 2: 'Salto', 1: 'Cachoeira', 3: 'Catarata'},
 'tiporecife': {20: 'Coral', 0: 'Desconhecido', 1: 'Arenito', 2: 'Rochoso'},
 'tipoptoestmed': {1: 'Esta\xc3\xa7\xc3\xa3o Climatol\xc3\xb3gica Principal - CP', 11: 'Esta\xc3\xa7\xc3\xa3o Maregr\xc3\xa1fica - MA', 2: 'Esta\xc3\xa7\xc3\xa3o Climatol\xc3\xb3gica Auxiliar - CA', 9: 'Esta\xc3\xa7\xc3\xa3o de Radiossonda - RS', 4: 'Esta\xc3\xa7\xc3\xa3o Pluviom\xc3\xa9trica - PL', 0: 'Desconhecido', 8: 'Esta\xc3\xa7\xc3\xa3o de Radar Meteorol\xc3\xb3gico - RD', 5: 'Esta\xc3\xa7\xc3\xa3o E\xc3\xb3lica - EO', 7: 'Esta\xc3\xa7\xc3\xa3o Solarim\xc3\xa9trica - SL', 6: 'Esta\xc3\xa7\xc3\xa3o Evaporim\xc3\xa9trica - EV', 10: 'Esta\xc3\xa7\xc3\xa3o Fluviom\xc3\xa9trica - FL', 3: 'Esta\xc3\xa7\xc3\xa3o Agroclimatol\xc3\xb3gica - AC', 12: 'Esta\xc3\xa7\xc3\xa3o de Mar\xc3\xa9s Terrestres - Crosta'},
 'tipoprodutoresiduo': {6: 'Gr\xc3\xa3os', 36: 'Esc\xc3\xb3ria', 41: 'Forragem', 34: 'Sal', 24: 'M\xc3\xa1rmore', 19: 'Semente', 21: 'Folhagens', 40: 'Pedras preciosas', 28: '\xc3\x93leo diesel', 35: 'Ferro', 33: 'Carv\xc3\xa3o', 22: 'Pedra', 39: 'Prata', 3: 'Petr\xc3\xb3leo', 32: 'Cobre', 16: 'Vinhoto', 25: 'Bauxita', 42: 'Areia', 23: 'Granito', 0: 'Desconhecido', 5: 'G\xc3\xa1s', 30: '\xc3\x81lcool', 26: 'Mangan\xc3\xaas', 31: 'Querosene', 27: 'Talco', 38: 'Diamante', 37: 'Ouro', 20: 'Inseticida', 99: 'Outros', 98: 'Misto', 44: 'Pi\xc3\xa7arra', 18: 'Cascalho', 17: 'Estrume', 43: 'Saibro', 29: 'Gasolina'},
 'tiporocha': {21: 'Matac\xc3\xa3o - pedra', 23: '\xc3\x81rea Rochosa - lajedo', 22: 'Penedo - isolado'},
 'tiposecaocnae': {3: 'F - Constru\xc3\xa7\xc3\xa3o', 1: 'C - Ind\xc3\xbastrias Extrativas', 2: 'D - Ind\xc3\xbastrias de Transforma\xc3\xa7\xc3\xa3o', 99: 'Outros', 0: 'Desconhecido'},
 'tipopostopol': {0: 'Desconhecido', 21: 'Posto PRF', 20: 'Posto PM'},
 'tiposinal': {5: 'Barca farol', 6: 'Sinaliza\xc3\xa7\xc3\xa3o de margem', 2: 'B\xc3\xb3ia cega', 1: 'B\xc3\xb3ia luminosa', 0: 'Desconhecido', 4: 'Farol ou farolete', 3: 'B\xc3\xb3ia de amarra\xc3\xa7\xc3\xa3o'},
 'tipotransporte': {22: 'Cargas', 0: 'Desconhecido', 98: 'Misto', 21: 'Passageiros'},
 'tipousocaminhoaer': {22: 'Cargas', 0: 'Desconhecido', 98: 'Misto', 21: 'Passageiros'},
 'tipotrechoduto': {1: 'Duto', 0: 'Desconhecido', 3: 'Correia transportadora', 2: 'Calha'},
 'tipotravessia': {1: 'Vau natural', 2: 'Vau constru\xc3\xadda', 0: 'Desconhecida', 3: 'Bote transportador', 4: 'Balsa'},
 'tiposumvert': {1: 'Sumidouro', 2: 'Vertedouro'},
 'tipotravessiaped': {7: 'Passagem subterr\xc3\xa2nea', 8: 'Passarela', 0: 'Desconhecida', 9: 'Pinguela'},
 'tipotrechorod': {4: 'Auto-estrada', 2: 'Rodovia', 1: 'Acesso', 3: 'Caminho carro\xc3\xa7\xc3\xa1vel'},
 'tipoterrexp': {24: 'Saibro', 4: 'Pedregoso', 23: 'Terra', 18: 'Cascalho', 0: 'Desconhecido', 12: 'Areia'},
 'tipotunel': {1: 'T\xc3\xbanel', 2: 'Passagem subterr\xc3\xa2nea sob via'},
 'tipounidprotinteg': {3: 'Monumento batural - MONA', 2: 'Parque - PAR', 1: 'Esta\xc3\xa7\xc3\xa3o Ecol\xc3\xb3gica - ESEC', 5: 'Ref\xc3\xbagio de Vida Silvestre - RVS', 4: 'Reserva Biol\xc3\xb3gica - REBIO'},
 'tipounidusosust': {5: 'Reserva Extrativista - RESEX', 3: 'Floresta - FLO', 7: 'Reserva Particular do Patrim\xc3\xb4nio Natural - RPPN', 6: 'Reserva de Fauna - REFAU', 1: '\xc3\x81rea de Prote\xc3\xa7\xc3\xa3o Ambiental - APA', 2: '\xc3\x81rea de Relevante Interesse Ecol\xc3\xb3gico - ARIE', 4: 'Reserva de Desenvolvimento Sustent\xc3\xa1vel - RDS'},
 'tipotrechoferrov': {6: 'Aerom\xc3\xb3vel', 0: 'Desconhecido', 7: 'Ferrovia', 8: 'Metrovia', 5: 'Bonde'},
 'tipotrechocomunic': {0: 'Desconhecido', 4: 'Dados', 99: 'Outros', 6: 'Telegr\xc3\xa1fica', 7: 'Telef\xc3\xb4nica'},
 'tipotrechomassa': {2: 'Canal', 1: 'Rio', 99: 'Outros', 9: 'Laguna', 10: 'Represa/a\xc3\xa7ude'},
 'usoprincipal': {0: 'Desconhecido', 99: 'Outros', 3: 'Energia', 1: 'Irriga\xc3\xa7\xc3\xa3o', 97: 'N\xc3\xa3o aplic\xc3\xa1vel', 2: 'Abastecimento'},
 'usopista': {12: 'Militar', 0: 'Desconhecido', 11: 'P\xc3\xbablico', 13: 'P\xc3\xbablico/Militar', 6: 'Particular'},
 'trafego': {0: 'Desconhecido', 1: 'Permanente', 2: 'Peri\xc3\xb3dico'},
 'unidadevolume': {0: 'Desconhecido', 2: 'Metro c\xc3\xbabico', 1: 'Litro'},
 'tipotorre': {0: 'Desconhecido', 1: 'Autoportante', 2: 'Estaiada'},
 'denominacaoassociada': {5: 'Crist\xc3\xa3', 99: 'Outras', 6: 'Israelita', 7: 'Mu\xc3\xa7ulmana'},
 'classificacaoporte': {1: 'Arb\xc3\xb3rea', 98: 'Misto', 2: 'Arbustiva', 0: 'Desconhecido', 3: 'Herb\xc3\xa1cea'},
 'tipoexposicao': {0: 'Desconhecido', 5: 'C\xc3\xa9u aberto', 99: 'Outros', 4: 'Coberto', 3: 'Fechado'},
 'tipocemiterio': {1: 'Cremat\xc3\xb3rio', 99: 'Outros', 5: 'T\xc3\xbamulo Isolado', 2: 'Parque', 3: 'Vertical', 0: 'Desconhecido', 98: 'Misto', 4: 'Comum'},
 'situacaoagua': {7: 'N\xc3\xa3o tratada', 6: 'Tratada', 0: 'Desconhecida'},
 'tipopostofisc': {0: 'Desconhecido', 11: 'Fiscaliza\xc3\xa7\xc3\xa3o', 99: 'Outros', 98: 'Mista', 10: 'Tributa\xc3\xa7\xc3\xa3o'},
 'tipousoedif': {1: 'Pr\xc3\xb3prio nacional', 0: 'Desconhecido', 2: 'Uso especial da Uni\xc3\xa3o'},
 'tipoedifcivil': {3: 'Cartorial', 99: 'Outros', 7: 'Seguridade Social', 22: 'Prefeitura', 5: 'Eleitoral', 2: 'Prisional', 0: 'Desconhecido', 6: 'Produ\xc3\xa7\xc3\xa3o e/ou pesquisa', 9: 'Assembl\xc3\xa9ia Legislativa', 4: 'Gest\xc3\xa3o', 1: 'Policial', 8: 'C\xc3\xa2mara Municipal'},
 'motivodescontinuidade': {5: 'Descontinuidade por diferente interpreta\xc3\xa7\xc3\xa3o das classes', 4: 'Descontinuidade por falta de acur\xc3\xa1cia', 3: 'Descontinuidade por escala de insumo', 7: 'Descontinuidade por excesso', 6: 'Descontinuidade por omiss\xc3\xa3o', 2: 'Descontinuidade devido a transforma\xc3\xa7\xc3\xa3o', 1: 'Descontinuidade Temporal'},
 'tratamento': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o', 97: 'N\xc3\xa3o aplic\xc3\xa1vel'},
 'tipopocomina': {0: 'Desconhecido', 3: 'Vertical', 97: 'N\xc3\xa3o aplic\xc3\xa1vel', 2: 'Horizontal'},
 'chamine': {1: 'Sim', 2: 'N\xc3\xa3o'},
 'operacional': {1: 'Sim', 0: 'Desconhecido', 2: 'N\xc3\xa3o'},
 'situacaofisica': {4: 'Planejada', 1: 'Abandonada', 5: 'Constru\xc3\xadda', 0: 'Desconhecida', 3: 'Em Constru\xc3\xa7\xc3\xa3o', 2: 'Destru\xc3\xadda'},
 'geometriaaproximada': {1: 'Sim', 2: 'N\xc3\xa3o'}
}

def ForcarAtributos(SimNao, camada, forcado):
 if SimNao:
     DP = camada.dataProvider()
     for item in forcado:
         if len(item)==2: #lista, Ex: ['atributo ref', 'valor_novo']
            if item[0] != 'geometriaaproximada':
             att_column = layer.pendingFields().fieldNameIndex(item[0])
             atributo = item[1]
             newColumnValueMap = {att_column : atributo}
             for feat in camada.getFeatures():
                 newAttributesValuesMap = {feat.id() : newColumnValueMap}
                 DP.changeAttributeValues(newAttributesValuesMap)
         else: #lista, Ex: ['atributo ref', 'valor_ref', 'atributo_teste', 'valor_novo']
            if item[0] != 'geometriaaproximada':
             att_ref = item[0]
             valor_ref = item[1]
             att_teste = layer.pendingFields().fieldNameIndex(item[2])
             valor_novo = item[3]
             newColumnValueMap = {att_teste : valor_novo}
             for feat in camada.getFeatures():
                 if feat[att_ref] == valor_ref:
                     newAttributesValuesMap = {feat.id() : newColumnValueMap}
                     DP.changeAttributeValues(newAttributesValuesMap)

def VerificarAtributos(camada, teste):
 for item in teste:
     atributo = (item[0]).split('_')[0]
     atributoDom = item[0]
     condicao = item[1]
     if condicao == 'string':
         for feat in camada.getFeatures():
             if feat[atributo] == None or feat[atributo] == '' or len(feat[atributo])<2:
                 nome = camada.name()
                 ID = feat.id()
                 correcao = 'Atributo "' + atributo +'" deve ser preenchido.'
                 att = [nome, ID, atributo, correcao]
                 geom = feat.geometry()
                 if geom:
                     c = geom.centroid()
                     feature.setGeometry(c)
                     feature.setAttributes(att)
                     writer.addFeature(feature)
     elif type(condicao) is tuple:
         minimo = condicao[0]
         maximo = condicao[1]
         for feat in camada.getFeatures():
             if not(feat[atributo] >= minimo and feat[atributo] <= maximo):
                 nome = camada.name()
                 ID = feat.id()
                 correcao = 'Valor de "' + atributo + '" deve estar entre ' + str(minimo) +' e ' + str(maximo) + '.'
                 att = [nome, ID, atributo, correcao]
                 geom = feat.geometry()
                 if geom:
                     c = geom.centroid()
                     feature.setGeometry(c)
                     feature.setAttributes(att)
                     writer.addFeature(feature)
     else:
         for feat in camada.getFeatures():
             if not feat[atributo] in condicao:
                 nome = camada.name()
                 ID = feat.id()
                 valores = ''
                 for val in condicao:
                     valores += '"' + dominios[atributoDom][val] +'", '
                 valores = valores[:-2]
                 correcao = 'Atributo "' +atributo+ '" deve ser: ' + (valores).decode('utf-8') + '.'
                 att = [nome, ID, atributo, correcao]
                 geom = feat.geometry()
                 if geom:
                     c = geom.centroid()
                     feature.setGeometry(c)
                     feature.setAttributes(att)
                     writer.addFeature(feature)

def VerificaOutros(camada, teste):
 atributo = teste[0]
 atributoObr = teste[1]
 for feat in camada.getFeatures():
     if feat[atributo] == 99 and (feat[atributoObr]==None or feat[atributoObr] == '' or len(feat[atributoObr])<2):
         nome = camada.name()
         ID = feat.id()
         correcao = 'Atributo "' + atributoObr + '" deve ser preenchido quando "' +atributo+ '" \xe9 Outros.'
         att = [nome, ID, atributoObr, correcao]
         geom = feat.geometry()
         if geom:
             c = geom.centroid()
             feature.setGeometry(c)
             feature.setAttributes(att)
             writer.addFeature(feature)

def VerificaMisto(camada, teste):
 atributo = teste[0]
 atributoObr = teste[1]
 for feat in camada.getFeatures():
     if feat[atributo] == 98 and (feat[atributoObr]==None or feat[atributoObr] == '' or len(feat[atributoObr])<2):
         nome = camada.name()
         ID = feat.id()
         correcao = 'Atributo "' + atributoObr + '" deve ser preenchido quando "' +atributo+ '" \xe9 Misto.'
         att = [nome, ID, atributoObr, correcao]
         geom = feat.geometry()
         if geom:
             c = geom.centroid()
             feature.setGeometry(c)
             feature.setAttributes(att)
             writer.addFeature(feature)
     elif feat[atributo] == 98 and not(feat[atributoObr]==None or feat[atributoObr] == '' or len(feat[atributoObr])<2):
         if len((feat[atributoObr]).split(','))<2:
             nome = camada.name()
             ID = feat.id()
             correcao = 'Atributo "' + atributoObr + '" deve conter mais de um elemento separado por "," quando "' +atributo+ '" \xe9 Misto.'
             att = [nome, ID, atributoObr, correcao]
             geom = feat.geometry()
             if geom:
                 c = geom.centroid()
                 feature.setGeometry(c)
                 feature.setAttributes(att)
                 writer.addFeature(feature)

def VerificarAtributosCond(camada, teste):
    atributo = teste[0]
    atributoObr = teste[1]
    for feat in camada.getFeatures():
         if (feat[atributo] in teste[2]) and (feat[atributoObr]==None or feat[atributoObr] == '' or len(feat[atributoObr])<2):
             nome = camada.name()
             ID = feat.id()
             correcao = 'Atributo "' + atributoObr + '" deve ser preenchido quando "' +atributo+ '" \xe9 ' +dominios[atributo][feat[atributo]] +'.'
             att = [nome, ID, atributoObr, correcao]
             geom = feat.geometry()
             if geom:
                 c = geom.centroid()
                 feature.setGeometry(c)
                 feature.setAttributes(att)
                 writer.addFeature(feature)

def VerificarCartaImpress(camada, campo):
    for feat in camada.getFeatures():
        if feat[campo]==None or feat[campo] == '':
             nome = camada.name()
             ID = feat.id()
             correcao = 'Verificar se o atributo "' + campo + '" consta na Carta Impressa.'
             att = [nome, ID, campo, correcao]
             geom = feat.geometry()
             if geom:
                 c = geom.centroid()
                 feature.setGeometry(c)
                 feature.setAttributes(att)
                 writer.addFeature(feature)

def VerificarSeEntao(camada, teste):
 att1 = teste[0][0]
 lista1 = teste[0][1]
 att2 = teste[1][0]
 lista2 = teste[1][1]
 for feat in camada.getFeatures():
     if feat[att1] in lista1:
         if not(feat[att2] in lista2):
             nome = camada.name()
             ID = feat.id()
             correcao = 'Atributos "' + att1 + '" e "' + att2 + '" n\xe3o s\xe3o compat\xedveis.'
             att = [nome, ID, att1 + ' e ' + att2, correcao]
             geom = feat.geometry()
             if geom:
                 c = geom.centroid()
                 feature.setGeometry(c)
                 feature.setAttributes(att)
                 writer.addFeature(feature)


progress.setInfo('<br/><b>1. ADMINISTRACAO PUBLICA...</b><br/>')

# adm_area_pub_civil_a
camada = 'adm_area_pub_civil_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# adm_area_pub_militar_a
camada = 'adm_area_pub_militar_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# adm_edif_pub_civil_a
camada = 'adm_edif_pub_civil_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97], ['tipousoedif', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]], ['tipoedifcivil', [3,99,7,22,5,2,6,9,4,1,8]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifcivil', 'nome']
 VerificaOutros(layer, teste)

# adm_edif_pub_civil_p
camada = 'adm_edif_pub_civil_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97], ['tipousoedif', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]], ['tipoedifcivil', [3,99,7,22,5,2,6,9,4,1,8]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifcivil', 'nome']
 VerificaOutros(layer, teste)

# adm_edif_pub_militar_a
camada = 'adm_edif_pub_militar_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97], ['tipousoedif', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]], ['tipoedifmil', [14,99,19,15,12,18,16,13,17]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifmil', 'nome']
 VerificaOutros(layer, teste)

# adm_edif_pub_militar_p
camada = 'adm_edif_pub_militar_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97], ['tipousoedif', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]], ['tipoedifmil', [14,99,19,15,12,18,16,13,17]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifmil', 'nome']
 VerificaOutros(layer, teste)

# adm_posto_fiscal_a
camada = 'adm_posto_fiscal_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]], ['tipopostofisc', [11,99,98,10]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipopostofisc', 'nome']
 VerificaOutros(layer, teste)
 # Verificar condicao Misto
 teste = ['tipopostofisc', 'nome']
 VerificaMisto(layer, teste)

# adm_posto_fiscal_p
camada = 'adm_posto_fiscal_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]], ['tipopostofisc', [11,99,98,10]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipopostofisc', 'nome']
 VerificaOutros(layer, teste)
 # Verificar condicao Misto
 teste = ['tipopostofisc', 'nome']
 VerificaMisto(layer, teste)

# adm_posto_pol_rod_a
camada = 'adm_posto_pol_rod_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]], ['tipopostopol', [21,20]]]
 VerificarAtributos(layer, teste)

# adm_posto_pol_rod_p
camada = 'adm_posto_pol_rod_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]], ['tipopostopol', [21,20]]]
 VerificarAtributos(layer, teste)


progress.setInfo('<b>2. ABASTECIMENTO DE AGUA E SANEAMENTO BASICO...</b><br/>')

# asb_area_abast_agua_a
camada = 'asb_area_abast_agua_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# asb_area_saneamento_a
camada = 'asb_area_saneamento_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 
# asb_cemiterio_a
camada = 'asb_cemiterio_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipocemiterio', [1,5,2,3,4]], ['denominacaoassociada',[5,6,7]]]
 VerificarAtributos(layer, teste)
 teste = ['tipocemiterio', 'nome',[1,2,3,4]]
 VerificarAtributosCond(layer, teste)

# asb_cemiterio_p
camada = 'asb_cemiterio_p'

layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipocemiterio', [1,5,2,3,4]], ['denominacaoassociada',[5,6,7]]]
 VerificarAtributos(layer, teste)
 teste = ['tipocemiterio', 'nome',[1,2,3,4]]
 VerificarAtributosCond(layer, teste)

# asb_dep_abast_agua_a
camada = 'asb_dep_abast_agua_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodepabast', [1,2,3,99]], ['construcao', [1,2]], ['finalidade_asb',[2,3,4,8]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipodepabast', 'nome']
 VerificaOutros(layer, teste)

# asb_dep_abast_agua_p
camada = 'asb_dep_abast_agua_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodepabast', [1,2,3,99]], ['construcao', [1,2]], ['finalidade_asb',[2,3,4,8]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipodepabast', 'nome']
 VerificaOutros(layer, teste)

# asb_dep_saneamento_a
camada = 'asb_dep_saneamento_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodepsaneam', [1,4,5,6,99]], ['construcao', [1,2]], ['finalidade_asb',[2,3,4,8]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['residuo',[1,2]], ['tiporesiduo',[14,15,99,9,12,98,13,16]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipodepsaneam', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tiporesiduo', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tiporesiduo', 'nome']
 VerificaMisto(layer, teste)

# asb_dep_saneamento_p
camada = 'asb_dep_saneamento_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodepsaneam', [1,4,5,6,99]], ['construcao', [1,2]], ['finalidade_asb',[2,3,4,8]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['residuo',[1,2]], ['tiporesiduo',[14,15,99,9,12,98,13,16]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipodepsaneam', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tiporesiduo', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tiporesiduo', 'nome']
 VerificaMisto(layer, teste)

# asb_edif_abast_agua_a
camada = 'asb_edif_abast_agua_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoedifabast', [1,2,3,98,99]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifabast', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tipoedifabast', 'nome']
 VerificaMisto(layer, teste)

# asb_edif_abast_agua_p
camada = 'asb_edif_abast_agua_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoedifabast', [1,2,3,98,99]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifabast', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tipoedifabast', 'nome']
 VerificaMisto(layer, teste)

# asb_edif_saneamento_a
camada = 'asb_edif_saneamento_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoedifsaneam', [3,5,6,7,99]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifsaneam', 'nome']
 VerificaOutros(layer, teste)

# asb_edif_saneamento_p
camada = 'asb_edif_saneamento_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoedifsaneam', [3,5,6,7,99]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifsaneam', 'nome']
 VerificaOutros(layer, teste)


progress.setInfo('<b>3. ESTRUTURA ECONOMICA...</b><br/>')

# eco_area_comerc_serv_a
camada = 'eco_area_comerc_serv_a'
forcado = [['geometriaaproximada', 1]]
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 ForcarAtributos(SimNao, layer, forcado)
 
# eco_area_ext_mineral_a
camada = 'eco_area_ext_mineral_a'
forcado = [['geometriaaproximada', 1]]
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 ForcarAtributos(SimNao, layer, forcado)
 
# eco_area_industrial_a
camada = 'eco_area_industrial_a'
forcado = [['geometriaaproximada', 1]]
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 ForcarAtributos(SimNao, layer, forcado)

# eco_deposito_geral_a
camada = 'eco_deposito_geral_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97], ['tratamento', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodepgeral', [9,11,99,32,19,8,10]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoexposicao',[3,4,5,99]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipodepgeral', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tipoexposicao', 'nome']
 VerificaOutros(layer, teste)

# eco_deposito_geral_p
camada = 'eco_deposito_geral_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97], ['tratamento', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodepgeral', [9,11,99,32,19,8,10]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoexposicao',[3,4,5,99]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipodepgeral', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tipoexposicao', 'nome']
 VerificaOutros(layer, teste)

# eco_edif_agrop_ext_veg_pesca_a
camada = 'eco_edif_agrop_ext_veg_pesca_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoedifagropec', [99,14,18,12,17,13,15,16]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifagropec', 'nome']
 VerificaOutros(layer, teste)

# eco_edif_agrop_ext_veg_pesca_p
camada = 'eco_edif_agrop_ext_veg_pesca_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoedifagropec', [99,14,18,12,17,13,15,16]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifagropec', 'nome']
 VerificaOutros(layer, teste)

# eco_edif_comerc_serv_a
camada = 'eco_edif_comerc_serv_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoedifcomercserv', [8,99,6,5,3,4,7]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['finalidade_eco',[98,1,2]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifcomercserv', 'nome']
 VerificaOutros(layer, teste)
 
# eco_edif_comerc_serv_p
camada = 'eco_edif_comerc_serv_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoedifcomercserv', [8,99,6,5,3,4,7]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['finalidade_eco',[98,1,2]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifcomercserv', 'nome']
 VerificaOutros(layer, teste)

# eco_edif_ext_mineral_a
camada = 'eco_edif_ext_mineral_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodivisaocnae', [92,21,45,19,30,32,36,24,33,52,14,1,26,31,28,22,27,55,50,16,11,20,37,5,35,15,51,74,99,13,17,25,34,29,18,10,2]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipodivisaocnae', 'nome']
 VerificaOutros(layer, teste)
 
# eco_edif_ext_mineral_p
camada = 'eco_edif_ext_mineral_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodivisaocnae', [92,21,45,19,30,32,36,24,33,52,14,1,26,31,28,22,27,55,50,16,11,20,37,5,35,15,51,74,99,13,17,25,34,29,18,10,2]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipodivisaocnae', 'nome']
 VerificaOutros(layer, teste)

# eco_edif_industrial_a
camada = 'eco_edif_industrial_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodivisaocnae', [92,21,45,19,30,32,36,24,33,52,14,1,26,31,28,22,27,55,50,16,11,20,37,5,35,15,51,74,99,13,17,25,34,29,18,10,2]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['chamine', [1,2]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipodivisaocnae', 'nome']
 VerificaOutros(layer, teste)

# eco_edif_industrial_p
camada = 'eco_edif_industrial_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodivisaocnae', [92,21,45,19,30,32,36,24,33,52,14,1,26,31,28,22,27,55,50,16,11,20,37,5,35,15,51,74,99,13,17,25,34,29,18,10,2]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['chamine', [1,2]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipodivisaocnae', 'nome']
 VerificaOutros(layer, teste)
 
# eco_ext_mineral_a
camada = 'eco_ext_mineral_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tiposecaocnae', [3,1,2,99]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoextmin', [5,99,4,6,8,7,1]], ['tipoprodutoresiduo', [6,36,41,34,24,19,21,40,28,35,33,22,39,3,32,16,25,42,23,5,30,26,31,27,38,37,20,99,98,44,18,17,43,29]], ['tipopocomina', [0,3,2]], ['procextracao', [1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tiposecaocnae', 'nome']
 VerificaOutros(layer, teste)
 
# eco_ext_mineral_p
camada = 'eco_ext_mineral_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tiposecaocnae', [3,1,2,99]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoextmin', [5,99,4,6,8,7,1]], ['tipoprodutoresiduo', [6,36,41,34,24,19,21,40,28,35,33,22,39,3,32,16,25,42,23,5,30,26,31,27,38,37,20,99,98,44,18,17,43,29]], ['tipopocomina', [0,3,2]], ['procextracao', [1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tiposecaocnae', 'nome']
 VerificaOutros(layer, teste)

# eco_plataforma_a
camada = 'eco_plataforma_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoplataforma', [3,98,5]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoplataforma', 'nome']
 VerificaMisto(layer, teste)
 
# eco_plataforma_p
camada = 'eco_plataforma_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoplataforma', [3,98,5]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoplataforma', 'nome']
 VerificaMisto(layer, teste)


progress.setInfo('<b>4. EDUCACAO E CULTURA...</b><br/>')

# edu_area_ensino_a
camada = 'edu_area_ensino_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# edu_area_lazer_a
camada = 'edu_area_lazer_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 
# edu_area_religiosa_a
camada = 'edu_area_religiosa_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# edu_area_ruinas_a
camada = 'edu_area_ruinas_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# edu_arquibancada_a
camada = 'edu_arquibancada_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]]]
 VerificarAtributos(layer, teste)

# edu_arquibancada_p
camada = 'edu_arquibancada_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]]]
 VerificarAtributos(layer, teste)

# edu_campo_quadra_a
camada = 'edu_campo_quadra_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# edu_campo_quadra_p
camada = 'edu_campo_quadra_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# edu_coreto_tribuna_a
camada = 'edu_coreto_tribuna_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# edu_coreto_tribuna_p
camada = 'edu_coreto_tribuna_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# edu_edif_const_lazer_a
camada = 'edu_edif_const_lazer_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoediflazer', [99,1,7,8,2,4,5,6,3]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoediflazer', 'nome']
 VerificaOutros(layer, teste)

# edu_edif_const_lazer_p
camada = 'edu_edif_const_lazer_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoediflazer', [99,1,7,8,2,4,5,6,3]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoediflazer', 'nome']
 VerificaOutros(layer, teste)

# edu_edif_const_turistica_a
camada = 'edu_edif_const_turistica_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string'], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifturist', [10,13,99,11,9,12]], ['ovgd',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifturist', 'nome']
 VerificaOutros(layer, teste)

# edu_edif_const_turistica_p
camada = 'edu_edif_const_turistica_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string'], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifturist', [10,13,99,11,9,12]], ['ovgd',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifturist', 'nome']
 VerificaOutros(layer, teste)

# edu_edif_ensino_a
camada = 'edu_edif_ensino_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoclassecnae', [35,16,32,21,28,7,8,19,13,18,17,10,12,27,34,30,24,11,9,6,15,5,26,14,25,99,33,4,98,1,20,2,23,22,31,29]] ]
 VerificarAtributos(layer, teste)
 teste = ['situacaofisica','nome', [5]]
 VerificarAtributosCond(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoclassecnae', 'nome']
 VerificaOutros(layer, teste)

# edu_edif_ensino_p
camada = 'edu_edif_ensino_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoclassecnae', [35,16,32,21,28,7,8,19,13,18,17,10,12,27,34,30,24,11,9,6,15,5,26,14,25,99,33,4,98,1,20,2,23,22,31,29]] ]
 VerificarAtributos(layer, teste)
 teste = ['situacaofisica','nome', [5]]
 VerificarAtributosCond(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoclassecnae', 'nome']
 VerificaOutros(layer, teste)

# edu_edif_religiosa_a
camada = 'edu_edif_religiosa_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifrelig', [4,5,1,6,2,3,99,7]], ['ensino',[1,2]], ['religiao', 'string']]
 VerificarAtributos(layer, teste)
 teste = ['nome', 'situacaofisica', [5]]
 VerificarAtributosCond(layer, teste)

# edu_edif_religiosa_p
camada = 'edu_edif_religiosa_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifrelig', [4,5,1,6,2,3,99,7]], ['ensino',[1,2]], ['religiao', 'string']]
 VerificarAtributos(layer, teste)
 teste = ['nome', 'situacaofisica', [5]]
 VerificarAtributosCond(layer, teste)
 
# edu_piscina_a
camada = 'edu_piscina_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]]]
 VerificarAtributos(layer, teste)

# edu_pista_competicao_l
camada = 'edu_pista_competicao_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipopista', [1,2,98,99,3,9,4,5,11,10]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipopista', 'nome']
 VerificaOutros(layer, teste)
 # Verificar condicao Misto
 teste = ['tipopista', 'nome']
 VerificaMisto(layer, teste)

# edu_ruina_a
camada = 'edu_ruina_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string']]
 VerificarAtributos(layer, teste)

# edu_ruina_p
camada = 'edu_ruina_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string']]
 VerificarAtributos(layer, teste)


progress.setInfo('<b>5. ENERGIA E COMUNICACOES...</b><br/>')

# enc_antena_comunic_p
camada = 'enc_antena_comunic_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['posicaoreledific', [17,18,14]] ]
 VerificarAtributos(layer, teste)

# enc_area_comunicacao_a
camada = 'enc_area_comunicacao_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# enc_area_energia_eletrica_a
camada = 'enc_area_energia_eletrica_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# enc_edif_comunic_a
camada = 'enc_edif_comunic_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['modalidade', [99,2,3,5,4,1]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['modalidade', 'nome']
 VerificaOutros(layer, teste)

# enc_edif_comunic_p
camada = 'enc_edif_comunic_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['modalidade', [99,2,3,5,4,1]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['modalidade', 'nome']
 VerificaOutros(layer, teste)

# enc_edif_energia_a
camada = 'enc_edif_energia_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifenergia', [3,99,1,2,4,5]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifenergia', 'nome']
 VerificaOutros(layer, teste)

# enc_edif_energia_p
camada = 'enc_edif_energia_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifenergia', [3,99,1,2,4,5]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoedifenergia', 'nome']
 VerificaOutros(layer, teste)

# enc_est_gerad_energia_eletr_a
camada = 'enc_est_gerad_energia_eletr_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string'], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoestgerad', [99,5,6,7]], ['destenergelet', [3,1,4,5,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoestgerad', 'nome']
 VerificaOutros(layer, teste)

# enc_est_gerad_energia_eletr_l
camada = 'enc_est_gerad_energia_eletr_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string'], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoestgerad', [99,5,6,7]], ['destenergelet', [3,1,4,5,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoestgerad', 'nome']
 VerificaOutros(layer, teste)

# enc_est_gerad_energia_eletr_p
camada = 'enc_est_gerad_energia_eletr_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string'], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoestgerad', [99,5,6,7]], ['destenergelet', [3,1,4,5,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoestgerad', 'nome']
 VerificaOutros(layer, teste)

# enc_grupo_transformadores_a
camada = 'enc_est_gerad_energia_eletr_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# enc_grupo_transformadores_p
camada = 'enc_grupo_transformadores_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# enc_hidreletrica_a
camada = 'enc_hidreletrica_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string'], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoestgerad', [99,5,6,7]], ['destenergelet', [3,1,4,5,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoestgerad', 'nome']
 VerificaOutros(layer, teste)

# enc_hidreletrica_l
camada = 'enc_hidreletrica_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string'], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoestgerad', [99,5,6,7]], ['destenergelet', [3,1,4,5,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoestgerad', 'nome']
 VerificaOutros(layer, teste)

# enc_hidreletrica_p
camada = 'enc_hidreletrica_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string'], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoestgerad', [99,5,6,7]], ['destenergelet', [3,1,4,5,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoestgerad', 'nome']
 VerificaOutros(layer, teste)

# enc_termeletrica_a
camada = 'enc_termeletrica_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string'], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoestgerad', [99,5,6,7]], ['destenergelet', [3,1,4,5,2]], ['tipocombustivel', [5,99,3,33,1,98]], ['combrenovavel',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoestgerad', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tipocombustivel', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tipocombustivel', 'nome']
 VerificaMisto(layer, teste)

# enc_termeletrica_p
camada = 'enc_termeletrica_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string'], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoestgerad', [99,5,6,7]], ['destenergelet', [3,1,4,5,2]], ['tipocombustivel', [5,99,3,33,1,98]], ['combrenovavel',[1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoestgerad', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tipocombustivel', 'nome']
 VerificaOutros(layer, teste)
 teste = ['tipocombustivel', 'nome']
 VerificaMisto(layer, teste)


progress.setInfo('<b>6. HIDROGRAFIA...</b><br/>')

# hid_area_umida_a
camada = 'hid_area_umida_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# hid_banco_areia_a
camada = 'hid_banco_areia_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['materialpredominante',0] ]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipobanco', [1,2,3,4]] ]
 VerificarAtributos(layer, teste)

# hid_banco_areia_l
camada = 'hid_banco_areia_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['materialpredominante',0] ]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipobanco', [1,2,3,4]] ]
 VerificarAtributos(layer, teste)

# hid_barragem_a
camada = 'hid_barragem_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['matconstr', [99,1,26,4,23,3,7,6,5,8,25,2]], ['usoprincipal', [97,99,3,1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['matconstr', 'nome']
 VerificaOutros(layer, teste)
 teste = ['usoprincipal', 'nome']
 VerificaOutros(layer, teste)
 
# hid_barragem_l
camada = 'hid_barragem_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['matconstr', [99,1,26,4,23,3,7,6,5,8,25,2]], ['usoprincipal', [97,99,3,1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['matconstr', 'nome']
 VerificaOutros(layer, teste)
 teste = ['usoprincipal', 'nome']
 VerificaOutros(layer, teste)

# hid_barragem_p
camada = 'hid_barragem_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['matconstr', [99,1,26,4,23,3,7,6,5,8,25,2]], ['usoprincipal', [97,99,3,1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['matconstr', 'nome']
 VerificaOutros(layer, teste)
 teste = ['usoprincipal', 'nome']
 VerificaOutros(layer, teste)

# hid_comporta_l
camada = 'hid_comporta_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional',[1,2]] ]
 VerificarAtributos(layer, teste)
 
# hid_comporta_p
camada = 'hid_comporta_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional',[1,2]] ]
 VerificarAtributos(layer, teste)
 
# hid_corredeira_a
camada = 'hid_corredeira_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# hid_corredeira_l
camada = 'hid_corredeira_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# hid_corredeira_p
camada = 'hid_corredeira_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 
# hid_fonte_dagua_p
camada = 'hid_fonte_dagua_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipofontedagua', [1,2,3]], ['regime', [1,6,4,3,2,5]] ]
 VerificarAtributos(layer, teste)

# hid_foz_maritima_a
camada = 'hid_foz_maritima_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# hid_foz_maritima_l
camada = 'hid_foz_maritima_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# hid_foz_maritima_p
camada = 'hid_foz_maritima_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# hid_ilha_a
camada = 'hid_ilha_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 campo = 'nome'
 VerificarCartaImpress(layer, campo)

# hid_ilha_l
camada = 'hid_ilha_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 campo = 'nome'
 VerificarCartaImpress(layer, campo)
 
# hid_ilha_p
camada = 'hid_ilha_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 campo = 'nome'
 VerificarCartaImpress(layer, campo)

# hid_massa_dagua_a
camada = 'hid_ilha_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipomassadagua', [10,5,3,7,4,6]], ['regime', [1,6,4,3,2,5]], ['salinidade', [1,2]] ]
 VerificarAtributos(layer, teste)
 campo = 'nome'
 VerificarCartaImpress(layer, campo)
  # verificar condicao
 teste = [['tipomassadagua', [5,3]], ['salinidade',[2]]]
 VerificarSeEntao(layer, teste)

# hid_quebramar_molhe_a
camada = 'hid_quebramar_molhe_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['matconstr', [99,1,26,4,23,3,7,6,5,8,25,2]], ['tipoquebramolhe', [1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['matconstr', 'nome']
 VerificaOutros(layer, teste)

# hid_quebramar_molhe_l
camada = 'hid_quebramar_molhe_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['matconstr', [99,1,26,4,23,3,7,6,5,8,25,2]], ['tipoquebramolhe', [1,2]] ]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['matconstr', 'nome']
 VerificaOutros(layer, teste)

# hid_queda_dagua_a
camada = 'hid_queda_dagua_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoqueda', [1,2,3]] ]
 VerificarAtributos(layer, teste)

# hid_queda_dagua_l
camada = 'hid_queda_dagua_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoqueda', [1,2,3]] ]
 VerificarAtributos(layer, teste)

# hid_queda_dagua_p
camada = 'hid_queda_dagua_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoqueda', [1,2,3]] ]
 VerificarAtributos(layer, teste)

# hid_recife_a
camada = 'hid_recife_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situamare', [7,8,9]] ]
 VerificarAtributos(layer, teste)

# hid_recife_l
camada = 'hid_recife_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situamare', [7,8,9]] ]
 VerificarAtributos(layer, teste)

# hid_recife_p
camada = 'hid_recife_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situamare', [7,8,9]] ]
 VerificarAtributos(layer, teste)

# hid_rocha_em_agua_a
camada = 'hid_rocha_em_agua_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# hid_rocha_em_agua_p
camada = 'hid_rocha_em_agua_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# hid_sumidouro_vertedouro_p
camada = 'hid_sumidouro_vertedouro_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tiposumvert', [1,2]], ['causa',[1,2,3]]]
 VerificarAtributos(layer, teste)

# hid_terreno_suj_inundacao_a
camada = 'hid_terreno_suj_inundacao_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# hid_trecho_drenagem_l
camada = 'hid_trecho_drenagem_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 2], ['coincidecomdentrode', 97,'geometriaaproximada', 1], ['coincidecomdentrode', 97,'eixoprincipal', 1], ['coincidecomdentrode', 97,'navegabilidade', 2], ['coincidecomdentrode', 97,'regime', 5], ['dentrodepoligono', 1,'geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['eixoprincipal', [1,2]], ['regime', [1,6,4,3,2,5]], ['compartilhado', [1,2]], ['coincidecomdentrode',[10,14,2,9,11,19,15,1,97,12,13,16]], ['dentrodepoligono', [1,2]] ]
 VerificarAtributos(layer, teste)
# campo = 'nome'
# VerificarCartaImpress(layer, campo)
 # verificar condicao
 teste = [['coincidecomdentrode', [1]], ['navegabilidade',[0]]]
 VerificarSeEntao(layer, teste)
 teste = [['coincidecomdentrode', [97]], ['navegabilidade',[2]]]
 VerificarSeEntao(layer, teste)
 teste = [['coincidecomdentrode', [1]], ['regime',[1,3,5]]]
 VerificarSeEntao(layer, teste)
 teste = [['coincidecomdentrode', [97]], ['regime',[5]]]
 VerificarSeEntao(layer, teste)

# hid_trecho_massa_dagua_a
camada = 'hid_trecho_massa_dagua_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipotrechomassa', [2,1,99,9,10]], ['regime', [1,6,4,3,2,5]], ['salinidade', [1,2]] ]
 VerificarAtributos(layer, teste)
 campo = 'nome'
 VerificarCartaImpress(layer, campo)
 # Verificar Outros
 teste = ['tipotrechomassa', 'nome']
 VerificaOutros(layer, teste)


progress.setInfo('<b>7. LIMITES...</b><br/>')

# lim_area_de_litigio_a
camada = 'lim_area_de_litigio_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string'], ['descricao','string'] ]
 VerificarAtributos(layer, teste)

# lim_area_uso_comunitario_a
camada = 'lim_area_de_litigio_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string'], ['tipoareausocomun',[1,2]] ]
 VerificarAtributos(layer, teste)

# lim_area_uso_comunitario_p
camada = 'lim_area_de_litigio_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string'], ['tipoareausocomun',[1,2]] ]
 VerificarAtributos(layer, teste)

# lim_bairro_a
camada = 'lim_bairro_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string']]
 VerificarAtributos(layer, teste)

# lim_delimitacao_fisica_l
camada = 'lim_delimitacao_fisica_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr',97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipodelimfis',[1,2]] ]
 VerificarAtributos(layer, teste)

# lim_distrito_a
camada = 'lim_distrito_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string'],['geocodigo','string']]
 VerificarAtributos(layer, teste)

# lim_marco_de_limite_p
camada = 'lim_marco_de_limite_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 2]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string'],['tipomarcolim',[1,2,3,99]]]
 VerificarAtributos(layer, teste)

# lim_regiao_administrativa_a
camada = 'lim_regiao_administrativa_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string']]
 VerificarAtributos(layer, teste)

# lim_sub_distrito_a
camada = 'lim_sub_distrito_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string'],['geocodigo','string']]
 VerificarAtributos(layer, teste)

# lim_terra_indigena_a
camada = 'lim_terra_indigena_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string'],['nometi','string']]
 VerificarAtributos(layer, teste)

# lim_terra_indigena_p
camada = 'lim_terra_indigena_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string'],['nometi','string']]
 VerificarAtributos(layer, teste)

# lim_unidade_conserv_nao_snuc_a
camada = 'lim_unidade_conserv_nao_snuc_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string']]
 VerificarAtributos(layer, teste)

# lim_unidade_protecao_integral_a
camada = 'lim_unidade_protecao_integral_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string']]
 VerificarAtributos(layer, teste)

# lim_unidade_protecao_integral_p
camada = 'lim_unidade_protecao_integral_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string']]
 VerificarAtributos(layer, teste)

# lim_unidade_uso_sustentavel_a
camada = 'lim_unidade_uso_sustentavel_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string']]
 VerificarAtributos(layer, teste)

# lim_unidade_uso_sustentavel_p
camada = 'lim_unidade_uso_sustentavel_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string']]
 VerificarAtributos(layer, teste)


progress.setInfo('<b>8. LOCALIDADES...</b><br/>')

# loc_aglom_rural_de_ext_urbana_p
camada = 'loc_aglom_rural_de_ext_urbana_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string']]
 VerificarAtributos(layer, teste)

# loc_aglomerado_rural_isolado_p
camada = 'loc_aglom_rural_de_ext_urbana_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string'], ['tipoaglomrurisol',[7,5,6]]]
 VerificarAtributos(layer, teste)

# loc_area_edificada_a
camada = 'loc_area_edificada_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# loc_area_habitacional_a
camada = 'loc_area_habitacional_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# loc_area_urbana_isolada_a
camada = 'loc_area_urbana_isolada_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string'], ['tipoassociado',[1,4]]]
 VerificarAtributos(layer, teste)

# loc_capital_p
camada = 'loc_capital_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string']]
 VerificarAtributos(layer, teste)

# loc_cidade_p
camada = 'loc_cidade_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome','string']]
 VerificarAtributos(layer, teste)

# loc_edif_habitacional_a
camada = 'loc_edif_habitacional_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]]]
 VerificarAtributos(layer, teste)

# loc_edif_habitacional_p
camada = 'loc_edif_habitacional_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]]]
 VerificarAtributos(layer, teste)

# loc_edificacao_a
camada = 'loc_edificacao_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]]]
 VerificarAtributos(layer, teste)

# loc_edificacao_p
camada = 'loc_edificacao_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]]]
 VerificarAtributos(layer, teste)

# loc_hab_indigena_a
camada = 'loc_hab_indigena_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['coletiva', [1,2]], ['isolada', [1,2]]]
 VerificarAtributos(layer, teste)

# loc_hab_indigena_p
camada = 'loc_hab_indigena_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['coletiva', [1,2]], ['isolada', [1,2]]]
 VerificarAtributos(layer, teste)

# loc_nome_local_p
camada = 'loc_nome_local_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string']]
 VerificarAtributos(layer, teste)
 
# loc_vila_p
camada = 'loc_nome_local_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string']]
 VerificarAtributos(layer, teste)


progress.setInfo('<b>9. PONTOS DE REFERENCIA...</b><br/>')

# pto_area_est_med_fenom_a
camada = 'pto_area_est_med_fenom_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# pto_edif_constr_est_med_fen_a
camada = 'pto_edif_constr_est_med_fen_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]]]
 VerificarAtributos(layer, teste)

# pto_edif_constr_est_med_fen_p
camada = 'pto_edif_constr_est_med_fen_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['operacional', [1,2]], ['situacaofisica', [1,2,3,4,5]]]
 VerificarAtributos(layer, teste)

# pto_pto_est_med_fenomenos_p
camada = 'pto_pto_est_med_fenomenos_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoptoestmed', [1,11,2,9,4,8,5,7,6,10,3,12]], ['orgaoenteresp', 'string']]
 VerificarAtributos(layer, teste)
 
# pto_pto_ref_geod_topo_p
camada = 'pto_pto_ref_geod_topo_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 2]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nomeabrev', 'string']]
 VerificarAtributos(layer, teste)
 

progress.setInfo('<b>10. RELEVO...</b><br/>')

# rel_alter_fisiog_antropica_a
camada = 'rel_alter_fisiog_antropica_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoalterantrop', [27,28,25,26,29,24]]]
 VerificarAtributos(layer, teste)

# rel_alter_fisiog_antropica_l
camada = 'rel_alter_fisiog_antropica_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoalterantrop', [27,28,25,26,29,24]]]
 VerificarAtributos(layer, teste)

# rel_curva_nivel_l
camada = 'rel_curva_nivel_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 2]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['depressao', [1,2]], ['indice', [1,2,3]], ['cota', (1,5000)]]
 VerificarAtributos(layer, teste)

# rel_dolina_a
camada = 'rel_dolina_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# rel_dolina_p
camada = 'rel_dolina_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 
# rel_duna_a
camada = 'rel_duna_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 
# rel_duna_p
camada = 'rel_duna_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 
# rel_elemento_fisiog_natural_a
camada = 'rel_elemento_fisiog_natural_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string']]
 VerificarAtributos(layer, teste)
 
# rel_elemento_fisiog_natural_l
camada = 'rel_elemento_fisiog_natural_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string']]
 VerificarAtributos(layer, teste)

# rel_elemento_fisiog_natural_p
camada = 'rel_elemento_fisiog_natural_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['nome', 'string']]
 VerificarAtributos(layer, teste)

# rel_gruta_caverna_p
camada = 'rel_gruta_caverna_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipogrutacaverna', [20,19]]]
 VerificarAtributos(layer, teste)

# rel_pico_p
camada = 'rel_pico_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# rel_ponto_cotado_altimetrico_p
camada = 'rel_ponto_cotado_altimetrico_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
  # forcar atributos
 forcado = [['cotacomprovada', 1, 'geometriaaproximada',2], ['cotacomprovada', 2, 'geometriaaproximada',1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['cota', (1,5000)]]
 VerificarAtributos(layer, teste)
 
# rel_rocha_a
camada = 'rel_rocha_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tiporocha', [21,23,22]]]
 VerificarAtributos(layer, teste)

# rel_rocha_p
camada = 'rel_rocha_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tiporocha', [21,23,22]]]
 VerificarAtributos(layer, teste)

# rel_terreno_exposto_a
camada = 'rel_terreno_exposto_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['causaexposicao', [4,5]]]
 VerificarAtributos(layer, teste)


progress.setInfo('<b>11. SAUDE E SERVICO SOCIAL...</b><br/>')

# sau_area_saude_a
camada = 'sau_area_saude_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 
# sau_area_servico_social_a
camada = 'sau_area_servico_social_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 
# sau_edif_saude_a
camada = 'sau_edif_saude_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['nivelatencao',[5,6,7]], ['tipoclassecnae', [35,16,32,21,28,7,8,19,13,18,17,10,12,27,34,30,24,11,9,6,15,5,26,14,25,99,33,4,98,1,20,2,23,22,31,29]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoclassecnae', 'nome']
 VerificaOutros(layer, teste)
 # Verificar condicao Misto
 teste = ['tipoclassecnae', 'nome']
 VerificaMisto(layer, teste)

# sau_edif_saude_P
camada = 'sau_edif_saude_P'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['nivelatencao',[5,6,7]], ['tipoclassecnae', [35,16,32,21,28,7,8,19,13,18,17,10,12,27,34,30,24,11,9,6,15,5,26,14,25,99,33,4,98,1,20,2,23,22,31,29]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoclassecnae', 'nome']
 VerificaOutros(layer, teste)
 # Verificar condicao Misto
 teste = ['tipoclassecnae', 'nome']
 VerificaMisto(layer, teste)
 
# sau_edif_servico_social_a
camada = 'sau_edif_servico_social_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoclassecnae', [35,16,32,21,28,7,8,19,13,18,17,10,12,27,34,30,24,11,9,6,15,5,26,14,25,99,33,4,98,1,20,2,23,22,31,29]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoclassecnae', 'nome']
 VerificaOutros(layer, teste)
 # Verificar condicao Misto
 teste = ['tipoclassecnae', 'nome']
 VerificaMisto(layer, teste)

# sau_edif_servico_social_P
camada = 'sau_edif_servico_social_P'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoclassecnae', [35,16,32,21,28,7,8,19,13,18,17,10,12,27,34,30,24,11,9,6,15,5,26,14,25,99,33,4,98,1,20,2,23,22,31,29]]]
 VerificarAtributos(layer, teste)
 # Verificar condicao Outros
 teste = ['tipoclassecnae', 'nome']
 VerificaOutros(layer, teste)
 # Verificar condicao Misto
 teste = ['tipoclassecnae', 'nome']
 VerificaMisto(layer, teste)


progress.setInfo('<b>12. TRANSPORTES...</b><br/>')

# tra_area_estrut_transporte_a
camada = 'tra_area_estrut_transporte_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 
 # tra_arruamento_l
camada = 'tra_arruamento_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['revestimento', 0], ['operacional', 0], ['situacaofisica', 0], ['trafego', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['canteirodivisorio', [1,2]]]
 VerificarAtributos(layer, teste)
 
# tra_atracadouro_a
camada = 'tra_atracadouro_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoatracad', [43,41,40,42,44,39,38]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_atracadouro_l
camada = 'tra_atracadouro_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoatracad', [43,41,40,42,44,39,38]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)
 
# tra_atracadouro_p
camada = 'tra_atracadouro_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipoatracad', [43,41,40,42,44,39,38]], ['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_caminho_aereo_l
camada = 'tra_caminho_aereo_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipousocaminhoaer', [21,22,98]], ['tipocaminhoaereo', [12,99]], ['operacional',[1,2]],['situacaofisica', [1,2,3,4,5]] ]
 VerificarAtributos(layer, teste)
 teste = ['tipousocaminhoaer', 'nome']
 VerificaMisto(layer, teste)
 teste = ['tipocaminhoaereo', 'nome']
 VerificaOutros(layer, teste)

# tra_condutor_hidrico_l
camada = 'tra_condutor_hidrico_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipotrechoduto', [1,2,3]], ['mattransp', [29,4,8,3,5,30,31,99,7,1,2,6,9]], ['operacional',[1,2]],['situacaofisica', [1,2,3,4,5]] ]
 VerificarAtributos(layer, teste)
 teste = ['mattransp', 'nome']
 VerificaOutros(layer, teste)

# tra_eclusa_a
camada = 'tra_eclusa_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]]]
 VerificarAtributos(layer, teste)

# tra_eclusa_l
camada = 'tra_eclusa_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]]]
 VerificarAtributos(layer, teste)

# tra_eclusa_p
camada = 'tra_eclusa_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]]]
 VerificarAtributos(layer, teste)

# tra_edif_constr_aeroportuaria_a
camada = 'tra_edif_constr_aeroportuaria_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifaero',[99,29,27,28,15,26]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['tipoedifaero', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_edif_constr_aeroportuaria_p
camada = 'tra_edif_constr_aeroportuaria_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifaero',[99,29,27,28,15,26]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['tipoedifaero', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_edif_constr_portuaria_a
camada = 'tra_edif_constr_portuaria_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifport',[34,99,32,37,15,36,27,35,33,26]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['tipoedifport', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_edif_constr_portuaria_p
camada = 'tra_edif_constr_portuaria_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifport',[34,99,32,37,15,36,27,35,33,26]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['tipoedifport', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_edif_metro_ferroviaria_a
camada = 'tra_edif_metro_ferroviaria_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['funcaoedifmetroferrov',[99,15,20,17,18,16,19]],['multimodal',[1,2]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['funcaoedifmetroferrov', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_edif_metro_ferroviaria_p
camada = 'tra_edif_metro_ferroviaria_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['funcaoedifmetroferrov',[99,15,20,17,18,16,19]],['multimodal',[1,2]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['funcaoedifmetroferrov', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_edif_rodoviaria_a
camada = 'tra_edif_rodoviaria_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifrod',[13,99,10,9,14,15,8,12]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['tipoedifrod', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_edif_rodoviaria_p
camada = 'tra_edif_rodoviaria_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]], ['tipoedifrod',[13,99,10,9,14,15,8,12]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['tipoedifrod', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_fundeadouro_a
camada = 'tra_fundeadouro_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['destinacaofundeadouro',[99,12,11,13,10]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['destinacaofundeadouro', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_fundeadouro_l
camada = 'tra_fundeadouro_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['destinacaofundeadouro',[99,12,11,13,10]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['destinacaofundeadouro', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_fundeadouro_p
camada = 'tra_fundeadouro_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['destinacaofundeadouro',[99,12,11,13,10]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['destinacaofundeadouro', 'nome']
 VerificaOutros(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_funicular_l
camada = 'tra_funicular_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]]]
 VerificarAtributos(layer, teste)

# tra_funicular_p
camada = 'tra_funicular_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]]]
 VerificarAtributos(layer, teste)

# tra_galeria_bueiro_l
camada = 'tra_galeria_bueiro_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)

# tra_galeria_bueiro_p
camada = 'tra_galeria_bueiro_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)

# tra_girador_ferroviario_p
camada = 'tra_girador_ferroviario_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]], ['operacional',[1,2]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_identific_trecho_rod_p
camada = 'tra_identific_trecho_rod_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # verificar atributos
 teste = [['sigla', 'string']]
 VerificarAtributos(layer, teste)

# tra_passag_elevada_viaduto_l
camada = 'tra_passag_elevada_viaduto_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['tipopassagviad',[6,5]],['modaluso',[14,9,5,98,7,8,4,6]], ['matconstr',[99,1,26,4,23,3,7,6,5,8,25,2]], ['nrpistas',(1,6)], ['nrfaixas', (1,10)], ['posicaopista', [12,13,97]], ['largura', (1,100)]]
 VerificarAtributos(layer, teste)
 teste = ['modaluso', 'nome']
 VerificaMisto(layer, teste)
 teste = ['matconstr', 'nome']
 VerificaOutros(layer, teste)

# tra_passag_elevada_viaduto_p
camada = 'tra_passag_elevada_viaduto_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['tipopassagviad',[6,5]],['modaluso',[14,9,5,98,7,8,4,6]], ['matconstr',[99,1,26,4,23,3,7,6,5,8,25,2]], ['nrpistas',(1,6)], ['nrfaixas', (1,10)], ['posicaopista', [12,13,97]], ['largura', (1,100)]]
 VerificarAtributos(layer, teste)
 teste = ['modaluso', 'nome']
 VerificaMisto(layer, teste)
 teste = ['matconstr', 'nome']
 VerificaOutros(layer, teste)

# tra_passagem_nivel_p
camada = 'tra_passagem_nivel_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# tra_patio_a
camada = 'tra_patio_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]],['modaluso',[14,9,5,98,7,8,4,6]]]
 VerificarAtributos(layer, teste)
 teste = ['modaluso', 'nome']
 VerificaMisto(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_patio_p
camada = 'tra_patio_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]],['modaluso',[14,9,5,98,7,8,4,6]]]
 VerificarAtributos(layer, teste)
 teste = ['modaluso', 'nome']
 VerificaMisto(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_pista_ponto_pouso_a
camada = 'tra_pista_ponto_pouso_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['tipopista',[98,99,9,11,10]], ['revestimento', [4,1,2,3]], ['usopista', [12,11,13,6]]]
 VerificarAtributos(layer, teste)
 teste = ['tipopista', 'nome']
 VerificaMisto(layer, teste)
 teste = ['tipopista', 'nome']
 VerificaOutros(layer, teste)

# tra_pista_ponto_pouso_l
camada = 'tra_pista_ponto_pouso_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['tipopista',[98,99,9,11,10]], ['revestimento', [4,1,2,3]], ['usopista', [12,11,13,6]]]
 VerificarAtributos(layer, teste)
 teste = ['tipopista', 'nome']
 VerificaMisto(layer, teste)
 teste = ['tipopista', 'nome']
 VerificaOutros(layer, teste)

# tra_pista_ponto_pouso_p
camada = 'tra_pista_ponto_pouso_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['tipopista',[98,99,9,11,10]], ['revestimento', [4,1,2,3]], ['usopista', [12,11,13,6]]]
 VerificarAtributos(layer, teste)
 teste = ['tipopista', 'nome']
 VerificaMisto(layer, teste)
 teste = ['tipopista', 'nome']
 VerificaOutros(layer, teste)

# tra_ponte_l
camada = 'tra_ponte_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['tipoponte',[1,2,3]],['modaluso',[14,9,5,98,7,8,4,6]], ['matconstr',[99,1,26,4,23,3,7,6,5,8,25,2]], ['nrpistas',(1,6)], ['nrfaixas', (1,10)], ['posicaopista', [12,13,97]], ['largura', (1,100)]]
 VerificarAtributos(layer, teste)
 teste = ['modaluso', 'nome']
 VerificaMisto(layer, teste)
 teste = ['matconstr', 'nome']
 VerificaOutros(layer, teste)

# tra_ponte_p
camada = 'tra_ponte_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['tipoponte',[1,2,3]],['modaluso',[14,9,5,98,7,8,4,6]], ['matconstr',[99,1,26,4,23,3,7,6,5,8,25,2]], ['nrpistas',(1,6)], ['nrfaixas', (1,10)], ['posicaopista', [12,13,97]], ['largura', (1,100)]]
 VerificarAtributos(layer, teste)
 teste = ['modaluso', 'nome']
 VerificaMisto(layer, teste)
 teste = ['matconstr', 'nome']
 VerificaOutros(layer, teste)

# tra_posto_combustivel_a
camada = 'tra_posto_combustivel_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_posto_combustivel_p
camada = 'tra_posto_combustivel_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr', 0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['administracao',[15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_sinalizacao_p
camada = 'tra_sinalizacao_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]],['tiposinal',[5,6,2,1,4,3]]]
 VerificarAtributos(layer, teste)

# tra_travessia_l
camada = 'tra_travessia_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipotravessia', [1,2,3,4]]]
 VerificarAtributos(layer, teste)

# tra_travessia_p
camada = 'tra_travessia_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipotravessia', [1,2,3,4]]]
 VerificarAtributos(layer, teste)

# tra_travessia_pedestre_l
camada = 'tra_travessia_pedestre_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipotravessiaped', [7,8,9]],['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]]]
 VerificarAtributos(layer, teste)

# tra_travessia_pedestre_p
camada = 'tra_travessia_pedestre_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipotravessiaped', [7,8,9]],['situacaofisica', [1,2,3,4,5]],['operacional',[1,2]]]
 VerificarAtributos(layer, teste)

# tra_trecho_duto_l
camada = 'tra_trecho_duto_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1],  ['matconstr',0], ['ndutos', None]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipotrechoduto', [1,2,3]], ['mattransp', [29,4,8,3,5,30,31,99,7,1,2,6,9]], ['operacional',[1,2]],['situacaofisica', [1,2,3,4,5]] ]
 VerificarAtributos(layer, teste)
 teste = ['mattransp', 'nome']
 VerificaOutros(layer, teste)

# tra_trecho_ferroviario_l
camada = 'tra_trecho_ferroviario_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['codtrechoferrov','string'], ['posicaorelativa', [5,3,2,4,6]], ['tipotrechoferrov',[7,8,5]], ['operacional',[1,2]],['situacaofisica', [1,2,3,4,5]], ['nrlinhas', (1,50)], ['eletrificada', [1,2]], ['jurisdicao', [9,3,11,12,10,1,2,6,8]], ['administracao', [15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarAtributos(layer, teste)
 teste = ['administracao', 'nome']
 VerificaMisto(layer, teste)

# tra_trecho_hidroviario_l
camada = 'tra_trecho_hidroviario_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['regime',[1,6,4,3,2]], ['extensaotrecho', (1,1e7)], ['caladomaxseca',(1,1000)], ['operacional',[1,2]],['situacaofisica', [1,2,3,4,5]]]
 VerificarAtributos(layer, teste)

# tra_trecho_rodoviario_l
camada = 'tra_trecho_rodoviario_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['revestimento', [4,1,2,3]], ['tipotrechorod',[4,2,1,3]], ['operacional',[1,2]],['situacaofisica', [1,2,3,4,5]], ['nrpistas', (1,10)], ['nrfaixas', (1,8)], ['trafego',[1,2]], ['canteirodivisorio',[1,2]]]
 VerificarAtributos(layer, teste)
 # Teste de Obrigacao de atributos relativos
 teste = ['administracao', 'codtrechorodov', [1,2]]
 VerificarAtributosCond(layer, teste)
 # Verificar Condicao
 teste = [['tipotrechorod', [3]], ['jurisdicao',[0,8]]]
 VerificarSeEntao(layer, teste)
 teste = [['tipotrechorod', [2,4]], ['jurisdicao',[9,3,11,12,10,1,2,6]]]
 VerificarSeEntao(layer, teste)
 teste = [['tipotrechorod', [1]], ['jurisdicao',[8,9,3,11,12,10,1,2,6]]]
 VerificarSeEntao(layer, teste)
 teste = [['tipotrechorod', [3]], ['administracao',[0,6]]]
 VerificarSeEntao(layer, teste)
 teste = [['tipotrechorod', [2,4]], ['administracao',[15,12,3,11,5,2,98,10,4,1,7,9]]]
 VerificarSeEntao(layer, teste)
 teste = [['tipotrechorod', [1]], ['administracao', [15,12,3,11,5,2,98,6,10,4,1,7,9]]]
 VerificarSeEntao(layer, teste)
 teste = [['tipotrechorod', [3]], ['nrpistas',[1]]]
 VerificarSeEntao(layer, teste)
 teste = [['tipotrechorod', [3]], ['nrfaixas',[1]]]
 VerificarSeEntao(layer, teste)
 teste = [['tipotrechorod', [3]], ['revestimento',[1]]]
 VerificarSeEntao(layer, teste)

# tra_trilha_picada_l
camada = 'tra_trilha_picada_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)

# tra_tunel_l
camada = 'tra_tunel_l'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr',97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipotunel', [1,2]], ['modaluso', [14,9,5,98,7,8,4,6]], ['operacional',[1,2]],['situacaofisica', [1,2,3,4,5]], ['nrpistas', (1,8)], ['nrfaixas',(1,10)],['posicaopista',[12,13,97]] ]
 VerificarAtributos(layer, teste)
 teste = ['modaluso', 'nome']
 VerificaMisto(layer, teste)

# tra_tunel_p
camada = 'tra_tunel_p'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1], ['matconstr',97]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipotunel', [1,2]], ['modaluso', [14,9,5,98,7,8,4,6]], ['operacional',[1,2]],['situacaofisica', [1,2,3,4,5]], ['nrpistas', (1,8)], ['nrfaixas',(1,10)],['posicaopista',[12,13,97]] ]
 VerificarAtributos(layer, teste)
 teste = ['modaluso', 'nome']
 VerificaMisto(layer, teste) 

progress.setInfo('<b>13. VEGETACAO...</b><br/><br/>')

# veg_brejo_pantano_a
camada = 'veg_brejo_pantano_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['classificacaoporte', [1,98,2,3]]]
 VerificarAtributos(layer, teste)

# veg_caatinga_a
camada = 'veg_caatinga_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['classificacaoporte', [1,98,2,3]]]
 VerificarAtributos(layer, teste)

# veg_campinarana_a
camada = 'veg_campinarana_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['classificacaoporte', [1,98,2,3]]]
 VerificarAtributos(layer, teste)

# veg_campo_a
camada = 'veg_campo_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1],['tipocampo',0]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['ocorrenciaem',[14,7,5,13,8,19,6,15]]]
 VerificarAtributos(layer, teste)

# veg_cerrado_cerradao_a
camada = 'veg_cerrado_cerradao_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipocerr', [1,2]], ['classificacaoporte', [1,98,2,3]]]
 VerificarAtributos(layer, teste)

# veg_estepe_a -> vegetacao nao prevista

# veg_floresta_a
camada = 'veg_floresta_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['caracteristicafloresta', [1,2,3]], ['classificacaoporte', [1,98,2,3]]]
 VerificarAtributos(layer, teste)
 teste = [['caracteristicafloresta', [2]], ['classificacaoporte',[98]]]
 VerificarSeEntao(layer, teste)
 teste = [['caracteristicafloresta', [1]], ['classificacaoporte',[1]]]
 VerificarSeEntao(layer, teste)
 

# veg_macega_chavascal_a
camada = 'veg_macega_chavascal_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['classificacaoporte', [1,98,2,3]]]
 VerificarAtributos(layer, teste)

# veg_mangue_a
camada = 'veg_mangue_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['classificacaoporte', [1,98,2,3]]]
 VerificarAtributos(layer, teste)

# veg_veg_cultivada_a
camada = 'veg_veg_cultivada_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['tipolavoura',[1,2,3]], ['classificacaoporte', [1,98,2,3]], ['finalidade_veg',[2,3,99,1]], ['terreno', [1,2,3]], ['cultivopredominante', [26,42,33,13,4,32,15,6,18,27,22,30,10,25,12,23,31,2,17,24,20,3,16,99,1,21,28,29,19,98,7,9,14,8,11]]]
 VerificarAtributos(layer, teste)
 teste = ['cultivopredominante', 'nome']
 VerificaMisto(layer, teste)
 teste = ['cultivopredominante', 'nome']
 VerificaOutros(layer, teste)
 teste = ['finalidade', 'nome']
 VerificaOutros(layer, teste)
 
# veg_veg_restinga_a
camada = 'veg_veg_restinga_a'
layerList = QgsMapLayerRegistry.instance().mapLayersByName(camada)
if layerList:
 layer = layerList[0]
 # forcar atributos
 forcado = [['geometriaaproximada', 1]]
 ForcarAtributos(SimNao, layer, forcado)
 # verificar atributos
 teste = [['classificacaoporte', [1,98,2,3]]]
 VerificarAtributos(layer, teste)

del writer

progress.setInfo('<b>Opera&ccedil;&atilde;o conclu&iacute;da com sucesso!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(8)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)