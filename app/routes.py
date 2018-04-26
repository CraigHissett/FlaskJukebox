from flask import render_template, flash, redirect, url_for
from app import app, db, vlcplayer
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from flask_login import login_required
from app.models import User
from flask import request
from werkzeug.urls import url_parse
from flask_login import logout_user
from datetime import datetime
import threading


Player=vlcplayer.MusicPlayer('/home/pi/Downloads')
Player.GetLibrary()

def background():
    Player.Routine1()

def foreground():
    main_loop.start()

b = threading.Thread(name='background', target=background)
f = threading.Thread(name='foreground', target=foreground)
b.start()
#f.start()

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Craig'}
    posts = [
        {
            'author': {'username': 'Jill'},
            'body': 'Beautiful day in Hetton!'
        },
        {
            'author': {'username': 'Isaac'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/jukebox', methods=['GET', 'POST'])
def jukebox():
    if request.method == 'POST':
        print('Post town')
        WebCommand = request.form ['command']
        WebValue = request.form ['value']
        
        if WebCommand == 'Pi':
            if WebValue == 'Shutdown':
                if sys.platform == 'win32':
                    os.system('shutdown /s')
                else:
                    os.system('shutdown -h now')
            elif WebValue == 'Reboot':
                if sys.platform == 'win32':
                    os.system('shutdown /r')
                else:
                    os.system('shutdown -r now')
            else:
                print('No matching Pi Command')
                return
        elif WebCommand == 'Arduino':
            if WebValue == 'Reset':
                slave = Aquarium(0)
                slave.ResetSlave()
            else:
                print('No matching Arduino Command')
                return
        elif WebCommand == 'Request':
            Player.AddRequest(Player.LibraryLocation + '\\' + WebValue)
        else:
            print('Command not recognised')

    items=Player.CompiledLibrary
    requests=Player.RequestLibrary
    DisplayItems=[]
    DisplayRequests=[]
    for i in items:
        DisplayItems.append(i.replace(Player.LibraryLocation + '\\',''))
    for i in requests:
        DisplayRequests.append(i.replace(Player.LibraryLocation + '\\',''))
    return render_template('jukebox.html', title='Flask JukeBox!', items=DisplayItems, requests=DisplayRequests)
