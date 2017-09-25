"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-03-13
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
##13. Relatorio da Revisao da Reambulacao=name
##LF2) Revisao=group
##Camada_de_observacoes=vector
##Campo_de_observacao=field Camada_de_observacoes
##Relatorio_CSV=output file
##MI=string Digite_o_MI_aqui
##Reambulador= string Digite_o_nome_do_reambulador_aqui

from qgis.utils import iface
from qgis.core import *
from qgis.gui import QgsMessageBar
from qgis.core import QgsMessageLog
import time

# Pegar caminho do arquivo
caminho = Relatorio_CSV
quebrado = (caminho.replace('/','\\')).split('\\')
tam = len(quebrado)-1
filename = quebrado[-1]+'.csv'
caminho = ''
for i in range(tam):
    caminho+=quebrado[i]+'\\'

# Contar numero de pontos, linhas e poligonos
progress.setInfo('<b>Etapa 1: </b><br/>Contagem de pontos, linhas e poligonos do Projeto.')
n_pnt = 0
n_lin = 0
n_pol = 0
n_class = 0 # numero de classes
layers = QgsMapLayerRegistry.instance().mapLayers()
for nome, layer in layers.iteritems():
    layer_source = (layer.dataProvider().dataSourceUri()).split('|')[0] # a camada de ganchos nao entra na contagem
    if layer.type()==0 and layer_source!=Camada_de_observacoes:# VectorLayer e nao eh a camada de ganchos
        # check the layer geometry type
        if layer.geometryType() == QGis.Point:
            if layer.featureCount()>0:
                n_pnt = n_pnt + layer.featureCount()
                n_class +=1
        if layer.geometryType() == QGis.Line:
            if layer.featureCount()>0:
                n_lin = n_lin + layer.featureCount()
                n_class +=1
        if layer.geometryType() == QGis.Polygon:
            if layer.featureCount()>0:
                n_pol = n_pol + layer.featureCount()
                n_class +=1

# Abrir camada de obsevacoes
progress.setInfo('<b>Etapa 2: </b><br/>Contagem de ganchos e tipos de ganchos.')
layer = processing.getObject(Camada_de_observacoes)
ganchos_total = layer.featureCount()

# Ajuda do sqlite3
import sqlite3
# criar lista de dados
dados = []
att_column = layer.pendingFields().fieldNameIndex(Campo_de_observacao) # parametro de entrada
for index, feature in enumerate(layer.getFeatures()):
    atributos = feature.attributes()
    atributo = (atributos[att_column]).replace('"'.decode('utf-8'),"'")
    dados = dados+[(index, atributo)]
# -*- coding: utf-8 -*-
conn = sqlite3.connect(caminho+"temporario.db")
cursor = conn.cursor()
cursor.execute(""" create table ganchos(
                                        id integer,
                                        gancho text)""")
for index, gancho in enumerate(dados):
    cursor.execute('insert into ganchos(id, gancho) values (?,?)', gancho)
conn.commit()
cursor.close()
conn.close()
# Consulta de Ganchos ordenados por sua quantidade
lista =[]
with sqlite3.connect(caminho+"temporario.db") as conn:
    for linha in conn.execute("""
    select gancho, count(*) as contagem
    from ganchos
    group by gancho
    order by contagem desc"""):
        lista = lista+[linha]
conn.close()
import os
os.remove(caminho+"temporario.db")  # deletar arquivo

# Construcao do arquivo CSV
progress.setInfo('<b>Etapa 3: </b><br/>Escrevendo arquivo CSV.')
arquivo = open(caminho+filename, "w")
# Contagem de erros
arquivo.write("RELATORIO DE REVISAO DA REAMBULACAO\n")
arquivo.write("MI: %s\n" %MI)
arquivo.write("Reambulador: %s\n" %Reambulador)
arquivo.write("Data-Hora: %s\n\n" %time.ctime())

arquivo.write("Quantidade de Feicoes:\n")
arquivo.write("Feicao|Quantidade\n")
arquivo.write("Pontos|%s\n" %str(n_pnt))
arquivo.write("Linhas|%s\n" %str(n_lin))
arquivo.write("Poligonos|%s\n\n" %str(n_pol))

arquivo.write("Qnt de Classes Instanciadas: %s\n\n" %str(n_class))

arquivo.write("Valores de Ganchos:\n")
arquivo.write("Total de Ganchos|%s\n" %str(ganchos_total))
arquivo.write("Qnt de Tipos de Ganchos|%s\n\n" %str(len(lista)))
arquivo.write("||Relatorio de tipos de problemas e quantidade de ocorrencias\n")
arquivo.write("|Ordem|Gancho|Quantidade\n")
for k in range(len(lista)):
    arquivo.write("|%d|%s|%d\n" %(k+1, (lista[k][0]).encode('utf-8'), lista[k][1]))

arquivo.close()
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(4)
iface.messageBar().pushMessage(u'Informacao', "Relatorio criado com sucesso", level=QgsMessageBar.INFO, duration=4)
