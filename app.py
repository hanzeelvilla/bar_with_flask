from flask import Flask
from flask_mysql_connector import MySQL 

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'hanzeelSQL1234'
app.config['MYSQL_DB'] = 'bar'

mysql = MySQL(app)

@app.route('/')
def home():
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute(f"USE {app.config['MYSQL_DB']}")
    cursor.execute('SELECT * FROM bebidas')
    result = cursor.fetchall()
    cursor.close()
    return result

if __name__ == '__main__':
    app.run()
