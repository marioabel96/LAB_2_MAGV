# -- ------------------------------------------------------------------------------------ -- #

# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance

# -- archivo: datos.py - datos generales para uso en el proyecto

# -- mantiene: marioabel96

# -- repositorio: https://github.com/marioabel96/LAB_2_MAGV/

# -- ------------------------------------------------------------------------------------ -- #

# importamos el archivo funciones
import funciones as fn
import pandas as pd
data = fn.f_leer_archivo(param_archivo="archivo_tradeview_1.xlsx")

data = fn.f_columnas_tiempos(data)
# creacion nuevo dataframe donde estaremos haciendo las modificaciones
newd = pd.DataFrame(data)




# obtenemos los pips de todos los inttrumentos uilizados y anexamos al dataframe
pips = [fn.f_pip_size(param_ins = newd['symbol'][i]) for i in range(len(newd))]
newd['pips'] =pips


newd = fn.f_columnas_pips(newd)

estadisticas = fn.f_estadisticas_ba1(newd)

ranking = fn.f_estadisticas_ba2(newd)

profits =fn.f_profit_diario(newd)

medap = fn.f_estadisticas_mad(profits,newd).T