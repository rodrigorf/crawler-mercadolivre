"""
Módulo para forçar a geração do excel com base no csv dos dados coletados
"""
import time

import config as cfg
from business import util
from business.logexecucao import LogExecucao

logOut = LogExecucao(0)
todayDate = time.strftime("%d/%m/%Y")
todayDate = todayDate.replace('/', '.')
fullPath = cfg.configPaths['CFG_CSV_FOLDER'] + "output_" + todayDate + ".csv"
if util.TransformCsvToExcel(fullPath):
    logOut.LogPrint('Arquivo XLSX criado.')
else:
    logOut.LogPrint(
        'Nenhum arquivo xlsx foi gerado. Verifique o log.')
