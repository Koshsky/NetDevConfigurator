import psycopg2


conn = psycopg2.connect(
    host="localhost",
    database="netbase",
    user="postgres",
    password="postgres"
)

def import_man():
    cur = conn.cursor()
    cur.execute("SELECT name FROM manufacturer")
    return cur.fetchall()
    conn.close

def import_model():
    cur = conn.cursor()
    cur.execute("SELECT name FROM model")
    #cur.execute("SELECT name FROM model WHERE man_id = %s", (manuf?))
    return cur.fetchall()
    conn.close