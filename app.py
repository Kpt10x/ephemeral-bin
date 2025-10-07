from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import sqlite3
import secrets
import string

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Database initialization
def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            max_views INTEGER,
            current_views INTEGER DEFAULT 0,
            expires_at DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Generate unique note ID
def generate_note_id(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Check if note is expired
def is_note_expired(note):
    if note['expires_at'] and datetime.fromisoformat(note['expires_at']) <= datetime.now():
        return True
    if note['max_views'] and note['current_views'] >= note['max_views']:
        return True
    return False

# Delete expired note
def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_note():
    content = request.form.get('content', '').strip()
    expiration_type = request.form.get('expiration_type')
    
    if not content:
        flash('Please enter some content for your note.', 'error')
        return redirect(url_for('index'))
    
    note_id = generate_note_id()
    max_views = None
    expires_at = None
    
    # Parse expiration settings
    if expiration_type == '1_view':
        max_views = 1
    elif expiration_type == '5_views':
        max_views = 5
    elif expiration_type == '10_views':
        max_views = 10
    elif expiration_type == '10_minutes':
        expires_at = datetime.now() + timedelta(minutes=10)
    elif expiration_type == '1_hour':
        expires_at = datetime.now() + timedelta(hours=1)
    elif expiration_type == '24_hours':
        expires_at = datetime.now() + timedelta(hours=24)
    
    # Save to database
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO notes (id, content, max_views, expires_at)
        VALUES (?, ?, ?, ?)
    ''', (note_id, content, max_views, expires_at.isoformat() if expires_at else None))
    conn.commit()
    conn.close()
    
    return redirect(url_for('success', note_id=note_id))

@app.route('/success/<note_id>')
def success(note_id):
    note_url = request.url_root + 'note/' + note_id
    return render_template('success.html', note_url=note_url, note_id=note_id)

@app.route('/note/<note_id>')
def view_note(note_id):
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    note = cursor.fetchone()
    
    if not note:
        conn.close()
        return render_template('expired.html', message="This note does not exist or has already been deleted.")
    
    # Convert to dict for easier handling
    note = dict(note)
    
    # Check if expired
    if is_note_expired(note):
        delete_note(note_id)
        conn.close()
        return render_template('expired.html', message="This note has expired and been deleted.")
    
    # Increment view count
    new_view_count = note['current_views'] + 1
    cursor.execute('UPDATE notes SET current_views = ? WHERE id = ?', (new_view_count, note_id))
    conn.commit()
    
    # Check if this view causes expiration
    note['current_views'] = new_view_count
    if is_note_expired(note):
        delete_note(note_id)
        conn.close()
        return render_template('view_note.html', content=note['content'], 
                             message="This note has been deleted after viewing.",
                             accessed_time=datetime.now().strftime('%b %d, %Y %H:%M'))
    
    conn.close()
    return render_template('view_note.html', content=note['content'],
                         accessed_time=datetime.now().strftime('%b %d, %Y %H:%M'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
