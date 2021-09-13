import numpy as np
import utils as u
import pandas as pd
from datetime import datetime,date,timedelta
import transformations as tr
import yfinance as yf
import utils as u
import math as mt

def optimizar(bmark,name,techo,piso,step,inv,dataFreq,startDate, serie, isItFred, numResults):
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

	serie = serie[serie["date"]>= startDate].reset_index()

	if isItFred:
		dic_toRealDate = tr.armarDic_toRealDate(serie)

	infoFechas = sp.index.to_list()
	
	for i in range(1,len(sp)):
		
		print("[{}] Faltan {} ruedas".format(name, len(sp)-i))
		
		value = []
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
	
		for umbral in np.arange(piso,techo,step):
			if umbral not in dic_res:
				dic_res[umbral] = [[],[]]
										
			if len(value) > 0:	
				
				dic_res[umbral][1].append(infoFechas[i])
				

				if value.iloc[-1] > umbral:
					if inv:
						dic_res[umbral][0].append(0)
					else:	
						dic_res[umbral][0].append(1)
				
				elif value.iloc[-1] < umbral: 		
				
					if inv:
						dic_res[umbral][0].append(1)
					else:	
						dic_res[umbral][0].append(0)	
				else:
					try:
						dic_res[umbral][0].append(dic_res[umbral][0][-1])
					except:
						dic_res[umbral][0].append(0)	
			else:
				try:
					dic_res[umbral][0].append(dic_res[umbral][0][-1])
				except:
					dic_res[umbral][0].append(0)

	return dic_res
	

