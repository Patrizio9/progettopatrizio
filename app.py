from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Chiave segreta per gestire la sessione

# Configurazione del database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'port': 3306,
    'password': 'Patriziogotti2003',
    'database': 'hofamedb'
}

# Creazione della tabella degli utenti all'avvio (se non esiste già)
try:
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
except Error as e:
    print(f"Error: {e}")

# Route per la homepage
@app.route('/')
def index():
    username = session.get('username')  # Recupera il nome utente dalla sessione se presente
    return render_template('index.html', username=username)

# Route per la pagina di registrazione
@app.route('/registra.html')
def registra():
    return render_template('registra.html')

# Route per la pagina di login
@app.route('/login.html')
def login():
    return render_template('login.html', error=None)  # Passiamo error=None inizialmente per non mostrare un errore

# Route per gestire il login degli utenti
@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()

            if user:
                # Se l'utente è trovato nel database, impostiamo la sessione
                session['username'] = user['username']
                session['user_id'] = user['id']
                return redirect(url_for('index'))  # Reindirizza alla homepage dopo il login

            cursor.close()
            conn.close()

    except Error as e:
        print(f"Error: {e}")

    # Se il login fallisce, mostriamo un messaggio di errore nella stessa pagina di login
    error = "Login non avvenuto con successo. Controlla le credenziali e riprova."
    return render_template('login.html', error=error)

# Route per gestire la registrazione degli utenti
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            cursor.close()
            conn.close()

    except Error as e:
        print(f"Error: {e}")

    return redirect(url_for('index'))

# Route per gestire il logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


