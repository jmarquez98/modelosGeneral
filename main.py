import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta,date
import mediaXvsmediaY as mmm
import umbralVSNivel as mu
import utils as u
import transformations as tr

PATH="resultadosModelos/"

def optimizarModelo(name, serie, isItFred, dateRange, numResults, dataFreq, signalType, modelInformation,inv):
	
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
	


			dic_res = mmm.optimizar(ultimaMedia,superposicion,inv,dataFreq,dateRange[0], serie, isItFred, numResults)

		
		elif model == "umbrales":	

			techo = m[1]
			piso  = m[2]
			step  = m[3]
		

			dic_res = mu.optimizar(techo,piso,inv,dataFreq,dateRange, serie, isItFred, numResults)
		
		else:
				
			raise Exception("El modelo ",model," no existe \n")	

		print("Ya se optimizo para ",model,"\n")

		print("Arrancando el analisis...\n")

		top_results = u.analizar(dic_res, dateRange, model, name, today, numResults)
		
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
				u.plotear(name, model, today, rdo[1][0], rdo[1][1]["dates_periodo"], rdo[1][1]["sp_periodo"], rdo[1][1]["ret_acumulado_port"], rdo[1][1]["signals_periodo"])
				u.plotear_ddn(name, model, today, rdo[1][0], rdo[1][1]["dates_periodo"], rdo[1][1]["ddn_sp"], rdo[1][1]["ddn_port"])
				


				parametros.append(rdo[1][0])
				anu_ret_porfolio.append(rdo[1][1]["anu_ret_porfolio"])
				anu_ret_sp.append(rdo[1][1]["anu_ret_sp"])
				volatility_port.append(rdo[1][1]["volatility_port"])
				volatility_sp.append(rdo[1][1]["volatility_sp"])
				sharpeRatio_por.append(rdo[1][1]["sharpeRatio_por"])
				sharpeRatio_sp.append(rdo[1][1]["sharpeRatio_sp"])
				ddn_port.append(min(rdo[1][1]["ddn_port"]))
				ddn_sp.append(min(rdo[1][1]["ddn_sp"]))
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
			df_res["ret_sp"]= anu_ret_sp
			df_res["vol_port"]= sharpeRatio_por
			df_res["vol_sp"]=volatility_sp
			df_res["sharpeRatio_port"]= sharpeRatio_por
			df_res["sharpeRatio_sp"]= sharpeRatio_sp
			df_res["drawdown_port"]=ddn_port
			df_res["drawdown_sp"]= ddn_sp
			df_res["infoRato"]= infoRatio
			
			df_res["numSignBuy"]= sigBuy
			df_res["numSignSell"]= sigSell
			df_res["monthAboveSp"]= t_above
			df_res["monthBelowSp"]= t_below
			df_res["monthBought"]= t_bought
			df_res["monthSold"]= t_sold
			dates_periodo_init=heap[0]
			dates_periodo_fin=heap[1]


			df_res.to_excel(PATH+"{}/{}/{}/res-{}-{}-{}.xlsx".format(name, model, today, dates_periodo_init,dates_periodo_fin, parametros))
	"""		
	dict periodos -> heaps (top 'n' rdos)
		heap: tupla(ret_anualizado, tupla(param, rdos))
	"""

serie = pd.read_csv("BAMLC4A0C710Y.csv")
optimizarModelo("BAMLC4A0C710Y", serie, True, ["2020-01-01","2020-05-01","2020-08-01"], 3, "diario", "pache", [["mediasmoviles", 10, 0.5]], True)