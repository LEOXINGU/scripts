


"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-10-04
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
# Transladar Vetor
##4. Transladar Vetor=name
##LF04) Vetor=group
##Entrada=vector
##Tipo_de_Deslocamento=selection Azimute e Distancia;Vetor XY
##Deslocamento=string
##Saida=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import processing
import time
from math import sin, cos, radians


# Validacao dos dados de entrada
problema = False
deslc = Deslocamento.replace('  ', ' ').replace(', ', ',').replace(' ', ',').split(',')

# Deve-ser ter 2 numeros para deslocamento
# Se for azimute e distancia, o angulo deve estar entre 0 e 360 graus
if len(deslc) ==2 and deslc[0].isdigit() and deslc[1].isdigit():
    if Tipo_de_Deslocamento == 0:
        if deslc[0]>360 and deslc[0]<0:
            problema = True
    deslc = [float(deslc[0]), float(deslc[1])]
    progress.setInfo('Parametros de entrada: %.2f e %.2f<br/>' %(deslc[0], deslc[1]))
    
else:
    problema = True

# Camada de entrada
layer = processing.getObject(Entrada)

# Transformacao de azimute para graus decimais
def azimuth2degrees(azimute):
    degrees = (450 - azimute)%360
    return degrees
    
# Criando vetor de deslocamento
if Tipo_de_Deslocamento == 0:
    graus = azimuth2degrees(deslc[0])
    vetor = [deslc[1]*cos(radians(graus)), deslc[1]*sin(radians(graus))]
elif Tipo_de_Deslocamento == 1:
    vetor = deslc
dx, dy, angle, scalex, scaley, anchorx, anchory = vetor[0], vetor[1], 0, 1, 1, 0, 0

# Execucao do processo
if problema:
    progress.setInfo('<b>Problema(s) durante a execucao do backup.</b><br/>')
    progress.setInfo('<b>Verifique se os parametros de deslocamento foram escritos corretamente.</b><br/>')
    time.sleep(8)
    iface.messageBar().pushMessage(u'Erro', "Problema(s) durante a execucao do comando.", level=QgsMessageBar.CRITICAL, duration=5)
else:
    output = processing.runalg('saga:transformshapes', layer, dx, dy, angle, scalex, scaley, anchorx, anchory, Saida)
    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(3)
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)