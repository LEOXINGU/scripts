"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-04-11
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
# RENOMEAR BD
##3. RENOMEAR BD=name
##LF01) PostGIS=group
##Nome_antigo=string
##Novo_nome=string
##Host=string localhost
##Versao_do_PostgreSQL=selection 10;9.3;9.4;9.5;9.6
##Usuario=string postgres

# Inputs
antigo = str(Nome_antigo)
novo = str(Novo_nome)
host = str(Host)
lista = [10,9.3,9.4,9.5,9.6]
version = str(lista[Versao_do_PostgreSQL])

import os
from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time

local = 'C:/Program Files/PostgreSQL/'+version+'/bin'
sentinela = False
if os.path.isdir(local):
    os.chdir(local)
    sentinela = True
else:
    local = 'C:\Program Files (x86)/PostgreSQL/'+version+'/bin'
    if os.path.isdir(local):
        os.chdir(local)
        sentinela = True
    else:
        progress.setInfo('<b>Problema(s) durante a execucao do backup.</b><br/>')
        progress.setInfo('<b>Verifique se a versao do PostgreSQL foi definida corretamente.</b><br/>')
        time.sleep(8)
        iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do comando.", level=QgsMessageBar.CRITICAL, duration=5) 

if sentinela:
    arquivo = open('C:/Users/Public/muda.sql','w')
    arquivo.write('ALTER DATABASE '+antigo+' RENAME TO '+novo)
    arquivo.close()
    comando = 'psql -d postgres -U '+Usuario+' -h '+host+' -p 5432 -f C:/Users/Public/muda.sql'
    progress.setInfo('<b>Renomeando o Banco de Dados...</b><br/>')
    result = os.system(comando)
    os.remove('C:/Users/Public/muda.sql')
    if result==0:
        progress.setInfo('<b>Operacao concluida com sucesso!</b><br/><br/>')
        progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
        time.sleep(4)
        iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 
    else:
        progress.setInfo('<b>Problema(s) durante a execucao do backup.</b><br/>')
        progress.setInfo('<b>Verifique se os parametros foram definidos corretamente.</b><br/>')
        time.sleep(8)
        iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do backup.", level=QgsMessageBar.CRITICAL, duration=10) 