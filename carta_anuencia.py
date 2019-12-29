# -*- encoding: utf-8 -*-
# Este script gera cartas de anuencia de confrontantes baseados em
# tabela SQL. E necessario ter o PostGIS instalado e o conector Psycopg.
# Autor: Emilio Bruno
# E-mail: emiliobrunoneto@gmail.com

import psycopg2
##Cartas de Anuencia=name
##Levantamento=group
# Dados de entrada
##nomeBanco = string base
##porta = string 5432
##host = string localhost
##usuario = string postgres
##senha = string postgres
##nomePasta =  folder
#nomeTabLotes = 

# outras variaveis
srid = '31983'
pasta = nomePasta # pasta onde os arquivos sao salvos
nomeTabLotes ='lotes'
tabCadastro = nomeTabLotes # tabela de areas
numLote = '6'

#conecta ao banco de dados
connect_str = "dbname='"+ nomeBanco + "' port ="+porta+" user='"+usuario+"' host='"+host+"' " + "password='"+senha+"'"
geodados = psycopg2.connect(connect_str)
geodados.set_client_encoding('utf-8')
 
# cria um cursor para realizar as operacoes
lotes = geodados.cursor()
confrontantes = geodados.cursor()
pontos = geodados.cursor()
pasta = nomePasta

# inicio do memorial
cabecalho = "CARTA DE ANUENCIA DE CONFRONTACAO\n  Retificacao e Certificacao de imovel rural \n\n"
 
# realiza uma instrucao SQL
strConfrontantes= """SELECT
    row_number() OVER () AS id,
    lotes.denominaca,
    lotes.id_proprietario,
    lotes.municipio,
    lotes.comarca,
    lotes.cartorio,
    lotes.matricula,
    lotes.area,
    lotes.ccir,
    lotes.area_ha,
    lotes.perimetro,
    lotes.geom,
    lotes.art,
    lotes.obs,
    lotes.num_gleba,
    lotes.itr,
    lotes.nirf,
    lotes.end_propriedade,
    lotes.nome_proprietario,
    lotes.cpf_proprietario,
    lotes.prof_proprietario,
    lotes.estado_civil,
    lotes.nome_conjuge,
    lotes.prof_conjuge,
    lotes.cpf_conjuge,
    lotes.end_proprietario from lotes, vw_limites_incra
     where lotes.id_proprietario = vw_limites_incra.id_confrontante 
     and vw_limites_incra.id_lote = %s
     group by
    lotes.denominaca,
    lotes.id_proprietario,
    lotes.municipio,
    lotes.comarca,
    lotes.cartorio,
    lotes.matricula,
    lotes.area,
    lotes.ccir,
    lotes.area_ha,
    lotes.perimetro,
    lotes.geom,
    lotes.art,
    lotes.obs,
    lotes.num_gleba,
    lotes.itr,
    lotes.nirf,
    lotes.end_propriedade,
    lotes.nome_proprietario,
    lotes.cpf_proprietario,
    lotes.prof_proprietario,
    lotes.estado_civil,
    lotes.nome_conjuge,
    lotes.prof_conjuge,
    lotes.cpf_conjuge,
    lotes.end_proprietario; """ % numLote
 

confrontantes.execute(strConfrontantes)

#Dados do solicitante

strLotes = """SELECT
    id_lote ,
    lotes.denominaca,
    lotes.id_proprietario,
    lotes.municipio,
    lotes.comarca,
    lotes.cartorio,
    lotes.matricula,
    lotes.area,
    lotes.ccir,
    lotes.area_ha,
    lotes.perimetro,
    lotes.geom,
    lotes.art,
    lotes.obs,
    lotes.num_gleba,
    lotes.itr,
    lotes.nirf,
    lotes.end_propriedade,
    lotes.nome_proprietario,
    lotes.cpf_proprietario,
    lotes.prof_proprietario,
    lotes.estado_civil,
    lotes.nome_conjuge,
    lotes.prof_conjuge,
    lotes.cpf_conjuge,
    lotes.end_proprietario from lotes
    where lotes.id_lote =  %s ;"""% numLote

lotes.execute(strLotes)
proprietario =""
proprietario = lotes.fetchone()
Intro1 = """%s , NIRF %s e CCIR %s, registrado no cartÃ³rio de %s, sob matri­cula %s , de propriedade do(a) Sr.(a) %s , CPF: %s"""% (str(proprietario[1]),str(proprietario[16]),str(proprietario[8]),str(proprietario[5]),str(proprietario[6]),str(proprietario[18]),str(proprietario[19]))
Intro2 ="""elaborados pelo Engenheiro Agrimensor Emilio Bruno Neto, CREA--BA 33.601 /D, conforme ART %s """ % (str(proprietario[12]))

# para cada confrontante, elabora uma carta
#id = 0
for confrontante in confrontantes:
    memorial = ""
    memorial += cabecalho
  
    
    intro = """Eu, %s, brasileiro(a), %s, registrado no CPF/MF n.º %s, %s com """ %(str ( confrontante [ 18 ] ),str ( confrontante [ 20 ] ),str ( confrontante [ 19 ] ), str ( confrontante [ 21 ] ))  +\
            """ %s, %s, CPF/MF n.Âº %s""" %(str ( confrontante [ 22 ] ),str ( confrontante [ 23 ] ), str ( confrontante [ 24 ] )) + """, residente e domiciliado na %s,""" %(str ( confrontante [ 25 ] )) +\
            """ na qualidade de justo possuidor do imovel rural  %s, localizado no(a) %s , NIRF %s e CCIR: %s, registrado  no %s,  sob matri­cula %s,"""%(str ( confrontante [ 1 ] ),str ( confrontante [ 17 ] ), str ( confrontante [ 16 ] ), str ( confrontante [ 8 ] ),str ( confrontante [ 5 ] ), str ( confrontante [ 6] )) +\
    """ concordo com os limites e confrontaÃ§Ãµes indicados na Planta e no Memorial Descritivo """+ Intro2 +""" que me foram apresentados, referentes ao imÃ³vel rural denominado """ + Intro1 +\
    """, apenas nos espacos em que o referido imovel faz confrontacao com o imovel de minha propriedade."""
  
    memorial += intro
    

    strPonto = """SELECT * from vw_limites_incra
    where id_lote = %s
    and id_confrontante = '%s'  ORDER BY id_limite; """ % (numLote, str ( confrontante [2] ))
  
    pontos.execute(strPonto)
    
    for pnt in pontos:
      
        if pontos.rownumber ==1:
               memorial += "\nPortanto, minha anuencia refere-se tao somente aos limites definidos pelos vertices expressos no Datum SIRGAS 2000 / UTM 23S, conforme a descricao a seguir:\n" +\
               "Do ponto " + str(pnt[3]) + " definido pelas coordenadas (E=" + str(pnt[4]) + \
               ", N=" + str(pnt[5]) + ") " +\
               "ate o ponto " + str(pnt[6]) +  " definido pelas coordenadas (E="      +\
               str(pnt[7])+ ",N="  + str(pnt[8]) + ") ;\n"
              
        else:
               memorial +="Do ponto " + str(pnt[3]) + " definido pelas coordenadas (E=" + str(pnt[4]) + \
               ", N=" + str(pnt[5]) + ") " +\
               "ate o ponto " + str(pnt[6]) +  " definido pelas coordenadas (E="      +\
               str(pnt[7])+ ",N="  + str(pnt[8]) + ") ;\n"
  
    strFinal = """\nPor ser verdade, e sob pena de responsabilizacao civil e penal firmo(amos) a presente carta de anuencia.\n\n"""
    memorial += strFinal
    assinatura1 = """\n________________________
    %s \n CPF: %s""" % (str ( confrontante [ 18 ] ), str ( confrontante [ 19 ] ))
    assinatura2 = """\n\n________________________
    %s \n CPF: %s """ % (str ( confrontante [ 22 ] ), str ( confrontante [ 24 ] ))
  

    memorial += assinatura1
    memorial += assinatura2
    
    arquivo =open(pasta + str(confrontante[18])+'.odt','w')
    arquivo.write(memorial)
    arquivo.close()

     
del confrontantes,  pontos, lotes