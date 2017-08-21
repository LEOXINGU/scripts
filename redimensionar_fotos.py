"""
/***************************************************************************
 3 CGEO
3th Brazilian Geoinformation Center
                              -------------------
        begin                : 2017-07-08
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
##6. Redimensionar Fotos=name
##Escolha_uma_pasta_de_imagens=optional folder
##Menor_lado=number 900
##LF3) GPS, Fotos e Midias=group

pasta = str(Escolha_uma_pasta_de_imagens)
lado = int(Menor_lado)
import os
os.chdir(pasta)
lista = os.listdir(pasta)
tam = len(lista)

import PIL.Image, PIL.ExifTags
import datetime
from qgis.core import *
import qgis.utils
from PyQt4.QtCore import *
from qgis.utils import iface
from qgis.gui import QgsMessageBar
import time


os.mkdir('Reduzido')
# Abrindo todas as imagens e redimensionando
for index, arquivo in enumerate(lista):
    if (arquivo[-3:]).lower() == 'jpg':
        img = PIL.Image.open(arquivo)
        exif = img.info['exif']
        altura = img.size[1]
        largura = img.size[0]
        if largura > altura:
            new_height = lado
            new_width =int(lado/float(altura)*largura)
        else:
            new_width = lado
            new_height =int(lado/float(largura)*altura)
        img = img.resize((new_width, new_height))
        img.save('Reduzido/'+ arquivo, exif=exif)
    progress.setPercentage(int((index/float(tam))*100))


progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(3)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=7)