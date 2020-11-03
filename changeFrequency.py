from datetime import datetime, timedelta
import pandas as pd

# Los inputs deberían ser series de pandas con las fechas reales como indice, se asume que estan acotadas [fecha_inicio:fecha_fin] (son del mismo periodo)
def spDailyToMonthly(diario_sp, mensual_indicador):

    # Al copiar el mensual del indicador, hacemos una copia del indice mensual, por eso itero luego por las fechas del index para extraer el mensual del sp
    mensual_sp = mensual_indicador.copy()
    for mes in mensual_sp.index:
        mes_sp = mes

        # La primera parte del if salva el caso en el que la primer fecha mensual sea menor a la primera fecha diaria del sp, por un par de dias (finde o algo por el estilo)
        if mes_sp < diario_sp.index[0]:
            mensual_sp[mes] = diario_sp[diario_sp.index[0]]
        
        # La segunda parte del if busca el precio del sp para la el 1ro del mes, si justo el 1ro no fue una rueda, va para atras a buscar el ultimo precio
        else:
            while (True):
                if mes_sp in diario_sp.index:
                    mensual_sp[mes] = diario_sp[mes_sp]
                    break
                else:
                    mes_sp = mes_sp - timedelta(days=1)
    
    return mensual_sp


# Los inputs deberían ser series de pandas con las fechas reales como indice, se asume que estan acotadas [fecha_inicio:fecha_fin] (son del mismo periodo)
def signalsMonthlyToDaily(diario_sp, senales_mensuales):

    # Al copiar el diario del sp, hacemos una copia del indice diario, por eso itero luego por las fechas del index para que las fechas de las señales diarias coincidan con las ruedas del diario del sp
    senales_diarias = diario_sp.copy()
    for date in senales_diarias.index:

        # Para cada fecha de cada rueda, busco la senal en su mes en senales_mensuales
        senales_diarias[date] = senales_mensuales[datetime(date.year, date.month, 1)]
    
    return senales_diarias