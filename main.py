import boto3
from flask import Flask, render_template, request, redirect, url_for, session

from utils.Utils import verify_user, user_exists, register_user, get_subscribed_music

app = Flask(__name__)
# secret_key to handle sessions.
app.secret_key = 'blacky123'



@app.route('/')
def root():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not verify_user(email, password):
            error = 'Email or password is invalid'
            return render_template('login.html', error=error)

        session['email'] = email
        session['username'] = email
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        if user_exists(email):
            error = 'Email already exists'
            return render_template('register.html', error=error)

        register_user(email, username, password)
        session['email'] = email
        session['username'] = username
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()  # clearing any sessions after logging out
    return redirect('/')


@app.route('/home')
def home():
    subscribed_music = get_subscribed_music(session['email'])
    return render_template('home.html', subscribed_music=subscribed_music)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)