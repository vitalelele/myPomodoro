from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import timedelta

app = Flask(__name__)

# Default settings
default_settings = {
    "pomodoro_duration": 25,
    "break_duration": 5,
    "cycles": 3,
    "theme": "dark"
}

# Initialize global variables
settings = default_settings.copy()
work_sessions_completed = 0
total_work_time = 0
total_break_time = 0

def load_settings():
    global settings
    config_file = "settings.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            settings = json.load(file)
    else:
        save_settings()

def save_settings():
    with open("settings.json", "w") as file:
        json.dump(settings, file)

@app.route('/')
def index():
    return render_template('index.html', settings=settings)

@app.route('/start_timer', methods=['POST'])
def start_timer():
    global work_sessions_completed, total_work_time, total_break_time
    return jsonify({"message": "Timer started!", "settings": settings})

@app.route('/update_settings', methods=['POST'])
def update_settings():
    global settings
    settings["pomodoro_duration"] = int(request.form['pomodoro_duration'])
    settings["break_duration"] = int(request.form['break_duration'])
    settings["cycles"] = int(request.form['cycles'])
    settings["theme"] = request.form['theme']
    save_settings()
    return jsonify({"message": "Settings updated!", "settings": settings})

@app.route('/report')
def report():
    global work_sessions_completed, total_work_time, total_break_time
    total_work_time_formatted = str(timedelta(seconds=total_work_time))
    total_break_time_formatted = str(timedelta(seconds=total_break_time))
    return jsonify({
        "sessions_completed": work_sessions_completed,
        "total_work_time": total_work_time_formatted,
        "total_break_time": total_break_time_formatted
    })

@app.route('/reset_report', methods=['POST'])
def reset_report():
    global work_sessions_completed, total_work_time, total_break_time
    work_sessions_completed = 0
    total_work_time = 0
    total_break_time = 0
    return jsonify({"message": "Report reset!"})

if __name__ == "__main__":
    load_settings()
    app.run(debug=True)
