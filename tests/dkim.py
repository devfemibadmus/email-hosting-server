import rsa
import base64
import mysql.connector
from django.settings import DB_PATH

dotenv_path = DB_PATH
load_dotenv(dotenv_path)

def generate_dkim_key(domain, selector):
    public_key, private_key = rsa.newkeys(1024)
    public_key_pem = public_key.save_pkcs1()
    dkim_key = f"v=DKIM1; k=rsa; p={base64.b64encode(public_key_pem).decode('utf-8')}"
    return dkim_key, private_key, public_key, domain, selector


def save_keys_in_mysql(private_key, public_key, domain, selector):
    try:
        db_connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO dkim_keys (domain, selector, private_key, public_key) VALUES (%s, %s, %s, %s)", 
                       (domain, selector, private_key.save_pkcs1().decode('utf-8'), public_key.save_pkcs1().decode('utf-8')))
        db_connection.commit()
        cursor.close()
        db_connection.close()
        print("Keys saved successfully in MySQL database.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def main():
    domain = "blackstackhub.com"
    selector = "mailblackstackhub"
    dkim_key, private_key, public_key, domain, selector = generate_dkim_key(domain, selector)
    save_keys_in_mysql(private_key, public_key, domain, selector)
    print("DKIM DNS TXT record:")
    print(dkim_key)

if __name__ == "__main__":
    main()
