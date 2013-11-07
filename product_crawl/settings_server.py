#SERVER Django settings for pospoll project.
#DOESN T MATTER WICH URL YOU USE - HEROKU AUTOMATICLY CHANGED
DB_POSTGRES_URL = 'postgres://postgresuser:p4stgr2s5s2r@localhost:5432/pospoll'

#FOR THE MOMENT WE USE THE SAME MONGODB FOR DEV AND PRODUCTION
MONGO_DB = {
    'NAME': 'heroku_app19278317',
    'USER': 'crawler',
    'PASSWORD': 'product_crawler',
    'HOST': 'ds053198.mongolab.com',
    'PORT': 53198,
}