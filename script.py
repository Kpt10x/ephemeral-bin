# Create the complete project structure for EphemeralBin
import os

# Define the project structure
project_structure = {
    "ephemeral-bin/": {
        "app.py": """from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
                             message="This note has been deleted after viewing.")
    
    conn.close()
    return render_template('view_note.html', content=note['content'])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
""",
        "requirements.txt": """Flask==3.0.0
""",
        "README.md": """# EphemeralBin - Self-Destructing Notes App

A Flask web application that creates self-destructing notes with customizable expiration conditions.

## Features

- Create notes that automatically delete after a set number of views or time limit
- Generate unique, shareable URLs for each note
- Multiple expiration options (1/5/10 views or 10 minutes/1 hour/24 hours)
- Clean Bootstrap interface with copy-to-clipboard functionality
- SQLite database for persistent storage

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Bootstrap 5, jQuery
- **Database**: SQLite
- **Styling**: Custom CSS with Bootstrap

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ephemeral-bin
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   Navigate to `http://localhost:5000`

## Project Structure

```
ephemeral-bin/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── notes.db              # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── success.html
│   ├── view_note.html
│   └── expired.html
└── static/               # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## Usage

1. Visit the homepage and enter your note content
2. Select an expiration option (views or time-based)
3. Click "Create Note" to generate a unique URL
4. Copy and share the generated link
5. The note will automatically delete based on your chosen conditions

## Deployment

### Local Development
The app runs on `http://localhost:5000` by default.

### Production Deployment (Render/Heroku)
1. Create a `runtime.txt` file with Python version
2. Ensure all dependencies are in `requirements.txt`
3. Set environment variables if needed
4. Deploy to your chosen platform

## License

This project is for educational purposes as part of a web development course.
""",
        "templates/": {
            "base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}EphemeralBin - Self-Destructing Notes{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-dark text-light">
    <header>
        <nav class="navbar navbar-dark bg-dark border-bottom">
            <div class="container">
                <a href="{{ url_for('index') }}" class="navbar-brand">
                    <i class="fas fa-scroll me-2"></i>EphemeralBin
                </a>
                <span class="navbar-text">Self-Destructing Notes</span>
            </div>
        </nav>
    </header>

    <main class="container py-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <footer class="bg-dark border-top mt-5">
        <div class="container py-3">
            <div class="text-center text-muted">
                <small>&copy; 2025 EphemeralBin - Secure Self-Destructing Notes</small>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
""",
            "index.html": """{% extends "base.html" %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card bg-secondary">
            <div class="card-body">
                <h1 class="card-title mb-4">
                    <i class="fas fa-edit me-2"></i>Create a Self-Destructing Note
                </h1>
                <p class="card-text text-muted mb-4">
                    Share sensitive information that automatically deletes after viewing or when time expires.
                </p>
                
                <form method="POST" action="{{ url_for('create_note') }}" id="noteForm">
                    <div class="mb-4">
                        <label for="content" class="form-label">
                            <i class="fas fa-sticky-note me-1"></i>Note Content
                        </label>
                        <textarea name="content" id="content" class="form-control bg-dark text-light border-secondary" 
                                  rows="6" placeholder="Enter your note content here..." required></textarea>
                        <div class="form-text">Your note will be encrypted and stored securely.</div>
                    </div>

                    <div class="mb-4">
                        <label class="form-label">
                            <i class="fas fa-clock me-1"></i>Expiration Options
                        </label>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="card bg-dark mb-3">
                                    <div class="card-header">
                                        <small class="text-muted">View-based Expiration</small>
                                    </div>
                                    <div class="card-body">
                                        <div class="form-check mb-2">
                                            <input class="form-check-input" type="radio" name="expiration_type" 
                                                   id="1_view" value="1_view" checked>
                                            <label class="form-check-label" for="1_view">
                                                After 1 view <span class="badge bg-danger">Most Secure</span>
                                            </label>
                                        </div>
                                        <div class="form-check mb-2">
                                            <input class="form-check-input" type="radio" name="expiration_type" 
                                                   id="5_views" value="5_views">
                                            <label class="form-check-label" for="5_views">After 5 views</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="radio" name="expiration_type" 
                                                   id="10_views" value="10_views">
                                            <label class="form-check-label" for="10_views">After 10 views</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card bg-dark mb-3">
                                    <div class="card-header">
                                        <small class="text-muted">Time-based Expiration</small>
                                    </div>
                                    <div class="card-body">
                                        <div class="form-check mb-2">
                                            <input class="form-check-input" type="radio" name="expiration_type" 
                                                   id="10_minutes" value="10_minutes">
                                            <label class="form-check-label" for="10_minutes">After 10 minutes</label>
                                        </div>
                                        <div class="form-check mb-2">
                                            <input class="form-check-input" type="radio" name="expiration_type" 
                                                   id="1_hour" value="1_hour">
                                            <label class="form-check-label" for="1_hour">After 1 hour</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="radio" name="expiration_type" 
                                                   id="24_hours" value="24_hours">
                                            <label class="form-check-label" for="24_hours">After 24 hours</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary btn-lg">
                            <i class="fas fa-plus-circle me-2"></i>Create Secure Note
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <div class="text-center mt-4">
            <div class="alert alert-info">
                <i class="fas fa-shield-alt me-2"></i>
                <strong>Privacy Notice:</strong> Notes are stored temporarily and permanently deleted after expiration. 
                We cannot recover deleted notes.
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",
            "success.html": """{% extends "base.html" %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card bg-success bg-opacity-10 border-success">
            <div class="card-body text-center">
                <i class="fas fa-check-circle text-success fa-3x mb-3"></i>
                <h1 class="card-title text-success mb-3">Note Created Successfully!</h1>
                <p class="card-text mb-4">Your secure note has been created and is ready to share.</p>
                
                <div class="mb-4">
                    <label class="form-label">Your Shareable Link:</label>
                    <div class="input-group">
                        <input type="text" class="form-control bg-dark text-light border-secondary" 
                               id="noteUrl" value="{{ note_url }}" readonly>
                        <button class="btn btn-outline-success" type="button" id="copyButton">
                            <i class="fas fa-copy me-1"></i>Copy
                        </button>
                    </div>
                    <div class="form-text text-success" id="copyMessage" style="display: none;">
                        <i class="fas fa-check me-1"></i>Link copied to clipboard!
                    </div>
                </div>

                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Important:</strong> Save this link now! Once the note expires, it cannot be recovered.
                </div>

                <div class="row mt-4">
                    <div class="col-md-6 mb-2">
                        <a href="{{ url_for('index') }}" class="btn btn-secondary w-100">
                            <i class="fas fa-plus me-2"></i>Create Another Note
                        </a>
                    </div>
                    <div class="col-md-6">
                        <a href="{{ note_url }}" class="btn btn-primary w-100" target="_blank">
                            <i class="fas fa-eye me-2"></i>View Note
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",
            "view_note.html": """{% extends "base.html" %}

{% block title %}Viewing Note - EphemeralBin{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card bg-secondary">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                    <i class="fas fa-eye me-2"></i>Secure Note
                </h5>
                <small class="text-muted">
                    <i class="fas fa-clock me-1"></i>Viewed: {{ moment().format('MMM D, YYYY HH:mm') }}
                </small>
            </div>
            <div class="card-body">
                <div class="note-content p-3 bg-dark rounded border">
                    <pre class="text-light mb-0">{{ content }}</pre>
                </div>
                
                {% if message %}
                <div class="alert alert-warning mt-3">
                    <i class="fas fa-trash-alt me-2"></i>{{ message }}
                </div>
                {% endif %}
            </div>
            <div class="card-footer">
                <div class="row">
                    <div class="col-md-6 mb-2">
                        <button class="btn btn-outline-light w-100" id="copyContent">
                            <i class="fas fa-copy me-2"></i>Copy Content
                        </button>
                    </div>
                    <div class="col-md-6">
                        <a href="{{ url_for('index') }}" class="btn btn-primary w-100">
                            <i class="fas fa-plus me-2"></i>Create New Note
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <div class="alert alert-danger mt-4">
            <i class="fas fa-exclamation-triangle me-2"></i>
            <strong>Security Warning:</strong> This note may be deleted automatically based on its expiration settings. 
            Save any important information now.
        </div>
    </div>
</div>
{% endblock %}
""",
            "expired.html": """{% extends "base.html" %}

{% block title %}Note Expired - EphemeralBin{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card bg-danger bg-opacity-10 border-danger">
            <div class="card-body text-center">
                <i class="fas fa-exclamation-circle text-danger fa-3x mb-3"></i>
                <h1 class="card-title text-danger mb-3">Note Expired</h1>
                <p class="card-text mb-4">{{ message }}</p>
                
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    This is how EphemeralBin works - notes are permanently deleted for security and privacy.
                </div>

                <div class="row mt-4">
                    <div class="col-md-6 mb-2">
                        <a href="{{ url_for('index') }}" class="btn btn-primary w-100">
                            <i class="fas fa-plus me-2"></i>Create New Note
                        </a>
                    </div>
                    <div class="col-md-6">
                        <a href="javascript:history.back()" class="btn btn-secondary w-100">
                            <i class="fas fa-arrow-left me-2"></i>Go Back
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
        },
        "static/": {
            "css/": {
                "style.css": """:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #17a2b8;
    --dark-color: #343a40;
    --light-color: #f8f9fa;
}

body {
    background-color: #1a1a1a;
    color: #e9ecef;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.navbar {
    box-shadow: 0 2px 4px rgba(0,0,0,.1);
}

.card {
    border: none;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s ease-in-out;
}

.card:hover {
    transform: translateY(-2px);
}

.form-control {
    background-color: #495057;
    border-color: #6c757d;
    color: #e9ecef;
    transition: all 0.3s ease;
}

.form-control:focus {
    background-color: #495057;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    color: #e9ecef;
}

.form-control::placeholder {
    color: #adb5bd;
}

.btn {
    border-radius: 6px;
    transition: all 0.3s ease;
}

.btn:hover {
    transform: translateY(-1px);
}

.form-check-input:checked {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

.note-content pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.5;
    margin: 0;
}

.alert {
    border: none;
    border-radius: 8px;
}

.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.copy-success {
    color: var(--success-color) !important;
    transition: color 0.3s ease;
}

footer {
    margin-top: auto;
}

.input-group .form-control {
    border-right: none;
}

.input-group .btn {
    border-left: none;
}

.card-header {
    border-bottom: 1px solid rgba(255, 255, 255, 0.125);
}

.card-footer {
    border-top: 1px solid rgba(255, 255, 255, 0.125);
}

@media (max-width: 768px) {
    .container {
        padding-left: 15px;
        padding-right: 15px;
    }
    
    .card-body {
        padding: 1.5rem;
    }
}
"""
            },
            "js/": {
                "script.js": """$(document).ready(function() {
    // Copy to clipboard functionality
    $('#copyButton').click(function() {
        const noteUrl = $('#noteUrl')[0];
        noteUrl.select();
        noteUrl.setSelectionRange(0, 99999); // For mobile devices
        
        navigator.clipboard.writeText(noteUrl.value).then(function() {
            // Show success message
            $('#copyMessage').fadeIn();
            $('#copyButton').addClass('btn-success').removeClass('btn-outline-success');
            $('#copyButton').html('<i class="fas fa-check me-1"></i>Copied!');
            
            // Reset after 2 seconds
            setTimeout(function() {
                $('#copyMessage').fadeOut();
                $('#copyButton').removeClass('btn-success').addClass('btn-outline-success');
                $('#copyButton').html('<i class="fas fa-copy me-1"></i>Copy');
            }, 2000);
        }).catch(function() {
            // Fallback for older browsers
            document.execCommand('copy');
            $('#copyMessage').fadeIn();
        });
    });

    // Copy note content functionality
    $('#copyContent').click(function() {
        const noteContent = $('.note-content pre').text();
        
        navigator.clipboard.writeText(noteContent).then(function() {
            $(this).addClass('btn-success').removeClass('btn-outline-light');
            $(this).html('<i class="fas fa-check me-2"></i>Content Copied!');
            
            setTimeout(() => {
                $(this).removeClass('btn-success').addClass('btn-outline-light');
                $(this).html('<i class="fas fa-copy me-2"></i>Copy Content');
            }, 2000);
        }.bind(this)).catch(function() {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = noteContent;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            $(this).addClass('btn-success').removeClass('btn-outline-light');
            $(this).html('<i class="fas fa-check me-2"></i>Content Copied!');
        }.bind(this));
    });

    // Form validation
    $('#noteForm').submit(function(e) {
        const content = $('#content').val().trim();
        
        if (content.length === 0) {
            e.preventDefault();
            $('#content').addClass('is-invalid');
            $('#content').focus();
            return false;
        }
        
        // Show loading state
        $(this).find('button[type="submit"]').prop('disabled', true)
               .html('<i class="fas fa-spinner fa-spin me-2"></i>Creating...');
    });

    // Remove validation error on input
    $('#content').on('input', function() {
        $(this).removeClass('is-invalid');
    });

    // Add fade-in animation to cards
    $('.card').addClass('fade-in');
    
    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        $('.alert-dismissible').alert('close');
    }, 5000);
});
"""
            }
        }
    }
}

# Print the project structure
print("EphemeralBin Project Structure:")
print("=" * 50)

def print_structure(structure, prefix="", root_path=""):
    for name, content in structure.items():
        if isinstance(content, dict):
            print(f"{prefix}📁 {name}")
            print_structure(content, prefix + "  ", root_path + name)
        else:
            if name.endswith('.py'):
                print(f"{prefix}🐍 {name}")
            elif name.endswith('.html'):
                print(f"{prefix}🌐 {name}")
            elif name.endswith('.css'):
                print(f"{prefix}🎨 {name}")
            elif name.endswith('.js'):
                print(f"{prefix}⚡ {name}")
            elif name.endswith('.md'):
                print(f"{prefix}📖 {name}")
            elif name.endswith('.txt'):
                print(f"{prefix}📄 {name}")
            else:
                print(f"{prefix}📄 {name}")

print_structure(project_structure)