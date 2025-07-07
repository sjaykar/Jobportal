import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="192.168.1.10",
        user="shashi1",
        password="shashi",
        database="jobportal",
        auth_plugin='mysql_native_password'
    )

