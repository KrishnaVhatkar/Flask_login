from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt





app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 
app.config['MONGO_URI'] = 'mongodb+srv://Krishna2:Krish_1323@cluster0.q06cohl.mongodb.net/MyDatabase?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/home')
def home():
    if 'username' in session:
         username = session['username']
         return render_template('index.html',username=username)
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            session['username'] = request.form['username']
            users.insert_one({'name': request.form['username'], 'password': hashed_password})
            return redirect(url_for('home'))
        else:
            flash('Username already exists. Please choose another.', 'error')

    return render_template('signup.html')

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name': request.form['username']})

        if login_user and bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' in session:
        if request.method == 'POST':
            users = mongo.db.users
            new_username = request.form['new_username']
            new_password = request.form['new_password']
           
            if users.find_one({'name': new_username}) is None:
                users.update_one({'name': session['username']}, {'$set': {'name': new_username, 'password': bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())}})
                session['username'] = new_username
                flash('Profile updated successfully', 'success')
            else:
                flash('Username already exists. Please choose another.', 'error')
            return redirect(url_for('home'))
        return render_template('edit_profile.html')
    return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) 
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)








