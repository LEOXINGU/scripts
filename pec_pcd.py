"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-05-19
        copyright            : (C) 2018 by Leandro Franca - Cartographic Engineer
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
# Alimentar Camada com outra Camada
##PEC-PCD=name
##LF07) Qualidade=group
##Camada_de_Referencia=vector
##Camada_Avaliada=vector
##Buffer_de_Relacionamento=number 200.0
##Relatorio_para_escalas=output html
##Escala_1_1k=boolean False
##Escala_1_2k=boolean False
##Escala_1_5k=boolean False
##Escala_1_10k=boolean False
##Escala_1_25k=boolean True
##Escala_1_50k=boolean True
##Escala_1_100k=boolean True
##Escala_1_250k=boolean True
##Discrepancias=output vector

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing
from numpy import sqrt, array, mean, std

buf = Buffer_de_Relacionamento

# PEC-PCD
PEC = {'1k': {'planim': {'A': {'EM': 0.28, 'EP': 0.17},'B': {'EM': 0.5, 'EP': 0.3},'C': {'EM': 0.8, 'EP': 0.5},'D': {'EM': 1, 'EP': 0.6}}, 'altim': {'A': {'EM': 0.27, 'EP': 0.17},'B': {'EM': 0.5, 'EP': 0.33},'C': {'EM': 0.6, 'EP': 0.4},'D': {'EM': 0.75, 'EP': 0.5}}},
            '2k': {'planim': {'A': {'EM': 0.56, 'EP': 0.34},'B': {'EM': 1, 'EP': 0.6},'C': {'EM': 1.6, 'EP': 1},'D': {'EM': 2, 'EP': 1.2}}, 'altim': {'A': {'EM': 0.27, 'EP': 0.17},'B': {'EM': 0.5, 'EP': 0.33},'C': {'EM': 0.6, 'EP': 0.4},'D': {'EM': 0.75, 'EP': 0.5}}},
            '5k': {'planim': {'A': {'EM': 1.4, 'EP': 0.85},'B': {'EM': 2.5, 'EP': 1.5},'C': {'EM': 4, 'EP': 2.5},'D': {'EM': 5, 'EP': 3}}, 'altim': {'A': {'EM': 0.54, 'EP': 0.34},'B': {'EM': 1, 'EP': 0.67},'C': {'EM': 1.2, 'EP': 0.8},'D': {'EM': 1.5, 'EP': 1}}},
            '10k': {'planim': {'A': {'EM': 2.8, 'EP': 1.7},'B': {'EM': 5, 'EP': 3},'C': {'EM': 8, 'EP': 5},'D': {'EM': 10, 'EP': 6}}, 'altim': {'A': {'EM': 1.35, 'EP': 0.84},'B': {'EM': 2.5, 'EP': 1.67},'C': {'EM': 3, 'EP': 2},'D': {'EM': 3.75, 'EP': 2.5}}},
            '25k': {'planim': {'A': {'EM': 7, 'EP': 4.25},'B': {'EM': 12.5, 'EP': 7.5},'C': {'EM': 20, 'EP': 12.5},'D': {'EM': 25, 'EP': 15}}, 'altim': {'A': {'EM': 2.7, 'EP': 1.67},'B': {'EM': 5, 'EP': 3.33},'C': {'EM': 6, 'EP': 4},'D': {'EM': 7.5, 'EP': 5}}},
            '50k': {'planim': {'A': {'EM': 14, 'EP': 8.5},'B': {'EM': 25, 'EP': 15},'C': {'EM': 40, 'EP': 25},'D': {'EM': 50, 'EP': 30}}, 'altim': {'A': {'EM': 5.5, 'EP': 3.33},'B': {'EM': 10, 'EP': 6.67},'C': {'EM': 12, 'EP': 8},'D': {'EM': 15, 'EP': 10}}},
            '100k': {'planim': {'A': {'EM': 28, 'EP': 17},'B': {'EM': 50, 'EP': 30},'C': {'EM': 80, 'EP': 50},'D': {'EM': 100, 'EP': 60}}, 'altim': {'A': {'EM': 13.7, 'EP': 8.33},'B': {'EM': 25, 'EP': 16.67},'C': {'EM': 30, 'EP': 20},'D': {'EM': 37.5, 'EP': 25}}},
            '250k': {'planim': {'A': {'EM': 70, 'EP': 42.5},'B': {'EM': 125, 'EP': 75},'C': {'EM': 200, 'EP': 125},'D': {'EM': 250, 'EP': 150}}, 'altim': {'A': {'EM': 27, 'EP': 16.67},'B': {'EM': 50, 'EP': 33.33},'C': {'EM': 60, 'EP': 40},'D': {'EM': 75, 'EP': 50}}}}
dicionario = {'1k': '1:1.000', '2k': '1:2.000', '5k': '1:5.000', '10k': '1:10.000', '25k': '1:25.000', '50k': '1:50.000', '100k': '1:100.000', '250k': '1:250.000'}

# Escalas a serem avaliadas
Escalas = []
if Escala_1_1k:
    Escalas+=['1k']
if Escala_1_2k:
    Escalas+=['2k']
if Escala_1_5k:
    Escalas+=['5k']
if Escala_1_10k:
    Escalas+=['10k']
if Escala_1_25k:
    Escalas+=['25k']
if Escala_1_50k:
    Escalas+=['50k']
if Escala_1_100k:
    Escalas+=['100k']
if Escala_1_250k:
    Escalas+=['250k']

valores = ['A', 'B', 'C', 'D']

# Camada de Referencia
ref = processing.getObject(Camada_de_Referencia)
SRC_ref = ref.crs()

# Camada Avaliada
teste = processing.getObject(Camada_Avaliada)
SRC_teste = teste.crs()
distance = QgsDistanceArea()
distance.setSourceCrs(SRC_teste)

if SRC_ref == SRC_teste and not(SRC_teste.geographicFlag()) and ref.geometryType() == QGis.Point and teste.geometryType() == QGis.Point:
    # Colocar linhas e seus buffers em uma lista
    list_ref = []
    for feat in ref.getFeatures():
        geom = feat.geometry()
        if geom:
            pnt = geom.asPoint()
            if pnt:
                Buffer = geom.buffer(buf, 5)
                pol = Buffer.asPolygon()
                list_ref +=[(pnt, pol)]

    list_teste = []
    for feat in teste.getFeatures():
        geom = feat.geometry()
        if geom:
            pnt = geom.asPoint()
            if pnt:
                Buffer = geom.buffer(buf, 5)
                pol = Buffer.asPolygon()
                list_teste +=[(pnt, pol)]

    # Relacionar Feicoes
    RELACOES = []
    DISCREP = []
    DISCREP_X = []
    DISCREP_Y = []
    tam = len(list_ref)
    for index, item_ref in enumerate(list_ref):
        pnt_ref = QgsGeometry.fromPoint(item_ref[0])
        min_dist = 1e9
        relacao = []
        sentinela = False
        for item_teste in list_teste:
            buf_teste = QgsGeometry.fromPolygon(item_teste[1])
            if pnt_ref.intersects(buf_teste):
                Distancia = distance.measureLine(item_ref[0], item_teste[0])
                if Distancia < min_dist:
                    sentinela = True
                    min_dist = Distancia
                    relacao = [item_ref[0], item_teste[0]]
                    deltaX = item_teste[0].x() - item_ref[0].x()
                    deltaY = item_teste[0].y() - item_ref[0].y()
        if sentinela:
            RELACOES += [relacao]
            DISCREP += [min_dist]
            DISCREP_X += [deltaX]
            DISCREP_Y += [deltaY]
        progress.setPercentage(int(((index+1)/float(tam))*100))

    # Criar camada de Saida (linhas)
    fields = QgsFields()
    fields.append(QgsField("discrep_X", QVariant.Double))
    fields.append(QgsField("discrep_Y", QVariant.Double))
    fields.append(QgsField("distancia", QVariant.Double))
    CRS = teste.crs()
    encoding = 'utf-8'
    formato = 'ESRI Shapefile'
    writer = QgsVectorFileWriter(Discrepancias, encoding, fields, QGis.WKBLineString, CRS, formato)
    fet = QgsFeature()
    for index, coord in enumerate(RELACOES):
        fet.setGeometry(QgsGeometry.fromPolyline(coord))
        fet.setAttributes([DISCREP_X[index], DISCREP_Y[index], DISCREP[index]])
        writer.addFeature(fet)
    del writer

    # Gerar relatorio do metodo
    DISCREP= array(DISCREP)
    EMQ = sqrt((DISCREP*DISCREP).sum()/len(DISCREP))
    RESULTADOS = {}
    for escala in Escalas:
        mudou = False
        for valor in valores[::-1]:
            EM = PEC[escala]['planim'][valor]['EM']
            EP = PEC[escala]['planim'][valor]['EP']
            if (sum(DISCREP<EM)/len(DISCREP))>0.9 and (EMQ < EP):
                RESULTADOS[escala] = valor
                mudou = True
        if not mudou:
            RESULTADOS[escala] = 'R'

    DISCREP_X= array(DISCREP_X)
    DISCREP_Y= array(DISCREP_Y)
    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<b>RESULTADOS:</b><br/>')
    progress.setInfo('<b>EMQ: %.1f m</b><br/><br/>' %EMQ)
    progress.setInfo('<b>Media dos Erros em X: %.1f m</b><br/><br/>' %DISCREP_X.mean())
    progress.setInfo('<b>Desvio-Padrao dos Erros em X: %.1f m</b><br/><br/>' %DISCREP_X.std())
    progress.setInfo('<b>Media dos Erros em Y: %.1f m</b><br/><br/>' %DISCREP_Y.mean())
    progress.setInfo('<b>Desvio-Padrao dos Erros em Y: %.1f m</b><br/><br/>' %DISCREP_Y.std())
    
    progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(5)
    
    if Escalas:
        # Criacao do arquivo html com os resultados
        arq = open(Relatorio_para_escalas, 'w')
        texto = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta content="text/html; charset=ISO-8859-1"
 http-equiv="content-type">
  <title>ACUR&Aacute;CIA POSICIONAL</title>
  <meta name="qrichtext" content="1">
  <meta http-equiv="Content-Type"
 content="text/html; charset=utf-8">
  <style type="text/css">
p, li { white-space: pre-wrap; }
  </style>
</head>
<body style="background-color: rgb(229, 233, 166);">
<div style="text-align: center;"><span
 style="font-weight: bold; text-decoration: underline;">RELAT&Oacute;RIO DE ACUR&Aacute;CIA POSICIONAL</span><br>
</div>
<br>
<span style="font-weight: bold;">1. Camada de Pontos de Refer&ecirc;ncia</span><br>
&nbsp;&nbsp;&nbsp; a. nome: %s<br>
&nbsp;&nbsp;&nbsp; b. total de pontos: %d<br>
<br>
<span style="font-weight: bold;">2. Camada de Pontos Avaliados</span><br>
&nbsp;&nbsp;&nbsp; a. nome: %s<br>
&nbsp;&nbsp;&nbsp; b. total de pontos: %d<br>
<br>
<span style="font-weight: bold;">3. Relat&oacute;rio</span><br>
&nbsp;&nbsp;&nbsp; a.&nbsp;total de pares de pontos hom&oacute;logos: %d<br>
&nbsp;&nbsp;&nbsp; b. Discrep&acirc;ncias em X:<br>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; b.1. 
m&eacute;dia das discrep&acirc;ncias (tend&ecirc;ncia): %.2f m<br>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; b.2. 
desvio-padr&atilde;o (precis&atilde;o):&nbsp;%.2f m<br>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; b.3. 
discrep&acirc;ncia m&aacute;xima:&nbsp;%.2f m<br>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; b.4. 
discrep&acirc;ncia m&iacute;nima:&nbsp;%.2f m<br>
&nbsp;&nbsp;&nbsp; c. Discrep&acirc;ncias em Y:<br>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; c.1. 
m&eacute;dia das discrep&acirc;ncias
(tend&ecirc;ncia):&nbsp;%.2f m<br>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; c.2. 
desvio-padr&atilde;o (precis&atilde;o):&nbsp;%.2f m<br>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; c.3. 
discrep&acirc;ncia m&aacute;xima:&nbsp;%.2f m<br>
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; c.4. 
discrep&acirc;ncia m&iacute;nima:&nbsp;%.2f m<br>
&nbsp;&nbsp;&nbsp; d. REMQ:&nbsp;%.2f m<br>
&nbsp;&nbsp;&nbsp; e. dist&acirc;ncia m&aacute;xima:&nbsp;%.2f m<br>
&nbsp;&nbsp;&nbsp; f.&nbsp;dist&acirc;ncia m&iacute;nima:&nbsp;%.2f m<br>
<br>
<span style="font-weight: bold;">4. Acur&aacute;cia Posicional (</span><span style="font-weight: bold;">PEC-PCD)<br>
<br>
</span>''' %(ref.name(), ref.featureCount(), teste.name(), teste.featureCount(), len(RELACOES), DISCREP_X.mean(), DISCREP_X.std(), DISCREP_X.max(), DISCREP_X.min(), DISCREP_Y.mean(), DISCREP_Y.std(), DISCREP_Y.max(), DISCREP_Y.min(), EMQ, DISCREP.max(), DISCREP.min())
        texto += '''<table style="margin: 0px;" border="1" cellpadding="2"
 cellspacing="2">
  <tbody>
    <tr>'''
        for escala in Escalas:
            texto += '    <td style="text-align: center; font-weight: bold;">%s</td>' %dicionario[escala]
        
        texto +='''
        </tr>
        <tr>'''
        for escala in Escalas:
            texto += '    <td style="text-align: center;">%s</td>' %RESULTADOS[escala]
        
        texto +='''
    </tr>
  </tbody>
</table>
<br>
<hr>
<address><font size="+l">Leandro Fran&ccedil;a
2018<br>
Eng. Cart&oacute;grafo<br>
email: geoleandro.franca@gmail.com<br>
</font>
</address>
</body>
</html>
    '''    
        arq.write(texto)
        arq.close()
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
else:
    progress.setInfo('<b><font  color="#ff0000">Erro nos parametros de entrada. Possiveis erros:</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 1. As camadas devem ser do tipo ponto.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 2. As camadas devem ter SRC compat&iacute;veis.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 3. As camadas devem estar com SRC projetado (metros).</b><br/><br/>')
    iface.messageBar().pushMessage(u'Situacao', "Problema com os dados de entrada!", level=QgsMessageBar.WARNING, duration=8)