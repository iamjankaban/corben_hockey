class Config(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'wfjei8fyh8weyfv78w7nRBb5FN57EDBEDbd'

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True