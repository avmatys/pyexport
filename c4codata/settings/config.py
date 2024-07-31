import os

class Common:
    DEBUG = False


class Demo(Common):
    DEBUG = True
    C4C_URL = os.environ['C4C_URL']
    C4C_USER = os.environ['DEMO_C4C_USER']
    C4C_PWD = os.environ['DEMO_C4C_PWD']