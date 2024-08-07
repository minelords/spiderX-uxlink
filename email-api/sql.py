import libsql_experimental as libsql
import os
import random
import time
import string
import re

def email_code(email):
    FLAG=1
    url = os.getenv('TURSO_DATABASE_URL')
    auth_token = os.getenv('TURSO_AUTH_TOKEN')

    conn = libsql.connect("emails.db", sync_url=url, auth_token=auth_token)
    while FLAG==1:
        conn.commit()
        conn.sync()
        time.sleep(1)
        details=conn.execute("SELECT message_to,subject,text FROM emails ORDER BY created_at DESC").fetchall()
        for detail in details:
            if detail[0]==email:
                FLAG=0
                title=detail[1]
                text=detail[2].replace("\n"," ")
                return title,text

def generate_mail():
    return "".join(random.choices(string.ascii_lowercase, k=random.randint(3,9)))
    

if __name__=="__main__":
    print(email_code("wtf@xxxx.top"))
    print(generate_mail())

