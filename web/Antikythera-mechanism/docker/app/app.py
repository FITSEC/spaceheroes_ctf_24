from flask import Flask,request, render_template,render_template_string

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form.get('date')
        for forbidden_string in ["__class__", "/dev/tcp", "nc", "netcat"]:
            if forbidden_string in date:
                return "Invalid characters detected in date input."
            else:
                template = 'Entered Date: ' + date + '\n\n'
                result = render_template_string(template, date=date)
                return result 
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()

