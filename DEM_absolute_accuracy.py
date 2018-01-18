"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-01-17
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
# Acuracia Absoluta de MDE
##Acuracia Absoluta de MDE=name
##LF7) Qualidade=group
##Camada_de_Pontos_de_Referencia=vector
##Cota_em_metros=field
##Camada_Raster_de_Teste=raster
##Tipo_de_Interpolacao=selection Bicubica;Bilinear;Vizinho Mais Proximo
##Relatorio_para_escalas=output html
##Escala_1_1k=boolean False
##Escala_1_2k=boolean False
##Escala_1_5k=boolean False
##Escala_1_10k=boolean False
##Escala_1_25k=boolean True
##Escala_1_50k=boolean True
##Escala_1_100k=boolean True
##Escala_1_250k=boolean True


interpolacao = ['bicubic', 'bilinear', 'nearest']
metodo = interpolacao[Tipo_de_Interpolacao]
MDE = Camada_Raster_de_Teste

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing
from numpy import sqrt, array, mean, std

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

# Funcao de Interpolacao
def Interpolar(X, Y, MDE, origem, resol_X, resol_Y, metodo):
    if metodo == 'nearest':
        linha = round((origem[1]-Y)/resol_Y - 0.5)
        coluna = round((X - origem[0])/resol_X - 0.5)
        return float(MDE[linha][coluna])
    elif metodo == 'bilinear':
        nlin = len(MDE)
        ncol = len(MDE[0])
        I = (origem[1]-Y)/resol_Y - 0.5
        J = (X - origem[0])/resol_X - 0.5
        di = I - floor(I)
        dj = J - floor(J)
        if I<0:
            I=0
        if I>nlin-1:
            I=nlin-1
        if J<0:
            J=0
        if J>ncol-1:
            J=ncol-1
        Z = (1-di)*(1-dj)*MDE[floor(I)][floor(J)] + (1-dj)*di*MDE[ceil(I)][floor(J)] + (1-di)*dj*MDE[floor(I)][ceil(J)] + di*dj*MDE[ceil(I)][ceil(J)]
        return float(Z)
    elif metodo == 'bicubic':
        nlin = len(MDE)
        ncol = len(MDE[0])
        I = (origem[1]-Y)/resol_Y - 0.5
        J = (X - origem[0])/resol_X - 0.5
        di = I - floor(I)
        dj = J - floor(J)
        I=floor(I)
        J=floor(J)
        if I<2:
            I=2
        if I>nlin-3:
            I=nlin-3
        if J<2:
            J=2
        if J>ncol-3:
            J=ncol-3
        MatrInv = (mat([[-1, 1, -1, 1], [0, 0, 0, 1], [1, 1, 1, 1], [8, 4, 2, 1]])).I # < Jogar para fora da funcao
        MAT  = mat([[MDE[I-1, J-1],   MDE[I-1, J],   MDE[I-1, J+1],  MDE[I-2, J+2]],
                             [MDE[I, J-1],      MDE[I, J],      MDE[I, J+1],      MDE[I, J+2]],
                             [MDE[I+1, J-1],  MDE[I+1, J], MDE[I+1, J+1], MDE[I+1, J+2]],
                             [MDE[I+2, J-1],  MDE[I+2, J], MDE[I+2, J+1], MDE[I+2, J+2]]])
        coef = MatrInv*MAT.transpose()
        # Horizontal
        pi = coef[0,:]*pow(dj,3)+coef[1,:]*pow(dj,2)+coef[2,:]*dj+coef[3,:]
        # Vertical
        coef2 = MatrInv*pi.transpose()
        pj = coef2[0]*pow(di,3)+coef2[1]*pow(di,2)+coef2[2]*di+coef2[3]
        return float(pj)
        
# Abrir camada de referencia
ref = processing.getObject(Camada_de_Pontos_de_Referencia)

# Abrir camada raster de teste
import gdal
from osgeo import osr
image = gdal.Open(MDE)
band = image.GetRasterBand(1).ReadAsArray()
prj=image.GetProjection()
geotransform = image.GetGeoTransform()
# Number of rows and columns
cols = image.RasterXSize # Number of columns
rows = image.RasterYSize # Number of rows
image=None # Close image
# Origem e resolucao da imagem
origem = (geotransform[0], geotransform[3])
resol_X = abs(geotransform[1])
resol_Y = abs(geotransform[5])

# Verificacoes
# As duas camadas devem ter o mesmo SRC
# Conferir CRS
crs = QgsCoordinateReferenceSystem()
crs.createFromWkt(prj)
# Verificar se as duas camadas tem o mesmo CRS e sao projetadas
if crs != ref.crs() or ref.geometryType() != QGis.Point:
    iface.messageBar().pushMessage(u'Erro', "Problema(s) com os parametros de entrada.", level=QgsMessageBar.CRITICAL, duration=5) 
    progress.setInfo('<b><font  color="#ff0000">Erro nos parametros de entrada. Possiveis erros:</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 1. A camada de referência é do tipo ponto.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 2. As camadas devem ter o mesmo SRC.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 3. O campo referente ao valor da cota deve ser do tipo numérico (em metros).</b><br/><br/>')
    time.sleep(8)
    iface.messageBar().pushMessage(u'Situacao', "Problema com os dados de entrada!", level=QgsMessageBar.WARNING, duration=8)

else:
    DISCREP = []    
    # Para cada ponto
        # determinar a cota Z
        # calcular a discrepância em relacao ao MDE, caso nao haja pixel nulo
        # armazenar nas somas para gerar (media, desvPad, EMQ, max, min, etc)
    
    
    for item in RELACOES:
        discrepItem = []
        for escala in Escalas:
            discrepEsc = []
            for valor in valores:
                buf = PEC[escala]['planim'][valor]['EM']
                lin1 = QgsGeometry.fromPolyline(item[0])
                lin2 = QgsGeometry.fromPolyline(item[1])
                buf1 = lin1.buffer(buf, 5)
                buf2 = lin2.buffer(buf, 5)
                Difer = buf1.difference(buf2)
                A_difer = Difer.area()
                AB_LT = buf2.area()
                dm = pi*buf*(A_difer/AB_LT)
                discrepEsc += [dm]
            discrepItem += discrepEsc
        DISCREP += [discrepItem]

    # Criar camada de Saida (Multilines)
    fields = QgsFields()
    for escala in Escalas:
        for valor in valores:
            nome = escala + '_PEC_' + valor
            fields.append(QgsField(nome, QVariant.Double))
    fields.append(QgsField('media', QVariant.Double))
    fields.append(QgsField('desPad', QVariant.Double))
    CRS = teste.crs()
    encoding = 'utf-8'
    formato = 'ESRI Shapefile'
    writer = QgsVectorFileWriter(Discrepancias, encoding, fields, QGis.WKBLineString, CRS, formato)
    fet = QgsFeature()
    for index, coord in enumerate(RELACOES):
        fet.setGeometry(QgsGeometry.fromMultiPolyline(coord))
        media = float((array(DISCREP[index])).mean())
        DP = float((array(DISCREP[index])).std())
        fet.setAttributes(DISCREP[index]+[media, DP])
        writer.addFeature(fet)
    del writer
    
    # Comprimento das Linhas de Referencia
    COMPR = []
    for relacao in RELACOES:
        geom = QgsGeometry.fromPolyline(relacao[0])
        compr = geom.length()
        COMPR += [compr]
    
    # Gerar relatorio do metodo
    DISCREP= array(DISCREP)
    DISCREP = DISCREP.transpose()
    COMPR = array(COMPR)
    cont = 0
    RESULTADOS = {}
    for escala in Escalas:
        mudou = False
        for valor in valores[::-1]:
            discrep = DISCREP[3-cont%4+4*cont/4]
            cont +=1
            EMQ = sqrt((discrep*discrep*COMPR).sum()/COMPR.sum())
            EM = PEC[escala]['planim'][valor]['EM']
            EP = PEC[escala]['planim'][valor]['EP']
            if (sum((discrep<EM)*COMPR)/sum(COMPR))>0.9 and (EMQ < EP):
                RESULTADOS[escala] = valor
                mudou = True
        if not mudou:
            RESULTADOS[escala] = 'R'
    
    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<b>RESULTADOS:</b><br/>')
    progress.setInfo('<b>Media das Discrepancias: %.1f m</b><br/>' %DISCREP.mean())
    progress.setInfo('<b>Desvio-Padrao: %.1f m</b><br/><br/>' %sqrt((DISCREP*DISCREP).sum()/(len(DISCREP)*len(DISCREP[0])-1)))
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
DO BUFFER DUPLO</span><br>
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
&nbsp;&nbsp;&nbsp; b. m&eacute;dia das discrep&acirc;ncias (m): %.1f<br>
&nbsp;&nbsp;&nbsp; c. desvio-padr&atilde;o (m): %.1f<br>
&nbsp;&nbsp;&nbsp; d. discrep&acirc;ncia m&aacute;xima: %.1f<br>
&nbsp;&nbsp;&nbsp; e. discrep&acirc;ncia m&iacute;nima: %.1f<br>
&nbsp;&nbsp;&nbsp; f. <span style="font-weight: bold;">PEC-PCD</span>:<br>''' %(ref.name(), ref.featureCount(), teste.name(), teste.featureCount(), len(RELACOES), DISCREP.mean(), sqrt((DISCREP*DISCREP).sum()/(len(DISCREP)*len(DISCREP[0])-1)), DISCREP.max(),DISCREP.min())
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

