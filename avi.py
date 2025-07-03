from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session, flash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for sessions

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy user credentials (for demo)
USER_CREDENTIALS = {
    'admin': 'password123'
}

# -------------------------------
# Routes
# -------------------------------

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in USER_CREDENTIALS and USER_CREDENTIALS[uname] == pwd:
            session['username'] = uname
            return redirect('/')
        else:
            flash('Invalid credentials')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'username' not in session:
        return redirect('/login')
    file = request.files['file']
    if file.filename == '':
        flash("No file selected")
        return redirect('/')
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return f"File uploaded! <a href='/files/{file.filename}'>View {file.filename}</a>"

@app.route('/files/<filename>')
def serve_file(filename):
    if 'username' not in session:
        return redirect('/login')
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found"), 404

# -------------------------------
# Main entry point
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
