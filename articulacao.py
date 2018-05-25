
"""
/***************************************************************************
 LEOXINGU
                              -------------------
        begin                : 2018-05-24
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
# Criar articulacao da folha
##5. Articulacao=name
##LF10) Cartografia=group
##Moldura=vector
#Articulacao=selection 1:25.000;1:50.000;100.000
##Arquivo_SVG=output file

from PyQt4.QtCore import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from qgis.core import *
import time
import processing
from numpy import sign, array
from math import floor

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


def map_sistem(lon, lat):
    nome = ''
    sinal = sign(lat)
    if sinal == -1:
        nome+='S'
    else:
        nome+='N'
    # Determinacao da letra
    letra = chr(int(65+floor(abs(lat)/4.0)))
    nome+=letra
    # Calculo do Fuso
    fuso = round((183+lon)/6.0)
    nome+='-'+str(int(fuso))
    # Calculo do Meridiano Central
    MC = 6*fuso-183
    valores = array([[3.0, 1.5, 0.5, 0.25, 0.125],[2.0, 1.0, 0.5, 0.25, 0.125]])
    # Escala 1:500.000
    centro = array([MC, 4.0*floor(lat/4.0)+valores[1][0]])
    sinal = sign(array([lon, lat]) - centro)
    if sinal[0]==-1 and sinal[1]==1:
        nome+='-V'
    elif sinal[0]==1 and sinal[1]==1:
        nome+='-X'
    elif sinal[0]==-1 and sinal[1]==-1:
        nome+='-Y'
    elif sinal[0]==1 and sinal[1]==-1:
        nome+='-Z'
    # Escala 1:250.000
    centro = centro + sinal*valores[:,1]
    sinal = sign(array([lon, lat]) - centro)
    if sinal[0]==-1 and sinal[1]==1:
        nome+='-A'
    elif sinal[0]==1 and sinal[1]==1:
        nome+='-B'
    elif sinal[0]==-1 and sinal[1]==-1:
        nome+='-C'
    elif sinal[0]==1 and sinal[1]==-1:
        nome+='-D'
    # Escala 1:100.000
    ok = False
    if sinal[0]==1:
        c1 = centro + sinal*valores[:,2]
        sinal_ = sign(array([lon, lat]) - c1)
        if sinal_[0]==-1 and sinal_[1]==1:
            nome+='-I'
            ok = True
            centro = c1
            sinalx = sinal_
        elif sinal_[0]==-1 and sinal_[1]==-1:
            nome+='-IV'
            ok = True
            centro = c1
            sinalx = sinal_
        c2 = centro + array([2*sinal[0], sinal[1]])*valores[:,2]
        sinal_ = sign(array([lon, lat]) - c2)
        if sinal_[0]==1 and sinal_[1]==1 and ok == False:
            nome+='-III'
            centro = c2
            sinalx = sinal_
        elif sinal_[0]==1 and sinal_[1]==-1 and ok == False:
            nome+='-VI'
            centro = c2
            sinalx = sinal_
        elif sinal_[0]==-1 and sinal_[1]==1 and ok == False:
            nome+='-II'
            centro = c2
            sinalx = sinal_
        elif sinal_[0]==-1 and sinal_[1]==-1 and ok == False:
            nome+='-V'
            centro = c2
            sinalx = sinal_
    elif sinal[0]==-1:
        c1 = centro + sinal*valores[:,2]
        sinal_ = sign(array([lon, lat]) - c1)
        if sinal_[0]==1 and sinal_[1]==1:
            nome+='-III'
            ok = True
            centro = c1
            sinalx = sinal_
        elif sinal_[0]==1 and sinal_[1]==-1:
            nome+='-VI'
            ok = True
            centro = c1
            sinalx = sinal_
        c2 = centro + array([2*sinal[0], sinal[1]])*valores[:,2]
        sinal_ = sign(array([lon, lat]) - c2)
        if sinal_[0]==1 and sinal_[1]==1 and ok == False:
            nome+='-II'
            centro = c2
            sinalx = sinal_
        elif sinal_[0]==1 and sinal_[1]==-1 and ok == False:
            nome+='-V'
            centro = c2
            sinalx = sinal_
        elif sinal_[0]==-1 and sinal_[1]==1 and ok == False:
            nome+='-I'
            centro = c2
            sinalx = sinal_
        elif sinal_[0]==-1 and sinal_[1]==-1 and ok == False:
            nome+='-IV'
            centro = c2
            sinalx = sinal_
    sinal = sinalx
    # Escala 1:50.000
    centro = centro + sinal*valores[:,3]
    sinal = sign(array([lon, lat]) - centro)
    if sinal[0]==-1 and sinal[1]==1:
        nome+='-1'
    elif sinal[0]==1 and sinal[1]==1:
        nome+='-2'
    elif sinal[0]==-1 and sinal[1]==-1:
        nome+='-3'
    elif sinal[0]==1 and sinal[1]==-1:
        nome+='-4'
    # Escala 1:25.000
    centro = centro + sinal*valores[:,4]
    sinal = sign(array([lon, lat]) - centro)
    if sinal[0]==-1 and sinal[1]==1:
        nome+='-NO'
    elif sinal[0]==1 and sinal[1]==1:
        nome+='-NE'
    elif sinal[0]==-1 and sinal[1]==-1:
        nome+='-SO'
    elif sinal[0]==1 and sinal[1]==-1:
        nome+='-SE'
        
    return nome

dicionario = {'SB-21-V-A-I': '709',
                'SB-21-V-A-II': '710',
                'SB-21-V-A-III': '711',
                'SB-21-V-A-IV': '779',
                'SB-21-V-A-V': '780',
                'SB-21-V-A-VI': '781',
                'SB-21-V-B-I': '712',
                'SB-21-V-B-II': '713',
                'SB-21-V-B-III': '714',
                'SB-21-V-B-IV': '782',
                'SB-21-V-B-V': '783',
                'SB-21-V-B-VI': '784',
                'SB-21-V-C-I': '852',
                'SB-21-V-C-II': '853',
                'SB-21-V-C-III': '854',
                'SB-21-V-C-IV': '929',
                'SB-21-V-C-V': '930',
                'SB-21-V-C-VI': '931',
                'SB-21-V-D-I': '855',
                'SB-21-V-D-II': '856',
                'SB-21-V-D-III': '857',
                'SB-21-V-D-IV': '932',
                'SB-21-V-D-V': '933',
                'SB-21-V-D-VI': '934',
                'SB-21-X-A-I': '715',
                'SB-21-X-A-II': '716',
                'SB-21-X-A-III': '717',
                'SB-21-X-A-IV': '785',
                'SB-21-X-A-V': '786',
                'SB-21-X-A-VI': '787',
                'SB-21-X-B-I': '718',
                'SB-21-X-B-II': '719',
                'SB-21-X-B-III': '720',
                'SB-21-X-B-IV': '788',
                'SB-21-X-B-V': '789',
                'SB-21-X-B-VI': '790',
                'SB-21-X-C-I': '858',
                'SB-21-X-C-II': '859',
                'SB-21-X-C-III': '860',
                'SB-21-X-C-IV': '935',
                'SB-21-X-C-V': '936',
                'SB-21-X-C-VI': '937',
                'SB-21-X-D-I': '861',
                'SB-21-X-D-II': '862',
                'SB-21-X-D-III': '863',
                'SB-21-X-D-IV': '938',
                'SB-21-X-D-V': '939',
                'SB-21-X-D-VI': '940',
                'SB-21-Y-A-I': '1006',
                'SB-21-Y-A-II': '1007',
                'SB-21-Y-A-III': '1008',
                'SB-21-Y-A-IV': '1085',
                'SB-21-Y-A-V': '1086',
                'SB-21-Y-A-VI': '1087',
                'SB-21-Y-B-I': '1009',
                'SB-21-Y-B-II': '1010',
                'SB-21-Y-B-III': '1011',
                'SB-21-Y-B-IV': '1088',
                'SB-21-Y-B-V': '1089',
                'SB-21-Y-B-VI': '1090',
                'SB-21-Y-C-I': '1164',
                'SB-21-Y-C-II': '1165',
                'SB-21-Y-C-III': '1166',
                'SB-21-Y-C-IV': '1243',
                'SB-21-Y-C-V': '1244',
                'SB-21-Y-C-VI': '1245',
                'SB-21-Y-D-I': '1167',
                'SB-21-Y-D-II': '1168',
                'SB-21-Y-D-III': '1169',
                'SB-21-Y-D-IV': '1246',
                'SB-21-Y-D-V': '1247',
                'SB-21-Y-D-VI': '1248',
                'SB-21-Z-A-I': '1012',
                'SB-21-Z-A-II': '1013',
                'SB-21-Z-A-III': '1014',
                'SB-21-Z-A-IV': '1091',
                'SB-21-Z-A-V': '1092',
                'SB-21-Z-A-VI': '1093',
                'SB-21-Z-B-I': '1015',
                'SB-21-Z-B-II': '1016',
                'SB-21-Z-B-III': '1017',
                'SB-21-Z-B-IV': '1094',
                'SB-21-Z-B-V': '1095',
                'SB-21-Z-B-VI': '1096',
                'SB-21-Z-C-I': '1170',
                'SB-21-Z-C-II': '1171',
                'SB-21-Z-C-III': '1172',
                'SB-21-Z-C-IV': '1249',
                'SB-21-Z-C-V': '1250',
                'SB-21-Z-C-VI': '1251',
                'SB-21-Z-D-I': '1173',
                'SB-21-Z-D-II': '1174',
                'SB-21-Z-D-III': '1175',
                'SB-21-Z-D-IV': '1252',
                'SB-21-Z-D-V': '1253',
                'SB-21-Z-D-VI': '1254',
                'NB-21-Y-A-IV': '2A',
                'NB-21-Y-C-I': '6',
                'NB-21-Y-C-IV': '16',
                'NB-20-Y-C-VI': '7',
                'NB-20-Y-D-IV': '8',
                'NB-20-Y-D-V': '9',
                'NB-20-Z-B-V': '1',
                'NB-20-Z-B-VI': '2',
                'NB-20-Z-C-IV': '10',
                'NB-20-Z-C-V': '11',
                'NB-20-Z-C-VI': '12',
                'NB-20-Z-D-I': '3',
                'NB-20-Z-D-II': '4',
                'NB-20-Z-D-III': '5',
                'NB-20-Z-D-IV': '13',
                'NB-20-Z-D-V': '14',
                'NB-20-Z-D-VI': '15',
                'SF-24-V-A-I': '2577',
                'SF-24-V-A-II': '2578',
                'SF-24-V-A-III': '2579',
                'SF-24-V-A-IV': '2613',
                'SF-24-V-A-V': '2614',
                'SF-24-V-A-VI': '2615',
                'SF-24-V-B-I': '2580',
                'SF-24-V-B-IV': '2616',
                'SF-24-V-C-I': '2649',
                'SF-24-V-C-II': '2650',
                'SF-24-V-C-III': '2651',
                'SF-24-V-C-IV': '2684',
                'SF-24-V-C-V': '2685',
                'SF-24-V-C-VI': '2685A',
                'SF-24-Y-A-I': '2718',
                'SF-24-Y-A-II': '2719',
                'SF-24-Y-A-IV': '2748',
                'SB-25-V-C-I': '900',
                'SB-25-V-C-II': '901',
                'SB-25-V-C-IV': '977',
                'SB-25-V-C-V': '978',
                'SB-25-Y-A-I': '1054',
                'SB-25-Y-A-II': '1055',
                'SB-25-Y-A-III': '1056',
                'SB-25-Y-A-IV': '1133',
                'SB-25-Y-A-V': '1134',
                'SB-25-Y-A-VI': '1135',
                'SB-25-Y-C-I': '1212',
                'SB-25-Y-C-II': '1213',
                'SB-25-Y-C-III': '1214',
                'SB-25-Y-C-IV': '1291',
                'SB-25-Y-C-V': '1292',
                'SB-25-Y-C-VI': '1293',
                'SH-22-V-A-I': '2915',
                'SH-22-V-A-II': '2916',
                'SH-22-V-A-III': '2917',
                'SH-22-V-A-IV': '2931',
                'SH-22-V-A-V': '2932',
                'SH-22-V-A-VI': '2933',
                'SH-22-V-B-I': '2918',
                'SH-22-V-B-II': '2919',
                'SH-22-V-B-III': '2920',
                'SH-22-V-B-IV': '2934',
                'SH-22-V-B-V': '2935',
                'SH-22-V-B-VI': '2936',
                'SH-22-V-C-I': '2948',
                'SH-22-V-C-II': '2949',
                'SH-22-V-C-III': '2950',
                'SH-22-V-C-IV': '2965',
                'SH-22-V-C-V': '2966',
                'SH-22-V-C-VI': '2967',
                'SH-22-V-D-I': '2951',
                'SH-22-V-D-II': '2952',
                'SH-22-V-D-III': '2953',
                'SH-22-V-D-IV': '2968',
                'SH-22-V-D-V': '2969',
                'SH-22-V-D-VI': '2970',
                'SH-22-X-A-I': '2921',
                'SH-22-X-A-II': '2922',
                'SH-22-X-A-III': '2923',
                'SH-22-X-A-IV': '2937',
                'SH-22-X-A-V': '2938',
                'SH-22-X-A-VI': '2939',
                'SH-22-X-B-I': '2924',
                'SH-22-X-B-II': '2925',
                'SH-22-X-B-IV': '2940',
                'SH-22-X-B-V': '2941',
                'SH-22-X-C-I': '2954',
                'SH-22-X-C-II': '2955',
                'SH-22-X-C-III': '2956',
                'SH-22-X-C-IV': '2971',
                'SH-22-X-C-V': '2972',
                'SH-22-X-C-VI': '2973',
                'SH-22-X-D-I': '2957',
                'SH-22-Y-A-I': '2982',
                'SH-22-Y-A-II': '2983',
                'SH-22-Y-A-III': '2984',
                'SH-22-Y-A-IV': '2995',
                'SH-22-Y-A-V': '2996',
                'SH-22-Y-A-VI': '2997',
                'SH-22-Y-B-I': '2985',
                'SH-22-Y-B-II': '2986',
                'SH-22-Y-B-III': '2987',
                'SH-22-Y-B-IV': '2998',
                'SH-22-Y-B-V': '2999',
                'SH-22-Y-B-VI': '3000',
                'SH-22-Y-C-I': '3008',
                'SH-22-Y-C-II': '3009',
                'SH-22-Y-C-III': '3010',
                'SH-22-Y-C-IV': '3017',
                'SH-22-Y-C-V': '3018',
                'SH-22-Y-C-VI': '3019',
                'SH-22-Y-D-I': '3011',
                'SH-22-Y-D-II': '3012',
                'SH-22-Y-D-III': '3013',
                'SH-22-Y-D-IV': '3020',
                'SH-22-Y-D-V': '3021',
                'SH-22-Y-D-VI': '3022',
                'SH-22-Z-A-I': '2988',
                'SH-22-Z-A-II': '2989',
                'SH-22-Z-A-IV': '3001',
                'SH-22-Z-A-V': '3002',
                'SH-22-Z-C-I': '3014',
                'NA-21-V-A-I': '29',
                'NA-21-V-A-IV': '42',
                'NA-21-V-C-I': '56',
                'NA-21-V-C-IV': '75',
                'NA-21-V-D-VI': '76',
                'NA-21-X-C-III': '57',
                'NA-21-X-C-V': '77',
                'NA-21-X-C-VI': '78',
                'NA-21-X-D-I': '58',
                'NA-21-X-D-II': '58A',
                'NA-21-X-D-IV': '79',
                'NA-21-X-D-V': '80',
                'NA-21-X-D-VI': '81',
                'NA-21-Y-A-I': '105',
                'NA-21-Y-A-II': '106',
                'NA-21-Y-A-IV': '143',
                'NA-21-Y-A-V': '144',
                'NA-21-Y-A-VI': '145',
                'NA-21-Y-B-I': '107',
                'NA-21-Y-B-II': '108',
                'NA-21-Y-B-III': '109',
                'NA-21-Y-B-IV': '146',
                'NA-21-Y-B-V': '147',
                'NA-21-Y-B-VI': '148',
                'NA-21-Y-C-I': '184',
                'NA-21-Y-C-II': '185',
                'NA-21-Y-C-III': '186',
                'NA-21-Y-C-IV': '226',
                'NA-21-Y-C-V': '227',
                'NA-21-Y-C-VI': '228',
                'NA-21-Y-D-I': '187',
                'NA-21-Y-D-II': '188',
                'NA-21-Y-D-III': '189',
                'NA-21-Y-D-IV': '229',
                'NA-21-Y-D-V': '230',
                'NA-21-Y-D-VI': '231',
                'NA-21-Z-A-I': '110',
                'NA-21-Z-A-II': '111',
                'NA-21-Z-A-III': '112',
                'NA-21-Z-A-IV': '149',
                'NA-21-Z-A-V': '150',
                'NA-21-Z-A-VI': '151',
                'NA-21-Z-B-I': '113',
                'NA-21-Z-B-II': '114',
                'NA-21-Z-B-III': '115',
                'NA-21-Z-B-IV': '152',
                'NA-21-Z-B-V': '153',
                'NA-21-Z-B-VI': '154',
                'NA-21-Z-C-I': '190',
                'NA-21-Z-C-II': '191',
                'NA-21-Z-C-III': '192',
                'NA-21-Z-C-IV': '232',
                'NA-21-Z-C-V': '233',
                'NA-21-Z-C-VI': '234',
                'NA-21-Z-D-I': '193',
                'NA-21-Z-D-II': '194',
                'NA-21-Z-D-III': '195',
                'NA-21-Z-D-IV': '235',
                'NA-21-Z-D-V': '236',
                'NA-21-Z-D-VI': '237',
                'SC-18-X-A-III': '1294',
                'SC-18-X-B-I': '1295',
                'SC-18-X-B-II': '1296',
                'SC-18-X-B-III': '1297',
                'SC-18-X-B-IV': '1373',
                'SC-18-X-B-V': '1374',
                'SC-18-X-B-VI': '1375',
                'SC-18-X-D-I': '1450',
                'SC-18-X-D-II': '1451',
                'SC-18-X-D-III': '1452',
                'SC-18-X-D-VI': '1527',
                'SF-23-V-A-I': '2565',
                'SF-23-V-A-II': '2566',
                'SF-23-V-A-III': '2567',
                'SF-23-V-A-IV': '2601',
                'SF-23-V-A-V': '2602',
                'SF-23-V-A-VI': '2603',
                'SF-23-V-B-I': '2568',
                'SF-23-V-B-II': '2569',
                'SF-23-V-B-III': '2570',
                'SF-23-V-B-IV': '2604',
                'SF-23-V-B-V': '2605',
                'SF-23-V-B-VI': '2606',
                'SF-23-V-C-I': '2637',
                'SF-23-V-C-II': '2638',
                'SF-23-V-C-III': '2639',
                'SF-23-V-C-IV': '2672',
                'SF-23-V-C-V': '2673',
                'SF-23-V-C-VI': '2674',
                'SF-23-V-D-I': '2640',
                'SF-23-V-D-II': '2641',
                'SF-23-V-D-III': '2642',
                'SF-23-V-D-IV': '2675',
                'SF-23-V-D-V': '2676',
                'SF-23-V-D-VI': '2677',
                'SF-23-X-A-I': '2571',
                'SF-23-X-A-II': '2572',
                'SF-23-X-A-III': '2573',
                'SF-23-X-A-IV': '2607',
                'SF-23-X-A-V': '2608',
                'SF-23-X-A-VI': '2609',
                'SF-23-X-B-I': '2574',
                'SF-23-X-B-II': '2575',
                'SF-23-X-B-III': '2576',
                'SF-23-X-B-IV': '2610',
                'SF-23-X-B-V': '2611',
                'SF-23-X-B-VI': '2612',
                'SF-23-X-C-I': '2643',
                'SF-23-X-C-II': '2644',
                'SF-23-X-C-III': '2645',
                'SF-23-X-C-IV': '2678',
                'SF-23-X-C-V': '2679',
                'SF-23-X-C-VI': '2680',
                'SF-23-X-D-I': '2646',
                'SF-23-X-D-II': '2647',
                'SF-23-X-D-III': '2648',
                'SF-23-X-D-IV': '2681',
                'SF-23-X-D-V': '2682',
                'SF-23-X-D-VI': '2683',
                'SF-23-Y-A-I': '2706',
                'SF-23-Y-A-II': '2707',
                'SF-23-Y-A-III': '2708',
                'SF-23-Y-A-IV': '2736',
                'SF-23-Y-A-V': '2737',
                'SF-23-Y-A-VI': '2738',
                'SF-23-Y-B-I': '2709',
                'SF-23-Y-B-II': '2710',
                'SF-23-Y-B-III': '2711',
                'SF-23-Y-B-IV': '2739',
                'SF-23-Y-B-V': '2740',
                'SF-23-Y-B-VI': '2741',
                'SF-23-Y-C-I': '2765',
                'SF-23-Y-C-II': '2766',
                'SF-23-Y-C-III': '2767',
                'SF-23-Y-C-IV': '2791',
                'SF-23-Y-C-V': '2792',
                'SF-23-Y-C-VI': '2793',
                'SF-23-Y-D-I': '2768',
                'SF-23-Y-D-II': '2769',
                'SF-23-Y-D-III': '2770',
                'SF-23-Y-D-IV': '2794',
                'SF-23-Y-D-V': '2795',
                'SF-23-Y-D-VI': '2796',
                'SF-23-Z-A-I': '2712',
                'SF-23-Z-A-II': '2713',
                'SF-23-Z-A-III': '2714',
                'SF-23-Z-A-IV': '2742',
                'SF-23-Z-A-V': '2743',
                'SF-23-Z-A-VI': '2744',
                'SF-23-Z-B-I': '2715',
                'SF-23-Z-B-II': '2716',
                'SF-23-Z-B-III': '2717',
                'SF-23-Z-B-IV': '2745',
                'SF-23-Z-B-V': '2746',
                'SF-23-Z-B-VI': '2747',
                'SF-23-Z-C-I': '2771',
                'SF-23-Z-C-II': '2772',
                'SF-23-Z-C-III': '2773',
                'SF-23-Z-D-I': '2774',
                'SF-23-Z-D-II': '2774A',
                'SE-21-V-A-I': '2235',
                'SE-21-V-A-II': '2236',
                'SE-21-V-A-III': '2237',
                'SE-21-V-B-I': '2238',
                'SE-21-V-B-II': '2239',
                'SE-21-V-B-III': '2240',
                'SE-21-V-B-IV': '2278',
                'SE-21-V-B-V': '2279',
                'SE-21-V-B-VI': '2280',
                'SE-21-V-D-I': '2318',
                'SE-21-V-D-II': '2319',
                'SE-21-V-D-III': '2320',
                'SE-21-V-D-V': '2357',
                'SE-21-V-D-VI': '2358',
                'SE-21-X-A-I': '2241',
                'SE-21-X-A-II': '2242',
                'SE-21-X-A-III': '2243',
                'SE-21-X-A-IV': '2281',
                'SE-21-X-A-V': '2282',
                'SE-21-X-A-VI': '2283',
                'SE-21-X-B-I': '2244',
                'SE-21-X-B-II': '2245',
                'SE-21-X-B-III': '2246',
                'SE-21-X-B-IV': '2284',
                'SE-21-X-B-V': '2285',
                'SE-21-X-B-VI': '2286',
                'SE-21-X-C-I': '2321',
                'SE-21-X-C-II': '2322',
                'SE-21-X-C-III': '2323',
                'SE-21-X-C-IV': '2359',
                'SE-21-X-C-V': '2360',
                'SE-21-X-C-VI': '2361',
                'SE-21-X-D-I': '2324',
                'SE-21-X-D-II': '2325',
                'SE-21-X-D-III': '2326',
                'SE-21-X-D-IV': '2362',
                'SE-21-X-D-V': '2363',
                'SE-21-X-D-VI': '2364',
                'SE-21-Y-B-II': '2395',
                'SE-21-Y-B-III': '2396',
                'SE-21-Y-B-V': '2432',
                'SE-21-Y-B-VI': '2433',
                'SE-21-Y-D-I': '2468-A',
                'SE-21-Y-D-II': '2469',
                'SE-21-Y-D-III': '2470',
                'SE-21-Y-D-IV': '2506',
                'SE-21-Y-D-V': '2507',
                'SE-21-Y-D-VI': '2508',
                'SE-21-Z-A-I': '2397',
                'SE-21-Z-A-II': '2398',
                'SE-21-Z-A-III': '2399',
                'SE-21-Z-A-IV': '2434',
                'SE-21-Z-A-V': '2435',
                'SE-21-Z-A-VI': '2436',
                'SE-21-Z-B-I': '2400',
                'SE-21-Z-B-II': '2401',
                'SE-21-Z-B-III': '2402',
                'SE-21-Z-B-IV': '2437',
                'SE-21-Z-B-V': '2438',
                'SE-21-Z-B-VI': '2439',
                'SE-21-Z-C-I': '2471',
                'SE-21-Z-C-II': '2472',
                'SE-21-Z-C-III': '2473',
                'SE-21-Z-C-IV': '2509',
                'SE-21-Z-C-V': '2510',
                'SE-21-Z-C-VI': '2511',
                'SE-21-Z-D-I': '2474',
                'SE-21-Z-D-II': '2475',
                'SE-21-Z-D-III': '2476',
                'SE-21-Z-D-IV': '2512',
                'SE-21-Z-D-V': '2513',
                'SE-21-Z-D-VI': '2514',
                'SE-20-X-B-III': '2234',
                'SC-21-V-A-I': '1322',
                'SC-21-V-A-II': '1323',
                'SC-21-V-A-III': '1324',
                'SC-21-V-A-IV': '1400',
                'SC-21-V-A-V': '1401',
                'SC-21-V-A-VI': '1402',
                'SC-21-V-B-I': '1325',
                'SC-21-V-B-II': '1326',
                'SC-21-V-B-III': '1327',
                'SC-21-V-B-IV': '1403',
                'SC-21-V-B-V': '1404',
                'SC-21-V-B-VI': '1405',
                'SC-21-V-C-I': '1477',
                'SC-21-V-C-II': '1478',
                'SC-21-V-C-III': '1479',
                'SC-21-V-C-IV': '1552',
                'SC-21-V-C-V': '1553',
                'SC-21-V-C-VI': '1554',
                'SC-21-V-D-I': '1480',
                'SC-21-V-D-II': '1481',
                'SC-21-V-D-III': '1482',
                'SC-21-V-D-IV': '1555',
                'SC-21-V-D-V': '1556',
                'SC-21-V-D-VI': '1557',
                'SC-21-X-A-I': '1328',
                'SC-21-X-A-II': '1329',
                'SC-21-X-A-III': '1330',
                'SC-21-X-A-IV': '1406',
                'SC-21-X-A-V': '1407',
                'SC-21-X-A-VI': '1408',
                'SC-21-X-B-I': '1331',
                'SC-21-X-B-II': '1332',
                'SC-21-X-B-III': '1333',
                'SC-21-X-B-IV': '1409',
                'SC-21-X-B-V': '1410',
                'SC-21-X-B-VI': '1411',
                'SC-21-X-C-I': '1483',
                'SC-21-X-C-II': '1484',
                'SC-21-X-C-III': '1485',
                'SC-21-X-C-IV': '1558',
                'SC-21-X-C-V': '1559',
                'SC-21-X-C-VI': '1560',
                'SC-21-X-D-I': '1486',
                'SC-21-X-D-II': '1487',
                'SC-21-X-D-III': '1488',
                'SC-21-X-D-IV': '1561',
                'SC-21-X-D-V': '1562',
                'SC-21-X-D-VI': '1563',
                'SC-21-Y-A-I': '1621',
                'SC-21-Y-A-II': '1622',
                'SC-21-Y-A-III': '1623',
                'SC-21-Y-A-IV': '1687',
                'SC-21-Y-A-V': '1688',
                'SC-21-Y-A-VI': '1689',
                'SC-21-Y-B-I': '1624',
                'SC-21-Y-B-II': '1625',
                'SC-21-Y-B-III': '1626',
                'SC-21-Y-B-IV': '1690',
                'SC-21-Y-B-V': '1691',
                'SC-21-Y-B-VI': '1692',
                'SC-21-Y-C-I': '1749',
                'SC-21-Y-C-II': '1750',
                'SC-21-Y-C-III': '1751',
                'SC-21-Y-C-IV': '1806',
                'SC-21-Y-C-V': '1807',
                'SC-21-Y-C-VI': '1808',
                'SC-21-Y-D-I': '1752',
                'SC-21-Y-D-II': '1753',
                'SC-21-Y-D-III': '1754',
                'SC-21-Y-D-IV': '1809',
                'SC-21-Y-D-V': '1810',
                'SC-21-Y-D-VI': '1811',
                'SC-21-Z-A-I': '1627',
                'SC-21-Z-A-II': '1628',
                'SC-21-Z-A-III': '1629',
                'SC-21-Z-A-IV': '1693',
                'SC-21-Z-A-V': '1694',
                'SC-21-Z-A-VI': '1695',
                'SC-21-Z-B-I': '1630',
                'SC-21-Z-B-II': '1631',
                'SC-21-Z-B-III': '1632',
                'SC-21-Z-B-IV': '1696',
                'SC-21-Z-B-V': '1697',
                'SC-21-Z-B-VI': '1698',
                'SC-21-Z-C-I': '1755',
                'SC-21-Z-C-II': '1756',
                'SC-21-Z-C-III': '1757',
                'SC-21-Z-C-IV': '1812',
                'SC-21-Z-C-V': '1813',
                'SC-21-Z-C-VI': '1814',
                'SC-21-Z-D-I': '1758',
                'SC-21-Z-D-II': '1759',
                'SC-21-Z-D-III': '1760',
                'SC-21-Z-D-IV': '1815',
                'SC-21-Z-D-V': '1816',
                'SC-21-Z-D-VI': '1817',
                'SD-22-V-A-I': '1874',
                'SD-22-V-A-II': '1875',
                'SD-22-V-A-III': '1876',
                'SD-22-V-A-IV': '1928',
                'SD-22-V-A-V': '1929',
                'SD-22-V-A-VI': '1930',
                'SD-22-V-B-I': '1877',
                'SD-22-V-B-II': '1878',
                'SD-22-V-B-III': '1879',
                'SD-22-V-B-IV': '1931',
                'SD-22-V-B-V': '1932',
                'SD-22-V-B-VI': '1933',
                'SD-22-V-C-I': '1979',
                'SD-22-V-C-II': '1980',
                'SD-22-V-C-III': '1981',
                'SD-22-V-C-IV': '2026',
                'SD-22-V-C-V': '2027',
                'SD-22-V-C-VI': '2028',
                'SD-22-V-D-I': '1982',
                'SD-22-V-D-II': '1983',
                'SD-22-V-D-III': '1984',
                'SD-22-V-D-IV': '2029',
                'SD-22-V-D-V': '2030',
                'SD-22-V-D-VI': '2031',
                'SD-22-X-A-I': '1880',
                'SD-22-X-A-II': '1881',
                'SD-22-X-A-III': '1882',
                'SD-22-X-A-IV': '1934',
                'SD-22-X-A-V': '1935',
                'SD-22-X-A-VI': '1936',
                'SD-22-X-B-I': '1883',
                'SD-22-X-B-II': '1884',
                'SD-22-X-B-III': '1885',
                'SD-22-X-B-IV': '1937',
                'SD-22-X-B-V': '1938',
                'SD-22-X-B-VI': '1939',
                'SD-22-X-C-I': '1985',
                'SD-22-X-C-II': '1986',
                'SD-22-X-C-III': '1987',
                'SD-22-X-C-IV': '2032',
                'SD-22-X-C-V': '2033',
                'SD-22-X-C-VI': '2034',
                'SD-22-X-D-I': '1988',
                'SD-22-X-D-II': '1989',
                'SD-22-X-D-III': '1990',
                'SD-22-X-D-IV': '2035',
                'SD-22-X-D-V': '2036',
                'SD-22-X-D-VI': '2037',
                'SD-22-Y-A-I': '2070',
                'SD-22-Y-A-II': '2071',
                'SD-22-Y-A-III': '2072',
                'SD-22-Y-A-IV': '2114',
                'SD-22-Y-A-V': '2115',
                'SD-22-Y-A-VI': '2116',
                'SD-22-Y-B-I': '2073',
                'SD-22-Y-B-II': '2074',
                'SD-22-Y-B-III': '2075',
                'SD-22-Y-B-IV': '2117',
                'SD-22-Y-B-V': '2118',
                'SD-22-Y-B-VI': '2119',
                'SD-22-Y-C-I': '2159',
                'SD-22-Y-C-II': '2160',
                'SD-22-Y-C-III': '2161',
                'SD-22-Y-C-IV': '2203',
                'SD-22-Y-C-V': '2204',
                'SD-22-Y-C-VI': '2205',
                'SD-22-Y-D-I': '2162',
                'SD-22-Y-D-II': '2163',
                'SD-22-Y-D-III': '2164',
                'SD-22-Y-D-IV': '2206',
                'SD-22-Y-D-V': '2207',
                'SD-22-Y-D-VI': '2208',
                'SD-22-Z-A-I': '2076',
                'SD-22-Z-A-II': '2077',
                'SD-22-Z-A-III': '2078',
                'SD-22-Z-A-IV': '2120',
                'SD-22-Z-A-V': '2121',
                'SD-22-Z-A-VI': '2122',
                'SD-22-Z-B-I': '2079',
                'SD-22-Z-B-II': '2080',
                'SD-22-Z-B-III': '2081',
                'SD-22-Z-B-IV': '2123',
                'SD-22-Z-B-V': '2124',
                'SD-22-Z-B-VI': '2125',
                'SD-22-Z-C-I': '2165',
                'SD-22-Z-C-II': '2166',
                'SD-22-Z-C-III': '2167',
                'SD-22-Z-C-IV': '2209',
                'SD-22-Z-C-V': '2210',
                'SD-22-Z-C-VI': '2211',
                'SD-22-Z-D-I': '2168',
                'SD-22-Z-D-II': '2169',
                'SD-22-Z-D-III': '2170',
                'SD-22-Z-D-IV': '2212',
                'SD-22-Z-D-V': '2213',
                'SD-22-Z-D-VI': '2214',
                'SG-23-V-A-I': '2812',
                'SG-23-V-A-II': '2813',
                'SG-23-V-A-III': '2814',
                'SG-23-V-A-IV': '2829',
                'SG-23-V-A-V': '2830',
                'SG-23-V-B-I': '2815',
                'SG-23-V-C-I': '2845',
                'SE-22-V-A-I': '2247',
                'SE-22-V-A-II': '2248',
                'SE-22-V-A-III': '2249',
                'SE-22-V-A-IV': '2287',
                'SE-22-V-A-V': '2288',
                'SE-22-V-A-VI': '2289',
                'SE-22-V-B-I': '2250',
                'SE-22-V-B-II': '2251',
                'SE-22-V-B-III': '2252',
                'SE-22-V-B-IV': '2290',
                'SE-22-V-B-V': '2291',
                'SE-22-V-B-VI': '2292',
                'SE-22-V-C-I': '2327',
                'SE-22-V-C-II': '2328',
                'SE-22-V-C-III': '2329',
                'SE-22-V-C-IV': '2365',
                'SE-22-V-C-V': '2366',
                'SE-22-V-C-VI': '2367',
                'SE-22-V-D-I': '2330',
                'SE-22-V-D-II': '2331',
                'SE-22-V-D-III': '2332',
                'SE-22-V-D-IV': '2368',
                'SE-22-V-D-V': '2369',
                'SE-22-V-D-VI': '2370',
                'SE-22-X-A-I': '2253',
                'SE-22-X-A-II': '2254',
                'SE-22-X-A-III': '2255',
                'SE-22-X-A-IV': '2293',
                'SE-22-X-A-V': '2294',
                'SE-22-X-A-VI': '2295',
                'SE-22-X-B-I': '2256',
                'SE-22-X-B-II': '2257',
                'SE-22-X-B-III': '2258',
                'SE-22-X-B-IV': '2296',
                'SE-22-X-B-V': '2297',
                'SE-22-X-B-VI': '2298',
                'SE-22-X-C-I': '2333',
                'SE-22-X-C-II': '2334',
                'SE-22-X-C-III': '2335',
                'SE-22-X-C-IV': '2371',
                'SE-22-X-C-V': '2372',
                'SE-22-X-C-VI': '2373',
                'SE-22-X-D-I': '2336',
                'SE-22-X-D-II': '2337',
                'SE-22-X-D-III': '2338',
                'SE-22-X-D-IV': '2374',
                'SE-22-X-D-V': '2375',
                'SE-22-X-D-VI': '2376',
                'SE-22-Y-A-I': '2403',
                'SE-22-Y-A-II': '2404',
                'SE-22-Y-A-III': '2405',
                'SE-22-Y-A-IV': '2440',
                'SE-22-Y-A-V': '2441',
                'SE-22-Y-A-VI': '2442',
                'SE-22-Y-B-I': '2406',
                'SE-22-Y-B-II': '2407',
                'SE-22-Y-B-III': '2408',
                'SE-22-Y-B-IV': '2443',
                'SE-22-Y-B-V': '2444',
                'SE-22-Y-B-VI': '2445',
                'SE-22-Y-C-I': '2477',
                'SE-22-Y-C-II': '2478',
                'SE-22-Y-C-III': '2479',
                'SE-22-Y-C-IV': '2515',
                'SE-22-Y-C-V': '2516',
                'SE-22-Y-C-VI': '2517',
                'SE-22-Y-D-I': '2480',
                'SE-22-Y-D-II': '2481',
                'SE-22-Y-D-III': '2482',
                'SE-22-Y-D-IV': '2518',
                'SE-22-Y-D-V': '2519',
                'SE-22-Y-D-VI': '2520',
                'SE-22-Z-A-I': '2409',
                'SE-22-Z-A-II': '2410',
                'SE-22-Z-A-III': '2411',
                'SE-22-Z-A-IV': '2446',
                'SE-22-Z-A-V': '2447',
                'SE-22-Z-A-VI': '2448',
                'SE-22-Z-B-I': '2412',
                'SE-22-Z-B-II': '2413',
                'SE-22-Z-B-III': '2414',
                'SE-22-Z-B-IV': '2449',
                'SE-22-Z-B-V': '2450',
                'SE-22-Z-B-VI': '2451',
                'SE-22-Z-C-I': '2483',
                'SE-22-Z-C-II': '2484',
                'SE-22-Z-C-III': '2485',
                'SE-22-Z-C-IV': '2521',
                'SE-22-Z-C-V': '2522',
                'SE-22-Z-C-VI': '2523',
                'SE-22-Z-D-I': '2486',
                'SE-22-Z-D-II': '2487',
                'SE-22-Z-D-III': '2488',
                'SE-22-Z-D-IV': '2524',
                'SE-22-Z-D-V': '2525',
                'SE-22-Z-D-VI': '2526',
                'SC-22-V-A-I': '1334',
                'SC-22-V-A-II': '1335',
                'SC-22-V-A-III': '1336',
                'SC-22-V-A-IV': '1412',
                'SC-22-V-A-V': '1413',
                'SC-22-V-A-VI': '1414',
                'SC-22-V-B-I': '1337',
                'SC-22-V-B-II': '1338',
                'SC-22-V-B-III': '1339',
                'SC-22-V-B-IV': '1415',
                'SC-22-V-B-V': '1416',
                'SC-22-V-B-VI': '1417',
                'SC-22-V-C-I': '1489',
                'SC-22-V-C-II': '1490',
                'SC-22-V-C-III': '1491',
                'SC-22-V-C-IV': '1564',
                'SC-22-V-C-V': '1565',
                'SC-22-V-C-VI': '1566',
                'SC-22-V-D-I': '1492',
                'SC-22-V-D-II': '1493',
                'SC-22-V-D-III': '1494',
                'SC-22-V-D-IV': '1567',
                'SC-22-V-D-V': '1568',
                'SC-22-V-D-VI': '1569',
                'SC-22-X-A-I': '1340',
                'SC-22-X-A-II': '1341',
                'SC-22-X-A-III': '1342',
                'SC-22-X-A-IV': '1418',
                'SC-22-X-A-V': '1419',
                'SC-22-X-A-VI': '1420',
                'SC-22-X-B-I': '1343',
                'SC-22-X-B-II': '1344',
                'SC-22-X-B-III': '1345',
                'SC-22-X-B-IV': '1421',
                'SC-22-X-B-V': '1422',
                'SC-22-X-B-VI': '1423',
                'SC-22-X-C-I': '1495',
                'SC-22-X-C-II': '1496',
                'SC-22-X-C-III': '1497',
                'SC-22-X-C-IV': '1570',
                'SC-22-X-C-V': '1571',
                'SC-22-X-C-VI': '1572',
                'SC-22-X-D-I': '1498',
                'SC-22-X-D-II': '1499',
                'SC-22-X-D-III': '1500',
                'SC-22-X-D-IV': '1573',
                'SC-22-X-D-V': '1574',
                'SC-22-X-D-VI': '1575',
                'SC-22-Y-A-I': '1633',
                'SC-22-Y-A-II': '1634',
                'SC-22-Y-A-III': '1635',
                'SC-22-Y-A-IV': '1699',
                'SC-22-Y-A-V': '1700',
                'SC-22-Y-A-VI': '1701',
                'SC-22-Y-B-I': '1636',
                'SC-22-Y-B-II': '1637',
                'SC-22-Y-B-III': '1638',
                'SC-22-Y-B-IV': '1702',
                'SC-22-Y-B-V': '1703',
                'SC-22-Y-B-VI': '1704',
                'SC-22-Y-C-I': '1761',
                'SC-22-Y-C-II': '1762',
                'SC-22-Y-C-III': '1763',
                'SC-22-Y-C-IV': '1818',
                'SC-22-Y-C-V': '1819',
                'SC-22-Y-C-VI': '1820',
                'SC-22-Y-D-I': '1764',
                'SC-22-Y-D-II': '1765',
                'SC-22-Y-D-III': '1766',
                'SC-22-Y-D-IV': '1821',
                'SC-22-Y-D-V': '1822',
                'SC-22-Y-D-VI': '1823',
                'SC-22-Z-A-I': '1639',
                'SC-22-Z-A-II': '1640',
                'SC-22-Z-A-III': '1641',
                'SC-22-Z-A-IV': '1705',
                'SC-22-Z-A-V': '1706',
                'SC-22-Z-A-VI': '1707',
                'SC-22-Z-B-I': '1642',
                'SC-22-Z-B-II': '1643',
                'SC-22-Z-B-III': '1644',
                'SC-22-Z-B-IV': '1708',
                'SC-22-Z-B-V': '1709',
                'SC-22-Z-B-VI': '1710',
                'SC-22-Z-C-I': '1767',
                'SC-22-Z-C-II': '1768',
                'SC-22-Z-C-III': '1769',
                'SC-22-Z-C-IV': '1824',
                'SC-22-Z-C-V': '1825',
                'SC-22-Z-C-VI': '1826',
                'SC-22-Z-D-I': '1770',
                'SC-22-Z-D-II': '1771',
                'SC-22-Z-D-III': '1772',
                'SC-22-Z-D-IV': '1827',
                'SC-22-Z-D-V': '1828',
                'SC-22-Z-D-VI': '1829',
                'SE-23-V-A-I': '2259',
                'SE-23-V-A-II': '2260',
                'SE-23-V-A-III': '2261',
                'SE-23-V-A-IV': '2299',
                'SE-23-V-A-V': '2300',
                'SE-23-V-A-VI': '2301',
                'SE-23-V-B-I': '2262',
                'SE-23-V-B-II': '2263',
                'SE-23-V-B-III': '2264',
                'SE-23-V-B-IV': '2302',
                'SE-23-V-B-V': '2303',
                'SE-23-V-B-VI': '2304',
                'SE-23-V-C-I': '2339',
                'SE-23-V-C-II': '2340',
                'SE-23-V-C-III': '2341',
                'SE-23-V-C-IV': '2377',
                'SE-23-V-C-V': '2378',
                'SE-23-V-C-VI': '2379',
                'SE-23-V-D-I': '2342',
                'SE-23-V-D-II': '2343',
                'SE-23-V-D-III': '2344',
                'SE-23-V-D-IV': '2380',
                'SE-23-V-D-V': '2381',
                'SE-23-V-D-VI': '2382',
                'SE-23-X-A-I': '2265',
                'SE-23-X-A-II': '2266',
                'SE-23-X-A-III': '2267',
                'SE-23-X-A-IV': '2305',
                'SE-23-X-A-V': '2306',
                'SE-23-X-A-VI': '2307',
                'SE-23-X-B-I': '2268',
                'SE-23-X-B-II': '2269',
                'SE-23-X-B-III': '2270',
                'SE-23-X-B-IV': '2308',
                'SE-23-X-B-V': '2309',
                'SE-23-X-B-VI': '2310',
                'SE-23-X-C-I': '2345',
                'SE-23-X-C-II': '2346',
                'SE-23-X-C-III': '2347',
                'SE-23-X-C-IV': '2383',
                'SE-23-X-C-V': '2384',
                'SE-23-X-C-VI': '2385',
                'SE-23-X-D-I': '2348',
                'SE-23-X-D-II': '2349',
                'SE-23-X-D-III': '2350',
                'SE-23-X-D-IV': '2386',
                'SE-23-X-D-V': '2387',
                'SE-23-X-D-VI': '2388',
                'SE-23-Y-A-I': '2415',
                'SE-23-Y-A-II': '2416',
                'SE-23-Y-A-III': '2417',
                'SE-23-Y-A-IV': '2452',
                'SE-23-Y-A-V': '2453',
                'SE-23-Y-A-VI': '2454',
                'SE-23-Y-B-I': '2418',
                'SE-23-Y-B-II': '2419',
                'SE-23-Y-B-III': '2420',
                'SE-23-Y-B-IV': '2455',
                'SE-23-Y-B-V': '2456',
                'SE-23-Y-B-VI': '2457',
                'SE-23-Y-C-I': '2489',
                'SE-23-Y-C-II': '2490',
                'SE-23-Y-C-III': '2491',
                'SE-23-Y-C-IV': '2527',
                'SE-23-Y-C-V': '2528',
                'SE-23-Y-C-VI': '2529',
                'SE-23-Y-D-I': '2492',
                'SE-23-Y-D-II': '2493',
                'SE-23-Y-D-III': '2494',
                'SE-23-Y-D-IV': '2530',
                'SE-23-Y-D-V': '2531',
                'SE-23-Y-D-VI': '2532',
                'SE-23-Z-A-I': '2421',
                'SE-23-Z-A-II': '2422',
                'SE-23-Z-A-III': '2423',
                'SE-23-Z-A-IV': '2458',
                'SE-23-Z-A-V': '2459',
                'SE-23-Z-A-VI': '2460',
                'SE-23-Z-B-I': '2424',
                'SE-23-Z-B-II': '2425',
                'SE-23-Z-B-III': '2426',
                'SE-23-Z-B-IV': '2461',
                'SE-23-Z-B-V': '2462',
                'SE-23-Z-B-VI': '2463',
                'SE-23-Z-C-I': '2495',
                'SE-23-Z-C-II': '2496',
                'SE-23-Z-C-III': '2497',
                'SE-23-Z-C-IV': '2533',
                'SE-23-Z-C-V': '2534',
                'SE-23-Z-C-VI': '2535',
                'SE-23-Z-D-I': '2498',
                'SE-23-Z-D-II': '2499',
                'SE-23-Z-D-III': '2500',
                'SE-23-Z-D-IV': '2536',
                'SE-23-Z-D-V': '2537',
                'SE-23-Z-D-VI': '2538',
                'SG-22-V-A-I': '2800',
                'SG-22-V-A-II': '2801',
                'SG-22-V-A-III': '2802',
                'SG-22-V-A-IV': '2817',
                'SG-22-V-A-V': '2818',
                'SG-22-V-A-VI': '2819',
                'SG-22-V-B-I': '2803',
                'SG-22-V-B-II': '2804',
                'SG-22-V-B-III': '2805',
                'SG-22-V-B-IV': '2820',
                'SG-22-V-B-V': '2821',
                'SG-22-V-B-VI': '2822',
                'SG-22-V-C-I': '2833',
                'SG-22-V-C-II': '2834',
                'SG-22-V-C-III': '2835',
                'SG-22-V-C-IV': '2848',
                'SG-22-V-C-V': '2849',
                'SG-22-V-C-VI': '2850',
                'SG-22-V-D-I': '2836',
                'SG-22-V-D-II': '2837',
                'SG-22-V-D-III': '2838',
                'SG-22-V-D-IV': '2851',
                'SG-22-V-D-V': '2852',
                'SG-22-V-D-VI': '2853',
                'SG-22-X-A-I': '2806',
                'SG-22-X-A-II': '2807',
                'SG-22-X-A-III': '2808',
                'SG-22-X-A-IV': '2823',
                'SG-22-X-A-V': '2824',
                'SG-22-X-A-VI': '2825',
                'SG-22-X-B-I': '2809',
                'SG-22-X-B-II': '2810',
                'SG-22-X-B-III': '2811',
                'SG-22-X-B-IV': '2826',
                'SG-22-X-B-V': '2827',
                'SG-22-X-B-VI': '2828',
                'SG-22-X-C-I': '2839',
                'SG-22-X-C-II': '2840',
                'SG-22-X-C-III': '2841',
                'SG-22-X-C-IV': '2854',
                'SG-22-X-C-V': '2855',
                'SG-22-X-C-VI': '2856',
                'SG-22-X-D-I': '2842',
                'SG-22-X-D-II': '2843',
                'SG-22-X-D-III': '2844',
                'SG-22-X-D-IV': '2857',
                'SG-22-X-D-V': '2858',
                'SG-22-X-D-VI': '2859',
                'SG-22-Y-A-I': '2860',
                'SG-22-Y-A-II': '2861',
                'SG-22-Y-A-III': '2862',
                'SG-22-Y-A-IV': '2872',
                'SG-22-Y-A-V': '2873',
                'SG-22-Y-A-VI': '2874',
                'SG-22-Y-B-I': '2863',
                'SG-22-Y-B-II': '2864',
                'SG-22-Y-B-III': '2865',
                'SG-22-Y-B-IV': '2875',
                'SG-22-Y-B-V': '2876',
                'SG-22-Y-B-VI': '2877',
                'SG-22-Y-C-I': '2884',
                'SG-22-Y-C-II': '2885',
                'SG-22-Y-C-III': '2886',
                'SG-22-Y-C-IV': '2899',
                'SG-22-Y-C-V': '2900',
                'SG-22-Y-C-VI': '2901',
                'SG-22-Y-D-I': '2887',
                'SG-22-Y-D-II': '2888',
                'SG-22-Y-D-III': '2889',
                'SG-22-Y-D-IV': '2902',
                'SG-22-Y-D-V': '2903',
                'SG-22-Y-D-VI': '2904',
                'SG-22-Z-A-I': '2866',
                'SG-22-Z-A-II': '2867',
                'SG-22-Z-A-III': '2868',
                'SG-22-Z-A-IV': '2878',
                'SG-22-Z-A-V': '2879',
                'SG-22-Z-A-VI': '2880',
                'SG-22-Z-B-I': '2869',
                'SG-22-Z-B-II': '2870',
                'SG-22-Z-B-III': '2871',
                'SG-22-Z-B-IV': '2881',
                'SG-22-Z-B-V': '2882',
                'SG-22-Z-C-I': '2890',
                'SG-22-Z-C-II': '2891',
                'SG-22-Z-C-III': '2892',
                'SG-22-Z-C-IV': '2905',
                'SG-22-Z-C-V': '2906',
                'SG-22-Z-C-VI': '2907',
                'SG-22-Z-D-I': '2893',
                'SG-22-Z-D-II': '2894',
                'SG-22-Z-D-III': '2895',
                'SG-22-Z-D-IV': '2908',
                'SG-22-Z-D-V': '2909',
                'SG-22-Z-D-VI': '2910',
                'SI-22-V-A-I': '3023',
                'SI-22-V-A-II': '3024',
                'SI-22-V-A-III': '3025',
                'SI-22-V-A-IV': '3028',
                'SI-22-V-A-V': '3029',
                'SI-22-V-A-VI': '3030',
                'SI-22-V-B-I': '3026',
                'SI-22-V-B-II': '3027',
                'SI-22-V-B-IV': '3031',
                'SI-22-V-C-I': '3032',
                'SI-22-V-C-II': '3033',
                'SI-22-V-C-III': '3034',
                'SI-22-V-C-IV': '3035',
                'SI-22-V-C-V': '3036',
                'SI-22-V-C-VI': '3036A',
                'NA-22-V-B-I': '30',
                'NA-22-V-B-II': '31',
                'NA-22-V-B-III': '32',
                'NA-22-V-B-IV': '43',
                'NA-22-V-B-V': '44',
                'NA-22-V-B-VI': '45',
                'NA-22-V-C-III': '59',
                'NA-22-V-C-IV': '82',
                'NA-22-V-C-V': '83',
                'NA-22-V-C-VI': '84',
                'NA-22-V-D-I': '60',
                'NA-22-V-D-II': '61',
                'NA-22-V-D-III': '62',
                'NA-22-V-D-IV': '85',
                'NA-22-V-D-V': '86',
                'NA-22-V-D-VI': '87',
                'NA-22-X-A-IV': '46',
                'NA-22-X-C-I': '63',
                'NA-22-X-C-IV': '88',
                'NA-22-X-C-V': '89',
                'NA-22-Y-A-I': '116',
                'NA-22-Y-A-II': '117',
                'NA-22-Y-A-III': '118',
                'NA-22-Y-A-IV': '155',
                'NA-22-Y-A-V': '156',
                'NA-22-Y-A-VI': '157',
                'NA-22-Y-B-I': '119',
                'NA-22-Y-B-II': '120',
                'NA-22-Y-B-III': '121',
                'NA-22-Y-B-IV': '158',
                'NA-22-Y-B-V': '159',
                'NA-22-Y-B-VI': '160',
                'NA-22-Y-C-I': '196',
                'NA-22-Y-C-II': '197',
                'NA-22-Y-C-III': '198',
                'NA-22-Y-C-IV': '238',
                'NA-22-Y-C-V': '239',
                'NA-22-Y-C-VI': '240',
                'NA-22-Y-D-I': '199',
                'NA-22-Y-D-II': '200',
                'NA-22-Y-D-III': '201',
                'NA-22-Y-D-IV': '241',
                'NA-22-Y-D-V': '242',
                'NA-22-Y-D-VI': '243',
                'NA-22-Z-A-I': '122',
                'NA-22-Z-A-II': '123',
                'NA-22-Z-A-III': '124',
                'NA-22-Z-A-IV': '161',
                'NA-22-Z-A-V': '162',
                'NA-22-Z-A-VI': '163',
                'NA-22-Z-C-I': '202',
                'NA-22-Z-C-II': '203',
                'NA-22-Z-C-III': '204',
                'NA-22-Z-C-IV': '244',
                'NA-22-Z-C-V': '245',
                'NA-22-Z-C-VI': '246',
                'NA-22-Z-D-IV': '247',
                'SB-18-X-B-V': '753',
                'SB-18-X-B-VI': '754',
                'SB-18-X-D-II': '826',
                'SB-18-X-D-III': '827',
                'SB-18-X-D-IV': '902',
                'SB-18-X-D-V': '903',
                'SB-18-X-D-VI': '904',
                'SB-18-Z-A-VI': '1057',
                'SB-18-Z-B-I': '979',
                'SB-18-Z-B-II': '980',
                'SB-18-Z-B-III': '981',
                'SB-18-Z-B-IV': '1058',
                'SB-18-Z-B-V': '1059',
                'SB-18-Z-B-VI': '1060',
                'SB-18-Z-C-III': '1136',
                'SB-18-Z-C-VI': '1215',
                'SB-18-Z-D-I': '1137',
                'SB-18-Z-D-II': '1138',
                'SB-18-Z-D-III': '1139',
                'SB-18-Z-D-IV': '1216',
                'SB-18-Z-D-V': '1217',
                'SB-18-Z-D-VI': '1218',
                'SA-21-V-A-I': '269',
                'SA-21-V-A-II': '270',
                'SA-21-V-A-III': '271',
                'SA-21-V-A-IV': '313',
                'SA-21-V-A-V': '314',
                'SA-21-V-A-VI': '315',
                'SA-21-V-B-I': '272',
                'SA-21-V-B-II': '273',
                'SA-21-V-B-III': '274',
                'SA-21-V-B-IV': '316',
                'SA-21-V-B-V': '317',
                'SA-21-V-B-VI': '318',
                'SA-21-V-C-I': '361',
                'SA-21-V-C-II': '362',
                'SA-21-V-C-III': '363',
                'SA-21-V-C-IV': '412',
                'SA-21-V-C-V': '413',
                'SA-21-V-C-VI': '414',
                'SA-21-V-D-I': '364',
                'SA-21-V-D-II': '365',
                'SA-21-V-D-III': '366',
                'SA-21-V-D-IV': '415',
                'SA-21-V-D-V': '416',
                'SA-21-V-D-VI': '417',
                'SA-21-X-A-I': '275',
                'SA-21-X-A-II': '276',
                'SA-21-X-A-III': '277',
                'SA-21-X-A-IV': '319',
                'SA-21-X-A-V': '320',
                'SA-21-X-A-VI': '321',
                'SA-21-X-B-I': '278',
                'SA-21-X-B-II': '279',
                'SA-21-X-B-III': '280',
                'SA-21-X-B-IV': '322',
                'SA-21-X-B-V': '323',
                'SA-21-X-B-VI': '324',
                'SA-21-X-C-I': '367',
                'SA-21-X-C-II': '368',
                'SA-21-X-C-III': '369',
                'SA-21-X-C-IV': '418',
                'SA-21-X-C-V': '419',
                'SA-21-X-C-VI': '420',
                'SA-21-X-D-I': '370',
                'SA-21-X-D-II': '371',
                'SA-21-X-D-III': '372',
                'SA-21-X-D-IV': '421',
                'SA-21-X-D-V': '422',
                'SA-21-X-D-VI': '423',
                'SA-21-Y-A-I': '464',
                'SA-21-Y-A-II': '465',
                'SA-21-Y-A-III': '466',
                'SA-21-Y-A-IV': '518',
                'SA-21-Y-A-V': '519',
                'SA-21-Y-A-VI': '520',
                'SA-21-Y-B-I': '467',
                'SA-21-Y-B-II': '468',
                'SA-21-Y-B-III': '469',
                'SA-21-Y-B-IV': '521',
                'SA-21-Y-B-V': '522',
                'SA-21-Y-B-VI': '523',
                'SA-21-Y-C-I': '579',
                'SA-21-Y-C-II': '580',
                'SA-21-Y-C-III': '581',
                'SA-21-Y-C-IV': '642',
                'SA-21-Y-C-V': '643',
                'SA-21-Y-C-VI': '644',
                'SA-21-Y-D-I': '582',
                'SA-21-Y-D-II': '583',
                'SA-21-Y-D-III': '584',
                'SA-21-Y-D-IV': '645',
                'SA-21-Y-D-V': '646',
                'SA-21-Y-D-VI': '647',
                'SA-21-Z-A-I': '470',
                'SA-21-Z-A-II': '471',
                'SA-21-Z-A-III': '472',
                'SA-21-Z-A-IV': '524',
                'SA-21-Z-A-V': '525',
                'SA-21-Z-A-VI': '526',
                'SA-21-Z-B-I': '473',
                'SA-21-Z-B-II': '474',
                'SA-21-Z-B-III': '475',
                'SA-21-Z-B-IV': '527',
                'SA-21-Z-B-V': '528',
                'SA-21-Z-B-VI': '529',
                'SA-21-Z-C-I': '585',
                'SA-21-Z-C-II': '586',
                'SA-21-Z-C-III': '587',
                'SA-21-Z-C-IV': '648',
                'SA-21-Z-C-V': '649',
                'SA-21-Z-C-VI': '650',
                'SA-21-Z-D-I': '588',
                'SA-21-Z-D-II': '589',
                'SA-21-Z-D-III': '590',
                'SA-21-Z-D-IV': '651',
                'SA-21-Z-D-V': '652',
                'SA-21-Z-D-VI': '653',
                'SA-24-Y-A-IV': '554',
                'SA-24-Y-A-V': '555',
                'SA-24-Y-A-VI': '556',
                'SA-24-Y-B-IV': '557',
                'SA-24-Y-B-V': '558',
                'SA-24-Y-C-I': '615',
                'SA-24-Y-C-II': '616',
                'SA-24-Y-C-III': '617',
                'SA-24-Y-C-IV': '678',
                'SA-24-Y-C-V': '679',
                'SA-24-Y-C-VI': '680',
                'SA-24-Y-D-I': '618',
                'SA-24-Y-D-II': '619',
                'SA-24-Y-D-III': '620',
                'SA-24-Y-D-IV': '681',
                'SA-24-Y-D-V': '682',
                'SA-24-Y-D-VI': '683',
                'SA-24-Z-C-I': '621',
                'SA-24-Z-C-IV': '684',
                'SA-24-Z-C-V': '685',
                'SD-21-V-A-I': '1862',
                'SD-21-V-A-II': '1863',
                'SD-21-V-A-III': '1864',
                'SD-21-V-A-IV': '1916',
                'SD-21-V-A-V': '1917',
                'SD-21-V-A-VI': '1918',
                'SD-21-V-B-I': '1865',
                'SD-21-V-B-II': '1866',
                'SD-21-V-B-III': '1867',
                'SD-21-V-B-IV': '1919',
                'SD-21-V-B-V': '1920',
                'SD-21-V-B-VI': '1921',
                'SD-21-V-C-I': '1967',
                'SD-21-V-C-II': '1968',
                'SD-21-V-C-III': '1969',
                'SD-21-V-C-IV': '2014',
                'SD-21-V-C-V': '2015',
                'SD-21-V-C-VI': '2016',
                'SD-21-V-D-I': '1970',
                'SD-21-V-D-II': '1971',
                'SD-21-V-D-III': '1972',
                'SD-21-V-D-IV': '2017',
                'SD-21-V-D-V': '2018',
                'SD-21-V-D-VI': '2019',
                'SD-21-X-A-I': '1868',
                'SD-21-X-A-II': '1869',
                'SD-21-X-A-III': '1870',
                'SD-21-X-A-IV': '1922',
                'SD-21-X-A-V': '1923',
                'SD-21-X-A-VI': '1924',
                'SD-21-X-B-I': '1871',
                'SD-21-X-B-II': '1872',
                'SD-21-X-B-III': '1873',
                'SD-21-X-B-IV': '1925',
                'SD-21-X-B-V': '1926',
                'SD-21-X-B-VI': '1927',
                'SD-21-X-C-I': '1973',
                'SD-21-X-C-II': '1974',
                'SD-21-X-C-III': '1975',
                'SD-21-X-C-IV': '2020',
                'SD-21-X-C-V': '2021',
                'SD-21-X-C-VI': '2022',
                'SD-21-X-D-I': '1976',
                'SD-21-X-D-II': '1977',
                'SD-21-X-D-III': '1978',
                'SD-21-X-D-IV': '2023',
                'SD-21-X-D-V': '2024',
                'SD-21-X-D-VI': '2025',
                'SD-21-Y-A-I': '2058',
                'SD-21-Y-A-II': '2059',
                'SD-21-Y-A-III': '2060',
                'SD-21-Y-A-IV': '2102',
                'SD-21-Y-A-V': '2103',
                'SD-21-Y-A-VI': '2104',
                'SD-21-Y-B-I': '2061',
                'SD-21-Y-B-II': '2062',
                'SD-21-Y-B-III': '2063',
                'SD-21-Y-B-IV': '2105',
                'SD-21-Y-B-V': '2106',
                'SD-21-Y-B-VI': '2107',
                'SD-21-Y-C-I': '2147',
                'SD-21-Y-C-II': '2148',
                'SD-21-Y-C-III': '2149',
                'SD-21-Y-C-IV': '2191',
                'SD-21-Y-C-V': '2192',
                'SD-21-Y-C-VI': '2193',
                'SD-21-Y-D-I': '2150',
                'SD-21-Y-D-II': '2151',
                'SD-21-Y-D-III': '2152',
                'SD-21-Y-D-IV': '2194',
                'SD-21-Y-D-V': '2195',
                'SD-21-Y-D-VI': '2196',
                'SD-21-Z-A-I': '2064',
                'SD-21-Z-A-II': '2065',
                'SD-21-Z-A-III': '2066',
                'SD-21-Z-A-IV': '2108',
                'SD-21-Z-A-V': '2109',
                'SD-21-Z-A-VI': '2110',
                'SD-21-Z-B-I': '2067',
                'SD-21-Z-B-II': '2068',
                'SD-21-Z-B-III': '2069',
                'SD-21-Z-B-IV': '2111',
                'SD-21-Z-B-V': '2112',
                'SD-21-Z-B-VI': '2113',
                'SD-21-Z-C-I': '2153',
                'SD-21-Z-C-II': '2154',
                'SD-21-Z-C-III': '2155',
                'SD-21-Z-C-IV': '2197',
                'SD-21-Z-C-V': '2198',
                'SD-21-Z-C-VI': '2199',
                'SD-21-Z-D-I': '2156',
                'SD-21-Z-D-II': '2157',
                'SD-21-Z-D-III': '2158',
                'SD-21-Z-D-IV': '2200',
                'SD-21-Z-D-V': '2201',
                'SD-21-Z-D-VI': '2202',
                'SD-24-V-A-I': '1898',
                'SD-24-V-A-II': '1899',
                'SD-24-V-A-III': '1900',
                'SD-24-V-A-IV': '1952',
                'SD-24-V-A-V': '1953',
                'SD-24-V-A-VI': '1954',
                'SD-24-V-B-I': '1901',
                'SD-24-V-B-II': '1902',
                'SD-24-V-B-III': '1903',
                'SD-24-V-B-IV': '1955',
                'SD-24-V-B-V': '1956',
                'SD-24-V-B-VI': '1957',
                'SD-24-V-C-I': '2003',
                'SD-24-V-C-II': '2004',
                'SD-24-V-C-III': '2005',
                'SD-24-V-C-IV': '2050',
                'SD-24-V-C-V': '2051',
                'SD-24-V-C-VI': '2052',
                'SD-24-V-D-I': '2006',
                'SD-24-V-D-II': '2007',
                'SD-24-V-D-III': '2008',
                'SD-24-V-D-IV': '2053',
                'SD-24-V-D-V': '2054',
                'SD-24-V-D-VI': '2055',
                'SD-24-X-A-I': '1904',
                'SD-24-X-A-II': '1905',
                'SD-24-X-A-III': '1906',
                'SD-24-X-A-IV': '1958',
                'SD-24-X-A-V': '1959',
                'SD-24-X-A-VI': '1960',
                'SD-24-X-C-I': '2009',
                'SD-24-X-C-IV': '2056',
                'SD-24-Y-A-I': '2094',
                'SD-24-Y-A-II': '2095',
                'SD-24-Y-A-III': '2096',
                'SD-24-Y-A-IV': '2138',
                'SD-24-Y-A-V': '2139',
                'SD-24-Y-A-VI': '2140',
                'SD-24-Y-B-I': '2097',
                'SD-24-Y-B-II': '2098',
                'SD-24-Y-B-III': '2099',
                'SD-24-Y-B-IV': '2141',
                'SD-24-Y-B-V': '2142',
                'SD-24-Y-B-VI': '2143',
                'SD-24-Y-C-I': '2183',
                'SD-24-Y-C-II': '2184',
                'SD-24-Y-C-III': '2185',
                'SD-24-Y-C-IV': '2227',
                'SD-24-Y-C-V': '2228',
                'SD-24-Y-C-VI': '2229',
                'SD-24-Y-D-I': '2186',
                'SD-24-Y-D-II': '2187',
                'SD-24-Y-D-III': '2188',
                'SD-24-Y-D-IV': '2230',
                'SD-24-Y-D-V': '2231',
                'SD-24-Y-D-VI': '2232',
                'SD-24-Z-A-I': '2100',
                'SD-24-Z-A-IV': '2144',
                'SD-24-Z-C-I': '2189',
                'SD-24-Z-C-IV': '2233',
                'SC-25-V-A-I': '1370',
                'SC-25-V-A-II': '1371',
                'SC-25-V-A-III': '1372',
                'SC-25-V-A-IV': '1448',
                'SC-25-V-A-V': '1449',
                'SC-25-V-A-VI': '1449-A',
                'SC-25-V-C-I': '1525',
                'SC-25-V-C-II': '1526',
                'SC-25-V-C-IV': '1600',
                'SH-21-V-D-VI': '2958',
                'SH-21-X-A-III': '2911',
                'SH-21-X-A-V': '2926',
                'SH-21-X-A-VI': '2927',
                'SH-21-X-B-I': '2912',
                'SH-21-X-B-II': '2913',
                'SH-21-X-B-III': '2914',
                'SH-21-X-B-IV': '2928',
                'SH-21-X-B-V': '2929',
                'SH-21-X-B-VI': '2930',
                'SH-21-X-C-I': '2942',
                'SH-21-X-C-II': '2943',
                'SH-21-X-C-III': '2944',
                'SH-21-X-C-IV': '2959',
                'SH-21-X-C-V': '2960',
                'SH-21-X-C-VI': '2961',
                'SH-21-X-D-I': '2945',
                'SH-21-X-D-II': '2946',
                'SH-21-X-D-III': '2947',
                'SH-21-X-D-IV': '2962',
                'SH-21-X-D-V': '2963',
                'SH-21-X-D-VI': '2964',
                'SH-21-Y-B-II': '2974',
                'SH-21-Y-B-III': '2975',
                'SH-21-Z-A-I': '2976',
                'SH-21-Z-A-II': '2977',
                'SH-21-Z-A-III': '2978',
                'SH-21-Z-A-V': '2990',
                'SH-21-Z-A-VI': '2991',
                'SH-21-Z-B-I': '2979',
                'SH-21-Z-B-II': '2980',
                'SH-21-Z-B-III': '2981',
                'SH-21-Z-B-IV': '2992',
                'SH-21-Z-B-V': '2993',
                'SH-21-Z-B-VI': '2994',
                'SH-21-Z-C-II': '3003',
                'SH-21-Z-C-III': '3004',
                'SH-21-Z-D-I': '3005',
                'SH-21-Z-D-II': '3006',
                'SH-21-Z-D-III': '3007',
                'SH-21-Z-D-V': '3015',
                'SH-21-Z-D-VI': '3016',
                'NB-22-Y-D-V': '17',
                'NB-22-Y-D-VI': '18',
                'SE-24-V-A-I': '2271',
                'SE-24-V-A-II': '2272',
                'SE-24-V-A-III': '2273',
                'SE-24-V-A-IV': '2311',
                'SE-24-V-A-V': '2312',
                'SE-24-V-A-VI': '2313',
                'SE-24-V-B-I': '2274',
                'SE-24-V-B-II': '2275',
                'SE-24-V-B-III': '2276',
                'SE-24-V-B-IV': '2314',
                'SE-24-V-B-V': '2315',
                'SE-24-V-B-VI': '2316',
                'SE-24-V-C-I': '2351',
                'SE-24-V-C-II': '2352',
                'SE-24-V-C-III': '2353',
                'SE-24-V-C-IV': '2389',
                'SE-24-V-C-V': '2390',
                'SE-24-V-C-VI': '2391',
                'SE-24-V-D-I': '2354',
                'SE-24-V-D-II': '2355',
                'SE-24-V-D-III': '2356',
                'SE-24-V-D-IV': '2392',
                'SE-24-V-D-V': '2393',
                'SE-24-V-D-VI': '2394',
                'SE-24-X-A-I': '2277',
                'SE-24-X-A-IV': '2317',
                'SE-24-Y-A-I': '2427',
                'SE-24-Y-A-II': '2428',
                'SE-24-Y-A-III': '2429',
                'SE-24-Y-A-IV': '2464',
                'SE-24-Y-A-V': '2465',
                'SE-24-Y-A-VI': '2466',
                'SE-24-Y-B-I': '2430',
                'SE-24-Y-B-II': '2431',
                'SE-24-Y-B-III': '2431A',
                'SE-24-Y-B-IV': '2467',
                'SE-24-Y-B-V': '2468',
                'SE-24-Y-C-I': '2501',
                'SE-24-Y-C-II': '2502',
                'SE-24-Y-C-III': '2503',
                'SE-24-Y-C-IV': '2539',
                'SE-24-Y-C-V': '2540',
                'SE-24-Y-C-VI': '2541',
                'SE-24-Y-D-I': '2504',
                'SE-24-Y-D-II': '2505',
                'SE-24-Y-D-IV': '2542',
                'SE-24-Y-D-V': '2543',
                'SB-20-V-A-I': '697',
                'SB-20-V-A-II': '698',
                'SB-20-V-A-III': '699',
                'SB-20-V-A-IV': '767',
                'SB-20-V-A-V': '768',
                'SB-20-V-A-VI': '769',
                'SB-20-V-B-I': '700',
                'SB-20-V-B-II': '701',
                'SB-20-V-B-III': '702',
                'SB-20-V-B-IV': '770',
                'SB-20-V-B-V': '771',
                'SB-20-V-B-VI': '772',
                'SB-20-V-C-I': '840',
                'SB-20-V-C-II': '841',
                'SB-20-V-C-III': '842',
                'SB-20-V-C-IV': '917',
                'SB-20-V-C-V': '918',
                'SB-20-V-C-VI': '919',
                'SB-20-V-D-I': '843',
                'SB-20-V-D-II': '844',
                'SB-20-V-D-III': '845',
                'SB-20-V-D-IV': '920',
                'SB-20-V-D-V': '921',
                'SB-20-V-D-VI': '922',
                'SB-20-X-A-I': '703',
                'SB-20-X-A-II': '704',
                'SB-20-X-A-III': '705',
                'SB-20-X-A-IV': '773',
                'SB-20-X-A-V': '774',
                'SB-20-X-A-VI': '775',
                'SB-20-X-B-I': '706',
                'SB-20-X-B-II': '707',
                'SB-20-X-B-III': '708',
                'SB-20-X-B-IV': '776',
                'SB-20-X-B-V': '777',
                'SB-20-X-B-VI': '778',
                'SB-20-X-C-I': '846',
                'SB-20-X-C-II': '847',
                'SB-20-X-C-III': '848',
                'SB-20-X-C-IV': '923',
                'SB-20-X-C-V': '924',
                'SB-20-X-C-VI': '925',
                'SB-20-X-D-I': '849',
                'SB-20-X-D-II': '850',
                'SB-20-X-D-III': '851',
                'SB-20-X-D-IV': '926',
                'SB-20-X-D-V': '927',
                'SB-20-X-D-VI': '928',
                'SB-20-Y-A-I': '994',
                'SB-20-Y-A-II': '995',
                'SB-20-Y-A-III': '996',
                'SB-20-Y-A-IV': '1073',
                'SB-20-Y-A-V': '1074',
                'SB-20-Y-A-VI': '1075',
                'SB-20-Y-B-I': '997',
                'SB-20-Y-B-II': '998',
                'SB-20-Y-B-III': '999',
                'SB-20-Y-B-IV': '1076',
                'SB-20-Y-B-V': '1077',
                'SB-20-Y-B-VI': '1078',
                'SB-20-Y-C-I': '1152',
                'SB-20-Y-C-II': '1153',
                'SB-20-Y-C-III': '1154',
                'SB-20-Y-C-IV': '1231',
                'SB-20-Y-C-V': '1232',
                'SB-20-Y-C-VI': '1233',
                'SB-20-Y-D-I': '1155',
                'SB-20-Y-D-II': '1156',
                'SB-20-Y-D-III': '1157',
                'SB-20-Y-D-IV': '1234',
                'SB-20-Y-D-V': '1235',
                'SB-20-Y-D-VI': '1236',
                'SB-20-Z-A-I': '1000',
                'SB-20-Z-A-II': '1001',
                'SB-20-Z-A-III': '1002',
                'SB-20-Z-A-IV': '1079',
                'SB-20-Z-A-V': '1080',
                'SB-20-Z-A-VI': '1081',
                'SB-20-Z-B-I': '1003',
                'SB-20-Z-B-II': '1004',
                'SB-20-Z-B-III': '1005',
                'SB-20-Z-B-IV': '1082',
                'SB-20-Z-B-V': '1083',
                'SB-20-Z-B-VI': '1084',
                'SB-20-Z-C-I': '1158',
                'SB-20-Z-C-II': '1159',
                'SB-20-Z-C-III': '1160',
                'SB-20-Z-C-IV': '1237',
                'SB-20-Z-C-V': '1238',
                'SB-20-Z-C-VI': '1239',
                'SB-20-Z-D-I': '1161',
                'SB-20-Z-D-II': '1162',
                'SB-20-Z-D-III': '1163',
                'SB-20-Z-D-IV': '1240',
                'SB-20-Z-D-V': '1241',
                'SB-20-Z-D-VI': '1242',
                'SF-21-V-B-I': '2544',
                'SF-21-V-B-II': '2545',
                'SF-21-V-B-III': '2546',
                'SF-21-V-B-IV': '2580-A',
                'SF-21-V-B-V': '2581',
                'SF-21-V-B-VI': '2582',
                'SF-21-V-D-II': '2617',
                'SF-21-V-D-III': '2618',
                'SF-21-V-D-V': '2652',
                'SF-21-V-D-VI': '2653',
                'SF-21-X-A-I': '2547',
                'SF-21-X-A-II': '2548',
                'SF-21-X-A-III': '2549',
                'SF-21-X-A-IV': '2583',
                'SF-21-X-A-V': '2584',
                'SF-21-X-A-VI': '2585',
                'SF-21-X-B-I': '2550',
                'SF-21-X-B-II': '2551',
                'SF-21-X-B-III': '2552',
                'SF-21-X-B-IV': '2586',
                'SF-21-X-B-V': '2587',
                'SF-21-X-B-VI': '2588',
                'SF-21-X-C-I': '2619',
                'SF-21-X-C-II': '2620',
                'SF-21-X-C-III': '2621',
                'SF-21-X-C-IV': '2654',
                'SF-21-X-C-V': '2655',
                'SF-21-X-C-VI': '2656',
                'SF-21-X-D-I': '2622',
                'SF-21-X-D-II': '2623',
                'SF-21-X-D-III': '2624',
                'SF-21-X-D-IV': '2657',
                'SF-21-X-D-V': '2658',
                'SF-21-X-D-VI': '2659',
                'SF-21-Y-B-I': '2685-B',
                'SF-21-Y-B-II': '2686',
                'SF-21-Y-B-III': '2687',
                'SF-21-Z-A-I': '2688',
                'SF-21-Z-A-II': '2689',
                'SF-21-Z-A-III': '2690',
                'SF-21-Z-A-VI': '2720',
                'SF-21-Z-B-I': '2691',
                'SF-21-Z-B-II': '2692',
                'SF-21-Z-B-III': '2693',
                'SF-21-Z-B-IV': '2721',
                'SF-21-Z-B-V': '2722',
                'SF-21-Z-B-VI': '2723',
                'SF-21-Z-C-III': '2749',
                'SF-21-Z-C-VI': '2775',
                'SF-21-Z-D-I': '2750',
                'SF-21-Z-D-II': '2751',
                'SF-21-Z-D-III': '2752',
                'SF-21-Z-D-IV': '2776',
                'SF-21-Z-D-V': '2777',
                'SF-21-Z-D-VI': '2778',
                'SB-19-V-A-I': '685A',
                'SB-19-V-A-II': '686',
                'SB-19-V-A-III': '687',
                'SB-19-V-A-IV': '755',
                'SB-19-V-A-V': '756',
                'SB-19-V-A-VI': '757',
                'SB-19-V-B-I': '688',
                'SB-19-V-B-II': '689',
                'SB-19-V-B-III': '690',
                'SB-19-V-B-IV': '758',
                'SB-19-V-B-V': '759',
                'SB-19-V-B-VI': '760',
                'SB-19-V-C-I': '828',
                'SB-19-V-C-II': '829',
                'SB-19-V-C-III': '830',
                'SB-19-V-C-IV': '905',
                'SB-19-V-C-V': '906',
                'SB-19-V-C-VI': '907',
                'SB-19-V-D-I': '831',
                'SB-19-V-D-II': '832',
                'SB-19-V-D-III': '833',
                'SB-19-V-D-IV': '908',
                'SB-19-V-D-V': '909',
                'SB-19-V-D-VI': '910',
                'SB-19-X-A-I': '691',
                'SB-19-X-A-II': '692',
                'SB-19-X-A-III': '693',
                'SB-19-X-A-IV': '761',
                'SB-19-X-A-V': '762',
                'SB-19-X-A-VI': '763',
                'SB-19-X-B-I': '694',
                'SB-19-X-B-II': '695',
                'SB-19-X-B-III': '696',
                'SB-19-X-B-IV': '764',
                'SB-19-X-B-V': '765',
                'SB-19-X-B-VI': '766',
                'SB-19-X-C-I': '834',
                'SB-19-X-C-II': '835',
                'SB-19-X-C-III': '836',
                'SB-19-X-C-IV': '911',
                'SB-19-X-C-V': '912',
                'SB-19-X-C-VI': '913',
                'SB-19-X-D-I': '837',
                'SB-19-X-D-II': '838',
                'SB-19-X-D-III': '839',
                'SB-19-X-D-IV': '914',
                'SB-19-X-D-V': '915',
                'SB-19-X-D-VI': '916',
                'SB-19-Y-A-I': '982',
                'SB-19-Y-A-II': '983',
                'SB-19-Y-A-III': '984',
                'SB-19-Y-A-IV': '1061',
                'SB-19-Y-A-V': '1062',
                'SB-19-Y-A-VI': '1063',
                'SB-19-Y-B-I': '985',
                'SB-19-Y-B-II': '986',
                'SB-19-Y-B-III': '987',
                'SB-19-Y-B-IV': '1064',
                'SB-19-Y-B-V': '1065',
                'SB-19-Y-B-VI': '1066',
                'SB-19-Y-C-I': '1140',
                'SB-19-Y-C-II': '1141',
                'SB-19-Y-C-III': '1142',
                'SB-19-Y-C-IV': '1219',
                'SB-19-Y-C-V': '1220',
                'SB-19-Y-C-VI': '1221',
                'SB-19-Y-D-I': '1143',
                'SB-19-Y-D-II': '1144',
                'SB-19-Y-D-III': '1145',
                'SB-19-Y-D-IV': '1222',
                'SB-19-Y-D-V': '1223',
                'SB-19-Y-D-VI': '1224',
                'SB-19-Z-A-I': '988',
                'SB-19-Z-A-II': '989',
                'SB-19-Z-A-III': '990',
                'SB-19-Z-A-IV': '1067',
                'SB-19-Z-A-V': '1068',
                'SB-19-Z-A-VI': '1069',
                'SB-19-Z-B-I': '991',
                'SB-19-Z-B-II': '992',
                'SB-19-Z-B-III': '993',
                'SB-19-Z-B-IV': '1070',
                'SB-19-Z-B-V': '1071',
                'SB-19-Z-B-VI': '1072',
                'SB-19-Z-C-I': '1146',
                'SB-19-Z-C-II': '1147',
                'SB-19-Z-C-III': '1148',
                'SB-19-Z-C-IV': '1225',
                'SB-19-Z-C-V': '1226',
                'SB-19-Z-C-VI': '1227',
                'SB-19-Z-D-I': '1149',
                'SB-19-Z-D-II': '1150',
                'SB-19-Z-D-III': '1151',
                'SB-19-Z-D-IV': '1228',
                'SB-19-Z-D-V': '1229',
                'SB-19-Z-D-VI': '1230',
                'SC-19-V-A-I': '1298',
                'SC-19-V-A-II': '1299',
                'SC-19-V-A-III': '1300',
                'SC-19-V-A-IV': '1376',
                'SC-19-V-A-V': '1377',
                'SC-19-V-A-VI': '1378',
                'SC-19-V-B-I': '1301',
                'SC-19-V-B-II': '1302',
                'SC-19-V-B-III': '1303',
                'SC-19-V-B-IV': '1379',
                'SC-19-V-B-V': '1380',
                'SC-19-V-B-VI': '1381',
                'SC-19-V-C-I': '1453',
                'SC-19-V-C-II': '1454',
                'SC-19-V-C-III': '1455',
                'SC-19-V-C-IV': '1528',
                'SC-19-V-C-V': '1529',
                'SC-19-V-C-VI': '1530',
                'SC-19-V-D-I': '1456',
                'SC-19-V-D-II': '1457',
                'SC-19-V-D-III': '1458',
                'SC-19-V-D-IV': '1531',
                'SC-19-V-D-V': '1532',
                'SC-19-V-D-VI': '1533',
                'SC-19-X-A-I': '1304',
                'SC-19-X-A-II': '1305',
                'SC-19-X-A-III': '1306',
                'SC-19-X-A-IV': '1382',
                'SC-19-X-A-V': '1383',
                'SC-19-X-A-VI': '1384',
                'SC-19-X-B-I': '1307',
                'SC-19-X-B-II': '1308',
                'SC-19-X-B-III': '1309',
                'SC-19-X-B-IV': '1385',
                'SC-19-X-B-V': '1386',
                'SC-19-X-B-VI': '1387',
                'SC-19-X-C-I': '1459',
                'SC-19-X-C-II': '1460',
                'SC-19-X-C-III': '1461',
                'SC-19-X-C-IV': '1534',
                'SC-19-X-C-V': '1535',
                'SC-19-X-C-VI': '1536',
                'SC-19-X-D-I': '1462',
                'SC-19-X-D-II': '1463',
                'SC-19-X-D-III': '1464',
                'SC-19-X-D-IV': '1537',
                'SC-19-X-D-V': '1538',
                'SC-19-X-D-VI': '1539',
                'SC-19-Y-A-III': '1601',
                'SC-19-Y-A-VI': '1669',
                'SC-19-Y-B-I': '1602',
                'SC-19-Y-B-II': '1603',
                'SC-19-Y-B-III': '1604',
                'SC-19-Y-B-IV': '1670',
                'SC-19-Y-B-V': '1671',
                'SC-19-Y-B-VI': '1672',
                'SC-19-Y-D-I': '1735',
                'SC-19-Y-D-III': '1735A',
                'SC-19-Z-A-I': '1605',
                'SC-19-Z-A-II': '1606',
                'SC-19-Z-A-III': '1607',
                'SC-19-Z-A-IV': '1673',
                'SC-19-Z-A-V': '1674',
                'SC-19-Z-A-VI': '1675',
                'SC-19-Z-B-I': '1608',
                'SC-19-Z-B-II': '1609',
                'SC-19-Z-C-I': '1736',
                'SC-19-Z-C-II': '1737',
                'SB-23-V-A-I': '733',
                'SB-23-V-A-II': '734',
                'SB-23-V-A-III': '735',
                'SB-23-V-A-IV': '803',
                'SB-23-V-A-V': '804',
                'SB-23-V-A-VI': '805',
                'SB-23-V-B-I': '736',
                'SB-23-V-B-II': '737',
                'SB-23-V-B-III': '738',
                'SB-23-V-B-IV': '806',
                'SB-23-V-B-V': '807',
                'SB-23-V-B-VI': '808',
                'SB-23-V-C-I': '876',
                'SB-23-V-C-II': '877',
                'SB-23-V-C-III': '878',
                'SB-23-V-C-IV': '953',
                'SB-23-V-C-V': '954',
                'SB-23-V-C-VI': '955',
                'SB-23-V-D-I': '879',
                'SB-23-V-D-II': '880',
                'SB-23-V-D-III': '881',
                'SB-23-V-D-IV': '956',
                'SB-23-V-D-V': '957',
                'SB-23-V-D-VI': '958',
                'SB-23-X-A-I': '739',
                'SB-23-X-A-II': '740',
                'SB-23-X-A-III': '741',
                'SB-23-X-A-IV': '809',
                'SB-23-X-A-V': '810',
                'SB-23-X-A-VI': '811',
                'SB-23-X-B-I': '742',
                'SB-23-X-B-II': '743',
                'SB-23-X-B-III': '744',
                'SB-23-X-B-IV': '812',
                'SB-23-X-B-V': '813',
                'SB-23-X-B-VI': '814',
                'SB-23-X-C-I': '882',
                'SB-23-X-C-II': '883',
                'SB-23-X-C-III': '884',
                'SB-23-X-C-IV': '959',
                'SB-23-X-C-V': '960',
                'SB-23-X-C-VI': '961',
                'SB-23-X-D-I': '885',
                'SB-23-X-D-II': '886',
                'SB-23-X-D-III': '887',
                'SB-23-X-D-IV': '962',
                'SB-23-X-D-V': '963',
                'SB-23-X-D-VI': '964',
                'SB-23-Y-A-I': '1030',
                'SB-23-Y-A-II': '1031',
                'SB-23-Y-A-III': '1032',
                'SB-23-Y-A-IV': '1109',
                'SB-23-Y-A-V': '1110',
                'SB-23-Y-A-VI': '1111',
                'SB-23-Y-B-I': '1033',
                'SB-23-Y-B-II': '1034',
                'SB-23-Y-B-III': '1035',
                'SB-23-Y-B-IV': '1112',
                'SB-23-Y-B-V': '1113',
                'SB-23-Y-B-VI': '1114',
                'SB-23-Y-C-I': '1188',
                'SB-23-Y-C-II': '1189',
                'SB-23-Y-C-III': '1190',
                'SB-23-Y-C-IV': '1267',
                'SB-23-Y-C-V': '1268',
                'SB-23-Y-C-VI': '1269',
                'SB-23-Y-D-I': '1191',
                'SB-23-Y-D-II': '1192',
                'SB-23-Y-D-III': '1193',
                'SB-23-Y-D-IV': '1270',
                'SB-23-Y-D-V': '1271',
                'SB-23-Y-D-VI': '1272',
                'SB-23-Z-A-I': '1036',
                'SB-23-Z-A-II': '1037',
                'SB-23-Z-A-III': '1038',
                'SB-23-Z-A-IV': '1115',
                'SB-23-Z-A-V': '1116',
                'SB-23-Z-A-VI': '1117',
                'SB-23-Z-B-I': '1039',
                'SB-23-Z-B-II': '1040',
                'SB-23-Z-B-III': '1041',
                'SB-23-Z-B-IV': '1118',
                'SB-23-Z-B-V': '1119',
                'SB-23-Z-B-VI': '1120',
                'SB-23-Z-C-I': '1194',
                'SB-23-Z-C-II': '1195',
                'SB-23-Z-C-III': '1196',
                'SB-23-Z-C-IV': '1273',
                'SB-23-Z-C-V': '1274',
                'SB-23-Z-C-VI': '1275',
                'SB-23-Z-D-I': '1197',
                'SB-23-Z-D-II': '1198',
                'SB-23-Z-D-III': '1199',
                'SB-23-Z-D-IV': '1276',
                'SB-23-Z-D-V': '1277',
                'SB-23-Z-D-VI': '1278',
                'SD-23-V-A-I': '1886',
                'SD-23-V-A-II': '1887',
                'SD-23-V-A-III': '1888',
                'SD-23-V-A-IV': '1940',
                'SD-23-V-A-V': '1941',
                'SD-23-V-A-VI': '1942',
                'SD-23-V-B-I': '1889',
                'SD-23-V-B-II': '1890',
                'SD-23-V-B-III': '1891',
                'SD-23-V-B-IV': '1943',
                'SD-23-V-B-V': '1944',
                'SD-23-V-B-VI': '1945',
                'SD-23-V-C-I': '1991',
                'SD-23-V-C-II': '1992',
                'SD-23-V-C-III': '1993',
                'SD-23-V-C-IV': '2038',
                'SD-23-V-C-V': '2039',
                'SD-23-V-C-VI': '2040',
                'SD-23-V-D-I': '1994',
                'SD-23-V-D-II': '1995',
                'SD-23-V-D-III': '1996',
                'SD-23-V-D-IV': '2041',
                'SD-23-V-D-V': '2042',
                'SD-23-V-D-VI': '2043',
                'SD-23-X-A-I': '1892',
                'SD-23-X-A-II': '1893',
                'SD-23-X-A-III': '1894',
                'SD-23-X-A-IV': '1946',
                'SD-23-X-A-V': '1947',
                'SD-23-X-A-VI': '1948',
                'SD-23-X-B-I': '1895',
                'SD-23-X-B-II': '1896',
                'SD-23-X-B-III': '1897',
                'SD-23-X-B-IV': '1949',
                'SD-23-X-B-V': '1950',
                'SD-23-X-B-VI': '1951',
                'SD-23-X-C-I': '1997',
                'SD-23-X-C-II': '1998',
                'SD-23-X-C-III': '1999',
                'SD-23-X-C-IV': '2044',
                'SD-23-X-C-V': '2045',
                'SD-23-X-C-VI': '2046',
                'SD-23-X-D-I': '2000',
                'SD-23-X-D-II': '2001',
                'SD-23-X-D-III': '2002',
                'SD-23-X-D-IV': '2047',
                'SD-23-X-D-V': '2048',
                'SD-23-X-D-VI': '2049',
                'SD-23-Y-A-I': '2082',
                'SD-23-Y-A-II': '2083',
                'SD-23-Y-A-III': '2084',
                'SD-23-Y-A-IV': '2126',
                'SD-23-Y-A-V': '2127',
                'SD-23-Y-A-VI': '2128',
                'SD-23-Y-B-I': '2085',
                'SD-23-Y-B-II': '2086',
                'SD-23-Y-B-III': '2087',
                'SD-23-Y-B-IV': '2129',
                'SD-23-Y-B-V': '2130',
                'SD-23-Y-B-VI': '2131',
                'SD-23-Y-C-I': '2171',
                'SD-23-Y-C-II': '2172',
                'SD-23-Y-C-III': '2173',
                'SD-23-Y-C-IV': '2215',
                'SD-23-Y-C-V': '2216',
                'SD-23-Y-C-VI': '2217',
                'SD-23-Y-D-I': '2174',
                'SD-23-Y-D-II': '2175',
                'SD-23-Y-D-III': '2176',
                'SD-23-Y-D-IV': '2218',
                'SD-23-Y-D-V': '2219',
                'SD-23-Y-D-VI': '2220',
                'SD-23-Z-A-I': '2088',
                'SD-23-Z-A-II': '2089',
                'SD-23-Z-A-III': '2090',
                'SD-23-Z-A-IV': '2132',
                'SD-23-Z-A-V': '2133',
                'SD-23-Z-A-VI': '2134',
                'SD-23-Z-B-I': '2091',
                'SD-23-Z-B-II': '2092',
                'SD-23-Z-B-III': '2093',
                'SD-23-Z-B-IV': '2135',
                'SD-23-Z-B-V': '2136',
                'SD-23-Z-B-VI': '2137',
                'SD-23-Z-C-I': '2177',
                'SD-23-Z-C-II': '2178',
                'SD-23-Z-C-III': '2179',
                'SD-23-Z-C-IV': '2221',
                'SD-23-Z-C-V': '2222',
                'SD-23-Z-C-VI': '2223',
                'SD-23-Z-D-I': '2180',
                'SD-23-Z-D-II': '2181',
                'SD-23-Z-D-III': '2182',
                'SD-23-Z-D-IV': '2224',
                'SD-23-Z-D-V': '2225',
                'SD-23-Z-D-VI': '2226',
                'SB-22-V-A-I': '721',
                'SB-22-V-A-II': '722',
                'SB-22-V-A-III': '723',
                'SB-22-V-A-IV': '791',
                'SB-22-V-A-V': '792',
                'SB-22-V-A-VI': '793',
                'SB-22-V-B-I': '724',
                'SB-22-V-B-II': '725',
                'SB-22-V-B-III': '726',
                'SB-22-V-B-IV': '794',
                'SB-22-V-B-V': '795',
                'SB-22-V-B-VI': '796',
                'SB-22-V-C-I': '864',
                'SB-22-V-C-II': '865',
                'SB-22-V-C-III': '866',
                'SB-22-V-C-IV': '941',
                'SB-22-V-C-V': '942',
                'SB-22-V-C-VI': '943',
                'SB-22-V-D-I': '867',
                'SB-22-V-D-II': '868',
                'SB-22-V-D-III': '869',
                'SB-22-V-D-IV': '944',
                'SB-22-V-D-V': '945',
                'SB-22-V-D-VI': '946',
                'SB-22-X-A-I': '727',
                'SB-22-X-A-II': '728',
                'SB-22-X-A-III': '729',
                'SB-22-X-A-IV': '797',
                'SB-22-X-A-V': '798',
                'SB-22-X-A-VI': '799',
                'SB-22-X-B-I': '730',
                'SB-22-X-B-II': '731',
                'SB-22-X-B-III': '732',
                'SB-22-X-B-IV': '800',
                'SB-22-X-B-V': '801',
                'SB-22-X-B-VI': '802',
                'SB-22-X-C-I': '870',
                'SB-22-X-C-II': '871',
                'SB-22-X-C-III': '872',
                'SB-22-X-C-IV': '947',
                'SB-22-X-C-V': '948',
                'SB-22-X-C-VI': '949',
                'SB-22-X-D-I': '873',
                'SB-22-X-D-II': '874',
                'SB-22-X-D-III': '875',
                'SB-22-X-D-IV': '950',
                'SB-22-X-D-V': '951',
                'SB-22-X-D-VI': '952',
                'SB-22-Y-A-I': '1018',
                'SB-22-Y-A-II': '1019',
                'SB-22-Y-A-III': '1020',
                'SB-22-Y-A-IV': '1097',
                'SB-22-Y-A-V': '1098',
                'SB-22-Y-A-VI': '1099',
                'SB-22-Y-B-I': '1021',
                'SB-22-Y-B-II': '1022',
                'SB-22-Y-B-III': '1023',
                'SB-22-Y-B-IV': '1100',
                'SB-22-Y-B-V': '1101',
                'SB-22-Y-B-VI': '1102',
                'SB-22-Y-C-I': '1176',
                'SB-22-Y-C-II': '1177',
                'SB-22-Y-C-III': '1178',
                'SB-22-Y-C-IV': '1255',
                'SB-22-Y-C-V': '1256',
                'SB-22-Y-C-VI': '1257',
                'SB-22-Y-D-I': '1179',
                'SB-22-Y-D-II': '1180',
                'SB-22-Y-D-III': '1181',
                'SB-22-Y-D-IV': '1258',
                'SB-22-Y-D-V': '1259',
                'SB-22-Y-D-VI': '1260',
                'SB-22-Z-A-I': '1024',
                'SB-22-Z-A-II': '1025',
                'SB-22-Z-A-III': '1026',
                'SB-22-Z-A-IV': '1103',
                'SB-22-Z-A-V': '1104',
                'SB-22-Z-A-VI': '1105',
                'SB-22-Z-B-I': '1027',
                'SB-22-Z-B-II': '1028',
                'SB-22-Z-B-III': '1029',
                'SB-22-Z-B-IV': '1106',
                'SB-22-Z-B-V': '1107',
                'SB-22-Z-B-VI': '1108',
                'SB-22-Z-C-I': '1182',
                'SB-22-Z-C-II': '1183',
                'SB-22-Z-C-III': '1184',
                'SB-22-Z-C-IV': '1261',
                'SB-22-Z-C-V': '1262',
                'SB-22-Z-C-VI': '1263',
                'SB-22-Z-D-I': '1185',
                'SB-22-Z-D-II': '1186',
                'SB-22-Z-D-III': '1187',
                'SB-22-Z-D-IV': '1264',
                'SB-22-Z-D-V': '1265',
                'SB-22-Z-D-VI': '1266',
                'SA-20-V-A-I': '257',
                'SA-20-V-A-II': '258',
                'SA-20-V-A-III': '259',
                'SA-20-V-A-IV': '301',
                'SA-20-V-A-V': '302',
                'SA-20-V-A-VI': '303',
                'SA-20-V-B-I': '260',
                'SA-20-V-B-II': '261',
                'SA-20-V-B-III': '262',
                'SA-20-V-B-IV': '304',
                'SA-20-V-B-V': '305',
                'SA-20-V-B-VI': '306',
                'SA-20-V-C-I': '349',
                'SA-20-V-C-II': '350',
                'SA-20-V-C-III': '351',
                'SA-20-V-C-IV': '400',
                'SA-20-V-C-V': '401',
                'SA-20-V-C-VI': '402',
                'SA-20-V-D-I': '352',
                'SA-20-V-D-II': '353',
                'SA-20-V-D-III': '354',
                'SA-20-V-D-IV': '403',
                'SA-20-V-D-V': '404',
                'SA-20-V-D-VI': '405',
                'SA-20-X-A-I': '263',
                'SA-20-X-A-II': '264',
                'SA-20-X-A-III': '265',
                'SA-20-X-A-IV': '307',
                'SA-20-X-A-V': '308',
                'SA-20-X-A-VI': '309',
                'SA-20-X-B-I': '266',
                'SA-20-X-B-II': '267',
                'SA-20-X-B-III': '268',
                'SA-20-X-B-IV': '310',
                'SA-20-X-B-V': '311',
                'SA-20-X-B-VI': '312',
                'SA-20-X-C-I': '355',
                'SA-20-X-C-II': '356',
                'SA-20-X-C-III': '357',
                'SA-20-X-C-IV': '406',
                'SA-20-X-C-V': '407',
                'SA-20-X-C-VI': '408',
                'SA-20-X-D-I': '358',
                'SA-20-X-D-II': '359',
                'SA-20-X-D-III': '360',
                'SA-20-X-D-IV': '409',
                'SA-20-X-D-V': '410',
                'SA-20-X-D-VI': '411',
                'SA-20-Y-A-I': '452',
                'SA-20-Y-A-II': '453',
                'SA-20-Y-A-III': '454',
                'SA-20-Y-A-IV': '506',
                'SA-20-Y-A-V': '507',
                'SA-20-Y-A-VI': '508',
                'SA-20-Y-B-I': '455',
                'SA-20-Y-B-II': '456',
                'SA-20-Y-B-III': '457',
                'SA-20-Y-B-IV': '509',
                'SA-20-Y-B-V': '510',
                'SA-20-Y-B-VI': '511',
                'SA-20-Y-C-I': '567',
                'SA-20-Y-C-II': '568',
                'SA-20-Y-C-III': '569',
                'SA-20-Y-C-IV': '630',
                'SA-20-Y-C-V': '631',
                'SA-20-Y-C-VI': '632',
                'SA-20-Y-D-I': '570',
                'SA-20-Y-D-II': '571',
                'SA-20-Y-D-III': '572',
                'SA-20-Y-D-IV': '633',
                'SA-20-Y-D-V': '634',
                'SA-20-Y-D-VI': '635',
                'SA-20-Z-A-I': '458',
                'SA-20-Z-A-II': '459',
                'SA-20-Z-A-III': '460',
                'SA-20-Z-A-IV': '512',
                'SA-20-Z-A-V': '513',
                'SA-20-Z-A-VI': '514',
                'SA-20-Z-B-I': '461',
                'SA-20-Z-B-II': '462',
                'SA-20-Z-B-III': '463',
                'SA-20-Z-B-IV': '515',
                'SA-20-Z-B-V': '516',
                'SA-20-Z-B-VI': '517',
                'SA-20-Z-C-I': '573',
                'SA-20-Z-C-II': '574',
                'SA-20-Z-C-III': '575',
                'SA-20-Z-C-IV': '636',
                'SA-20-Z-C-V': '637',
                'SA-20-Z-C-VI': '638',
                'SA-20-Z-D-I': '576',
                'SA-20-Z-D-II': '577',
                'SA-20-Z-D-III': '578',
                'SA-20-Z-D-IV': '639',
                'SA-20-Z-D-V': '640',
                'SA-20-Z-D-VI': '641',
                'SA-22-V-A-I': '281',
                'SA-22-V-A-II': '282',
                'SA-22-V-A-III': '283',
                'SA-22-V-A-IV': '325',
                'SA-22-V-A-V': '326',
                'SA-22-V-A-VI': '327',
                'SA-22-V-B-I': '284',
                'SA-22-V-B-II': '285',
                'SA-22-V-B-III': '286',
                'SA-22-V-B-IV': '328',
                'SA-22-V-B-V': '329',
                'SA-22-V-B-VI': '330',
                'SA-22-V-C-I': '373',
                'SA-22-V-C-II': '374',
                'SA-22-V-C-III': '375',
                'SA-22-V-C-IV': '424',
                'SA-22-V-C-V': '425',
                'SA-22-V-C-VI': '426',
                'SA-22-V-D-I': '376',
                'SA-22-V-D-II': '377',
                'SA-22-V-D-III': '378',
                'SA-22-V-D-IV': '427',
                'SA-22-V-D-V': '428',
                'SA-22-V-D-VI': '429',
                'SA-22-X-A-I': '287',
                'SA-22-X-A-II': '288',
                'SA-22-X-A-III': '289',
                'SA-22-X-A-IV': '331',
                'SA-22-X-A-V': '332',
                'SA-22-X-A-VI': '333',
                'SA-22-X-B-I': '290',
                'SA-22-X-B-II': '291',
                'SA-22-X-B-III': '292',
                'SA-22-X-B-IV': '334',
                'SA-22-X-B-V': '335',
                'SA-22-X-B-VI': '336',
                'SA-22-X-C-I': '379',
                'SA-22-X-C-II': '380',
                'SA-22-X-C-III': '381',
                'SA-22-X-C-IV': '430',
                'SA-22-X-C-V': '431',
                'SA-22-X-C-VI': '432',
                'SA-22-X-D-I': '382',
                'SA-22-X-D-II': '383',
                'SA-22-X-D-III': '384',
                'SA-22-X-D-IV': '433',
                'SA-22-X-D-V': '434',
                'SA-22-X-D-VI': '435',
                'SA-22-Y-A-I': '476',
                'SA-22-Y-A-II': '477',
                'SA-22-Y-A-III': '478',
                'SA-22-Y-A-IV': '530',
                'SA-22-Y-A-V': '531',
                'SA-22-Y-A-VI': '532',
                'SA-22-Y-B-I': '479',
                'SA-22-Y-B-II': '480',
                'SA-22-Y-B-III': '481',
                'SA-22-Y-B-IV': '533',
                'SA-22-Y-B-V': '534',
                'SA-22-Y-B-VI': '535',
                'SA-22-Y-C-I': '591',
                'SA-22-Y-C-II': '592',
                'SA-22-Y-C-III': '593',
                'SA-22-Y-C-IV': '654',
                'SA-22-Y-C-V': '655',
                'SA-22-Y-C-VI': '656',
                'SA-22-Y-D-I': '594',
                'SA-22-Y-D-II': '595',
                'SA-22-Y-D-III': '596',
                'SA-22-Y-D-IV': '657',
                'SA-22-Y-D-V': '658',
                'SA-22-Y-D-VI': '659',
                'SA-22-Z-A-I': '482',
                'SA-22-Z-A-II': '483',
                'SA-22-Z-A-III': '484',
                'SA-22-Z-A-IV': '536',
                'SA-22-Z-A-V': '537',
                'SA-22-Z-A-VI': '538',
                'SA-22-Z-B-I': '485',
                'SA-22-Z-B-II': '486',
                'SA-22-Z-B-III': '487',
                'SA-22-Z-B-IV': '539',
                'SA-22-Z-B-V': '540',
                'SA-22-Z-B-VI': '541',
                'SA-22-Z-C-I': '597',
                'SA-22-Z-C-II': '598',
                'SA-22-Z-C-III': '599',
                'SA-22-Z-C-IV': '660',
                'SA-22-Z-C-V': '661',
                'SA-22-Z-C-VI': '662',
                'SA-22-Z-D-I': '600',
                'SA-22-Z-D-II': '601',
                'SA-22-Z-D-III': '602',
                'SA-22-Z-D-IV': '663',
                'SA-22-Z-D-V': '664',
                'SA-22-Z-D-VI': '665',
                'SB-24-V-A-I': '745',
                'SB-24-V-A-II': '746',
                'SB-24-V-A-III': '747',
                'SB-24-V-A-IV': '815',
                'SB-24-V-A-V': '816',
                'SB-24-V-A-VI': '817',
                'SB-24-V-B-I': '748',
                'SB-24-V-B-II': '749',
                'SB-24-V-B-III': '750',
                'SB-24-V-B-IV': '818',
                'SB-24-V-B-V': '819',
                'SB-24-V-B-VI': '820',
                'SB-24-V-C-I': '888',
                'SB-24-V-C-II': '889',
                'SB-24-V-C-III': '890',
                'SB-24-V-C-IV': '965',
                'SB-24-V-C-V': '966',
                'SB-24-V-C-VI': '967',
                'SB-24-V-D-I': '891',
                'SB-24-V-D-II': '892',
                'SB-24-V-D-III': '893',
                'SB-24-V-D-IV': '968',
                'SB-24-V-D-V': '969',
                'SB-24-V-D-VI': '970',
                'SB-24-X-A-I': '751',
                'SB-24-X-A-II': '752',
                'SB-24-X-A-III': '752-A',
                'SB-24-X-A-IV': '821',
                'SB-24-X-A-V': '822',
                'SB-24-X-A-VI': '823',
                'SB-24-X-B-IV': '824',
                'SB-24-X-B-V': '825',
                'SB-24-X-C-I': '894',
                'SB-24-X-C-II': '895',
                'SB-24-X-C-III': '896',
                'SB-24-X-C-IV': '971',
                'SB-24-X-C-V': '972',
                'SB-24-X-C-VI': '973',
                'SB-24-X-D-I': '897',
                'SB-24-X-D-II': '898',
                'SB-24-X-D-III': '899',
                'SB-24-X-D-IV': '974',
                'SB-24-X-D-V': '975',
                'SB-24-X-D-VI': '976',
                'SB-24-Y-A-I': '1042',
                'SB-24-Y-A-II': '1043',
                'SB-24-Y-A-III': '1044',
                'SB-24-Y-A-IV': '1121',
                'SB-24-Y-A-V': '1122',
                'SB-24-Y-A-VI': '1123',
                'SB-24-Y-B-I': '1045',
                'SB-24-Y-B-II': '1046',
                'SB-24-Y-B-III': '1047',
                'SB-24-Y-B-IV': '1124',
                'SB-24-Y-B-V': '1125',
                'SB-24-Y-B-VI': '1126',
                'SB-24-Y-C-I': '1200',
                'SB-24-Y-C-II': '1201',
                'SB-24-Y-C-III': '1202',
                'SB-24-Y-C-IV': '1279',
                'SB-24-Y-C-V': '1280',
                'SB-24-Y-C-VI': '1281',
                'SB-24-Y-D-I': '1203',
                'SB-24-Y-D-II': '1204',
                'SB-24-Y-D-III': '1205',
                'SB-24-Y-D-IV': '1282',
                'SB-24-Y-D-V': '1283',
                'SB-24-Y-D-VI': '1284',
                'SB-24-Z-A-I': '1048',
                'SB-24-Z-A-II': '1049',
                'SB-24-Z-A-III': '1050',
                'SB-24-Z-A-IV': '1127',
                'SB-24-Z-A-V': '1128',
                'SB-24-Z-A-VI': '1129',
                'SB-24-Z-B-I': '1051',
                'SB-24-Z-B-II': '1052',
                'SB-24-Z-B-III': '1053',
                'SB-24-Z-B-IV': '1130',
                'SB-24-Z-B-V': '1131',
                'SB-24-Z-B-VI': '1132',
                'SB-24-Z-C-I': '1206',
                'SB-24-Z-C-II': '1207',
                'SB-24-Z-C-III': '1208',
                'SB-24-Z-C-IV': '1285',
                'SB-24-Z-C-V': '1286',
                'SB-24-Z-C-VI': '1287',
                'SB-24-Z-D-I': '1209',
                'SB-24-Z-D-II': '1210',
                'SB-24-Z-D-III': '1211',
                'SB-24-Z-D-IV': '1288',
                'SB-24-Z-D-V': '1289',
                'SB-24-Z-D-VI': '1290',
                'SF-22-V-A-I': '2553',
                'SF-22-V-A-II': '2554',
                'SF-22-V-A-III': '2555',
                'SF-22-V-A-IV': '2589',
                'SF-22-V-A-V': '2590',
                'SF-22-V-A-VI': '2591',
                'SF-22-V-B-I': '2556',
                'SF-22-V-B-II': '2557',
                'SF-22-V-B-III': '2558',
                'SF-22-V-B-IV': '2592',
                'SF-22-V-B-V': '2593',
                'SF-22-V-B-VI': '2594',
                'SF-22-V-C-I': '2625',
                'SF-22-V-C-II': '2626',
                'SF-22-V-C-III': '2627',
                'SF-22-V-C-IV': '2660',
                'SF-22-V-C-V': '2661',
                'SF-22-V-C-VI': '2662',
                'SF-22-V-D-I': '2628',
                'SF-22-V-D-II': '2629',
                'SF-22-V-D-III': '2630',
                'SF-22-V-D-IV': '2663',
                'SF-22-V-D-V': '2664',
                'SF-22-V-D-VI': '2665',
                'SF-22-X-A-I': '2559',
                'SF-22-X-A-II': '2560',
                'SF-22-X-A-III': '2561',
                'SF-22-X-A-IV': '2595',
                'SF-22-X-A-V': '2596',
                'SF-22-X-A-VI': '2597',
                'SF-22-X-B-I': '2562',
                'SF-22-X-B-II': '2563',
                'SF-22-X-B-III': '2564',
                'SF-22-X-B-IV': '2598',
                'SF-22-X-B-V': '2599',
                'SF-22-X-B-VI': '2600',
                'SF-22-X-C-I': '2631',
                'SF-22-X-C-II': '2632',
                'SF-22-X-C-III': '2633',
                'SF-22-X-C-IV': '2666',
                'SF-22-X-C-V': '2667',
                'SF-22-X-C-VI': '2668',
                'SF-22-X-D-I': '2634',
                'SF-22-X-D-II': '2635',
                'SF-22-X-D-III': '2636',
                'SF-22-X-D-IV': '2669',
                'SF-22-X-D-V': '2670',
                'SF-22-X-D-VI': '2671',
                'SF-22-Y-A-I': '2694',
                'SF-22-Y-A-II': '2695',
                'SF-22-Y-A-III': '2696',
                'SF-22-Y-A-IV': '2724',
                'SF-22-Y-A-V': '2725',
                'SF-22-Y-A-VI': '2726',
                'SF-22-Y-B-I': '2697',
                'SF-22-Y-B-II': '2698',
                'SF-22-Y-B-III': '2699',
                'SF-22-Y-B-IV': '2727',
                'SF-22-Y-B-V': '2728',
                'SF-22-Y-B-VI': '2729',
                'SF-22-Y-C-I': '2753',
                'SF-22-Y-C-II': '2754',
                'SF-22-Y-C-III': '2755',
                'SF-22-Y-C-IV': '2779',
                'SF-22-Y-C-V': '2780',
                'SF-22-Y-C-VI': '2781',
                'SF-22-Y-D-I': '2756',
                'SF-22-Y-D-II': '2757',
                'SF-22-Y-D-III': '2758',
                'SF-22-Y-D-IV': '2782',
                'SF-22-Y-D-V': '2783',
                'SF-22-Y-D-VI': '2784',
                'SF-22-Z-A-I': '2700',
                'SF-22-Z-A-II': '2701',
                'SF-22-Z-A-III': '2702',
                'SF-22-Z-A-IV': '2730',
                'SF-22-Z-A-V': '2731',
                'SF-22-Z-A-VI': '2732',
                'SF-22-Z-B-I': '2703',
                'SF-22-Z-B-II': '2704',
                'SF-22-Z-B-III': '2705',
                'SF-22-Z-B-IV': '2733',
                'SF-22-Z-B-V': '2734',
                'SF-22-Z-B-VI': '2735',
                'SF-22-Z-C-I': '2759',
                'SF-22-Z-C-II': '2760',
                'SF-22-Z-C-III': '2761',
                'SF-22-Z-C-IV': '2785',
                'SF-22-Z-C-V': '2786',
                'SF-22-Z-C-VI': '2787',
                'SF-22-Z-D-I': '2762',
                'SF-22-Z-D-II': '2763',
                'SF-22-Z-D-III': '2764',
                'SF-22-Z-D-IV': '2788',
                'SF-22-Z-D-V': '2789',
                'SF-22-Z-D-VI': '2790',
                'SA-23-V-A-IV': '337',
                'SA-23-V-A-V': '338',
                'SA-23-V-A-VI': '339',
                'SA-23-V-B-IV': '340',
                'SA-23-V-C-I': '385',
                'SA-23-V-C-II': '386',
                'SA-23-V-C-III': '387',
                'SA-23-V-C-IV': '436',
                'SA-23-V-C-V': '437',
                'SA-23-V-C-VI': '438',
                'SA-23-V-D-I': '388',
                'SA-23-V-D-II': '389',
                'SA-23-V-D-III': '390',
                'SA-23-V-D-IV': '439',
                'SA-23-V-D-V': '440',
                'SA-23-V-D-VI': '441',
                'SA-23-X-C-I': '391',
                'SA-23-X-C-IV': '442',
                'SA-23-X-C-V': '443',
                'SA-23-Y-A-I': '488',
                'SA-23-Y-A-II': '489',
                'SA-23-Y-A-III': '490',
                'SA-23-Y-A-IV': '542',
                'SA-23-Y-A-V': '543',
                'SA-23-Y-A-VI': '544',
                'SA-23-Y-B-I': '491',
                'SA-23-Y-B-II': '492',
                'SA-23-Y-B-III': '493',
                'SA-23-Y-B-IV': '545',
                'SA-23-Y-B-V': '546',
                'SA-23-Y-B-VI': '547',
                'SA-23-Y-C-I': '603',
                'SA-23-Y-C-II': '604',
                'SA-23-Y-C-III': '605',
                'SA-23-Y-C-IV': '666',
                'SA-23-Y-C-V': '667',
                'SA-23-Y-C-VI': '668',
                'SA-23-Y-D-I': '606',
                'SA-23-Y-D-II': '607',
                'SA-23-Y-D-III': '608',
                'SA-23-Y-D-IV': '669',
                'SA-23-Y-D-V': '670',
                'SA-23-Y-D-VI': '671',
                'SA-23-Z-A-I': '494',
                'SA-23-Z-A-II': '495',
                'SA-23-Z-A-III': '495-A',
                'SA-23-Z-A-IV': '548',
                'SA-23-Z-A-V': '549',
                'SA-23-Z-A-VI': '550',
                'SA-23-Z-B-I': '496',
                'SA-23-Z-B-II': '497',
                'SA-23-Z-B-IV': '551',
                'SA-23-Z-B-V': '552',
                'SA-23-Z-B-VI': '553',
                'SA-23-Z-C-I': '609',
                'SA-23-Z-C-II': '610',
                'SA-23-Z-C-III': '611',
                'SA-23-Z-C-IV': '672',
                'SA-23-Z-C-V': '673',
                'SA-23-Z-C-VI': '674',
                'SA-23-Z-D-I': '612',
                'SA-23-Z-D-II': '613',
                'SA-23-Z-D-III': '614',
                'SA-23-Z-D-IV': '675',
                'SA-23-Z-D-V': '676',
                'SA-23-Z-D-VI': '677',
                'SG-21-X-B-I': '2797',
                'SG-21-X-B-II': '2798',
                'SG-21-X-B-III': '2799',
                'SG-21-X-B-VI': '2816',
                'SG-21-X-D-II': '2831',
                'SG-21-X-D-III': '2832',
                'SG-21-X-D-V': '2846',
                'SG-21-X-D-VI': '2847',
                'SG-21-Z-D-II': '2882-A',
                'SG-21-Z-D-III': '2883',
                'SG-21-Z-D-IV': '2896',
                'SG-21-Z-D-V': '2897',
                'SG-21-Z-D-VI': '2898',
                'SC-24-V-A-I': '1358',
                'SC-24-V-A-II': '1359',
                'SC-24-V-A-III': '1360',
                'SC-24-V-A-IV': '1436',
                'SC-24-V-A-V': '1437',
                'SC-24-V-A-VI': '1438',
                'SC-24-V-B-I': '1361',
                'SC-24-V-B-II': '1362',
                'SC-24-V-B-III': '1363',
                'SC-24-V-B-IV': '1439',
                'SC-24-V-B-V': '1440',
                'SC-24-V-B-VI': '1441',
                'SC-24-V-C-I': '1513',
                'SC-24-V-C-II': '1514',
                'SC-24-V-C-III': '1515',
                'SC-24-V-C-IV': '1588',
                'SC-24-V-C-V': '1589',
                'SC-24-V-C-VI': '1590',
                'SC-24-V-D-I': '1516',
                'SC-24-V-D-II': '1517',
                'SC-24-V-D-III': '1518',
                'SC-24-V-D-IV': '1591',
                'SC-24-V-D-V': '1592',
                'SC-24-V-D-VI': '1593',
                'SC-24-X-A-I': '1364',
                'SC-24-X-A-II': '1365',
                'SC-24-X-A-III': '1366',
                'SC-24-X-A-IV': '1442',
                'SC-24-X-A-V': '1443',
                'SC-24-X-A-VI': '1444',
                'SC-24-X-B-I': '1367',
                'SC-24-X-B-II': '1368',
                'SC-24-X-B-III': '1369',
                'SC-24-X-B-IV': '1445',
                'SC-24-X-B-V': '1446',
                'SC-24-X-B-VI': '1447',
                'SC-24-X-C-I': '1519',
                'SC-24-X-C-II': '1520',
                'SC-24-X-C-III': '1521',
                'SC-24-X-C-IV': '1594',
                'SC-24-X-C-V': '1595',
                'SC-24-X-C-VI': '1596',
                'SC-24-X-D-I': '1522',
                'SC-24-X-D-II': '1523',
                'SC-24-X-D-III': '1524',
                'SC-24-X-D-IV': '1597',
                'SC-24-X-D-V': '1598',
                'SC-24-X-D-VI': '1599',
                'SC-24-Y-A-I': '1657',
                'SC-24-Y-A-II': '1658',
                'SC-24-Y-A-III': '1659',
                'SC-24-Y-A-IV': '1723',
                'SC-24-Y-A-V': '1724',
                'SC-24-Y-A-VI': '1725',
                'SC-24-Y-B-I': '1660',
                'SC-24-Y-B-II': '1661',
                'SC-24-Y-B-III': '1662',
                'SC-24-Y-B-IV': '1726',
                'SC-24-Y-B-V': '1727',
                'SC-24-Y-B-VI': '1728',
                'SC-24-Y-C-I': '1785',
                'SC-24-Y-C-II': '1786',
                'SC-24-Y-C-III': '1787',
                'SC-24-Y-C-IV': '1842',
                'SC-24-Y-C-V': '1843',
                'SC-24-Y-C-VI': '1844',
                'SC-24-Y-D-I': '1788',
                'SC-24-Y-D-II': '1789',
                'SC-24-Y-D-III': '1790',
                'SC-24-Y-D-IV': '1845',
                'SC-24-Y-D-V': '1846',
                'SC-24-Y-D-VI': '1847',
                'SC-24-Z-A-I': '1663',
                'SC-24-Z-A-II': '1664',
                'SC-24-Z-A-III': '1665',
                'SC-24-Z-A-IV': '1729',
                'SC-24-Z-A-V': '1730',
                'SC-24-Z-A-VI': '1731',
                'SC-24-Z-B-I': '1666',
                'SC-24-Z-B-II': '1667',
                'SC-24-Z-B-III': '1668',
                'SC-24-Z-B-IV': '1732',
                'SC-24-Z-B-V': '1733',
                'SC-24-Z-B-VI': '1734',
                'SC-24-Z-C-I': '1791',
                'SC-24-Z-C-II': '1792',
                'SC-24-Z-C-III': '1793',
                'SC-24-Z-C-IV': '1848',
                'SC-24-Z-C-V': '1849',
                'SC-24-Z-C-VI': '1850',
                'SC-24-Z-D-I': '1794',
                'SC-24-Z-D-IV': '1851',
                'SC-23-V-A-I': '1346',
                'SC-23-V-A-II': '1347',
                'SC-23-V-A-III': '1348',
                'SC-23-V-A-IV': '1424',
                'SC-23-V-A-V': '1425',
                'SC-23-V-A-VI': '1426',
                'SC-23-V-B-I': '1349',
                'SC-23-V-B-II': '1350',
                'SC-23-V-B-III': '1351',
                'SC-23-V-B-IV': '1427',
                'SC-23-V-B-V': '1428',
                'SC-23-V-B-VI': '1429',
                'SC-23-V-C-I': '1501',
                'SC-23-V-C-II': '1502',
                'SC-23-V-C-III': '1503',
                'SC-23-V-C-IV': '1576',
                'SC-23-V-C-V': '1577',
                'SC-23-V-C-VI': '1578',
                'SC-23-V-D-I': '1504',
                'SC-23-V-D-II': '1505',
                'SC-23-V-D-III': '1506',
                'SC-23-V-D-IV': '1579',
                'SC-23-V-D-V': '1580',
                'SC-23-V-D-VI': '1581',
                'SC-23-X-A-I': '1352',
                'SC-23-X-A-II': '1353',
                'SC-23-X-A-III': '1354',
                'SC-23-X-A-IV': '1430',
                'SC-23-X-A-V': '1431',
                'SC-23-X-A-VI': '1432',
                'SC-23-X-B-I': '1355',
                'SC-23-X-B-II': '1356',
                'SC-23-X-B-III': '1357',
                'SC-23-X-B-IV': '1433',
                'SC-23-X-B-V': '1434',
                'SC-23-X-B-VI': '1435',
                'SC-23-X-C-I': '1507',
                'SC-23-X-C-II': '1508',
                'SC-23-X-C-III': '1509',
                'SC-23-X-C-IV': '1582',
                'SC-23-X-C-V': '1583',
                'SC-23-X-C-VI': '1584',
                'SC-23-X-D-I': '1510',
                'SC-23-X-D-II': '1511',
                'SC-23-X-D-III': '1512',
                'SC-23-X-D-IV': '1585',
                'SC-23-X-D-V': '1586',
                'SC-23-X-D-VI': '1587',
                'SC-23-Y-A-I': '1645',
                'SC-23-Y-A-II': '1646',
                'SC-23-Y-A-III': '1647',
                'SC-23-Y-A-IV': '1711',
                'SC-23-Y-A-V': '1712',
                'SC-23-Y-A-VI': '1713',
                'SC-23-Y-B-I': '1648',
                'SC-23-Y-B-II': '1649',
                'SC-23-Y-B-III': '1650',
                'SC-23-Y-B-IV': '1714',
                'SC-23-Y-B-V': '1715',
                'SC-23-Y-B-VI': '1716',
                'SC-23-Y-C-I': '1773',
                'SC-23-Y-C-II': '1774',
                'SC-23-Y-C-III': '1775',
                'SC-23-Y-C-IV': '1830',
                'SC-23-Y-C-V': '1831',
                'SC-23-Y-C-VI': '1832',
                'SC-23-Y-D-I': '1776',
                'SC-23-Y-D-II': '1777',
                'SC-23-Y-D-III': '1778',
                'SC-23-Y-D-IV': '1833',
                'SC-23-Y-D-V': '1834',
                'SC-23-Y-D-VI': '1835',
                'SC-23-Z-A-I': '1651',
                'SC-23-Z-A-II': '1652',
                'SC-23-Z-A-III': '1653',
                'SC-23-Z-A-IV': '1717',
                'SC-23-Z-A-V': '1718',
                'SC-23-Z-A-VI': '1719',
                'SC-23-Z-B-I': '1654',
                'SC-23-Z-B-II': '1655',
                'SC-23-Z-B-III': '1656',
                'SC-23-Z-B-IV': '1720',
                'SC-23-Z-B-V': '1721',
                'SC-23-Z-B-VI': '1722',
                'SC-23-Z-C-I': '1779',
                'SC-23-Z-C-II': '1780',
                'SC-23-Z-C-III': '1781',
                'SC-23-Z-C-IV': '1836',
                'SC-23-Z-C-V': '1837',
                'SC-23-Z-C-VI': '1838',
                'SC-23-Z-D-I': '1782',
                'SC-23-Z-D-II': '1783',
                'SC-23-Z-D-III': '1784',
                'SC-23-Z-D-IV': '1839',
                'SC-23-Z-D-V': '1840',
                'SC-23-Z-D-VI': '1841',
                'NA-19-X-C-VI': '64',
                'NA-19-X-D-IV': '65',
                'NA-19-Y-B-II': '90',
                'NA-19-Y-B-III': '91',
                'NA-19-Y-B-V': '125',
                'NA-19-Y-B-VI': '126',
                'NA-19-Y-D-I': '163A',
                'NA-19-Y-D-II': '164',
                'NA-19-Y-D-III': '165',
                'NA-19-Y-D-IV': '205',
                'NA-19-Y-D-V': '206',
                'NA-19-Y-D-VI': '207',
                'NA-19-Z-A-I': '92',
                'NA-19-Z-A-II': '93',
                'NA-19-Z-A-III': '94',
                'NA-19-Z-A-IV': '127',
                'NA-19-Z-A-V': '128',
                'NA-19-Z-A-VI': '129',
                'NA-19-Z-B-I': '95',
                'NA-19-Z-B-IV': '130',
                'NA-19-Z-B-V': '131',
                'NA-19-Z-C-I': '166',
                'NA-19-Z-C-II': '167',
                'NA-19-Z-C-III': '168',
                'NA-19-Z-C-IV': '208',
                'NA-19-Z-C-V': '209',
                'NA-19-Z-C-VI': '210',
                'NA-19-Z-D-I': '169',
                'NA-19-Z-D-II': '170',
                'NA-19-Z-D-III': '171',
                'NA-19-Z-D-IV': '211',
                'NA-19-Z-D-V': '212',
                'NA-19-Z-D-VI': '213',
                'SC-20-V-A-I': '1310',
                'SC-20-V-A-II': '1311',
                'SC-20-V-A-III': '1312',
                'SC-20-V-A-IV': '1388',
                'SC-20-V-A-V': '1389',
                'SC-20-V-A-VI': '1390',
                'SC-20-V-B-I': '1313',
                'SC-20-V-B-II': '1314',
                'SC-20-V-B-III': '1315',
                'SC-20-V-B-IV': '1391',
                'SC-20-V-B-V': '1392',
                'SC-20-V-B-VI': '1393',
                'SC-20-V-C-I': '1465',
                'SC-20-V-C-II': '1466',
                'SC-20-V-C-III': '1467',
                'SC-20-V-C-IV': '1540',
                'SC-20-V-C-V': '1541',
                'SC-20-V-C-VI': '1542',
                'SC-20-V-D-I': '1468',
                'SC-20-V-D-II': '1469',
                'SC-20-V-D-III': '1470',
                'SC-20-V-D-IV': '1543',
                'SC-20-V-D-V': '1544',
                'SC-20-V-D-VI': '1545',
                'SC-20-X-A-I': '1316',
                'SC-20-X-A-II': '1317',
                'SC-20-X-A-III': '1318',
                'SC-20-X-A-IV': '1394',
                'SC-20-X-A-V': '1395',
                'SC-20-X-A-VI': '1396',
                'SC-20-X-B-I': '1319',
                'SC-20-X-B-II': '1320',
                'SC-20-X-B-III': '1321',
                'SC-20-X-B-IV': '1397',
                'SC-20-X-B-V': '1398',
                'SC-20-X-B-VI': '1399',
                'SC-20-X-C-I': '1471',
                'SC-20-X-C-II': '1472',
                'SC-20-X-C-III': '1473',
                'SC-20-X-C-IV': '1546',
                'SC-20-X-C-V': '1547',
                'SC-20-X-C-VI': '1548',
                'SC-20-X-D-I': '1474',
                'SC-20-X-D-II': '1475',
                'SC-20-X-D-III': '1476',
                'SC-20-X-D-IV': '1549',
                'SC-20-X-D-V': '1550',
                'SC-20-X-D-VI': '1551',
                'SC-20-Y-A-II': '1610',
                'SC-20-Y-A-III': '1611',
                'SC-20-Y-A-V': '1676',
                'SC-20-Y-A-VI': '1677',
                'SC-20-Y-B-I': '1612',
                'SC-20-Y-B-II': '1613',
                'SC-20-Y-B-III': '1614',
                'SC-20-Y-B-IV': '1678',
                'SC-20-Y-B-V': '1679',
                'SC-20-Y-B-VI': '1680',
                'SC-20-Y-C-II': '1738',
                'SC-20-Y-C-III': '1739',
                'SC-20-Y-C-V': '1795',
                'SC-20-Y-C-VI': '1796',
                'SC-20-Y-D-I': '1740',
                'SC-20-Y-D-II': '1741',
                'SC-20-Y-D-III': '1742',
                'SC-20-Y-D-IV': '1797',
                'SC-20-Y-D-V': '1798',
                'SC-20-Y-D-VI': '1799',
                'SC-20-Z-A-I': '1615',
                'SC-20-Z-A-II': '1616',
                'SC-20-Z-A-III': '1617',
                'SC-20-Z-A-IV': '1681',
                'SC-20-Z-A-V': '1682',
                'SC-20-Z-A-VI': '1683',
                'SC-20-Z-B-I': '1618',
                'SC-20-Z-B-II': '1619',
                'SC-20-Z-B-III': '1620',
                'SC-20-Z-B-IV': '1684',
                'SC-20-Z-B-V': '1685',
                'SC-20-Z-B-VI': '1686',
                'SC-20-Z-C-I': '1743',
                'SC-20-Z-C-II': '1744',
                'SC-20-Z-C-III': '1745',
                'SC-20-Z-C-IV': '1800',
                'SC-20-Z-C-V': '1801',
                'SC-20-Z-C-VI': '1802',
                'SC-20-Z-D-I': '1746',
                'SC-20-Z-D-II': '1747',
                'SC-20-Z-D-III': '1748',
                'SC-20-Z-D-IV': '1803',
                'SC-20-Z-D-V': '1804',
                'SC-20-Z-D-VI': '1805',
                'SA-19-V-B-I': '248',
                'SA-19-V-B-II': '249',
                'SA-19-V-B-III': '250',
                'SA-19-V-B-V': '293',
                'SA-19-V-B-VI': '294',
                'SA-19-V-D-II': '341',
                'SA-19-V-D-III': '342',
                'SA-19-V-D-V': '392',
                'SA-19-V-D-VI': '393',
                'SA-19-X-A-I': '251',
                'SA-19-X-A-II': '252',
                'SA-19-X-A-III': '253',
                'SA-19-X-A-IV': '295',
                'SA-19-X-A-V': '296',
                'SA-19-X-A-VI': '297',
                'SA-19-X-B-I': '254',
                'SA-19-X-B-II': '255',
                'SA-19-X-B-III': '256',
                'SA-19-X-B-IV': '298',
                'SA-19-X-B-V': '299',
                'SA-19-X-B-VI': '300',
                'SA-19-X-C-I': '343',
                'SA-19-X-C-II': '344',
                'SA-19-X-C-III': '345',
                'SA-19-X-C-IV': '394',
                'SA-19-X-C-V': '395',
                'SA-19-X-C-VI': '396',
                'SA-19-X-D-I': '346',
                'SA-19-X-D-II': '347',
                'SA-19-X-D-III': '348',
                'SA-19-X-D-IV': '397',
                'SA-19-X-D-V': '398',
                'SA-19-X-D-VI': '399',
                'SA-19-Y-B-II': '444',
                'SA-19-Y-B-III': '445',
                'SA-19-Y-B-V': '498',
                'SA-19-Y-B-VI': '499',
                'SA-19-Y-D-II': '559',
                'SA-19-Y-D-III': '560',
                'SA-19-Y-D-V': '622',
                'SA-19-Y-D-VI': '623',
                'SA-19-Z-A-I': '446',
                'SA-19-Z-A-II': '447',
                'SA-19-Z-A-III': '448',
                'SA-19-Z-A-IV': '500',
                'SA-19-Z-A-V': '501',
                'SA-19-Z-A-VI': '502',
                'SA-19-Z-B-I': '449',
                'SA-19-Z-B-II': '450',
                'SA-19-Z-B-III': '451',
                'SA-19-Z-B-IV': '503',
                'SA-19-Z-B-V': '504',
                'SA-19-Z-B-VI': '505',
                'SA-19-Z-C-I': '561',
                'SA-19-Z-C-II': '562',
                'SA-19-Z-C-III': '563',
                'SA-19-Z-C-IV': '624',
                'SA-19-Z-C-V': '625',
                'SA-19-Z-C-VI': '626',
                'SA-19-Z-D-I': '564',
                'SA-19-Z-D-II': '565',
                'SA-19-Z-D-III': '566',
                'SA-19-Z-D-IV': '627',
                'SA-19-Z-D-V': '628',
                'SA-19-Z-D-VI': '629',
                'SD-20-V-A-III': '1852',
                'SD-20-V-B-I': '1853',
                'SD-20-V-B-II': '1854',
                'SD-20-V-B-III': '1855',
                'SD-20-V-B-IV': '1907',
                'SD-20-V-B-V': '1908',
                'SD-20-V-B-VI': '1909',
                'SD-20-X-A-I': '1856',
                'SD-20-X-A-II': '1857',
                'SD-20-X-A-III': '1858',
                'SD-20-X-A-IV': '1910',
                'SD-20-X-A-V': '1911',
                'SD-20-X-A-VI': '1912',
                'SD-20-X-B-I': '1859',
                'SD-20-X-B-II': '1860',
                'SD-20-X-B-III': '1861',
                'SD-20-X-B-IV': '1913',
                'SD-20-X-B-V': '1914',
                'SD-20-X-B-VI': '1915',
                'SD-20-X-C-I': '1961',
                'SD-20-X-C-II': '1962',
                'SD-20-X-C-III': '1963',
                'SD-20-X-C-VI': '2010',
                'SD-20-X-D-I': '1964',
                'SD-20-X-D-II': '1965',
                'SD-20-X-D-III': '1966',
                'SD-20-X-D-IV': '2011',
                'SD-20-X-D-V': '2012',
                'SD-20-X-D-VI': '2013',
                'SD-20-Z-B-III': '2057',
                'SD-20-Z-B-VI': '2101',
                'SD-20-Z-D-II': '2145',
                'SD-20-Z-D-III': '2146',
                'SD-20-Z-D-VI': '2190',
                'NA-20-V-A-III': '19',
                'NA-20-V-B-I': '20',
                'NA-20-V-B-II': '21',
                'NA-20-V-B-III': '22',
                'NA-20-V-B-IV': '33',
                'NA-20-V-B-V': '34',
                'NA-20-V-B-VI': '35',
                'NA-20-V-D-I': '47',
                'NA-20-V-D-II': '48',
                'NA-20-V-D-III': '49',
                'NA-20-V-D-IV': '66',
                'NA-20-V-D-V': '67',
                'NA-20-V-D-VI': '68',
                'NA-20-X-A-I': '23',
                'NA-20-X-A-II': '24',
                'NA-20-X-A-III': '25',
                'NA-20-X-A-IV': '36',
                'NA-20-X-A-V': '37',
                'NA-20-X-A-VI': '38',
                'NA-20-X-B-I': '26',
                'NA-20-X-B-II': '27',
                'NA-20-X-B-III': '28',
                'NA-20-X-B-IV': '39',
                'NA-20-X-B-V': '40',
                'NA-20-X-B-VI': '41',
                'NA-20-X-C-I': '50',
                'NA-20-X-C-II': '51',
                'NA-20-X-C-III': '52',
                'NA-20-X-C-IV': '69',
                'NA-20-X-C-V': '70',
                'NA-20-X-C-VI': '71',
                'NA-20-X-D-I': '53',
                'NA-20-X-D-II': '54',
                'NA-20-X-D-III': '55',
                'NA-20-X-D-IV': '72',
                'NA-20-X-D-V': '73',
                'NA-20-X-D-VI': '74',
                'NA-20-Y-A-V': '132',
                'NA-20-Y-A-VI': '133',
                'NA-20-Y-B-I': '96',
                'NA-20-Y-B-II': '97',
                'NA-20-Y-B-III': '98',
                'NA-20-Y-B-IV': '134',
                'NA-20-Y-B-V': '135',
                'NA-20-Y-B-VI': '136',
                'NA-20-Y-C-I': '172',
                'NA-20-Y-C-II': '173',
                'NA-20-Y-C-III': '174',
                'NA-20-Y-C-IV': '214',
                'NA-20-Y-C-V': '215',
                'NA-20-Y-C-VI': '216',
                'NA-20-Y-D-I': '175',
                'NA-20-Y-D-II': '176',
                'NA-20-Y-D-III': '177',
                'NA-20-Y-D-IV': '217',
                'NA-20-Y-D-V': '218',
                'NA-20-Y-D-VI': '219',
                'NA-20-Z-A-I': '99',
                'NA-20-Z-A-II': '100',
                'NA-20-Z-A-III': '101',
                'NA-20-Z-A-IV': '137',
                'NA-20-Z-A-V': '138',
                'NA-20-Z-A-VI': '139',
                'NA-20-Z-B-I': '102',
                'NA-20-Z-B-II': '103',
                'NA-20-Z-B-III': '104',
                'NA-20-Z-B-IV': '140',
                'NA-20-Z-B-V': '141',
                'NA-20-Z-B-VI': '142',
                'NA-20-Z-C-I': '178',
                'NA-20-Z-C-II': '179',
                'NA-20-Z-C-III': '180',
                'NA-20-Z-C-IV': '220',
                'NA-20-Z-C-V': '221',
                'NA-20-Z-C-VI': '222',
                'NA-20-Z-D-I': '181',
                'NA-20-Z-D-II': '182',
                'NA-20-Z-D-III': '183',
                'NA-20-Z-D-IV': '223',
                'NA-20-Z-D-V': '224',
                'NA-20-Z-D-VI': '225'}


# Abrir camada de CT
moldura = processing.getObject(Moldura)
SRC_origem = moldura.crs()
features = moldura.getFeatures()
feature = features.next()
centroide = feature.geometry().centroid()
crs = QgsCoordinateReferenceSystem()
crs.createFromSrsId(4326)
xform = QgsCoordinateTransform(SRC_origem, crs)
P = reprojetar(centroide)
X,Y = P.asPoint()

# Calcular MI
delta = 0.125
C_INOM = map_sistem(X, Y)
if C_INOM[:-5] in dicionario:
    C_MI = dicionario[C_INOM[:-5]] + C_INOM[-5:]
else:
    C_MI = ''

NW_INOM = map_sistem(X-delta, Y+delta)
if NW_INOM[:-5] in dicionario:
    NW_MI = dicionario[NW_INOM[:-5]] + NW_INOM[-5:]
else:
    NW_MI = ''

N_INOM = map_sistem(X, Y+delta)
if N_INOM[:-5] in dicionario:
    N_MI = dicionario[N_INOM[:-5]] + N_INOM[-5:]
else:
    N_MI = ''

NE_INOM = map_sistem(X+delta, Y+delta)
if NE_INOM[:-5] in dicionario:
    NE_MI = dicionario[NE_INOM[:-5]] + NE_INOM[-5:]
else:
    NE_MI = ''

SW_INOM = map_sistem(X-delta, Y-delta)
if SW_INOM[:-5] in dicionario:
    SW_MI = dicionario[SW_INOM[:-5]] + SW_INOM[-5:]
else:
    SW_MI = ''

S_INOM = map_sistem(X, Y-delta)
if S_INOM[:-5] in dicionario:
    S_MI = dicionario[S_INOM[:-5]] + S_INOM[-5:]
else:
    S_MI = ''

SE_INOM = map_sistem(X+delta, Y-delta)
if SE_INOM[:-5] in dicionario:
    SE_MI = dicionario[SE_INOM[:-5]] + SE_INOM[-5:]
else:
    SE_MI = ''

E_INOM = map_sistem(X+delta, Y)
if E_INOM[:-5] in dicionario:
    E_MI = dicionario[E_INOM[:-5]] + E_INOM[-5:]
else:
    E_MI = ''

W_INOM = map_sistem(X-delta, Y)
if W_INOM[:-5] in dicionario:
    W_MI = dicionario[W_INOM[:-5]] + W_INOM[-5:]
else:
    W_MI = ''

# Parametros
parametros=  {'C_INOM': C_INOM,
                      'C_MI': C_MI,
                      'NW_INOM': NW_INOM,
                      'NW_MI': NW_MI,
                      'N_INOM': N_INOM,
                      'N_MI': N_MI,
                      'NE_INOM': NE_INOM,
                      'NE_MI': NE_MI,
                      '_W_INOM': W_INOM,
                      '_W_MI': W_MI,
                      '_E_INOM': E_INOM,
                      '_E_MI': E_MI,
                      'SW_INOM': SW_INOM,
                      'SW_MI': SW_MI,
                      'S_INOM': S_INOM,
                      'S_MI': S_MI,
                      'SE_INOM': SE_INOM,
                      'SE_MI': SE_MI}

# Arquivo Modelo
texto = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="200mm"
   height="200mm"
   viewBox="0 0 2362.2048 2362.2084"
   version="1.2"
   id="svg348"
   sodipodi:docname="ESCADA.svg"
   inkscape:version="0.92.2 (5c3e80d, 2017-08-06)">
  <metadata
     id="metadata352">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title />
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="1920"
     inkscape:window-height="1001"
     id="namedview350"
     showgrid="false"
     inkscape:zoom="0.95627042"
     inkscape:cx="392.40017"
     inkscape:cy="385.23958"
     inkscape:window-x="1691"
     inkscape:window-y="-9"
     inkscape:window-maximized="1"
     inkscape:current-layer="g572" />
  <desc
     id="desc2">Generated with Qt</desc>
  <defs
     id="defs4" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g6"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="translate(0,-117.79161)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g8"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,0,-117.79161)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g14"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,0,-117.79161)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g16"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,0,-117.79161)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g18"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g20"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g26"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g56"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g58"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1538.3,1086.7284)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g64"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1538.3,1086.7284)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g66"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g68"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1781.74,1145.7084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
     id="g72"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,1781.74,1145.7084)">
    <path
       style="vector-effect:non-scaling-stroke;fill-rule:evenodd"
       inkscape:connector-curvature="0"
       id="path70"
       d="" />
  </g>
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g74"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1781.74,1145.7084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g76"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g78"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1640.77,1204.6984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g84"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1640.77,1204.6984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g86"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g88"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1541.8,1675.8084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g94"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1541.8,1675.8084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g96"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g98"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1781.74,1734.7984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
     id="g102"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,1781.74,1734.7984)">
    <path
       style="vector-effect:non-scaling-stroke;fill-rule:evenodd"
       inkscape:connector-curvature="0"
       id="path100"
       d="" />
  </g>
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g104"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1781.74,1734.7984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g106"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g108"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1644.27,1793.7784)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g114"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1644.27,1793.7784)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g116"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g118"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1541.8,497.64139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g124"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1541.8,497.64139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g126"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g128"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1781.74,556.62639)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
     id="g132"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,1781.74,556.62639)">
    <path
       style="vector-effect:non-scaling-stroke;fill-rule:evenodd"
       inkscape:connector-curvature="0"
       id="path130"
       d="" />
  </g>
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g134"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1781.74,556.62639)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g136"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g138"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1644.27,615.61139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g144"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1644.27,615.61139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g146"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g148"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,953.212,1086.7284)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g154"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,953.212,1086.7284)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g156"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g158"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1192.65,1145.7084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
     id="g162"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,1192.65,1145.7084)">
    <path
       style="vector-effect:non-scaling-stroke;fill-rule:evenodd"
       inkscape:connector-curvature="0"
       id="path160"
       d="" />
  </g>
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g164"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1192.65,1145.7084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g166"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g168"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1055.69,1204.6984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g174"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1055.69,1204.6984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g176"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g178"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2131.38,1086.7284)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g184"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2131.38,1086.7284)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g186"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g188"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2370.82,1145.7084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
     id="g192"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,2370.82,1145.7084)">
    <path
       style="vector-effect:non-scaling-stroke;fill-rule:evenodd"
       inkscape:connector-curvature="0"
       id="path190"
       d="" />
  </g>
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g194"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2370.82,1145.7084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g196"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g198"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2233.86,1204.6984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g204"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2233.86,1204.6984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g206"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g208"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,956.711,497.64139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g214"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,956.711,497.64139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g216"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g218"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1192.65,556.62639)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
     id="g222"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,1192.65,556.62639)">
    <path
       style="vector-effect:non-scaling-stroke;fill-rule:evenodd"
       inkscape:connector-curvature="0"
       id="path220"
       d="" />
  </g>
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g224"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1192.65,556.62639)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g226"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g228"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1059.19,615.61139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g234"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1059.19,615.61139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g236"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g238"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2134.88,1675.8084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g244"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2134.88,1675.8084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g246"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g248"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2370.82,1734.7984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
     id="g252"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,2370.82,1734.7984)">
    <path
       style="vector-effect:non-scaling-stroke;fill-rule:evenodd"
       inkscape:connector-curvature="0"
       id="path250"
       d="" />
  </g>
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g254"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2370.82,1734.7984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g256"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g258"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2237.35,1793.7784)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g264"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2237.35,1793.7784)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g266"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g268"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2134.88,497.64139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g274"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2134.88,497.64139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g276"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g278"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2370.82,556.62639)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
     id="g282"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,2370.82,556.62639)">
    <path
       style="vector-effect:non-scaling-stroke;fill-rule:evenodd"
       inkscape:connector-curvature="0"
       id="path280"
       d="" />
  </g>
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g284"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2370.82,556.62639)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g286"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g288"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2237.35,615.61139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g294"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,2237.35,615.61139)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g296"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g298"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,956.711,1675.8084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g304"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,956.711,1675.8084)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g306"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g308"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1192.65,1734.7984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
     id="g312"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,1192.65,1734.7984)">
    <path
       style="vector-effect:non-scaling-stroke;fill-rule:evenodd"
       inkscape:connector-curvature="0"
       id="path310"
       d="" />
  </g>
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g314"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1192.65,1734.7984)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g316"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g318"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1059.19,1793.7784)" />
  <g
     id="g572"
     transform="matrix(1.3324742,0,0,1.3331101,4925.9025,290.04779)">
    <g
       transform="matrix(0.999751,0,0,0.999751,-3942.7595,-448.07711)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g50"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#dbdbdb;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:5.43307018;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1">
      <path
         d="M 248.727,821.78 V 625.37 428.959 232.549 h 196.411 196.41 196.411 V 428.959 625.37 821.78 H 641.548 445.138 248.727"
         id="path32"
         inkscape:connector-curvature="0"
         style="vector-effect:none;fill-rule:evenodd" />
      <path
         d="M 837.959,821.78 V 625.37 428.959 232.549 h 196.411 196.41 196.41 V 428.959 625.37 821.78 H 1230.78 1034.37 837.959"
         id="path34"
         inkscape:connector-curvature="0"
         style="vector-effect:none;fill-rule:evenodd" />
      <path
         d="M 1427.19,821.78 V 625.37 428.959 232.549 h 196.41 196.41 196.41 V 428.959 625.37 821.78 H 1820.01 1623.6 1427.19"
         id="path36"
         inkscape:connector-curvature="0"
         style="vector-effect:none;fill-rule:evenodd" />
      <path
         d="M 248.727,1411.01 V 1214.6 1018.19 821.78 h 196.411 196.41 196.411 v 196.41 196.41 196.41 H 641.548 445.138 248.727"
         id="path38"
         inkscape:connector-curvature="0"
         style="vector-effect:none;fill-rule:evenodd" />
      <path
         d="m 248.727,2000.24 v -196.41 -196.41 -196.41 h 196.411 196.41 196.411 v 196.41 196.41 196.41 H 641.548 445.138 248.727"
         id="path40"
         inkscape:connector-curvature="0"
         style="vector-effect:none;fill-rule:evenodd" />
      <path
         d="M 837.959,1411.01 V 1214.6 1018.19 821.78 h 196.411 196.41 196.41 v 196.41 196.41 196.41 H 1230.78 1034.37 837.959"
         id="path42"
         inkscape:connector-curvature="0"
         style="vector-effect:none;fill-rule:evenodd" />
      <path
         d="M 1427.19,1411.01 V 1214.6 1018.19 821.78 h 196.41 196.41 196.41 v 196.41 196.41 196.41 H 1820.01 1623.6 1427.19"
         id="path44"
         inkscape:connector-curvature="0"
         style="vector-effect:none;fill-rule:evenodd" />
      <path
         d="m 837.959,2000.24 v -196.41 -196.41 -196.41 h 196.411 196.41 196.41 v 196.41 196.41 196.41 H 1230.78 1034.37 837.959"
         id="path46"
         inkscape:connector-curvature="0"
         style="vector-effect:none;fill-rule:evenodd" />
      <path
         d="m 1427.19,2000.24 v -196.41 -196.41 -196.41 h 196.41 196.41 196.41 v 196.41 196.41 196.41 H 1820.01 1623.6 1427.19"
         id="path48"
         inkscape:connector-curvature="0"
         style="vector-effect:none;fill-rule:evenodd" />
    </g>
    <g
       transform="matrix(0.999751,0,0,0.999751,-3942.7595,-448.07711)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g54"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1">
      <path
         d="M 837.959,1411.01 V 1214.6 1018.19 821.78 h 196.411 196.41 196.41 v 196.41 196.41 196.41 H 1230.78 1034.37 837.959"
         id="path52"
         inkscape:connector-curvature="0"
         style="vector-effect:none;fill-rule:evenodd" />
    </g>
    <g
       transform="matrix(0.999751,0,0,0.999751,-3032.0788,40.744225)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g212"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel">
      <flowRoot
         xml:space="preserve"
         id="flowRoot574-5"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:0.5;font-family:sans-serif;text-align:center;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
         transform="matrix(2.3458489,0,0,2.3447299,309.50789,-179.89846)"><flowRegion
           id="flowRegion576-5"
           style="line-height:0.5;text-align:center;text-anchor:middle"><rect
             id="rect578-2"
             width="250.80847"
             height="73.697327"
             x="-415.83514"
             y="58.464336"
             style="line-height:0.5;text-align:center;text-anchor:middle" /></flowRegion><flowPara
           id="flowPara580-2"
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle">NW_INOM</flowPara><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara582-2" /><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara584-4">NW_MI</flowPara></flowRoot>      <flowRoot
         xml:space="preserve"
         id="flowRoot616"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"
         transform="matrix(2.3458489,0,0,2.3447299,-61.333037,-255.10268)"><flowRegion
           id="flowRegion618"><rect
             id="rect620"
             width="87.359161"
             height="173.28621"
             x="-193.33585"
             y="48.439514" /></flowRegion><flowPara
           id="flowPara622" /></flowRoot>    </g>
    <g
       transform="matrix(0.99975099,0,0,0.999751,-4108.1188,638.22695)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g212-2"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel">
      <flowRoot
         xml:space="preserve"
         id="flowRoot574-5-7"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:0.5;font-family:sans-serif;text-align:center;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
         transform="matrix(2.3458489,0,0,2.3447299,1598.5911,-200.04603)"><flowRegion
           id="flowRegion576-5-2"
           style="line-height:0.5;text-align:center;text-anchor:middle"><rect
             id="rect578-2-8"
             width="253.94562"
             height="74.743057"
             x="-506.81357"
             y="57.418606"
             style="line-height:0.5;text-align:center;text-anchor:middle" /></flowRegion><flowPara
           id="flowPara580-2-7"
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle">_W_INOM</flowPara><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara582-2-9" /><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara584-4-3">_W_MI</flowPara></flowRoot>      <flowRoot
         xml:space="preserve"
         id="flowRoot616-7"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"
         transform="matrix(2.3458489,0,0,2.3447299,-61.333037,-255.10268)"><flowRegion
           id="flowRegion618-3"><rect
             id="rect620-4"
             width="87.359161"
             height="173.28621"
             x="-193.33585"
             y="48.439514" /></flowRegion><flowPara
           id="flowPara622-7" /></flowRoot>    </g>
    <g
       transform="matrix(0.99975099,0,0,0.999751,-4844.9307,1269.3603)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g212-2-4"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel">
      <flowRoot
         xml:space="preserve"
         id="flowRoot574-5-7-0"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:0.5;font-family:sans-serif;text-align:center;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
         transform="matrix(2.3458489,0,0,2.3447299,2334.4701,-223.55153)"><flowRegion
           id="flowRegion576-5-2-0"
           style="line-height:0.5;text-align:center;text-anchor:middle"><rect
             id="rect578-2-8-3"
             width="247.67122"
             height="73.697334"
             x="-504.72214"
             y="59.510067"
             style="line-height:0.5;text-align:center;text-anchor:middle" /></flowRegion><flowPara
           id="flowPara580-2-7-8"
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle">SW_INOM</flowPara><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara582-2-9-9" /><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara584-4-3-0">SW_MI</flowPara></flowRoot>      <flowRoot
         xml:space="preserve"
         id="flowRoot616-7-5"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"
         transform="matrix(2.3458489,0,0,2.3447299,-61.333037,-255.10268)"><flowRegion
           id="flowRegion618-3-1"><rect
             id="rect620-4-4"
             width="87.359161"
             height="173.28621"
             x="-193.33585"
             y="48.439514" /></flowRegion><flowPara
           id="flowPara622-7-3" /></flowRoot>    </g>
    <g
       transform="matrix(0.99975099,0,0,0.999751,-2455.6411,40.744225)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g212-5"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel">
      <flowRoot
         xml:space="preserve"
         id="flowRoot574-5-9"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:0.5;font-family:sans-serif;text-align:center;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
         transform="matrix(2.3458489,0,0,2.3447299,520.63439,-179.89846)"><flowRegion
           id="flowRegion576-5-29"
           style="line-height:0.5;text-align:center;text-anchor:middle"><rect
             id="rect578-2-7"
             width="248.71707"
             height="75.788788"
             x="-498.44775"
             y="56.372879"
             style="line-height:0.5;text-align:center;text-anchor:middle" /></flowRegion><flowPara
           id="flowPara580-2-3"
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle">N_INOM</flowPara><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara582-2-1" /><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara584-4-2">N_MI</flowPara></flowRoot>      <flowRoot
         xml:space="preserve"
         id="flowRoot616-2"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"
         transform="matrix(2.3458489,0,0,2.3447299,-61.333037,-255.10268)"><flowRegion
           id="flowRegion618-4"><rect
             id="rect620-1"
             width="87.359161"
             height="173.28621"
             x="-193.33585"
             y="48.439514" /></flowRegion><flowPara
           id="flowPara622-8" /></flowRoot>    </g>
    <g
       transform="matrix(0.99975099,0,0,0.999751,-3531.6811,634.7901)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g212-2-5"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel">
      <flowRoot
         xml:space="preserve"
         id="flowRoot574-5-7-6"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:0.5;font-family:sans-serif;text-align:center;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
         transform="matrix(2.3458489,0,0,2.3447299,1598.5911,-200.04603)"><flowRegion
           id="flowRegion576-5-2-1"
           style="line-height:0.5;text-align:center;text-anchor:middle"><rect
             id="rect578-2-8-4"
             width="250.80841"
             height="71.605865"
             x="-500.53922"
             y="58.464336"
             style="line-height:0.5;text-align:center;text-anchor:middle" /></flowRegion><flowPara
           id="flowPara580-2-7-3"
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle">C_INOM</flowPara><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara582-2-9-7" /><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara584-4-3-4">C_MI</flowPara></flowRoot>      <flowRoot
         xml:space="preserve"
         id="flowRoot616-7-8"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"
         transform="matrix(2.3458489,0,0,2.3447299,-61.333037,-255.10268)"><flowRegion
           id="flowRegion618-3-13"><rect
             id="rect620-4-6"
             width="87.359161"
             height="173.28621"
             x="-193.33585"
             y="48.439514" /></flowRegion><flowPara
           id="flowPara622-7-2" /></flowRoot>    </g>
    <g
       transform="matrix(0.99975099,0,0,0.999751,-4268.493,1265.9235)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g212-2-4-0"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel">
      <flowRoot
         xml:space="preserve"
         id="flowRoot574-5-7-0-3"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:0.5;font-family:sans-serif;text-align:center;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
         transform="matrix(2.3458489,0,0,2.3447299,2334.4701,-223.55153)"><flowRegion
           id="flowRegion576-5-2-0-5"
           style="line-height:0.5;text-align:center;text-anchor:middle"><rect
             id="rect578-2-8-3-1"
             width="251.85417"
             height="75.788788"
             x="-499.49347"
             y="58.464336"
             style="line-height:0.5;text-align:center;text-anchor:middle" /></flowRegion><flowPara
           id="flowPara580-2-7-8-6"
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle">S_INOM</flowPara><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara582-2-9-9-4" /><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara584-4-3-0-5">S_MI</flowPara></flowRoot>      <flowRoot
         xml:space="preserve"
         id="flowRoot616-7-5-6"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"
         transform="matrix(2.3458489,0,0,2.3447299,-61.333037,-255.10268)"><flowRegion
           id="flowRegion618-3-1-9"><rect
             id="rect620-4-4-5"
             width="87.359161"
             height="173.28621"
             x="-193.33585"
             y="48.439514" /></flowRegion><flowPara
           id="flowPara622-7-3-6" /></flowRoot>    </g>
    <g
       transform="matrix(0.99975099,0,0,0.999751,-1861.1522,40.744225)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g212-5-7"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel">
      <flowRoot
         xml:space="preserve"
         id="flowRoot574-5-9-6"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:0.5;font-family:sans-serif;text-align:center;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
         transform="matrix(2.3458489,0,0,2.3447299,520.63439,-179.89846)"><flowRegion
           id="flowRegion576-5-29-1"
           style="line-height:0.5;text-align:center;text-anchor:middle"><rect
             id="rect578-2-7-0"
             width="249.76282"
             height="73.697327"
             x="-501.58493"
             y="58.464336"
             style="line-height:0.5;text-align:center;text-anchor:middle" /></flowRegion><flowPara
           id="flowPara580-2-3-9"
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle">NE_INOM</flowPara><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara582-2-1-6" /><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara584-4-2-1">NE_MI</flowPara></flowRoot>      <flowRoot
         xml:space="preserve"
         id="flowRoot616-2-7"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"
         transform="matrix(2.3458489,0,0,2.3447299,-61.333037,-255.10268)"><flowRegion
           id="flowRegion618-4-7"><rect
             id="rect620-1-0"
             width="87.359161"
             height="173.28621"
             x="-193.33585"
             y="48.439514" /></flowRegion><flowPara
           id="flowPara622-8-5" /></flowRoot>    </g>
    <g
       transform="matrix(0.99975099,0,0,0.999751,-2937.1923,634.09543)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g212-2-5-1"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel">
      <flowRoot
         xml:space="preserve"
         id="flowRoot574-5-7-6-8"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:0.5;font-family:sans-serif;text-align:center;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
         transform="matrix(2.3458489,0,0,2.3447299,1598.5911,-200.04603)"><flowRegion
           id="flowRegion576-5-2-1-5"
           style="line-height:0.5;text-align:center;text-anchor:middle"><rect
             id="rect578-2-8-4-6"
             width="246.62556"
             height="71.605873"
             x="-500.53922"
             y="59.510067"
             style="line-height:0.5;text-align:center;text-anchor:middle" /></flowRegion><flowPara
           id="flowPara580-2-7-3-3"
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle">_E_INOM</flowPara><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara582-2-9-7-2" /><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara584-4-3-4-2">_E_MI</flowPara></flowRoot>      <flowRoot
         xml:space="preserve"
         id="flowRoot616-7-8-2"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"
         transform="matrix(2.3458489,0,0,2.3447299,-61.333037,-255.10268)"><flowRegion
           id="flowRegion618-3-13-7"><rect
             id="rect620-4-6-3"
             width="87.359161"
             height="173.28621"
             x="-193.33585"
             y="48.439514" /></flowRegion><flowPara
           id="flowPara622-7-2-5" /></flowRoot>    </g>
    <g
       transform="matrix(0.99975099,0,0,0.999751,-3674.0041,1265.2288)"
       font-size="34.375"
       font-weight="400"
       font-style="normal"
       id="g212-2-4-0-8"
       style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel">
      <flowRoot
         xml:space="preserve"
         id="flowRoot574-5-7-0-3-6"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:0.5;font-family:sans-serif;text-align:center;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel"
         transform="matrix(2.3458489,0,0,2.3447299,2334.4701,-223.55153)"><flowRegion
           id="flowRegion576-5-2-0-5-1"
           style="line-height:0.5;text-align:center;text-anchor:middle"><rect
             id="rect578-2-8-3-1-7"
             width="249.76276"
             height="74.743057"
             x="-499.49347"
             y="58.464336"
             style="line-height:0.5;text-align:center;text-anchor:middle" /></flowRegion><flowPara
           id="flowPara580-2-7-8-6-5"
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle">SE_INOM</flowPara><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara582-2-9-9-4-4" /><flowPara
           style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:22.66666603px;line-height:0.60000002;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle"
           id="flowPara584-4-3-0-5-3">SE_MI</flowPara></flowRoot>      <flowRoot
         xml:space="preserve"
         id="flowRoot616-7-5-6-7"
         style="font-style:normal;font-weight:normal;font-size:40px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"
         transform="matrix(2.3458489,0,0,2.3447299,-61.333037,-255.10268)"><flowRegion
           id="flowRegion618-3-1-9-8"><rect
             id="rect620-4-4-5-4"
             width="87.359161"
             height="173.28621"
             x="-193.33585"
             y="48.439514" /></flowRegion><flowPara
           id="flowPara622-7-3-6-6" /></flowRoot>    </g>
  </g>
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g324"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.31992,0,0,0.31992,1059.19,1793.7784)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:#4c9095;fill-opacity:0;fill-rule:evenodd;stroke:#e31a1c;stroke-width:18.89760017;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g326"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(0.999751,0,0,0.999751,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g328"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g330"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g332"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g334"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="translate(0,-117.79161)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g336"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g338"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,649.444,12.097392)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g340"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,0,-117.79161)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g342"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="matrix(11.8081,0,0,11.8081,0,-117.79161)" />
  <g
     style="font-style:normal;font-weight:400;font-size:34.375px;font-family:'MS Shell Dlg 2';fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:1"
     id="g344"
     font-style="normal"
     font-weight="400"
     font-size="34.375"
     transform="translate(0,-117.79161)" />
</svg>
'''

texto = texto.decode('utf-8')
# Inserir Valores
for item in parametros.keys():
    texto = texto.replace(item, parametros[item])

# Escrever Arquivo
if Arquivo_SVG[-4:] != '.svg':
    Arquivo_SVG += '.svg'

texto = texto.encode('utf-8')
arquivo = open(Arquivo_SVG, 'w')
arquivo.write(texto)
arquivo.close()

progress.setInfo('<br/><b>Leandro Fran&ccedil;a - Eng Cart</b><br/>')
time.sleep(5)
iface.messageBar().pushMessage(u'Situacao', "Operacao Concluida com Sucesso!", level=QgsMessageBar.INFO, duration=5)
