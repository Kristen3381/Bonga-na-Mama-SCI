from flask import Flask, render_template, request, flash, redirect, url_for, Response
import os

app = Flask(__name__)
# Generates a fresh secret key for session security every time the server restarts
app.secret_key = os.urandom(24)

# The "Master Key" - Use this in your URL to access admin features
# Example: http://127.0.0.1:5000/admin-portal-sci-2026?key=MAMA_SCI_2026
ADMIN_ACCESS_KEY = "MAMA_SCI_2026"

# In-memory storage (Resets when server restarts - perfect for anonymity)
feedback_storage = {
    "ladies": [],
    "gents": [],
    "general": []
}

# --- PUBLIC ROUTES ---

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
        flash("The field is empty, Comrade. Please share your thoughts.", "error")
    
    return redirect(url_for('index'))

# --- ADMIN & SECURITY ROUTES ---

@app.route('/admin-portal-sci-2026')
def admin_view():
    # Security: Look for ?key=MAMA_SCI_2026 in the URL
    user_key = request.args.get('key')
    
    if user_key == ADMIN_ACCESS_KEY:
        # Calculate pulse counters dynamically
        counts = {k: len(v) for k, v in feedback_storage.items()}
        return render_template('admin.html', storage=feedback_storage, counts=counts)
    else:
        # Unauthorized access attempt
        flash("Access Denied: Invalid Security Key.", "error")
        return redirect(url_for('index'))

@app.route('/download-report')
def download_report():
    user_key = request.args.get('key')
    if user_key != ADMIN_ACCESS_KEY:
        return redirect(url_for('index'))

    # Build the official text report
    report = "OFFICIAL SCI FEEDBACK REPORT - MAMA SCI 2026\n"
    report += "="*50 + "\n\n"
    
    for category, messages in feedback_storage.items():
        report += f"[{category.upper()} LOUNGE]\n"
        if not messages:
            report += "No entries recorded.\n"
        for i, msg in enumerate(messages, 1):
            report += f"{i}. {msg}\n"
        report += "\n"

    return Response(
        report,
        mimetype="text/plain",
        headers={"Content-disposition": "attachment; filename=SCI_Feedback_Report.txt"}
    )
@app.route('/clear-inbox')
def clear_inbox():
    user_key = request.args.get('key')
    if user_key == ADMIN_ACCESS_KEY:
        # Purge all data from memory
        for key in feedback_storage:
            feedback_storage[key] = []
        flash("System Purge Complete. All records cleared. 🧹", "success")
        return redirect(url_for('admin_view', key=ADMIN_ACCESS_KEY))
    
    return redirect(url_for('index'))

# --- SERVER BOOT ---
if __name__ == '__main__':
    # Running in Debug mode for development
    app.run(debug=True, port=5000)