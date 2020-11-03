import numpy as np
import utils as u
import pandas as pd
from datetime import datetime,date,timedelta

def optimizar(ultimaMedia,superposicion,inv,dataFreq,dateRange, serie, isItFred, numResults):
	return nnualizedRet_SP, annualizedRet_port, vol, sharpeRatio, infoRatio, drawdown, numSignBuy, numSignSell, monthAboveSp, monthBelowSp, monthBought, monthSold