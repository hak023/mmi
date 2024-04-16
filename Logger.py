import logging
import logging.handlers
import sys
import datetime

cfg_path="/home/vfras/mmi/conf/info.cfg"

log_homedir=''
log_level=0

def funcGetLogger():
    try:
        with open(cfg_path,'r') as file:
            config=file.read()
            lines=config.split('\n')
            for line in lines:
                if line.startswith('log.homedir='):
                    log_homedir=line.split('=')[1]
                if line.startswith('log.level='):
                    log_level=line.split('=')[1]
            #print(f"log_homedir: '{log_homedir}'")
            #print(f"log_level: '{log_level}'")
    except FileNotFoundError:
        print(f"{file_path} not found...!!!")
    except Exception as e:
        print(f"Error Reading config file...!!!")

    logger=logging.getLogger(__name__)
    logger.setLevel(int(log_level))
    formatter=logging.Formatter(fmt='%(asctime)s %(filename)s-%(levelname)s >> %(message)s')

    file_handler = logging.FileHandler(log_homedir+'logfile_{:%Y%m%d}.log'.format(datetime.datetime.now()), encoding='utf-8')
    file_handler.setFormatter(formatter)

    timedfilehandler=logging.handlers.TimedRotatingFileHandler(filename=log_homedir+'/LogFile', when='midnight', interval=1, encoding='utf-8')
    timedfilehandler.setFormatter(formatter)
    timedfilehandler.suffix = "%Y%m%d"

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
    
    logger.addHandler(stream_handler)
    #logger.addHandler(file_handler)
    logger.addHandler(timedfilehandler)

    return logger;
