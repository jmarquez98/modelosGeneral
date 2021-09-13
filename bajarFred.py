import pandas as pd
from datetime import datetime, timedelta, date
from fredapi import Fred
import mysql.connector
from sqlalchemy import create_engine
import shutil
import os
import yfinance as yf
import transformations as tr

########Este codigo necesita arreglar casos borde. SOlo funciona para cuando no necesitamos usar el to real date i.e  series diarias o sin correcciones
def getSerieFred(serie):
	
	fred = Fred(api_key='28e08a61092c82103eb375231e1aa0e8')
	engine = create_engine('mysql+mysqlconnector://root:Delphos.01@localhost:3306/SeriesFred')
	 
	df=fred.get_series_all_releases(serie)

	df = df.set_index("date")
	df = df["value"]


	df.to_csv(serie + ".csv")
	return df