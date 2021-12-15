from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras

app = Flask(__name__)

app.config['SECRET_KEY'] = 'api-login-tests'

DB_HOST = "localhost"
DB_NAME = "users"
DB_USER = "postgres"
DB_PASS = "root"

conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)


@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return jsonify({'message': 'You are already logged in', 'username': username})
    else:
        resp = jsonify({'message': 'Unauthorized'})
        resp.status_code = 401
        return resp


@app.route('/login', methods=['POST'])
def login():
    _json = request.json
    _username = _json['username']
    _password = _json['password']
    print(session)
    # validate the received values
    if _username and _password:
        # check user exists
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "SELECT * FROM users WHERE username=%s and password=%s"
        bind_params = (_username, _password)
        cursor.execute(query, bind_params)

        row = cursor.fetchone()
        username = row['username']
        if row:
            session['username'] = username
            cursor.close()
            return jsonify({'message': 'You are logged in successfully'})
    else:
        resp = jsonify({'message': 'Bad Request - invalid credendtials'})
        resp.status_code = 400
        return resp


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message': 'You successfully logged out'})


if __name__ == "__main__":
    app.run()
