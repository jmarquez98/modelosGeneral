import numpy as np
import utils as u
import pandas as pd
from datetime import datetime,date,timedelta


def optimizar(techo,piso,inv,dataFreq,dateRange, serie, isItFred, numResults):
	#dic_res tiene key el valor del modelo (una media movil, un umbral ) y value un diccionario con key annualizedRet_SP, annualizedRet_port, signals,date
	dic_res = {}

	return dic_res