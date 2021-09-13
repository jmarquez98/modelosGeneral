import numpy as np
import utils as u
import pandas as pd
from datetime import datetime,date,timedelta
import transformations as tr
import yfinance as yf
import utils as u
import math as mt

def optimizar(bmark, name, ultimaMedia,superposicion,inv,dataFreq,startDate, serie, isItFred, numResults,diff_medias):
	#dic_res tiene key el valor del modelo (una media movil, un umbral ) y value un diccionario con key cumRet_SP, cumRet_port, signals,date
	dic_res = {}

	#Si la serie de entrada no es del estilo fred la hago como fred.
	if(not isItFred):
		serie = tr.toFred(serie)
	
	startDate = datetime.strptime(startDate, '%Y-%m-%d')
 		
	

	serie["date"] = pd.to_datetime(serie.date)
	serie["realtime_start"] = pd.to_datetime(serie.realtime_start)
	sp = yf.download(bmark,startDate)
	#Hasra aca tenemos la serie recortada por el periodo a analizar

	serie = serie[serie["date"]> startDate].reset_index()
	
	
	#Llevamos la serie del sp a la frecuencia del indicador.
	valor_freq = 1
	demora     = 1
	
	if dataFreq.lower() == "mensual": 
		valor_freq = 20
		demora     = 15
	elif dataFreq.lower() == "semanal":
		valor_freq = 10
		demora     = 12	
	
	# for rapida in range(2,3):
	# 	for lenta in range(8,9):
	if isItFred:
		dic_toRealDate = tr.armarDic_toRealDate(serie)

	infoFechas = sp.index.to_list()
	
	serie["date"] = pd.to_datetime(serie["date"], infer_datetime_format=True)
	
	for i in range(2*valor_freq+demora,len(sp)):
		
		print("[{}] Faltan {} ruedas".format(name, len(sp)-i))
		
		if isItFred:

			realtime_start = tr.toRealDate(dic_toRealDate,infoFechas[i])
			
			if len(realtime_start) != 0: 

				date_list=list(realtime_start.keys())
				
				date_list.sort()

				value = []
	
				for j in range(0,len(date_list)):
					
					value.append(realtime_start[date_list[j]])
		
		else:	
			
			value = serie["value"][0:i]



		tope1 = ultimaMedia+1 if ultimaMedia+1 < 60 else 60
		for lenta in list(range(2,tope1)) + list(range(60,ultimaMedia+1,5)):
			
			topeRapida =  mt.floor(lenta - lenta*superposicion)
			
			tope2 = topeRapida+1 if topeRapida+1 < 60 else 60
			for rapida in list(range(1,tope2)) + list(range(60,topeRapida+1,5)):
				
				if rapida*(1/superposicion) > lenta:
					break

				if (lenta,rapida) not in dic_res:
					dic_res[(lenta,rapida)] = [[],[]]
						

				
				
				if len(value) > lenta: 
					dic_res[(lenta,rapida)][1].append(infoFechas[i])
					
					mediaMovilLenta = np.mean(value[-lenta:])
					
					mediaMovilRapida = np.mean(value[-rapida:])
						
				
					if mediaMovilRapida*(1+diff_medias) > mediaMovilLenta:
						if inv:
							dic_res[(lenta,rapida)][0].append(0)
						else:	
							dic_res[(lenta,rapida)][0].append(1)
					elif mediaMovilRapida*(1-diff_medias) < mediaMovilLenta:	
						if inv:
							dic_res[(lenta,rapida)][0].append(1)
						else:	
							dic_res[(lenta,rapida)][0].append(0)
					else:			
						try:
							dic_res[(lenta,rapida)][0].append(dic_res[(lenta,rapida)][0][-1])
						except:	
							dic_res[(lenta,rapida)][0].append(0)	

	return dic_res
	

# serie = pd.read_csv("RRSFS.csv")
# print(optimizar(5,0,False,"mensual","2019-01-01", serie, True, 0))
