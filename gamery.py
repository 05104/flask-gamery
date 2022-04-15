from flask import Flask
import psycopg2

app = Flask(__name__)
app.config.from_pyfile('config.py')

connection = psycopg2.connect(
host=app.config['DB_HOST'],
database=app.config['DB_NAME'],
user=app.config['DB_USERNAME'],
password=app.config['DB_PASSWORD'])

game_dao = GameDao(connection)
user_dao = UserDao(connection)

@app.route('/')
def index():
    return render_template('list.html', title='Games', games=game_dao.list())

@app.route('/new')
def new():
    if 'user_login' not in session or session['user_login'] == None:
        return redirect(url_for('login', next=url_for('new')))
    return render_template('new.html', title='New game')

@app.route('/create', methods=['POST',])
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    image = request.files['image']
    game = game_dao.save(Game(name, category, console))
    image.save(app.config['UPLOAD_PATH'] + '/' + f'{game.id}.jpg')
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_login' not in session or session['user_login'] == None:
        return redirect(url_for('login', next=url_for('new')))
    
    game = game_dao.find_by_id(id)
    banner = f'{game.id}.jpg'
    
    if game:
        return render_template('edit.html', title=f'Editing {game.name}', game=game, banner=banner)
    else:
        flash(f'Not found')
        return redirect(url_for('index'))
    
@app.route('/delete/<int:id>')
def delete(id):
    if 'user_login' not in session or session['user_login'] == None:
        return redirect(url_for('login', next=url_for('new')))
    
    game = game_dao.find_by_id(id)
    if game:
        flash(f'Successfully deleted {game.name}')
        game_dao.delete(game.id)
        image_path = app.config['UPLOAD_PATH'] + '/' + f'{game.id}.jpg'
        if os.path.exists(image_path): os.remove(image_path) 
        return redirect(url_for('index'))
    else:
        flash(f'Not found')
        return redirect(url_for('index'))
        

@app.route('/update', methods=['POST',])
def update():
    name = request. form['name']
    category = request. form['category']
    console = request. form['console']
    id = request. form['id']
    image = request.files['image']
    game_dao.save(Game(name, category, console, id))
    if image:
        image.save(app.config['UPLOAD_PATH'] + '/' + f'{id}.jpg')
    return redirect(url_for('index'))

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

@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory('uploads', filename)

app.run(debug=True)
