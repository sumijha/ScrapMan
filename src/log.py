import logging
from time import gmtime, strftime
import os, sys, inspect
dir_path =os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
filename = strftime("%d-%m-%Y_%S%M%H", gmtime())
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=dir_path+"\\logs\\Logs_" + filename + ".log", level=logging.DEBUG)

class logger():
    def __init__(self):
        print('using of logger')

    def debug(self, message):
        logging.debug(message)

    def info(self, message):
        logging.info(message)

    def error(self, message):
        logging.error(message)
