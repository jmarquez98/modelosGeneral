import pandas as pd
from datetime import datetime, timedelta, date
from fredapi import Fred
import mysql.connector
from sqlalchemy import create_engine
import shutil
import os
import yfinance as yf
import transformations as tr

fred = Fred(api_key='28e08a61092c82103eb375231e1aa0e8')
engine = create_engine('mysql+mysqlconnector://root:Delphos.01@localhost:3306/SeriesFred')
  
df_CCSA=fred.get_series_all_releases('CCSA')
df_CLF16OV=fred.get_series_all_releases('CLF16OV')

df_CCSA.to_csv("CCSA.csv")
df_CLF16OV.to_csv("CLF16OV.csv")

realtime_start = []

date = []

value_fin = []
df_nueva = pd.DataFrame()
dic_toRealDate = tr.armarDic_toRealDate(df_CLF16OV)

for i in range(0,len(df_CCSA)):


	rtst = tr.toRealDate(dic_toRealDate, df_CCSA["date"][i]+timedelta(days=12))
	
	if len(rtst) != 0: 
		

				date_list=list(rtst.keys())
				date_list.sort()

				value = []
	
				for j in range(0,len(date_list)):
					
					value.append(rtst[date_list[j]])


	realtime_start.append(df_CCSA["date"][i]+timedelta(days=12))
	date.append(df_CCSA["date"][i])
	value_fin.append(df_CCSA["value"][i]/value[-1])


df_nueva["realtime_start"] = realtime_start

df_nueva["date"] = date

df_nueva["value"] = value_fin


df_nueva.to_excel("CCSATransformado.xlsx")