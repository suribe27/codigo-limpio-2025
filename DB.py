import psycopg2

PGHOST='ep-snowy-lab-a4mk1kuj-pooler.us-east-1.aws.neon.tech'
PGDATABASE='liquidador_nomina'
PGUSER='neondb_owner'
PGPASSWORD='npg_Tg1KxQSat3Yl'

psycopg2.connect(host=PGHOST, database=PGDATABASE, user=PGUSER, password=PGPASSWORD)