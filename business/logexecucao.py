import time

import config as cfg


class LogExecucao:
    def __init__(self, totalExecucoes):
        self.totalExecucoes = totalExecucoes
        self.execucaoAtual = 0

    def LogPrint(self, text, logType):
        datetime = time.strftime("%d/%m/%Y %H:%M:%S")
        if(self.totalExecucoes > 0):
            percentRun = round((self.execucaoAtual/self.totalExecucoes)*100,2)
        else:
            percentRun = 0
        outMsg = "{0} -> [{1} -- {3}%]: {2}".format(logType, datetime, text, percentRun)
        print(outMsg)
        #self.SaveLog(outMsg)
        
    def SaveLog(self, text):
        with open(cfg.configPaths['CFG_LOG_FOLDER'] + 'log.txt', mode="a" , encoding="utf-8") as myfile:
            myfile.write(text + " \n")
