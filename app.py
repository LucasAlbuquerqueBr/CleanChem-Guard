import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from database import db

app = Flask(__name__)
app.secret_key = 'supersecretkey_cleanchainguard'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = db.get_user_by_email(email)
    
    if user and user['password'] == password:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect(url_for('profile'))
    
    flash('Invalid credentials', 'error')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        
        if password != confirm:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))
            
        if db.get_user_by_email(email):
            flash('Email already exists', 'error')
            return redirect(url_for('signup'))
            
        db.create_user(email, username, password)
        flash('Account created! Please login.', 'success')
        return redirect(url_for('index'))
        
    return render_template('signup.html')

@app.route('/gallery')
def gallery():
    posts = db.get_all_posts()
    # Enrich posts with username if needed, for now just raw
    return render_template('gallery.html', posts=posts)

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    messages = db.get_messages()
    return render_template('chat.html', messages=messages)

@app.route('/ai')
def ai():
    return render_template('ai.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_posts = db.get_user_posts(session['user_id'])
    return render_template('profile.html', posts=user_posts, username=session['username'])

@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('profile'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('profile'))
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        description = request.form.get('description', '')
        tags = request.form.get('tags', '').split(',')
        
        db.create_post(session['user_id'], filename, description, tags)
        flash('Post created!', 'success')
        
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
