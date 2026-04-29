import mysql.connector

cnx = mysql.connector.connect(user='flickz', password='animanlevel7',
                              host='127.0.0.1', database='library_db')

with cnx.cursor() as cursor: 
    res = cursor.execute("SELECT * from Book limit 5")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

cnx.close()
