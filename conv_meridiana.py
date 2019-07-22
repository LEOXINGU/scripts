"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-03-19
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
# Convergencia Meridiana
##3. Convergencia Meridiana=name
##LF10) Cartografia=group
##Moldura=vector
##Resultado=output html

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing
import math

moldura = processing.getObject(Moldura)
SRC = moldura.crs()

# Pegar centroide da moldura
features = moldura.getFeatures()
feat = features.next()
geom = feat.geometry()
centroide = geom.centroid().asPoint()

# Verificar os SRC da moldura
if not SRC.geographicFlag():
    # Transformar Coordenadas Projetadas do sistema UTM para geograficas
    crsDest = QgsCoordinateReferenceSystem()
    crsDest.createFromSrsId(4674)
    coordinateTransformer = QgsCoordinateTransform(SRC, crsDest)
    centroide = coordinateTransformer.transform(centroide)

# Pegar coordenadas do Centroide
lon = centroide.x()
lat = centroide.y()

# Calculo do Fuso
fuso = round((183+lon)/6.0)
# Calculo do Meridiano Central
MC = 6*fuso-183
# Fator de distorcao inicial
kappaZero = 0.9996
# Pegar Semi-eixo Maior e Menor do Datum da Moldura
distanceArea = QgsDistanceArea()
distanceArea.setEllipsoid(SRC.ellipsoidAcronym())
a = distanceArea.ellipsoidSemiMajor()
b = distanceArea.ellipsoidSemiMinor()

# Calcular fator de escala para sistema de projecao UTM
def FatorK(lon, lat):
    b = math.cos(math.radians(lat))*math.sin(math.radians(lon - MC))
    k = kappaZero/math.sqrt(1 - b*b)
    return k

# Calcular Convergencia Meridiana para sistema de projecao UTM
def ConvMer(lon, lat, a, b):
    delta_lon = abs( MC - lon )
    p = 0.0001*( delta_lon*3600 )
    xii = math.sin(math.radians(lat))*math.pow(10, 4)
    e2 = math.sqrt(a*a - b*b)/b
    c5 = math.pow(math.sin(math.radians(1/3600)), 4)*math.sin(math.radians(lat))*math.pow(math.cos(math.radians(lat)), 4)*(2 - math.pow(math.tan(math.radians(lat)), 2))*math.pow(10, 20)/15
    xiii = math.pow(math.sin(math.radians(1/3600)), 2)*math.sin(math.radians(lat))*math.pow(math.cos(math.radians(lat)), 2)*(1 + 3*e2*e2*math.pow(math.cos(math.radians(lat)), 2) + 2*math.pow(e2, 4)*math.pow(math.cos(math.radians(lat)), 4))*math.pow(10, 12)/3
    cSeconds = xii*p + xiii*math.pow(p, 3) + c5*math.pow(p, 5)
    c = cSeconds/3600
    return c

def dd2dms(dd):
    is_positive = dd >= 0
    dd = abs(dd)
    minutes,seconds = math.divmod(dd*3600,60)
    degrees,minutes = math.divmod(minutes,60)
    degrees = str(int(degrees)) if is_positive else '-' + str(int(degrees))
    minutes = int(minutes)
    return degrees + u"\u00b0" + str(minutes).zfill(2) + "'" + "%0.2f"%(seconds) + "''"

def dd2dmsHTML(degs):
    neg = degs < 0
    degs = (-1) ** neg * degs
    degs, d_int = math.modf(degs)
    mins, m_int = math.modf(60 * degs)
    secs        =           60 * mins
    if neg:
        return u'-%d&deg;%02d\'%02d"' %(int(d_int), int(m_int), int(secs))
    else:
        return u'+%d&deg;%02d\'%02d"' %(int(d_int), int(m_int), int(secs))

# Escrever Arquivo
if Resultado[-5:] != '.html':
    Resultado += '.html'

texto = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta content="text/html; charset=ISO-8859-1"
 http-equiv="content-type">
  <title></title>
</head>
<body style="background-color: rgb(229, 233, 166);">
<div style="text-align: center;"><big><big><big><span
 style="font-weight: bold;">RESULTADOS</span></big></big></big><br>
<br>
<span style="text-decoration: underline;">DADOS DO
CENTR&Oacute;IDE DA MOLDURA</span><br>
<div style="text-align: center;"><br>
</div>
<table
 style="width: 508px; text-align: left; margin-left: auto; margin-right: auto; height: 137px;"
 border="1" cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td style="width: 253px; text-align: center; height: 43px;">LONGITUDE</td>
      <td style="width: 237px; text-align: center; height: 43px;">%s</td>
    </tr>
    <tr>
      <td style="width: 253px; text-align: center; height: 43px;">LATITUDE</td>
      <td style="width: 237px; text-align: center; height: 43px;">%s</td>
    </tr>
    <tr>
      <td style="width: 253px; text-align: center; height: 43px;">SRID</td>
      <td style="width: 237px; text-align: center; height: 43px;">%s</td>
    </tr>
  </tbody>
</table>
<div style="text-align: center;"><br>
</div>
<br>
<span style="text-decoration: underline;">CONVERG&Ecirc;NCIA
MERIDIANA</span><br>
</div>
<div style="text-align: center;"><br>
</div>
<table
 style="width: 508px; text-align: left; margin-left: auto; margin-right: auto; height: 89px;"
 border="1" cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td style="width: 253px; text-align: center; height: 43px;">GRAUS
DECIMAIS</td>
      <td style="width: 237px; text-align: center; height: 43px;">%s</td>
    </tr>
    <tr>
      <td style="width: 253px; text-align: center; height: 43px;">GRAUS,
MINUTOS E SEGUNDOS</td>
      <td style="width: 237px; text-align: center; height: 43px;">%s</td>
    </tr>
  </tbody>
</table>
<span style="text-decoration: underline;"><br>
</span>
<div style="text-align: center;"><span
 style="text-decoration: underline;"><br>
FATOR DE DISTOR&Ccedil;&Atilde;O DE ESCALA (KAPPA)</span><br>
</div>
<div style="text-align: center;"><br>
</div>
<table
 style="width: 508px; text-align: left; margin-left: auto; margin-right: auto; height: 47px;"
 border="1" cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td style="width: 253px; text-align: center; height: 43px;">KAPPA</td>
      <td style="width: 237px; text-align: center; height: 43px;">%s</td>
    </tr>
  </tbody>
</table>
<div style="text-align: center;"><br>
</div>
<br>
</body>
</html>
''' %(dd2dmsHTML(lon), dd2dmsHTML(lat), SRC.authid().split(':')[-1], str(ConvMer(lon, lat, a, b)), dd2dmsHTML(ConvMer(lon, lat, a, b)), str(FatorK(lon, lat)))

arquivo = open(Resultado, 'w')
arquivo.write(texto)
arquivo.close()

progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(5)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)