"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-06-08
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
# Atualizar Ortografia
##04. Atualizar Ortografia=name
##LF2) Revisao=group
##Arquivo_CSV_corrigido=file

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time

FileCSV = Arquivo_CSV_corrigido
FileIndice =  FileCSV[:-4] +'.indice'

# Funcao para ler arquivo csv
def abrirCSV(filename, separador):
    arquivo = open(filename,"r")
    lista =[]
    for linha in arquivo.readlines():
        recorte = linha.split(separador)
        # Sumir com o "\n"
        ultimo = recorte[-1].rstrip("\n")
        recorte[-1]=ultimo
        lista = lista+[recorte]
    arquivo.close()
    return lista

# Ler arquivos CSV e .indice
CSV = abrirCSV(FileCSV, ';')
INDICE = abrirCSV(FileIndice, ';')

# Identificar a classe na lista de camadas pelo seu nome
ind_class = []
tam = len(INDICE)
for ind in range(tam):
    if INDICE[ind][0] == 'Classe:':
        ind_class += [ind]

ind = 1
ind_campo = []
lista = []
while ind < tam:
    if ind not in ind_class:
        lista += [ind]
        ind +=2
    else:
        ind +=1
        mudou = True
        ind_campo += [lista]
        lista = []
ind_campo += [lista]

s = 0
for k, ind in enumerate(ind_class):
    nome = INDICE[ind][1]
    layerList = QgsMapLayerRegistry.instance().mapLayersByName(nome)
    layer = layerList[0]
    DP = layer.dataProvider()
    # Para cada campo
    for ind2 in ind_campo[k]:
        campo = INDICE[ind2][1]
        att_column = layer.pendingFields().fieldNameIndex(campo)
        # Para cada ID alterar no BD o valor da string
        IDs = INDICE[ind2+1][1:]
        for t, ID in enumerate(IDs):
            atributo = (CSV[s][t+1]).decode('utf-8')
            newColumnValueMap = {att_column : atributo}
            newAttributesValuesMap = {int(ID) : newColumnValueMap}
            DP.changeAttributeValues(newAttributesValuesMap)
        s +=1
    progress.setPercentage(int(((k+1)/float(len(ind_class)))*100))


progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)