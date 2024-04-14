from flask import Flask, render_template, send_from_directory, request, abort, jsonify
import secrets

app = Flask(__name__)

# Generate a random session token
session_token = secrets.token_hex(16)

# Your existing routes
@app.route('/')
def home():
    return render_template('sd.html')

@app.route('/SMALL_THOUGHTS.html')
def small_thoughts():
    return render_template('SMALL_THOUGHTS.html')

@app.route('/abit.html')
def abit_worried():
    return render_template('abit.html', session_token=session_token)

@app.route('/getto.html')
def getto():
    return render_template('getto.html')

@app.route('/style.css')
def style():
    return app.send_static_file('style.css')

@app.route('/text/<path:filename>')
def text_file(filename):
    try:
        return send_from_directory('text', filename)
    except FileNotFoundError:
        return "File not found."

# Check referrer for sensitive URLs
def check_referrer():
    if not request.referrer or not request.referrer.startswith(request.url_root):
        abort(403, "You don't have the permission to access the requested resource. URL root does not match /abit.html.")  # Forbidden if referrer is not from the same domain

# Check if the request is from curl for flag.txt
def check_flag_curl():
    user_agent = request.headers.get('User-Agent')
    if user_agent and 'curl' in user_agent.lower() and 'flag.txt' in request.path:
        abort(403, "You don't have the permission to access the requested resource. I know you invaders all too well. My secrets are mine alone.")  # Forbidden if request is from curl for flag.txt

@app.route('/text/credentials/<path:filename>')
def user_credentials(filename):
    check_referrer()
    try:
        return send_from_directory('text/credentials', filename)
    except FileNotFoundError:
        return "File not found."

@app.route('/text/secret/flag.txt')
def secret_flag():
    check_referrer()
    check_flag_curl()
    try:
        return send_from_directory('text/secret', 'flag.txt')
    except FileNotFoundError:
        return "File not found."

# Endpoint to provide session token to the client
@app.route('/get-session-token')
def get_session_token():
    return jsonify({'token': session_token})

@app.route('/interpretations')
def interpretations():
    return render_template('interpretations.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
