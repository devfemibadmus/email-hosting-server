from django.conf import settings
import mysql.connector
import os

def load_env_vars(env_file_path):
    with open(env_file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

load_env_vars('secrete/db.env')

def get_domain_id(domain):
    try:
        db_connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM virtual_domains WHERE name = %s", (domain,))
        id = cursor.fetchone()[0]
        cursor.close()
        db_connection.close()
        return id
    except mysql.connector.Error as err:
        print("Error:", err)
        return None

print(get_domain_id('blackstackhub.com'))