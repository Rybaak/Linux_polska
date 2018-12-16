import csv

import cx_Oracle
import numpy as np

con = cx_Oracle.connect('system/oracle@127.0.0.1:49161/xe')
cur = con.cursor()

#cur.prepare('select * from HR.employees where employee_id = :id')
#cur.execute(None, {'id': 100})

cur.execute('select * from HR.employees')
result_qery = np.asarray(cur.fetchall())

print (result_qery)

with open('foo.csv', "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(result_qery)