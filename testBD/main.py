from flask import Flask, render_template
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
    'database': 'mysql'
}

# Create MySQL Connection
mysql_connection = mysql.connector.connect(**db_config)
cursor = mysql_connection.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        UserID INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        FullName VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        Role VARCHAR(255) NOT NULL
    ) 
''')

mysql_connection.commit()
cursor.close()
mysql_connection.close()


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)