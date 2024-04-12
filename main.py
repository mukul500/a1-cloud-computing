import boto3
from flask import Flask, render_template, request, redirect, url_for, session

from utils.S3SignedUrl import get_music_with_signed_url
from utils.Utils import verify_user, user_exists, register_user, get_subscribed_music, query_music, \
    add_subscribed_music, remove_subscribed_music

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

    return render_template('Login.html')


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

    return render_template('Register.html')


@app.route('/logout')
def logout():
    session.clear()  # clearing any sessions after logging out
    return redirect('/')


@app.route('/home')
def home():
    subscribed_music = get_subscribed_music(session['email'])
    subscribed_music_with_image = get_music_with_signed_url(subscribed_music)
    return render_template('Home.html', subscribed_music=subscribed_music_with_image)


@app.route('/search', methods=['POST'])
def search():
    print(request.method)
    if request.method == 'POST':
        title = request.form.get('title')
        artist = request.form.get('artist')
        year = request.form.get('year')
        print(request.form)
        print(f"Title: {title}, Artist: {artist}, Year: {year}")
        music_list = query_music(title, artist, year)
        music_list_with_image = get_music_with_signed_url(music_list)
        print("--------------------")
        return render_template('Home.html', query_music=music_list_with_image[:1])

    return redirect(url_for('home'))


@app.route('/subscribe', methods=['POST'])
def subscribe():
    title = request.form.get('title')
    email = session['email']
    add_subscribed_music(email, title)
    return redirect(url_for('home'))


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    title = request.form.get('title')
    email = session['email']
    remove_subscribed_music(email, title)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)