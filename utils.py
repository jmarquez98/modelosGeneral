import numpy as np
import pandas as pd

def drawdown(serie):

	res = [0]

	for i in range(1,len(serie))

		res.append(serie[i]/max(serie[0:i+1])-1)

	return res
	
def volatility(serie):
	
	res = float(pd.DataFrame(serie).pct_change(1).std()*np.sqrt(252)*100)  

	return res

def mediaMovil(serie,n):

	res = list(pd.DataFrame(serie).rolling(n).mean())

	return res 
	
def analizar(dic):





	return parametros,annualizedRet_SP, annualizedRet_port, vol, sharpeRatio, infoRatio, drawdown, numSignBuy, numSignSell, monthAboveSp, monthBelowSp, monthBought, monthSold parametros,annualizedRet_SP, annualizedRet_port, vol, sharpeRatio, infoRatio, drawdown, numSignBuy, numSignSell, monthAboveSp, monthBelowSp, monthBought, monthSold 

