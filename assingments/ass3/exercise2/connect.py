import psycopg2

conn = psycopg2.connect( 
    user = 'postgres',
    password = 'postgres-cloud-app-dev',
    database = 'sample_db',
    host = '34.140.249.176',
    port = 5432
)

cursor = conn.cursor()
cursor.execute('SELECT * FROM users')

rows = cursor.fetchall()

for row in rows:
    print(row)
    
cursor.close()
conn.close()