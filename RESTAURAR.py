"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-04-11
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
# RESTAURAR
##1. RESTAURAR=name
##LF1) PostGIS=group
##Arquivo_SQL=file
##Host=string localhost
##Versao_do_PostgreSQL=selection 9.3;9.4;9.5;9.6

# Inputs
host = Host
lista = [9.3,9.4,9.5,9.6]
version = str(lista[Versao_do_PostgreSQL])

import os
from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import shutil

# Nome do arquivo e caminho
def file_path(caminho):
    quebrado = (caminho.replace('/','\\')).split('\\')
    tam = len(quebrado)-2
    filename = quebrado[-1]
    caminho = ''
    for i in range(tam):
        caminho+=quebrado[i]+'\\'
    caminho += quebrado[-2]
    return caminho, filename

# Copiar arquivo sql para um pasta no C:
saida = file_path(Arquivo_SQL)
if Arquivo_SQL[0] != 'C':
    shutil.copy2(Arquivo_SQL, 'C:/Users/Public/'+saida[1])
    path_name = 'C:/Users/Public/'+saida[1]
else:
    path_name = Arquivo_SQL

pasta = 'C:/Program Files/PostgreSQL/'+version+'/bin'
sentinela = False
if os.path.isdir(pasta):
    os.chdir(pasta)
    sentinela = True
else:
    pasta = 'C:\Program Files (x86)/PostgreSQL/'+version+'/bin'
    if os.path.isdir(pasta):
        os.chdir(pasta)
        sentinela = True
    else:
        progress.setInfo('<b>Problema(s) durante a execucao do backup.</b><br/>')
        iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do backup.", level=QgsMessageBar.CRITICAL, duration=5) 
        progress.setInfo('<b>Verifique se a versao do PostgreSQL foi definida corretamente.</b><br/>')
        time.sleep(8)

if sentinela:
    comando ='psql -d postgres -U postgres -h '+host+' -p 5432 -f '+path_name
    progress.setInfo('<b>Iniciando processo de Restauracao do BD...</b><br/>')
    result = os.system(comando)
    if result==0:
        progress.setInfo('<b>Operacao concluida com sucesso!</b><br/><br/>')
        iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 
        progress.setInfo('<b>3 CGEO</b><br/>')
        progress.setInfo('<b>Cap Leandro - Eng Cart</b><br/>')
        time.sleep(4)
    else:
        progress.setInfo('<b>Problema(s) durante a execucao do backup.</b><br/>')
        iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do backup.", level=QgsMessageBar.CRITICAL, duration=10) 
        progress.setInfo('<b>Verifique se os parametros foram definidos corretamente.</b><br/>')
        time.sleep(8)
if Arquivo_SQL[0] != 'C':
    os.remove(path_name)