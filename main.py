import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta,date
import modeloMediasMoviles as mmm
import modeloUmbrales as mu

PATH="resultadosModelos/"

def optimizarModelo(name, serie, isItFred, dateRange, numResults, dataFreq, signalType, modelInformation,inv):
	
	#Creo el directorio del modelo, formato: Nombre/modelo/fecha
	
	print("Creando carpetas ... \n")
	
	if not os.path.exists(PATH+name):
		
		os.makedirs(PATH+name)
	for m in modelInformation:	
		
		model = lower(m[0])
		
		if not os.path.exists(PATH+name+"/"+model):
	    	
			os.makedirs(PATH+name+"/"+model)

		if not os.path.exists(PATH+name+"/"+model+"/"+date.today().strftime("%Y-%m-%d")):
	    	
			os.makedirs(PATH+name+"/"+model+"/"+date.today().strftime("%Y-%m-%d"))	
		
	print("Carpetas creadas correctamente \n")

	#Itero sobre el arreglo modelInformation llamando al modelo solicitado 
	
	print("Optimizando modelos...")

	for m in modelInformation:
		
		model = lower(m[0])
		
		""" Orden de los parametros segun modelo:
				
				UMBRAL: TECHO,PISO,STEP  


				MEDIAS MOVILES:  FIN, SUPERPOSICION

			
			Y luego los parametros generales van al final:
			inv, dataFreq, dateRange, serie, isItFred, numResults

		"""
		print("Optimizando para ",modeloActual,"\n")
		
		#Lo que devuelve cada optimizacion son arreglos de longitud numResults
		# De ahi decidimos el mejor
		
		if model == "mediasmoviles":
		
			ultimaMedia = m[1]
			superposicion = m[2]
	


			annualizedRet_SP, annualizedRet_port, vol, sharpeRatio, infoRatio, drawdown, numSignBuy, numSignSell, monthAboveSp, monthBelowSp, monthBought, monthSold = mmm.optimizar(ultimaMedia,superposicion,inv,dataFreq,dateRange, serie, isItFred, numResults
)
		
		elif model == "umbrales":	

			techo = m[1]
			piso = m[2]
			step = m[3]
		

			annualizedRet_SP, annualizedRet_port, vol, sharpeRatio, infoRatio, drawdown, numSignBuy, numSignSell, monthAboveSp, monthBelowSp, monthBought, monthSold = mu.optimizar(techo,piso,inv,dataFreq,dateRange, serie, isItFred, numResults
)
		
		else:
				
				print("El modelo ",modeloActual," no existe \n")	

		print("Ya se optimizo para ",modeloActual,"\n")