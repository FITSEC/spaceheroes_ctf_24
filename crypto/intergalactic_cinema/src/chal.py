from flask import Flask, send_file, request, redirect, url_for
import string
import random
import sys
import base64
import bcrypt

app = Flask(__name__)

# Define the combined_array and shifted_array
combined_array = list(string.ascii_lowercase + string.digits)
shifted_array = combined_array[:]
random.shuffle(shifted_array)

# Initialize a dictionary to store user input values
user_input_values = {char: char for char in combined_array}

# Encrypt plaintext.txt and store in encrypted.txt
def encrypt_plain():
    with open('plaintext.txt', 'r') as file, open('encrypted.txt', 'w') as out:
        for line in file:
            for char in line:
                shifted_char = shifted_array[combined_array.index(char)] if char in combined_array else char
                out.write(shifted_char)

# Function to update encrypted.txt with user input
def update_encrypted_text(new_mapping):
    with open('encrypted.txt', 'r') as file:
        encrypted_text = file.read()
    updated_text = ''.join(new_mapping.get(char, char) for char in encrypted_text)
    with open('update.txt', 'w') as file:
        file.write(updated_text)

@app.route('/')
def index():
    # Ensure encrypted text is up to date
    encrypt_plain()
    
    # Read encrypted text
    with open('encrypted.txt', 'r') as file:
        encrypted_text = file.read()
    
    # Generate the HTML for the character mapping table
    table_html = '<table>'
    for i, char in enumerate(combined_array):
        if i % 4 == 0:
            table_html += '<tr>'
        # Populate the input fields with previously entered values
        table_html += f'<td>{char}</td><td><input type="text" name="{char}" value="{user_input_values[char]}" maxlength="1"></td>'
        if i % 4 == 3:
            table_html += '</tr>'
    table_html += '</table>'
    
    # Render the updated encrypted text if available
    updated_text = request.args.get('updated_text', '')
    updated_encrypted_text = ''
    if updated_text:
        with open('update.txt', 'r') as file:
            updated_encrypted_text = file.read()
    
    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Encrypted Text</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #3b3a3a;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }}
        .container {{
            max-width: 900px;
            width: 90%;
            background-color: #ededed;
            padding: 40px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            background-image: linear-gradient(to right, #7300ff 2%, #00fbff 98%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-align:center;
        }}
        p {{
            color: black;
        }}
        a {{
            background: linear-gradient(to left, 
            violet, indigo, blue, green, yellow, orange, red);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-decoration: underline;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .scrollable-box {{
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            margin-top: 20px;
        }}
        table {{
            margin-top: 20px;
        }}
        table td {{
            padding: 5px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Intergalactic Cinema</h1>
        <p>I was partaking in a fun viewing of some show/movie with my alien bros but couldn't understand anything due to the alien voice dubbing present in the movie.</p>
        <p>I've managed to download a script of what was said during the viewing but it seems to be encrypted, can you help me decrypt it? I've attached a tool to this message that may help you.</p>
        <p><b>Here's what I've found: <a href="/download">download</a></b></p>
        <p>P.S. One of my alien friends who loves this movie told me one of the lines was changed to a CTF flag due to interplanetary laws against quotes that are really cool. Whatever that means.</p>
        <p>Contents of <b>encrypted.txt:</b></p>
        <div class="scrollable-box">
            <pre>{encrypted_text}</pre>
        </div>
        <form method="post" action="/update">
            {table_html}
            <input type="submit" value="Submit">
        </form>
        <p><b>{updated_text}</b></p>
        <div class="scrollable-box">
            <pre>{updated_encrypted_text}</pre>
        </div>
        <p>If you'd like I can ask my alien friend Fletcher to check the flag for you, just send it my way</p>
        <form method="post" action="/check_flag" onsubmit="submitFlag(event)">
            <input type="text" name="flag_input" id="flagInput" placeholder="Enter flag here">
            <input type="submit" value="Submit Flag">
        </form>
        <div class="result-message" id="resultMessage"></div>
    </div>
    <script>
        function submitFlag(event) {{
            event.preventDefault();
            var flagInput = document.getElementById('flagInput').value;
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/check_flag', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onreadystatechange = function() {{
                if (xhr.readyState === 4 && xhr.status === 200) {{
                    document.getElementById('resultMessage').innerHTML = xhr.responseText;
                }}
            }};
            xhr.send('flag_input=' + encodeURIComponent(flagInput));
        }}
    </script>
</body>
</html>
'''

@app.route('/download')
def download_file():
    return send_file('encrypted.txt', as_attachment=True)

@app.route('/update', methods=['POST'])
def update_mapping():
    new_mapping = {}
    for char in combined_array:
        new_mapping[char] = request.form[char]
        # Update user input values dictionary
        user_input_values[char] = new_mapping[char]
    
    # Update the encrypted text with the new mapping
    update_encrypted_text(new_mapping)
    
    # Redirect to the index page with the updated text
    return redirect(url_for('index', updated_text='Updated Encrypted Text:'))

@app.route('/check_flag', methods=['POST'])
def check_flag():
    flag_input = request.form['flag_input']
    if bcrypt.checkpw(flag_input.encode('utf-8'), b'$2b$12$KwrMBJLJrxPJZiIIfma.O.ODon/bCd5zqLW9ABbRkRXj98HCyQy5W'):
        return "</br>In Whiplash (2014) Fletcher forces Neiman to count off 215 BPM, then insults him for getting it wrong. However, Neiman’s timing is actually perfect. It’s an early clue that Fletcher is playing a twisted game with Neiman to try and turn him into the best musician in the entire universe.</br></br>The entered flag is correct. Congratulations!"
    else:
        return "</br>\"Not quite my tempo.\"</br></br>The entered flag is incorrect."

if __name__ == '__main__':
    ip = '127.0.0.1'  # Default IP address
    port = 5000  # Default port
    for arg in sys.argv[1:]:
        if arg.startswith('IP='):
            ip = arg.split('=')[1]
        elif arg.startswith('PORT='):
            port = int(arg.split('=')[1])
    app.run(debug=True, host=ip, port=port)
