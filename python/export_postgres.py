import psycopg2
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=gpadmin")

cur = conn.cursor()

with open('foo.csv', 'r') as f:
    cur.copy_from(f, 'EMPLOYEES_PART', sep=',', null='')

conn.commit()