import logging

def GetLogger(name, level=logging.DEBUG):
  logger = logging.getLogger(name)
  logger.setLevel(level)

  # create file handler which logs even debug messages
  fh = logging.FileHandler('/home/yuweilin/log/'+name+'.log')
  fh.setLevel(level)
  # create console handler with a higher log level
  ch = logging.StreamHandler()
  ch.setLevel(logging.ERROR)
  # create formatter and add it to the handlers
  formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
  ch.setFormatter(formatter)
  fh.setFormatter(formatter)
  # add the handlers to logger
  logger.addHandler(ch)
  logger.addHandler(fh)

  return logger
