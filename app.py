from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import csv
from datetime import datetime
import webbrowser
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management

# Hardcoded credentials
users = {
    'admin': 'admin123',
    'user': 'user123'
}

meeting_status = {'active': False}
current_tabs = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            if username == 'admin':
                return redirect(url_for('admin_page'))
            else:
                return redirect(url_for('user_page'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/start_meeting', methods=['POST'])
def start_meeting():
    meeting_status['active'] = True
    webbrowser.open_new('https://meet.google.com/fvz-zssy-euh')
    return {'status': 'Meeting Started and Google Meet link opened'}


@app.route('/stop_meeting', methods=['POST'])
def stop_meeting():
    meeting_status['active'] = False
    return {'status': 'Meeting Stopped'}


@app.route('/is_meeting_active', methods=['GET'])
def is_meeting_active():
    return {'active': meeting_status['active']}


@app.route('/update_tabs', methods=['POST'])
def update_tabs():
    if not meeting_status['active']:
        print("Ignoring tabs update. Meeting not active.")
        return {'status': 'Meeting not active'}, 403

    try:
        data = request.json
        print(f"Received tabs: {data['tabs']}")

        os.makedirs('logs', exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open('logs/meeting_tabs.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for tab in data['tabs']:
                title = tab.get('title', 'No title')
                url = tab.get('url', 'No URL')
                writer.writerow([timestamp, title, url])

        return {'status': 'Tabs updated'}

    except Exception as e:
        print(f"Error in /update_tabs: {e}")
        return {'status': 'Error'}, 500


CSV_FILE = 'logs/meeting_tabs.csv'


@app.route('/get_tabs_data')
def get_tabs_data():
    tabs = []
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['timestamp'] and row['title'] and row['url']:
                tabs.append(row)
    return jsonify(tabs)


@app.route('/admin_tabs', methods=['GET'])
def admin_tabs():
    return jsonify({'tabs': current_tabs})


@app.route('/user')
def user_page():
    if 'username' not in session or session['username'] != 'user':
        return redirect(url_for('login'))
    return render_template('user.html')


@app.route('/admin')
def admin_page():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html')


if __name__ == "__main__":
    app.run(port=5000)
