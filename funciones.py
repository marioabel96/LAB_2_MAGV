# -- ------------------------------------------------------------------------------------ -- #

# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance

# -- archivo: datos.py - datos generales para uso en el proyecto

# -- mantiene: marioabel96

# -- repositorio: https://github.com/marioabel96/LAB_2_MAGV/



import datetime
import pandas as pd
import numpy as np
from datetime import  datetime
from datetime import timedelta
import collections

# -- ------------------------------------------------------------------------------------ -- #
# -- --------------------------------------------------- FUNCION: Leer archivo de entrada -- #
# -- ------------------------------------------------------------------------------------ -- #
# --

def f_leer_archivo(param_archivo):
     # Leer archivo de datos y guardarlo en un DataFrame
    df_data = pd.read_excel('Data/' + param_archivo, sheet_name='Hoja1')
    df_data = df_data.loc[df_data['Type']!='balance']
    
    # elegir solo renglones en los que la columna type == buy | type == sell

    # Convertir en minusculas el nombre de las columnas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]
    # Asegurar que ciertas son del tipo numerico
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap',
              'taxes', 'order']

    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)
    df_data.index = range(len(df_data))

    #print(df_data)
    return df_data

# -- --------------------------------------------------- FUNCION: columnas tiempos -- #
# -- ------------------------------------------------------------------------------------ -- #
# --

def f_columnas_tiempos(data):
    #conversion a tiempo de columnas apertura y cierre en un datframe nuevo donde comezaremos a registrar los datos nuevos
    data['opentime'] = pd.to_datetime(data['opentime'])
    data['closetime'] = pd.to_datetime(data['closetime'])
    
    #duracion de la operacion
    data['dif_time'] = (data['closetime'] - data['opentime'])
    #conversion a segundos
    data['dif_seconds'] = data['dif_time'].dt.total_seconds()
    return data

    




def limpiar_2(param_ins):  
    symbol = list(newd['symbol'])
    symbol= [symbol[i].replace("-2","") for i in range(len(symbol))]
    newd['symbol']= pd.DataFrame(symbol)
    newd
    return newd



# -- ------------------------------------------------------ FUNCION: Pips por instrumento -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- calcular el tamaño de los pips por instrumento

def f_pip_size(param_ins):
    """
           Parameters
       ----------
       param_ins : str : nombre de instrumento
       Returns
       -------
       Debugging
       -------
       param_ins = 'usdjpy'
       """

    # encontrar y eliminar un guion bajo
    # inst = param_ins.replace('_', '')

    # transformar a minusculas
    inst = param_ins.lower()

    # lista de pips por instrumento
    pips_inst = {'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                 'chfjpy': 100,
                 'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 'usdmxn': 10000,
                 'audusd': 10000, 'nzdusd': 10000,
                 'usdchf': 10000,
                 'eurgbp': 10000, 'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000,
                 'gbpnzd': 10000, 'gbpchf': 10000, 'gbpaud': 10000,
                 'audnzd': 10000, 'nzdcad': 10000, 'audcad': 10000,
                 'xauusd': 10, 'xagusd': 10, 'btcusd': 10, 'wticousd':10,'natgasusd':10}

    return pips_inst[inst]


# -- --------------------------------------------------- FUNCION: columnas pips -- #
# -- ------------------------------------------------------------------------------------ -- #
# --

def f_columnas_pips(newd):

    # obtenemos los pips de todos los inttrumentos uilizados y anexamos al dataframe
    pips = [f_pip_size(param_ins = newd['symbol'][i]) for i in range(len(newd))]
    newd['pips'] =pips
    
        #calculamos las diferencias entre entrada y salida de la operacion y multiplicamos por su valor equivalente
    #deltasprice = [n for n in range(len(newd)) if n%2 == 0]
    piptotales = []
    conta = 0
    for i in range(0,len(newd)):
        if newd['type'][i] == 'buy':
            piptotales.append((newd['closeprice'][i] - newd['openprice'][i])*pips[i])
        else:
            piptotales.append((newd['openprice'][i] - newd['closeprice'][i])*pips[i])
        conta = conta + 1
    newd['piptotales'] = piptotales
    newd['profit_t'] = newd['profit'].cumsum() 
    return newd


# -- --------------------------------------------------- FUNCION: columnas pips -- #
# -- ------------------------------------------------------------------------------------ -- #
# --




def f_estadisticas_ba1(newd):
    return pd.DataFrame({
        'Ops totales': [len(newd['order']), 'Operaciones totales'],
        'Ganadoras': [len(newd[newd['piptotales']>=0]), 'Operaciones ganadoras'],
        'Ganadoras_c': [len(newd[(newd['type']=='buy') & (newd['piptotales']>=0)]), 'Operaciones ganadoras de compra'],
        'Ganadoras_v': [len(newd[(newd['type']=='sell') & (newd['piptotales']>=0)]), 'Operaciones ganadoras de venta'],
        'Perdedoras': [len(newd[newd['piptotales'] < 0]), 'Operaciones perdedoras'],
        'Perdedoras_c': [len(newd[(newd['type']=='buy') & (newd['piptotales']<0)]), 'Operaciones perdedoras de compra'],
        'Perdedoras_v': [len(newd[(newd['type']=='sell') & (newd['piptotales']<0)]), 'Operaciones perdedoras de venta'],
        'Media (Profit)': [newd['profit'].median(), 'Mediana de profit de operaciones '],
        'Media (Pips)': [newd['pips'].median(), 'Mediana de pips de operaciones'],
        'r_efectividad': [len(newd[newd['profit'] >= 0])/len(newd['order']), 'Ganadoras Totales/Operaciones Totales'],
        'r_proporcion': [len(newd[newd['profit'] >= 0]) / len(newd[newd['profit'] < 0]), 'Ganadoras Totales/Perdedoras Totales'],
        'r_efectividad_c': [len(newd[(newd['type'] == 'buy') & (newd['profit'] >= 0)]) / len(newd['order']), 'Ganadoras Compras/Operaciones Totales'],
        'r_efectividad_v': [len(newd[(newd['type'] == 'sell') & (newd['profit'] >= 0)]) / len(newd['order']), 'Ganadoras Ventas/ Operaciones Totales'],
      
    })
    estadisticas = f_estadisticas_ba1(newd).T
    estadisticas.index.name = 'medida'
    estadisticas.columns = ['valor', 'descripcion']  
    estadisticas
    return estadisticas


# -- --------------------------------------------------- FUNCION: columnas pips -- #
# -- ------------------------------------------------------------------------------------ -- #
# --


def f_estadisticas_ba2(newd):
        #tabla de ranking
    #contamos el total de operaciones por instrumento
    
    counter=collections.Counter(newd['symbol'])
    counter= pd.DataFrame(counter, index=[0]).T
    # separamos las positivas
    rankingp = newd[['symbol','profit']]
    rankingp = rankingp.loc[rankingp['profit'] > 0]
    
    # contamos positivas por instrumento
    
    ncounter=collections.Counter(rankingp['symbol'])
    rankingt = pd.DataFrame(ncounter, index=[0]).T
    
    # generamos y mostramos la tabloa de rankings
    
    ranking = rankingt/counter
    ranking = ranking.sort_values(by=[0], ascending=False)
    ranking = (ranking*100).round(2).astype(str) + '%'
    ranking.columns = ['rank']
    return ranking
    
# -- --------------------------------------------------- FUNCION: columnas pips -- #
# -- ------------------------------------------------------------------------------------ -- #
# --



def f_profit_diario(newd):
        # obtenemos solo la columna profits y closetime
    profits = newd[['closetime','profit']]
    # quitamos la hora y solo dejamos la fecha
    profits.columns = ['timestamp', 'profit_d']
    profits['timestamp'] = profits['timestamp'].dt.date
    
    # cum sum por fecha
    profits = pd.DataFrame(profits.groupby(['timestamp'])['profit_d'].agg('sum'))
    #calculamos y agregamos profits_acm_d
    profits['profits_acm_d'] = 5000+profits['profit_d'].cumsum()
    return profits


# -- --------------------------------------------------- FUNCION: columnas pips -- #
# -- ------------------------------------------------------------------------------------ -- #
# --

def f_estadisticas_mad(profits,newd):
    #Sharpe Ratio 
    rp= (np.log(profits['profits_acm_d']/(profits['profits_acm_d'].shift(1)).iloc[1:]))
    rf= .08/300
    sharpe=(rp.mean()-rf)/rp.std()



    #Sortino
    mar=.3/300

    #compra

    compra = newd.loc[newd['type'] == 'buy']
    # obtenemos solo la columna profits y closetime
    profitsc = compra[['closetime','profit']]
    # quitamos la hora y solo dejamos la fecha
    profitsc.columns = ['timestamp', 'profit_d']
    profitsc['timestamp'] = profitsc['timestamp'].dt.date
    # cum sum por fecha
    profitsc = pd.DataFrame(profitsc.groupby(['timestamp'])['profit_d'].agg('sum'))
    #calculamos y agregamos profits_acm_d
    profitsc['profits_acm_d'] = 5000+profitsc['profit_d'].cumsum()
    rp_c= (np.log(profitsc['profits_acm_d']/(profitsc['profits_acm_d'].shift(1)).iloc[1:]))

    sortino_c=(rp_c.mean()-rf)/rp_c[rp_c<mar].std()

    #Venta

    venta = newd.loc[newd['type'] == 'sell']
    # obtenemos solo la columna profits y closetime
    profitsv = venta[['closetime','profit']]
    # quitamos la hora y solo dejamos la fecha
    profitsv.columns = ['timestamp', 'profit_d']
    profitsv['timestamp'] = profitsv['timestamp'].dt.date
    # cum sum por fecha
    profitsv = pd.DataFrame(profitsv.groupby(['timestamp'])['profit_d'].agg('sum'))
    #calculamos y agregamos profits_acm_d
    profitsv['profits_acm_d'] = 5000+profitsv['profit_d'].cumsum()
    rp_v= (np.log(profitsv['profits_acm_d']/(profitsv['profits_acm_d'].shift(1)).iloc[1:]))

    sortino_v=(rp_v.mean()-rf)/rp_v[rp_v<mar].std()


    #Drawdown / DrawUp
    dd= profits.cummin().min()
    du =profits.cummax().max()
    
    return pd.DataFrame({
         'sharpe': [sharpe, 'Sharpe Ratio'],
        'sortino_c': [sortino_c,'Sortino Ratio para Posiciones  de Compra'],
        'sortino_v': [sortino_v,'Sortino Ratio para Posiciones de Venta'],
        'Drawdown': [dd, 'DrawDown de Capital'],
        'DrawUp': [du, 'DrawUp de Capital'],
      
    },index=['valor', 'Descripcion'])
