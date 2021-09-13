import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta,date
import mediaXvsmediaY as mmm
import umbralVSNivel as mu
import umbralSimpleVsNivel as mus
import utils as u
import transformations as tr
import yfinance as yf
import sys
import bajarFred as bf
PATH="resultadosModelos/"

def optimizarModelo(bmark, name, serie, isItFred, dateRange, numResults, dataFreq, signalType, paramTooptimize,modelInformation,inv,diff_medias):
	
	#Creo el directorio del modelo, formato: Nombre/modelo/fecha
	today = date.today().strftime("%Y-%m-%d")
	print("Creando carpetas ... \n")
	
	if not os.path.exists(PATH+name):
		
		os.makedirs(PATH+name)
	for m in modelInformation:	
		
		model = m[0].lower()
		
		if not os.path.exists(PATH+name+"/"+model):
	    	
			os.makedirs(PATH+name+"/"+model)

		if not os.path.exists(PATH+name+"/"+model+"/"+today):
	    	
			os.makedirs(PATH+name+"/"+model+"/"+today)	
		
	print("Carpetas creadas correctamente \n")

	#Itero sobre el arreglo modelInformation llamando al modelo solicitado 
	
	


	print("Optimizando modelos...")

	


	for m in modelInformation:
		
		model = m[0].lower()
		
		""" Orden de los parametros segun modelo:
				
				UMBRAL: TECHO,PISO,STEP  


				MEDIAS MOVILES:  FIN, SUPERPOSICION

			
			Y luego los parametros generales van al final:
			inv, dataFreq, dateRange, serie, isItFred, numResults

		"""
		print("Optimizando para ",model,"\n")
		
		#Lo que devuelve cada optimizacion son dic de longitud numResults
		# De ahi decidimos el mejor
		#dic_res tiene key el valor del modelo (una media movil, un umbral ) y value un diccionario con key  signals,date
		if model == "mediasmoviles":
		
			ultimaMedia = m[1]
			superposicion = m[2]
	

			f = open(PATH+"{}/{}/{}/parametros.txt".format(name, model, today),"w+")

			f.write("BMARK: "+ bmark)
			f.write("\n")
			f.write("NAME: "+name)
			f.write("\n")
			f.write("ultima Media: "+str(ultimaMedia))
			f.write("\n")
			f.write("Superposicion: "+str(superposicion))
			f.write("\n")
			f.write("Inverso: "+str(inv))
			f.write("\n")
			f.write("Frecuencia: "+dataFreq)
			f.write("\n")
			f.write("Inicio: "+dateRange[0])
			f.write("\n")
			f.write("Fred: "+str(isItFred))
			f.write("\n")
			f.write("cantidad Resultados: "+str(numResults))
			f.write("\n")
			f.write("diferencia medias: "+str(1+diff_medias))
			f.write("\n")



			f.close()

			dic_res = mmm.optimizar(bmark, name, ultimaMedia,superposicion,inv,dataFreq,dateRange[0], serie, isItFred, numResults,diff_medias)
			

		
		elif model == "umbrales":	

			techo = m[1]
			piso  = m[2]
			step  = m[3]
			

			dic_res = mu.optimizar(bmark,name, techo,piso,step,inv,dataFreq,dateRange[0], serie, isItFred, numResults)
			
		

		elif model == "un umbral":	

			techo = m[1]
			piso  = m[2]
			step  = m[3]
			

			dic_res = mus.optimizar(bmark,name, techo,piso,step,inv,dataFreq,dateRange[0], serie, isItFred, numResults)

		
		
		else:
				
			raise Exception("El modelo ",model," no existe \n")	

		print("Ya se optimizo para ",model,"\n")

		print("Arrancando el analisis...\n")
		
		top_results = u.analizar(bmark, dic_res, dateRange, model, name, today, numResults,paramTooptimize)
		
		#Lo que devuelve son vectores de longitud numResults
		
		# parametros,annualizedRet_SP, annualizedRet_port, vol, sharpeRatio, infoRatio, drawdown, numSignBuy, numSignSell, monthAboveSp, monthBelowSp, monthBought, monthSold = u.analizar(dic_res) 
	
		print("Analisis terminado, vamos con los gráficos \n")
		# return(top_results)
		for heap in top_results.keys():
			df_res = pd.DataFrame()
			
			parametros=[]
			anu_ret_porfolio=[]
			anu_ret_sp=[]
			volatility_port=[]
			volatility_sp=[]
			sharpeRatio_por=[]
			sharpeRatio_sp=[]
			ddn_port=[]
			ddn_sp=[]
			infoRatio=[]
			
			sigBuy=[]
			sigSell=[]
			
			t_above=[]
			t_below=[]
			t_bought=[]
			t_sold=[]



			for rdo in top_results[heap]:
				u.plotear(name, model, today, rdo[1][0], rdo[1][1]["dates_periodo"], rdo[1][1][bmark+"_periodo"], rdo[1][1]["ret_acumulado_port"], rdo[1][1]["signals_periodo"])
				u.plotear_ddn(bmark, name, model, today, rdo[1][0], rdo[1][1]["dates_periodo"], rdo[1][1]["ddn_"+bmark], rdo[1][1]["ddn_port"])
				


				parametros.append(rdo[1][0])
				anu_ret_porfolio.append(rdo[1][1]["anu_ret_porfolio"])
				anu_ret_sp.append(rdo[1][1]["anu_ret_"+bmark])
				volatility_port.append(rdo[1][1]["volatility_port"])
				volatility_sp.append(rdo[1][1]["volatility_"+bmark])
				sharpeRatio_por.append(rdo[1][1]["sharpeRatio_por"])
				sharpeRatio_sp.append(rdo[1][1]["sharpeRatio_"+bmark])
				ddn_port.append(min(rdo[1][1]["ddn_port"]))
				ddn_sp.append(min(rdo[1][1]["ddn_"+bmark]))
				infoRatio.append(rdo[1][1]["infoRatio"])
				

				compra = 0
				venta  = 0
				for i in range(1,len(rdo[1][1]["signals_periodo"])):
					
					if(rdo[1][1]["signals_periodo"][i]==1 and rdo[1][1]["signals_periodo"][i-1]==0):
						compra+=1
					if(rdo[1][1]["signals_periodo"][i]==0 and rdo[1][1]["signals_periodo"][i-1]==1):
						venta+=1	



				sigBuy.append(compra)
				sigSell.append(venta)
				
				t_above.append(rdo[1][1]["t_above"])
				t_below.append(1- rdo[1][1]["t_above"])
				t_bought.append(rdo[1][1]["t_bought"])
				t_sold.append(1- rdo[1][1]["t_bought"])



		
			df_res["parametro"]=parametros  
			df_res["ret_port"]= anu_ret_porfolio
			df_res["ret_"+bmark]= anu_ret_sp
			df_res["vol_port"]= volatility_port
			df_res["vol_"+bmark]=volatility_sp
			df_res["sharpeRatio_port"]= sharpeRatio_por
			df_res["sharpeRatio_"+bmark]= sharpeRatio_sp
			df_res["drawdown_port"]=ddn_port
			df_res["drawdown_"+bmark]= ddn_sp
			df_res["infoRato"]= infoRatio
			
			df_res["numSignBuy"]= sigBuy
			df_res["numSignSell"]= sigSell
			df_res["monthAbove"+bmark]= t_above
			df_res["monthBelow"+bmark]= t_below
			df_res["monthBought"]= t_bought
			df_res["monthSold"]= t_sold
			dates_periodo_init=heap[0]
			dates_periodo_fin=heap[1]

			df_res.to_excel(PATH+"{}/{}/{}/res-[{}~{}].xlsx".format(name, model, today, dates_periodo_init.strftime("%Y-%m-%d"),dates_periodo_fin.strftime("%Y-%m-%d")))
	"""		
	dict periodos -> heaps (top 'n' rdos)
		heap: tupla(ret_anualizado, tupla(param, rdos))
	"""
# serie = yf.download("^GSPC")["Adj Close"]
#optimizarModelo("SP500", serie, False, ["1928-01-01","1933-04-05","1971-08-15","2009-03-06"], 50, "diario", "pache", "DrAwDowN" ,[["mediasmoviles", 756, 0.5]], False)

# import time
# import os

# f = open("tiempos.txt", "a+")
# start_time = time.time()
# optimizarModelo("SP500", serie, False, ["2020-06-01"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 30, 0.5]], False)
# f.write("--- %s seconds ---" % (time.time() - start_time))
# f.write("\n")
# f.close

#serie = pd.read_excel("CCSATransformado.xlsx")
#optimizarModelo("CCSATransformado", serie, True, ["2000-01-01","2008-01-01","2020-01-01"], 5, "semanal", "pache","retorno Anualizado" ,[["mediasmoviles", 40,0.85]], True)

# import time
# start_time = time.time()
# ### INSERT ALGO PARA CORRER
# print("--- %s seconds ---" % (time.time() - start_time))

# serie = yf.download("EWZ")["Adj Close"]
# optimizarModelo("EWZ", "EWZ", serie, False, ['2000-07-14','2009-03-06'], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False)
"""
etf = "DX-Y.NYB"
serie = yf.download(etf)["Adj Close"]['2000-07-14':]

optimizarModelo("EWZ", etf, serie, False, ['2000-07-14','2009-03-06'], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0.05)


etf = "DJCI"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False, ['2009-10-29'], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False)

etf = "ENOR"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False, ["2012-01-24"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False)



etf = "EEM"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False, ['2003-04-14',"2009-03-06"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 100, 0.5]], False)


etf = "EWM"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["1996-03-18","2009-03-06"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False)

etf = "EWY"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False, ["2000-05-12","2009-03-06"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False)



etf = "EIDO"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2010-05-07"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False)


etf = "INDA"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2012-02-03"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False)


etf = "EWT"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2000-06-23","2009-03-06"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False)


etf = "THD"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2008-04-01"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False)

etf = "QUAL"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2013-07-18"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)

etf = "MTUM"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False, ["2013-04-18"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)



etf = "IWM"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2000-05-26","2009-03-06"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)


etf = "ESGU"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2016-12-06"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)


etf = "SUSL"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2019-05-10"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)


etf = "IWC"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2005-08-16"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)


etf = "EZA"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2003-02-07"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)

serie = pd.read_excel("news_sentiment_data.xlsx")
serie = serie.set_index("date")
serie = serie["News Sentiment"]
optimizarModelo("^GSPC", "news_sentiment_data", serie, False, ["1980-01-01","2009-03-06"], 5, "diario", "pache", "retorno Anualizado" ,[["un umbral", 0.6,-0.6, 0.002]], False,0)


etf = "EPHE"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False, ["2010-09-29"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 10, 0.5]], False,0)


etf = "THD"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2008-04-01"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False)

etf = "QUAL"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2013-07-18"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)

etf = "MTUM"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False, ["2013-04-18"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)



etf = "IWM"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2000-05-26","2009-03-06"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)


etf = "ESGU"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2016-12-06"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)


etf = "SUSL"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2019-05-10"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)


etf = "IWC"
serie = yf.download(etf)["Adj Close"]
optimizarModelo(etf, etf, serie, False,["2005-08-16"], 5, "diario", "pache", "retorno Anualizado" ,[["mediasmoviles", 756, 0.5]], False,0)

etfs = ['XLU',
'XLP',
'XLY',
'XHB',
'XTN',
'XLV',
'XHE',
'XHS',
'XBI',
'XPH',
'XLK',
'XSD',
'XSW',
'XTH',
'XLB',
'XME',
'XLF',
'XLE',
'XES'
]
for etf in etfs:

	serie = yf.download(etf)["Adj Close"]
	,"1971-08-15"

"""

bmark = sys.argv[1] 
name = sys.argv[2]
serie = bf.getSerieFred(sys.argv[3])

fred = True
if  sys.argv[4] == "False":
	fred = False


d = sys.argv[5]
numRes = int(sys.argv[6])
freq = sys.argv[7]
vacio=sys.argv[8]
maximizar = sys.argv[9]
modelo=[[sys.argv[10],int(sys.argv[11]),float(sys.argv[12])]]

inv = True
if  sys.argv[13] == "False":
	inv = False
diff= float(sys.argv[14])

dateRange = [d]

d = datetime.strptime(d, "%Y-%m-%d")

if d < datetime(1968,1,1):

	dateRange.append("1971-08-15")

	dateRange.append("2009-03-06")

elif d < datetime(2005,1,1):	

	dateRange.append("2009-03-06")


optimizarModelo(bmark,name,serie,fred,dateRange,numRes,freq,vacio,maximizar,modelo,inv,diff)
