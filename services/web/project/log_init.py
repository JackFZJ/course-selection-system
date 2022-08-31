# --*--coding: utf-8 --*--
import os
import logging.config
logfile_dir = os.path.dirname(os.path.abspath(__file__))  # log文件的目录
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": os.path.join(logfile_dir,"logfiles", "info.log"),
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": os.path.join(logfile_dir,"logfiles","errors.log"),
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8",
            },
            "debug_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": os.path.join(logfile_dir,"logfiles","debug.log"),
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "my_module": {"level": "ERROR", "handlers": ["console"], "propagate": "no"}
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["error_file_handler", "debug_file_handler"],
        },
    }
)

# import logging.config
#
# # 定义三种日志输出格式 开始
#
# standard_format = '[%(asctime) -s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
#
# '[%(levelname)s][%(message)s]'
#
# simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
#
# id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'
#
# # 定义日志输出格式 结束
#
# logfile_dir = os.path.dirname(os.path.abspath(__file__))  # log文件的目录
#
# logfile_name = 'all2.log'  # log文件名
#
# # 如果不存在定义的日志目录就创建一个
#
# if not os.path.isdir(logfile_dir):
#
#     os.mkdir(logfile_dir)
#
# # log文件的全路径
#
# logfile_path = os.path.join(logfile_dir, logfile_name)
#
# # log配置字典
#
# LOGGING_DIC = {
#
# 'version': 1,
#
# 'disable_existing_loggers': False,
#
# 'formatters': {
#
# 'standard': {
#
# 'format': standard_format,
#
# 'datefmt': '%Y-%m-%d %H:%M:%S',
#
# },
#
# 'simple': {
#
# 'format': simple_format
#
# },
#
# },
#
# 'filters': {},
#
# 'handlers': {
#
# 'console': {
#
# 'level': 'DEBUG',
#
# 'class': 'logging.StreamHandler',  # 打印到屏幕
#
# 'formatter': 'simple'
#
# },
#
# 'default': {
#
# 'level': 'DEBUG',
#
# 'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件。自动切日志
#
# 'filename': logfile_path,  # 日志文件
#
# 'maxBytes': 1024*1024*5,  # 日志大小5M
#
# 'backupCount': 5,  # 日志文件备份个数
#
# 'formatter': 'standard',  # 使用的日志文件格式
#
# 'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
#
# },
#
# },
#
# 'loggers': {
#
# '': {
#
# 'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
#
# 'level': 'DEBUG',
#
# 'propagate': True,  # 向上(更高level的logger)传递
#
# },
#
# },
#
# }
#
# logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的配置
# print(logfile_path)