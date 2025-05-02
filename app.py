from flask import Flask, render_template, request, redirect, url_for, send_file, session
import csv
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management

# Ensure the CSV file exists
if not os.path.exists('parking_data.csv'):
    with open('parking_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Full Name', 'Vehicle Type', 'Vehicle Number', 'Entry Direction', 'Exit Direction'])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('admin'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = [
        request.form['fullName'],
        request.form['vehicleType'],
        request.form['vehicleNumber'],
        request.form['entryDirection'],
        request.form['exitDirection']
    ]
    
    with open('parking_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        
    return render_template('admin.html')

@app.route('/dashboard')
@login_required
def dashboard():
    parking_data = []
    with open('parking_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        parking_data = list(reader)
    
    return render_template('dashboard.html', parking_data=parking_data)

@app.route('/download')
@login_required
def download():
    return send_file('parking_data.csv',
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='parking_data.csv')

if __name__ == '__main__':
    app.run(debug=True)