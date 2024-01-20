import atexit
from flask import Flask, render_template, request
import mysql.connector
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
Bootstrap5(app)

# Configure MySQL connection
db_config = {
    'host': 'localhost',
    'port': 8889,
    'user': 'root',
    'password': 'root',
}

# Create MySQL Connection
mysql_connection = mysql.connector.connect(**db_config)
cursor = mysql_connection.cursor()

cursor.execute(f'CREATE DATABASE IF NOT EXISTS taskforge')
cursor.execute(f'USE taskforge')

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users 
    (
        UserID INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        FullName VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        Role VARCHAR(255) NOT NULL
    ) 
    ''')
mysql_connection.commit()


# except Exception as e:
#     print(f'Error: {e}')
# finally:
# Close cursor and connection


@app.route('/')
def login():
    return render_template('reglog.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user_data = {
            'email': request.form.get('email'),
            'name': request.form.get('name'),
            'username': request.form.get('username'),
            'role': request.form.get('role'),
            'password': request.form.get('password')
        }
        cursor.execute('''
            INSERT INTO users (Username, Password, FullName, Email, Role)
                VALUES (%(username)s, %(password)s, %(name)s, %(email)s, %(role)s)
        ''', new_user_data)
        mysql_connection.commit()
        return render_template('index.html', username=request.form.get('username'))
    return render_template('sign-up.html')


@app.route('/home')
def home():
    return render_template('index.html')


def close_db_connection():
    cursor.close()
    mysql_connection.close()

# Register the function to be called on exit
atexit.register(close_db_connection)

if __name__ == "__main__":
    app.run(debug=True)
