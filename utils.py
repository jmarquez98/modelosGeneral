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

	res = np.std(((np.array(serie[1:])/np.array(serie[:-1]))-1), ddof=1)*np.sqrt(252)*100
	
	# res = float(pd.DataFrame(serie).pct_change(1).std()*np.sqrt(252)*100)  

	return res

def mediaMovil(serie,n):

	res = pd.Series(serie).rolling(n).mean().tolist()

	return res 

def info_ratio(portfolio_diario,sp_diario,anu_ret_port,anu_ret_sp):
	
	dif = np.array(portfolio_diario)-np.array(sp_diario)

	# dif = []
	
	# for i in range(0,len(sp_diario)):
		
	# 	dif.append(portfolio_diario[i]-sp_diario[i])

	res = (anu_ret_port-anu_ret_sp)/(np.std(dif)*np.sqrt(252))

	return res

def plotear(nombre,modelo,today,parametros,dates_periodo,sp_periodo,ret_acum,signals):

	plt.figure(figsize=(15,8))
	titulo = "{} {} {}".format(nombre, modelo, parametros)
	plt.title(titulo)

	# print(parametros)
	# print(dates_periodo)
	# print(sp_periodo)
	plt.plot(dates_periodo,sp_periodo)
	
	for i in range(2,len(signals)):
		
		if signals[i-1] == 1 and signals[i-2] == 0  :
			plt.scatter(dates_periodo[i], sp_periodo[i], color='green', s=40, marker="v")
			
		
		if signals[i-1] == 0 and signals[i-2] == 1:
			plt.scatter(dates_periodo[i], sp_periodo[i], color='red', s=40, marker="v")
	df = pd.DataFrame()

	plt.plot(dates_periodo,ret_acum) 
	plt.yscale('log')
	plt.tight_layout()
	plt.savefig("resultadosModelos/{}/{}/{}/ret-[{}~{}]-{}.png".format(nombre, modelo, today, dates_periodo[0].strftime("%Y-%m-%d"), dates_periodo[-1].strftime("%Y-%m-%d"), parametros))
	plt.close("all")

def plotear_ddn(bmark,nombre,modelo,today,parametros,dates_periodo,ddn_sp,ddn_port):
	plt.figure(figsize=(15,8))
	plt.title("Drawdown portfolio vs "+bmark)
	plt.ylabel("Drawdown")
	plt.xlabel("Fechas")
	plt.fill_between(dates_periodo,ddn_sp, color='blue', alpha=0.3,label=bmark)
	plt.fill_between(dates_periodo,ddn_port, color='orange', alpha=0.3,label="Drawdown")
	plt.legend(loc="lower left")
	plt.tight_layout()
	plt.savefig("resultadosModelos/{}/{}/{}/ddn-[{}~{}]-{}.png".format(nombre, modelo, today, dates_periodo[0].strftime("%Y-%m-%d"), dates_periodo[-1].strftime("%Y-%m-%d"), parametros))
	plt.close("all")


def anualizar_retorno(serie,dias):
	
	res = ((serie[-1]/serie[0])**(365/dias))-1

	return res

	
def analizar(bmark, dic,dateRange,modelo, nombre, today, numResults,paramTooptimize):
	print(dic)
	periods = []

	optimize = {}

	optimize["retorno anualizado"]= "anu_ret_porfolio"
	optimize["drawdown"]= "ddn_port"
	optimize["information ratio"]= "infoRatio"
	optimize["sharpe ratio"]= "sharpeRatio_por"
	optimize["volatilidad anualizada"]= "volatility_port"

	
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
	
	sp_total = yf.download(bmark,datetime.strptime(dateRange[0], '%Y-%m-%d'),datetime.today()-timedelta(days=1))
	sp_total = sp_total["Adj Close"]

	# sp_cada_periodo = {}
	# for p in periods:
	# 	sp_cada_periodo[p]= sp_total[p[0]:p[1]-timedelta(days=1)]

	
	for key in dic:	
		print("Analizando para ", key)
		primera = True
		
		signals	= dic[key][0]
		dates   = dic[key][1]

		sp = sp_total[dates[0]:]

		# sp = yf.download("^GSPC",dates[0],datetime.today()-timedelta(days=1))
		# sp = sp["Adj Close"]
	
		i = 1
		periodosRestantes = len(periods)
		for p in periods:
			#print(p)

			if periodosRestantes == 1:
				i = 1
			
				
			fechaLimite = p[1]
			ret_diario_porfolio    = [0]
			ret_acumulado_porfolio = [sp[i-1]]
			
			ret_diario_sp          = [0]
			buySignals  =  0
			sellSignals =  0
			if not  primera  and periodosRestantes > 1:
				i+=1
			
			dates_periodo = [dates[i-1]]

			signals_periodo = [signals[i-1]]

			tot_seniales = 0
			diasComprado = 0
			porArribaSp  = 0
			periodosRestantes-=1
			# print(len(signals))
			while i < len(dates) and dates[i]< fechaLimite and i< len(sp):

				dates_periodo.append(dates[i])
				signals_periodo.append(signals[i])

				ret_diario_sp.append((sp[i]/sp[i-1]-1))	
				
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

			sp_periodo=sp[p[0]:p[1]-timedelta(days=1)]
			
			# sp_periodo=sp_cada_periodo[p]
			
			primera = False
			
			# print(dates_periodo[0])
			# print(sp_periodo.index[0])
			# print(dates_periodo[-1])
			# print(sp_periodo.index[-1])
			# print(len(dates_periodo))
			# print(len(sp_periodo))
			
			rdos = {}
			rdos[bmark+"_periodo"] = sp_periodo
			# rdos["ret_diario_sp"] = ret_diario_sp
			rdos["signals_periodo"] = signals_periodo

			rdos["dates_periodo"] = dates_periodo

			if paramTooptimize.lower() == "drawdown":
			
				ddn_port = drawdown(ret_acumulado_porfolio)		
				ddn_sp   = drawdown(sp_periodo)
				rdos["ddn_port"] = ddn_port
				rdos["ddn_"+bmark] = ddn_sp

			if paramTooptimize.lower() in {"volatilidad anualizada"}:
				
				volatility_port = volatility(ret_acumulado_porfolio)
				volatility_sp = volatility(sp_periodo)
				rdos["volatility_port"] = volatility_port
				rdos["volatility_"+bmark] = volatility_sp
			print(ret_acumulado_porfolio)
			anu_ret_porfolio = anualizar_retorno(ret_acumulado_porfolio,(p[1]-p[0]).days)
			anu_ret_sp = anualizar_retorno(sp_periodo,(p[1]-p[0]).days) 
			rdos["anu_ret_porfolio"] = anu_ret_porfolio
			rdos["anu_ret_"+bmark] = anu_ret_sp

			rdos["ret_acumulado_port"] = ret_acumulado_porfolio

			if paramTooptimize.lower() in {"sharpe ratio"}:
				
				sharpeRatio_por = anu_ret_porfolio/volatility_port
				sharpeRatio_sp = anu_ret_sp/volatility_sp
				rdos["sharpeRatio_por"] = sharpeRatio_por
				rdos["sharpeRatio_"+bmark] = sharpeRatio_sp
			
			rdos["ret_diario_porfolio"] = ret_diario_porfolio
			rdos["ret_diario_"+bmark]	=ret_diario_sp
			
			if paramTooptimize.lower() in {"info ratio"}:
				
				infoRatio = info_ratio(ret_diario_porfolio, ret_diario_sp, anu_ret_porfolio, anu_ret_sp)
				rdos["infoRatio"] = infoRatio

			if tot_seniales > 0:
				t_bought = diasComprado / tot_seniales			
				t_above  = porArribaSp  / tot_seniales
				rdos["t_bought"] = t_bought
				rdos["t_above"] = t_above
			
			
			if paramTooptimize.lower() == "drawdown":
				toOpt = min(rdos["ddn_port"])
			elif paramTooptimize.lower() in {"volatilidad anualizada"}:
				toOpt = rdos["volatility_port"] * (-1)
			else:
				toOpt = rdos[optimize[paramTooptimize.lower()]]
				

			hp.heappush(dict_heaps[p], (toOpt, [key, rdos]))
			if len(dict_heaps[p]) > numResults:
				hp.heappop(dict_heaps[p])
	

	for heap in dict_heaps.keys(): 			

		for t in dict_heaps[heap]:
			
			ddn_port = drawdown(t[1][1]["ret_acumulado_port"])		
			ddn_sp   = drawdown(t[1][1][bmark+"_periodo"])
			t[1][1]["ddn_port"] = ddn_port
			t[1][1]["ddn_"+bmark] = ddn_sp

			volatility_port = volatility(t[1][1]["ret_acumulado_port"])
			volatility_sp = volatility(t[1][1][bmark+"_periodo"])
			t[1][1]["volatility_port"] = volatility_port
			t[1][1]["volatility_"+bmark] = volatility_sp


			sharpeRatio_por = t[1][1]["anu_ret_porfolio"]/volatility_port
			sharpeRatio_sp = t[1][1]["anu_ret_"+bmark]/volatility_sp
			t[1][1]["sharpeRatio_por"] = sharpeRatio_por
			t[1][1]["sharpeRatio_"+bmark] = sharpeRatio_sp

			infoRatio = info_ratio(t[1][1]["ret_diario_porfolio"], t[1][1]["ret_diario_"+bmark], t[1][1]["anu_ret_porfolio"], t[1][1]["anu_ret_"+bmark])
			t[1][1]["infoRatio"] = infoRatio



	return dict_heaps

