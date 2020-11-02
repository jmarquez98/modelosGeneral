import pandas as pd
import numpy as np
from datetime import datetime, timedelta

####Voy a recibir un pandas dataframe con columnas realtime_start	date	value
####Y una fecha limite. Voy a devolver un diccionario key=real_date, value=[Value, dateOfValue]
####Tal que me devuelva los datos hasta la fecha pasada como parametro, que es el dia que yo analizo
####EL formato de las fechas TIENE que ser %Y-%m-%d (datetime python)
####Las fechas que vengan en formato string y aca las transformamos
def toRealDate(df, date_end):
	"""Hay un caso borde que es cuando el realtime es posterior al la fecha del periodo de referencia
	   Osea para los datos anteriores al primer realtime del primer datos (Ej datos de 1929 con realtime en 2010)
	   Para eso haremos un estimativo de cuanto tardan en publicarse los datos y generaremos un realtimefake estimado para esos datos"""

	fechaInicioReal = datetime.strptime(df["realtime_start"][0], '%Y-%m-%d')

	tenemosDiferencia = False #Variable boolean para saber si ya calcule la diferencia (quiero hacerla para el primer caso que es cuando estoy en los datos que se actualizan normalmente, no los cargado al arranque)
	diferenciaDias = None # Aca voy a tener la diferencia de dias entre el dato y la carga
	################
	date_end =  datetime.strptime(date_end, '%Y-%m-%d')#Cambio el tipo de dato de la fecha. De string a datetime

	dic_realtime = {}# Diccionario de respuesta, con las fechas reales segun date_end

	############################

	dic_date = {} # Voy a guardar para cada date todos los values que tiene y su real date asociada.
	#El formato va a ser diccionario con key date y value arreglo de [realtime, value]. Osea me quedan
	#Para date todos sus values posibles
	for i in range(0,len(df)): 
		
		d =  datetime.strptime(df["date"][i], '%Y-%m-%d') 
		
		if d in  dic_date:

			dic_date[d].append([datetime.strptime(df["realtime_start"][i], '%Y-%m-%d') ,df["value"][i]])
		
		elif d not  in  dic_date:	

			dic_date[d] = []
			
			dic_date[d].append([datetime.strptime(df["realtime_start"][i], '%Y-%m-%d') ,df["value"][i]])
		
		else:
		
			raise Exception("Error toRealDate.py armando diccionario de fechas. El date no esta y tampoco esta.")

		if  fechaInicioReal < datetime.strptime(df["date"][i], '%Y-%m-%d') and not tenemosDiferencia: # Cuando llego al caso de que son datos cargados en vivo y no los que se cargaron todos juntos al inicio calculo la diferencia
			
			tenemosDiferencia = True
		
			diferenciaDias  = (datetime.strptime(df["realtime_start"][i], '%Y-%m-%d') - datetime.strptime(df["date"][i], '%Y-%m-%d')).days
			print(diferenciaDias)


	for date in dic_date: # Para los datos cargados todos juntos les armo un realtime estimado fake de diferenciaDias mas entre su date
		
		if date  <	fechaInicioReal:

			value = dic_date[date][0][1]

			real_estimado =  date + timedelta(days=diferenciaDias)
			
			dic_date[date].append([real_estimado ,value])		

   
	for date in dic_date: # Me quedo con los datos mas recientes anteriores a mi fecha limite.
		
		if date  <	date_end:

			real_values = dic_date[date]

			real_values.sort()
			disponibles = [a for a in real_values if a[0] < date_end]

			if len(disponibles) > 0: # Esto es porque pueden ser el caso de que el date sea valido pero el real no lo sea entonces no hay datos posibles
				

				dic_realtime[date] = [disponibles[-1][0],disponibles[-1][1]]



	



