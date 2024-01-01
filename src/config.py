class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    #DEBUG = True
    #MYSQL_HOST = 'localhost'
    #MYSQL_USER = 'root'
    #MYSQL_PASSWORD = 'Borjas199823@'
    #MYSQL_DB = 'portalestadistico'

    #conxion con heroku
    DEBUG = True
    MYSQL_HOST = 'us-cdbr-east-06.cleardb.net'
    MYSQL_USER = 'bde2a77fe3b3b0'
    MYSQL_PASSWORD = '9f05f1dc'
    MYSQL_DB = 'heroku_36969848344a6e3'



config = {
    'development': DevelopmentConfig
}
