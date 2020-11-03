import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta,date
import modeloMediasMoviles as mmm
import modeloUmbrales as mu
import utils as u

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
		print("Optimizando para ",modeloActual,"\n")
		
		#Lo que devuelve cada optimizacion son dic de longitud numResults
		# De ahi decidimos el mejor
		#dic_res tiene key el valor del modelo (una media movil, un umbral ) y value un diccionario con key annualizedRet_SP, annualizedRet_port, signals
		if model == "mediasmoviles":
		
			ultimaMedia = m[1]
			superposicion = m[2]
	


			dic_res = mmm.optimizar(ultimaMedia,superposicion,inv,dataFreq,dateRange, serie, isItFred, numResults)

		
		elif model == "umbrales":	

			techo = m[1]
			piso  = m[2]
			step  = m[3]
		

			dic_res = mu.optimizar(techo,piso,inv,dataFreq,dateRange, serie, isItFred, numResults)
		
		else:
				
			raise Exception("El modelo ",modeloActual," no existe \n")	

		print("Ya se optimizo para ",modeloActual,"\n")


		#Lo que devuelve son vectores de longitud numResults
		parametros,annualizedRet_SP, annualizedRet_port, vol, sharpeRatio, infoRatio, drawdown, numSignBuy, numSignSell, monthAboveSp, monthBelowSp, monthBought, monthSold = u.analizar(dic_res) 

		df_res = pd.DataFrame()

		df_res["parametro"]= parametros
		df_res["ret_sp"]= annualizedRet_SP
		df_res["ret_port"]= annualizedRet_port
		df_res["vol"]= vol
		df_res["sharpeRatio"]= sharpeRatio
		df_res["drawdown"]= drawdown
		df_res["numSignBuy"]= numSignBuy
		df_res["numSignSell"]= numSignSell
		df_res["monthAboveSp"]= monthAboveSp
		df_res["monthBelowSp"]= monthBelowSp
		df_res["monthBought"]= monthBought
		df_res["monthSold"]= monthSold


		df_res.to_excel(PATH+name+"/"+model+"/"+today+"/resultados.xlsx")
