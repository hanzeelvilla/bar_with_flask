from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysql_connector import MySQL
import mysql.connector
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SiNoPongoAgoLaAppSeCrasheaXD'

# ------------------- Conección con la base de datos mySQL ------------------- #
db = mysql.connector.connect( 
    host = "localhost",
    user = "root",
    password = "hanzeelSQL1234",
    database = "bar"
)

cursor = db.cursor(dictionary=True)

class Admins(UserMixin):
    def __init__(self, usuario, pswd):
        self.usuario = usuario
        self.pswd = pswd
    
    #Función necesaria para llamar la bd NO QUITAR
    def get_id(self):
        return str(self.usuario)

# ------------------------------ Habilitar login ----------------------------- #
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Función donde está el login

# ----------------------- Página cuando inician sesión ----------------------- #
@login_manager.user_loader
def load_user(user_id):
    return Admins(user_id, None)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        pswd = request.form['pswd']
        cursor.execute(f"SELECT * FROM admins WHERE usuario = '{user}' AND pswd = '{pswd}'")
        user_data = cursor.fetchone()
        if user_data:
            user = Admins(user_data['usuario'], user_data['pswd'])
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin():
    return render_template('admins.html')

if __name__ == '__main__':
    app.run()