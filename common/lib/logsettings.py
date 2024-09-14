import sys
import platform
from logging.handlers import SysLogHandler

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

def get_logger_config(log_dir, logging_env="no_env", local_loglevel='INFO', service_variant=""):
    hostname = platform.node().split(".")[0]
    syslog_format = ("[service_variant={service_variant}]"
                    "[%(name)s][env:{logging_env}] %(levelname)s "
                    "[{hostname}  %(process)d] [user %(userid)s] [ip %(remoteip)s] [%(filename)s:%(lineno)d] "
                    "- %(message)s").format(service_variant=service_variant,
                                            logging_env=logging_env,
                                            hostname=hostname)
    
    logger_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)s %(process)d'
                          '[%(name)s] [user %(userid)s] [ip %(remoteip)s] %(filename)s:%(lineno)d - %(message)s',
            },
            'syslog_format': {'format': syslog_format},
            'raw': {'format': '%(message)s'},
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'userid_context': {
                '()': 'common.mdm_django_utils.logging.UserIdFilter',
            },
            'remoteip_context': {
                '()': 'common.mdm_django_utils.logging.RemoteIpFilter',
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'filters': ['userid_context', 'remoteip_context'],
                'stream': sys.stderr,
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'local': {
                'level': local_loglevel,
                'class': 'logging.handlers.SysLogHandler',
                'address': '/dev/log',
                'formatter': 'syslog_format',
                'filters': ['userid_context', 'remoteip_context'],
                'facility': SysLogHandler.LOG_LOCAL0,
            },
            'tracking': {
                'level': 'DEBUG',
                'class': 'logging.handlers.SysLogHandler',
                'address': '/dev/log',
                'facility': SysLogHandler.LOG_LOCAL1,
                'formatter': 'raw',
            },
            # 'logfile': {  # define and name a handler
            #     'level': 'INFO',
            #     'class': 'logging.FileHandler',  # set the logging class to log to a file
            #     'formatter': 'standard',  # define the formatter to associate
            #     'filename': log_dir  # log file
            # },
        },
        'loggers': {
            'tracking': {
                'handlers': ['tracking'],
                'level': 'DEBUG',
                'propagate': False,
            },
            '': {
                # 'handlers': ['console', 'local', 'logfile'],
                'handlers': ['console', 'local'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True
            },
            'request.packages.urllib3': {
                'level': 'WARN'
            }
        }
    }

    return logger_config