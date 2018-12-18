import datetime
import time

import cx_Oracle
import numpy as np
import pandas as pd
import psycopg2

v_count = 0
v_table = 'EMPLOYEES_PART'
v_table_15_min = 'EMPLOYEES_LAST_15_MIN'
my_list = []

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print(st)

con_pstgress = psycopg2.connect("host=localhost dbname=postgres user=postgres password=gpadmin")
cur_pstgress = con_pstgress.cursor()

con_oracle = cx_Oracle.connect('system/oracle@127.0.0.1:49161/xe')
cur_oracle = con_oracle.cursor()

cur_oracle.execute('select * from HR.employees')

result_qery = np.asarray(cur_oracle.fetchall())
print("")
print("result_qery.shape: " + str(result_qery.shape))
print("result_qery.ndim: " + str(result_qery.ndim))
print("result_qery.size: " + str(result_qery.size))
print("")

print('')
dataset = pd.DataFrame({
    'EMPLOYEE_ID': result_qery[:, 0],
    'FIRST_NAME': result_qery[:, 1],
    'LAST_NAME': result_qery[:, 2],
    'EMAIL': result_qery[:, 3],
    'PHONE_NUMBER': result_qery[:, 4],
    'HIRE_DATE': result_qery[:, 5],
    'JOB_ID': result_qery[:, 6],
    'SALARY': result_qery[:, 7],
    'COMMISSION_PCT': result_qery[:, 8],
    'MANAGER_ID': result_qery[:, 9],
    'DEPARTMENT_ID': result_qery[:, 10],
})
dataset.index = result_qery[:, 0]
print("dataset.loc['3']: \n" + str(dataset.loc[100]))
print('')

print('')
for row in result_qery:
    a = str(str(row[5])[0:4].replace('-', ''))
    my_list.append(a)

my_list = list(set(my_list))

cur_pstgress.execute(
    """select relname from pg_inherits i join pg_class c on c.oid = inhrelid 
    where inhparent = 'EMPLOYEES_PART' ::regclass""")
a = np.asarray(cur_pstgress.fetchall())

for i in my_list:
    if 'employees_part_' + i not in a.astype(str):
        cur_pstgress.execute(
            f"CREATE TABLE EMPLOYEES_PART_{i} PARTITION OF EMPLOYEES_"
            f"PART FOR VALUES FROM ('{i}-01-01') TO ('{i}-12-31');",
            i)
        print(f'Dodano partycję za: {i}')
print('')

cur_pstgress.execute('INSERT INTO ' + v_table + ' select * from ' + v_table_15_min + ';')
cur_pstgress.execute('TRUNCATE TABLE ' + v_table_15_min + ';')

for row in result_qery:
    cur_pstgress.execute(
        "INSERT INTO " + v_table_15_min + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row
    )
    v_count += 1
con_pstgress.commit()

ts2 = time.time()
st2 = datetime.datetime.fromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')
print(st2)
print("Załadowano " + str(v_count) + " rekordów do tabeli: " + v_table)
