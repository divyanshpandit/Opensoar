from flask import Flask, render_template
from app import create_app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    print("Looking for templates in:", app.template_folder)  # Debug print
    app.run(debug=True)
