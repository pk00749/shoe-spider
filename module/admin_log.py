import logging, os

class Logger:
    def __init__(self, path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        # sh = logging.StreamHandler()
        # sh.setFormatter(fmt)
        # sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        # self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    logyyx = Logger('yyx.log', logging.ERROR, logging.DEBUG)
    logyyx.debug('一个debug信息')
    logyyx.info('一个info信息')
    logyyx.war('一个warning信息')
    logyyx.error('一个error信息')
    logyyx.cri('一个致命critical信息')

# import logging
# logger = logging.getLogger("simple_example")
# logger.setLevel(logging.DEBUG)
# # 建立一个filehandler来把日志记录在文件里，级别为debug以上
# fh = logging.FileHandler("spam.log")
# fh.setLevel(logging.DEBUG)
# # 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
# # ch = logging.StreamHandler()
# # ch.setLevel(logging.ERROR)
# # 设置日志格式
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# # ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# #将相应的handler添加在logger对象中
# # logger.addHandler(ch)
# logger.addHandler(fh)
# # 开始打日志
# logger.debug("debug message")
# logger.info("info message")
# logger.warn("warn message")
# logger.error("error message")
# logger.critical("critical message")

# import logging
#
# logger = logging.basicConfig(level=logging.WARNING,
#                     filename='../log/error.log',
#                     filemode='w',
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# # use logging
# logger.info('testing')
# logging.info('this is a loggging info message')
# logging.debug('this is a loggging debug message')
# logging.warning('this is loggging a warning message')
# logging.error('this is an loggging error message')
# logging.critical('this is a loggging critical message')

# import logging  # 引入logging模块
# import os.path
# import time
# # 第一步，创建一个logger
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)  # Log等级总开关
# # 第二步，创建一个handler，用于写入日志文件
# rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '/Logs/'
# log_name = log_path + rq + '.log'
# logfile = log_name
# fh = logging.FileHandler(logfile, mode='w')
# fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# # 第三步，定义handler的输出格式
# formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# fh.setFormatter(formatter)
# # 第四步，将logger添加到handler里面
# logger.addHandler(fh)
# # 日志
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')