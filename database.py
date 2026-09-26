import psycopg2
connection=psycopg2.connect(dbname="nasa_explorer",user="nasa_user",password="nasa_password",host="localhost",port="5432")
print("Database connected!")

cursor=connection.cursor()
cursor.execute("Select * from asteroids")
rows=cursor.fetchall()
for row in rows:
    print(row)
connection.close()