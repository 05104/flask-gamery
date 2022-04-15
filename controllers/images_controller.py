from flask import send_from_directory
from gamery import app

@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory('uploads', filename)