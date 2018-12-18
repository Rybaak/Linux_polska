import csv

import cx_Oracle
import numpy as np

import config

user = config.ORACLE_DATABASE_CONFIG['user']
password = config.ORACLE_DATABASE_CONFIG['password']
host = config.ORACLE_DATABASE_CONFIG['host']
port = str(config.ORACLE_DATABASE_CONFIG['port'])
dbname = config.ORACLE_DATABASE_CONFIG['dbname']

con = cx_Oracle.connect(user + '/' + password + '@' + host + ':' + port + '/' + dbname)
cur = con.cursor()

cur.execute('select * from HR.employees')
result_qery = np.asarray(cur.fetchall())

print(result_qery)

with open('foo.csv', "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(result_qery)
