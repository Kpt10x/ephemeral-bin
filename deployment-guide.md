# EphemeralBin Deployment Guide

## 🚀 Complete Deployment Instructions

### Step 1: Project Setup
1. **Download all project files** (from the provided files above):
   - app.py
   - requirements.txt  
   - README.md
   - base.html, index.html, success.html, view-note.html, expired.html
   - style.css
   - script.js

2. **Create the folder structure**:
```bash
ephemeral-bin/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── success.html
│   ├── view_note.html    # Note: rename view-note.html to view_note.html
│   └── expired.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

### Step 2: Local Development Setup

#### Option A: Command Line Setup
```bash
# Create project directory
mkdir ephemeral-bin
cd ephemeral-bin

# Create subdirectories
mkdir templates static
mkdir static/css static/js

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Flask
pip install Flask==3.0.0

# Create the Python files
# Copy app.py content into app.py
# Copy requirements.txt content into requirements.txt

# Create templates
# Copy each HTML file content into templates/ directory
# Copy style.css into static/css/
# Copy script.js into static/js/

# Run the application
python app.py
```

#### Option B: IDE Setup (VS Code/PyCharm)
1. Create new folder `ephemeral-bin`
2. Open in your IDE
3. Create the folder structure as shown above
4. Copy file contents into respective files
5. Set up Python interpreter with virtual environment
6. Install Flask: `pip install Flask==3.0.0`
7. Run app.py

### Step 3: Testing Locally
1. **Start the application**: `python app.py`
2. **Open browser**: Navigate to `http://localhost:5000`
3. **Test functionality**:
   - Create a note with different expiration settings
   - Copy the generated URL
   - Open in new tab/browser to verify viewing
   - Test that notes expire correctly

### Step 4: Production Deployment Options

#### 🔥 Option 1: Render (Recommended - Free Tier Available)

**Prerequisites**: GitHub account

**Steps**:
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: EphemeralBin Flask app"
   git branch -M main
   git remote add origin https://github.com/USERNAME/ephemeral-bin.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [render.com](https://render.com)
   - Connect your GitHub account
   - Select "New Web Service"
   - Connect your repository
   - Configure:
     - **Name**: ephemeral-bin
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
     - **Instance Type**: Free
   - Click "Create Web Service"

3. **Environment Variables** (if needed):
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-random-secret-key`

#### 🌊 Option 2: Heroku

**Prerequisites**: Heroku CLI installed

**Steps**:
1. **Prepare for Heroku**:
   ```bash
   # Add gunicorn to requirements
   echo "gunicorn==21.2.0" >> requirements.txt
   
   # Create Procfile
   echo "web: gunicorn app:app" > Procfile
   
   # Create runtime.txt (optional)
   echo "python-3.11.0" > runtime.txt
   ```

2. **Deploy**:
   ```bash
   heroku login
   heroku create your-app-name
   git add .
   git commit -m "Prepare for Heroku deployment"
   git push heroku main
   heroku open
   ```

#### 🚄 Option 3: Railway

**Steps**:
1. Push code to GitHub (same as Render steps)
2. Go to [railway.app](https://railway.app)
3. Connect GitHub account
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway auto-detects Flask and deploys

#### 🐍 Option 4: PythonAnywhere (Good for beginners)

**Steps**:
1. Sign up for [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload files via Files tab
3. Open Bash console and set up virtual environment:
   ```bash
   cd ~
   python -m venv myenv
   source myenv/bin/activate
   pip install flask
   ```
4. In Web tab, create new web app:
   - Python version: 3.10
   - Manual configuration
   - Set WSGI file path to your app location

#### ☁️ Option 5: AWS/Google Cloud/Azure
For advanced users - requires knowledge of cloud platforms and may incur costs.

### Step 5: Domain and SSL (Optional)

#### Custom Domain Setup:
1. **Purchase domain** from registrar (Namecheap, GoDaddy, etc.)
2. **Update DNS records**:
   - Point A record to your deployment platform's IP
   - Or use CNAME for subdomain
3. **Configure in platform**:
   - Render: Add custom domain in dashboard
   - Heroku: `heroku domains:add yourdomain.com`

#### SSL Certificate:
Most platforms (Render, Heroku) provide automatic SSL. Just use `https://` URLs.

### Step 6: Environment Variables for Production

**Set these in your deployment platform**:
```bash
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DATABASE_URL=sqlite:///notes.db  # or your database URL
```

### Step 7: Monitoring and Maintenance

#### Health Checks:
- Set up monitoring (platform-specific)
- Monitor database size (SQLite can grow)
- Check application logs regularly

#### Database Maintenance:
```python
# Add to app.py for automatic cleanup
import os
from datetime import datetime, timedelta

def cleanup_expired_notes():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    
    # Delete expired notes
    cursor.execute('''
        DELETE FROM notes 
        WHERE (expires_at IS NOT NULL AND expires_at <= ?) 
        OR (max_views IS NOT NULL AND current_views >= max_views)
    ''', (datetime.now().isoformat(),))
    
    conn.commit()
    conn.close()

# Run periodically (add to a background job if needed)
```

### Step 8: Git Workflow for Updates

```bash
# Make changes to your code
git add .
git commit -m "Add new feature or fix"
git push origin main

# Automatic deployment will trigger on most platforms
```

### 🛠️ Troubleshooting Common Issues

#### **Port Issues**:
```python
# Modify app.py for production
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

#### **Static Files Not Loading**:
- Ensure correct folder structure
- Check static file URLs in templates
- Verify deployment includes all static files

#### **Database Issues**:
- SQLite file permissions
- Database creation in production environment
- Consider upgrading to PostgreSQL for production

#### **Environment Variables**:
- Double-check all required environment variables are set
- Use platform-specific methods to set them
- Test locally with environment variables first

### 🎯 Final Checklist

- [ ] All files in correct folder structure
- [ ] Virtual environment created and activated
- [ ] Flask installed and app runs locally
- [ ] Git repository created and pushed to GitHub
- [ ] Deployment platform configured
- [ ] Application accessible via public URL
- [ ] All features tested in production
- [ ] Environment variables set for production
- [ ] SSL certificate active (https)
- [ ] Custom domain configured (optional)

### 📞 Support Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Render Support**: https://render.com/docs
- **Heroku Documentation**: https://devcenter.heroku.com/
- **Bootstrap Documentation**: https://getbootstrap.com/docs/

Your EphemeralBin application should now be fully deployed and accessible to users worldwide! 🌍