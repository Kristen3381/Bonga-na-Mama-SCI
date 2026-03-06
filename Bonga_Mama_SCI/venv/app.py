from flask import Flask, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__)
# Generate a secret key for security
app.secret_key = os.urandom(24)

# A simple list to act as a temporary DB in the mean time
feedback_storage = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    message = request.form.get('feedback')
    if message:
        # We store only the message, no IP address or timestamps for true anonymity
        feedback_storage.append(message)
        flash("Your voice has been heard anonymously, Comrade!", "success")
    else:
        flash("Please enter a message before submitting.", "error")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)