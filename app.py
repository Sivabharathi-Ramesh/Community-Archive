import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'simple_archive_secret_key'

DATABASE = 'archive.db'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists physically on your computer
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            edition TEXT,
            keywords TEXT,
            file_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    search_query = request.args.get('search', '').strip()
    conn = get_db_connection()
    
    if search_query:
        # Search across titles, authors, or keywords
        books = conn.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? OR keywords LIKE ?
        ''', (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')).fetchall()
    else:
        books = conn.execute('SELECT * FROM books').fetchall()
        
    conn.close()
    return render_template('index.html', books=books, search_query=search_query)

@app.route('/upload', methods=['POST'])
def upload_book():
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    edition = request.form.get('edition', '').strip()
    keywords = request.form.get('keywords', '').strip()
    
    # Validation Check: Title is completely essential
    if not title or not author:
        flash('Book Title and Author are strictly required!', 'danger')
        return redirect(url_for('index'))
        
    if 'book_file' not in request.files:
        flash('No file part found.', 'danger')
        return redirect(url_for('index'))
        
    file = request.files['book_file']
    
    if file.filename == '':
        flash('No file selected for upload.', 'danger')
        return redirect(url_for('index'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        relative_path = os.path.join('uploads', filename)
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the physical PDF file to static/uploads/
        file.save(full_path)
        
        # Save the metadata information to SQLite
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO books (title, author, edition, keywords, file_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, author, edition, keywords, relative_path))
        conn.commit()
        conn.close()
        
        flash(f'Success! "{title}" has been added to the archive.', 'success')
    else:
        flash('Invalid file extension. Only PDF documents are permitted.', 'danger')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)