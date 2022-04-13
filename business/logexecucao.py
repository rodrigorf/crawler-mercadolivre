import logging


class LogExecucao:
    def __init__(self, totalExecucoes):
        logging.basicConfig(level=logging.DEBUG)
        logging.basicConfig(filename="log/logs.log", filemode="w", format="%(name)s -> %(levelname)s: %(message)s")

    def LogPrint(self, text, logType='INFO'):
        if(logType == 'INFO'):
            logging.info(text)
        elif(logType == 'ERRO'):
            logging.error(text)

