#default config
class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = '\x8d\x18r\xa2\xcd\x95p h\xd6\x803\xa4\x14sf\xc2$\x8c\xef\xb1AII'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///User.db'
