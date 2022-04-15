from flask import render_template, request, redirect, session, flash, url_for
from dao import UserDao
from gamery import connection, app

user_dao = UserDao(connection)

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)


@app.route('/sessions', methods=['POST', ])
def sessions():
    user = user_dao.find_by_name(request.form['username'])
    
    if user and user.password == request.form['password']:
        session['user_login'] = user.id
        flash(f'Welcome {user.name}')
        return redirect(request.form['next'] or url_for('index'))
    else:
        flash('Error')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['user_login'] = None
    flash('User not logged!')
    return redirect(url_for('index'))