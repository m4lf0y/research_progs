import subprocess
import sys
import sqlite3

# Main
if __name__=="__main__":

    running_procs=[]
    
    # connect to db
    dbname = '../db/./rssi.sqlite3'
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute('select * from sqlite_master WHERE type="table"')
    for row in cursor.fetchall():
        if row[1] != "alldata" and row[1] != "estimates":
            running_procs.append(subprocess.run(["python", "estimation.py",'['+row[1]+']'], stdout=subprocess.PIPE))

    print(running_procs)

    conn.close()
