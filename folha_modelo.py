# -*- coding: utf-8 -*-
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
# Gerar Folha Modelo
##4. Folha Modelo=name
##LF10) Cartografia=group
##Moldura=vector
##Convergencia_Meridiana=number 0.0
##Declinacao_Magnetica=number 0.0
##Variacao_da_Declinacao_Magnetica=number 0.0
##Pasta_com_Figuras=folder
##Modelo=output file

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing
from math import ceil, floor, modf

# Denominador da Escala
denominador = 25000

# Convergencia Meridiana
CM = Convergencia_Meridiana

# Rotacao
if CM < 0:
    ROTACAO = '%.1f' %(-1.0*CM)
else:
    ROTACAO = '%.1f' %(360-CM)

# Declinacao Magnetica
DM = Declinacao_Magnetica

# Variacao da Declinacao Declinacao_Magnetica
VarDM = Variacao_da_Declinacao_Magnetica

# Transformar graus decimais em GMS (html)
def dd2dmsHTML(degs):
    neg = degs < 0
    degs = (-1) ** neg * degs
    degs, d_int = modf(degs)
    mins, m_int = modf(60 * degs)
    secs        =           60 * mins
    if neg:
        return u'-%d&amp;deg;%02d\'%02d&quot' %(int(d_int), int(m_int), int(secs))
    else:
        return u'+%d&amp;deg;%02d\'%02d&quot' %(int(d_int), int(m_int), int(secs))

# Abrir camada de CT
moldura = processing.getObject(Moldura)
SRC_origem = moldura.crs()
Extensao = moldura.extent().asPolygon().replace(',','').split(' ')
Xmin = float(Extensao[0])
Xmax = float(Extensao[4])
Ymin = float(Extensao[1])
Ymax = float(Extensao[3])
# Sistema de Referencia de Coordenadas do Projeto
canvas = iface.mapCanvas()
SRC_destino = canvas.mapRenderer().destinationCrs()

# Funcao de Transformacao de Coordenadas
xform = QgsCoordinateTransform(SRC_origem, SRC_destino)
def reprojetar(geom):
    if geom.type() == 0: #Ponto
        if geom.isMultipart():
            pnts = geom.asMultiPoint()
            newPnts = []
            for pnt in pnts:
                newPnts += [xform.transform(pnt)]
            newGeom = QgsGeometry.fromMultiPoint(newPnts)
        else:
            pnt = geom.asPoint()
            newPnt = xform.transform(pnt)
            newGeom = QgsGeometry.fromPoint(newPnt)
    elif geom.type() == 1: #Linha
        if geom.isMultipart():
            linhas = geom.asMultiPolyline()
            newLines = []
            for linha in linhas:
                newLine =[]
                for pnt in linha:
                    newLine += [xform.transform(pnt)]
                newLines += [newLine]
            newGeom = QgsGeometry.fromMultiPolyline(newLines)
        else:
            linha = geom.asPolyline()
            newLine =[]
            for pnt in linha:
                newLine += [xform.transform(pnt)]
            newGeom = QgsGeometry.fromPolyline(newLine)
    elif geom.type() == 2: #Poligono
        if geom.isMultipart():
            poligonos = geom.asMultiPolygon()
            newPolygons = []
            for aneis in poligonos:
                newAneis = []
                for anel in aneis:
                    newAnel = []
                    for pnt in anel:
                        newAnel += [xform.transform(pnt)]
                newAneis += [newAnel]
            newPolygons += [newAneis]
            newGeom = QgsGeometry.fromMultiPolygon(newPolygons)
        else:
            aneis = geom.asPolygon()
            newAneis = []
            for anel in aneis:
                newAnel = []
                for pnt in anel:
                    newAnel += [xform.transform(pnt)]
            newAneis += [newAnel]
            newGeom = QgsGeometry.fromPolygon(newAneis)
    return newGeom

# Converter as coordenadas para sitema projetado UTM
P1 = reprojetar(QgsGeometry.fromPoint(QgsPoint(Xmin, Ymax)))
P2 = reprojetar(QgsGeometry.fromPoint(QgsPoint(Xmax, Ymax)))
P3 = reprojetar(QgsGeometry.fromPoint(QgsPoint(Xmax, Ymin)))
P4 = reprojetar(QgsGeometry.fromPoint(QgsPoint(Xmin, Ymin)))

# Extensao
tol = 0.2*denominador/1000
x_ext_max = (P2.asPoint().x()+P3.asPoint().x())/2 + tol
x_ext_min = (P1.asPoint().x()+P4.asPoint().x())/2 - tol
y_ext_max = (P1.asPoint().y()+P2.asPoint().y())/2 + tol
y_ext_min = (P3.asPoint().y()+P4.asPoint().y())/2 - tol

# Tamanho
largura= ceil(1000*(x_ext_max - x_ext_min)/denominador)
altura= ceil(1000*(y_ext_max - y_ext_min)/denominador)

# Informacoes da Carta (Nome, INOM, MI)
features = moldura.getFeatures()
feat = features.next()
TITULO_TEXTO = feat['carta_nome']
IND_NOMENCLATURA = feat['inom']
MAPA_INDICE = feat['mi']

# Nome do Banco
NOME_BANCO = (moldura.source()).split("'")[1]

# Parametros
parametros=  {'TITULO_TEXTO': TITULO_TEXTO,
             'IND_NOMENCLATURA': IND_NOMENCLATURA,
             'MAPA_INDICE': MAPA_INDICE,
             'CONV_MER': dd2dmsHTML(CM),
             'DECL_MAGN': dd2dmsHTML(DM),
             'VAR_DECL_MAGN': dd2dmsHTML(VarDM),
             'LARGURA': str(largura),
             'ALTURA': str(altura),
             'X_EXT_MIN': str(x_ext_min),
             'Y_EXT_MIN': str(y_ext_min),
             'X_EXT_MAX': str(x_ext_max),
             'Y_EXT_MAX': str(y_ext_max),
             'PASTA_COM_FIGURAS': Pasta_com_Figuras,
             'NOME_BANCO': NOME_BANCO,
             'ROTACAO': ROTACAO
             }

# Arquivo Modelo
texto = '''<Composer title="Carta Topo" visible="1">
 <Composition resizeToContentsMarginLeft="0" snapping="0" showPages="1" guidesVisible="1" resizeToContentsMarginTop="0" worldFileMap="{699e8201-4b47-4fff-b608-50d59d7cfe76}" alignmentSnap="1" printResolution="300" paperWidth="841" gridVisible="0" snapGridOffsetX="0" smartGuides="1" snapGridOffsetY="0" resizeToContentsMarginRight="0" snapTolerancePixels="5" printAsRaster="1" generateWorldFile="0" paperHeight="594" numPages="1" snapGridResolution="10" resizeToContentsMarginBottom="0">
  <symbol alpha="1" clip_to_extent="1" type="fill" name="">
   <layer pass="0" class="SimpleFill" locked="0">
    <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
    <prop k="color" v="255,255,255,255"/>
    <prop k="joinstyle" v="miter"/>
    <prop k="offset" v="0,0"/>
    <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
    <prop k="offset_unit" v="MM"/>
    <prop k="outline_color" v="0,0,0,255"/>
    <prop k="outline_style" v="no"/>
    <prop k="outline_width" v="0.26"/>
    <prop k="outline_width_unit" v="MM"/>
    <prop k="style" v="solid"/>
   </layer>
  </symbol>
  <SnapLine y1="594.742" x1="0" y2="594.742" x2="841"/>
  <ComposerItemGroup>
   <ComposerItemGroupElement uuid="{142fdf06-f692-4b9c-8af0-6a5f792ec3b5}"/>
   <ComposerItemGroupElement uuid="{5fded6e3-a8a5-4696-884a-5af8b67b429a}"/>
   <ComposerItemGroupElement uuid="{2ef84c3a-936e-418e-8bec-5933f4e5479e}"/>
   <ComposerItem pagey="109.927" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="727.635" y="109.927" visibility="1" zValue="90" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="78.537" outlineWidth="0.3" excludeFromExports="0" uuid="{b8e74875-99f8-4f69-9332-fc238ff37505}" height="32.421" itemRotation="0" frame="false" pagex="727.635">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerItemGroup>
  <ComposerPicture resizeMode="0" svgBorderWidth="0.2" pictureRotation="0" pictureWidth="24.2305" svgFillColor="255,255,255,255" svgBorderColor="0,0,0,255" northMode="0" file="PASTA_COM_FIGURAS/DECART.png" northOffset="0" pictureHeight="13.4907" mapId="-1" anchorPoint="0">
   <ComposerItem pagey="508.381" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="72.1208" y="508.381" visibility="1" zValue="80" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="24.2305" outlineWidth="0.3" excludeFromExports="0" uuid="{744cd524-cb26-4165-b839-397b78f5be00}" height="15.4935" itemRotation="0" frame="false" pagex="72.1208">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <dataDefinedSource expr="" field="" active="false" useExpr="true"/>
    <customproperties/>
   </ComposerItem>
  </ComposerPicture>
  <ComposerItemGroup>
   <ComposerItemGroupElement uuid="{636aa128-eee2-4563-872a-087beff46d11}"/>
   <ComposerItemGroupElement uuid="{ec87f86b-033c-4b1d-9c37-00dffd7f11bf}"/>
   <ComposerItem pagey="42.5193" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="724.038" y="42.5193" visibility="1" zValue="76" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="86.315" outlineWidth="0.3" excludeFromExports="0" uuid="{5eda0549-4107-469e-8f5e-656b6ac50c19}" height="34" itemRotation="0" frame="false" pagex="724.038">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerItemGroup>
  <ComposerMap followPreset="false" mapRotation="ROTACAO" keepLayerSet="false" followPresetName="" id="0" previewMode="Cache" drawCanvasItems="true">
   <Extent ymin="Y_EXT_MIN" xmin="X_EXT_MIN" ymax="Y_EXT_MAX" xmax="X_EXT_MAX"/>
   <LayerSet/>
   <Grid/>
   <ComposerMapGrid rightAnnotationDirection="0" gridFramePenColor="0,0,0,255" show="1" bottomAnnotationPosition="1" annotationPrecision="0" showAnnotation="1" topFrameDivisions="0" uuid="{5eb0dabc-f198-4053-93df-1e68fc4c99f7}" leftAnnotationDirection="0" topAnnotationPosition="1" rightAnnotationDisplay="0" offsetX="0" offsetY="0" rightFrameDivisions="0" gridStyle="3" annotationFontColor="63,63,63,255" intervalX="0.125" gridFrameSideFlags="15" intervalY="0.125" bottomAnnotationDirection="0" leftAnnotationDisplay="0" leftFrameDivisions="0" frameFillColor1="255,255,255,255" annotationExpression="" frameFillColor2="0,0,0,255" crossLength="3" gridFramePenThickness="0.5" bottomAnnotationDisplay="0" unit="0" topAnnotationDisplay="0" leftAnnotationPosition="1" blendMode="0" gridFrameStyle="0" rightAnnotationPosition="1" gridFrameWidth="2" name="Grade 1" annotationFormat="2" bottomFrameDivisions="0" topAnnotationDirection="0" frameAnnotationDistance="1">
    <lineStyle>
     <symbol alpha="1" clip_to_extent="1" type="line" name="">
      <layer pass="0" class="SimpleLine" locked="0">
       <prop k="capstyle" v="square"/>
       <prop k="customdash" v="5;2"/>
       <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="customdash_unit" v="MM"/>
       <prop k="draw_inside_polygon" v="0"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="line_color" v="0,0,0,255"/>
       <prop k="line_style" v="solid"/>
       <prop k="line_width" v="0"/>
       <prop k="line_width_unit" v="MM"/>
       <prop k="offset" v="0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="use_custom_dash" v="0"/>
       <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
      </layer>
     </symbol>
    </lineStyle>
    <markerStyle>
     <symbol alpha="1" clip_to_extent="1" type="marker" name="">
      <layer pass="0" class="SimpleMarker" locked="0">
       <prop k="angle" v="0"/>
       <prop k="color" v="0,0,0,255"/>
       <prop k="horizontal_anchor_point" v="1"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="name" v="circle"/>
       <prop k="offset" v="0,0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="outline_color" v="0,0,0,255"/>
       <prop k="outline_style" v="solid"/>
       <prop k="outline_width" v="0"/>
       <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="outline_width_unit" v="MM"/>
       <prop k="scale_method" v="diameter"/>
       <prop k="size" v="2"/>
       <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="size_unit" v="MM"/>
       <prop k="vertical_anchor_point" v="1"/>
      </layer>
     </symbol>
    </markerStyle>
    <spatialrefsys>
     <proj4>+proj=longlat +datum=WGS84 +no_defs</proj4>
     <srsid>3452</srsid>
     <srid>4326</srid>
     <authid>EPSG:4326</authid>
     <description>WGS 84</description>
     <projectionacronym>longlat</projectionacronym>
     <ellipsoidacronym>WGS84</ellipsoidacronym>
     <geographicflag>true</geographicflag>
    </spatialrefsys>
    <annotationFontProperties description="Arial,6,-1,5,50,0,0,0,0,0" style=""/>
   </ComposerMapGrid>
   <AtlasMap scalingMode="2" atlasDriven="0" margin="0.10000000000000001"/>
   <ComposerItem pagey="88.794" page="1" id="" lastValidViewScaleFactor="3.77953" positionMode="0" positionLock="false" x="33.0955" y="88.794" visibility="1" zValue="75" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="75" outlineWidth="0.3" excludeFromExports="0" uuid="{6e667887-367f-4a21-ad1d-8fd122d78014}" height="75" itemRotation="0" frame="true" pagex="33.0955">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerMap>
  <ComposerMap followPreset="false" mapRotation="0" keepLayerSet="false" followPresetName="" id="5" previewMode="Cache" drawCanvasItems="true">
   <Extent ymin="9006706.23834823444485664" xmin="240604.46360584086505696" ymax="9044206.2383864838629961" xmax="278104.46364409086527303"/>
   <LayerSet/>
   <Grid/>
   <ComposerMapGrid rightAnnotationDirection="0" gridFramePenColor="0,0,0,255" show="0" bottomAnnotationPosition="1" annotationPrecision="3" showAnnotation="0" topFrameDivisions="0" uuid="{a537fde9-ae66-4060-a2b8-aaed51858d46}" leftAnnotationDirection="0" topAnnotationPosition="1" rightAnnotationDisplay="0" offsetX="0" offsetY="0" rightFrameDivisions="0" gridStyle="0" annotationFontColor="0,0,0,255" intervalX="0" gridFrameSideFlags="15" intervalY="0" bottomAnnotationDirection="0" leftAnnotationDisplay="0" leftFrameDivisions="0" frameFillColor1="255,255,255,255" annotationExpression="" frameFillColor2="0,0,0,255" crossLength="3" gridFramePenThickness="0.5" bottomAnnotationDisplay="0" unit="0" topAnnotationDisplay="0" leftAnnotationPosition="1" blendMode="0" gridFrameStyle="0" rightAnnotationPosition="1" gridFrameWidth="2" name="Grade 1" annotationFormat="0" bottomFrameDivisions="0" topAnnotationDirection="0" frameAnnotationDistance="1">
    <lineStyle>
     <symbol alpha="1" clip_to_extent="1" type="line" name="">
      <layer pass="0" class="SimpleLine" locked="0">
       <prop k="capstyle" v="square"/>
       <prop k="customdash" v="5;2"/>
       <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="customdash_unit" v="MM"/>
       <prop k="draw_inside_polygon" v="0"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="line_color" v="0,0,0,255"/>
       <prop k="line_style" v="solid"/>
       <prop k="line_width" v="0"/>
       <prop k="line_width_unit" v="MM"/>
       <prop k="offset" v="0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="use_custom_dash" v="0"/>
       <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
      </layer>
     </symbol>
    </lineStyle>
    <markerStyle>
     <symbol alpha="1" clip_to_extent="1" type="marker" name="">
      <layer pass="0" class="SimpleMarker" locked="0">
       <prop k="angle" v="0"/>
       <prop k="color" v="0,0,0,255"/>
       <prop k="horizontal_anchor_point" v="1"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="name" v="circle"/>
       <prop k="offset" v="0,0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="outline_color" v="0,0,0,255"/>
       <prop k="outline_style" v="solid"/>
       <prop k="outline_width" v="0"/>
       <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="outline_width_unit" v="MM"/>
       <prop k="scale_method" v="diameter"/>
       <prop k="size" v="2"/>
       <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="size_unit" v="MM"/>
       <prop k="vertical_anchor_point" v="1"/>
      </layer>
     </symbol>
    </markerStyle>
    <annotationFontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
   </ComposerMapGrid>
   <AtlasMap scalingMode="2" atlasDriven="0" margin="0.10000000000000001"/>
   <ComposerItem pagey="309.527" page="1" id="" lastValidViewScaleFactor="3.77953" positionMode="0" positionLock="false" x="32.359" y="309.527" visibility="1" zValue="74" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="75" outlineWidth="0.3" excludeFromExports="0" uuid="{6507c268-6561-4795-bac3-29458f766e6d}" height="75" itemRotation="0" frame="true" pagex="32.359">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerMap>
  <ComposerMap followPreset="false" mapRotation="0" keepLayerSet="false" followPresetName="" id="4" previewMode="Cache" drawCanvasItems="true">
   <Extent ymin="8670470.90119930543005466" xmin="-471762.44284305576002225" ymax="9495470.90204080566763878" xmax="353237.5579984441283159"/>
   <LayerSet/>
   <Grid/>
   <ComposerMapGrid rightAnnotationDirection="0" gridFramePenColor="0,0,0,255" show="0" bottomAnnotationPosition="1" annotationPrecision="3" showAnnotation="0" topFrameDivisions="0" uuid="{9d6be539-7c5f-4bc4-95e5-a90d8df38583}" leftAnnotationDirection="0" topAnnotationPosition="1" rightAnnotationDisplay="0" offsetX="0" offsetY="0" rightFrameDivisions="0" gridStyle="0" annotationFontColor="0,0,0,255" intervalX="0" gridFrameSideFlags="15" intervalY="0" bottomAnnotationDirection="0" leftAnnotationDisplay="0" leftFrameDivisions="0" frameFillColor1="255,255,255,255" annotationExpression="" frameFillColor2="0,0,0,255" crossLength="3" gridFramePenThickness="0.5" bottomAnnotationDisplay="0" unit="0" topAnnotationDisplay="0" leftAnnotationPosition="1" blendMode="0" gridFrameStyle="0" rightAnnotationPosition="1" gridFrameWidth="2" name="Grade 1" annotationFormat="0" bottomFrameDivisions="0" topAnnotationDirection="0" frameAnnotationDistance="1">
    <lineStyle>
     <symbol alpha="1" clip_to_extent="1" type="line" name="">
      <layer pass="0" class="SimpleLine" locked="0">
       <prop k="capstyle" v="square"/>
       <prop k="customdash" v="5;2"/>
       <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="customdash_unit" v="MM"/>
       <prop k="draw_inside_polygon" v="0"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="line_color" v="0,0,0,255"/>
       <prop k="line_style" v="solid"/>
       <prop k="line_width" v="0"/>
       <prop k="line_width_unit" v="MM"/>
       <prop k="offset" v="0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="use_custom_dash" v="0"/>
       <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
      </layer>
     </symbol>
    </lineStyle>
    <markerStyle>
     <symbol alpha="1" clip_to_extent="1" type="marker" name="">
      <layer pass="0" class="SimpleMarker" locked="0">
       <prop k="angle" v="0"/>
       <prop k="color" v="0,0,0,255"/>
       <prop k="horizontal_anchor_point" v="1"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="name" v="circle"/>
       <prop k="offset" v="0,0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="outline_color" v="0,0,0,255"/>
       <prop k="outline_style" v="solid"/>
       <prop k="outline_width" v="0"/>
       <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="outline_width_unit" v="MM"/>
       <prop k="scale_method" v="diameter"/>
       <prop k="size" v="2"/>
       <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="size_unit" v="MM"/>
       <prop k="vertical_anchor_point" v="1"/>
      </layer>
     </symbol>
    </markerStyle>
    <annotationFontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
   </ComposerMapGrid>
   <AtlasMap scalingMode="2" atlasDriven="0" margin="0.10000000000000001"/>
   <ComposerItem pagey="215.675" page="1" id="" lastValidViewScaleFactor="3.77953" positionMode="0" positionLock="false" x="33.2306" y="215.675" visibility="1" zValue="73" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="75" outlineWidth="0.3" excludeFromExports="0" uuid="{c3448441-0fe1-4de6-9da3-edabf6214210}" height="75" itemRotation="0" frame="true" pagex="33.2306">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerMap>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="ORIGEM DOS DADOS" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="544.535" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="730.902" y="544.535" visibility="1" zValue="72" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="72.7167" outlineWidth="0.3" excludeFromExports="0" uuid="{7ae4be7d-99eb-4003-a3da-3c760533f286}" height="5.75785" itemRotation="0" frame="false" pagex="730.902">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="INFORMAÃÃES TÃCNICAS DA CARTA" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="456.639" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="730.967" y="456.639" visibility="1" zValue="71" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="72.7167" outlineWidth="0.3" excludeFromExports="0" uuid="{e0d15219-27c9-4cca-abed-00d041dd2a2c}" height="5.75785" itemRotation="0" frame="false" pagex="730.967">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="ETAPAS DE PRODUÃÃO" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="381.593" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="739.768" y="381.593" visibility="1" zValue="70" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="57.1573" outlineWidth="0.3" excludeFromExports="0" uuid="{bc12cb8b-13c0-4d4a-98a7-4a160169cf6a}" height="6.16896" itemRotation="0" frame="false" pagex="739.768">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerPicture resizeMode="0" svgBorderWidth="0.2" pictureRotation="ROTACAO" pictureWidth="10.222" svgFillColor="255,255,255,255" svgBorderColor="0,0,0,255" northMode="0" file="PASTA_COM_FIGURAS/BrasÃ£o_da_UFPE.png" northOffset="0" pictureHeight="15.1839" mapId="1" anchorPoint="4">
   <ComposerItem pagey="508.381" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="44.7784" y="508.381" visibility="1" zValue="63" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="11.0492" outlineWidth="0.3" excludeFromExports="0" uuid="{1353c365-84ea-4fb2-b12e-599db73218df}" height="15.2443" itemRotation="0" frame="false" pagex="44.7784">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <dataDefinedSource expr="" field="" active="false" useExpr="true"/>
    <customproperties/>
   </ComposerItem>
  </ComposerPicture>
  <ComposerPicture resizeMode="0" svgBorderWidth="0.2" pictureRotation="ROTACAO" pictureWidth="20.2262" svgFillColor="255,255,255,255" svgBorderColor="0,0,0,255" northMode="0" file="PASTA_COM_FIGURAS/BDGEx_mobile.png" northOffset="0" pictureHeight="20.2262" mapId="1" anchorPoint="4">
   <ComposerItem pagey="176.094" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="60.4226" y="176.094" visibility="1" zValue="62" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="20.3459" outlineWidth="0.3" excludeFromExports="0" uuid="{7b90b096-a756-4c5e-b548-5e4a0162f33e}" height="20.5123" itemRotation="0" frame="false" pagex="60.4226">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <dataDefinedSource expr="" field="" active="false" useExpr="true"/>
    <customproperties/>
   </ComposerItem>
  </ComposerPicture>
  <ComposerItemGroup>
   <ComposerItemGroupElement uuid="{898495bb-6c69-4dba-b80f-93f749b08e79}"/>
   <ComposerItemGroupElement uuid="{877893ae-6530-470f-a726-96785bf81622}"/>
   <ComposerItem pagey="221.232" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="725.825" y="221.232" visibility="1" zValue="61" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="89.8538" outlineWidth="0.3" excludeFromExports="0" uuid="{6045d6f3-2220-4875-9e17-50296c4ae164}" height="20.6492" itemRotation="0" frame="false" pagex="725.825">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerItemGroup>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="EDIFICAÃÃO" htmlState="0" halign="4">
   <LabelFont description="Arial,7,-1,5,50,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="170.897" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="714.594" y="170.897" visibility="1" zValue="60" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="107.776" outlineWidth="0.3" excludeFromExports="0" uuid="{45113fa1-9201-45e0-9fa7-812804d03c8c}" height="4.42097" itemRotation="0" frame="false" pagex="714.594">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="217" blue="217" green="217"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerScaleBar lineCapStyle="square" style="Single Box" numMapUnitsPerScaleBarUnit="1" segmentSizeMode="0" alignment="0" numSegments="0" segmentMillimeters="20.0063" lineJoinStyle="miter" minBarWidth="0" numUnitsPerSegment="500" units="1" labelBarSpace="0.5" outlineWidth="0.2" numSegmentsLeft="5" maxBarWidth="150" height="2" boxContentSpace="1" mapId="1" unitLabel="m">
   <scaleBarFont description="MS Shell Dlg 2,1,-1,5,50,0,0,0,0,0" style=""/>
   <fillColor alpha="255" red="0" blue="0" green="0"/>
   <fillColor2 alpha="255" red="255" blue="255" green="255"/>
   <strokeColor alpha="255" red="0" blue="0" green="0"/>
   <textColor alpha="255" red="255" blue="255" green="255"/>
   <ComposerItem pagey="226.059" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="726.373" y="226.059" visibility="1" zValue="59" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="23.2063" outlineWidth="0.3" excludeFromExports="0" uuid="{898495bb-6c69-4dba-b80f-93f749b08e79}" height="5.16073" itemRotation="0" frame="false" pagex="726.373">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerScaleBar>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="RELEVO" htmlState="0" halign="4">
   <LabelFont description="Arial,7,-1,5,50,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="150.504" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="713.862" y="150.504" visibility="1" zValue="58" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="107.776" outlineWidth="0.3" excludeFromExports="0" uuid="{58a6da2f-0f8a-4765-ac99-91de1460b5ae}" height="4.42097" itemRotation="0" frame="false" pagex="713.862">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="217" blue="217" green="217"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="255,255,255,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.3"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="116.8" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="736.613" y="116.8" visibility="1" zValue="57" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="2.38992" outlineWidth="0.3" excludeFromExports="0" uuid="{293fcf59-b227-43e6-acfc-0abd5d2550c5}" height="23.9616" itemRotation="0" frame="false" pagex="736.613">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="Combater: Jogos de Guerra / Ajuda HumanitÃ¡ria CMNE" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,50,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="489.555" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="19.2342" y="489.555" visibility="1" zValue="56" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="100.557" outlineWidth="0.3" excludeFromExports="0" uuid="{8d0339d5-04eb-4ad8-bc24-2db3ce3a2374}" height="7.50554" itemRotation="0" frame="false" pagex="19.2342">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerItemGroup>
   <ComposerItemGroupElement uuid="{293fcf59-b227-43e6-acfc-0abd5d2550c5}"/>
   <ComposerItemGroupElement uuid="{9c5fa40a-99be-43c7-b888-b5077b020c10}"/>
   <ComposerItem pagey="116.8" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="728.342" y="116.8" visibility="1" zValue="55" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="10.6604" outlineWidth="0.3" excludeFromExports="0" uuid="{bdaaa82e-ab87-4455-9753-d01e07981c90}" height="25.5476" itemRotation="0" frame="false" pagex="728.342">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerItemGroup>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="ESCALA 1:25.000" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="211.356" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="713.94" y="211.356" visibility="1" zValue="53" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="109.084" outlineWidth="0.3" excludeFromExports="0" uuid="{4929aa70-8c41-440e-9408-b5f5301b5136}" height="6.16896" itemRotation="0" frame="false" pagex="713.94">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="MOBILIDADE" htmlState="0" halign="4">
   <LabelFont description="Arial,7,-1,5,50,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="109.927" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="713.862" y="109.927" visibility="1" zValue="52" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="107.776" outlineWidth="0.3" excludeFromExports="0" uuid="{546f5d44-064d-4755-bda8-0a38e51a35dc}" height="4.42097" itemRotation="0" frame="false" pagex="713.862">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="217" blue="217" green="217"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="MINISTÃRIO DA DEFESA - EXÃRCITO BRASILEIRO&#xa;DEPARTAMENTO DE CIÃNCIAS E TECNOLOGIA&#xa;DIRETORIA DE SERVIÃO GEOGRÃFICO" htmlState="0" halign="4">
   <LabelFont description="Arial,8,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="15.9881" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="25.964" y="15.9881" visibility="1" zValue="51" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="88.2819" outlineWidth="0.3" excludeFromExports="0" uuid="{748c0d53-04ea-4805-a770-b884602290c6}" height="13.5201" itemRotation="0" frame="false" pagex="25.964">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerScaleBar lineCapStyle="square" style="Single Box" numMapUnitsPerScaleBarUnit="1" segmentSizeMode="0" alignment="0" numSegments="4" segmentMillimeters="20.0063" lineJoinStyle="miter" minBarWidth="0" numUnitsPerSegment="500" units="1" labelBarSpace="3" outlineWidth="0.3" numSegmentsLeft="0" maxBarWidth="150" height="2" boxContentSpace="1" mapId="1" unitLabel="m">
   <scaleBarFont description="Arial,8,-1,5,50,0,0,0,0,0" style=""/>
   <fillColor alpha="255" red="0" blue="0" green="0"/>
   <fillColor2 alpha="255" red="255" blue="255" green="255"/>
   <strokeColor alpha="255" red="0" blue="0" green="0"/>
   <textColor alpha="255" red="0" blue="0" green="0"/>
   <ComposerItem pagey="221.232" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="725.825" y="221.232" visibility="1" zValue="50" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="89.8253" outlineWidth="0.3" excludeFromExports="0" uuid="{877893ae-6530-470f-a726-96785bf81622}" height="20.6492" itemRotation="0" frame="false" pagex="725.825">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerScaleBar>
  <ComposerLegend symbolWidth="7" title="" rasterBorderWidth="0" titleAlignment="1" map="1" wmsLegendWidth="50" rasterBorderColor="0,0,0,255" wrapChar="" fontColor="#000000" legendFilterByAtlas="0" columnCount="1" wmsLegendHeight="25" columnSpace="2" symbolHeight="4" equalColumnWidth="0" resizeToContents="1" splitLayer="0" boxSpace="2" rasterBorder="1">
   <styles>
    <style marginBottom="2" name="title">
     <styleFont description="MS Shell Dlg 2,16,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="group">
     <styleFont description="MS Shell Dlg 2,14,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="subgroup">
     <styleFont description="MS Shell Dlg 2,12,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="symbol">
     <styleFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" marginLeft="2" name="symbolLabel">
     <styleFont description="Arial,8,-1,5,50,0,0,0,0,0" style=""/>
    </style>
   </styles>
   <layer-tree-group expanded="1" checked="Qt::Checked" name="">
    <customproperties/>
    <layer-tree-layer expanded="1" providerKey="postgres" checked="Qt::Checked" id="ponto_urbano_p20180305083928233" source="dbname='NOME_BANCO' host=localhost port=5432 user='postgres' key='id' selectatid=false table=&quot;base&quot;.&quot;ponto_urbano_p&quot; (geom) sql=id in (SELECT id FROM ONLY &quot;base&quot;.&quot;ponto_urbano_p&quot;)" name="ponto_urbano_p">
     <customproperties>
      <property key="legend/title-label" value="Localidade / Aglomerado Rural"/>
     </customproperties>
    </layer-tree-layer>
   </layer-tree-group>
   <ComposerItem pagey="176.35" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="740.843" y="176.35" visibility="1" zValue="49" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="51.3" outlineWidth="0.3" excludeFromExports="0" uuid="{b873a523-0347-48f5-bd23-0b7f8214ab9c}" height="10" itemRotation="0" frame="false" pagex="740.843">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLegend>
  <ComposerLegend symbolWidth="7" title="" rasterBorderWidth="0" titleAlignment="1" map="1" wmsLegendWidth="50" rasterBorderColor="0,0,0,255" wrapChar="" fontColor="#000000" legendFilterByAtlas="0" columnCount="2" wmsLegendHeight="25" columnSpace="37" symbolHeight="4" equalColumnWidth="0" resizeToContents="1" splitLayer="1" boxSpace="2" rasterBorder="1">
   <styles>
    <style name="title">
     <styleFont description="MS Shell Dlg 2,16,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="group">
     <styleFont description="MS Shell Dlg 2,14,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="subgroup">
     <styleFont description="MS Shell Dlg 2,12,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="symbol">
     <styleFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginLeft="3" name="symbolLabel">
     <styleFont description="Arial,8,-1,5,50,0,0,0,0,0" style=""/>
    </style>
   </styles>
   <layer-tree-group expanded="1" checked="Qt::Checked" name="">
    <customproperties/>
    <layer-tree-layer expanded="0" providerKey="postgres" checked="Qt::Checked" id="curva_nivel_l20180305083928026" source="dbname='NOME_BANCO' host=localhost port=5432 user='postgres' key='id' selectatid=false table=&quot;base&quot;.&quot;curva_nivel_l&quot; (geom) sql=id in (SELECT id FROM ONLY &quot;base&quot;.&quot;curva_nivel_l&quot;)" name="curva_nivel_l">
     <customproperties>
      <property key="legend/title-label" value=""/>
     </customproperties>
    </layer-tree-layer>
   </layer-tree-group>
   <ComposerItem pagey="155.944" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="727.226" y="155.944" visibility="1" zValue="48" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="78.5" outlineWidth="0.3" excludeFromExports="0" uuid="{4fdddfb2-4949-41c0-94ac-4e2e356e55e9}" height="8" itemRotation="0" frame="false" pagex="727.226">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLegend>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="255,255,255,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.3"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="118.386" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="728.342" y="118.386" visibility="1" zValue="47" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="2.38992" outlineWidth="0.3" excludeFromExports="0" uuid="{9c5fa40a-99be-43c7-b888-b5077b020c10}" height="23.9616" itemRotation="0" frame="false" pagex="728.342">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerLegend symbolWidth="10" title="" rasterBorderWidth="0" titleAlignment="1" map="1" wmsLegendWidth="50" rasterBorderColor="0,0,0,255" wrapChar="" fontColor="#000000" legendFilterByAtlas="0" columnCount="1" wmsLegendHeight="25" columnSpace="2" symbolHeight="4" equalColumnWidth="0" resizeToContents="1" splitLayer="0" boxSpace="2" rasterBorder="1">
   <styles>
    <style name="title">
     <styleFont description="MS Shell Dlg 2,16,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="group">
     <styleFont description="MS Shell Dlg 2,14,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="subgroup">
     <styleFont description="MS Shell Dlg 2,12,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="symbol">
     <styleFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" marginLeft="2" name="symbolLabel">
     <styleFont description="Arial,8,-1,5,50,0,0,0,0,0" style=""/>
    </style>
   </styles>
   <layer-tree-group expanded="1" checked="Qt::Checked" name="">
    <customproperties/>
    <layer-tree-layer expanded="1" providerKey="postgres" checked="Qt::Checked" id="ferrovia_l20180305083928090" source="dbname='NOME_BANCO' host=localhost port=5432 user='postgres' key='id' selectatid=false table=&quot;base&quot;.&quot;ferrovia_l&quot; (geom) sql=id in (SELECT id FROM ONLY &quot;base&quot;.&quot;ferrovia_l&quot;)" name="ferrovia_l">
     <customproperties>
      <property key="legend/title-label" value="Ferrovia"/>
     </customproperties>
    </layer-tree-layer>
    <layer-tree-layer expanded="1" providerKey="postgres" checked="Qt::Checked" id="tunel_l20180305083928185" source="dbname='NOME_BANCO' host=localhost port=5432 user='postgres' key='id' selectatid=false table=&quot;base&quot;.&quot;tunel_l&quot; (geom) sql=id in (SELECT id FROM ONLY &quot;base&quot;.&quot;tunel_l&quot;)" name="tunel_l">
     <customproperties>
      <property key="legend/title-label" value="TÃºnel"/>
     </customproperties>
    </layer-tree-layer>
   </layer-tree-group>
   <ComposerItem pagey="123.499" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="780.172" y="123.499" visibility="1" zValue="46" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="26" outlineWidth="0.3" excludeFromExports="0" uuid="{5fded6e3-a8a5-4696-884a-5af8b67b429a}" height="14" itemRotation="0" frame="false" pagex="780.172">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLegend>
  <ComposerPicture resizeMode="0" svgBorderWidth="0.2" pictureRotation="ROTACAO" pictureWidth="36.2932" svgFillColor="255,255,255,255" svgBorderColor="0,0,0,255" northMode="0" file="PASTA_COM_FIGURAS/Pe_de_galinha.svg" northOffset="0" pictureHeight="72.5863" mapId="1" anchorPoint="4">
   <ComposerItem pagey="265.43" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="721.774" y="265.43" visibility="1" zValue="45" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="94.7245" outlineWidth="0.3" excludeFromExports="0" uuid="{3994c257-8e4b-41e4-8494-ce2e18ed4cb0}" height="72.8004" itemRotation="0" frame="false" pagex="721.774">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <dataDefinedSource expr="" field="" active="false" useExpr="true"/>
    <customproperties/>
   </ComposerItem>
  </ComposerPicture>
  <ComposerLegend symbolWidth="4" title="" rasterBorderWidth="0" titleAlignment="1" map="1" wmsLegendWidth="50" rasterBorderColor="0,0,0,255" wrapChar="" fontColor="#000000" legendFilterByAtlas="0" columnCount="1" wmsLegendHeight="25" columnSpace="2" symbolHeight="4" equalColumnWidth="0" resizeToContents="1" splitLayer="0" boxSpace="2" rasterBorder="1">
   <styles>
    <style name="title">
     <styleFont description="MS Shell Dlg 2,16,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="group">
     <styleFont description="MS Shell Dlg 2,14,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="subgroup">
     <styleFont description="MS Shell Dlg 2,12,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="symbol">
     <styleFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginLeft="6" name="symbolLabel">
     <styleFont description="Arial,8,-1,5,50,0,0,0,0,0" style=""/>
    </style>
   </styles>
   <layer-tree-group expanded="1" checked="Qt::Checked" name="">
    <customproperties/>
    <layer-tree-group expanded="1" checked="Qt::Checked" name="">
     <customproperties/>
     <layer-tree-layer expanded="1" providerKey="postgres" checked="Qt::Checked" id="ponte_l20180305083928136" source="dbname='NOME_BANCO' host=localhost port=5432 user='postgres' key='id' selectatid=false table=&quot;base&quot;.&quot;ponte_l&quot; (geom) sql=id in (SELECT id FROM ONLY &quot;base&quot;.&quot;ponte_l&quot;)" name="ponte_l">
      <customproperties>
       <property key="legend/label-2" value="Ponte"/>
       <property key="legend/node-order" value="2"/>
       <property key="legend/title-label" value=""/>
      </customproperties>
     </layer-tree-layer>
    </layer-tree-group>
   </layer-tree-group>
   <ComposerItem pagey="109.927" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="781.81" y="109.927" visibility="1" zValue="44" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="21.4" outlineWidth="0.3" excludeFromExports="0" uuid="{2ef84c3a-936e-418e-8bec-5933f4e5479e}" height="14.4" itemRotation="0" frame="false" pagex="781.81">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLegend>
  <ComposerLegend symbolWidth="8" title="" rasterBorderWidth="0" titleAlignment="1" map="1" wmsLegendWidth="50" rasterBorderColor="0,0,0,255" wrapChar="" fontColor="#000000" legendFilterByAtlas="0" columnCount="1" wmsLegendHeight="25" columnSpace="2" symbolHeight="4" equalColumnWidth="0" resizeToContents="1" splitLayer="0" boxSpace="2" rasterBorder="1">
   <styles>
    <style name="title">
     <styleFont description="MS Shell Dlg 2,16,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="group">
     <styleFont description="MS Shell Dlg 2,14,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="subgroup">
     <styleFont description="MS Shell Dlg 2,12,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="symbol">
     <styleFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" marginLeft="4" name="symbolLabel">
     <styleFont description="Arial,8,-1,5,50,0,0,0,0,0" style=""/>
    </style>
   </styles>
   <layer-tree-group expanded="1" checked="Qt::Checked" name="">
    <customproperties/>
    <layer-tree-layer expanded="0" providerKey="postgres" checked="Qt::Checked" id="estrada_l__copiar20180305085451130" source="dbname='NOME_BANCO' host=localhost port=5432 user='postgres' key='id' selectatid=false table=&quot;base&quot;.&quot;estrada_l&quot; (geom) sql=id in (SELECT id FROM ONLY &quot;base&quot;.&quot;estrada_l&quot;)" name="estrada_l">
     <customproperties>
      <property key="legend/node-order" value="0,1,2,3"/>
      <property key="legend/title-label" value=""/>
     </customproperties>
    </layer-tree-layer>
   </layer-tree-group>
   <ComposerItem pagey="114.348" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="727.635" y="114.348" visibility="1" zValue="43" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="36.4" outlineWidth="0.3" excludeFromExports="0" uuid="{142fdf06-f692-4b9c-8af0-6a5f792ec3b5}" height="28" itemRotation="0" frame="false" pagex="727.635">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLegend>
  <ComposerPicture resizeMode="0" svgBorderWidth="0.2" pictureRotation="ROTACAO" pictureWidth="74.4337" svgFillColor="255,255,255,255" svgBorderColor="0,0,0,255" northMode="0" file="PASTA_COM_FIGURAS/Dobradura.svg" northOffset="0" pictureHeight="21.2668" mapId="1" anchorPoint="4">
   <ComposerItem pagey="556.32" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="27.4383" y="556.32" visibility="1" zValue="42" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="80.6687" outlineWidth="0.3" excludeFromExports="0" uuid="{1e7a77ab-9280-4325-a82f-b60008f78635}" height="21.7081" itemRotation="0" frame="false" pagex="27.4383">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <dataDefinedSource expr="" field="" active="false" useExpr="true"/>
    <customproperties/>
   </ComposerItem>
  </ComposerPicture>
  <ComposerPicture resizeMode="0" svgBorderWidth="0.2" pictureRotation="ROTACAO" pictureWidth="18.9163" svgFillColor="255,255,255,255" svgBorderColor="0,0,0,255" northMode="0" file="PASTA_COM_FIGURAS/DSG.svg" northOffset="0" pictureHeight="18.9163" mapId="1" anchorPoint="4">
   <ComposerItem pagey="13.9935" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="107.509" y="13.9935" visibility="1" zValue="41" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="19.1231" outlineWidth="0.3" excludeFromExports="0" uuid="{ded2129f-d65f-4f22-b9dc-bc4a926caf9b}" height="19.0282" itemRotation="0" frame="false" pagex="107.509">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <dataDefinedSource expr="" field="" active="false" useExpr="true"/>
    <customproperties/>
   </ComposerItem>
  </ComposerPicture>
  <ComposerPicture resizeMode="0" svgBorderWidth="0.2" pictureRotation="ROTACAO" pictureWidth="16.4161" svgFillColor="255,255,255,255" svgBorderColor="0,0,0,255" northMode="0" file="PASTA_COM_FIGURAS/EB.svg" northOffset="0" pictureHeight="16.4161" mapId="1" anchorPoint="4">
   <ComposerItem pagey="15.1995" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="15.132" y="15.1995" visibility="1" zValue="40" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="16.8041" outlineWidth="0.3" excludeFromExports="0" uuid="{e5eff36f-18fc-4e6b-9421-2516b1375e0f}" height="16.5132" itemRotation="0" frame="false" pagex="15.132">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <dataDefinedSource expr="" field="" active="false" useExpr="true"/>
    <customproperties/>
   </ComposerItem>
  </ComposerPicture>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="CARTA TEMÃTICA" htmlState="0" halign="4">
   <LabelFont description="Arial,14,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="255" blue="255" green="255"/>
   <ComposerItem pagey="37.5628" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="18.6014" y="37.5628" visibility="1" zValue="39" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="102.158" outlineWidth="0.3" excludeFromExports="0" uuid="{c76d8ee3-6698-459f-8458-3db35d2ffbbd}" height="10.4924" itemRotation="0" frame="false" pagex="18.6014">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="41" blue="35" green="128"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="584.123" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="708.57" y="584.123" visibility="1" zValue="38" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="119.825" outlineWidth="0.3" excludeFromExports="0" uuid="{b2502105-508c-432d-a3e6-b1e409246768}" height="2.14814" itemRotation="0" frame="false" pagex="708.57">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="584.123" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="592.559" y="584.123" visibility="1" zValue="37" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{f9d97cd5-cc49-4e92-b4a2-957fe0e5ab2b}" height="2.14814" itemRotation="0" frame="false" pagex="592.559">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="584.123" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="476.584" y="584.123" visibility="1" zValue="36" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{d035ee43-ecb7-4f9d-b7d2-262e46aa8c25}" height="2.14814" itemRotation="0" frame="false" pagex="476.584">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="584.123" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="360.647" y="584.123" visibility="1" zValue="35" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{cb22f1d8-e1f5-440f-8b34-0f5cf22c33d1}" height="2.14814" itemRotation="0" frame="false" pagex="360.647">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="584.123" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="244.689" y="584.123" visibility="1" zValue="34" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{1ec9f642-1524-4187-9fde-e5a6bb58772d}" height="2.14814" itemRotation="0" frame="false" pagex="244.689">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="584.123" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="128.729" y="584.123" visibility="1" zValue="33" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{6e30bbdf-5ae6-455b-b9fe-d88fc9d8bb3e}" height="2.14814" itemRotation="0" frame="false" pagex="128.729">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="584.123" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="12.7406" y="584.123" visibility="1" zValue="32" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{4c3bcf5e-cace-464a-aa75-e91723932c2e}" height="2.14814" itemRotation="0" frame="false" pagex="12.7406">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="TRECHO DE DRENAGEM" htmlState="0" halign="4">
   <LabelFont description="Arial,7,-1,5,50,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="84.5259" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="713.438" y="84.5259" visibility="1" zValue="30" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="107.776" outlineWidth="0.3" excludeFromExports="0" uuid="{6e2034d6-837e-4fa5-90e8-90a3a47a0e04}" height="4.42097" itemRotation="0" frame="false" pagex="713.438">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="217" blue="217" green="217"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLegend symbolWidth="7" title="" rasterBorderWidth="0" titleAlignment="1" map="1" wmsLegendWidth="50" rasterBorderColor="0,0,0,255" wrapChar="" fontColor="#000000" legendFilterByAtlas="0" columnCount="3" wmsLegendHeight="25" columnSpace="7" symbolHeight="4" equalColumnWidth="1" resizeToContents="1" splitLayer="1" boxSpace="2" rasterBorder="1">
   <styles>
    <style name="title">
     <styleFont description="MS Shell Dlg 2,16,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="group">
     <styleFont description="MS Shell Dlg 2,14,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="subgroup">
     <styleFont description="MS Shell Dlg 2,12,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="symbol">
     <styleFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginLeft="4" name="symbolLabel">
     <styleFont description="MS Shell Dlg 2,8,-1,5,50,0,0,0,0,0" style=""/>
    </style>
   </styles>
   <layer-tree-group expanded="1" checked="Qt::Checked" name="">
    <customproperties/>
    <layer-tree-layer expanded="1" providerKey="postgres" checked="Qt::Checked" id="rio_l20180305083928160" source="dbname='NOME_BANCO' host=localhost port=5432 user='postgres' key='id' selectatid=false table=&quot;base&quot;.&quot;rio_l&quot; (geom) sql=id in (SELECT id FROM ONLY &quot;base&quot;.&quot;rio_l&quot;)" name="rio_l">
     <customproperties>
      <property key="legend/node-order" value="0,1,2"/>
      <property key="legend/title-label" value=""/>
     </customproperties>
    </layer-tree-layer>
   </layer-tree-group>
   <ComposerItem pagey="91.2306" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="723.446" y="91.2306" visibility="1" zValue="29" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="85" outlineWidth="0.3" excludeFromExports="0" uuid="{ab2b838d-3ac3-4e89-a173-5ee94af2200c}" height="8" itemRotation="0" frame="false" pagex="723.446">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLegend>
  <ComposerLegend symbolWidth="7" title="" rasterBorderWidth="0.1" titleAlignment="1" map="1" wmsLegendWidth="50" rasterBorderColor="0,0,0,255" wrapChar="" fontColor="#000000" legendFilterByAtlas="0" columnCount="1" wmsLegendHeight="25" columnSpace="2" symbolHeight="4" equalColumnWidth="0" resizeToContents="1" splitLayer="1" boxSpace="2" rasterBorder="1">
   <styles>
    <style name="title">
     <styleFont description="MS Shell Dlg 2,7,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="group">
     <styleFont description="MS Shell Dlg 2,1,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="subgroup">
     <styleFont description="MS Shell Dlg 2,1,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="symbol">
     <styleFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" marginLeft="3" name="symbolLabel">
     <styleFont description="Arial,8,-1,5,50,0,0,0,0,0" style=""/>
    </style>
   </styles>
   <layer-tree-group expanded="1" checked="Qt::Checked" name="">
    <customproperties/>
    <layer-tree-layer expanded="1" providerKey="postgres" checked="Qt::Checked" id="cob_ter_a20180305083928280" source="dbname='NOME_BANCO' host=localhost port=5432 user='postgres' key='id' selectatid=false table=&quot;base&quot;.&quot;cob_ter_a&quot; (geom) sql=id in (SELECT id FROM ONLY &quot;base&quot;.&quot;cob_ter_a&quot;)" name="cob_ter_a">
     <customproperties>
      <property key="legend/label-8" value="VegetaÃ§Ã£o Mista"/>
      <property key="legend/node-order" value="0,7,1,8,2"/>
      <property key="legend/title-label" value=""/>
     </customproperties>
    </layer-tree-layer>
   </layer-tree-group>
   <ComposerItem pagey="42.5193" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="724.038" y="42.5193" visibility="1" zValue="28" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="34.7" outlineWidth="0.3" excludeFromExports="0" uuid="{ec87f86b-033c-4b1d-9c37-00dffd7f11bf}" height="34" itemRotation="0" frame="false" pagex="724.038">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLegend>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="APOIO:" htmlState="0" halign="1">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="501.723" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="19.2342" y="501.723" visibility="1" zValue="27" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="28.5787" outlineWidth="0.3" excludeFromExports="0" uuid="{daf847d8-6fe8-4f99-bbdf-ca3636ad9b93}" height="7.50554" itemRotation="0" frame="false" pagex="19.2342">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="ÃNDICE: IND_NOMENCLATURA&#xa;MI: MAPA_INDICE" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,50,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="67.7593" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="31.9361" y="67.7593" visibility="1" zValue="26" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="82.015" outlineWidth="0.3" excludeFromExports="0" uuid="{a11b5098-6b2a-4164-8200-8169079f276c}" height="13.5201" itemRotation="0" frame="false" pagex="31.9361">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="PROJETO:" htmlState="0" halign="1">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="483.375" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="19.2342" y="483.375" visibility="1" zValue="25" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="28.5787" outlineWidth="0.3" excludeFromExports="0" uuid="{8b68d946-de8c-4b2a-bb23-89e351fba467}" height="7.50554" itemRotation="0" frame="false" pagex="19.2342">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="DIAGRAMA DE CONVERGÃNCIA E DECLINAÃÃO" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="260.747" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="714.594" y="260.747" visibility="1" zValue="24" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="109.084" outlineWidth="0.3" excludeFromExports="0" uuid="{c0f688d8-e836-4d81-bea4-e7428e162c33}" height="6.16896" itemRotation="0" frame="false" pagex="714.594">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="TITULO_TEXTO" htmlState="0" halign="4">
   <LabelFont description="Arial,20,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="60.0711" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="31.9361" y="60.0711" visibility="1" zValue="23" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="82.015" outlineWidth="0.3" excludeFromExports="0" uuid="{008c6867-58bd-4728-b7db-a3de4b85e3c6}" height="11.8494" itemRotation="0" frame="false" pagex="31.9361">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="SIMBOLOGIA" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="18.4282" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="739.769" y="18.4282" visibility="1" zValue="22" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="57.1573" outlineWidth="0.3" excludeFromExports="0" uuid="{52d88ee5-9757-4ab6-97c9-c7cfccdab37a}" height="6.16896" itemRotation="0" frame="false" pagex="739.769">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="A DSG agradece a gentileza da comunicaÃ§Ã£o de alteraÃ§Ãµes,&#xa;falhas ou omissÃµes verificadas nessa folha.&#xa;www.dsg.eb.mil.br" htmlState="0" halign="4">
   <LabelFont description="Arial,8,-1,5,50,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="541.369" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="25.8228" y="541.369" visibility="1" zValue="21" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="85.9878" outlineWidth="0.3" excludeFromExports="0" uuid="{f45432f3-e596-464b-9140-ff04c270a97e}" height="15.2195" itemRotation="0" frame="false" pagex="25.8228">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="REGIÃO NORDESTE DO BRASIL" htmlState="0" halign="4">
   <LabelFont description="Arial,11,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="53.9021" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="29.8745" y="53.9021" visibility="1" zValue="20" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="82.015" outlineWidth="0.3" excludeFromExports="0" uuid="{2242fb2a-7d38-4f97-b2d7-4b9245357166}" height="6.16896" itemRotation="0" frame="false" pagex="29.8745">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="ARTICULAÃÃO DA FOLHA" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="392.604" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="40.4522" y="392.604" visibility="1" zValue="19" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="57.1573" outlineWidth="0.3" excludeFromExports="0" uuid="{ccc23f27-d163-40ea-a982-c29486275351}" height="6.16896" itemRotation="0" frame="false" pagex="40.4522">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="DIVISÃO POLÃTICA-ADMINISTRATIVA" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="300.47" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="21.9723" y="300.47" visibility="1" zValue="18" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="97.8188" outlineWidth="0.3" excludeFromExports="0" uuid="{ebf94ef0-b9b3-43ea-a64d-3d0fa448eed5}" height="6.16896" itemRotation="0" frame="false" pagex="21.9723">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="LOCALIZAÃÃO DA FOLHA" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="207.214" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="42.303" y="207.214" visibility="1" zValue="17" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="57.1573" outlineWidth="0.3" excludeFromExports="0" uuid="{52b21987-22d0-4051-a697-5fbcf435f3db}" height="6.16896" itemRotation="0" frame="false" pagex="42.303">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="COBERTURA TERRESTRE" htmlState="0" halign="4">
   <LabelFont description="Arial,7,-1,5,50,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="36.7228" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="713.438" y="36.7228" visibility="1" zValue="16" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="107.776" outlineWidth="0.3" excludeFromExports="0" uuid="{88e1e7e3-3154-46ec-8586-70f83a44994a}" height="4.42097" itemRotation="0" frame="false" pagex="713.438">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="217" blue="217" green="217"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerLabel valign="128" marginX="1" marginY="1" labelText="Diretoria de ServiÃ§o GeogrÃ¡fico" htmlState="0" halign="4">
   <LabelFont description="Arial,10,-1,5,75,0,0,0,0,0" style=""/>
   <FontColor red="0" blue="0" green="0"/>
   <ComposerItem pagey="538.285" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="39.194" y="538.285" visibility="1" zValue="15" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="57.1573" outlineWidth="0.3" excludeFromExports="0" uuid="{a1fb24da-b385-452c-b5ef-71f567ec9d9f}" height="6.16896" itemRotation="0" frame="false" pagex="39.194">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLabel>
  <ComposerMap followPreset="false" mapRotation="ROTACAO" keepLayerSet="false" followPresetName="" id="1" previewMode="Cache" drawCanvasItems="true">
   <Extent ymin="Y_EXT_MIN" xmin="X_EXT_MIN" ymax="Y_EXT_MAX" xmax="X_EXT_MAX"/>
   <LayerSet/>
   <Grid/>
   <ComposerMapGrid rightAnnotationDirection="0" gridFramePenColor="0,0,0,255" show="1" bottomAnnotationPosition="1" annotationPrecision="0" showAnnotation="1" topFrameDivisions="0" uuid="{da609f17-3238-4f97-9397-64cc7e64cbd0}" leftAnnotationDirection="0" topAnnotationPosition="1" rightAnnotationDisplay="0" offsetX="0" offsetY="0" rightFrameDivisions="0" gridStyle="0" annotationFontColor="0,0,0,255" intervalX="1000" gridFrameSideFlags="15" intervalY="1000" bottomAnnotationDirection="0" leftAnnotationDisplay="0" leftFrameDivisions="0" frameFillColor1="255,255,255,255" annotationExpression=" @grid_number  / 1000 " frameFillColor2="0,0,0,255" crossLength="3" gridFramePenThickness="0.29999999999999999" bottomAnnotationDisplay="0" unit="0" topAnnotationDisplay="0" leftAnnotationPosition="1" blendMode="0" gridFrameStyle="0" rightAnnotationPosition="1" gridFrameWidth="2" name="Grade 1" annotationFormat="8" bottomFrameDivisions="0" topAnnotationDirection="0" frameAnnotationDistance="1">
    <lineStyle>
     <symbol alpha="1" clip_to_extent="1" type="line" name="">
      <layer pass="0" class="SimpleLine" locked="0">
       <prop k="capstyle" v="flat"/>
       <prop k="customdash" v="5;2"/>
       <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="customdash_unit" v="MM"/>
       <prop k="draw_inside_polygon" v="0"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="line_color" v="45,45,45,255"/>
       <prop k="line_style" v="solid"/>
       <prop k="line_width" v="0.1"/>
       <prop k="line_width_unit" v="MM"/>
       <prop k="offset" v="0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="use_custom_dash" v="0"/>
       <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
      </layer>
     </symbol>
    </lineStyle>
    <markerStyle>
     <symbol alpha="1" clip_to_extent="1" type="marker" name="">
      <layer pass="0" class="SimpleMarker" locked="0">
       <prop k="angle" v="0"/>
       <prop k="color" v="0,0,0,255"/>
       <prop k="horizontal_anchor_point" v="1"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="name" v="circle"/>
       <prop k="offset" v="0,0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="outline_color" v="0,0,0,255"/>
       <prop k="outline_style" v="solid"/>
       <prop k="outline_width" v="0"/>
       <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="outline_width_unit" v="MM"/>
       <prop k="scale_method" v="diameter"/>
       <prop k="size" v="2"/>
       <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="size_unit" v="MM"/>
       <prop k="vertical_anchor_point" v="1"/>
      </layer>
     </symbol>
    </markerStyle>
    <spatialrefsys>
     <proj4>+proj=utm +zone=25 +south +datum=WGS84 +units=m +no_defs</proj4>
     <srsid>3175</srsid>
     <srid>32725</srid>
     <authid>EPSG:32725</authid>
     <description>WGS 84 / UTM zone 25S</description>
     <projectionacronym>utm</projectionacronym>
     <ellipsoidacronym>WGS84</ellipsoidacronym>
     <geographicflag>false</geographicflag>
    </spatialrefsys>
    <annotationFontProperties description="Arial,7,-1,5,50,0,0,0,0,0" style=""/>
   </ComposerMapGrid>
   <ComposerMapGrid rightAnnotationDirection="2" gridFramePenColor="92,92,92,255" show="1" bottomAnnotationPosition="1" annotationPrecision="1" showAnnotation="1" topFrameDivisions="0" uuid="{780cfa79-8e42-4449-b2cd-401b558b35c9}" leftAnnotationDirection="1" topAnnotationPosition="1" rightAnnotationDisplay="0" offsetX="0" offsetY="0" rightFrameDivisions="0" gridStyle="1" annotationFontColor="92,92,92,255" intervalX="0.025" gridFrameSideFlags="15" intervalY="0.025" bottomAnnotationDirection="0" leftAnnotationDisplay="0" leftFrameDivisions="0" frameFillColor1="255,255,255,255" annotationExpression="" frameFillColor2="0,0,0,255" crossLength="3" gridFramePenThickness="0.10000000000000001" bottomAnnotationDisplay="3" unit="0" topAnnotationDisplay="3" leftAnnotationPosition="1" blendMode="0" gridFrameStyle="2" rightAnnotationPosition="1" gridFrameWidth="3" name="Grade 2" annotationFormat="2" bottomFrameDivisions="0" topAnnotationDirection="0" frameAnnotationDistance="8">
    <lineStyle>
     <symbol alpha="1" clip_to_extent="1" type="line" name="">
      <layer pass="0" class="SimpleLine" locked="0">
       <prop k="capstyle" v="flat"/>
       <prop k="customdash" v="5;2"/>
       <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="customdash_unit" v="MM"/>
       <prop k="draw_inside_polygon" v="0"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="line_color" v="72,72,72,255"/>
       <prop k="line_style" v="solid"/>
       <prop k="line_width" v="0.2"/>
       <prop k="line_width_unit" v="MM"/>
       <prop k="offset" v="0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="use_custom_dash" v="0"/>
       <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
      </layer>
     </symbol>
    </lineStyle>
    <markerStyle>
     <symbol alpha="1" clip_to_extent="1" type="marker" name="">
      <layer pass="0" class="SimpleMarker" locked="0">
       <prop k="angle" v="0"/>
       <prop k="color" v="0,0,0,255"/>
       <prop k="horizontal_anchor_point" v="1"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="name" v="circle"/>
       <prop k="offset" v="0,0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="outline_color" v="0,0,0,255"/>
       <prop k="outline_style" v="solid"/>
       <prop k="outline_width" v="0"/>
       <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="outline_width_unit" v="MM"/>
       <prop k="scale_method" v="diameter"/>
       <prop k="size" v="2"/>
       <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="size_unit" v="MM"/>
       <prop k="vertical_anchor_point" v="1"/>
      </layer>
     </symbol>
    </markerStyle>
    <spatialrefsys>
     <proj4>+proj=longlat +datum=WGS84 +no_defs</proj4>
     <srsid>3452</srsid>
     <srid>4326</srid>
     <authid>EPSG:4326</authid>
     <description>WGS 84</description>
     <projectionacronym>longlat</projectionacronym>
     <ellipsoidacronym>WGS84</ellipsoidacronym>
     <geographicflag>true</geographicflag>
    </spatialrefsys>
    <annotationFontProperties description="Arial,6,-1,5,50,0,0,0,0,0" style=""/>
   </ComposerMapGrid>
   <ComposerMapGrid rightAnnotationDirection="0" gridFramePenColor="0,0,0,255" show="1" bottomAnnotationPosition="1" annotationPrecision="1" showAnnotation="1" topFrameDivisions="0" uuid="{75289ed4-28f8-4e63-b89b-979b4897e68c}" leftAnnotationDirection="0" topAnnotationPosition="1" rightAnnotationDisplay="3" offsetX="0" offsetY="0" rightFrameDivisions="0" gridStyle="3" annotationFontColor="92,92,92,255" intervalX="0.025" gridFrameSideFlags="15" intervalY="0.025" bottomAnnotationDirection="0" leftAnnotationDisplay="3" leftFrameDivisions="0" frameFillColor1="255,255,255,255" annotationExpression="" frameFillColor2="0,0,0,255" crossLength="3" gridFramePenThickness="0.29999999999999999" bottomAnnotationDisplay="0" unit="0" topAnnotationDisplay="0" leftAnnotationPosition="1" blendMode="0" gridFrameStyle="0" rightAnnotationPosition="1" gridFrameWidth="2" name="Grade 3" annotationFormat="2" bottomFrameDivisions="0" topAnnotationDirection="0" frameAnnotationDistance="4">
    <lineStyle>
     <symbol alpha="1" clip_to_extent="1" type="line" name="">
      <layer pass="0" class="SimpleLine" locked="0">
       <prop k="capstyle" v="flat"/>
       <prop k="customdash" v="5;2"/>
       <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="customdash_unit" v="MM"/>
       <prop k="draw_inside_polygon" v="0"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="line_color" v="0,0,0,255"/>
       <prop k="line_style" v="solid"/>
       <prop k="line_width" v="0.3"/>
       <prop k="line_width_unit" v="MM"/>
       <prop k="offset" v="0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="use_custom_dash" v="0"/>
       <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
      </layer>
     </symbol>
    </lineStyle>
    <markerStyle>
     <symbol alpha="1" clip_to_extent="1" type="marker" name="">
      <layer pass="0" class="SimpleMarker" locked="0">
       <prop k="angle" v="0"/>
       <prop k="color" v="0,0,0,255"/>
       <prop k="horizontal_anchor_point" v="1"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="name" v="circle"/>
       <prop k="offset" v="0,0"/>
       <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="outline_color" v="0,0,0,255"/>
       <prop k="outline_style" v="solid"/>
       <prop k="outline_width" v="0"/>
       <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="outline_width_unit" v="MM"/>
       <prop k="scale_method" v="diameter"/>
       <prop k="size" v="2"/>
       <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
       <prop k="size_unit" v="MM"/>
       <prop k="vertical_anchor_point" v="1"/>
      </layer>
     </symbol>
    </markerStyle>
    <spatialrefsys>
     <proj4>+proj=longlat +datum=WGS84 +no_defs</proj4>
     <srsid>3452</srsid>
     <srid>4326</srid>
     <authid>EPSG:4326</authid>
     <description>WGS 84</description>
     <projectionacronym>longlat</projectionacronym>
     <ellipsoidacronym>WGS84</ellipsoidacronym>
     <geographicflag>true</geographicflag>
    </spatialrefsys>
    <annotationFontProperties description="Arial,6,-1,5,50,0,0,0,0,0" style=""/>
   </ComposerMapGrid>
   <AtlasMap scalingMode="2" atlasDriven="0" margin="0"/>
   <ComposerItem pagey="17.578" page="1" id="" lastValidViewScaleFactor="3.77953" positionMode="0" positionLock="false" x="140.441" y="17.578" visibility="1" zValue="14" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="LARGURA" outlineWidth="0.3" excludeFromExports="0" uuid="{699e8201-4b47-4fff-b608-50d59d7cfe76}" height="ALTURA" itemRotation="0" frame="true" pagex="140.441">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerMap>
  <ComposerLegend symbolWidth="7" title="" rasterBorderWidth="0.1" titleAlignment="1" map="1" wmsLegendWidth="50" rasterBorderColor="0,0,0,255" wrapChar="" fontColor="#000000" legendFilterByAtlas="0" columnCount="1" wmsLegendHeight="25" columnSpace="2" symbolHeight="4" equalColumnWidth="0" resizeToContents="1" splitLayer="1" boxSpace="2" rasterBorder="1">
   <styles>
    <style name="title">
     <styleFont description="MS Shell Dlg 2,7,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="group">
     <styleFont description="MS Shell Dlg 2,1,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style name="subgroup">
     <styleFont description="MS Shell Dlg 2,1,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" name="symbol">
     <styleFont description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
    </style>
    <style marginTop="2" marginLeft="3" name="symbolLabel">
     <styleFont description="Arial,8,-1,5,50,0,0,0,0,0" style=""/>
    </style>
   </styles>
   <layer-tree-group expanded="1" checked="Qt::Checked" name="">
    <customproperties/>
    <layer-tree-layer expanded="1" providerKey="postgres" checked="Qt::Checked" id="cob_ter_a20180305083928280" source="dbname='NOME_BANCO' host=localhost port=5432 user='postgres' key='id' selectatid=false table=&quot;base&quot;.&quot;cob_ter_a&quot; (geom) sql=id in (SELECT id FROM ONLY &quot;base&quot;.&quot;cob_ter_a&quot;)" name="cob_ter_a">
     <customproperties>
      <property key="legend/label-3" value="Terreno Exposto"/>
      <property key="legend/label-4" value="Ãrea Ãmida"/>
      <property key="legend/label-5" value="Massa d'Ãgua"/>
      <property key="legend/node-order" value="3,4,5,6"/>
      <property key="legend/title-label" value=""/>
     </customproperties>
    </layer-tree-layer>
   </layer-tree-group>
   <ComposerItem pagey="42.5429" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="776.153" y="42.5429" visibility="1" zValue="13" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="34.2" outlineWidth="0.3" excludeFromExports="0" uuid="{636aa128-eee2-4563-872a-087beff46d11}" height="28" itemRotation="0" frame="false" pagex="776.153">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerLegend>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,0"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.1"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="10.2529" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="710.55" y="10.2529" visibility="1" zValue="12" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="114.402" outlineWidth="0.3" excludeFromExports="0" uuid="{7d9d4be4-506f-4d5c-8ddb-9db198df1e2d}" height="573.863" itemRotation="0" frame="false" pagex="710.55">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="7.78027" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="12.6055" y="7.78027" visibility="1" zValue="11" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{0e709c3f-3fb0-4db4-a971-f9be5bd35a75}" height="2.14814" itemRotation="0" frame="false" pagex="12.6055">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="7.78027" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="128.593" y="7.78027" visibility="1" zValue="10" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{1615d604-42fa-4461-80c7-e9859fe6cc5c}" height="2.14814" itemRotation="0" frame="false" pagex="128.593">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="7.78027" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="244.553" y="7.78027" visibility="1" zValue="9" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{befa73b2-4ae0-4341-a536-5aca28736944}" height="2.14814" itemRotation="0" frame="false" pagex="244.553">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="7.78027" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="592.424" y="7.78027" visibility="1" zValue="8" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{e0b5b8c8-6cf8-4a9c-8480-11a206ab3160}" height="2.14814" itemRotation="0" frame="false" pagex="592.424">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="7.78027" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="476.448" y="7.78027" visibility="1" zValue="7" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{34471edf-0d61-432e-a203-94aded4a9b48}" height="2.14814" itemRotation="0" frame="false" pagex="476.448">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="7.78027" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="708.434" y="7.78027" visibility="1" zValue="6" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="119.825" outlineWidth="0.3" excludeFromExports="0" uuid="{5405b867-1a88-47a6-abf4-1cc15be079dd}" height="2.14814" itemRotation="0" frame="false" pagex="708.434">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,255"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="200,200,200,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.2"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="7.78027" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="360.512" y="7.78027" visibility="1" zValue="5" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="115.98" outlineWidth="0.3" excludeFromExports="0" uuid="{a4242482-2e9d-48ed-b284-5258e7172b9d}" height="2.14814" itemRotation="0" frame="false" pagex="360.512">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerPicture resizeMode="3" svgBorderWidth="0.2" pictureRotation="0" pictureWidth="74.5589" svgFillColor="255,255,255,255" svgBorderColor="0,0,0,255" northMode="0" file="PASTA_COM_FIGURAS/articulacao.png" northOffset="0" pictureHeight="74.5589" mapId="-1" anchorPoint="4">
   <ComposerItem pagey="403.318" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="32.1566" y="403.318" visibility="1" zValue="4" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="74.5589" outlineWidth="0.3" excludeFromExports="0" uuid="{6e97f803-f95f-407b-a965-1b6a697970d4}" height="74.5589" itemRotation="0" frame="true" pagex="32.1566">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <dataDefinedSource expr="" field="" active="false" useExpr="true"/>
    <customproperties/>
   </ComposerItem>
  </ComposerPicture>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,0"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="63,63,63,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.1"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="10.075" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="15.205" y="10.075" visibility="1" zValue="3" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="809.747" outlineWidth="0.3" excludeFromExports="0" uuid="{9b8d5599-d764-4379-ba49-3fc4ae57e768}" height="573.898" itemRotation="0" frame="false" pagex="15.205">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,0"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="63,63,63,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.1"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="7.67865" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="12.6906" y="7.67865" visibility="1" zValue="2" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="815.671" outlineWidth="0.3" excludeFromExports="0" uuid="{5d71251c-d7f1-4386-b89f-e323fbc60745}" height="578.561" itemRotation="0" frame="false" pagex="12.6906">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerShape shapeType="1" cornerRadius="0">
   <symbol alpha="1" clip_to_extent="1" type="fill" name="">
    <layer pass="0" class="SimpleFill" locked="0">
     <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="color" v="255,255,255,0"/>
     <prop k="joinstyle" v="miter"/>
     <prop k="offset" v="0,0"/>
     <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_color" v="0,0,0,255"/>
     <prop k="outline_style" v="solid"/>
     <prop k="outline_width" v="0.1"/>
     <prop k="outline_width_unit" v="MM"/>
     <prop k="style" v="solid"/>
    </layer>
   </symbol>
   <ComposerItem pagey="10.0071" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="15.182" y="10.0071" visibility="1" zValue="1" background="true" transparency="0" frameJoinStyle="miter" blendMode="0" width="111.4" outlineWidth="0.3" excludeFromExports="0" uuid="{3a12ea1e-3481-43d1-86d2-7cbca4b5f668}" height="573.863" itemRotation="0" frame="false" pagex="15.182">
    <FrameColor alpha="255" red="0" blue="0" green="0"/>
    <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
    <customproperties/>
   </ComposerItem>
  </ComposerShape>
  <ComposerHtml maxBreakDistance="10" contentMode="1" resizeMode="0" url="" useSmartBreaks="true" evaluateExpressions="true" html="&lt;!DOCTYPE html PUBLIC &quot;-//W3C//DTD HTML 4.01 Transitional//EN&quot;>&#xd;&#xa;&lt;html>&#xd;&#xa;&lt;head>&#xd;&#xa;  &lt;meta content=&quot;text/html; charset=ISO-8859-1&quot;&#xd;&#xa; http-equiv=&quot;content-type&quot;>&#xd;&#xa;  &lt;title>DM e CM&lt;/title>&#xd;&#xa;&lt;/head>&#xd;&#xa;&lt;body style=&quot;width: 336px;&quot;>&#xd;&#xa;&lt;table&#xd;&#xa; style=&quot;text-align: left; margin-left: 0px; margin-right: auto; height: 90px; width: 397px;&quot;&#xd;&#xa; border=&quot;1&quot; cellpadding=&quot;0&quot; cellspacing=&quot;0&quot;>&#xd;&#xa;  &lt;tbody>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Ortofoto&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>UFPE&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;font-family: Arial;&quot;>&amp;nbsp;Modelo&#xd;&#xa;Digital do Terreno&lt;/td>&#xd;&#xa;      &lt;td style=&quot;text-align: center; font-family: Arial;&quot;>UFPE&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Divis&amp;atilde;o&#xd;&#xa;Territorial&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>IBGE&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Rodovias&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>OSM&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;  &lt;/tbody>&#xd;&#xa;&lt;/table>&#xd;&#xa;&lt;div style=&quot;text-align: left;&quot;>&lt;br>&#xd;&#xa;&lt;/div>&#xd;&#xa;&lt;/body>&#xd;&#xa;&lt;/html>" stylesheetEnabled="false" stylesheet="">
   <ComposerFrame sectionWidth="100.924" sectionHeight="24.96" hideBackgroundIfEmpty="0" hidePageIfEmpty="0" sectionX="0" sectionY="0">
    <ComposerItem pagey="552.91" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="717.288" y="552.91" visibility="1" zValue="68" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="100.924" outlineWidth="0.3" excludeFromExports="0" uuid="{2a2b1bc5-e1ba-4004-8c92-1574039ed4e3}" height="26.4325" itemRotation="0" frame="false" pagex="717.288">
     <FrameColor alpha="255" red="0" blue="0" green="0"/>
     <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
     <customproperties/>
    </ComposerItem>
   </ComposerFrame>
   <customproperties/>
  </ComposerHtml>
  <ComposerHtml maxBreakDistance="10" contentMode="1" resizeMode="0" url="" useSmartBreaks="true" evaluateExpressions="true" html="&lt;!DOCTYPE html PUBLIC &quot;-//W3C//DTD HTML 4.01 Transitional//EN&quot;>&#xd;&#xa;&lt;html>&#xd;&#xa;&lt;head>&#xd;&#xa;  &lt;meta content=&quot;text/html; charset=ISO-8859-1&quot;&#xd;&#xa; http-equiv=&quot;content-type&quot;>&#xd;&#xa;  &lt;title>&lt;/title>&#xd;&#xa;&lt;/head>&#xd;&#xa;&lt;body style=&quot;width: 336px;&quot;>&#xd;&#xa;&lt;table&#xd;&#xa; style=&quot;text-align: left; margin-left: 0px; margin-right: auto; width: 327px; height: 90px;&quot;&#xd;&#xa; border=&quot;1&quot; cellpadding=&quot;0&quot; cellspacing=&quot;0&quot;>&#xd;&#xa;  &lt;tbody>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;font-family: Arial; width: 227px;&quot;>&amp;nbsp;Converg&amp;ecirc;ncia&#xd;&#xa;Meridiana (CM)&lt;/td>&#xd;&#xa;      &lt;td style=&quot;text-align: center; width: 90px;&quot;>&amp;nbsp;CONV_MER;&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;font-family: Arial; width: 227px;&quot;>&amp;nbsp;Declina&amp;ccedil;&amp;atilde;o&#xd;&#xa;Magn&amp;eacute;tica (DM)&lt;/td>&#xd;&#xa;      &lt;td style=&quot;width: 90px; text-align: center;&quot;>DECL_MAGN;&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;font-family: Arial; width: 227px;&quot;>&amp;nbsp;Taxa&#xd;&#xa;de Varia&amp;ccedil;&amp;atilde;o da DM&lt;/td>&#xd;&#xa;      &lt;td style=&quot;width: 90px; text-align: center;&quot;>VAR_DECL_MAGN;&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 227px;&quot;>&lt;span&#xd;&#xa; style=&quot;font-family: Arial;&quot;>&amp;nbsp;Ano de&#xd;&#xa;Refer&amp;ecirc;ncia&lt;/span>&lt;/td>&#xd;&#xa;      &lt;td style=&quot;width: 90px; text-align: center;&quot;>2018&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;  &lt;/tbody>&#xd;&#xa;&lt;/table>&#xd;&#xa;&lt;div style=&quot;text-align: left;&quot;>&lt;br>&#xd;&#xa;&lt;/div>&#xd;&#xa;&lt;/body>&#xd;&#xa;&lt;/html>" stylesheetEnabled="false" stylesheet="">
   <ComposerFrame sectionWidth="85.4683" sectionHeight="25.2" hideBackgroundIfEmpty="0" hidePageIfEmpty="0" sectionX="0" sectionY="0">
    <ComposerItem pagey="335.387" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="724.592" y="335.387" visibility="1" zValue="65" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="85.4683" outlineWidth="0.3" excludeFromExports="0" uuid="{904aa28b-03c1-4336-9490-a1dfbc34d5e8}" height="27.0267" itemRotation="0" frame="false" pagex="724.592">
     <FrameColor alpha="255" red="0" blue="0" green="0"/>
     <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
     <customproperties/>
    </ComposerItem>
   </ComposerFrame>
   <customproperties/>
  </ComposerHtml>
  <ComposerHtml maxBreakDistance="10" contentMode="1" resizeMode="0" url="" useSmartBreaks="true" evaluateExpressions="true" html="&lt;!DOCTYPE html PUBLIC &quot;-//W3C//DTD HTML 4.01 Transitional//EN&quot;>&#xd;&#xa;&lt;html>&#xd;&#xa;&lt;head>&#xd;&#xa;  &lt;meta content=&quot;text/html; charset=ISO-8859-1&quot;&#xd;&#xa; http-equiv=&quot;content-type&quot;>&#xd;&#xa;  &lt;title>DM e CM&lt;/title>&#xd;&#xa;&lt;/head>&#xd;&#xa;&lt;body style=&quot;width: 336px;&quot;>&#xd;&#xa;&lt;table&#xd;&#xa; style=&quot;text-align: left; margin-left: 0px; margin-right: auto; height: 90px; width: 397px;&quot;&#xd;&#xa; border=&quot;1&quot; cellpadding=&quot;0&quot; cellspacing=&quot;0&quot;>&#xd;&#xa;  &lt;tbody>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 209px; font-family: Arial;&quot;>FASES&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>EXECUTANTE&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 64px; font-family: Arial;&quot;>ANO&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Voo&#xd;&#xa;LIDAR&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>Esteio&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 64px; font-family: Arial;&quot;>2015&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Gera&amp;ccedil;&amp;atilde;o&#xd;&#xa;de curvas de n&amp;iacute;vel&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>3&amp;ordm;&#xd;&#xa;CGEO&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 64px; font-family: Arial;&quot;>2018&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Aquisi&amp;ccedil;&amp;atilde;o&#xd;&#xa;de dados &lt;br>&#xd;&#xa;&amp;nbsp;geoespaciais&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>3&amp;ordm;&#xd;&#xa;CGEO&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 64px; font-family: Arial;&quot;>2018&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Valida&amp;ccedil;&amp;atilde;o&#xd;&#xa;dos dados&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>3&amp;ordm;&#xd;&#xa;CGEO&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 64px; font-family: Arial;&quot;>2018&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Edi&amp;ccedil;&amp;atilde;o&#xd;&#xa;da carta&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>3&amp;ordm;&#xd;&#xa;CGEO&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 64px; font-family: Arial;&quot;>2018&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;  &lt;/tbody>&#xd;&#xa;&lt;/table>&#xd;&#xa;&lt;div style=&quot;text-align: left;&quot;>&lt;br>&#xd;&#xa;&lt;/div>&#xd;&#xa;&lt;/body>&#xd;&#xa;&lt;/html>" stylesheetEnabled="false" stylesheet="">
   <ComposerFrame sectionWidth="101.904" sectionHeight="40.32" hideBackgroundIfEmpty="0" hidePageIfEmpty="0" sectionX="0" sectionY="0">
    <ComposerItem pagey="391.892" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="716.798" y="391.892" visibility="1" zValue="66" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="101.904" outlineWidth="0.3" excludeFromExports="0" uuid="{16916bc4-bcf8-4b62-83a0-13ea6d864937}" height="43.8064" itemRotation="0" frame="false" pagex="716.798">
     <FrameColor alpha="255" red="0" blue="0" green="0"/>
     <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
     <customproperties/>
    </ComposerItem>
   </ComposerFrame>
   <customproperties/>
  </ComposerHtml>
  <ComposerHtml maxBreakDistance="10" contentMode="1" resizeMode="0" url="" useSmartBreaks="true" evaluateExpressions="true" html="&lt;!DOCTYPE html PUBLIC &quot;-//W3C//DTD HTML 4.01 Transitional//EN&quot;>&#xd;&#xa;&lt;html>&#xd;&#xa;&lt;head>&#xd;&#xa;  &lt;meta content=&quot;text/html; charset=ISO-8859-1&quot;&#xd;&#xa; http-equiv=&quot;content-type&quot;>&#xd;&#xa;  &lt;title>DM e CM&lt;/title>&#xd;&#xa;&lt;/head>&#xd;&#xa;&lt;body style=&quot;width: 336px;&quot;>&#xd;&#xa;&lt;table&#xd;&#xa; style=&quot;text-align: left; margin-left: 0px; margin-right: auto; height: 90px; width: 397px;&quot;&#xd;&#xa; border=&quot;1&quot; cellpadding=&quot;0&quot; cellspacing=&quot;0&quot;>&#xd;&#xa;  &lt;tbody>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Sistema&#xd;&#xa;de Refer&amp;ecirc;ncia de&lt;br>&#xd;&#xa;&amp;nbsp;Coordenadas (SRC)&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>SIRGAS&#xd;&#xa;2000&lt;br>&#xd;&#xa;UTM 25 S&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;font-family: Arial;&quot;>&amp;nbsp;Proje&amp;ccedil;&amp;atilde;o&lt;/td>&#xd;&#xa;      &lt;td style=&quot;text-align: center; font-family: Arial;&quot;>Transversa&#xd;&#xa;de Mercator&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Meridiano&#xd;&#xa;Central&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>-33&amp;deg;&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Fuso&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>25&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Datum&#xd;&#xa;Horizontal&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>SIRGAS&#xd;&#xa;2000&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;width: 209px; font-family: Arial;&quot;>&amp;nbsp;Datum&#xd;&#xa;Vertical&lt;/td>&#xd;&#xa;      &lt;td&#xd;&#xa; style=&quot;text-align: center; width: 120px; font-family: Arial;&quot;>Imbituba&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;font-family: Arial;&quot;>&amp;nbsp;Equidist&amp;acirc;ncia&#xd;&#xa;das &lt;br>&#xd;&#xa;&amp;nbsp;Curvas de N&amp;iacute;vel&lt;/td>&#xd;&#xa;      &lt;td style=&quot;text-align: center; font-family: Arial;&quot;>10&#xd;&#xa;m&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;    &lt;tr>&#xd;&#xa;      &lt;td style=&quot;font-family: Arial;&quot;>SRID/ EPSG&lt;/td>&#xd;&#xa;      &lt;td style=&quot;text-align: center; font-family: Arial;&quot;>31985&lt;/td>&#xd;&#xa;    &lt;/tr>&#xd;&#xa;  &lt;/tbody>&#xd;&#xa;&lt;/table>&#xd;&#xa;&lt;div style=&quot;text-align: left;&quot;>&lt;br>&#xd;&#xa;&lt;/div>&#xd;&#xa;&lt;/body>&#xd;&#xa;&lt;/html>" stylesheetEnabled="false" stylesheet="">
   <ComposerFrame sectionWidth="100.924" sectionHeight="54" hideBackgroundIfEmpty="0" hidePageIfEmpty="0" sectionX="0" sectionY="0">
    <ComposerItem pagey="467.654" page="1" id="" lastValidViewScaleFactor="-1" positionMode="0" positionLock="false" x="716.798" y="467.654" visibility="1" zValue="67" background="false" transparency="0" frameJoinStyle="miter" blendMode="0" width="100.924" outlineWidth="0.3" excludeFromExports="0" uuid="{b44f4ffa-ec2c-4135-83b4-4b5331d0698e}" height="56.22" itemRotation="0" frame="false" pagex="716.798">
     <FrameColor alpha="255" red="0" blue="0" green="0"/>
     <BackgroundColor alpha="255" red="255" blue="255" green="255"/>
     <customproperties/>
    </ComposerItem>
   </ComposerFrame>
   <customproperties/>
  </ComposerHtml>
  <customproperties/>
 </Composition>
</Composer>
'''

texto = texto.decode('utf-8')
# Inserir Valores
for item in parametros.keys():
    texto = texto.replace(item, parametros[item])

# Escrever Arquivo
if Modelo[-4:] != '.qpt':
    Modelo += '.qpt'

texto = texto.encode('utf-8')
arquivo = open(Modelo, 'w')
arquivo.write(texto)
arquivo.close()

progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(5)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
