"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2017-09-15
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
# Metodo dos Retangulos Equivalentes
##MRE - Metodo dos Retangulos Equivalentes=name
##LF7) Qualidade=group
##Camada_de_Referencia=vector
##Camada_de_Teste=vector
##Buffer_de_Relacionamento=number 30.0
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

# Abrir camadas
ref = processing.getObject(Camada_de_Referencia)
teste = processing.getObject(Camada_de_Teste)

# Verificacoes
# As duas camadas devem estar no mesmo SRC e estarem projetadas
# As duas camadas devem ser do tipo linha
crs1 = ref.crs()
crs2 = teste.crs()
distance = QgsDistanceArea()

# Funcao para Gerar Poligonos
def GeraPoligono(lin1, lin2):
    Pfim1 = lin1[-1]
    Pini2 = lin2[0]
    Pfim2 = lin2[-1]
    m1 = distance.measureLine(Pfim1, Pini2)
    m2 = distance.measureLine(Pfim1, Pfim2)
    if m1<m2:
        coord = [lin1+lin2+[lin1[0]]]
    else:
        coord = [lin1+lin2[::-1]+[lin1[0]]]
    return coord

if crs1 == crs2 and not(crs1.geographicFlag()) and ref.geometryType() == QGis.Line and teste.geometryType() == QGis.Line:
    # Colocar linhas e seus buffers em uma lista
    list_ref = []
    for feat in ref.getFeatures():
        geom = feat.geometry()
        if geom:
            lin = geom.asPolyline()
            if not (lin):
                lin = geom.asMultiPolyline()
            Buffer = geom.buffer(buf, 5)
            pol = Buffer.asPolygon()
            list_ref +=[(lin, pol)]

    list_teste = []
    for feat in teste.getFeatures():
        geom = feat.geometry()
        if geom:
            lin = geom.asPolyline()
            if not (lin):
                lin = geom.asMultiPolyline()[0]
            Buffer = geom.buffer(buf, 5)
            pol = Buffer.asPolygon()
            list_teste +=[(lin, pol)]

    # Relacionar Feicoes
    RELACOES = []
    tam = len(list_ref)
    for index, item_ref in enumerate(list_ref):
        lin_ref = QgsGeometry.fromPolyline(item_ref[0])
        buf_ref = QgsGeometry.fromPolygon(item_ref[1])
        min_area = 1e9
        relacao = []
        sentinela = False
        for item_teste in list_teste:
            lin_teste = QgsGeometry.fromPolyline(item_teste[0])
            buf_teste = QgsGeometry.fromPolygon(item_teste[1])
            if lin_ref.intersects(buf_teste):
                if lin_ref.within(buf_teste) and lin_teste.within(buf_ref):
                    Poligono = QgsGeometry.fromPolygon(GeraPoligono(item_ref[0], item_teste[0]))
                    Area = Poligono.area()
                    if Area < min_area:
                        sentinela = True
                        min_area = Area
                        relacao = [item_ref[0], item_teste[0]]
        if sentinela:
            RELACOES += [relacao]
        progress.setPercentage(int(((index+1)/float(tam))*100))

    # Aplicar o Metodo dos Retangulos Equivalentes
    
    # Criar poligonos
    POLIGONOS = []
    for item in RELACOES:
        lin1 = item[0]
        lin2 = item[1]
        POLIGONOS += [GeraPoligono(lin1, lin2)]
    
    # Calcular Discrepancias
    DISCREP = []
    for index, coord in enumerate(POLIGONOS):
        pol = QgsGeometry.fromPolygon(coord)
        S = pol.area()
        p = pol.length()/2.0
        x1 = (p-sqrt(p*p-4*S))/2.0
        DISCREP += [float(x1)]

    # Criar camada de Saida (Poligonos)
    fields = QgsFields()
    fields.append(QgsField("discrepanc", QVariant.Double))
    CRS = teste.crs()
    encoding = 'utf-8'
    formato = 'ESRI Shapefile'
    writer = QgsVectorFileWriter(Discrepancias, encoding, fields, QGis.WKBPolygon, CRS, formato)
    fet = QgsFeature()
    for index, coord in enumerate(POLIGONOS):
        fet.setGeometry(QgsGeometry.fromPolygon(coord))
        fet.setAttributes([DISCREP[index]])
        writer.addFeature(fet)
    del writer
    
    # Comprimento das Linhas de Referencia
    COMPR = []
    for relacao in RELACOES:
        geom = QgsGeometry.fromPolyline(relacao[0])
        compr = geom.length()
        COMPR += [compr]
        
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
    
    # Gerar relatorio do metodo
    DISCREP= array(DISCREP)
    COMPR = array(COMPR)
    EMQ = sqrt((DISCREP*DISCREP*COMPR).sum()/COMPR.sum())
    media_Pond =sum(DISCREP*COMPR)/sum(COMPR)
    RESULTADOS = {}
    for escala in Escalas:
        mudou = False
        for valor in valores[::-1]:
            EM = PEC[escala]['planim'][valor]['EM']
            EP = PEC[escala]['planim'][valor]['EP']
            if (sum((DISCREP<EM)*COMPR)/sum(COMPR))>0.9 and (EMQ < EP):
                RESULTADOS[escala] = valor
                mudou = True
        if not mudou:
            RESULTADOS[escala] = 'R'

    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<b>RESULTADOS:</b><br/>')
    progress.setInfo('<b>Media Ponderada das Discrepancias: %.1f m</b><br/>' %media_Pond)
    progress.setInfo('<b>Desvio-Padrao Ponderado: %.1f m</b><br/><br/>' %EMQ)
    if Escalas:
        for escala in Escalas:
            progress.setInfo('<b>Escala 1:%s -> PEC: %s.</b><br/>' %(dicionario[escala], RESULTADOS[escala]))
    
    progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(8)
    
    if Escalas:
        # Criacao do arquivo html com os resultados
        arq = open(Relatorio_para_escalas, 'w')
        texto = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta content="text/html; charset=ISO-8859-1"
 http-equiv="content-type">
  <title>MRE</title>
</head>
<body  bgcolor="#e5e9a6">
<div style="text-align: center;"><span
 style="font-weight: bold; text-decoration: underline;">M&Eacute;TODO
DOS
RET&Acirc;NGULOS EQUIVALENTES</span><br>
</div>
<br>
<span style="font-weight: bold;">1. Camada de
Refer&ecirc;ncia</span><br>
&nbsp;&nbsp;&nbsp; a. nome: %s<br>
&nbsp;&nbsp;&nbsp; b. total de fei&ccedil;&otilde;es: %d<br>
<br>
<span style="font-weight: bold;">2. Camada de Teste</span><br>
&nbsp;&nbsp;&nbsp; a. nome: %s<br>
&nbsp;&nbsp;&nbsp; b. total de fei&ccedil;&otilde;es: %d<br>
<br>
<span style="font-weight: bold;">3. Relat&oacute;rio</span><br>
&nbsp;&nbsp;&nbsp; a. n&uacute;mero de fei&ccedil;&otilde;es relacionadas: %d<br>
&nbsp;&nbsp;&nbsp; b. m&eacute;dia ponderada das discrep&acirc;ncias (m): %.1f<br>
&nbsp;&nbsp;&nbsp; c. desvio-padr&atilde;o ponderado (m): %.1f<br>
&nbsp;&nbsp;&nbsp; d. discrep&acirc;ncia m&aacute;xima: %.1f<br>
&nbsp;&nbsp;&nbsp; e. discrep&acirc;ncia m&iacute;nima: %.1f<br>
&nbsp;&nbsp;&nbsp; f. <span style="font-weight: bold;">PEC-PCD</span>:<br>''' %(ref.name(), ref.featureCount(), teste.name(), teste.featureCount(), len(RELACOES), media_Pond, EMQ, max(DISCREP),min(DISCREP))
        texto += '''<table style="text-align: left; width: 100%;" border="1"
 cellpadding="2" cellspacing="2">
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
<br>
<hr>
<address><font size="+l">Leandro Fran&ccedil;a
2017<br>
Eng. Cart&oacute;grafo<br>
email: geoleandro.franca@gmail.com<br>
</font>
</address>
</body>
</html>'''
        arq.write(texto)
        arq.close()
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
else:
    progress.setInfo('<b><font  color="#ff0000">Erro nos parametros de entrada. Possiveis erros:</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 1. As camadas devem ser do tipo linha.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 2. As camadas devem ter SRC compat&iacute;veis.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 3. As camadas devem estar com SRC projetado (metros).</b><br/><br/>')
    iface.messageBar().pushMessage(u'Situacao', "Problema com os dados de entrada!", level=QgsMessageBar.WARNING, duration=8)
