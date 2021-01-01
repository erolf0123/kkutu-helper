import sqlite3
kuutu_db = sqlite3.connect("kkutu.db")
cur = kuutu_db.cursor()
def input_db():
    r = open('db_end.txt', mode='r')
    for line in r:
        check = 0
        a = line.strip()
        row = cur.execute("select * from test where word = '"+str(a)+"'")
        for i in row:
            check = 1
            break
        if check == 0:
            cur.execute("insert into test values('" +
                        str(a)+"','"+str(len(a))+"','0')")
            kuutu_db.commit()
    r.close()
    exit()

input_db()