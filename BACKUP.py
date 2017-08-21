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
# BACKUP
##2. BACKUP=name
##LF1) PostGIS=group
##Nome_do_BD=string
##Local_para_salvar_o_backup=folder
##Host=string localhost
##Versao_do_PostgreSQL=selection 9.5;9.3;9.4;9.6
##Renomear_BD_de_Saida=boolean False
##Novo_nome_para_BD_de_saida=optional string

# Inputs
database = str(Nome_do_BD)
local = str(Local_para_salvar_o_backup)
host = str(Host)
lista = [9.5,9.3,9.4,9.6]
version = str(lista[Versao_do_PostgreSQL])

import os
from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time

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

def ExecutarCmdo(database, host, local):
    comando = 'pg_dump -Fp -C -h ' +host+ ' -U postgres ' +database+ ' > ' +local+ '/'+database+'.sql'
    progress.setInfo('<b>Iniciando processo de backup...</b><br/>')
    result = os.system(comando)
    if result==0:
        progress.setInfo('<b>Operacao concluida com sucesso!</b><br/><br/>')
        progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
        time.sleep(4)
        iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5) 
    else:
        progress.setInfo('<b>Problema(s) durante a execucao do backup.</b><br/>')
        iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do backup.", level=QgsMessageBar.CRITICAL, duration=5) 
        progress.setInfo('<b>Verifique se os parametros foram definidos corretamente.</b><br/>')
        time.sleep(8)

if sentinela:
    if not Renomear_BD_de_Saida:
        ExecutarCmdo(database, host, local)
    else:
        import processing
        nome_antigo = database
        novo_nome = Novo_nome_para_BD_de_saida
        versao = Versao_do_PostgreSQL
        ok = processing.runalg('script:3renomearbd', nome_antigo, novo_nome, host, versao)
        database = novo_nome
        ExecutarCmdo(database, host, local)
        # Voltar para o nome antigo
        ok = processing.runalg('script:3renomearbd', novo_nome, nome_antigo, host, versao)
        