from flask import Flask, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__)
# Secure secret key for session encryption
app.secret_key = os.urandom(24)

# Data structure to separate feedback categories
feedback_storage = {
    "ladies": [],
    "gents": [],
    "general": []
}

@app.route('/')
def index():
    return render_template('index.html')

# --- NEW ROUTES PLACED BEFORE THE RUN COMMAND ---
@app.route('/wistem')
def wistem():
    return render_template('wistem.html')

@app.route('/agricycle')
def agricycle():
    return render_template('agricycle.html')
# ----------------------------------------------

@app.route('/submit', methods=['POST'])
def submit_feedback():
    message = request.form.get('feedback')
    category = request.form.get('category', 'general')
    
    if message and message.strip():
        # Store message in the specific lounge
        feedback_storage[category].append(message)
        flash(f"Success! Your voice is safe in the {category.capitalize()} Lounge. 🕊️", "success")
    else:
        flash("The message field is empty, Comrade. Please share your thoughts.", "error")
    
    return redirect(url_for('index'))

@app.route('/admin-portal-sci-2026')
def admin_view():
    return render_template('admin.html', storage=feedback_storage)

if __name__ == '__main__':
    # The run command MUST be the very last thing in the file
    app.run(debug=True, port=5000)