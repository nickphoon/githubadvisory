import csv
import sqlite3

def convert(database,file,type):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("select * from "+type+";")
    with open(file, 'w',newline='' ,encoding="utf-8") as csv_file: 
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description]) 
        csv_writer.writerows(cursor)
    conn.close()

convert("inthewild.db","exploits.csv","exploits")

# convert("inthewild.db","vulnerabilities.csv","vulns")


