from log import Log

log = Log(Log.LEVEL_INF, name='canvas')

def write(msg):
  log.imp(msg)