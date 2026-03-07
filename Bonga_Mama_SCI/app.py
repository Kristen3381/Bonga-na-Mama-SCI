from flask import Flask, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

ADMIN_ACCESS_KEY = "MAMA_SCI_2026"

feedback_storage = {
    "ladies": [],
    "gents": [],
    "general": []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wistem')
def wistem():
    return render_template('wistem.html')

@app.route('/agricycle')
def agricycle():
    return render_template('agricycle.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    message = request.form.get('feedback')
    category = request.form.get('category', 'general')
    if message and message.strip():
        feedback_storage[category].append(message)
        flash(f"Success! Message secured in the {category.capitalize()} Lounge. ✨", "success")
    else:
        flash("The field is empty, Comrade.", "error")
    return redirect(url_for('index'))

@app.route('/admin-portal-sci-2026')
def admin_view():
    user_key = request.args.get('key')
    if user_key == ADMIN_ACCESS_KEY:
        # Calculate counts dynamically
        counts = {k: len(v) for k, v in feedback_storage.items()}
        return render_template('admin.html', storage=feedback_storage, counts=counts)
    else:
        flash("Access Denied: Invalid Security Key.", "error")
        return redirect(url_for('index'))

@app.route('/clear-inbox')
def clear_inbox():
    user_key = request.args.get('key')
    if user_key == ADMIN_ACCESS_KEY:
        for key in feedback_storage:
            feedback_storage[key] = []
        flash("System Purge Complete. All records cleared. 🧹", "success")
        return redirect(url_for('admin_view', key=ADMIN_ACCESS_KEY))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)