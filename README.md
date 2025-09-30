# EphemeralBin - Self-Destructing Notes App

A Flask web application that creates self-destructing notes with customizable expiration conditions.

## Features

- Create notes that automatically delete after a set number of views or time limit
- Generate unique, shareable URLs for each note
- Multiple expiration options (1/5/10 views or 10 minutes/1 hour/24 hours)
- Clean Bootstrap interface with copy-to-clipboard functionality
- SQLite database for persistent storage
- Responsive design that works on all devices

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Bootstrap 5, jQuery
- **Database**: SQLite
- **Styling**: Custom CSS with Bootstrap
- **Icons**: Font Awesome

## Project Structure

```
ephemeral-bin/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── notes.db              # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html         # Base template with Bootstrap
│   ├── index.html        # Homepage form
│   ├── success.html      # Note creation success page
│   ├── view_note.html    # Note viewing page
│   └── expired.html      # Expired note page
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── script.js     # jQuery frontend logic
```

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### 1. Create Project Directory
```bash
mkdir ephemeral-bin
cd ephemeral-bin
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Folder Structure
```bash
# Create directories
mkdir templates static
mkdir static/css static/js

# Place the files in their respective locations:
# - app.py in root directory
# - HTML templates in templates/ folder
# - style.css in static/css/
# - script.js in static/js/
```

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Create a Note**: Visit the homepage and enter your note content
2. **Set Expiration**: Choose between view-based (1, 5, 10 views) or time-based (10 minutes, 1 hour, 24 hours) expiration
3. **Get Shareable Link**: After creation, you'll receive a unique URL
4. **Share**: Copy and share the generated link
5. **Auto-Deletion**: The note will automatically delete based on your chosen conditions

## Deployment

### Local Development
The app runs on `http://localhost:5000` by default with debug mode enabled.

## Security Features

- Unique 12-character note IDs using Python's secrets module
- Automatic note deletion prevents data persistence
- No user accounts or personal data storage
- HTTPS recommended for production deployment

### Add Features
The modular structure makes it easy to add features like:
- Password-protected notes
- File attachments
- Note statistics
- API endpoints

## Troubleshooting

### Common Issues
1. **Database not found**: Make sure SQLite3 is installed and the app has write permissions
2. **Static files not loading**: Ensure the `static/` folder structure is correct
3. **Templates not found**: Verify the `templates/` folder contains all HTML files

### Debug Mode
Run with debug mode for development:
```bash
export FLASK_DEBUG=1
python app.py
```

## License

This project is for educational purposes as part of a web development course.

## Acknowledgments

- Bootstrap for responsive UI components
- Font Awesome for icons
- Flask framework for backend simplicity
- jQuery for frontend interactions