from logging import basicConfig, getLogger

basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
log = getLogger()
log.setLevel(3)
