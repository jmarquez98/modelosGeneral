import numpy as np
import utils as u
import pandas as pd
from datetime import datetime,date,timedelta
import transformations as tr
import yfinance as yf
import utils as u
import math as mt

def optimizar(ultimaMedia,superposicion,inv,dataFreq,startDate, serie, isItFred, numResults):
	#dic_res tiene key el valor del modelo (una media movil, un umbral ) y value un diccionario con key cumRet_SP, cumRet_port, signals,date
	dic_res = {}

	#Si la serie de entrada no es del estilo fred la hago como fred.
	if(not isItFred):
		serie = tr.toFred(serie)
	
	startDate = datetime.strptime(startDate, '%Y-%m-%d')
 		
	

	serie["date"] = pd.to_datetime(serie.date)
	serie["realtime_start"] = pd.to_datetime(serie.realtime_start)
	sp = yf.download("^GSPC",startDate)
	#Hasra aca tenemos la serie recortada por el periodo a analizar

	serie = serie[serie["date"]> startDate].reset_index()
	
	
	#Llevamos la serie del sp a la frecuencia del indicador.
	valor_freq = 1
	demora     = 1
	
	if dataFreq.lower() == "mensual": 
		valor_freq = 20
		demora     = 15
	
	# for rapida in range(2,3):
	# 	for lenta in range(8,9):
	for lenta in range(2,ultimaMedia+1):
		topeRapida = lenta - mt.floor(lenta*superposicion)
		for rapida in range(1,topeRapida+1):
			dic_res[(lenta,rapida)] = [[],[]]
			print("Arrancando analisis para medias movil rapida ",rapida, " y lenta ",lenta,"\n")
											
			for i in range(lenta*valor_freq+demora,len(sp)):
				# print("Me faltan ",len(sp)-i," ruedas")

				
				#print(sp.index.to_list()[i])
				# print(serie)
				realtime_start = tr.toRealDate(serie,sp.index.to_list()[i])
				
				if len(realtime_start) != 0: 
					dic_res[(lenta,rapida)][1].append(sp.index.to_list()[i])

					date_list=list(realtime_start.keys())
					date_list.sort()

					value = []
		
					for j in range(0,len(date_list)):
						
						value.append(realtime_start[date_list[j]])
					# print(realtime_start)
					# print(value)

					mediaMovilLenta = u.mediaMovil(value,lenta)
					
					mediaMovilRapida = u.mediaMovil(value,rapida)	

					if mediaMovilRapida[-1] > mediaMovilLenta[-1]:
						if inv:
							dic_res[(lenta,rapida)][0].append(0)
						else:	
							dic_res[(lenta,rapida)][0].append(1)
					else:	
						if inv:
							dic_res[(lenta,rapida)][0].append(1)
						else:	
							dic_res[(lenta,rapida)][0].append(0)	
		
	return dic_res
	

# serie = pd.read_csv("RRSFS.csv")
# print(optimizar(5,0,False,"mensual","2019-01-01", serie, True, 0))
