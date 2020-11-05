import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
import yfinance as yf
import matplotlib.pyplot as plt
import heapq as hp

def drawdown(serie):

	res = [0]

	for i in range(1,len(serie)):

		res.append(serie[i]/max(serie[0:i+1])-1)

	return res
	
def volatility(serie):
	
	res = float(pd.DataFrame(serie).pct_change(1).std()*np.sqrt(252)*100)  

	return res

def mediaMovil(serie,n):

	res = list(pd.DataFrame(serie).rolling(n).mean())

	return res 

def info_ratio(portfolio_diario,sp_diario,anu_ret_port,anu_ret_sp):
	
	dif = []
	
	for i in range(0,len(sp_diario)):
		
		dif.append(portfolio_diario[i]-sp_diario[i])

	res = (anu_ret_port-anu_ret_sp)/(np.std(dif)*np.sqrt(252))

	return res
def plotear(nombre,modelo,parametros,dates_periodo,sp_periodo,ret_acum,signals):

	plt.figure(figsize=(15,8))
	titulo = nombre+" "+modelo+" "+parametros
	plt.title(titulo)

	plt.plot(dates_periodo,sp_periodo)
	for i in (2,len(signals)):
		if signals[i-1] == 1 and signals[i-2] == 0  :
			plt.scatter(dates_periodo[i], sp_periodo[i], color='green', s=40, marker="v")
			
		
		if signals[i-1] == 0 and signals[i-2] == 1:
			plt.scatter(dates_periodo[i], sp_periodo[i], color='red', s=40, marker="v")
		
	
	plt.plot(dates_periodo,ret_acum) 
	plt.tight_layout()
	plt.savefig()
	plt.close("all")




def anualizar_retorno(serie,dias):
	
	res = ((serie[-1]/serie[0])**(365/dias))-1

	return res

	
def analizar(dic,dateRange,modelo, nombre, today, numResults):

	periods = []

	for i in range(0,len(dateRange)-1):

		p0 = datetime.strptime(dateRange[i], '%Y-%m-%d')
		p1 = datetime.strptime(dateRange[i+1], '%Y-%m-%d')

		periods.append((p0,p1))
		if i == len(dateRange)-2:
			periods.append((p1,datetime.today()))

	p0 = datetime.strptime(dateRange[0], '%Y-%m-%d')
			

	periods.append((p0,datetime.today()))	

	dict_heaps = { periodo: [] for periodo in periods }

	######### dict_heaps[p1] = heap(ret_anualizado_de_param, (dict[param] = [estadisticos]))

	#dic_res tiene key el valor del modelo (una media movil, un umbral ) y value un diccionario con key  signals,date
	for key in dic:	
		
		signals	= dic[key][0]
		dates   = dic[key][1]
		print(len(dates))
		i = 1
		sp = yf.download("^GSPC",dates[0])
		sp = sp["Adj Close"]
		
		for p in periods:
			print(p)

			fechaLimite = p[1]
			ret_diario_porfolio    = [0]
			ret_acumulado_porfolio = [sp[i-1]]
			
			ret_diario_sp          = [sp[i-1]]
			buySignals  =  0
			sellSignals =  0

			dates_periodo = [dates[i-1]]

			tot_seniales = 0
			diasComprado = 0
			porArribaSp  = 0

			while i < len(dates) and dates[i]< fechaLimite:

				dates_periodo.append(dates[i])

				ret_diario_sp.append((sp[i]/sp[i-1]-1)*100)	
				
				tot_seniales+=1
				
				try:
					if signals[i-2] == 1:

						ret_diario_porfolio.append(ret_diario_sp[-1])
						
						ret_acumulado_porfolio.append((ret_diario_sp[-1]+1)*ret_acumulado_porfolio[-1])
						diasComprado+=1

					else:
						
						ret_diario_porfolio.append(0)
						
						ret_acumulado_porfolio.append(ret_acumulado_porfolio[-1])
				
				except:		
					
					ret_diario_porfolio.append(0)
					
					ret_acumulado_porfolio.append(ret_acumulado_porfolio[-1])
				
				if ret_acumulado_porfolio[-1] > sp[i]:
					porArribaSp+=1		

				if signals[i-1] == 0 and signals[i] == 1:
					
					buySignals+=1
				
				elif signals[i-1] == 1 and signals[i] == 0:
					
					sellSignals+=1	

				i+=1
			
			sp_periodo=sp[p[0]:p[1]]

			rdos = {}

			ddn_port = drawdown(ret_acumulado_porfolio)		
			ddn_sp   = drawdown(sp_periodo)
			rdos["ddn_port"] = ddn_port
			rdos["ddn_sp"] = ddn_sp

			volatility_port = volatility(ret_acumulado_porfolio)
			volatility_sp = volatility(sp_periodo)
			rdos["volatility_port"] = volatility_port
			rdos["volatility_sp"] = volatility_sp

			anu_ret_porfolio = anualizar_retorno(ret_acumulado_porfolio,(p[1]-p[0]).days)
			anu_ret_sp = anualizar_retorno(sp_periodo,(p[1]-p[0]).days) 
			rdos["anu_ret_porfolio"] = anu_ret_porfolio
			rdos["anu_ret_sp"] = anu_ret_sp


			sharpeRatio_por = anu_ret_porfolio/volatility_port
			sharpeRatio_sp = anu_ret_sp/volatility_sp
			rdos["sharpeRatio_por"] = sharpeRatio_por
			rdos["sharpeRatio_sp"] = sharpeRatio_sp


			infoRatio = info_ratio(ret_diario_porfolio, ret_diario_sp, anu_ret_porfolio, anu_ret_sp)
			rdos["infoRatio"] = infoRatio

			t_bought = diasComprado / tot_seniales			
			t_above  = porArribaSp  / tot_seniales
			rdos["t_bought"] = t_bought
			rdos["t_above"] = t_above

			hp.heappush(dict_heaps[p], (anu_ret_porfolio, [key, rdos]))
			if len(dict_heaps[p]) > numResults:
				hp.heappop(dict_heaps[p])
			
	return dict_heaps
