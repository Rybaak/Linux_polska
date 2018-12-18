import psycopg2

import config

user = config.POSTGRESS_DATABASE_CONFIG['user']
password = config.POSTGRESS_DATABASE_CONFIG['password']
host = config.POSTGRESS_DATABASE_CONFIG['host']
dbname = config.POSTGRESS_DATABASE_CONFIG['dbname']

conn = psycopg2.connect('host='+host+' dbname='+dbname+' user='+user+' password='+password+'')

cur = conn.cursor()

with open('foo.csv', 'r') as f:
    cur.copy_from(f, 'EMPLOYEES_PART', sep=',', null='')

conn.commit()
