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
##LF07) Qualidade=group
##Camada_de_Pontos_de_Referencia=vector
##Cota_em_metros=field Camada_de_Pontos_de_Referencia
##MDE_Avaliado=raster
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
MDE = MDE_Avaliado


from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing
from numpy import sqrt, array, mean, std, mat
from math import ceil, floor

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
def Interpolar(X, Y, MDE, origem, resol_X, resol_Y, metodo, nulo):
    if metodo == 'nearest':
        linha = int(round((origem[1]-Y)/resol_Y - 0.5))
        coluna = int(round((X - origem[0])/resol_X - 0.5))
        if MDE[linha][coluna] != nulo:
            return float(MDE[linha][coluna])
        else:
            return nulo
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
        if (MDE[int(floor(I)):int(ceil(I))+1, int(floor(J)):int(ceil(J))+1] == nulo).sum() == 0:
            Z = (1-di)*(1-dj)*MDE[int(floor(I))][int(floor(J))] + (1-dj)*di*MDE[int(ceil(I))][int(floor(J))] + (1-di)*dj*MDE[int(floor(I))][int(ceil(J))] + di*dj*MDE[int(ceil(I))][int(ceil(J))]
            return float(Z)
        else:
            return nulo
    elif metodo == 'bicubic':
        nlin = len(MDE)
        ncol = len(MDE[0])
        I = (origem[1]-Y)/resol_Y - 0.5
        J = (X - origem[0])/resol_X - 0.5
        di = I - floor(I)
        dj = J - floor(J)
        I=int(floor(I))
        J=int(floor(J))
        if I<2:
            I=2
        if I>nlin-3:
            I=nlin-3
        if J<2:
            J=2
        if J>ncol-3:
            J=ncol-3
        if (MDE[I-1:I+3, J-1:J+3] == nulo).sum() == 0:
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
        else:
            return nulo
        
# Abrir camada de referencia
ref = processing.getObject(Camada_de_Pontos_de_Referencia)
# Verificar o tipo de campo para o valor da cota
numerico = False
for field in ref.pendingFields():
    if field.name() == Cota_em_metros:
        if field.typeName() in [u'Integer', u'Real', u'Double']:
            numerico = True

# Abrir camada raster de teste
import gdal
from osgeo import osr
image = gdal.Open(MDE)
band = image.GetRasterBand(1).ReadAsArray()
NULO = image.GetRasterBand(1).GetNoDataValue()
if NULO == None:
    NULO =-1e6
prj=image.GetProjection()
# Number of rows and columns
cols = image.RasterXSize # Number of columns
rows = image.RasterYSize # Number of rows
# Origem e resolucao da imagem
ulx, xres, xskew, uly, yskew, yres  = image.GetGeoTransform()
origem = (ulx, uly)
resol_X = abs(xres)
resol_Y = abs(yres)
lrx = ulx + (cols * xres)
lry = uly + (rows * yres)
bbox = [ulx, lrx, lry, uly]
image=None # Fechar imagem
teste = processing.getObject(MDE) # Para pegar nome da imagem

# Verificacoes
crs = QgsCoordinateReferenceSystem()
crs.createFromWkt(prj)
if crs != ref.crs() or ref.geometryType() != QGis.Point or not(numerico):
    iface.messageBar().pushMessage(u'Erro', "Problema(s) com os parametros de entrada.", level=QgsMessageBar.CRITICAL, duration=5) 
    progress.setInfo('<b><font  color="#ff0000">Erro nos parametros de entrada. Possiveis erros:</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 1. A camada de referencia e do tipo ponto.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 2. As camadas devem ter o mesmo SRC.</b><br/>')
    progress.setInfo('<b><font  color="#ff0000"> 3. O campo referente ao valor da cota deve ser do tipo numerico (em metros).</b><br/><br/>')
    time.sleep(8)
    iface.messageBar().pushMessage(u'Situacao', "Problema com os dados de entrada!", level=QgsMessageBar.WARNING, duration=8)

else:
    DISCREP = []
    total_nulos = 0
    # Para cada ponto
        # calcular a discrepancia em relacao ao MDE, caso nao haja pixel nulo
        # armazenar nas somas para gerar (media, desvPad, EMQ, max, min,). quantidade de pontos avaliados, qnt de pontos em pixel nulo
    for feat in ref.getFeatures():
        geom = feat.geometry()
        pnt = geom.asPoint()
        X = pnt.x()
        Y = pnt.y()
        if bbox[0]<X and bbox[1]>X and bbox[2]<Y and bbox[3]>Y:
            cotaRef = feat[Cota_em_metros]
            cotaTest = Interpolar(X, Y, band, origem, resol_X, resol_Y, metodo, NULO)
            if cotaTest != NULO:
                DISCREP += [cotaTest - cotaRef]
            else:
                total_nulos +=1
        
    # Gerar relatorio do metodo
    DISCREP= array(DISCREP)
    EMQ = sqrt((DISCREP*DISCREP).sum()/len(DISCREP))
    cont = 0
    RESULTADOS = {}
    for escala in Escalas:
        mudou = False
        for valor in valores[::-1]:
            EM = PEC[escala]['altim'][valor]['EM']
            EP = PEC[escala]['altim'][valor]['EP']
            if ((DISCREP<EM).sum()/float(len(DISCREP)))>0.9 and (EMQ < EP):
                RESULTADOS[escala] = valor
                mudou = True
        if not mudou:
            RESULTADOS[escala] = 'R'
    
    progress.setInfo('<b>Operacao concluida!</b><br/><br/>')
    progress.setInfo('<b>RESULTADOS:</b><br/>')
    progress.setInfo('<b>Media das Discrepancias: %.1f m</b><br/>' %DISCREP.mean())
    progress.setInfo('<b>Desvio-Padrao: %.1f m</b><br/><br/>' %DISCREP.std())
    progress.setInfo('<b>EMQ: %.1f m</b><br/><br/>' %EMQ)
    if Escalas:
        for escala in Escalas:
            progress.setInfo('<b>Escala 1:%s -> PEC: %s.</b><br/>' %(dicionario[escala], RESULTADOS[escala]))
    
    progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
    time.sleep(8)
    
    if Escalas:
        # Criacao do arquivo html com os resultados
        arq = open(Relatorio_para_escalas, 'w')
        texto = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta content="text/html; charset=ISO-8859-1"
 http-equiv="content-type">
  <title>ACUR&Aacute;CIA ABSOLUTA</title>
</head>
<body style="background-color: rgb(229, 233, 166);">
<div style="text-align: center;"><span style="font-weight: bold; text-decoration: underline;">ACUR&Aacute;CIA POSICIONAL ABSOLUTA</span><br>
</div>
<br>
<span style="font-weight: bold;">1. Camada de Pontos de Controle</span><br>
&nbsp;&nbsp;&nbsp; a. nome: %s<br>
&nbsp;&nbsp;&nbsp; b. total de pontos de controle: %d<br>
&nbsp;&nbsp;&nbsp; c. total de pontos sobre o MDE: %d<br>
<br>
<span style="font-weight: bold;">2. Modelo Digital de Eleva&ccedil;&atilde;o Avaliado</span><br>
&nbsp;&nbsp;&nbsp; a. nome: %s<br>
&nbsp;&nbsp;&nbsp; b. n&uacute;mero de pixels: %d<br>
&nbsp;&nbsp;&nbsp; c. n&uacute;mero de pixels nulos: %d<br>
<br>
<span style="font-weight: bold;">3. Relat&oacute;rio</span><br>
&nbsp;&nbsp;&nbsp; a. n&uacute;mero de pontos utilizados: %d<br>
&nbsp;&nbsp;&nbsp; b. n&uacute;mero de pontos&nbsp;pr&oacute;ximo/sobre pixel nulo: %d<br>
&nbsp;&nbsp;&nbsp; c. m&eacute;dia das discrep&acirc;ncias (tend&ecirc;ncia): %.2f m<br>
&nbsp;&nbsp;&nbsp; d. desvio-padr&atilde;o: %.2f m<br>
&nbsp;&nbsp;&nbsp; e. REMQ: %.2f m<br>
&nbsp;&nbsp;&nbsp; f. discrep&acirc;ncia m&aacute;xima: %.2f m<br>
&nbsp;&nbsp;&nbsp; g. discrep&acirc;ncia m&iacute;nima: %.2f m<br>
&nbsp;&nbsp;&nbsp; h. m&eacute;todo de interpola&ccedil;&atilde;o: %s<br>
<br>
<span style="font-weight: bold;">4. Acur&aacute;cia Posicional (</span><span style="font-weight: bold;">PEC-PCD)<br>
<br>
</span>
<meta name="qrichtext" content="1">
<meta http-equiv="Content-Type"
 content="text/html; charset=utf-8">
<style type="text/css">
p, li { white-space: pre-wrap; }
</style>
<table style="margin: 0px;" border="1" cellpadding="2"
 cellspacing="2">
  <tbody>
    <tr>''' %(ref.name(), ref.featureCount(), total_nulos+len(DISCREP), teste.name(), cols*rows, (band==NULO).sum(), len(DISCREP), total_nulos, DISCREP.mean(), DISCREP.std(), EMQ, DISCREP.max(),DISCREP.min(), metodo)

        for escala in Escalas:
            texto += '<td><p style="margin: 0px; text-indent: 0px;"><span style="font-weight: 600;">%s</span></p></td>'  %dicionario[escala]
        texto +='''
    </tr>
    <tr>'''
        for escala in Escalas:
            texto += '<td style="text-align: center;"><p style="margin: 0px; text-indent: 0px;">%s</p></td>'  %RESULTADOS[escala]
        texto +='''</tr>
  </tbody>
</table>
<br>
<hr>
<address><font size="+l">Leandro Fran&ccedil;a 2018<br>
Eng. Cart&oacute;grafo<br>
email: geoleandro.franca@gmail.com<br>
</font>
</address>
</body>
</html>'''
        arq.write(texto)
        arq.close()
    iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)

