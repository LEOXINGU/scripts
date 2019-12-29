# -*- encoding: utf-8 -*-
# Este script gera memoriais descritivos para um ou mais poligonos em uma
# tabela SQL. E necessario ter o PostGIS instalado e o conector Psycopg.

import psycopg2
from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, "")

# Dados de entrada
##Memorial Descritivo=name
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

# cria um cursor para realizar as operaÃ§Ãµes
cadastros = geodados.cursor()
vertices = geodados.cursor()
adjacente = geodados.cursor()
pasta = nomePasta

# inÃ­cio do memorial
cabecalho = "MEMORIAL DESCRITIVO\n\n"

# realiza uma instruÃ§Ã£o SQL
strCadastros = """SELECT *
  FROM %s;""" % tabCadastro

strAdjacente= """SELECT row_number() OVER () AS id_limite,
    geo.id_lote,
    geo.nome_proprietario,
    em_get_nome_ponto(geo.sp) AS ponto_ini,
    round(st_x(geo.sp)::numeric, 2) AS x_ini,
    round(st_y(geo.sp)::numeric, 2) AS y_ini,
    em_get_nome_ponto(geo.ep) AS fim,
    round(st_x(geo.ep)::numeric, 2) AS x_fim,
    round(st_y(geo.ep)::numeric, 2) AS y_fim,
    round(st_length(st_makeline(geo.sp, geo.ep))::numeric, 2) AS distancia,
    em_mostra_graus(em_graus(degrees(st_azimuth(geo.sp, geo.ep))::numeric)) AS azimute,
    st_makeline(geo.sp, geo.ep) AS limite,
    tipo_limite.cod_tipo_limite,
    tipo_limite.desc_tipo_limite,
    pontos_geo.id_tipo_posicionamento,
    tipo_posicionamento.cod_posicionamento,
    ( SELECT confr.nome_propriedade
           FROM em_confrontante_geral(limites.geom, geo.id_lote) confr(id_lote, nome_propriedade, nome_confrontante, id_confrontante, cpf_proprietario, prof_proprietario, estado_civil, nome_conjuge, cpf_conjuge, prof_conjuge, cartorio, matricula, ccir, itr, nirf, end_proprietario, end_propriedade)) AS nome_propriedade,
    ( SELECT confr.cartorio
           FROM em_confrontante_geral(limites.geom, geo.id_lote) confr(id_lote, nome_propriedade, nome_confrontante, id_confrontante, cpf_proprietario, prof_proprietario, estado_civil, nome_conjuge, cpf_conjuge, prof_conjuge, cartorio, matricula, ccir, itr, nirf, end_proprietario, end_propriedade)) AS cartorio,
    ( SELECT confr.matricula
           FROM em_confrontante_geral(limites.geom, geo.id_lote) confr(id_lote, nome_propriedade, nome_confrontante, id_confrontante, cpf_proprietario, prof_proprietario, estado_civil, nome_conjuge, cpf_conjuge, prof_conjuge, cartorio, matricula, ccir, itr, nirf, end_proprietario, end_propriedade)) AS matricula,
    ( SELECT confr.nome_confrontante
           FROM em_confrontante_geral(limites.geom, geo.id_lote) confr(id_lote, nome_propriedade, nome_confrontante, id_confrontante, cpf_proprietario, prof_proprietario, estado_civil, nome_conjuge, cpf_conjuge, prof_conjuge, cartorio, matricula, ccir, itr, nirf, end_proprietario, end_propriedade)) AS nome_confrontante,
    ( SELECT confr.id_confrontante
           FROM em_confrontante_geral(limites.geom, geo.id_lote) confr(id_lote, nome_propriedade, nome_confrontante, id_confrontante, cpf_proprietario, prof_proprietario, estado_civil, nome_conjuge, cpf_conjuge, prof_conjuge, cartorio, matricula, ccir, itr, nirf, end_proprietario, end_propriedade)) AS id_confrontante
   FROM ( WITH t AS (
                 SELECT lotes.id_lote,
                    lotes.denominaca,
                    lotes.nome_proprietario,
                    lotes.municipio,
                    lotes.comarca,
                    lotes.cartorio,
                    lotes.matricula,
                    lotes.area,
                    lotes.area_ha,
                    lotes.perimetro,
                    lotes.geom,
                    lotes.art,
                    lotes.obs,
                    lotes.num_gleba,
                    (st_dump(st_boundary(lotes.geom))).geom AS bound_geom
                   FROM lotes where id_lote =%s
                )
         SELECT t.id_lote,
            t.nome_proprietario,
            t.cartorio,
            t.matricula,
            st_pointn(t.bound_geom, generate_series(1, st_npoints(t.bound_geom) - 1)) AS sp,
            st_pointn(t.bound_geom, generate_series(2, st_npoints(t.bound_geom))) AS ep
           FROM t) geo,
    limites,
    tipo_limite,
    pontos_geo,
    tipo_posicionamento
  WHERE st_covers(st_makeline(geo.sp, geo.ep), limites.geom) = true AND limites.id_tp_lim = tipo_limite.id_tipo_limite AND pontos_geo.nome_ponto::text = em_get_nome_ponto(geo.sp) AND pontos_geo.id_tipo_posicionamento = tipo_posicionamento.id_tipo_posicionamento;
"""

cadastros.execute(strCadastros)

# para cada Ã¡rea da tabela, elabora um memorial descritivo
for cadastro in cadastros:
	memorial = ""
	
	id = cadastro[0] #Id do lote
	
	# formata o valor flutuante para separador decimal de vÃ­rgula para a Ã¡rea e o perÃ­metro
	area= locale.format("%0.4f", float(cadastro[9]),  0)
	perimetro = locale.format("%0.4f", float(cadastro[10]),  0)
	
	
	memorial += cabecalho
	
	
	identificacao = """\tImÃ³vel:  %s\t\t\t\t\tGleba:  %s\tCod_controle: %s
     MunicÃ­pio: %s\t\t\t\t\tComarca: %s
     CartÃ³rio:%s\t\t\t\t\t\tMatrÃ­cula: %s
     CCIR: %s\t\t\t\t\t\tNIRF: %s
     ProprietÃ¡rio: %s\t\t\t\t\tCPF: %s
     Ãrea: %s ha \t\t\t\t\t\tPerÃ­metro: %s m
        \n\n DESCRIÃÃO""" % (str(cadastro[1]),str(cadastro[14]),str(cadastro[0]),str(cadastro[3]),
	                    str(cadastro[4]),str(cadastro[5]),str(cadastro[6]),  str(cadastro[8]),
	                    str(cadastro[16]),str(cadastro[18]),str(cadastro[19]),area,perimetro)
	
	
	memorial += identificacao
	
	
	adjacente.execute(strAdjacente %(id))
	
	for adj in adjacente:
		
		
		if adjacente.rownumber ==1:
			memorial += "\n\nInicia-se a descriÃ§Ã£o deste perÃ­metro no vÃ©rtice " + \
			            str(adj[3]) + ", de coordenadas N=" + str(adj[5]) + \
			            "m e E= " + str(adj[4]) + "m. Deste segue, " + \
			            "delimitado por " + str(adj[13]) +  ", "      + \
			            "confrontando com " + str(adj[16])+ " ("  + str(adj[19]) +   ")"     + \
			            " por azimute "+ str(adj[10]) +" e distÃ¢ncia de "  + \
			            str(adj[9]) + " m atÃ© o vÃ©rtice " + \
			            str(adj[6]) + " de coordenadas N=" + \
			            str(adj[8]) + "m e E=" + str(adj[7]) + "m ;"
		
		else:
			
			memorial += " deste segue, " + \
			            "delimitado por " + str(adj[13]) +  ", "      + \
			            "confrontando com " + str(adj[16])+ " ("  + str(adj[19]) +   ")"     + \
			            " por azimute "+ str(adj[10]) +" e distÃ¢ncia de "  + \
			            str(adj[9]) + " m atÃ© o vÃ©rtice " + \
			            str(adj[6]) + " de coordenadas N=" + \
			            str(adj[8]) + "m e E=" + str(adj[7]) + "m ;"
	
	
	strFinal = """, ponto inicial da descriÃ§Ã£o deste perÃ­metro. Todas as coordenadas""" +\
	""" aqui descritas estÃ£o georreferenciadas ao Sistema GeodÃ©sico Brasileiro, a partir """ +\
	""" das constantes N=10.000.000,00m e E=500.000,00m, referenciadas ao Meridiano Central 45Â° WGr""" +\
	""" tendo como datum o SIRGAS 2000. Todos os azimutes e distÃ¢ncias, Ã¡reas e perÃ­metros foram calculados no plano de projeÃ§Ã£o UTM."""
	memorial +=  strFinal
	
	now = datetime.now ()
	data =now.strftime("%d  de %B de %Y")
	
	
	
	assina_data ="""\n\n\n\n\n%s, %s\n\n\n"""%( str(cadastro[3]),data)
	
	memorial += assina_data
	
	assinatura = """______________________________\nEmilio Bruno Neto\nEng. Agrimensor - CREA/BA 33601-D\nART %s"""%(str(cadastro[12]))
	
	memorial += assinatura
	
	
	arquivo =open(pasta +  str(cadastro[1])+'_'+str(id) +'_Gleba_'+str(cadastro[14])+'.txt','w')
	arquivo.write(memorial)
	arquivo.close()


del cadastros