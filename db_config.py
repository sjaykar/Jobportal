import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="ip address",
        user="username",
        password="password",
        database="database_name",
        auth_plugin='mysql_native_password'
    )

