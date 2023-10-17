from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config['MONGO_DBNAME'] = "LoginPage"
app.config['MONGO_URI'] = 'mongodb+srv://Krishna:Krishna_1234@cluster0.q06cohl.mongodb.net/LoginPage?retryWrites=true&w=majority'
mongo = PyMongo(app)


@app.route('/')
def home():
    if 'username' in session:
        return 'You are logged'
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])  # Corrected method
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], "password": hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('home'))  # Corrected redirect

    return render_template('signup.html')

@app.route('/login', methods=['POST'])  # Corrected method
def login():
    users = mongo.db.users
    login_user = users.find_one({"name": request.form['username']})

    if login_user and bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
        session['username'] = request.form['username']
        return redirect(url_for('home'))

    return 'Invalid username or password'

if __name__ == "__main__":
    app.run(debug=True, port=3000)
